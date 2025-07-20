import os
from pathlib import Path
import yaml    # type: ignore
from datetime import datetime
from pathlib import Path

# As a first step, this build script builds from local source
# it does not get "fresh files" from GitHub

# this file lives in the dir:  repo root/dev util scripts
# the top level yaml config file is also here.


def main():

    keep_orig = False

    # CONSTANTS
    REPO_ROOT_PATH = Path(
        r"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts")
    VERSION_REPLACE_TEXT = r'UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE'
    TOP_LEVEL_CONFIG_NAME = r"_top_level_build_config.yaml"
    RM_PATH = REPO_ROOT_PATH / "RM"

    file1="_DB get fresh copy of Production.cmd"
    file2="_DB reset test db.cmd"
    file3="_DB get fresh copy of TestData.cmd"

    try:
        dev_util_fldr_path= REPO_ROOT_PATH / "dev util scripts"
        top_level_config_path = dev_util_fldr_path / TOP_LEVEL_CONFIG_NAME
        
        if (not Path(top_level_config_path).exists()):
            print("Can't find the top level config file.\n")

        with open(top_level_config_path, 'r') as top_lev:
            doc = yaml.safe_load(top_lev)
            suite_version = doc["SuiteVersion"]
            suite_name = doc["SuiteName"]
            project_root_dir_path = doc["ProjectRootDirPath"]
            project_list = doc["ProjectList"]
    except:
        print("Problem getting the values from the top level yaml file.\n")
        exit()
    
    doc_folder = REPO_ROOT_PATH / "RM" / "doc"

    # Process each project
    for project in project_list:
        project_dir_path = RM_PATH / project

        # create a hard link in the docs folder for each ReaMe
        try:
            os.link(project_dir_path / 'ReadMe.txt', doc_folder / F"DocFull_{project}")
        except FileExistsError:
            print(f"Error: The file '{doc_folder / F"DocFull_{project}"}' already exists.")

        #create a DB folder in each project folder
        project_DB_path = project_dir_path / "DB"
        try:
            os.mkdir(project_DB_path)
        except FileExistsError:
            print(F"Directory '{project_DB_path}' already exists.")
        # make a hardlink to the db utility cmd files in each DB folder


        try:
            if not keep_orig:
                try:
                    os.remove(project_DB_path / file1 )
                except FileNotFoundError:
                    continue
            os.link( dev_util_fldr_path / file1, project_DB_path / file1 )
        except FileExistsError:
            print(f"Error: The file '{project_DB_path / file1}' already exists.")

        try:
            if not keep_orig:
                try:
                    os.remove(project_DB_path / file2 )
                except FileNotFoundError:
                    continue
            os.link( dev_util_fldr_path / file2, project_DB_path / file2 )
        except FileExistsError:
            print(f"Error: The file '{project_DB_path / file2}' already exists.")

        try:
            if not keep_orig:
                try:
                    os.remove(project_DB_path / file3 )
                except FileNotFoundError:
                    continue
            os.link( dev_util_fldr_path / file3, project_DB_path / file3 )
        except FileExistsError:
            print(f"Error: The file '{project_DB_path / file3}' already exists.")

    return

# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
