import sys
from pathlib import Path
sys.path.append( r'.' )

from datetime import datetime
import sqlite3
import configparser
import subprocess
import traceback

import RMpy.common as RMc  # type: ignore

# ===================================================DIV60==
def launcher(utility_info):

    db_connection = None
    report_display_app = None

    # ===========================================DIV50==
    # Errors go to console window
    # ===========================================DIV50==
    try:
        # Configuration file location- 
        # either specified by quoted command line argument or default
        # encoded as UTF-8 (no BOM).
        # see   https://docs.python.org/3/library/configparser.html
        if len(sys.argv) >2: 
            raise RMc.RM_Py_Exception(
                "\n\nERROR: Only one parameter allowed.\n"
                "       Enclose the configuration file path parameter with \n"
                "       double quotes if it contains spaces or special characters.")
        if len(sys.argv) == 2:
            config_file_path = Path(sys.argv[1])
        else:
            config_file_name = utility_info["config_file_name"]
            config_file_path = (
                RMc.get_current_directory(utility_info["script_path"]) 
                    / config_file_name )
        # Check that config file exists and that it is readable & valid.
        if not config_file_path.exists():
            raise RMc.RM_Py_Exception(
                f'\n\nERROR: The configuration file: "{config_file_path}"'
                F" was not found.\n\n")

        config = configparser.ConfigParser(empty_lines_in_values=False,
                                           interpolation=None)
        try:
            config.read(config_file_path, 'utf-8')
        except:
            raise RMc.RM_Py_Exception(
                F"\n\nERROR: The {config_file_name}"
                F" file contains a format error and cannot be parsed.\n")
        try:
            report_path = config['FILE_PATHS']['REPORT_FILE_PATH']
        except:
            raise RMc.RM_Py_Exception(
                F"\n\nERROR: REPORT_FILE_PATH must be specified in the"
                F" {config_file_name}\n\n")
        try:
            # Use UTF-8 encoding for the report file. Test for write-ability
            open(report_path,  mode='w', encoding='utf-8')
        except:
            raise RMc.RM_Py_Exception(
                F"\n\nERROR: Cannot create the report file as specified:\n"
                F"{report_path}\n\n")

    except RMc.RM_Py_Exception as e:
        RMc.pause_with_message(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        RMc.pause_with_message(
            F"\n\nERROR: Application failed. Please email error report:\n\n "
            F"{e} \n\nto the author")
        return 1

    # open the already tested report file
    report_file = open(report_path,  mode='w', encoding='utf-8')

    # ===========================================DIV50==
    # Errors from here forward, go to Report File
    # ===========================================DIV50==
    try:
        try:
            report_display_app = Path(config['FILE_PATHS']['REPORT_FILE_DISPLAY_APP'])
        except:
            pass
        if report_display_app is not None and not report_display_app.exists():
            bad_path = report_display_app
            report_display_app = None
            raise RMc.RM_Py_Exception(
                F"ERROR: Path for report file display app not found:"
                F" {bad_path}")

        try:
            database_path = Path(config['FILE_PATHS']['DB_PATH'])
        except:
            raise RMc.RM_Py_Exception('ERROR: DB_PATH must be specified.')
        if not database_path.exists():
            raise RMc.RM_Py_Exception(
                F"ERROR: Database path not found: {database_path}\n\n\n")


        if utility_info["RMNOCASE_required"]:
            try:
                rmnocase_path = Path(config['FILE_PATHS']['RMNOCASE_PATH'])
            except:
                raise RMc.RM_Py_Exception(
                    'ERROR: RMNOCASE_PATH must be specified.')
            if not rmnocase_path.exists():
                raise RMc.RM_Py_Exception(
                    f'ERROR: Path for RMNOCASE extension (unifuzz64.dll)\n'
                    f'not found: {rmnocase_path}\n\n')
            
        if utility_info["RegExp_required"]:
            try:
                regexp_path = config['FILE_PATHS']['REGEXP_PATH']
            except:
                raise RMc.RM_Py_Exception(
                    'ERROR: REGEXP_PATH must be specified.')
            if not rmnocase_path.exists():
                raise RMc.RM_Py_Exception(
                    f'ERROR: Path for REGEXP extension not found:'
                    f' {rmnocase_path}\n\n')

        # RM database file info
        file_modification_time = datetime.fromtimestamp(
            database_path.stat().st_mtime)

        if utility_info["RMNOCASE_required"] and not utility_info["RegExp_required"]:
            db_connection = RMc.create_db_connection(database_path, [rmnocase_path])
        elif not utility_info["RMNOCASE_required"] and utility_info["RegExp_required"]:
            db_connection = RMc.create_db_connection(database_path, [regexp_path])
        elif utility_info["RMNOCASE_required"] and utility_info["RegExp_required"]:
            db_connection = RMc.create_db_connection(database_path, [rmnocase_path, regexp_path])
        else:
            db_connection = RMc.create_db_connection(database_path, None)

        # write header to report file
        format = "%Y-%m-%d %H:%M:%S"
        report_file.write(
                F"Report generated at      = {RMc.time_stamp_now()}\n"
                F"Utility name             = {utility_info["utility_name"]}\n"
                F"Utility version          = v{utility_info["utility_version"]}\n"
                F"Python version           = v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
                F"SQLite library version   = v{RMc.get_SQLite_library_version(db_connection)}\n"
                F"Database last changed on = {file_modification_time.strftime(format)}\n"
                F"Database processed       = {database_path.resolve()}\n"
                F"\n\n\n")


        # Call the function pointer to run the functional part of the app
        utility_info["run_features_function"](config, db_connection, report_file)


        if utility_info["allow_db_changes"]:
            db_connection.commit()

    except KeyboardInterrupt:
        # Just quit the app
        return 1
    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        if str(e) == "database is locked":
            divider = "="*50 + "===DIV60=="
            div_line= divider + "\n"
            report_file.seek(0, 0)
            report_file.write( F"{div_line}{div_line}{div_line}"
                F"Database is locked.\nRootsMagic is preventing the group updates\n"
                F"Close RootsMagic and rerun this app.\n"
                F"{div_line}{div_line}{div_line}\n\n\n\n")
        else:
            report_file.write(
                F"ERROR: SQL execution returned an error \n\n{e}")
        return 1
    except RMc.RM_Py_Exception as e:
        report_file.write(str(e))
        return 1
    except Exception as e:
        traceback.print_exception(e, file=report_file)
        report_file.write(
            "\n\n" "ERROR: Application failed. Please email report file to author. ")
        return 1

    finally:
        if db_connection is not None:
            db_connection.close()
        report_file.close()
        if report_display_app is not None:
            # display the report file
            subprocess.Popen([report_display_app, report_path])
    return 0


# ===================================================DIV60==

