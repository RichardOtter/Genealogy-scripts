"""Normalize line endings in every Note column across all RootsMagic tables.

Every TEXT column named "Note" (case-insensitive) in every table is scanned.
Line endings are rewritten to the style selected by EOL_STYLE in
RM-Python-config.ini ("LF" for \\n or "CRLF" for \\r\\n).  Set
MAKE_CHANGES = true to apply the changes; the default is a report-only dry run.
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
#   RootsMagic database file v10
#   Python for Windows v3.13

# Config file fields used
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#
#    OPTIONS     EOL_STYLE
#    OPTIONS     MAKE_CHANGES


# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"] = "NormalizeNoteLineEndings"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"] = Path(__file__).parent
    utility_info["run_features_function"] = run_selected_features
    utility_info["allow_db_changes"] = True
    utility_info["RMNOCASE_required"] = False
    utility_info["RMNOCASE_optional"] = False
    utility_info["RegExp_required"] = False
    utility_info["RegExp_optional"] = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    try:
        eol_style = config['OPTIONS'].get('EOL_STYLE').strip().upper()
    except:
        raise RMc.RM_Py_Exception(
            'ERROR: section: [OPTIONS], key: EOL_STYLE must be specified.\n')
    if eol_style not in ('LF', 'CRLF'):
        raise RMc.RM_Py_Exception(
            F'ERROR: EOL_STYLE must be LF or CRLF, found: {RMc.q_str(eol_style)}\n')
    new_eol = '\n' if eol_style == 'LF' else '\r\n'

    try:
        make_changes = config['OPTIONS'].getboolean('MAKE_CHANGES')
    except:
        raise RMc.RM_Py_Exception(
            'ERROR: section: [OPTIONS], key: MAKE_CHANGES could not be parsed as boolean.\n')

    report_file.write(F"Target line ending: {eol_style}\n\n")

    total_rows_changed = 0
    for table_name, column_name in note_columns(db_connection):
        rows_changed = normalize_column(
            db_connection, table_name, column_name, new_eol, make_changes, report_file)
        total_rows_changed += rows_changed

    report_file.write(
        F"\n{'Would change' if not make_changes else 'Changed'}"
        F" {total_rows_changed} row(s) in total.\n")
    if not make_changes:
        report_file.write(
            '\nDry run only. Set MAKE_CHANGES = true in the configuration'
            ' file to apply these changes.\n')
    return


# ===================================================DIV60==
def note_columns(connection):
    """Yield (table_name, column_name) for every Note-like column in the database."""
    tables = [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )
    ]
    for table_name in tables:
        for column in connection.execute(F'PRAGMA table_info({quote_identifier(table_name)})'):
            column_name = column[1]
            if column_name.upper() == 'NOTE':
                yield table_name, column_name


# ===================================================DIV60==
def normalize_column(connection, table_name, column_name, new_eol, make_changes, report_file):

    quoted_table = quote_identifier(table_name)
    quoted_column = quote_identifier(column_name)
    key_column = primary_key_column(connection, table_name)
    quoted_key = quote_identifier(key_column)

    statement = (
        F"SELECT {quoted_key}, {quoted_column} FROM {quoted_table} "
        F"WHERE {quoted_column} IS NOT NULL"
    )
    updates = [
        (row_id, normalized_text)
        for row_id, note_text in connection.execute(statement)
        for normalized_text in [normalize_line_endings(note_text, new_eol)]
        if normalized_text != note_text
    ]

    if updates:
        report_file.write(
            F"{table_name}.{column_name}: {len(updates)} row(s) need normalization.\n")

    if make_changes and updates:
        update_statement = (
            F"UPDATE {quoted_table} SET {quoted_column} = ? WHERE {quoted_key} = ?"
        )
        connection.executemany(
            update_statement, [(text, row_id) for row_id, text in updates])

    return len(updates)


# ===================================================DIV60==
def normalize_line_endings(text, new_eol):
    # Collapse any mix of \r\n, bare \r, or \n to a single style.
    unified = text.replace('\r\n', '\n').replace('\r', '\n')
    return unified.replace('\n', new_eol)


# ===================================================DIV60==
def primary_key_column(connection, table_name):
    for column in connection.execute(F'PRAGMA table_info({quote_identifier(table_name)})'):
        # column tuple: (cid, name, type, notnull, dflt_value, pk)
        if column[5] == 1:
            return column[1]
    raise RMc.RM_Py_Exception(
        F'ERROR: table {RMc.q_str(table_name)} has no single-column primary key.\n')


# ===================================================DIV60==
def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


if __name__ == '__main__':
    main()
