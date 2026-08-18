"""Merge RootsMagic FamilyTable rows that have identical parents.

The lowest FamilyID in each duplicate parent pair is retained.  Links to the
other rows are redirected before those rows are deleted.  Run on a closed copy
of the RootsMagic database.  The default is a report-only dry run.
"""

import argparse
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


FAMILY_OWNER_TYPE = 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('database', type=Path,
                        help='Path to the closed .rmtree database')
    parser.add_argument(
        '--apply', action='store_true', help='Create a backup and perform the merge'
    )
    arguments = parser.parse_args()

    if not arguments.database.is_file():
        raise SystemExit(f"Database not found: {arguments.database}")

    connection = sqlite3.connect(arguments.database)
    try:
        groups = duplicate_family_groups(connection)
        if not groups:
            print('No duplicate FamilyTable parent pairs found.')
            return

        report_groups(groups)
        if not arguments.apply:
            print(
                '\nDry run only. Re-run with --apply to create a backup and merge these records.')
            return

        backup_path = create_backup(arguments.database)
        removed_ids = duplicate_family_ids(groups)
        changed = []
        with connection:
            for _father_id, _mother_id, keep_id, family_ids, _record_count in groups:
                for family_id in family_ids.split(','):
                    old_family_id = int(family_id)
                    if old_family_id != keep_id:
                        changed.extend(
                            family_reference_updates(
                                connection, old_family_id, keep_id)
                        )

            unresolved = remaining_references(connection, removed_ids)
            if unresolved:
                raise RuntimeError(
                    f"References remain after redirect: {unresolved}")

            placeholders = ', '.join('?' for _ in removed_ids)
            connection.execute(
                f"DELETE FROM FamilyTable WHERE FamilyID IN ({placeholders})", removed_ids
            )

        print(f"Backup created: {backup_path}")
        print(f"Deleted {len(removed_ids)} duplicate FamilyTable rows.")
        for table_name, column_name, row_count in changed:
            print(f"Redirected {row_count} row(s): {table_name}.{column_name}")
    finally:
        connection.close()


def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def table_columns(connection, table_name):
    statement = f"PRAGMA table_info({quote_identifier(table_name)})"
    return {row[1] for row in connection.execute(statement)}


def database_tables(connection):
    return [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )
    ]


def duplicate_family_groups(connection):
    return connection.execute(
        """
        SELECT FatherID, MotherID, MIN(FamilyID) AS KeepFamilyID,
               GROUP_CONCAT(FamilyID) AS FamilyIDs, COUNT(*) AS RecordCount
          FROM FamilyTable
         GROUP BY FatherID, MotherID
        HAVING COUNT(*) > 1
         ORDER BY KeepFamilyID
        """
    ).fetchall()


def duplicate_family_ids(groups):
    return [
        int(family_id)
        for _father_id, _mother_id, keep_id, family_ids, _count in groups
        for family_id in family_ids.split(',')
        if int(family_id) != keep_id
    ]


def count_rows(connection, table_name, where_clause, parameters):
    statement = (
        f"SELECT COUNT(*) FROM {quote_identifier(table_name)} "
        f"WHERE {where_clause}"
    )
    return connection.execute(statement, parameters).fetchone()[0]


def family_reference_updates(connection, old_family_id, keep_family_id):
    """Redirect every known and schema-discoverable family reference."""
    updates = []
    tables = database_tables(connection)

    # Any current or future table with a concrete FamilyID column.
    for table_name in tables:
        if table_name == 'FamilyTable':
            continue
        columns = table_columns(connection, table_name)
        if 'FamilyID' in columns:
            updates.append((table_name, 'FamilyID', None))

    # ParentID stores a person's selected parent family.
    if 'PersonTable' in tables and 'ParentID' in table_columns(connection, 'PersonTable'):
        updates.append(('PersonTable', 'ParentID', None))

    # OwnerID is a polymorphic key.  OwnerType 1 is FamilyTable.FamilyID.
    for table_name in tables:
        columns = table_columns(connection, table_name)
        if {'OwnerType', 'OwnerID'} <= columns:
            updates.append((table_name, 'OwnerID', 'OwnerType'))

    # RootsMagic's online-tree links use the same family type value.
    for table_name in tables:
        columns = table_columns(connection, table_name)
        if {'LinkType', 'rmID'} <= columns:
            updates.append((table_name, 'rmID', 'LinkType'))

    changed = []
    seen = set()
    for table_name, id_column, type_column in updates:
        update_key = (table_name, id_column, type_column)
        if update_key in seen:
            continue
        seen.add(update_key)

        where_clause = f"{quote_identifier(id_column)} = ?"
        parameters = [old_family_id]
        if type_column is not None:
            where_clause += f" AND {quote_identifier(type_column)} = ?"
            parameters.append(FAMILY_OWNER_TYPE)

        row_count = count_rows(connection, table_name,
                               where_clause, parameters)
        if row_count:
            statement = (
                f"UPDATE {quote_identifier(table_name)} "
                f"SET {quote_identifier(id_column)} = ? WHERE {where_clause}"
            )
            connection.execute(statement, [keep_family_id, *parameters])
            changed.append((table_name, id_column, row_count))
    return changed


def remaining_references(connection, removed_family_ids):
    """Return references that should have been redirected by this utility."""
    if not removed_family_ids:
        return []

    placeholders = ', '.join('?' for _ in removed_family_ids)
    references = []
    tables = database_tables(connection)
    for table_name in tables:
        if table_name == 'FamilyTable':
            continue
        columns = table_columns(connection, table_name)

        checks = []
        if 'FamilyID' in columns:
            checks.append(('FamilyID', None))
        if table_name == 'PersonTable' and 'ParentID' in columns:
            checks.append(('ParentID', None))
        if {'OwnerType', 'OwnerID'} <= columns:
            checks.append(('OwnerID', 'OwnerType'))
        if {'LinkType', 'rmID'} <= columns:
            checks.append(('rmID', 'LinkType'))

        for id_column, type_column in checks:
            where_clause = f"{quote_identifier(id_column)} IN ({placeholders})"
            parameters = list(removed_family_ids)
            if type_column is not None:
                where_clause += f" AND {quote_identifier(type_column)} = ?"
                parameters.append(FAMILY_OWNER_TYPE)
            row_count = count_rows(
                connection, table_name, where_clause, parameters)
            if row_count:
                references.append((table_name, id_column, row_count))
    return references


def create_backup(database_path):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    backup_path = database_path.with_name(
        f"{database_path.stem}-before-family-merge-{timestamp}{database_path.suffix}"
    )
    shutil.copy2(database_path, backup_path)
    return backup_path


def report_groups(groups):
    for father_id, mother_id, keep_id, family_ids, record_count in groups:
        print(
            f"FatherID={father_id}, MotherID={mother_id}: "
            f"keep FamilyID {keep_id}; merge [{family_ids}] ({record_count} rows)"
        )


if __name__ == '__main__':
    main()
