import sys
from pathlib import Path
sys.path.append(str(Path.resolve(Path(__file__).resolve().parent / '../RMpy package')))

import RMpy.common as RMc       # noqa #type: ignore
import RMpy.launcher            # noqa #type: ignore
from RMpy.common import q_str   # noqa #type: ignore


G_DEBUG = False

# These are used by the time conversion routines
MMJD_OFFSET =  2_415_018.5   # the microsoft standard used in Excel

# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"]     = "MoveCitations" 
    utility_info["utility_version"]  = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"]      = Path(__file__).parent.resolve()
    utility_info["run_features_function"]  = run_selected_features
    utility_info["allow_db_changes"]       = True
    utility_info["RMNOCASE_required"]      = False
    utility_info["RMNOCASE_optional"]      = False
    utility_info["RegExp_required"]        = False
    utility_info["RegExp_optional"]        = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    section("START", "Move citations", report_file)

    # test option values conversion to boolean
    # if missing, treated as false
    try:
        config['OPTIONS'].getboolean('TESTING_USE_LOCAL_RM_XML')

    except:
        raise RMc.RM_Py_Exception(
            "One of the OPTIONS values could not be interpreted as either on or off.\n")


    # for now, just run by setting options here

#    group_name = "everyone"
    group_name = "bad: FACT-Census: bad description or note"

    direction="name_to_person"
#    direction="person_to_name"


    process_group(db_connection, group_name, direction, delete_original=True)

    section("FINAL", "", report_file)


# ===================================================DIV60==
def process_group(conn, group_name, direction="name_to_person", delete_original=True):
    """
    direction = "name_to_person" or "person_to_name"
    """

    person_ids = get_person_ids_for_group(conn, group_name)

    for pid in person_ids:
        if direction == "name_to_person":
            move_name_citations_to_person(conn, pid, delete_original)
        elif direction == "person_to_name":
            move_person_citations_to_name(conn, pid, delete_original)
        else:
            raise ValueError("direction must be 'name_to_person' or 'person_to_name'")


# ===================================================DIV60==
def get_person_ids_for_group(conn, group_name):
    cur = conn.cursor()

    # Special case: everyone
    if group_name.lower() == "everyone":
        cur.execute("SELECT PersonID FROM PersonTable")
        return [row[0] for row in cur.fetchall()]

    # Look up GroupID from TagTable
    cur.execute("""
        SELECT TagValue
        FROM TagTable
        WHERE TagName COLLATE NOCASE = ? COLLATE NOCASE
          AND TagType = 0
    """, (group_name,))
    row = cur.fetchone()
    if not row:
        raise ValueError(f"Group '{group_name}' not found")

    group_id = row[0]

    # Get ranges from GroupTable
    cur.execute("""
        SELECT StartID, EndID
        FROM GroupTable
        WHERE GroupID = ?
    """, (group_id,))

    person_ids = []
    for start_id, end_id in cur.fetchall():
        person_ids.extend(range(start_id, end_id + 1))

    return person_ids


# ===================================================DIV60==
def section(pos, name, report_file):

    Divider = "="*60 + "===DIV70=="
    if pos == "START":
        text = F"\n{Divider}\n=== Start of {RMc.q_str(name)} listing\n\n"
    elif pos == "END":
        text = F"\n=== End of {RMc.q_str(name)} listing\n"
    elif pos == "FINAL":
        text = F"\n{Divider}\n=== End of Report\n"
    else:
        raise RMc.RM_Py_Exception(
            "INTERNAL ERROR: Section position not correctly defined")

    report_file.write(text)
    report_file.flush()
    return


# ---------------------------------------------------------
def local_time_str(mjd):
    return mjd_float_to_datetime(mjd, LocalTZ=True).strftime("%Y-%m-%d %H:%M:%S")


# ===================================================DIV60==
def move_name_citations_to_person(conn, person_id, delete_original=True):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO CitationLinkTable (CitationID, OwnerType, OwnerID, SortOrder, Quality, IsPrivate, Flags, UTCModDate)
        SELECT cl.CitationID,
               0 AS OwnerType,
               nt.OwnerID AS PersonID,
               cl.SortOrder, cl.Quality, cl.IsPrivate, cl.Flags,
               julianday('now') - 2415018.5
        FROM CitationLinkTable cl
        JOIN NameTable nt ON nt.NameID = cl.OwnerID
        WHERE cl.OwnerType = 7
          AND nt.IsPrimary = 1
          AND nt.OwnerID = ?
          AND NOT EXISTS (
                SELECT 1 FROM CitationLinkTable cl2
                WHERE cl2.CitationID = cl.CitationID
                  AND cl2.OwnerType = 0
                  AND cl2.OwnerID = nt.OwnerID
          );
    """, (person_id,))

    if delete_original:
        cur.execute("""
            DELETE FROM CitationLinkTable
            WHERE OwnerType = 7
              AND OwnerID = (SELECT NameID FROM NameTable WHERE OwnerID = ? AND IsPrimary = 1);
        """, (person_id,))


# ===================================================DIV60==
def move_person_citations_to_name(conn, person_id, delete_original=True):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO CitationLinkTable (CitationID, OwnerType, OwnerID, SortOrder, Quality, IsPrivate, Flags, UTCModDate)
        SELECT cl.CitationID,
               7 AS OwnerType,
               nt.NameID,
               cl.SortOrder, cl.Quality, cl.IsPrivate, cl.Flags,
               julianday('now') - 2415018.5
        FROM CitationLinkTable cl
        JOIN NameTable nt ON nt.OwnerID = cl.OwnerID AND nt.IsPrimary = 1
        WHERE cl.OwnerType = 0
          AND cl.OwnerID = ?
          AND NOT EXISTS (
                SELECT 1 FROM CitationLinkTable cl2
                WHERE cl2.CitationID = cl.CitationID
                  AND cl2.OwnerType = 7
                  AND cl2.OwnerID = nt.NameID
          );
    """, (person_id,))

    if delete_original:
        cur.execute("""
            DELETE FROM CitationLinkTable
            WHERE OwnerType = 0
              AND OwnerID = ?;
        """, (person_id,))


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
