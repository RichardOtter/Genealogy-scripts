import os
import stat
import ctypes
import json
from pathlib import Path
import yaml    # type: ignore
from datetime import datetime
from pathlib import Path
from send2trash import send2trash

# As a first step, this build script builds from local source
# it does not get "fresh files" from GitHub

# this file lives in the dir:  repo root/dev util scripts/doc
# the top level yaml config file is in: repo root/dev util scripts
# the doc folder structure is at: repo root/doc

# ===================================================DIV60==


def main():

    # CONSTANTS
    # Navigate up two levels from this script's location to repo root
    SCRIPT_DIR = Path(__file__).resolve().parent
    DEV_UTIL_DIR = SCRIPT_DIR.parent
    REPO_ROOT_PATH = DEV_UTIL_DIR.parent

    TOP_LEVEL_CONFIG_NAME = r"projects-to-build.yaml"
    VERSION_REPLACE_TEXT = r'DOC_VERSION_NUMBER_RM_UTILS_OVERRIDE'
    doc_folder = REPO_ROOT_PATH / "doc"

    try:
        time_stamp = time_stamp_now("file")
        top_level_config_path = DEV_UTIL_DIR / TOP_LEVEL_CONFIG_NAME

        if (not Path(top_level_config_path).exists()):
            print("Can't find the top level config file.\n")

        with open(top_level_config_path, 'r') as top_lev:
            doc = yaml.safe_load(top_lev)
            suite_version = doc["SuiteVersion"]
            build_type = doc.get("BuildType")
            suite_name = doc["SuiteName"]
            project_root_dir_path = doc["ProjectRootDirPath"]
            project_list = doc["ProjectList"]
    except:
        raise Exception(
            "Problem getting the values from the top level yaml file.\n")

    if build_type not in ("DEV", "ALPHA", "BETA", "RELEASE"):
        print(
            f"ERROR: BuildType must be DEV, ALPHA, BETA, or RELEASE; got {build_type!r}.")
        pause_with_message()
        return 1

    is_release = build_type == "RELEASE"
    version_suffix = f" {build_type}" if build_type and not is_release else ""
    snippet_prefix = "╋" if build_type in ("DEV", "ALPHA") else ""

    try:
        # Ensure docs-generated folder exists
        doc_built_folder = doc_folder / "docs-generated"
        doc_built_folder.mkdir(parents=True, exist_ok=True)

        # Create VS Code settings to mark generated files as read-only
        create_vscode_readonly_settings(REPO_ROOT_PATH, doc_built_folder)

        # Clear any existing files in the docs-generated folder
        for existing_file in doc_built_folder.glob("*"):
            if existing_file.is_file():
                # Remove read-only attribute before sending to trash
                os.chmod(existing_file, stat.S_IWRITE)
                send2trash(str(existing_file))

        # Process each doc template
        for project in project_list:
            template_file_path = doc_folder / \
                "doc-sources" / F"DocOutline_{project}.txt"
            doc_file_path = doc_built_folder / f"ReadMe_{project}.txt"
            lib_file_path = doc_folder / "docs-reusable-content.txt"
            project_dir_path = REPO_ROOT_PATH / project
            util_info_path = project_dir_path / "_util_info.yaml"

            # Get utility version from project's _util_info.yaml
            utility_version = "Unknown"
            if util_info_path.exists():
                with open(util_info_path, 'r') as util_info:
                    util_doc = yaml.safe_load(util_info)
                    if util_doc and "Version" in util_doc:
                        utility_version = util_doc["Version"]

            # Parse variables from the template
            variables = parse_variables(template_file_path)

            print(f"Building: {doc_file_path}")
            with open(template_file_path, 'r') as doc_template, \
                    open(doc_file_path, 'w') as doc_final:

                in_variables_section = False
                for line in doc_template:
                    # Skip the variables section
                    if line.startswith("█_VARIABLES:"):
                        in_variables_section = True
                        continue
                    if line.startswith("█_END_VARIABLES"):
                        in_variables_section = False
                        continue
                    if in_variables_section:
                        continue

                    if line.startswith("█_INCLUDE: "):
                        label = line[11::]
                        for lib_line in get_snippet(label, lib_file_path):
                            # Apply variable substitution to included snippet
                            substituted_line = substitute_variables(
                                lib_line, variables)
                            doc_final.write(snippet_prefix + substituted_line)
                    else:
                        # Apply variable substitution to doc content
                        substituted_line = substitute_variables(
                            line, variables)
                        doc_final.write(substituted_line)

                # Add version and build date footer
                doc_final.write("\n\n")
                doc_final.write("=" * 80 + "\n")
                doc_final.write(
                    f"Suite Version: {suite_version}{version_suffix}\n")
                doc_final.write(
                    f"Utility Version: {utility_version}{version_suffix}\n")
                doc_final.write(f"Built: {time_stamp_now()}\n")
                doc_final.write("=" * 80 + "\n")

            # Make the generated file read-only
            os.chmod(doc_file_path, stat.S_IREAD)
    except (Exception) as e:
        print(e)
    finally:
        pause_with_message()
    return

# ===================================================DIV60==


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
    if (message != None):
        print(str(message))
    if launched_from_explorer():
        input("\n" "Press the <Enter> key to continue...")
    return


# ===================================================DIV60==
def create_vscode_readonly_settings(repo_root, doc_built_folder):
    """Create VS Code settings to mark generated files as read-only"""
    vscode_dir = repo_root / ".vscode"
    settings_file = vscode_dir / "settings.json"

    vscode_dir.mkdir(parents=True, exist_ok=True)

    # Read existing settings if file exists
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {}

    # Add files.readonlyInclude setting for generated docs
    # Use relative path from repo root to docs-generated folder
    readonly_pattern = "doc/docs-generated/**"
    if "files.readonlyInclude" not in settings:
        settings["files.readonlyInclude"] = {}

    settings["files.readonlyInclude"][readonly_pattern] = True

    # Write updated settings
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)


# ===================================================DIV60==
def parse_variables(template_file_path):
    """Parse the █_VARIABLES: section and return a dictionary of variables"""
    variables = {}
    with open(template_file_path, 'r') as f:
        in_variables_section = False
        for line in f:
            if line.startswith("█_VARIABLES:"):
                in_variables_section = True
                continue
            if line.startswith("█_END_VARIABLES"):
                in_variables_section = False
                break
            if in_variables_section:
                # Parse "KEY = VALUE" format
                if "=" in line:
                    parts = line.split("=", 1)
                    key = parts[0].strip()
                    value = parts[1].strip()
                    variables[key] = value
    return variables


# ===================================================DIV60==
def substitute_variables(text, variables):
    """Replace all {VARIABLE_NAME} with corresponding values"""
    result = text
    for key, value in variables.items():
        result = result.replace("{" + key + "}", value)
    return result


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    raise SystemExit(main())


# ===================================================DIV60==
