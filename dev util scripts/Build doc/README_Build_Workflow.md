# ReadMe Build Workflow

This directory contains three scripts that work together to manage ReadMe documentation for all projects listed in _top_level_build_config.yaml in a safe, staged workflow.

## Workflow Overview

```
Edit DocOutline_{project}.txt 
         ↓
  Build ReadMe files.py
         ↓
  Doc/Doc-built/ReadMe_{project}.txt (staging)
         ↓
  Copy-ReadMe-to-Projects.py
         ↓
  {project}/ReadMe.txt (actual)
```

## Scripts

### 1. **Build ReadMe files.py** (Modified)

Builds ReadMe files from templates in `Doc/Doc-templates/` and snippets in `Doc/DocLibrary_snippets.txt`

**What it does:**
- Reads: `Doc/Doc-templates/DocOutline_{project}.txt`
- Processes INCLUDE directives to insert snippets
- **Outputs to:** `Doc/Doc-built/ReadMe_{project}.txt` (not to project folders!)
- Adds version number and build date footer to each file
- Creates `Doc/Doc-built/` folder if it doesn't exist
- Reads utility version from each project's `_util_info.yaml`

**Run:** `python "Build ReadMe files.py"`

**Output example:**
```
================================================================================
Suite Version: 1.1.0 ALPHA
Utility Version: 1.2.2
Built: 2026-11-19 10:15:14
================================================================================
```

---

### 2. **Copy-ReadMe-to-Projects.py** (New)

Copies staged ReadMe files from `Doc/Doc-built/` to project folders

**What it does:**
- Reads: `Doc/Doc-built/ReadMe_{project}.txt`
- Copies to: `{project}/ReadMe.txt` (overwrites existing)
- Processes all projects from `_top_level_build_config.yaml`
- Console output only (no log files)
- **Stops on first error**

**Run:** `python "Copy-ReadMe-to-Projects.py"`

**Output example:**
```
✓ Copied: Change source for citation
✓ Copied: Change source template
✓ Copied: Color from group
...
All ReadMe files copied successfully to project folders.
```

---

### 3. **Discard-ReadMe-Changes.py** (New)

Discards changes made to project ReadMe.txt files, restoring them to last committed state

**What it does:**
- Checks each project's ReadMe.txt for uncommitted changes
- **If changes exist:** Sends the modified file to Windows Recycle Bin (trash)
- Then runs `git checkout` to restore the git version
- Preserves local changes in trash for recovery if needed
- Processes all projects from `_top_level_build_config.yaml`
- Console output only
- **Stops on first error**

**Requirements:**
- `send2trash` package: `pip install send2trash`

**Run:** `python "Discard-ReadMe-Changes.py"`

**Output example:**
```
✓ Discarded changes: Change source for citation
✓ Discarded changes: Change source template
  → Sent to trash: Run SQL/ReadMe.txt
✓ Discarded changes: Run SQL
...
All ReadMe changes have been discarded.
```

**Workflow:**
1. Detects if file has local changes
2. If yes: Sends to Windows Recycle Bin
3. Restores git version
4. If no changes: Just restores (no trash action needed)

**Note:** This script only works for files already committed to git. If a project's ReadMe.txt isn't in git, the script will stop with an error (as designed).

---

## Typical Usage Scenario

### Edit and test ReadMe content safely:

```
1. Edit the template: Doc/Doc-templates/DocOutline_{project}.txt
   (or modify Doc/DocLibrary_snippets.txt)

2. Build: python "Build ReadMe files.py"
   (creates/updates Doc/Doc-built/ReadMe_{project}.txt)

3. Review the file: Doc/Doc-built/ReadMe_{project}.txt
   (project folders are NOT affected yet!)

4. If happy, copy: python "Copy-ReadMe-to-Projects.py"
   (copies to actual project folders)

5. If unhappy with copy, discard: python "Discard-ReadMe-Changes.py"
   (reverts project folders to last git commit)
```

---

## Why This Workflow?

**Before:** Editing templates immediately affected project ReadMe.txt files  
**Now:** Staging area lets you test, review, and control when changes go live

**Benefits:**
- ✅ Safe testing (project folders untouched until you're ready)
- ✅ Easy rollback (git discard reverts unwanted changes)
- ✅ Clear separation of concerns (templates vs. deployed files)
- ✅ Version tracking (each build marks suite version and timestamp)
- ✅ Utility versions (each ReadMe shows its own utility version)

---

## Configuration

All scripts read projects from: `../dev util scripts/_top_level_build_config.yaml`

```yaml
ProjectList:
  - Change source for citation
  - Change source template
  - Color from group
  - Convert fact
  - Group from SQL
  - List citations for PersonID
  - Lump sources
  - Modify citation list
  - Run SQL
  - Test external files
  - External Files Info
  - Mini report
  - Merge duplicate family records
```

To add or remove projects, edit this YAML file and all three scripts will respect it.

---

## File Locations

Scripts are now located in: `dev util scripts/doc/`

- Build ReadMe files.py
- Copy-ReadMe-to-Projects.py
- Discard-ReadMe-Changes.py

Configuration file: `dev util scripts/_top_level_build_config.yaml`

Doc folders: `doc/`
- Doc-templates/ (input templates)
- Doc-built/ (staging area, created if needed)
- DocLibrary_snippets.txt (snippet library)

---

## Notes

- **Path handling:** Scripts use relative navigation to find config and doc folders from their location
- **Error handling:** All scripts stop on first error (as requested). Error messages are clear.
- **Console-only:** No report files are generated (as requested).
- **Git requirement:** Discard script requires git to be installed and the repo to be initialized.
- **Folder renaming:** If you rename folder structure, paths in scripts may need adjustment
