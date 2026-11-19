import sys
from pathlib import Path

import os
import yaml    # type: ignore
# from datetime import datetime

# this file lives in the dir:  repo root/dev util scripts/local DB folder
# the top level yaml config file is in: repo root/dev util scripts
# the .lnk files are in: repo root/dev util scripts/local DB folder (same as this script)

def main():

    # if a file already exists, delete it
    keep_orig = False

    # CONSTANTS
    REPO_ROOT_PATH = Path(
        r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts")
    TOP_LEVEL_CONFIG_NAME = r"_top_level_build_config.yaml"

    # Shortcut files to copy to each project's DB folder
    db_shortcut_files = [
        "_DB_Copy1 PRODUCTION.lnk",
        "_DB_Copy2 LOCAL TEST DATA.lnk",
        "_DB_Copy2 TEST DATA.lnk",
        "_DB_Copy3 RESET.lnk"
    ]

    doc_folder = REPO_ROOT_PATH / "doc"
    links_folder = doc_folder / "Links"

    try:
        # Navigate paths from this script's new location
        script_dir = Path(__file__).resolve().parent  # local DB folder
        dev_util_fldr_path = script_dir.parent  # dev util scripts
        local_db_folder_path = script_dir  # Same folder as this script
        
        top_level_config_path = dev_util_fldr_path / TOP_LEVEL_CONFIG_NAME
        
        if (not Path(top_level_config_path).exists()):
            print("Can't find the top level config file.\n")
            return

        with open(top_level_config_path, 'r') as top_lev:
            doc = yaml.safe_load(top_lev)
            suite_version = doc["SuiteVersion"]
            suite_name = doc["SuiteName"]
            project_root_dir_path = doc["ProjectRootDirPath"]
            project_list = doc["ProjectList"]
    except Exception as e:
        print(f"Problem getting the values from the top level yaml file.\n{e}\n")
        return
    

    # Process each project
    for project in project_list:
        project_dir_path = REPO_ROOT_PATH / project

        # # create a hard link in the docs folder for each ReadMe
        # try:
        #     os.link(project_dir_path / 'ReadMe.txt', links_folder / F"DocFull_{project}.txt")
        # except FileExistsError:
        #     print(f"Error: The file '{links_folder / F"DocFull_{project}"}' already exists.")

        #create a DB folder in each project folder
        project_DB_path = project_dir_path / "DB"
        try:
            os.mkdir(project_DB_path)
        except FileExistsError:
            print(F"Directory '{project_DB_path}' already exists.")

        # make hardlinks to the db utility shortcut files in each DB folder
        for shortcut_file in db_shortcut_files:
            shortcut_path = project_DB_path / shortcut_file
            try:
                # Always remove existing file to allow overwrite
                try:
                    os.remove(shortcut_path)
                except FileNotFoundError:
                    pass
                os.link(local_db_folder_path / shortcut_file, shortcut_path)
            except Exception as e:
                print(f"Error creating '{shortcut_path}': {e}")

    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    try:
        main()
    finally:
        # Always pause before exit
        try:
            input("\nPress the <Enter> key to exit...")
        except (EOFError, OSError):
            pass

# ===================================================DIV60==
