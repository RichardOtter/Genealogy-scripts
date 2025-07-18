import sys
from pathlib import Path
sys.path.append(str(Path.resolve(Path.cwd() / r'..\RMpy package')))

import RMpy.common as RMc       # noqa #type: ignore
import RMpy.launcher            # noqa #type: ignore
from RMpy.common import q_str   # noqa #type: ignore

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.13

# Config files fields used
#    [FILE_PATHS]  DB_PATH
#    [FILE_PATHS]  REPORT_FILE_PATH
#    [FILE_PATHS]  REPORT_FILE_DISPLAY_APP
#    [OPTIONS]     COLOR_COMMAND
#  note: COLOR_COMMAND may be a single name or a list of names, one per line.
# name(s) refer to sections in the same config file that contain color coding instructions.

#  note:Section name is the same label as [OPTIONS] COLOR_COMMAND's value
#    [GROUP_NAME_Value]  ACTION   what to do
#    [GROUP_NAME_Value]  COLOR_CODE_SET   which set to modify
#    [GROUP_NAME_Value]  COLOR   which color to modify
#    [GROUP_NAME_Value]  GROUP   which group to use or _ALL when action is clear


# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"] = "ColorFromGroup"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"] = Path(__file__).parent
    utility_info["run_features_function"] = run_selected_features
    utility_info["allow_db_changes"] = True
    utility_info["RMNOCASE_required"] = False
    utility_info["RegExp_required"] = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    # this indirection is needed when util has several
    # features and user cna choose which to run
    color_from_group_feature(config, db_connection, report_file)


# ===================================================DIV60==
def color_from_group_feature(config, db_connection, report_file):

    # confirm config keys and sections
    try:
        color_cmd_name_list = config['OPTIONS'].get(
            'COLOR_COMMAND').split('\n')
    except:
        raise RMc.RM_Py_Exception(
            'section: [OPTIONS],  key: COLOR_COMMAND   not found.')

    # confirm that the corresponding sections exist
    for color_cmd_name in color_cmd_name_list:
        if color_cmd_name == '':
            continue
        try:
            config[color_cmd_name]
        except:
            raise RMc.RM_Py_Exception(
                F'section: [{q_str(color_cmd_name)}]   not found.')

    Divider = "="*50 + "===DIV60=="

    # iterate thru the color commands
    for color_cmd_name in color_cmd_name_list:
        if color_cmd_name == '':
            continue
        report_file.write(F"\n{Divider}\n")
        report_file.write(F"Run {color_cmd_name}\n")
        exec_color_cmd(db_connection, config, report_file, color_cmd_name)

    report_file.write(F"\n{Divider}\n")
    report_file.write("Last color command operation finished.")
    return


# ===================================================DIV60==
def exec_color_cmd(db_connection, config, report_file, color_cmd_section):

    # execute a color command set (named section in ini file)

    # validate the kes in the current section
    # get the raw values from config
    try:
        action = config[color_cmd_section].get('ACTION')
    except:
        raise RMc.RM_Py_Exception(
            F'section: [{color_cmd_section}],  key: ACTION    not found.')

    try:
        code_set = config[color_cmd_section].get('COLOR_CODE_SET')
    except:
        raise RMc.RM_Py_Exception(
            F'section: [{color_cmd_section}],  key: COLOR_CODE_SET    not found.')

    try:
        color_txt = config[color_cmd_section].get('COLOR')
    except:
        raise RMc.RM_Py_Exception(
            F'section: [{color_cmd_section}],  key: COLOR    not found.')

    try:
        group_name = config[color_cmd_section].get('GROUP')
    except:
        raise RMc.RM_Py_Exception(
            F'section: [{color_cmd_section}],  key: GROUP    not found.')

    # Validate the raw values

    # validate group_name
    if group_name == "_ALL":
        group_id = 0
    else:
        group_id = validate_DB_group_name(
            group_name, report_file, db_connection)
    # from this point further, group_id of 0 means use _ALL

    # validate action
    if (action != "set"
        and action != "clear"
        and action != "clearOnlyIf"
        and action != "clearAny"
        and action != "setOnlyIf"
            ):
        raise RMc.RM_Py_Exception(
            F'\n\n Section: [{color_cmd_section}],  key: ACTION {action}   is not supported.\n'
            "Allowed actions:\nset\nclearAny\nclearOnlyIf\nsetOnlyIf\n")

    # color_txt
    # for now, the color must be a number
    db_color_num = translate_ui_color_to_db(ui_number=int(color_txt))

    # code_set
    try:
        if (int(code_set) < 1 or int(code_set) > 10):
            raise RMc.RM_Py_Exception(
                F'section: [{color_cmd_section}],  key: COLOR_CODE_SET'
                F'{code_set}  is out of range.\nMust be in the range 1-10.')
    except TypeError:
        raise RMc.RM_Py_Exception(
            F'section: [{color_cmd_section}],  key: COLOR_CODE_SET'
            F'   must be an integer.')

    report_file.write(
        F'Parameters:\nACTION = {action}\nCOLOR_CODE_SET = {code_set}\n'
        F'COLOR = {color_txt}\nGROUP = {group_name}\n')

    update_people_colors(db_connection, group_id,
                         int(code_set), db_color_num, action)

    return


# ===================================================DIV60==
def update_people_colors(db_connection, group_id, color_group, db_color_num, action):

    # validate input which has not yet been checked
    if color_group < 1 or color_group > 10:
        raise RMc.RM_Py_Exception('color_group is out of range.')

    # Construct the SQL statement so correct color group column is updated
    # can't use a SQL variable, must use python string manipulation
    # because the column name to update is a variable. Would need to
    # use one of 10 SQL statements each with a different column name.

    # Columns in PersonTable are named: Color, Color1, Color2 ... Color9
    # prepare the string that will be concatenated to the word "Color"
    # to be used as column name

    column_num_str = str(color_group - 1)
    if color_group == 1:
        column_num_str = ''


    # keep this in reserve
    test_color_str = str(db_color_num)

    # For clear operations, the number to be set to is always 0
    if action == "set" or action == "setOnlyIf":
        color_str = str(db_color_num)
    else:
        color_str = str(0)

    # These are prototypes for the SQL to be used
    # they need the {num} string replaced before they can be used

    # If sql text name includes:
    #  sub selection        then is is using a real group, id not = 0
    #  AND Color{num} = :color;  then it is an OnlyIf
    #  AND Color{num} = 0      then it is an OnlyIfZero

    proto_GRP_Any_SqlStmt = """
UPDATE  PersonTable AS pt
    SET Color{num}  = :set_color
FROM (
    SELECT pt2.PersonID
    FROM PersonTable AS pt2
    JOIN GroupTable AS gt ON pt2.PersonID BETWEEN gt.StartID AND gt.EndID
    WHERE gt.GroupID = :group_id ) AS id
WHERE pt.PersonID = id.PersonID;
"""

    proto_ALL_Any_SqlStmt = """
UPDATE  PersonTable
    SET Color{num}  = :set_color;
"""

    proto_GRP_OnlyIf_SqlStmt = """
UPDATE  PersonTable AS pt
    SET Color{num}  = :set_color
FROM (
    SELECT pt2.PersonID
    FROM PersonTable AS pt2
    JOIN GroupTable AS gt ON pt2.PersonID BETWEEN gt.StartID AND gt.EndID
    WHERE gt.GroupID = :group_id ) AS id
WHERE pt.PersonID = id.PersonID
    AND Color{num} = :test_color;
"""

    proto_ALL_OnlyIf_SqlStmt = """
UPDATE  PersonTable
    SET Color{num}  = :set_color
WHERE Color{num} = :test_color;
"""

    proto_GRP_OnlyIfZero_SqlStmt = """
UPDATE  PersonTable AS pt
    SET Color{num}  = :set_color
FROM (
    SELECT pt2.PersonID
    FROM PersonTable AS pt2
    JOIN GroupTable AS gt ON pt2.PersonID BETWEEN gt.StartID AND gt.EndID
    WHERE gt.GroupID = :group_id ) AS id
WHERE pt.PersonID = id.PersonID
    AND Color{num} = :test_color;
"""

    # input params:   group_id, color_group, db_color_num, action
    #    not group_id ==-0  means it operates on a real group

    if not group_id == 0 and action == "set":
        SqlStmt = proto_GRP_Any_SqlStmt.format(num=column_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt, {"group_id": str(
            group_id), "set_color": color_str})

    elif not group_id == -0 and action == "setOnlyIf":
        SqlStmt = proto_GRP_OnlyIfZero_SqlStmt.format(num=column_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt, {"group_id": str(group_id),
                    "set_color": color_str, "test_color": str(0)})

    elif not group_id == -0 and action == "clearAny":
        SqlStmt = proto_GRP_Any_SqlStmt.format(num=column_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt, {"group_id": str(
            group_id), "set_color": color_str})

    elif not group_id == -0 and action == "clearOnlyIf":
        SqlStmt = proto_GRP_OnlyIf_SqlStmt.format(num=column_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt, {"group_id": str(
            group_id), "set_color": color_str, "test_color": test_color_str})

    elif group_id == -0 and action == "clearAny":
        SqlStmt = proto_ALL_Any_SqlStmt.format(num=column_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt, {"group_id": str(
            group_id), "set_color": color_str})

    elif group_id == -0 and action == "clearOnlyIf":
        SqlStmt = proto_ALL_OnlyIf_SqlStmt.format(num=column_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt, {"group_id": str(group_id),
                    "set_color": color_str, "test_color": color_str})

    else:
        raise RMc.RM_Py_Exception('Action not found. Something went wrong.')

    return


# ===================================================DIV60==
def translate_ui_color_to_db(ui_number=None, ui_color_name=None, ui_custom_name=None):

    # provide one of either input argument
    # def translate_ui_color_to_db( ui_number, ui_color_name=None, ui_name=None):

    if ui_number is not None:
        if ui_number == 1:
            db_color = 4
        elif ui_number == 2:
            db_color = 15
        elif ui_number == 3:
            db_color = 16
        elif ui_number == 4:
            db_color = 17
        elif ui_number == 5:
            db_color = 18
        elif ui_number == 6:
            db_color = 6
        elif ui_number == 7:
            db_color = 19
        elif ui_number == 8:
            db_color = 20
        elif ui_number == 9:
            db_color = 7
        elif ui_number == 10:
            db_color = 1
        elif ui_number == 11:
            db_color = 21
        elif ui_number == 12:
            db_color = 5
        elif ui_number == 13:
            db_color = 2
        elif ui_number == 14:
            db_color = 9
        elif ui_number == 15:
            db_color = 22
        elif ui_number == 16:
            db_color = 3
        elif ui_number == 17:
            db_color = 11
        elif ui_number == 18:
            db_color = 14
        elif ui_number == 19:
            db_color = 8
        elif ui_number == 20:
            db_color = 12
        elif ui_number == 21:
            db_color = 23
        elif ui_number == 22:
            db_color = 24
        elif ui_number == 23:
            db_color = 25
        elif ui_number == 24:
            db_color = 13
        elif ui_number == 25:
            db_color = 10
        elif ui_number == 26:
            db_color = 26
        elif ui_number == 27:
            db_color = 27
        else:
            raise RMc.RM_Py_Exception(" Color number out of range 1-27")

    elif ui_color_name is not None:
        ui_color_name_lower = ui_color_name.lower()

        if ui_color_name_lower == "Pink".lower():
            db_color = 4
        elif ui_color_name_lower == "Apricot".lower():
            db_color = 15
        elif ui_color_name_lower == "Lemon".lower():
            db_color = 16
        elif ui_color_name_lower == "Chartreuse".lower():
            db_color = 17
        elif ui_color_name_lower == "Mint".lower():
            db_color = 18
        elif ui_color_name_lower == "Aqua".lower():
            db_color = 6
        elif ui_color_name_lower == "Azure".lower():
            db_color = 19
        elif ui_color_name_lower == "Mauve".lower():
            db_color = 20
        elif ui_color_name_lower == "Silver".lower():
            db_color = 7
        elif ui_color_name_lower == "Red".lower():
            db_color = 1
        elif ui_color_name_lower == "Orange".lower():
            db_color = 21
        elif ui_color_name_lower == "Yellow".lower():
            db_color = 5
        elif ui_color_name_lower == "Lime".lower():
            db_color = 2
        elif ui_color_name_lower == "Green".lower():
            db_color = 9
        elif ui_color_name_lower == "Turquoise".lower():
            db_color = 22
        elif ui_color_name_lower == "Blue".lower():
            db_color = 3
        elif ui_color_name_lower == "Purple".lower():
            db_color = 11
        elif ui_color_name_lower == "Grey".lower():
            db_color = 14
        elif ui_color_name_lower == "Maroon".lower():
            db_color = 8
        elif ui_color_name_lower == "Brown".lower():
            db_color = 12
        elif ui_color_name_lower == "Khaki".lower():
            db_color = 23
        elif ui_color_name_lower == "Olive".lower():
            db_color = 24
        elif ui_color_name_lower == "Forest".lower():
            db_color = 25
        elif ui_color_name_lower == "Teal".lower():
            db_color = 13
        elif ui_color_name_lower == "Navy".lower():
            db_color = 10
        elif ui_color_name_lower == "Aubergine".lower():
            db_color = 26
        elif ui_color_name_lower == "Slate".lower():
            db_color = 27
        else:
            raise RMc.RM_Py_Exception("Color name not found. Check spelling.")

    elif ui_custom_name is not None:
        raise RMc.RM_Py_Exception(
            "ui_custom_name translation not yet implemented")
    else:
        raise RMc.RM_Py_Exception(
            "An argument must be provided to translate_ui_color_to_db")

    return db_color


# ===================================================DIV60==
def group_members(group_id, db_connection):

    member_list = []
    # check how many groupNames with name and TagType=0 already exist
    SqlStmt = """
SELECT  StartID,  EndID
FROM GroupTable
WHERE GroupID = ?
ORDER BY StartID
"""

    cur = db_connection.cursor()
    cur.execute(SqlStmt, (group_id,))
    result = cur.fetchall()
    for line_set in result:
        if line_set[0] == line_set[1]:
            member_list.append(line_set[0])
        else:
            for i in range(line_set[0], line_set[1]):
                member_list.append(i)

    return member_list


# ===================================================DIV60==
def validate_DB_group_name(group_name, report_file, db_connection):

    #  TagTable
    #   TagID=rowid
    #   TagType =0 for Groups
    #   TagName   duplicates not constrained

    # check how many groupNames with name and TagType=0 already exist
    SqlStmt = """
SELECT count(*), TagValue
FROM TagTable
WHERE TagName=:Name COLLATE NOCASE AND TagType=0 COLLATE NOCASE
"""
    cur=db_connection.cursor()
    cur.execute(SqlStmt, {"Name": group_name})
    result=cur.fetchone()
    existingNumber=result[0]
    GroupID=result[1]

    if existingNumber > 1:
        raise RMc.RM_Py_Exception(F"\nERROR: Group: {q_str(group_name)}  exists more than once in the database.\n"
                                  "Rename one of the duplicates. \n")
    elif existingNumber == 0:
        raise RMc.RM_Py_Exception(
            F'\nERROR: Group: {q_str(group_name)} does not exist in the database. \n')

    return GroupID


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
