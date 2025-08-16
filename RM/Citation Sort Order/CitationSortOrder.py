import sys
from pathlib import Path
sys.path.append(str(Path.resolve(Path.cwd() / r'..\RMpy package')))

import RMpy.common as RMc       # noqa #type: ignore
import RMpy.launcher            # noqa #type: ignore
import RMpy.RMDate              # noqa #type: ignore

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.13

# Config files fields use
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP

# TODO  support associations, tasks, fam facts

# ===================================================DIV60==
#  Globals

G_RIN_offset = int(10**12)


# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"] = "CitationSortOrder"
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

    change_citation_order_feature(config, db_connection, report_file)


# ===================================================DIV60==
def change_citation_order_feature(config, db_connection, report_file):

    while True:
        # keep asking for RINs until break

        # request the PersonID / RIN
        response_RIN = input('Enter the RIN of the person who has '
                             'the citations to modify, or q to quit the app:\n')
        if response_RIN == '':
            continue
        if response_RIN in 'Qq':
            # exit the app
            break

        try:
            PersonID = int(response_RIN)
        except ValueError:
            print('Cannot interpret the response. Enter an integer or "q"')
            continue

        if not valid_PersonID(PersonID, db_connection, report_file):
            print('The number entered is not a valid RIN in this database.\n\n')
            continue

        # Now ask for the kind of object the citation list is attached to
        while True:
            response_attachment = input(
                '\nIs the citation list that is to be modified attached to:\n'
                'a Fact (f), a Name (n) the Person (p) or skip this RIN (s)?:\n')

            if response_attachment == "":
                continue
            if response_attachment in "Pp":
                rows = attached_to_person(PersonID, db_connection, report_file)
                continue
            elif response_attachment in "Ff":
                rows = attached_to_fact(PersonID, db_connection, report_file)
                continue
            elif response_attachment in "Nn":
                rows = attached_to_name(PersonID, db_connection, report_file)
                continue
            elif response_attachment in "Ss":
                break
            else:
                print(F'{response_attachment} is not understood.\n'
                      'Enter one of:  f, n, p, s     (s will skip this RIN).')
                continue

    return 0


# ===========================================DIV50==
def attached_to_any(PersonID, db_connection, report_file):

    # Select nameID's that have more than 1 citation attached1
    SqlStmt = """
SELECT  nt.NameID, nt.Prefix, nt.Given, nt.Surname, nt.Suffix
  FROM NameTable AS nt
  INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = nt.NameID AND clt.OwnerType = 7
  WHERE  nt.OwnerID = ?
GROUP BY nt.NameID
HAVING COUNT() > 1;
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (PersonID, ))
    rows = cur.fetchall()

    return


# ===========================================DIV50==
def attached_to_name(PersonID, db_connection, report_file):

    # Select names connected to RIN and that have more than 1 citation attached
    SqlStmt = """
SELECT  nt.NameID, nt.Date, nt.Prefix, nt.Given, nt.Surname, nt.Suffix
  FROM NameTable AS nt
  INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = nt.NameID
  WHERE  nt.OwnerID = ?
    AND clt.OwnerType = 7
GROUP BY nt.NameID
HAVING COUNT() > 1;
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (PersonID, ))
    rows = cur.fetchall()

    number_of_names = len(rows)

    if (number_of_names > 1):
        print(F'{number_of_names} names found having more than'
              ' 1 attached citation.\n')
        NameID = select_name_from_list(rows)

    elif (number_of_names == 1):
        NameID = rows[0][0]
        temp_date = RMpy.RMDate.from_RMDate(
            rows[0][1], RMpy.RMDate.Format.SHORT)
        print('Found one name with more than one citation.\n' +
              F'{rows[0][0]:<5}:    {temp_date:15} : '
              F'{rows[0][2]} {rows[0][3]} {rows[0][4]} {rows[0][5]}\n\n\n')

    elif (number_of_names == 0):
        print('This person does not hae any names with more than one citation.')
        return

    # get the citation list
    SqlStmt = """
SELECT clt.SortOrder, clt.LinkID, st.Name, ct.CitationName
  FROM CitationTable AS ct
  JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
  JOIN SourceTable AS st ON ct.SourceID = st.SourceID
  WHERE clt.OwnerID = ?
    AND clt.OwnerType = 7
ORDER BY clt.SortOrder ASC;
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (NameID, ))
    rows = cur.fetchall()

    modify_local_citation_list(rows, db_connection, report_file)

    return


# ===========================================DIV50==
def select_name_from_list(rows):

    # nt.NameID, nt.Date, nt.Prefix, nt.Given, nt.Surname, nt.Suffix

    for i in range(0, len(rows)):
        # print(i, rows[i-1][1], rows[i-1][2], rows[i-1][3], rows[i-1][4])
        temp_date = RMpy.RMDate.from_RMDate(
            rows[i][1], RMpy.RMDate.Format.SHORT)
        print(F'{i+1:<5}:{temp_date:15} : '
              F'{rows[i][2]} {rows[i][3]} {rows[i][4]} {rows[i][5]}')

    while True:
        try:
            event_number = int(
                input("\nWhich name's citations will be re-ordered? "))
            if event_number < 1 or event_number > len(rows):
                print(F'Enter a number 1-{len(rows)}')
                continue
            break
        except ValueError as e:
            print(F'Enter a number 1-{len(rows)}')

    return rows[event_number - 1][0]



# ===========================================DIV50==
def NEW_attached_to_fact(PersonID, db_connection, report_file):

    EventID = None
    FactTypeID = input('Enter the FactTypeID or\n'
                       'blank for full list of attached '
                       'Facts with more than one citation\n')

    if FactTypeID == '':
        # Select all EventID's that have more than 1 citation attached
        SqlStmt = """
SELECT et.EventID, ftt.Name, et.Date, et.Details
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID
  WHERE et.OwnerID = ?
    AND et.OwnerType = 0
    AND clt.OwnerType = 2
GROUP BY et.EventID
HAVING COUNT() > 1;
"""
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (PersonID, ))
        rows = cur.fetchall()

    else:
        # Select EventID's of specified type that have more than 1 citation attached
        SqlStmt = """
SELECT et.EventID, ftt.Name, et.Date, et.Details
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID AND clt.OwnerType = 2
  WHERE (et.OwnerID = ? OR et.OwnerID = ?)
    AND et.OwnerType = 0
    AND et.EventType = ?
GROUP BY et.EventID
HAVING COUNT() > 1;
"""
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (PersonID, PersonID + G_RIN_offset, FactTypeID))
        rows = cur.fetchall()

    number_of_events = len(rows)

    if number_of_events > 1:
        print(F'{number_of_events} events found having more than'
              ' 1 attached citation.')
        EventID = select_fact_from_list(rows)
        modify_local_citation_list(rows, report_file)

    elif number_of_events == 0:
        raise RMc.RM_Py_Exception(
            'No events with more than one citation found. Try again.')
    elif number_of_events == 1:
        EventID = rows[0][0]
        temp_date = RMpy.RMDate.from_RMDate(
            rows[0][2], RMpy.RMDate.Format.SHORT)
        print('Found one event with more than one citation.\n' +
              F'{rows[0][1]}:    {temp_date}  {rows[0][3]}\n\n')
        modify_local_citation_list(rows, report_file)

    return


# ===========================================DIV50==
def attached_to_fact(PersonID, db_connection, report_file):

    # Select all Events connected to RIN that have more than 1 citation attached
    SqlStmt = """
SELECT et.EventID, ftt.Name, et.Date, et.Details
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID
  WHERE et.OwnerID = ?
    AND et.OwnerType = 0
    AND clt.OwnerType = 2
GROUP BY et.EventID
HAVING COUNT() > 1;
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (PersonID, ))
    rows = cur.fetchall()

    number_of_events = len(rows)

    if number_of_events > 1:
        print(F'{number_of_events} events found having more than'
              ' 1 attached citation.\n\n')
        EventID = select_fact_from_list(rows)
    elif number_of_events == 1:
        EventID = rows[0][0]
        temp_date = RMpy.RMDate.from_RMDate(
                                rows[0][2], RMpy.RMDate.Format.SHORT)
        print('Found one event with more than one citation.\n' +
              F'{rows[0][0]:<5}:{rows[0][1]}    {temp_date}'
              F'  {rows[0][3]}\n\n\n')
    elif number_of_events == 0:
        print('This person does not hae any facts with more than one citation.')
        return

    # get the citation list
    SqlStmt = """
    SELECT clt.SortOrder, clt.LinkID, clt.OwnerID, st.Name, ct.CitationName
      FROM CitationTable AS ct
      JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
      JOIN SourceTable AS st ON ct.SourceID = st.SourceID
      WHERE (clt.OwnerID = ? OR clt.OwnerID = ?)
        AND clt.OwnerType = 2
    ORDER BY clt.SortOrder ASC
    """

    cur.execute(SqlStmt, (EventID, EventID + G_RIN_offset))
    rows = cur.fetchall()

    rowDict = modify_local_citation_list(rows, report_file)
    UpdateDatabase(rowDict, db_connection)
    return


# =======================================1====DIV50==
def select_fact_from_list(rows):

    # et.EventID, ftt.Name, et.Date, et.Details
    for i in range(0, len(rows)):
        temp_date = RMpy.RMDate.from_RMDate(
            rows[i][2], RMpy.RMDate.Format.SHORT)
        message = F'{i+1:<5}{rows[i][1]:15}: {temp_date:15}{rows[i][3]}'
        print(message)

    while True:
        try:
            event_number = int(
                input("\nWhich fact's citation list will be modified? "))
            if event_number < 1 or event_number > len(rows):
                print(F'Enter a number 1-{len(rows)}')
                continue
            break
        except ValueError as e:
            print(F'Enter a number 1-{len(rows)}')

    return rows[event_number - 1][0]


# ===========================================DIV50==
def attached_to_person(PersonID, db_connection, report_file):

# Only one citation list is associated with the RIN
# So retrieve that list immediately

# Third  return value is a flag for "hidden" 0 is visible, 1 (true)is hidden
    SqlStmt = """
SELECT clt.SortOrder, clt.LinkID, clt.OwnerID, st.Name, ct.CitationName
  FROM CitationTable AS ct
  JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
  JOIN SourceTable AS st ON ct.SourceID = st.SourceID
  WHERE (clt.OwnerID = ? OR clt.OwnerID = ?)
    AND clt.OwnerType = 0
ORDER BY clt.SortOrder ASC;
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (PersonID, PersonID + G_RIN_offset))

    rows = cur.fetchall()

    if len(rows) >1:
        rowDict = modify_local_citation_list(rows, report_file)
        UpdateDatabase(rowDict, db_connection)
        return
    else:
        print("Person does not have more than one citations attached")
        return


# ===========================================DIV50==
def modify_local_citation_list(rows, report_file):

    # Create the origin 1 based dictionary
    # Use 1 based indexing for human user
    rowDict = dict()

#  0 clt.SortOrder
#  1 clt.LinkID
#  2 clt.OwnerID
#  3 st.Name
#  4 ct.CitationName

    for i in range(0, len(rows)):
        rowDict[i+1] = [rows[i][1], rows[i][2], (rows[i][3], (rows[i][4])[0:50])]

# the dictionary
#         rowDict key = cit order index starting at 1
#         rowDict value
#  [0]    clt.LinkID
#  [1]    clt.OwnerID
#  [2][0] st.Name
#  [2][1] ct.CitationName

    print(
        '\n'
        '------------------------------------------------------\n'
        'To modify the citation list, at each prompt, enter a command:\n'
        '*  the number of the citation that should be swapped into this slot\n'
        '*  or\n'
        '*  blank    to accept current line as it is and move to the next\n'
        '*  h        to toggle HIDDEN vs. VISIBLE\n'
        '*  s        to accept current and following slots as they are\n'
        '*  a        to abort and make no changes\n'
        '------------------------------------------------------\n')
    
    # Print the list as it is
    report_file.write("\n\n Previous citation list \n")
    list_output(rowDict, report_file)

    done_with_this_list = False
    while not done_with_this_list:
        j = 1  # indexing is 1-based
        while j <= len(rowDict):
            response = str(input(F'Enter a command for line # {j} : '))
            if response == '':
                j = j + 1
                continue
            elif response in 'Hh':
                # Toggle the hidden attribute
                if rowDict[j][1] < G_RIN_offset:
                    rowDict[j][1] = rowDict[j][1] + G_RIN_offset
                else:
                    rowDict[j][1] = rowDict[j][1] - G_RIN_offset
                list_output(rowDict)
                continue
            elif response in 'Ss':
                break
            elif response in 'Aa':
                raise RMc.RM_Py_Exception("No changes made to this list.")
            else:
                try:
                    swapVal = int(response)
#                    if swapVal < (j + 1) or swapVal > (len(rowDict)):
                    if swapVal < 1 or swapVal > len(rowDict):
                        print(F'Integer must be in the range {1}-{len(rowDict)}')
                        continue
                except ValueError:
                    print('Enter an integer, blank,  or one of: h/H/s/S/a/A')
                    continue
                #  Python swap mechanism using tuples
                rowDict[swapVal], rowDict[j] = rowDict[j], rowDict[swapVal]
                j = j + 1
                print("\n\n")
                list_output(rowDict)
        # End while j

        # Print list after a round of modifications
        print("\n\n")
        list_output(rowDict)

        response = input(
            '\n\n'
            'Save the new citation list as shown above?\n'
            'Enter one of-\n'
            '*  Y/y: make the change as shown above\n'
            '*  N/n :go back and do another round of modifications\n'
            '*  A/a :do not save any changes to this list and exit app\n')

        if response in "Yy":
            # Print order after a round of sorting
            report_file.write("\n\n Current order \n")
            list_output(rowDict, report_file)
            done_with_this_list = True

        elif response in "Aa":
            print('No changes made to this list in the database')
            report_file.write(
                'No changes made to this list in the database.\n\n\n')
            done_with_this_list = True

        elif response in "Nn":
            print('Try another round of re-ordering.\n\n')
            list_output(rowDict)
            done_with_this_list = False

    # end while not_done
    print("\n\n")
    return rowDict


# ===========================================DIV50==
def list_output(rowDict, report_file = None ):
    for key, value in sorted(rowDict.items()):
        message = F'{key}   {"HIDDEN " if value[1] > G_RIN_offset else "VISIBLE"}  {value[2][0][0:40]:<43}    {value[2][1][0:50]}'
        print(message)
        if report_file is not None:
            report_file.write(message + '\n')
    print('\n\n')
    if report_file is not None:
        report_file.write('\n\n')


# ===========================================DIV50==
def valid_PersonID(PersonID, dbConnection, report_file):

    SqlStmt = """
SELECT nt.Prefix, nt.Given, nt.Surname, nt.Suffix
FROM PersonTable AS pt
INNER JOIN NameTable AS nt ON nt.OwnerID=pt.PersonID
WHERE nt.OwnerID = ?
    AND nt.IsPrimary = 1;
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (PersonID, ))
    rows = cur.fetchall()

    if len(rows) == 0 or len(rows) > 1:
        is_valid = False

    else:
        message = (F"RIN= {PersonID}  person's primary name is: "
                   F'{rows[0][0]} {rows[0][1]} {rows[0][2]} {rows[0][3]}')
        print(message)
        report_file.write(message + '\n')
        is_valid = True

    return is_valid

# ===========================================DIV50==
def UpdateDatabase(rowDict, db_connection):

    # do not update the UTCModDate
    SqlStmt = """
UPDATE  CitationLinkTable AS clt
  SET SortOrder = ?,
      OwnerID = ?
  WHERE LinkID = ?;
"""
#    for i in range(1, len(rowDict)+1):
#        cur = db_connection.cursor()
#        cur.execute(SqlStmt, (i, rowDict[i][1], rowDict[i][0]))
#        db_connection.commit()

    for key, value in rowDict.items():
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (key, value[1], value[0]))
        db_connection.commit()

    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
