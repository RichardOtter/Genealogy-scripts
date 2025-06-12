import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.append(str(Path.resolve(Path.cwd() / r'..\RMpy package')))

import RMpy.common as RMc  # type:ignore  # noqa
import RMpy.launcher  # type:ignore  # noqa


# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.13

# Config files fields used
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  RMNOCASE_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#
#    LUMP_MAPPINGS   MAPPING_SRC_CIT
#    LUMP_MAPPINGS   MAPPING_IDENT_SRC
#    LUMP_OPTIONS   TEMPLATE_CHECK_OVERRIDE (optional)

# ===================================================DIV60==
#  Global Variables
G_DEBUG = False


# ================================================================
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"] = "Lump_Newspapers"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"] = Path(__file__).parent
    utility_info["run_features_function"] = run_selected_features
    utility_info["allow_db_changes"] = True
    utility_info["RMNOCASE_required"] = True
    utility_info["RegExp_required"] = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    lump_sources(config, db_connection, report_file)


# ===================================================DIV60==
def lump_sources(config, db_connection, report_file):

    try:
        lump_list_raw = config["LUMP_MAPPINGS"]["MAPPING_IDENT_SRC"]
    except:
        raise RMc.RM_Py_Exception(
            'ERROR: MAPPING_IDENT_SRC must be specified.')

    try:
        mapping_raw = config["LUMP_MAPPINGS"]['MAPPING_SRC_CIT']
    except:
        raise RMc.RM_Py_Exception(
            'ERROR: MAPPING_SRC_CITPING must be specified.')

    try:
        # if missing, treated as false/off
        template_check_override = config["LUMP_OPTIONS"].getboolean(
            'TEMPLATE_CHECK_OVERRIDE')
    except:
        raise RMc.RM_Py_Exception(
            "One of the LUMP_OPTIONS values could not be interpreted as either on or off.\n")

    field_mapping = parse_field_mapping(mapping_raw)
    lump_list = parse_field_mapping(lump_list_raw)

    # Check whether all sources use the same template
    # If they use more than one Template, it is not necessarily an error, as
    # long as the MAPPING_IDENT_SRC is appropriate
    sources_to_check = []
    for source_type_to_check in lump_list:
        lumped_SourceID = source_type_to_check[1]
        split_src_name_identifier = source_type_to_check[0]

        # List the split sources which will be converted to citations of the lumped source
        SQL_stmt = (
            """SELECT SourceID, TemplateID, Name
      FROM SourceTable
      WHERE Name LIKE ?
    """)
        cur = db_connection.cursor()
        cur.execute(SQL_stmt, (split_src_name_identifier,))
        for cur_row in cur:
            sources_to_check.append(
                (split_src_name_identifier, cur_row[0], cur_row[1], cur_row[2]))

    templates_all_same = True
    if len(sources_to_check) > 0:
        templateID = sources_to_check[0][2]
        for src in sources_to_check:
            if templateID != src[2]:
                templates_not_all_same = False
                break

    if not templates_all_same:
        report_file.write("\n\nWARNING: Source templates are not all the same.\n"
                          " Ensure that the mapping can handle all templates in use.\n\n"
                          "The sources selected for lumping: (identifier, SourceID, TemplateID, Name)\n\n")
        for src in sources_to_check:
            report_file.write(F"{str(src)}\n")

    if not templates_all_same and not template_check_override:
        continue_anyway = input(
            "Source templates are not all the same. Continue anyway ? (Y/N):\n")
        if continue_anyway != 'y' or continue_anyway != 'Y':
            raise RMc.RM_Py_Exception(
                "\n\n\nERROR: Source templates are not all the same for the selected sources.")

    report_file.write(
        F"\n\nNumber of source identifiers in MAPPING_IDENT_SRC= {len(lump_list)}")

    # Deal with RMNOCASE index and the fact that the collation sequence is different here than in RM
    # Must Rebuild Indexes in RM immediately upon opening the DB.
    # There is one SQL in convert_citation that updates CitationName
    RMc.reindex_RMNOCASE(db_connection)

    # Iterate through list of the new (lumped) sources and add the citations to each
    for lumped_source in lump_list:

        # specify the single source that is to get the new citations
        lumped_SourceID = lumped_source[1]
        split_src_name_identifier = lumped_source[0]

        # List the split sources which will be converted to citations of the lumped source
        SQL_stmt = (
            """SELECT SourceID, Name, TemplateID
      FROM SourceTable
      WHERE Name LIKE ?
    """)
        cur = db_connection.cursor()
        cur.execute(SQL_stmt, (split_src_name_identifier,))
        split_sources_to_lump = []
        for cur_row in cur:
            split_sources_to_lump.append((cur_row[0], cur_row[1], cur_row[2]))

        report_file.write(
            F"\n\n\nUsing {split_src_name_identifier}\n"
            F"found {len(split_sources_to_lump)} source citations to lump\n"
            F"into the lumped source with ID {lumped_SourceID}\n")

        report_file.write(
            "\n=====================================================\n\n")

        # iterate through each of the old sources, converting each one separately
        for split_source in split_sources_to_lump:
            report_file.write(F"Split Source name= {split_source[1]}\n")
            ConvertSource(
                db_connection, split_source[0], lumped_SourceID, field_mapping, report_file)
            report_file.write(
                "\n=====================================================\n\n")

    report_file.write(
        "\n=====================================================\n== END OF REPORT\n")

    return


# ================================================================
def ConvertSource(db_connection, split_SourceID, lumped_SourceID, field_mapping, report_file):

    # display source name for confirmation
    SqlStmt = (
        """SELECT Name
    FROM SourceTable
    WHERE SourceID = ?
  """)
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (lumped_SourceID,))
    report_file.write(F"Source to receive citation= {cur.fetchone()[0]}")

    citation_IDs_to_move = getCitationsToMove(db_connection, split_SourceID)
    # For the given old source, count its citations
    # Code as written only handles sources that have one citation and
    # no info in that citation is preserved.
    # Must make code changes to deal with #citations >1 or preserve info in the citation.

    if len(citation_IDs_to_move) != 1:
        raise (RMc.RM_Py_Exception(
            "\n\nERROR: A split source to be lumped has more than one citation."))

    for citation_to_move in citation_IDs_to_move:
        if ConvertCitation(db_connection, split_SourceID, lumped_SourceID, citation_to_move, field_mapping, report_file) == False:
            return

    # delete the old src (all of its citations have been moved to new source)
    SqlStmt = (
        """DELETE from SourceTable
      WHERE SourceID = ?
  """)
    RunSqlNoResult(db_connection, SqlStmt, (split_SourceID, ))
    return


# ================================================================
def ConvertCitation(db_connection, split_SourceID, newSourceID, citationIDToMove, field_mapping, report_file):

    # Copy standard fields from old src record to the citationToMove
    SqlStmt = (
        """UPDATE CitationTable
    SET (CitationName, ActualText, Comments, UTCModDate)
      = (SELECT Name, ActualText, Comments, UTCModDate FROM SourceTable WHERE SourceID = ?)
    WHERE CitationID = ?
  """)
    RunSqlNoResult(db_connection, SqlStmt, (split_SourceID, citationIDToMove))

    # Change owner & type columns for relevant web tags so they follow the citationToMove
    # takes all webtags linked to old source and add them to the citation in process
    # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE WEB TAGS.  NOTE only 1 citation in the old source is supported

    SqlStmt = (
        """UPDATE URLTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """)
    RunSqlNoResult(db_connection, SqlStmt, tuple(
        [citationIDToMove, split_SourceID]))

    # Change owner & type for relevant media so they follow the citationToMove
    # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE MEDIA LINKS.

    SqlStmt = (
        """UPDATE MediaLinkTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """)
    RunSqlNoResult(db_connection, SqlStmt, tuple(
        [citationIDToMove, split_SourceID]))

    #  move the existing citation to the new (existing) source
    SqlStmt = (
        """UPDATE CitationTable
    SET SourceID = ?
    WHERE CitationID = ?
  """)
    RunSqlNoResult(db_connection, SqlStmt, tuple(
        [newSourceID, citationIDToMove]))

    # Get the SourceTable.Fields XML BLOB from the oldSource
    SqlStmt = (
        """SELECT Fields
    FROM SourceTable
    WHERE SourceID = ?
  """)
    oldSrcFields = {}
    srcRoot = getFieldsXmlDataAsDOM(db_connection, SqlStmt, split_SourceID)

    if G_DEBUG:
        print("citation XML OLD START ============================")
        ET.indent(srcRoot)
        ET.dump(srcRoot)
        print("citation XML OLD END ==============================")

    adjust_xml_fields(field_mapping, srcRoot)

    if G_DEBUG:
        print("citation XML NEW START ============================")
        ET.indent(srcRoot)
        ET.dump(srcRoot)
        print("citation XML NEW END ==============================")

    # Update the citation Fields column with the new XML
    SqlStmt = (
        """UPDATE CitationTable
    SET Fields = ?
    WHERE CitationID = ?
  """)
    RunSqlNoResult(db_connection, SqlStmt,
                   (ET.tostring(srcRoot), citationIDToMove))

    return


# ================================================================
def RunSqlNoResult(db_connection, SqlStmt):
    cur = db_connection.cursor()
    cur.execute(SqlStmt)


# ================================================================
def RunSqlNoResult(db_connection, SqlStmt, myTuple):
    cur = db_connection.cursor()
    cur.execute(SqlStmt, myTuple)


# ================================================================
def getFieldsXmlDataAsDOM(db_connection, SqlStmt, rowID):
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (rowID,))
    XmlTxt_raw = cur.fetchone()
    if XmlTxt_raw == None:
        return None

    XmlTxt = (XmlTxt_raw[0])
    if not isinstance(XmlTxt, str):
        XmlTxt = XmlTxt.decode('utf-8')

    # test for and fix old style "XML" no longer used in RM8
    xmlStart = "<Root"
    rootLoc = XmlTxt.find(xmlStart)
    if rootLoc != 0:
        XmlTxt = XmlTxt[rootLoc::]

    # read into DOM and parse for needed values
    # only Page needed from old cit  XML data
    XmlRoot = ET.fromstring(XmlTxt)

    return XmlRoot


# ================================================================
def getCitationsToMove(db_connection, oldSourceID):
    # get citations for oldSourceID
    SqlStmt = (
        """SELECT CitationID
    FROM CitationTable
    WHERE SourceID = ?
  """)
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (oldSourceID,))
    citationsIDs = cur.fetchall()

    citationIDsToMove = []

    # change the data structure from list of tuples to list of ints
    for each in citationsIDs:
        citationIDsToMove.append(each[0])

    return citationIDsToMove


# ================================================================
def GetListOfRows(db_connection, SqlStmt):
    # SqlStmt should return a set of single values
    cur = db_connection.cursor()
    cur.execute(SqlStmt)

    result = []
    for t in cur:
        for x in t:
            result.append(x)
    return result


# ===================================================DIV60==
def adjust_xml_fields(field_mapping, root_element):

    fields_element = root_element.find(".//Fields")
    # change fields in XML as per mapping:
    for transform in field_mapping:
        # transform[0] is the From, transform[1] is the To.
        if transform[0] == transform[1]:
            continue
        if transform[0] == "NULL":
            # check whether transform[1] already exists as a Name
            if root_element.find("Fields/Field[Name='" + transform[1] + "']") == None:
                # if it does not exist, create it
                create_empty_field(transform[1], fields_element)
            else:
                raise RMc.RM_Py_Exception(
                    "Tried to create duplicate Name in XML. NULL on left")
            continue

        # for each existing field in the XML...
        fields_in_xml = fields_element.findall('.//Field')
        for eachField in fields_in_xml:
            current_xml_field_name = eachField.find('Name').text
            if current_xml_field_name != transform[0]:
                # not the relevant XML field, continue with the next
                continue
            # found the xml field for the From field of the transform  under consideration
            # now check if transform 1 (To field) is null (already checked for transform 0 is null)
            if transform[1] == "NULL":
                # delete the field
                root_element.find(".//Fields").remove(eachField)
                break
            # Do the rename, but first check for existing field with that name
            # xpath search Fields/Field[Name='name of transform1']
            field_names_transform1 = root_element.find(
                "Fields/Field[Name='" + transform[1] + "']")
            if field_names_transform1 == None:
                # target doesn't exist, so rename source to the target name
                eachField.find('Name').text = transform[1]
                break
            else:
                raise RMc.RM_Py_Exception(
                    "Tried to create duplicate Name in XML.")
        # end of for eachField loop
    # end of for each transform loop

    # After all transforms done, *now* deal with XML that is missing a name/value element
    # For now, make it a requirement that all fields in new template be
    # included as destinations in field mapping if they are to be fixed
    for transform in field_mapping:
        # check whether transform[1] already exists as a Name
        if root_element.find("Fields/Field[Name='" + transform[1] + "']") == None:
            # if it does not exist, create it
            create_empty_field(transform[1], fields_element)


# ===================================================DIV60==
def create_empty_field(name_to_use, fields):

    # create a new field with name_to_use and empty value, in the fields element.
    newPair = ET.SubElement(fields, "Field")
    ET.SubElement(newPair, "Name").text = name_to_use
    ET.SubElement(newPair, "Value")


# ===================================================DIV60==
def parse_field_mapping(in_str):

    # convert string to list of lists (of 3 strings)
    in_str = in_str.strip()
    list_of_lines = in_str.splitlines()
    list_of_lists = []
    for each_line in list_of_lines:
        item_set = list(each_line.split(sep='>'))
        item_set = [x.strip() for x in item_set]
        item_set = [x.strip('"') for x in item_set]
        list_of_lists.append(item_set)
    return list_of_lists


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
