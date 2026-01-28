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
        r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts")
    TOP_LEVEL_CONFIG_NAME = r"_top_level_build_config.yaml"
    VERSION_REPLACE_TEXT = r'UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE'
    doc_folder = REPO_ROOT_PATH / "doc"

    try:
        time_stamp = time_stamp_now("file")
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
    

    # Process each doc template
    for project in project_list:
        project_dir_path = REPO_ROOT_PATH / project
        template_file_path = doc_folder / F"DocOutline_{project}.txt"
        # doc_file_path = doc_folder / F"docFinal-{project}.txt"
        doc_file_path = project_dir_path/ "ReadMe.txt"
        lib_file_path = doc_folder / "DocLibrary_snippets.txt"
        print (template_file_path)
        with open(template_file_path, 'r') as doc_template, \
             open(doc_file_path, 'w') as doc_final:
            
            for line in doc_template:
                if line.startswith("INCLUDE: "):
                    label = line[9::]
                    for lib_line in get_snippet(label, lib_file_path):
                        doc_final.write(lib_line)
                else:
                    doc_final.write(line)

    pause_with_message()
    return


def get_snippet(label, lib_file):

    term = "=========================================================================DIV80=="
    snippet = []
    with open(lib_file, 'r') as lib:
        for line in lib:
            skip_label = False
            if line.startswith(label):
                # start accumulating text
                save = True
                skip_label = True
            if line.startswith(term):
                save = False
            if save and not skip_label:
                snippet.append(line)
    if len(snippet) == 0:
        raise Exception(F'Snippet "{label}" not found in Text library file.')
    return snippet


# ===================================================DIV60==
def time_stamp_now(type=""):

    # return a TimeStamp string
    now = datetime.now()
    if type == '':
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string

# ===================================================DIV60==
def pause_with_message(message=None):

    if (message != None):
        input(str(message))
    else:
        input("\nPress the <Enter> key to exit...")
    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
