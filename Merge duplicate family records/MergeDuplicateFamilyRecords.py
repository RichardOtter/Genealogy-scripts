"""Merge RootsMagic FamilyTable rows that have identical parents.

The lowest FamilyID in each duplicate parent pair is retained.  Links to the
other rows are redirected before those rows are deleted.  Run on a closed copy
of the RootsMagic database.
"""

import sys
from pathlib import Path
sys.path.append(
    str(Path.resolve(Path(__file__).resolve().parent / '../RMpy package')))

import RMpy.launcher            # noqa #type: ignore
import RMpy.common as RMc       # noqa #type: ignore

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v11
#   Python for Windows v3.14

# Config file fields used
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP

# The polymorphic owner identifier
FAMILY_OWNER_TYPE = 1

# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"] = "MergeDuplicateFamilyRecords"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"] = Path(__file__).parent
    utility_info["run_features_function"] = merge_records
    utility_info["allow_db_changes"] = True
    utility_info["RMNOCASE_required"] = False
    utility_info["RMNOCASE_optional"] = False
    utility_info["RegExp_required"] = False
    utility_info["RegExp_optional"] = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def merge_records(config, db_connection, report_file):

    groups = duplicate_family_groups(db_connection)
    if not groups:
        report_file.write('No duplicate FamilyTable parent pairs found.\n')
        return

    report_groups(report_file, groups)

    removed_ids = duplicate_family_ids(groups)
    changed = []
    for _father_id, _mother_id, keep_id, family_ids, _record_count in groups:
        for family_id in family_ids.split(','):
            old_family_id = int(family_id)
            if old_family_id != keep_id:
                changed.extend(
                    family_reference_updates(
                        db_connection, old_family_id, keep_id)
                )

    unresolved = remaining_references(db_connection, removed_ids)
    if unresolved:
        raise RMc.RM_Py_Exception(
            F"ERROR: References remain after redirect: {unresolved}")

    placeholders = ', '.join('?' for _ in removed_ids)
    db_connection.execute(
        f"DELETE FROM FamilyTable WHERE FamilyID IN ({placeholders})", removed_ids
    )

    report_file.write(
        F"\nDeleted {len(removed_ids)} duplicate FamilyTable rows.\n")
    for action, table_name, column_name, row_count in changed:
        report_file.write(
            F"{action} {row_count} row(s): "
            F"{table_name}.{column_name}\n")
    return


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


def child_reference_updates(connection, old_family_id, keep_family_id):
    if 'ChildTable' not in database_tables(connection):
        return []

    child_rows = connection.execute(
        "SELECT RecID, ChildID FROM ChildTable WHERE FamilyID = ?",
        (old_family_id,),
    ).fetchall()
    redirected = 0
    removed = 0

    for old_rec_id, child_id in child_rows:
        retained_row = connection.execute(
            "SELECT RecID FROM ChildTable "
            "WHERE FamilyID = ? AND ChildID = ? LIMIT 1",
            (keep_family_id, child_id),
        ).fetchone()
        if retained_row is None:
            connection.execute(
                "UPDATE ChildTable SET FamilyID = ? WHERE RecID = ?",
                (keep_family_id, old_rec_id),
            )
            redirected += 1
        else:
            connection.execute(
                "DELETE FROM ChildTable WHERE RecID = ?",
                (old_rec_id,),
            )
            removed += 1

    changed = []
    if redirected:
        changed.append(('Redirected', 'ChildTable', 'FamilyID', redirected))
    if removed:
        changed.append(
            ('Removed duplicate', 'ChildTable', 'FamilyID', removed))
    return changed


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
    if 'PersonTable' in tables and 'SpouseID' in table_columns(connection, 'PersonTable'):
        updates.append(('PersonTable', 'SpouseID', None))

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
    changed.extend(
        child_reference_updates(connection, old_family_id, keep_family_id)
    )
    seen = set()
    for table_name, id_column, type_column in updates:
        if table_name == 'ChildTable':
            continue
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
            changed.append(('Redirected', table_name, id_column, row_count))
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
        if table_name == 'PersonTable' and 'SpouseID' in columns:
            checks.append(('SpouseID', None))
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


def report_groups(report_file, groups):
    for father_id, mother_id, keep_id, family_ids, record_count in groups:
        report_file.write(
            f"FatherID={father_id}, MotherID={mother_id}: "
            f"keep FamilyID {keep_id}; merge [{family_ids}] ({record_count} rows)\n"
        )


if __name__ == '__main__':
    main()
