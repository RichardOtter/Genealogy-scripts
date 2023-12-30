TestExternalFiles
Utility application for use with RootsMagic databases


RootsMagic (RM) software uses a relational database as its main storage.
The database includes links to external files called "media files".
These files appear under the RM version 9 Media tab.

As the number of linked files increases, user errors become more likely.
* A file on disk may get renamed or moved, breaking the link
    from the database.
    RM has tools to fix these, but it does not give a log of what it has done.
    There is a report that can be run, but
    with effort.
* A file may be added to the media folder on disk but then not attached to the
    desired database element. A common oversight when working quickly.
* A file may be added to RM, but then detached from all source, facts etc,
    leaving it "un-tagged". No harm in leaving it, but de-cluttering may be
    desirable.
* A file may be added to the database more than once.
* A file may be renamed, or misplaced and the original file contents cannot
    be verified.

This utility will identify these issues.
It is recommended to run this script daily as part of your backup routine.


======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
    referred to as the "ini file".)
    The utility needs to know where the RM database file is located, which
    functions to perform, and where to create the report file.
    Editing the ini file can be done using the Windows NotePad app.

2:  Double click the TestExternalFiles file. This momentarily displays the
    black command console window and at the same time, generates the report
    text file.

3:  Open the report text file in Notepad. (Just double click it.)
    The file will contain the analysis results.


======================================================================
Capabilities

The utility is can perform several functions, as configured in the
ini file's Options section, either separately or in combination:

CHECK_FILES
    Checks that each file referenced in the RM database actually
    exists on disk at the specified location. Any database file path link not
    found on disk is listed.

UNREF_FILES
    Lists all files found in the folder specified by SEARCH_ROOT_FLDR_PATH in
    the ini file (see below) that are NOT referenced in the RM database.
    This will find files that were perhaps added to the folder, but were
    mistakenly never added to the database.
    This feature is designed for use when media files referenced by RM are all
    under a single folder hierarchy.

NO_TAG_FILES
    Lists all files found in RM's Media tab that have zero tags.

DUP_FILEPATHS
    Lists files that have been added more than one time to the database. These
    will appear more than once in RM's Media tab.

DUP_FILENAMES
    Lists files that have the same filename. This is not usually a problem, but
    being aware of the duplicate names may help your organizing efforts.

FOLDER_LIST
    Lists all folders referenced in the RM database. A file in an unexpected
    location may have been accidentally added to the database. This list will
    make it obvious.

HASH_FILE
    Generates a text file containing a listing of each media file's name,
    location and HASH value, currently set to use MD5.
    The HASH text file, when requested, is generated at the location
    specified in the ini file.
    (MD5 is no longer considered secure for cryptography, but serves well for
    this purpose.)


======================================================================
Performance
    A database with 7,000 media files requires about 3 seconds run time for 5
    features turned on without hash file.
    Generating a hash file for 7,000 files takes about a minute.


======================================================================
Compatibility
Works with RootsMagic v7, v8, and v9

.exe file version
       Windows 64bit only. Tested with Window 11.

.py file version
       Python for Windows v3.11.4   64bit
       The py file has not been tested on MacOS.
       The script could probably be modified to work on MacOS with Python
       version 3 installed.


======================================================================
Backups

IMPORTANT: This utility ONLY reads the RM database file. This utility cannot
change your RM file. However, until you trust that this statement is true,
you should run this script on a copy of your database file or at least
have a known-good backup.


======================================================================
Getting Started

To install and use the exe single file version:

*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.

*  Copy these files from the downloaded zip file to the working folder-
      TestExternalFiles.exe
      RM-Python-config.ini

*  Edit the ini file in the working folder to specify the location
   of the RM file and the output report file.
   Some utility functions may be turned on or off. The required edits should
   be obvious. The sample ini file is already configured with the most useful
   options turned on. (To edit, Open NotePad and drag the ini file onto the
   NotePad window.)

*  Double click the TestExternalFiles.exe file to run the utility and
   generate the report file.

*  Examine the report output file.


--- OR ---

Use the py script file.  See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


======================================================================
NOTES

*   If no report file is generated, look at the black command console window for
    error messages that will help you fix the problem.

*   CHECK_FILES feature: file path case in the database or in the file system
    path name is not significant.

*   UNREF_FILES
    If there is a difference in capitalization of file name or directory
    path in the database vs. the file system, the file will be listed as
    un-referenced.  (Unix-like file system case sensitivity)

*   UNREF_FILES
    The folder specified in RM's preferences as the Media
    folder is not necessarily the same as the folder specified by the
    SEARCH_ROOT_FLDR_PATH variable in the ini file, but it is
    recommended that they be the same.

*   UNREF_FILES
    To shorten the list of unreferenced items, the IGNORED_OBJECTS section can
    be used to list items that are to be ignored by the utility.
    The goal should be to produce a report with no unreferenced files found.
    That is an easy result to interpret. If a file is added to the media folder
    but not added to the RM database, it will show up here.

    If a file is in the media folder but is intentionally not referenced by
    RM, add it to the IGNORED_OBEJECTS section. That prevents it from showing
    up in the report and confusing interpretation.

*   UNREF_FILES
    Only file names and folder names may be added to the IGNORED_OBJECTS list.
    I suggest that you organize your file and folders so that ignored folders
    all have the same name, even though there may be many of them in different
    locations in the media folder.

*   UNREF_FILES
    The value of- "# DB links minus # non-ignored files" should, in a
    sense, be zero. However, if a folder is ignored, but there are linked files
    within, then the value will be positive.

*   DUP_FILEPATHS
    Files with the same path and name may be duplicated in the media tab
    intentionally as they might have different captions etc. )This may no
    longer be an issue after RM8.)

*   DUP_FILENAMES
    Files listed have the same file names, ignoring case.
    Duplicate file names are not a problem. This function is provided as a
    troubleshooting tool. This feature does not check the file contents,
    only the names. Use the HASH_File feature to distinguish file contents.

*   SHOW_ORIG_PATH (RM v8 & v9 only)
    A display option is available for files found by either the CHECK_FILES or
    NO_TAG_FILES or DUP_FILES
    The option is turned on with the option SHOW_ORIG_PATH in the ini file.
    With this option on, the path for each file is shown twice,
    - the path on disk, that is, after any RM8 token in the path has been expanded.
    - the path as saved in the database with the token not expanded.

*   General information: File paths pointing to external files
    in RM 7:   all paths are absolute starting with a drive letter
    in RM 8&9: absolute file path starting with a drive letter
            or
            a path relative to another location.
    RM 8&9 Relative path symbols
    (these are expanded when found in the first position of the stored path)
    ~    home directory  (%USERPROFILE%)
    ?    media folder as set in RM preferences
    *    RM main database file location

*   RM-Python-config.ini  (the ini file)
    If there are any non-ASCII characters in the ini file, perhaps in a database
    path, or in ignored objects names, then the file must be saved in UTF-8
    format, with no byte order mark (BOM). The included sample ini file has an
    umlauted ä in a comment at the end to force it to be in the correct format.
    File format is an option in the save dialog box in NotePad.

*   Switching between RM 8 and RM 9
    This section probably applies to no-one. Please don't read it and get confused !
    If the machine running the script has had multiple versions of RootsMagic
    installed, over the years, there may be slightly unexpected behavior in some
    cases. RootsMagic saves some of its settings in an .xml file located in the
    user's home folder/AppData/Roaming/RootsMagic. A separate sub folder is
    created for each RM major version. The script will read the Media Folder
    location setting found in the highest installed RM version .xml file.
    This is fine if you are not using ver 8 after having installed ver 9, or
    when the same media folder location has been used for ver 8 and later.

    When run on a RM7 database, the Media Folder location is not needed so the
    XML file is not referenced, so switching  between ver 7 and ver 9 will not
    be an issue.


======================================================================
======================================================================
Which to use? Standalone .exe file or .py file

Decide whether you wish to use the script file (.py) or the executable
file (.exe) version. They produce exactly the same output at the same speed.
Using one does not preclude using the other.

Pro's and Con's

*   The .exe Executable File Version 
  Pro:
   The single exe file is all you need. No need to install Python.
  Con:
   The exe file is not human readable.
   A certain amount of trust is required to run a program not distributed
   by a major software publisher. Unknown software from an untrusted source
   could contain mal-ware. Rely on reviews by other users to establish trust.

--- OR ---

*   The .py Script File Version
  Pro:
   The script file is easily readable and one can confirm what it does.
   You may want to learn Python and make your own changes to the script
   and be able to use other scripts.
  Con:
   The script version requires an installation of the Python environment to run.
   This is a 100 MB investment in disk space. (Not big for modern day hard disks)


======================================================================
To use the py script version of the app

To install and use the script file version:
*  Install Python for Windows x64  -see immediately below
*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.
*  Copy these files from downloaded zip file to the working folder-
      TestExternalFiles.py
      RM-Python-config.ini
*  Edit the ini file in the working folder to specify the location
   of the RM file and the output report file.
   Some utility functions may be turned on or off. The required edits should
   be obvious. The sample ini file is already configured with the most useful
   options turned on. (To edit, Open NotePad and drag the ini file onto the NotePad
   window.)
   The same ini file may be used with either the .exe or .py version of the utility.
*  Double click the TestExternalFiles.py file to run the utility and
   generate the report file.
*  Examine the report output file.


======================================================================
Python install-
Install Python from the Microsoft Store
or download and install from Python.org web site

From Microsoft Store
Run a command in Windows by pressing the keyboard key combination
"Windows + R", then in the small window, type Python.
Windows store will open in your browser and you will be be shown
the various versions of Python.
Click the Get button for the latest version.

Web site download and install
Download the current version of Python 3, ( or see direct link below
for the current as of this date)
https://www.python.org/downloads/windows/

Click on the link near the top of page. Then ...
Find the link near bottom left side of the page, in the "Stable Releases"
section, labeled "Download Windows installer (64-bit)"
Click it and save the installer.

Direct link to recent (2023-07) version installer-
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


======================================================================
TODO
*  Add code to find duplicate files represented by different relative paths
   in database.
*  ?? what would you find useful?

======================================================================
Feedback
The author appreciates comments and suggestions regarding this software.
Richard.J.Otter@gmail.com

Public comments may be made at-
https://github.com/ricko2001/Genealogy-scripts/discussions


Also see:
My website containing other RootsMagic relevant information:
https://RichardOtter.github.io

My Linked-In profile at-
https://www.linkedin.com/in/richardotter/


======================================================================
Distribution
Everyone is free to use this utility. However, instead of
distributing it yourself, please instead distribute the URL
of my website where I describe it- https://RichardOtter.github.io
This is especially true of the exe file version.

======================================================================
