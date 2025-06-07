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

    # CONSTANTS
    REPO_ROOT_PATH = Path(
        r"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts")
    VERSION_REPLACE_TEXT = r'UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE'
    TOP_LEVEL_CONFIG_NAME = r"_top_level_build_config.yaml"
    RM_PATH = REPO_ROOT_PATH / "RM"

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
    
    doc_fldr = REPO_ROOT_PATH / "RM" / "doc"

    # Process each project
    for project in project_list:
        project_dir_path = RM_PATH / project

        # create a hard link in the docs folder for each ReaMe
        os.link(project_dir_path / 'ReadMe.txt', doc_fldr / F"doc-{project}")

        #create a DB folder in each project folder
        os.mkdir(project_dir_path / "DB")
        # make a hardlink to the db utility cmd files in each DB
        os.link( dev_util_fldr_path / "_DB get fresh copy.cmd", project_dir_path / "DB" )
        os.link( dev_util_fldr_path / "_DB reset test db.cmd", project_dir_path / "DB" )

    return

# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
