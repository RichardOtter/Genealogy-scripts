import sqlite3


DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\DB\TEST-DB schema changes.rmtree"          # <-- update
LOG_table = "AuxChangeLog"   # <-- update

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
   
    # Load columns except PK
    cur.execute(f"PRAGMA table_info({table})")
    cols=[]
    for row in cur.fetchall():
      if row[5] == 1:
          pk= row[1]
      else:
          cols.append(row[1])


    col_lines = []
    for col in cols:
        col_lines.append(
            f"      '{col}',  CASE WHEN OLD.{col}  IS DISTINCT FROM NEW.{col}   THEN json_object( 'old',OLD.{col},  'new',NEW.{col})   END,"
            )

    # FIX: last line must NOT end with a comma, and must close all json_patch(
    # Remove trailing comma
    col_lines[-1] = col_lines[-1].rstrip(',')

    # for p in patches:
    #     print(p, "\n")
    # print("\n\n\n")


    # Build the trigger
    trigger = f"""
    CREATE TRIGGER {table}_AuxLogUpdate
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

    # Add json_patch lines
    for p in col_lines:
        trigger += f"        {p}\n"

    trigger += """    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    """

    file_path = f"DB Schema changes/Logging/generated/logging_trigger_{table}__full.sql"
    output_file = open(file_path,  mode='w', encoding='utf-8')
    output_file.write(trigger)
    output_file.close()



