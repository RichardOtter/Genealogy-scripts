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
SCRIPT_DIR = Path(__file__).resolve().parent  # local DB folder
DEV_UTIL_DIR = SCRIPT_DIR.parent  # dev util scripts
REPO_ROOT = DEV_UTIL_DIR.parent  # repo root

# Edit this list to change which items are copied and what they are called.
TEST_BUILDS_FLDR = Path(r"C:\Users\rotter\dev\Genealogy\Genealogy-scripts Releases\in test phase")

TEST_BUILD_FLDR_1 = "Release RM_Utilities_Suite_v1.1.0 ALPHA 2026-11-18_193724"
TEST_BUILD_FLDR_2 = "RM_Utilities_Suite_v1.1.0 ALPHA"

SOURCE_FOLDER = TEST_BUILDS_FLDR / TEST_BUILD_FLDR_1 / TEST_BUILD_FLDR_2

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


def main() -> int:
    destination_dir = DESTINATION_DIR.expanduser().resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)

    print(f"Destination folder: {destination_dir}")

    for entry in COPY_DEFINITIONS:
        source_path = entry["source"].expanduser().resolve()
        destination_path = destination_dir / entry["name"]

        print(f"- {source_path} -> {destination_path}")
        copy_item(source_path, destination_path)
        print("  copied")

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
