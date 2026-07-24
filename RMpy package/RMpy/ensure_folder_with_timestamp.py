import os
import datetime
import shutil

def ensure_folder_with_timestamp(path: str) -> str:
    """
    Handles:
      - Normal paths (C:\folder)
      - UNC paths (\\server\share\folder)
      - Extended-length UNC (\\?\\UNC\\server\\share\\folder)
      - Extended-length local (\\?\\C:\\folder)

    Behavior:
      1. If path exists and is a folder:
            rename it by appending -YYYYMMDD-HHMMSS
            recreate the folder at the original path
            verify the new folder exists and is writable
      2. If path does NOT exist:
            check parent; if parent is a folder, create the folder
            verify the new folder exists and is writable

    Returns:
        The renamed path (if rename occurred) or the created path.
    """

    # --- Helper: detect extended-length UNC prefix ---
    def is_extended_unc(p: str) -> bool:
        return p.startswith(r"\\?\UNC\")

    def is_extended_local(p: str) -> bool:
        return p.startswith(r"\\?\") and not p.startswith(r"\\?\UNC\")

    # --- Safe trailing slash removal ---
    if is_extended_unc(path):
        prefix = r"\\?\UNC"
        rest = path[len(prefix):]
        rest = rest.rstrip("\\/")
        path = prefix + rest
    else:
        path = path.rstrip("\\/")

    # --- Case 1: Path exists ---
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Path exists but is not a folder: {path}")

        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        new_path = f"{path}-{ts}"

        # Rename the existing folder
        shutil.move(path, new_path)

        # Recreate the original folder
        os.mkdir(path)

        # Validate writability
        _validate_writable(path)

        return new_path  # return renamed path

    # --- Case 2: Path does not exist → check parent ---
    if is_extended_unc(path):
        prefix = r"\\?\UNC"
        rest = path[len(prefix):]
        parent_rest = os.path.dirname(rest)
        parent = prefix + parent_rest
    else:
        parent = os.path.dirname(path)

    if not os.path.exists(parent):
        raise FileNotFoundError(f"Parent directory does not exist: {parent}")

    if not os.path.isdir(parent):
        raise NotADirectoryError(f"Parent exists but is not a folder: {parent}")

    # Create the folder
    os.mkdir(path)

    # Validate folder is writable.
    _validate_writable(path)

    return path


def _validate_writable(path: str):
    """
    Ensures the directory exists and is writable by attempting
    to create and delete a temporary file inside it.
    """
    testfile = os.path.join(path, ".__write_test__")

    try:
        with open(testfile, "w") as f:
            f.write("test")
        os.remove(testfile)
    except Exception as e:
        raise PermissionError(f"Folder exists but is not writable: {path}") from e
