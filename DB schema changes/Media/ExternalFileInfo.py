import sys
from pathlib import Path
sys.path.append(str(Path.resolve(Path(__file__).resolve().parent / '../../RMpy package')))

import RMpy.common as RMc       # noqa #type: ignore
import RMpy.launcher            # noqa #type: ignore
from RMpy.common import q_str   # noqa #type: ignore
import RMpy.gitignore  # type: ignore

import xml.etree.ElementTree as ET
import hashlib

import os
import ctypes
import datetime


MJD_OFFSET =  2_415_018.5   # the microsoft standard used in Excel
FILETIME_EPOCH = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)

# ===================================================DIV60==
#  Globals

# when set, these will both be a pathlib.Path
G_media_directory_path = None
G_db_file_folder_path = None

G_DEBUG = False


# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"]     = "InsertNewRecords" 
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

    global G_db_file_folder_path
    global G_media_directory_path

    # used only in function expand_relative_dir_path, but no access to config there.
    parent_dir = Path(config['FILE_PATHS']['DB_PATH']).parent
    # get the absolute path in case the DB_PATH was relative
    G_db_file_folder_path = parent_dir.resolve()

    # test option values conversion to boolean
    # if missing, treated as false
    try:
        config['OPTIONS'].getboolean('MAIN')
        config['OPTIONS'].getboolean('UPDATE')
        config['OPTIONS'].getboolean('TESTING_USE_LOCAL_RM_XML')

        if config['OPTIONS'].getboolean('TESTING_MODE_USE_TEST_MEDIA_FOLDER'):
            # app is in test mode.
            # Set the path to the RM media folder preference setting
            # overriding what might be in the production RM xml config file
            G_media_directory_path =parent_dir.parent / "media" / 'testing' / 'media folder'
            report_file.write(f"Test mode: TESTING_MODE_USE_TEST_MEDIA_FOLDER\n")
            report_file.write(f"Media folder ={G_media_directory_path}\n\n")

    except:
        raise RMc.RM_Py_Exception(
            "One of the OPTIONS values could not be interpreted as either on or off.\n")


    # Run all of the requested options.
    if config['OPTIONS'].getboolean('MAIN'):
        main_feature(config, db_connection, report_file)

    section("FINAL", "", report_file)


# ===================================================DIV60==
def main_feature(config, db_connection, report_file):

    feature_name = "Update populate"
    missing_items = 0
    C_hash_type = "MD5"

    try:
        config['OPTIONS'].getboolean('UPDATE')
    except:
        raise RMc.RM_Py_Exception(
            "One of the OPTIONS values could not be interpreted as either on or off.\n")

    update_aux_table = False
    if config['OPTIONS'].getboolean('UPDATE'):
        update_aux_table = True
        report_file.write(f"UPDATE mode: AuxMultimediaTable will be updated to match files in filesystem\n")



    section("START", feature_name, report_file)

    count_missing_fs_files = 0
    count_missing_aux_rows = 0
    count_aux_rows = 0
    count_hash_differs = 0
    count_mod_date_differs = 0
    count_create_date_differs = 0

# TEST files in TESTING_MODE_USE_TEST_MEDIA_FOLDER  mode:
# ignore the files not found messages (although they constitute test cases)
#     C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\Media\testing\media folder\sub1\DBTest file s1 01.jpg
#     C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\Media\testing\media folder\sub1\DBTest file s1 02.jpg
#     C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\Media\testing\media folder\sub1\DBTest file s1 03.jpg


    # for each file link in the multimedia table
    cur = get_full_info_db_file_list(db_connection)
    # SELECT  MediaID, MediaPath, MediaFile, AuxMediaID, FileSize, FileTimeCreation, FileTimeModification, HashType, Hash
    for row in cur:

        media_id            = int(row[0] or 0)
        file_fldr_path_db   = str(row[1])
        file_name           = str(row[2])
        aux_media_id        = row[3]
        file_size           = int(row[4] or 0)
        file_create_date    = float(row[5] or 0)
        file_mod_date       = float(row[6] or 0)
        hash_type           = str(row[7])
        hash                = str(row[8])

        if len(file_fldr_path_db) == 0 or len(file_name) == 0:
            continue

        file_fldr_path = expand_relative_dir_path(file_fldr_path_db)
        file_path = file_fldr_path / file_name

        if not file_path.exists() or not file_path.is_file():
            # Just increment the counter and write to log. Nothing else to do.
            count_missing_fs_files += 1
            report_file.write(f"Missing file: {file_path}\n")
            continue

        # get data from files in filesystem
        file_data = get_file_info_tuple(file_path)
        fs_file_size        = file_data[0]
        fs_file_create_date = file_data[1]
        fs_file_mod_date    = file_data[2]

        fs_hash = get_file_MD5(file_path)

    # Data now available 
    # from database
        #  media_id
        #  file_fldr_path
        #  file_name
        #  file_size
        #  file_time_create
        #  file_time_mod
        #  hash_type
        #  hash
    # from filesystem
        #  fs_file_size
        #  fs_file_time_create
        #  fs_file_time_mod
        #  fs_md5


        sub_vars = {
            "media_ID" : media_id,
            "file_size" : fs_file_size,
            "file_creation_date" : fs_file_create_date,
            "file_modification_date" : fs_file_mod_date,
            "hash_type" : C_hash_type,
            "hash_value" : fs_hash
        }

        #   is there an Aux table row?
        if aux_media_id is None :
            count_missing_aux_rows += 1
            report_file.write(f"Missing AuxMultimediaTable row  {media_id=}\n{file_path}\n\n")
            if update_aux_table:
               update_aux_row(db_connection, sub_vars)
            else:
                continue
        
        #compare values
        if hash != fs_hash:
            count_hash_differs += 1
            report_file.write(f"hash differs  {media_id=}\n{file_path}\n\n")
            if update_aux_table:
               update_aux_row(db_connection, sub_vars)

        if file_mod_date != fs_file_mod_date:
            count_mod_date_differs += 1
            report_file.write(f"file_mod_date differs  {media_id=}\n{file_path}\n\n")
            if update_aux_table:
               update_aux_row(db_connection, sub_vars)

        if file_create_date != fs_file_create_date:
            count_create_date_differs += 1
            report_file.write(f"file_create_date differs  {media_id=}\n{file_path}\n\n")
            if update_aux_table:
               update_aux_row(db_connection, sub_vars)

        count_aux_rows += 1


    report_file.write(f"\n\n\n{count_missing_aux_rows=}\n\n")
    report_file.write(f"{count_aux_rows=}\n\n")

    return


# ===================================================DIV60==
def initial_populate_feature(config, db_connection, report_file):

    feature_name = "initial populate"
    missing_items = 0

    section("START", feature_name, report_file)


    # for each file link in the multimedia table
    cur = get_db_file_list(db_connection)
    #   SELECT  MediaID, MediaPath, MediaFile
    for row in cur:
        if len(str(row[1])) == 0 or len(str(row[2])) == 0:
            continue
        media_ID = row[0]
        dir_path_original = row[1]
        file_name = row[2]
        dir_path = expand_relative_dir_path(dir_path_original)
        file_path = dir_path / file_name

        file_data = get_file_info_tuple(file_path)

        # take hash
        BUF_SIZE = 65536  # reads in 64kb chunks

        md5 = hashlib.md5()
        # or sha1 = hashlib.sha1()

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)

        sub_vars = {
            "media_ID" : media_ID,
            "file_size" : file_data[0],
            "file_creation_date" : file_data[1],
            "file_modification_date" : file_data[2],
            "hash_type" : "MD5",
            "hash_value" : md5.hexdigest()
        }

        SQL_stmt = """
        INSERT INTO AuxMultimediaTable
        VALUES (
        :media_ID,
        :hash_type,
        :hash_value,
        :file_creation_date,
        :file_modification_date,
        julianday('now') - 2415018.5
        );
        """

        cur = db_connection.cursor()
        cur.execute(SQL_stmt, sub_vars)

    return


# ===================================================DIV60==
def get_file_MD5(file_path):

    # take hash
    BUF_SIZE = 65536  # reads in 64kb chunks

    md5 = hashlib.md5()
    # or sha1 = hashlib.sha1()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()



# ===================================================DIV60==
def get_db_folder_list(dbConnection):

    SqlStmt = """
  SELECT  DISTINCT MediaPath
  FROM MultimediaTable
    ORDER BY MediaPath
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def get_db_file_list(db_connection):

    SqlStmt = """
  SELECT  MediaID, MediaPath, MediaFile
  FROM MultimediaTable
    ORDER BY MediaPath, MediaFile COLLATE NOCASE
  """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)
    return cur

# ===================================================DIV60==
def update_aux_row(db_connection, db_values):

        SQL_stmt = """
        INSERT OR IGNORE INTO AuxMultimediaTable
        VALUES (
        :media_ID,
        :file_size,
        :file_creation_date,
        :file_modification_date,
        :hash_type,
        :hash_value,
        julianday('now') - 2415018.5
        );
        """

        cur = db_connection.cursor()
        cur.execute(SQL_stmt, db_values)




# ===================================================DIV60==
def get_full_info_db_file_list(db_connection):

    SqlStmt = """
  SELECT  MediaID, MediaPath, MediaFile,
            AuxMediaID, FileSize, FileTimeCreation, FileTimeModification,
            HashType, Hash, mmt.UTCModDate, amt.UTCModDate
  FROM MultimediaTable AS mmt
  LEFT JOIN AuxMultimediaTable AS amt ON MediaID = AuxMediaID
    ORDER BY MediaID
  """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def report_empty_paths(db_connection, report_file):

    # First check database for empty paths or filenames
    # easier to handle them now than later

    SqlStmt = """
    SELECT  MediaPath, MediaFile, Caption, Description
    FROM MultimediaTable
    WHERE MediaPath == ''
       OR MediaFile == ''COLLATE NOCASE
    """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)

    rows = cur.fetchall()
    if len(rows) != 0:
        report_file.write(
            f"{len(rows)} entires with blank filename or path found:\n\n")
        for row in rows:
            # MediaPath, MediaFile, Caption, Description
            report_file.write(
                f"Path       = {row[0]} \n"
                f"File Name  = {row[1]} \n"
                f"Caption    = {row[2]} \n"
                f"Description= {row[3]} \n\n")



# ===================================================DIV60==
def section(pos, name, report_file):

    Divider = "="*60 + "===DIV70=="
    if pos == "START":
        text = f"\n{Divider}\n=== Start of {RMc.q_str(name)} listing\n\n"
    elif pos == "END":
        text = f"\n=== End of {RMc.q_str(name)} listing\n"
    elif pos == "FINAL":
        text = f"\n{Divider}\n=== End of Report\n"
    else:
        raise RMc.RM_Py_Exception(
            "INTERNAL ERROR: Section position not correctly defined")

    report_file.write(text)
    report_file.flush()
    return


# ===================================================DIV60==
def expand_relative_dir_path(in_path_str: str) -> Path:

    # deal with relative paths in RootsMagic v8 and later databases
    # RM7 path are always absolute and will never be processed here

    global G_media_directory_path
    # use this global as sort of a static constant. Want it initialed once.

    path = str(in_path_str)
    # input parameter path should always be of type str, output will be Path
    # note when using Path / operator, second operand should not be absolute

    if path[0] == "?":
        if G_media_directory_path is None:
            G_media_directory_path = get_media_directory()
        if len(path) == 1:
            absolute_path = G_media_directory_path
        else:
            absolute_path = Path(G_media_directory_path) / path[2:]

    elif path[0] == "~":
        absolute_path = Path(path).expanduser()

    elif path[0] == "*":
        if len(path) == 1:
            absolute_path = G_db_file_folder_path
        else:
            absolute_path = G_db_file_folder_path / path[2:]

    else:
        absolute_path = Path(path)

    return absolute_path


# ===================================================DIV60==
def get_media_directory() ->Path:

    # TODO make this work for future releases of RM
    # Maybe get a dir listing of rm folders

    #  Relies on the RM installed xml file containing application preferences
    #  File location set by RootsMagic installer
    RM_Config_FilePath_13 = Path(r"AppData\Roaming\RootsMagic\Version 13\RootsMagicUser.xml")
    RM_Config_FilePath_12 = Path(r"AppData\Roaming\RootsMagic\Version 12\RootsMagicUser.xml")
    RM_Config_FilePath_11 = Path(r"AppData\Roaming\RootsMagic\Version 11\RootsMagicUser.xml")
    RM_Config_FilePath_10 = Path(r"AppData\Roaming\RootsMagic\Version 10\RootsMagicUser.xml")
    RM_Config_FilePath_9 =  Path(r"~ppData\Roaming\RootsMagic\Version 9\RootsMagicUser.xml")
    RM_Config_FilePath_8 =  Path(r"~ppData\Roaming\RootsMagic\Version 8\RootsMagicUser.xml")

    media_folder_path = "RM8 or later not installed"

#  If xml settings file for RM 8 - 10 not found, return the mediaPath containing the
#  error message. It will never be used for RM 7 because RM 7 and earlier
#  do not need to know the media folder path.

#  Potential problem if RM 8, 9 or 10 both installed and they have different
#  media folders specified. The highest version number path found is used here.

#  TODO Could base this off of the database version number, but that's not readily available.

    home_dir = Path.home()
    xmlSettingsPath = home_dir / RM_Config_FilePath_11
    if not xmlSettingsPath.exists():
        xmlSettingsPath = home_dir / RM_Config_FilePath_10
        if not xmlSettingsPath.exists():
            xmlSettingsPath = home_dir / RM_Config_FilePath_9
            if not xmlSettingsPath.exists():
                xmlSettingsPath = home_dir / RM_Config_FilePath_8
                if not xmlSettingsPath.exists():
                    return media_folder_path

    root = ET.parse(xmlSettingsPath)
    media_folder_path_ele = root.find("./Folders/Media")
    if media_folder_path_ele is None:
        raise RMc.RM_Py_Exception(
            "Media Folder not set in RM folder preferences.")
    media_folder_path = media_folder_path_ele.text

    return Path(media_folder_path)



# ===================================================DIV60==


# ---------------------------------------------------------
# MJD conversion helpers (float version)
# ---------------------------------------------------------

def datetime_to_mjd_float(dt):
    """Convert datetime → Microsoft Modified Julian Date (float)."""
    if dt.tzinfo is None:
        dt = dt.astimezone()
    dt = dt.astimezone(datetime.timezone.utc)

    year = dt.year
    month = dt.month
    day_fraction = (
        dt.day +
        dt.hour / 24 +
        dt.minute / 1440 +
        dt.second / 86400 +
        dt.microsecond / 86400_000_000
    )

    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + (A // 4)

    jd = (
        int(365.25 * (year + 4716)) +
        int(30.6001 * (month + 1)) +
        day_fraction + B - 1524.5
    )

    return jd - MJD_OFFSET


def mjd_float_to_datetime(mjd):
    """Convert Microsoft MJD float → datetime (UTC)."""
    jd = mjd + MJD_OFFSET

    Z = int(jd + 0.5)
    F = (jd + 0.5) - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - (alpha // 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715

    day_int = int(day)
    frac = day - day_int
    seconds = frac * 86400

    return datetime.datetime(
        year, month, day_int,
        tzinfo=datetime.timezone.utc
    ) + datetime.timedelta(seconds=seconds)



# ---------------------------------------------------------
# NTFS timestamp helpers
# ---------------------------------------------------------

def dt_to_filetime(dt):
    dt_utc = dt.astimezone(datetime.timezone.utc)
    delta = dt_utc - FILETIME_EPOCH
    return int(delta.total_seconds() * 10_000_000)


def set_ntfs_times(path, created_dt, modified_dt):
    kernel32 = ctypes.windll.kernel32

    handle = kernel32.CreateFileW(
        str(path),
        0x100,  # FILE_WRITE_ATTRIBUTES
        0x01 | 0x02,
        None,
        3,
        0x02000000,
        None
    )
    if handle == -1:
        raise OSError(f"Unable to open file: {path}")

    def to_ft_struct(dt):
        return ctypes.c_uint64(dt_to_filetime(dt))

    ctime = to_ft_struct(created_dt)
    mtime = to_ft_struct(modified_dt)

    kernel32.SetFileTime(
        handle,
        ctypes.byref(ctime),
        None,
        ctypes.byref(mtime)
    )
    kernel32.CloseHandle(handle)

# ---------------------------------------------------------
# MAIN FUNCTIONS (float MJD version, using modern stat fields)
# ---------------------------------------------------------

def get_file_info_tuple(path):
    """
    Return (file_size, created_mjd_float, modified_mjd_float) for a file.
    Uses st_ctime_ns and st_mtime_ns (nanosecond precision).
    """
    stat = os.stat(path)

    created = datetime.datetime.fromtimestamp(
        stat.st_ctime_ns / 1e9, tz=datetime.timezone.utc
    )
    modified = datetime.datetime.fromtimestamp(
        stat.st_mtime_ns / 1e9, tz=datetime.timezone.utc
    )

    return (
        stat.st_size,
        datetime_to_mjd_float(created),
        datetime_to_mjd_float(modified)
    )


def set_file_dates_from_mjd_float(path, mjd_tuple):
    """
    Take (created_mjd_float, modified_mjd_float) and set NTFS timestamps.
    """
    created_mjd, modified_mjd = mjd_tuple

    created_dt = mjd_float_to_datetime(created_mjd)
    modified_dt = mjd_float_to_datetime(modified_mjd)

    set_ntfs_times(path, created_dt, modified_dt)

# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
