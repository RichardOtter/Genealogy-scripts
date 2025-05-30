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

    lump_citations(config, db_connection, report_file)


## global _G_count

# ===================================================DIV60==
def lump_citations(config, db_connection, report_file):

  # Deal with index and the fact that the collation sequence is different here than in RM
  SqlStmt_ReIndex= """
   REINDEX RMNOCASE;
   """

  cur = db_connection.cursor()
  cur.execute(SqlStmt_ReIndex)

  old_src_TemplateID= 10070
  new_src_TemplateID= 10071

  lumped_source_list = [
#    (6813, "-pTBE", "NP US,NY- Brooklyn Eagle")
#    (6814, "-pHSA", "NP US,HI- Honolulu Star-Advertiser")
    (6815, "%-pHTH=%", "NP US,HI- Hawaii Tribune-Herald")
#    (6816, "-pNDNE", "NP US,NY- Newsday (Nassau Edition) ")
#    (6817, "-pHSB", "NP US,HI- Honolulu Star-Bulletin")
#    (6818, "NP US,IN- Palladium-Item")
#    (6819, "NP US,NJ- The Daily Register")
#    (6820, "NP US,NY- Kings County Rural Gazette")
#    (6821, "NP US,CA- Daily Independent Journal")
#    (6822, "NP US,IN- The Star Press")
#    (6823, "NP US,FL- The Naples Daily News")
#    (6824, "NP US,LA- The Times-Picayune")
#    (6825, "NP US,IN- The News-Examiner")
#    (6826, "NP US,FL- South Florida Sun-Sentinel")
#    (6827, "NP US,NY- The Journal News")
#    (6828, "NP US,CA- Los Angeles Sentinel")
#    (6829, "NP US,FL- The Banner")
#    (6830, "NP US,NY- Long Island Daily Press")
#    (6831, "NP US,CA- The San Francisco Examiner")
#    (6832, "NP US,NY- New York Post")
#    (6833, "NP US,MF- The Baltimore Sun")
#    (6834, "NP US,OH- The Zanesville Signal")
#    (6835, "NP US,OH- The Piqua Daily Call")
#    (6836, "NP US,PA- The Gettysburg Times")
#    (6837, "NP US,NH- Nashua Telegraph")
#    (6838, "NP US,OH- Mansfield News Journal")
#    (6839, "NP US,OH- The Daily Advocate")
#    (6840, "NP US,OH- Miami Union")
#    (6841, "NP US,OH- Troy Daily News")
#    (6842, "NP US,KY- The Kentucky Enquirer")
#    (6843, "NP US,KY- Lexington Herald-Leader")
#    (6844, "NP US,OH- The Arcanum Times")
#    (6845, "NP US,OH- News Journal")
#    (6847, "NP US,OH- Dayton Daily News")
#    (6848, "NP US,OH- The Dayton Herald")
#    (6849, "NP US,TN- Evening Herald Courier")
#    (6850, "NP US,IN- The Journal-Press")
#    (6851, "NP US,IN- The Aurora Journal")
#    (6852, "NP US,OH- The Galion Inquirer")
#    (6853, "NP US,IN- The Indianapolis News")
#    (6854, "NP US,OH- The Journal News")
#    (6855, "NP US,CA- The Sacramento Bee")
#    (6856, "NP US,NJ- Asbury Park Press")
#    (6857, "NP US,NJ- The Ocean Star")
#    (6860, "NP US,WI- The Daily Tribune")
#    (6861, "NP US,FL- News-Press")
#    (6862, "NP US,NY- The Post-Standard")
#    (6863, "NP US,CA- The Los Angeles Times")
#    (6864, "NP US,IN- The Call-Leader")
#    (6865, "NP US,CA- The Desert Sun")
#    (6866, "NP US,OH- Springfield News-Sun")
#    (6867, "NP US,IN- Tipton County Tribune")
#    (6868, "NP US,AZ- Arizona Republic")
#    (6869, "NP US,OR- Statesman Journal")
#    (6870, "NP US,IN- Muncie Evening Press")
#    (6871, "NP US,FL- The Orlando Sentinel")
#    (6872, "NP US,FL- The Bradenton Herald")
#    (6873, "NP US,PA- The Morning Call")
#    (6875, "NP US,HI- West Hawaii Today")
#    (6877, "NP US,GA- The Atlanta Constitution")
#    (6878, "NP US,IN- The Daily Reporter")
#    (6879, "NP US,IN- The Commercial-Mail")
#    (6880, "NP US,IN- The Kokomo Tribune")
#    (6881, "NP US,NY- The Ithaca Journal")
#    (6882, "NP US,FL- Pensacola News Journal")
#    (6883, "NP US,MA- The Boston Globe")
#    (6884, "NP US,NY- Times Union")
#    (6885, "NP US,OH- The Circleville Herald")
#    (6886, "NP US,NY- Daily News")
#    (6887, "NP US,NJ- The Herald-News")
#    (6888, "NP US,NY- The Standard Union")
#    (6889, "NP US,FL- The Miami Herald")
#    (6890, "NP US,MI- Detroit Free Press")
#    (6892, "NP US,NV- Reno Gazette-Journal")
#    (6893, "NP US,TX- Corpus Christi Times")
#    (6894, "NP US,IN- The Brookville Democrat")
#    (6895, "NP US,CT- Hartford Courant")
#    (6896, "NP US,IN- The Terre Haute Tribune")
#    (6897, "NP US,IL- Pekin Daily Times ")
    ]
    

  for source in lumped_source_list:

    # specify the single source that is to get the new citations
    NewSourceID = source[0]
    src_name_identifier=  source[1]
   
    # List the sources which will be converted to citations of the 'new' source
    SQL_stmt = "SELECT SourceID FROM SourceTable WHERE Name LIKE ? AND TemplateID=?"
  #  SourcesToLump = GetListOfRows( db_connection, SQL_stmt, (src_name_identifier, old_src_TemplateID))
   
    cur = db_connection.cursor()
    subs=(src_name_identifier, old_src_TemplateID)
    cur.execute(SQL_stmt, subs)

    SourcesToLump = []
    for t in cur:
      for x in t:
        SourcesToLump.append(x)

    print ("\n\n\n number of source to process: ", len(SourcesToLump))
   
    #iterate through each of the old sources, converting each one separately
    for oldSrc in SourcesToLump:
        print ("old SourceID= " + str(oldSrc) )
        ConvertSource (db_connection, oldSrc, NewSourceID)
        print ("=====================================================")

  print ("total not found",G_count)
  input( "\n\nPress Enter to continue...")
  return 0


# ================================================================
def ConvertSource ( conn, oldSourceID, newSourceID):

  global G_count

  # For the given old source, count its citations 
  # Code as written only handles sources that have one citation and
  # no info in that citation is preserved.
  # Must make code changes to deal with #cits !=1 or preserve info in the citation.

  # print source name for confirmation
  SqlStmt = """
  SELECT Name
    FROM SourceTable
    WHERE SourceID = ?
  """
  cur = conn.cursor()
  cur.execute(SqlStmt, (newSourceID,))
  print ("source to get cited......" + cur.fetchone()[0]  )

  citationIDsToMove= getCitationsToMove(conn,oldSourceID)
  if len(citationIDsToMove) != 1:  return

  for citationIDToMove in citationIDsToMove:
    if ConvertCitation( conn, oldSourceID, newSourceID, citationIDToMove) == False:
       return

  # delete the old src (all of its citations have been moved to new source)
  SqlStmt = """
  DELETE from SourceTable
      WHERE SourceID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([oldSourceID, ]) )
  conn.commit()
  return

# ================================================================
def ConvertCitation( conn, oldSourceID, newSourceID, citationIDToMove ):
  global G_count

# Copy fields from old src record to the citationToMove
  SqlStmt = """
  UPDATE CitationTable
    SET (CitationName, ActualText, Comments, UTCModDate)
      = (SELECT Name, ActualText, Comments, UTCModDate FROM SourceTable WHERE SourceID = ?)
    WHERE CitationID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([oldSourceID, citationIDToMove]) )

  # Change owner & type columns for relevant web tags so they follow the citationToMove
  # takes all webtags linked to old source and add them to the citation in process
  # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE WEB TAGS.

  SqlStmt = """
  UPDATE URLTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  # Change owner & type for relevant media so they follow the citationToMove
  # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE MEDIA LINKS.

  SqlStmt = """
  UPDATE MediaLinkTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  #  move the existing citation to the new (existing) source
  SqlStmt = """
  UPDATE CitationTable
    SET SourceID = ?
    WHERE CitationID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([newSourceID, citationIDToMove]) )


  # Get the SourceTable.Fields BLOB from the oldSource to extract its data
  SqlStmt = """
  SELECT Fields
    FROM SourceTable
    WHERE SourceID = ?
  """

  oldSrcFields = {}
  srcRoot = getFieldsXmlDataAsDOM ( conn, SqlStmt, oldSourceID )
  srcFields = srcRoot.find("Fields")


#  print( ET.indent(srcRoot, space=" ", level=0) )
#  print(ET.tostring(srcRoot))
#  return

  for item in srcFields:
    if   item[0].text == "Household": oldSrcFields["Household"] = item[1].text
    elif item[0].text == "BirthDateHead": oldSrcFields["BirthDateHead"] = item[1].text
    elif item[0].text == "Place": oldSrcFields["Place"] = item[1].text
    elif item[0].text == "Location": oldSrcFields["Location"] = item[1].text
    elif item[0].text == "County": oldSrcFields["County"] = item[1].text
    elif item[0].text == "State": oldSrcFields["State"] = item[1].text
    elif item[0].text == "HouseNumber": oldSrcFields["HouseNumber"] = item[1].text
    elif item[0].text == "Street": oldSrcFields["Street"] = item[1].text
    elif item[0].text == "FilmNumber": oldSrcFields["FilmNumber"] = item[1].text
    elif item[0].text == "DateSheet": oldSrcFields["DateSheet"] = item[1].text
    elif item[0].text == "Page": oldSrcFields["Page"] = item[1].text
    elif item[0].text == "EnumerationDistrict": oldSrcFields["EnumerationDistrict"] = item[1].text
    elif item[0].text == "Dwelling": oldSrcFields["Dwelling"] = item[1].text
    elif item[0].text == "Family": oldSrcFields["Family"] = item[1].text
    elif item[0].text == "FS_ark": oldSrcFields["FS_ark"] = item[1].text
    elif item[0].text == "CD": oldSrcFields["CD"] = item[1].text
    elif item[0].text == "CitationDateUpdated": oldSrcFields["CitationDateUpdated"] = item[1].text
    elif item[0].text == "ANC_RID": oldSrcFields["ANC_RID"] = item[1].text

  print (oldSrcFields)


  # retrieve an empty sample XML chunk that has the citation fields of the source template used by the newSource
  # this means the citation does not retain any old data not explicitly saved.
  # Get the CitationTable.Fields BLOB for the new source (must be pre-existing and named "sample citation")
  SqlStmt = """
  SELECT CT.Fields
    FROM CitationTable CT
    JOIN SourceTable ST ON CT.SourceId = ST.SourceID
    WHERE CT.SourceID = ? AND CT.CitationName = "sample citation"
  """
  newRoot = getFieldsXmlDataAsDOM ( conn, SqlStmt, newSourceID)
  if newRoot == None:
    print( "cannot find the 'sample citation'")
    return False
  newFields = newRoot.find("Fields")

  # now fill the XML with values
  for item in newFields:
    if   item[0].text == "Household":           item[1].text = oldSrcFields["Household"]
    elif item[0].text == "DateHeadBirth":       item[1].text = oldSrcFields["BirthDateHead"]
    elif item[0].text == "DateSheet":           item[1].text = oldSrcFields["DateSheet"]
    elif item[0].text == "PlaceFull":           item[1].text = oldSrcFields["Place"]
    elif item[0].text == "PlaceLocality":       item[1].text = oldSrcFields["Location"]
    elif item[0].text == "PlaceCounty":         item[1].text = oldSrcFields["County"]
    elif item[0].text == "PlaceStreet":         item[1].text = oldSrcFields["Street"]
    elif item[0].text == "PlaceHouseNumber":    item[1].text = oldSrcFields["HouseNumber"]
    elif item[0].text == "EnumerationDistrict": item[1].text = oldSrcFields["EnumerationDistrict"]
    elif item[0].text == "SheetLineNumber":     item[1].text = oldSrcFields["Page"]
    # elif item[0].text == "DwellingSN":          item[1].text = oldSrcFields["Dwelling"]
    elif item[0].text == "DwellingSN":          item[1].text = oldSrcFields["Family"]
    elif item[0].text == "FilmRollNumber":      item[1].text = oldSrcFields["FilmNumber"]
    elif item[0].text == "ANC_SRC_ID":          item[1].text = oldSrcFields["ANC_RID"]
    elif item[0].text == "FS_SRC_ID":           item[1].text = oldSrcFields["FS_ark"]
    elif item[0].text == "DateCitation":        item[1].text = oldSrcFields["CitationDateUpdated"]
  #  elif item[0].text == "CD":                  item[1].text = oldSrcFields["CD"]


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
  RunSqlNoResult( conn, SqlStmt, tuple([ET.tostring(newRoot), citationIDToMove]) )
  conn.commit()
  return True


# ================================================================
def RunSqlNoResult ( conn, SqlStmt, myTuple):
    cur = conn.cursor()
    cur.execute(SqlStmt, myTuple)


# ================================================================
def getFieldsXmlDataAsDOM ( conn, SqlStmt, rowID ):
  cur = conn.cursor()
  cur.execute(SqlStmt, (rowID,))
  XmlTxt_raw = cur.fetchone()
  if XmlTxt_raw == None: return None
  XmlTxt=XmlTxt_raw[0].decode()

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
def getCitationsToMove ( conn, oldSourceID):
  # get citations for oldSourceID
  SqlStmt = """
  SELECT CitationID
    FROM CitationTable
    WHERE SourceID = ?
  """
  cur = conn.cursor()
  cur.execute(SqlStmt, (oldSourceID,))
  citationsIDs = cur.fetchall()

  citationIDsToMove= []

  # change the data structure from list of tuples to list of ints
  for each in citationsIDs:
      citationIDsToMove.append(each[0])

  return citationIDsToMove


# ================================================================
def GetListOfRows ( conn, SqlStmt):
    # SqlStmt should return a set of single values
    cur = conn.cursor()
    cur.execute(SqlStmt)

    result = []
    for t in cur:
      for x in t:
        result.append(x)
    return result


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
