import os
import ctypes
import shutil
from pathlib import Path
import yaml  # type: ignore

# This script copies ReadMe files from Doc/Doc-built staging folder
# to their respective project folders, overwriting existing files.
#
# This allows working on ReadMe content without immediately affecting
# the project folders.
#
# This file lives in: repo root/dev util scripts/doc
# Config file is in: repo root/dev util scripts
# Doc folder is at: repo root/doc

# ===================================================DIV60==
def main():

    # CONSTANTS
    # Navigate up two levels from this script's location to repo root
    SCRIPT_DIR = Path(__file__).resolve().parent
    DEV_UTIL_DIR = SCRIPT_DIR.parent
    REPO_ROOT_PATH = DEV_UTIL_DIR.parent
    
    TOP_LEVEL_CONFIG_NAME = r"_top_level_build_config.yaml"
    doc_folder = REPO_ROOT_PATH / "doc"
    doc_built_folder = doc_folder / "Doc-built"

    try:
        top_level_config_path = DEV_UTIL_DIR / TOP_LEVEL_CONFIG_NAME

        if not Path(top_level_config_path).exists():
            raise FileNotFoundError("Can't find the top level config file.\n")

        with open(top_level_config_path, 'r') as top_lev:
            doc = yaml.safe_load(top_lev)
            project_list = doc["ProjectList"]

    except Exception as e:
        print(f"ERROR: Problem getting values from config file: {e}")
        pause_with_message()
        return 1

    try:
        # Copy each ReadMe file from Doc-built to project folder
        for project in project_list:
            source_file = doc_built_folder / f"ReadMe_{project}.txt"
            destination_file = REPO_ROOT_PATH / project / "ReadMe.txt"

            # Check source exists
            if not source_file.exists():
                raise FileNotFoundError(
                    f"Source file not found: {source_file}")

            # Copy file (overwrites destination)
            shutil.copy2(source_file, destination_file)
            print(f"✓ Copied: {project}")

    except Exception as e:
        print(f"\nERROR: {e}")
        print("Stopping on first error.")
        pause_with_message()
        return 1

    print("\nAll ReadMe files copied successfully to project folders.")
    pause_with_message()
    return 0


# ===================================================DIV60==
def launched_from_explorer():
    # Check how many processes are attached to the console
    arr = (ctypes.c_uint * 10)()
    count = ctypes.windll.kernel32.GetConsoleProcessList(arr, 10)

    # VS Code always sets TERM_PROGRAM=vscode
    in_vscode = os.environ.get("TERM_PROGRAM", "").lower() == "vscode"

    # Explorer launch: count == 2 AND not VS Code
    return count == 2 and not in_vscode


# ===================================================DIV60==
def pause_with_message(message=None):
    # Don't pause when running from a terminal or when input output is redirected
    if message is not None:
        print(str(message))
    if launched_from_explorer():
        input("\nPress the <Enter> key to continue...")
    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)

# ===================================================DIV60==
