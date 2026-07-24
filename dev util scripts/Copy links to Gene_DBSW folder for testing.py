#!/usr/bin/env python3
"""Create link files to a predefined set of files in a destination folder.

This utility is intended for creating quick test links into a single folder.
Each entry in LINK_DEFINITIONS can point to a source file and give it a
custom destination name.

Examples:
    python "Copy links to Gene_DBSW folder for testing.py"
    python "Copy links to Gene_DBSW folder for testing.py" --dest "C:/temp/Gene_DBSW_links" --overwrite
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


# Edit this list to change which files are linked and what they are called.
# Paths are hard-coded below and do not require command-line arguments.
SOURCE_FOLDER = Path(
    r"C:\Users\rotter\dev\Genealogy\Genealogy-scripts Releases\in test phase\Release RM_Utilities_Suite_v1.0.3 ALPHA 2026-07-23_222655\RM_Utilities_Suite_v1.0.3 ALPHA"
)
DESTINATION_DIR = Path(r"C:\Users\rotter\Genealogy\GeneDB\SW")

LINK_DEFINITIONS = [
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
    }
]


def create_link(source: Path, destination: Path, link_type: str, overwrite: bool) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() or destination.is_symlink():
        if not overwrite:
            raise FileExistsError(f"Destination already exists: {destination}")
        if destination.is_dir() and not destination.is_symlink():
            raise IsADirectoryError(
                f"Destination is a directory: {destination}")
        destination.unlink()

    if link_type == "symlink":
        try:
            os.symlink(source, destination)
        except (OSError, NotImplementedError):
            # Fall back to a hard link if symlink creation is unavailable.
            os.link(source, destination)
    elif link_type == "hardlink":
        os.link(source, destination)
    else:
        raise ValueError(f"Unsupported link type: {link_type}")


def main() -> int:
    destination_dir = DESTINATION_DIR.expanduser().resolve()

    print(f"Destination folder: {destination_dir}")
    print("Link type: symlink")

    for entry in LINK_DEFINITIONS:
        source_path = entry["source"].expanduser().resolve()
        destination_path = destination_dir / entry["name"]

        print(f"- {source_path} -> {destination_path}")
        create_link(source_path, destination_path, "symlink", True)
        print("  created")

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
