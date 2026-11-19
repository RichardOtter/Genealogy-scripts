import os
import ctypes
import subprocess
from pathlib import Path
import yaml  # type: ignore

# This script uses git to discard any changes made to ReadMe.txt files
# in project folders, restoring them to the last committed state.
#
# Local modified files are sent to Windows Recycle Bin (trash) before
# the git version is restored, allowing recovery if needed.
#
# Requires: pip install send2trash
#
# This file lives in: repo root/dev util scripts/doc
# Config file is in: repo root/dev util scripts

try:
    from send2trash import send2trash
    HAS_SEND2TRASH = True
except ImportError:
    HAS_SEND2TRASH = False

# ===================================================DIV60==
def main():

    # CONSTANTS
    # Navigate up two levels from this script's location to repo root
    SCRIPT_DIR = Path(__file__).resolve().parent
    DEV_UTIL_DIR = SCRIPT_DIR.parent
    REPO_ROOT_PATH = DEV_UTIL_DIR.parent
    
    TOP_LEVEL_CONFIG_NAME = r"_top_level_build_config.yaml"

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

    if not HAS_SEND2TRASH:
        print("ERROR: send2trash module not installed.")
        print("Run: pip install send2trash")
        print("Then try again.")
        pause_with_message()
        return 1

    try:
        # Discard changes for each project's ReadMe.txt
        for project in project_list:
            readme_file = REPO_ROOT_PATH / project / "ReadMe.txt"
            relative_path = f"{project}/ReadMe.txt"

            # If file exists and has local changes, send to trash before git checkout
            if readme_file.exists():
                # Check if file has uncommitted changes
                result_status = subprocess.run(
                    ["git", "status", "--porcelain", relative_path],
                    cwd=str(REPO_ROOT_PATH),
                    capture_output=True,
                    text=True
                )
                
                # If status output is not empty, file has changes
                if result_status.stdout.strip():
                    try:
                        send2trash(str(readme_file))
                        print(f"  → Sent to trash: {project}/ReadMe.txt")
                    except Exception as e:
                        raise RuntimeError(
                            f"Failed to send {relative_path} to trash: {e}")

            # Run git checkout to restore from git
            result = subprocess.run(
                ["git", "checkout", relative_path],
                cwd=str(REPO_ROOT_PATH),
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"Git checkout failed for {relative_path}:\n{result.stderr}")

            print(f"✓ Discarded changes: {project}")

    except Exception as e:
        print(f"\nERROR: {e}")
        print("Stopping on first error.")
        pause_with_message()
        return 1

    print("\nAll ReadMe changes have been discarded.")
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
