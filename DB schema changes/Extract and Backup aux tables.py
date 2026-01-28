import sqlite3
from pathlib import Path
from datetime import datetime


# Handles tables:       confirm TODO
#   AuxDNATable
#   AuxMediaTable
#   AuxCitationLinkTable

# ===================================================DIV60==
def main():

    TIMESTAMP = time_stamp_now("file")

    new_db_folder = Path(r"E:\Users Overflow\ROtter external\Genealogy\Generated Output\AuxTable Extracted")
    new_db_filename = "RMDataExtra-" + TIMESTAMP + ".sqlite"
    new_db_file_path = new_db_folder / new_db_filename

    production_db_folder = Path(r"C:\Users\rotter\Genealogy\GeneDB")
    production_db_filename = "Otter-Saito.rmtree"
    production_db_file_path = production_db_folder / production_db_filename

    # Create the backup DB
    conn = sqlite3.connect(new_db_file_path)
    conn.close()

    # Open the production DB
    conn = sqlite3.connect(production_db_file_path)

    # Create a cursor and a sample table
    cursor = conn.cursor()

    cursor.execute('''
ATTACH DATABASE ?
AS adf;  -- auxiliary data file
''', (str(new_db_file_path),))

    cursor.execute('''
--  does not create constraints on the table copies
CREATE TABLE adf.AuxDNATable AS SELECT * FROM AuxDNATable;
''')

    cursor.execute('''
--  does not create constraints on the table copies
CREATE TABLE adf.AuxMultimediaTable AS SELECT * FROM AuxMultimediaTable;
''')

    cursor.execute('''
--  does not create constraints on the table copies
CREATE TABLE adf.AuxCitationLinkTable AS SELECT * FROM AuxCitationLinkTable;
''')

    conn.commit()
    conn.close()


# ===================================================DIV60==
def time_stamp_now(type=None):

    # return a TimeStamp string
    now = datetime.now()
    if type is None:
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
