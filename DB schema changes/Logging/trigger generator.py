import sqlite3


DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\DB\TEST-DB schema changes.rmtree"          # <-- update
TABLE = "NameTable"         # <-- update
PK_COL = "NameID"           # <-- update
LOG_TABLE = "AuxChangeLog"   # <-- update

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Load columns except PK
cur.execute(f"PRAGMA table_info({TABLE})")
cols = [row[1] for row in cur.fetchall() if row[1] != PK_COL]

# Build CASE expressions wrapped in json_patch(
patches = []
for col in cols:
    patches.append(
        f"'{col}',  CASE WHEN OLD.{col}  IS DISTINCT FROM NEW.{col}   THEN json_object( 'old',OLD.{col},  'new',NEW.{col})   END,"
        )

# FIX: last line must NOT end with a comma, and must close all json_patch(
# Remove trailing comma
patches[-1] = patches[-1].rstrip(',')

# for p in patches:
#     print(p, "\n")
# print("\n\n\n")


# Build the trigger
trigger = f"""
CREATE TRIGGER {TABLE}_AuxLogUpdate
AFTER UPDATE ON {TABLE}
FOR EACH ROW
BEGIN
  INSERT INTO {LOG_TABLE} (TableName, RowID, ChangeTime, ChangesJSON)
  SELECT *
    FROM (
      SELECT
        '{TABLE}',
        OLD.{PK_COL},
        julianday('now') - 2415018.5,
        json_patch('{{}}', json_object(
        {patches[0]}
"""

# Add remaining json_patch lines
for p in patches[1:]:
    trigger += f"        {p}\n"

trigger += """    ) ) AS DIFF
    ) AS t
    WHERE t.diff IS NOT NULL
      AND t.diff <> '{}';
END;
"""

file_path = f"DB Schema changes/Logging/logging_trigger_{TABLE}__full.sql"
output_file = open(file_path,  mode='w', encoding='utf-8')
output_file.write(trigger)
output_file.close()


