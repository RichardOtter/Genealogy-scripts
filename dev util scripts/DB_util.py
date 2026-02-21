import os
import shutil
import sys
import time
import msvcrt
import stat
import argparse


def main():
    # Handle double-click (no args)
    if len(sys.argv) == 1:
        print("ERROR: Missing required argument.")
        print("Usage: python dbtool.py [production|test|reset]")
        print()
        input("Press Enter to exit...")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Database sync/reset tool for TEST DB environment."
    )
    parser.add_argument(
        "mode",
        choices=["production", "test", "reset"],
        help="Mode: 'production', 'test', or 'reset'"
    )
    args = parser.parse_args()

    # ---------------------------------------------------------
    # Constants
    # ---------------------------------------------------------
    DB_EXTEN = "rmtree"
    DB_BU_EXTEN = "rmtreeBU"

    PRODUCTION_DB_PATH = r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"
    TEST_DB_PATH       = r"C:\Users\rotter\dev\Genealogy\Test Data\General test\TestData-RMpython -v11 -REDUCED.rmtree"

    DEV_DB_PATH = "."

    # Determine folder-based DB names
    script_dir = os.getcwd()
    parent_dir = os.path.dirname(script_dir)
    curr_dir_name = os.path.basename(parent_dir)

    DEV_DB_NAME = f"TEST-{curr_dir_name}"
    DEV_DB_BACKUP = f"BACKUP_TEST-{curr_dir_name}"

    dev_db_file = os.path.join(DEV_DB_PATH, f"{DEV_DB_NAME}.{DB_EXTEN}")
    dev_db_backup_file = os.path.join(DEV_DB_PATH, f"{DEV_DB_BACKUP}.{DB_BU_EXTEN}")

    # ---------------------------------------------------------
    # RESET MODE
    # ---------------------------------------------------------
    if args.mode == "reset":
        print("Resetting TEST database from local backup copy")

#        # Diagnostics
#        print("\n=== PATH DIAGNOSTICS ===")
#        print("Working directory:", full(os.getcwd()))
#        print("Parent directory:", full(parent_dir))
#        print("Current folder name:", repr(curr_dir_name))
#        print()
#        print("Target TEST DB file:", full(dev_db_file))
#        print("  Exists:", os.path.exists(full(dev_db_file)))
#        print("  Is file:", os.path.isfile(full(dev_db_file)))
#        print("  Is dir:", os.path.isdir(full(dev_db_file)))
#        print()
#        print("Backup DB file:", full(dev_db_backup_file))
#        print("  Exists:", os.path.exists(full(dev_db_backup_file)))
#        print("  Is file:", os.path.isfile(full(dev_db_backup_file)))
#        print("  Is dir:", os.path.isdir(full(dev_db_backup_file)))
#        print("========================\n")

        # Delete TEST DB (read-only allowed)
        safe_delete(dev_db_file, allow_readonly=True)

        # Ensure backup exists
        if not os.path.exists(full(dev_db_backup_file)):
            fail(f"Backup file does not exist: {full(dev_db_backup_file)}")

        # Copy backup → TEST
        safe_copy(
            dev_db_backup_file,
            dev_db_file,
            "Restoring TEST DB from local backup failed."
        )

        print("Reset completed successfully.")
        timeout_with_break(5)
        return

    # ---------------------------------------------------------
    # SYNC MODE (production or test)
    # ---------------------------------------------------------
    if args.mode == "production":
        source_file = PRODUCTION_DB_PATH
        print("Syncing from PRODUCTION database")
    else:
        source_file = TEST_DB_PATH
        print("Syncing from TEST database")

    if not os.path.exists(full(source_file)):
        fail(f"Selected source file does not exist: {full(source_file)}")

    print(f"Using source DB: {full(source_file)}")

    # Delete existing dev DB + backup
    safe_delete(dev_db_file)
    safe_delete(dev_db_backup_file)

    # Copy source → dev
    safe_copy(
        source_file,
        dev_db_file,
        "Copying source DB to dev DB failed."
    )

    if  source_file == TEST_DB_PATH:
        # make sure that the database is not ReadOnly
        clear_readonly(dev_db_file)

    # Copy dev → backup
    safe_copy(
        dev_db_file,
        dev_db_backup_file,
        "Creating local backup copy failed."
    )


    print("Sync completed successfully.")
    timeout_with_break(5)


# ---------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------

def fail(msg):
    print()
    print(f"ERROR: {msg}")
    print()
    input("Press Enter to exit...")
    sys.exit(1)

def full(path):
    """Return fully resolved absolute path."""
    return os.path.abspath(path)

def safe_delete(path, allow_readonly=False):
    """
    Delete a file and verify it is gone.
    If allow_readonly=True, clear read-only attribute before deleting.
    """
    resolved = full(path)

    if os.path.exists(resolved):

        if allow_readonly:
            try:
                os.chmod(resolved, stat.S_IWRITE)
            except Exception:
                pass  # deletion will catch any remaining issues

        try:
            os.remove(resolved)
        except Exception as e:
            fail(f"DELETE FAILED (locked, read-only, or in use): {resolved}\n{e}")

        if os.path.exists(resolved):
            fail(f"DELETE FAILED (still exists): {resolved}")

def safe_copy(src, dst, errmsg):
    """Copy a file and verify success."""
    src_resolved = full(src)
    dst_resolved = full(dst)

    try:
        shutil.copy2(src_resolved, dst_resolved)
    except Exception as e:
        fail(f"{errmsg}\nSource: {src_resolved}\nDest: {dst_resolved}\n{e}")

    if not os.path.exists(dst_resolved):
        fail(f"{errmsg} (destination missing after copy)\nDest: {dst_resolved}")

    if os.path.getsize(dst_resolved) == 0:
        fail(f"{errmsg} (destination file is zero bytes)\nDest: {dst_resolved}")

def timeout_with_break(seconds):
    """Emulate CMD 'timeout /t N' where any keypress interrupts the wait."""
    print(f"Waiting {seconds} seconds... (press any key to continue)")
    end_time = time.time() + seconds

    while time.time() < end_time:
        if msvcrt.kbhit():
            msvcrt.getch()  # clear keypress
            return
        time.sleep(0.1)


def clear_readonly(path):
    """Remove the read-only attribute from a file on Windows."""
    try:
        # Get current attributes
        attrs = os.stat(path).st_mode

        # If read-only bit is set, clear it
        if not (attrs & stat.S_IWRITE):
            os.chmod(path, stat.S_IWRITE)
    except Exception as e:
        raise RuntimeError(f"Failed to clear read-only attribute: {path}\n{e}")

if __name__ == "__main__":
    main()