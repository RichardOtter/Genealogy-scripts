#!/usr/bin/env python3
"""Copy a predefined set of files and folders into a destination folder.

This utility is intended for creating a real-copy test set in a single folder.
Each entry in COPY_DEFINITIONS can point to a source file or folder and give it
an explicit destination name.

This script is located in: dev util scripts/local DB folder/
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Navigate to repo root from script location
SCRIPT_DIR = Path(__file__).resolve().parent  # dev util scripts
DEV_UTIL_DIR = SCRIPT_DIR.parent  # dev util scripts
REPO_ROOT = DEV_UTIL_DIR.parent  # repo root

# COMMENTED OUT: Old hardcoded source path - keep for potential future use
# TEST_BUILDS_FLDR = Path(r"C:\Users\rotter\dev\Genealogy\Genealogy-scripts Releases\in test phase")
# TEST_BUILD_FLDR_1 = "Release RM_Utilities_Suite_v1.1.0 ALPHA 2026-11-19_154416"
# TEST_BUILD_FLDR_2 = "RM_Utilities_Suite_v1.1.0 ALPHA"
# SOURCE_FOLDER = TEST_BUILDS_FLDR / TEST_BUILD_FLDR_1 / TEST_BUILD_FLDR_2

# Find the latest Release folder in the script's current directory
def find_source_folder(start_dir: Path) -> Path:
    """Find the latest Release folder in the script's directory."""
    release_folders = sorted(
        [d for d in start_dir.iterdir() if d.is_dir() and d.name.startswith("Release ")],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    if not release_folders:
        raise FileNotFoundError(f"No Release folders found in {start_dir}")
    
    latest = release_folders[0]
    suite_folders = [d for d in latest.iterdir() if d.is_dir() and not d.name.startswith(".")]
    
    if not suite_folders:
        raise FileNotFoundError(f"No suite folder found in {latest}")
    
    return suite_folders[0]

SOURCE_FOLDER = find_source_folder(SCRIPT_DIR)

DESTINATION_DIR = Path(r"C:\Users\rotter\Genealogy\GeneDB\SW")

COPY_DEFINITIONS = [
    {
        "source": SOURCE_FOLDER / "Run SQL" / "RMpy",
        "name": "RMpy",
    },
    {
        "source": SOURCE_FOLDER / "Test external files" / "TestExternalFiles.py",
        "name": "1  TestExternalFiles.py",
    },
    {
        "source": SOURCE_FOLDER / "External Files Info" / "ExternalFilesInfo.py",
        "name": "2  ExternalFilesInfo.py",
    },
    {
        "source": SOURCE_FOLDER / "Group from SQL" / "GroupFromSQL.py",
        "name": "3 GroupFromSQL.py",
    },
    {
        "source": SOURCE_FOLDER / "Color from group" / "ColorFromGroup.py",
        "name": "4 ColorFromGroup.py",
    },
    {
        "source": SOURCE_FOLDER / "Run SQL" / "RunSQL.py",
        "name": "5 RunSQL.py",
    },
    {
        "source": SOURCE_FOLDER / "Modify citation list" / "ModifyCitationList.py",
        "name": "99  ModifyCitationList.py",
    },
    {
        "source": SOURCE_FOLDER / "Change source for citation" / "ChangeSrcForCitation.py",
        "name": "99  ChangeSrcForCitation.py",
    },
    {
        "source": SOURCE_FOLDER / "Mini report" / "MiniReport.pyw",
        "name": "99  MiniReport.pyw",
    }

]


def copy_item(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() or destination.is_symlink():
        if destination.is_dir() and not destination.is_symlink():
            shutil.rmtree(destination)
        else:
            destination.unlink()

    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)


def pause_with_message(message: str = None) -> None:
    if message is not None:
        print(str(message))
    input("\nPress the <Enter> key to continue...")


def confirm_action(prompt: str) -> bool:
    """Ask user for yes/no confirmation."""
    while True:
        response = input(f"\n{prompt} (yes/no): ").strip().lower()
        if response in ("yes", "y"):
            return True
        elif response in ("no", "n"):
            return False
        print("Please enter 'yes' or 'no'.")


def main() -> int:
    try:
        source_folder = SOURCE_FOLDER
        print(f"Source folder: {source_folder}\n")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        pause_with_message()
        return 1

    destination_dir = DESTINATION_DIR.expanduser().resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)

    print(f"Destination folder: {destination_dir}\n")
    print("=" * 80)
    print(f"Copy from: {source_folder}")
    print(f"Copy to:   {destination_dir}")
    print("=" * 80)

    # Ask for confirmation
    if not confirm_action("Proceed with copying?"):
        print("Copy cancelled.")
        pause_with_message()
        return 0

    # Perform the copy
    print("\nCopying files...")
    for entry in COPY_DEFINITIONS:
        # Reconstruct source path relative to SOURCE_FOLDER
        try:
            source_path = source_folder / str(entry["source"]).split(str(SOURCE_FOLDER))[-1].lstrip("/\\")
        except:
            source_path = entry["source"].expanduser().resolve()
        
        destination_path = destination_dir / entry["name"]

        print(f"  Copying {source_path.name}...")
        try:
            copy_item(source_path, destination_path)
        except FileNotFoundError as e:
            print(f"  ERROR: Source not found: {source_path}")
            if destination_path.exists():
                if destination_path.is_dir():
                    shutil.rmtree(destination_path)
                else:
                    destination_path.unlink()
                print(f"  Deleted destination: {destination_path.name}")
            else:
                print(f"  Destination does not exist")
        except Exception as e:
            print(f"  ERROR: {e}")
            print(f"  Skipping {source_path.name}")

    pause_with_message("Copy complete.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        raise SystemExit(130)
    except Exception as exc:  # pragma: no cover - simple CLI error reporting
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
