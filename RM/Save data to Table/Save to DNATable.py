import sys
from pathlib import Path
sys.path.append(str(Path.resolve(Path.cwd() / r'..\RMpy package')))

import RMpy.common as RMc       # noqa #type: ignore
import RMpy.launcher            # noqa #type: ignore
from RMpy.common import q_str   # noqa #type: ignore
import RMpy.RMDate        # noqa #type: ignore


# ===================================================DIV60==
#  Global Variables
G_DEBUG = False


# ================================================================
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"] = "Insert_Data"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"] = Path(__file__).parent
    utility_info["run_features_function"] = parse_insert_data
    utility_info["allow_db_changes"] = True
    utility_info["RMNOCASE_required"] = False
    utility_info["RegExp_required"] = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def parse_insert_data(config, db_connection, report_file):

    # open the text file- read only
    # read each section delimited with empty line
    # each section is either 3 or 4 lines

    filename = r"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts\RM\Save data to Table\WORKING Page copy and paste GCS 2025-03-23.txt"
#    with open file
#
    insert_data(config, db_connection, report_file)


# ===================================================DIV60==
def insert_data(config, db_connection, report_file):

# the ddl to create the DNATable

# CREATE TABLE DNATable (RecID INTEGER PRIMARY KEY, ID1 INTEGER, ID2 INTEGER, Label1 TEXT, Label2 TEXT, DNAProvider INTEGER, SharedCM FLOAT, SharedPercent FLOAT, LargeSeg FLOAT, SharedSegs INTEGER, Date TEXT, Relate1 INTEGER, Relate2 INTEGER, CommonAnc INTEGER, CommonAncType INTEGER, Verified INTEGER, Note TEXT, UTCModDate FLOAT )

# not RMNOCASE indexed
    SQL_statement= """
INSERT INTO DNATable
(
ID1,
ID2,
Label1,
Label2,
DNAProvider,
SharedCM,
SharedPercent,
LargeSeg,
SharedSegs,
Date,
Relate1,
Relate2,
CommonAnc,
CommonAncType,
Verified,
Note,
UTCModDate)

VALUES(
:ID1,
:ID2,
:Label1,
:Label2,
:DNAProvider,
:SharedCM,
:SharedPercent,
:LargeSeg,
:SharedSegs,
:Date,
:Relate1,
:Relate2,
:CommonAnc,
:CommonAncType,
:Verified,
:Note,
julianday('now') - 2415018.5
);
"""

    label2 = 'test label2'
    SharedPercent = .23
    SharedSegs = 2
    Note = """test note line 1
test note line 2
test note line 3
"""

    print(RMpy.RMDate.now_RMDate())

    match_data= {
        'ID1': 1,
        'ID2': 17132,
        'Label1': 'Richard J Otter',
        'Label2': label2,
        'DNAProvider': 1,
        'SharedCM': 0,
        'SharedPercent': SharedPercent,
        'LargeSeg': 0,
        'SharedSegs': SharedSegs,
        'Date': RMpy.RMDate.now_RMDate(),
        'Relate1': 0,
        'Relate2': 0,
        'CommonAnc': 0,
        'CommonAncType': 0,
        'Verified': 0,
        'Note': Note
        }

    cur = db_connection.cursor()

    cur.execute(SQL_statement, match_data)






# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
