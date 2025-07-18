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

    filepath = r"TestData\test input.txt"
    
    entries= parse_grouped_file(filepath)

    try:
        for entry in entries:
            Note = ""
            for line in entry:
                Note= Note + line + '\n'
            label2 = entry[0]
            SharedPercent = float( (entry[2])[0 : (entry[2]).find('%')])
            SharedSegs = int( (entry[2])[(entry[2]).find('shared,') + 7 : (entry[2]).find('segments')    ])
            insert_data(label2, SharedPercent, SharedSegs, Note, config, db_connection, report_file)
    except Exception as e:
        print (e, entry)

# ===================================================DIV60==
def parse_grouped_file(filepath):
    try:
        with open(filepath,  mode='r', encoding='utf-8') as input_file:
            content = input_file.read()
            # Split the content by two or more consecutive newline characters
            # to handle both single and multiple blank lines as separators.
            groups_raw = content.split('\n\n')

            parsed_groups = []
            for group_str in groups_raw:
                # Remove leading/trailing whitespace and split into individual lines
                lines = [line.strip() for line in group_str.split('\n') if line.strip()]
                if lines:  # Only add non-empty groups
                    parsed_groups.append(lines)
            return parsed_groups
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# ===================================================DIV60==
def insert_data(label2, SharedPercent, SharedSegs, Note, config, db_connection, report_file):

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

# TODO  different for most runs
# some items are constant, some are calculated, others are from input file
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
