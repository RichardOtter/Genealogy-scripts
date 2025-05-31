# OLD TODO
import xml.etree.ElementTree as ET


import sys
from pathlib import Path
sys.path.append( str(Path.resolve(Path.cwd() / r'..\RMpy package')))
import RMpy.launcher          # type: ignore
import RMpy.common as RMc     # type: ignore
from RMpy.common import q_str # type: ignore


# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.13

# Config files fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH
#
# OLD TODO
#    MAPPING     FACTTYPE_CURRENT
#    MAPPING     FACTTYPE_NEW
#    MAPPING     ROLE
#    SOURCE_FILTER     DESC
#    SOURCE_FILTER     DATE


G_count = 0

# ================================================================
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"]      = "Lump_Newspapers" 
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"]  = "RM-Python-config.ini"
    utility_info["script_path"]  = Path(__file__).parent
    utility_info["run_features_function"]  = run_selected_features
    utility_info["allow_db_changes"]  = True
    utility_info["RMNOCASE_required"] = True
    utility_info["RegExp_required"]   = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    lump_sources(config, db_connection, report_file)

# ===================================================DIV60==
def lump_sources(config, db_connection, report_file):

  # Deal with RMNOCASE index and the fact that the collation sequence is different here than in RM
  # Must Rebild Indexes in RM immediatly upon opening the DB.
  SqlStmt_ReIndex= """
   REINDEX RMNOCASE;
   """

  cur = db_connection.cursor()
  cur.execute(SqlStmt_ReIndex)

#  old_src_TemplateID= 10070
#  new_src_TemplateID= 10071

  lumped_source_map = config ["MAPPING"]["LUMP_MAP"]
  mapping = config["MAPPING"]['FIELD_MAPPING']

  field_mapping = parse_field_mapping(mapping)

  lumped_source_list = [
    (6815, "%-pHTH=%", "NP US,HI- Hawaii Tribune-Herald")
    ]
    

  for source in lumped_source_list:

    # specify the single source that is to get the new citations
    NewSourceID = source[0]
    src_name_identifier=  source[1]
   
    # List the sources which will be converted to citations of the 'new' source
    SQL_stmt = "SELECT SourceID FROM SourceTable WHERE Name LIKE ?"
  #  SourcesToLump = GetListOfRows( db_connection, SQL_stmt, (src_name_identifier, old_src_TemplateID))
   
# get template id from old source- just want to be sure all od sources have same template
# actually, the mapping takes casre of that, but probably want to alert user


    cur = db_connection.cursor()
    subs=(src_name_identifier,)
    cur.execute(SQL_stmt, subs)

    SourcesToLump = []
    for t in cur:
      for x in t:
        SourcesToLump.append(x)

    report_file.write (f"\n\n\nNumber of source to process: {str(len(SourcesToLump))}\n")
   
    #iterate through each of the old sources, converting each one separately
    for oldSrc in SourcesToLump:
        report_file.write (f"old SourceID= {str(oldSrc)}\n" )
        ConvertSource (db_connection, oldSrc, NewSourceID, field_mapping, report_file)
        report_file.write ("=====================================================\n")

  report_file.write ("total not found",G_count)

  return 0


# ================================================================
def ConvertSource ( db_connection, oldSourceID, newSourceID, field_mapping, report_file):

  global G_count

  # display source name for confirmation
  SqlStmt = """
  SELECT Name
    FROM SourceTable
    WHERE SourceID = ?
  """
  cur = db_connection.cursor()
  cur.execute(SqlStmt, (newSourceID,))
  report_file.write ("source to receive citations......" + cur.fetchone()[0]  )

  citation_IDs_to_move= getCitationsToMove(db_connection,oldSourceID)
  # For the given old source, count its citations 
  # Code as written only handles sources that have one citation and
  # no info in that citation is preserved.
  # Must make code changes to deal with #cits !=1 or preserve info in the citation.

  if len(citation_IDs_to_move) != 1:  raise (RMc.RM_Py_Exception("more than one citation"))

  for citation_to_move in citation_IDs_to_move:
    if ConvertCitation( db_connection, oldSourceID, newSourceID, citation_to_move, field_mapping, report_file) == False:
       return

  # delete the old src (all of its citations have been moved to new source)
  SqlStmt = """
  DELETE from SourceTable
      WHERE SourceID = ?
  """
  RunSqlNoResult( db_connection, SqlStmt, tuple([oldSourceID, ]) )
  return

# ================================================================
def ConvertCitation( db_connection, oldSourceID, newSourceID, citationIDToMove, field_mapping, report_file ):

  global G_count

# Copy standard fields from old src record to the citationToMove
  SqlStmt = """
  UPDATE CitationTable
    SET (CitationName, ActualText, Comments, UTCModDate)
      = (SELECT Name, ActualText, Comments, UTCModDate FROM SourceTable WHERE SourceID = ?)
    WHERE CitationID = ?
  """
  RunSqlNoResult( db_connection, SqlStmt, (oldSourceID, citationIDToMove) )

  # Change owner & type columns for relevant web tags so they follow the citationToMove
  # takes all webtags linked to old source and add them to the citation in process
  # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE WEB TAGS.  NOTE only 1 citation in the old source is supported

  SqlStmt = """
      UPDATE URLTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( db_connection, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  # Change owner & type for relevant media so they follow the citationToMove
  # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE MEDIA LINKS.

  SqlStmt = """
  UPDATE MediaLinkTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( db_connection, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  #  move the existing citation to the new (existing) source
  SqlStmt = """
  UPDATE CitationTable
    SET SourceID = ?
    WHERE CitationID = ?
  """
  RunSqlNoResult( db_connection, SqlStmt, tuple([newSourceID, citationIDToMove]) )


  # Get the SourceTable.Fields BLOB from the oldSource to extract its data
  SqlStmt = """
  SELECT Fields
    FROM SourceTable
    WHERE SourceID = ?
  """

  oldSrcFields = {}
  srcRoot = getFieldsXmlDataAsDOM ( db_connection, SqlStmt, oldSourceID )
  srcFields = srcRoot.find("Fields")


#  print( ET.indent(srcRoot, space=" ", level=0) )
#  print(ET.tostring(srcRoot))
#  return

  for item in srcFields:
    if   item[0].text == "Name":               oldSrcFields["Name"] = item[1].text
    elif item[0].text == "BirthDate":          oldSrcFields["BirthDate"] = item[1].text
    elif item[0].text == "Name2":              oldSrcFields["Name2"] = item[1].text
    elif item[0].text == "Title":              oldSrcFields["Title"] = item[1].text
    elif item[0].text == "PublicationDate":    oldSrcFields["PublicationDate"] = item[1].text
    elif item[0].text == "PublicationPage":    oldSrcFields["PublicationPage"] = item[1].text
    elif item[0].text == "PublicationColumn":  oldSrcFields["PublicationColumn"] = item[1].text
    elif item[0].text == "DateCitation":       oldSrcFields["DateCitation"] = item[1].text
    elif item[0].text == "CD":                 oldSrcFields["CD"] = item[1].text

  report_file.write (str(oldSrcFields))


  # retrieve an empty sample XML chunk that has the citation fields of the source template used by the newSource
  # this means the citation does not retain any old data not explicitly saved.
  # Get the CitationTable.Fields BLOB for the new source (must be pre-existing and named "sample citation")
  SqlStmt = """
  SELECT CT.Fields
    FROM CitationTable CT
    JOIN SourceTable ST ON CT.SourceId = ST.SourceID
    WHERE CT.SourceID = ? AND CT.CitationName = "sample citation"
  """
  newRoot = getFieldsXmlDataAsDOM ( db_connection, SqlStmt, newSourceID)
  if newRoot == None:
    raise RMc.RM_Py_Exception( "Cannot find the 'sample citation'")

  newFields = newRoot.find("Fields")

  # now fill the XML with values
  for item in newFields:
    if   item[0].text == "Name":                 item[1].text = oldSrcFields["Name"]
    elif item[0].text == "DateBirth":            item[1].text = oldSrcFields["BirthDate"]
    elif item[0].text == "Name2":                item[1].text = oldSrcFields["Name2"]
    elif item[0].text == "Title":                item[1].text = oldSrcFields["Title"]
    elif item[0].text == "PublicationDate":      item[1].text = oldSrcFields["PublicationDate"]
    elif item[0].text == "PublicationPage":      item[1].text = oldSrcFields["PublicationPage"]
    elif item[0].text == "PublicationColumn":    item[1].text = oldSrcFields["PublicationColumn"]
    elif item[0].text == "DateCitation":         item[1].text = oldSrcFields["DateCitation"]
    elif item[0].text == "CD":                   item[1].text = oldSrcFields["CD"]


#  NOTE field name DwellingSN should be changed to HouseholdSN. 
#  NOTE  for now
#  NOTE  1950 census-   field DwellingSN is filled by Dwelling in old template
#  NOTE  1940 census-   field DwellingSN is filled by Family in old template which was called Household in census

  # Update the citation Fields column with the new XML
  SqlStmt = """
  UPDATE CitationTable
    SET Fields = ?
    WHERE CitationID = ?
  """
  RunSqlNoResult( db_connection, SqlStmt, tuple([ET.tostring(newRoot), citationIDToMove]) )

  return


# ================================================================
def RunSqlNoResult ( db_connection, SqlStmt, myTuple):
    cur = db_connection.cursor()
    cur.execute(SqlStmt, myTuple)


# ================================================================
def getFieldsXmlDataAsDOM ( db_connection, SqlStmt, rowID ):
  cur = db_connection.cursor()
  cur.execute(SqlStmt, (rowID,))
  XmlTxt_raw = cur.fetchone()
  if XmlTxt_raw == None: return None

  XmlTxt=(XmlTxt_raw[0])
  print(type(XmlTxt) )
  if not isinstance(XmlTxt, str):
    XmlTxt=XmlTxt.decode('utf-8')

  # test for and fix old style "XML" no longer used in RM8
  xmlStart = "<Root"
  rootLoc=XmlTxt.find(xmlStart)
  if rootLoc != 0:
    XmlTxt = XmlTxt[rootLoc::]

  # read into DOM and parse for needed values
  # only Page needed from old cit  XML data
  XmlRoot = ET.fromstring(XmlTxt)

  return XmlRoot


# ================================================================
def getCitationsToMove ( db_connection, oldSourceID):
  # get citations for oldSourceID
  SqlStmt = """
  SELECT CitationID
    FROM CitationTable
    WHERE SourceID = ?
  """
  cur = db_connection.cursor()
  cur.execute(SqlStmt, (oldSourceID,))
  citationsIDs = cur.fetchall()

  citationIDsToMove= []

  # change the data structure from list of tuples to list of ints
  for each in citationsIDs:
      citationIDsToMove.append(each[0])

  return citationIDsToMove


# ================================================================
def GetListOfRows ( db_connection, SqlStmt):
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
            field_names_transform1 = root_element.find("Fields/Field[Name='" + transform[1] + "']")
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
