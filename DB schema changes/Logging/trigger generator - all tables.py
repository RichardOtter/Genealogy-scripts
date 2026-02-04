import sqlite3

DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\DB\TEST-DB schema changes.rmtree"          # <-- update
LOG_table = "AuxChangeLogTable"   # <-- update
file_path_create = f"DB Schema changes/Logging/generated/_logging_trigger_full.sql"
file_path_drop = f"DB Schema changes/Logging/generated/_logging_trigger_drop.sql"
output_file_trigger = open(file_path_create,  mode='w', encoding='utf-8')
output_file_drop_trigger = open(file_path_drop,  mode='w', encoding='utf-8')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

tables = [
    row[0]
    for row in cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
          AND name NOT LIKE 'sqlite_%'
    """)
]

for table in tables:
    if table in ("AuxChangeLog", "AuxChangeLogTable", "AddressLinkTable", 
                 "AddressTable", "AncestryTable", "FamilySearchTable",
                 "HealthTable", "AuxCitationLinkTable"):
        continue    # don't log this table

    trigger_name = f"{table}_{LOG_table}_update"

    # Load columns except PK of BLOB types
    cur.execute(f"PRAGMA table_info({table})")
    cols=[]
    for row in cur.fetchall():
      if row[5] == 1:
          pk= row[1]
      else:
        if row[2] != "BLOB":
            cols.append(row[1])
        else:
            continue  # BLOBs cannot go into JSON

    col_lines = []
    for col in cols:
        col_lines.append(
            f"      '{col}',  CASE WHEN OLD.{col}  IS DISTINCT FROM NEW.{col}   THEN json_object( 'old',OLD.{col},  'new',NEW.{col})   END,"
            )

    # Remove trailing comma
    col_lines[-1] = col_lines[-1].rstrip(',')

    # Build the trigger
    trigger = f"""
    CREATE TRIGGER {trigger_name}
    AFTER UPDATE ON {table}
    FOR EACH ROW
    BEGIN
      INSERT INTO {LOG_table} (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            '{table}',
            OLD.{pk},
            julianday('now') - 2415018.5,
            json_patch('{{}}', json_object(
"""

    # Add column specific lines
    for p in col_lines:
        trigger += f"        {p}\n"

    trigger += """    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    \n\n\n
    """

    output_file_trigger.write(trigger)

    drop_sql =  f"DROP TRIGGER IF EXISTS {trigger_name}; "
    output_file_drop_trigger.write(drop_sql +"\n\n")


output_file_trigger.close()
output_file_drop_trigger.close()


