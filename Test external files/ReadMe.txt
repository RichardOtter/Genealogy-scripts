=========================================================================DIV80==
Test usage and status of external/media files
TestExternalFiles.py


Utility application for use with RootsMagic databases

RootsMagic (RM) software (https://RootsMagic.com) uses a SQLite relational
database (https://sqlite.org) as its data storage file.

Access to the RM data file via third party tools is a major advantage RM
has over other genealogy project management applications.

This utility is part of a suite of utilities that has been written to
perform analysis or data modification not available within the RM application.
See https://RichardOtter.github.io


=========================================================================DIV80==
Purpose

The database includes links to external files which RM calls "media files".
These files appear in the RM Media tab.

As the number of linked files increases, user errors become more likely.
* A file on disk may get renamed or moved, breaking the link from the database.
    RM has tools to fix these, but it does not give a log of what it has done.
    There is a report that can be run, but with effort.
* A file may be added to the media folder on disk but then not added to the
    database. A common oversight when working quickly.
* A file may be added to RM, but then detached from all source, facts etc,
    leaving it "un-tagged". No harm in leaving it, but de-cluttering may be
    desirable.
* A file may be added to the database more than once.
* A file from a far-flung folder may be added and it's location forgotten.
* A file may be renamed, or misplaced or its contents altered. One will not be
  able to verify the original file's contents are the same as in the current file.

This utility will identify these issues.
It is recommended to run this script as part of your backup routine when
mew files are being added.

=========================================================================DIV80==
Backups

IMPORTANT
This script only reads the database file and makes no changes.
However, you should run this script on a copy of your database file or at least
have multiple known-good backups until you are confident that the the database
remains intact after use. At that point, run this utility of your
"production" database.

=========================================================================DIV80==
Software Safety

This utility is written in the Python programming language (https://Python.org)
and is distributed as plain-text '.py' files that can be viewed with Notepad or
any other text editor.

Because the source code is distributed in human readable text form, users can
open any of the .py files in a text editor to inspect the complete
implementation, verify its behavior, and assess its safety.

The source files can also be reviewed by AI to help identify potential security
or safety concerns. Here is a recent report generated from the code by AI:
https://github.com/RichardOtter/Genealogy-scripts/blob/main/SECURITY_ANALYSIS.md

=========================================================================DIV80==
Compatibility

Tested with a RootsMagic v 12.1.3 database
using Python for Windows v3.15.2   64bit

RM 7 and later and much earlier version of Python, say after 3.10 will
also probably work but have not been recently tested.

The python script file has also not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3.n installed.

=========================================================================DIV80==
Performance

A database with 7,000 media files requires about 3 seconds run time for 5
features turned on without hash file.
Generating a hash file for 7,000 image files takes roughly a minute.

=========================================================================DIV80==
General Overview

This program is what is called a "command line utility". It is in the form of a
single text file with a "py" file name extension ("TestExternalFiles.py")
along with the package "RMpy" which is a folder included in the 
distribution zip file.
The TestExternalFiles.py file relies on code in the RMpy folder.
These utilities are not installed in the traditional Windows sense, they are
simply copied to the computer.

The utilities are told what to do by editing a configuration file. This
configuration tells the utility which database to use and how to display the
output.

The default name of the configuration file (called, hereinafter, the
"config file") is "RM-Python-config.ini". For now, it should be located in the
same folder as the MainScriptFile.py file and the RMpy folder.

How it works
Test External Files is started by the user, a terminal window is displayed,
the program processes the configuration data and the database, a report file
is displayed in Notepad, the terminal window closes and the program exits.


Getting Started     *****  Details follow immediately below. *****

To install and use the utility for the first time:

*  Install Python for Windows x64.

*  Create a new folder on your computer, the "working folder" to contain
   a copy of your database, the program files and the config file.

*  Edit the config file in the working folder to tell the utility what to
   do and how to do it.

*  Double click the TestExternalFiles.py file to run the utility.

*  A terminal window with a black background and white text will appear.

*  The terminal window will close and a summary report will be displayed
   in Notepad.

=========================================================================DIV80==
Capabilities

The utility can perform several functions, as configured in the config file's
OPTIONS section, either separately or in combination:

CHECK_FILES
    Checks that each file referenced in the RM database actually
    exists on disk at the specified location. Any file path link found in
    the database but not found on disk is listed.

UNREF_FILES
    Lists all files found in the folder specified by SEARCH_ROOT_FLDR_PATH in
    the config file (see below) that are NOT referenced in the RM database.
    This will find files that were perhaps added to the folder but were
    mistakenly never added to the database.
    This feature is designed for use when media files referenced by RM are all
    under a single folder hierarchy.

NO_TAG_FILES
    Lists all files found in RM's Media tab that have zero tags.

FOLDER_LIST
    Lists all folders referenced in the RM database.
    A file in an unexpected location may have been accidentally added to the
    database. This list will make it obvious.

NOT_MEDIA_FLDR
    Lists all files that are not in the RM "Media folder" as specified in the 
    RM preferences settings. Best practice is to set the "Media Folder" in 
    preferences and use that folder as the location for all media.

DUP_FILEPATHS
    Lists files that have been added more than one time to the database. These
    will appear more than once in RM's Media tab.

DUP_FILENAMES
    Lists files that have the same filename. This is not usually a problem, but
    being aware of the duplicate names may help your organizing efforts.

HASH_FILE     (deprecated)
    Generates a text file containing a listing of each media file's name,
    location and HASH value, currently set to use MD5.
    https://en.wikipedia.org/wiki/MD5
    The HASH text file, when requested, is generated at the folder location
    specified in the config file.
    While MD5 is no longer considered secure for cryptography, it serves well
    for this purpose.

    A separate RM utility app ExternalFilesInfo has been released that stores the
    hash info and more within the database file. That is now the recommended
    solution.


=========================================================================DIV80==
Running the utility - detailed step by step

The steps listed here run the utility on a copy of your database created in a
new directory location. Once you feel comfortable with how the app operates,
you will want to run the app on your production database at its usual folder
location and create another folder for all of the utilities and config files
you regularly use.

==========-
Install Python for Windows x64
- follow the three easy steps in "APPENDIX  Python install" below.

==========-
Create a folder on your computer that you will not confuse with other
folders. It will be referred to as the "working folder".

You may want to create it within your home folder. Your home folder is
"C:\Users\me", where "me" is your user name. This is a safe location that will
not be affected by OneDrive.

==========-
Copy these items from the downloaded zip file to the working folder-
     (file)     TestExternalFiles.py
     (file)     RM-Python-config.ini
     (folder)   RMpy

==========-
Make a copy of your database, move the copy into the working folder.

Rename the database copy to "TEST.rmtree" in order to prevent any
confusion about the purpose of the new file.

==========-
Edit the sample RM-Python-config.ini file in the working folder.
(See the section "APPENDIX  Config file: location, contents and editing"
if you need help)

A summary of the config file (ini file) structure:
      The names in square brackets are section names.
      The items in a section are key-value pairs.

The sample config file contains a section named [FILE_PATHS].
In that section, reside several key-value pairs, one of which is
DB_PATH = TEST.rmtree

"DB_PATH" is the key, "TEST.rmtree" is the value. Key-value pairs are separated
with an equals sign character.

The utility needs to know where the RM database file is located, the output
report file name and its location.

The next key: REPORT_FILE_PATH tells the utility where to create the report
file. The setting as it is in the sample says create a file with a name starting
withe "REPORT_" in the current (working) folder.

The next key: REPORT_FILE_DISPLAY_APP names the app that will be automatically
called to display the report file.

Save the config file but leave it open in Notepad.

=========-
See the Notes section below to help you determine which features to enable.
It is suggested that for your first run, leave the CHECK_FILES option on and
the others OFF.
After you have a successful run, you can try the other options.

=========-
Double click the "TestExternalFiles.py" file in the working folder
to start the utility.

=========-
A terminal window is displayed while the utility processes
the commands.

=========-
The terminal window is closed and the utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

=========-
Examine the report and note any discrepancies from what was expected

This utility does not change the database.


=========================================================================DIV80==
Notes

=========-
CHECK_FILES feature: By default, folder path and file name capitalization in
the database and in the file system path name must match for the file to be
found by this utility. They do not need to match for RM to find the file. 
The author's opinion is that case miss-matches should be fixed.
This behavior can be reversed by the setting the  
option CASE_INSENSITIVE to "on".

=========-
UNREF_FILES
This option is designed so that your goal should be to produce a report
with no unreferenced files found. That result is easy to interpret.
If a file is added to the media folder but not added to the RM database,
it will show up om this list.

 However, there may be files and folders of files that you want to store
 near your media files, but are not actually referenced by the database.

 To shorten the list of unreferenced items, a specified set of files and folders
 within the SEARCH_ROOT_FLDR_PATH folder can be ignored and not displayed in the
 Unreferenced Files report. There are two methods of specifying the objects
 to ignore:
 1: the IGNORED_OBJECTS section can be used to tell the utility to not include 
 certain files in the list of unreferenced files. See below.
 2: The option IGNORED_ITEMS_FILE can be set to on or off. When the option is
 set to on, the specification of the files/folders to ignore is done by the
 file TestExternalFiles_ignore.txt which should be found in the
 SEARCH_ROOT_FLDR_PATH folder. The TestExternalFiles_ignore.txt file contains
 a set of exclusion patterns. A pattern may contain wildcard characters.
 The format of the patterns can be found in many on-line sources, for example-
     https://www.atlassian.com/git/tutorials/saving-changes/gitignore#git-ignore-patterns
     https://git-scm.com/docs/gitignore
A sample file is included in the zip file.
   
To use these kind of match patterns containing wild cards, one must turn on the
option IGNORED_ITEMS_FILE, create a text file named TestExternalFiles_ignore.txt, 
in the root of the SEARCH_ROOT_FLDR_PATH folder, and then edit that file to
contain the patterns for the files to ignore.

The TestExternalFiles_ignore.txt must be stored in utf-8 format if it 
contains non-ASCII 
characters. (Same as for the config file)


=========-
IGNORED_OBJECTS
IGNORED_OBJECTS FILES and FOLDERS settings in the config file are only used 
when the IGNORED_ITEMS_FILE setting is set to off.

FILES
Add file names that should not be reported as being unreferenced.
One name per line. Indented with at least one space character.
No paths, just file names.
All files with this name are ignored no matter where they are within
the SEARCH_ROOT_FLDR_PATH folder

FOLDERS
Add folder names whose entire contents should not be reported as being
unreferenced.
One name per line. Indented with at least one space character.
No paths, just folder names. (e.g. Folder1   and not  C:\Users\me\Folder1 )
All folders with this name have their contents ignored no matter where they
are within the SEARCH_ROOT_FLDR_PATH folder

I suggest that you organize your file and folders so that ignored folders
all have the same name, even though there may be many of them in different
locations in the media folder.


=========-
SEARCH_ROOT_FLDR_PATH
The folder specified in RM's preferences as the Media folder is not 
necessarily the same as the folder specified by the SEARCH_ROOT_FLDR_PATH
variable in the config file  (but I recommended that they be the same).
Use the absolute path of the folder.


=========-
UNREF_FILES
The value of- "# DB links minus # non-ignored files" should, in a
sense, be zero. However, if a folder is ignored, but there are linked files
within, then the value will be positive.


=========-
DUP_FILEPATHS
Files with the same path and name may be duplicated in the media tab
intentionally as they might have different captions etc.


=========-
DUP_FILENAMES
Files listed have the same file names, ignoring case.
Duplicate file names are not a error. This function is provided as a
organizational tool. This feature does not check the file contents,
only the names. Use the HASH_File feature to distinguish file contents.


=========-
SHOW_ORIG_PATH (RM v8 through v10 only)
A display option is available for files found by either the CHECK_FILES or
NO_TAG_FILES or DUP_FILES
The option is turned on with the option SHOW_ORIG_PATH in the config file.
With this option on, the path for each file is shown twice,
- the path on disk, that is, after any RM8-9 token in the path has been expanded.
- the path as saved in the database with the relative path anchor token 
not expanded.
See the note below "Background information" regarding relative paths in RM.



=========-
IGNORED_OBJECTS section of the config file
Due to how the config file is parsed by the python library, files and folders
whose names start with the # character cannot be added to the FILES or FOLDERS.
Instead, they are considered comments. There is a way to overcome this
limitation but the explanation of how is not worth the confusion it would
create. Bottom line- if you really want to add the file or folder, change
its name so it doesn't start with a # - or use the new ignore file method to
exclude files.


=========-
A listing of "DB entires with blank filename or path found" is displayed when a
media item in the database has a blank file path or file name. These items
should be fixed first.

=========-
Paths specified in the Config file and command line
Paths may, in general, be written as either Absolute or Relative format.

Allows absolute or relative to current directory:
Command line argument specifying the config file location

Allows absolute or relative to folder containing py file:
DB__PATH
REPORT_FILE_PATH

Allows absolute
REPORT_FILE_DISPLAY_APP

RMNOCASE_PATH
SEARCH_ROOT_FLDR_PATH
HASH_FILE_FLDR_PATH


=========-
Background information: File paths pointing to external files
in RM 7:   all paths are absolute starting with a drive letter
in RM 8&9: absolute file path starting with a drive letter
        or
        a path relative to another location.
RM 8&9 Relative path symbols
(these are expanded when found in the first position of the stored path)
    ?    media folder as set in RM preferences
    ~    home directory  (%USERPROFILE%)
    *    RM main database file location


=========-
Switching between RM 8, RM 9, RM 10 and RM 11
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
XML file is not referenced, so switching  between ver 7 and ver 10 will not
be an issue.


=========-
Files attached to RM Tasks are not analyzed by this utility and they do not 
appear in the RM Media tab.

=========================================================================DIV80==
APPENDIX  Using a database with external file links from a new directory location

RM finds media files linked to a database by several methods. In my opinion,
the most reliable method to find all media files in the Media Folder, as
specified in the RM Preferences. The other methods can certainly be
useful in some circumstances.
One of the other "search methods" is to find a file by recording it location in
relation to the database file. This is fine unless the database file is moved
and the files are not.
This point needs to be made in regards to the instructions for testing the
utility app described here. When you make a copy of your database and move the
copy to the "Working folder", as instructed earlier, some of the database's
external files may not be found when running the database in the new location.
This is only temporary. Move the database back to it's original location and
the media files will be found again.
So, while the database is in its temporary test location, don't be alarmed to
see red X's on media file thumbnails. Don't try to fix the links until you have
returned the database to its usual directory location.

=========================================================================DIV80==
APPENDIX  Config file: location, contents and editing

Name and folder location
The utility requires a configuration file. A file named "RM-Python-config.ini"
will be recognized as the utility's configuration file when placed in the same
directory as the TestExternalFiles.py file. Each utility is distributed with
a sample config file to get you started.

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "TestExternalFiles.py" is executed from a terminal
window which has the folder "C:\Users\me\TestFolder" as its 'current directory',
it will use the configuration file "C:\Users\me\TestFolder\RM-Python-config.ini"
if it exists. If the utility is run with an explicit argument, such as:
TestExternalFiles.py "C:\Users\me\Documents\RM-Python-config.ini" then the
specified ini configuration file will be used instead.

Note also that the file name is not restricted to the default.
For instance, running the utility from a terminal window as:
TestExternalFiles.py config_mine.ini
will instruct the utility to use config_mine.ini in the current directory
as its configuration file.

A configuration file that is used from the command line can be named so as
to convey its purpose.
A Windows shortcut can also be constructed with the above described script name
with config file name argument to allow execution from the desktop with a
double mouse click.

Editing
Use any text editor to edit the configuration file. The Windows built-in
app "Notepad" is suitable.
To edit the configuration file, first open the Notepad app and then use the
mouse to drag the configuration file onto the open Notepad window.
(By default, files with the .ini extension are not associated with an
editor program.)

Format and conventions
The config file uses the "standard" ini file format. You can ask AI for help
with a formatting problem. Just mention that you are using 
"Python configparser" so that it will be accurate.

The config file is made up of the elements: 
Sections, Keys, Values and Comments.

A name in square brackets is a section name that identifies the start
of a section. A section continues until a new section starts. The order of
sections is a config file is not important, but all of the sample config files
start with the [FILE_PATHS] section.

A section contains one or more key-value pairs and comment lines. Every key
should be in a named section.

A name on the left side of a "=" sign is a key.
Text on the right side of a "=" is the value assigned to the key on the left.
Spaces immediately to the left of the = character are ignored; as are leading and
trailing spaces around the value.

Comment lines start with a "#" character and are only included to help
the human user read and understand the file. They are ignored by the utility
software. Comments may appear almost anywhere in the config file, except within
a multi-line value.

For an example, here is a section containing 3 key-values used by all of the
RM utilities:

[FILE_PATHS]
# this is the test database
DB_PATH         = TEST.rmtree
REPORT_FILE_PATH  = ..\Report_utilName.txt
REPORT_FILE_DISPLAY_APP  = C:\Windows\system32\Notepad.exe

[OPTIONS]
UPPER_CASE = on

The 3 keys, DB_PATH, REPORT_FILE_PATH, and REPORT_FILE_DISPLAY_APP are all
in the [FILE_PATHS] section. The UPPER_CASE key is in the OPTIONS section.
The second line is a comment.

=========-
Keys used by all of the utilities.
DB_PATH, REPORT_FILE_PATH, REPORT_FILE_DISPLAY_APP

See "APPENDIX  Config file: location, contents and editing" for more general
editing information.

These keys all appear in the [FILE_PATHS] section of the config file.

DB_PATH     =  TEST.rmtree
DB_PATH     =  my TEST database.rmtree
DB_PATH     =  my database folder\TEST.rmtree
DB_PATH     =  ..\..\TEST.rmtree
DB_PATH     =  Y:\weird drive\TEST.rmtree

Specifies the file path to the RM database to be analyzed.
The path may be an absolute or relative path.
Leading an trailing white space is ignored.

REPORT_FILE_PATH         = Report.txt
REPORT_FILE_PATH         = ..\Report.txt

The name and path to the report file generated for each run.
This path must be writeable.
An existing file will be overwritten.
The path may be absolute or relative path.
Leading an trailing white space is ignored

REPORT_FILE_DISPLAY_APP  = C:\Windows\System32\notepad.exe

The application used to display the report at the end of the run.
If this key is not given (say, the line is commented out), then the report is
generated but not automatically displayed.

multi-line value

The ini file format used by the config file allows entry of multi-line values.
These are used when the key is to be assigned more than a single name or datum.
The multi line value is still just one value, but the values is split up into
multiple lines.

Each line of a value after the first, must be indented with at least one
space character more than the key name.

All the lines in a value should have the same indentation. Not required but
looks much more tidy and is easier to read.

There must be one or more blank lines at the end of a value separating it
from the next key or section marker or comment.

!! Comment lines are not allowed within a multi-line value. !!

Examples-

correct formats-

KEY_NAME1 = item1

KEY_NAME2 =
  item1

KEY_NAME3 = item1
  item2
  item3

KEY_NAME4 =
  item1
  item2
  item3

===========-
incorrect format- (empty line not allowed)

KEY_NAME =
  item1

  item2
  item3

===========-
incorrect format (not indented)

KEY_NAME =
item1
item2
item3

===========-
incorrect format (not indented)

KEY_NAME = item1
item2
item3

===========-
incorrect format (comment lines not allowed within a multi line value)

KEY_NAME =
  item1
  # item2
  item3

Text Encoding
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an umlauted ä in the first line comment to
force it to be in the correct format.
Text encoding can be found in the file format option in the "Save file" dialog
box in NotePad.

=========================================================================DIV80==
APPENDIX  Python install

Install Python using the "winget" command line package manager.

It is also possible to install from the Microsoft Store or from the
Python.org web site but only the winget method is described here.

The completed install folder occupies about 140 MB of disk space.

Installation using winget.

1. Open a command line terminal.
   A quick method is to right click the Windows menu icon in the file manager
   task bar and select the Terminal command; not the "Terminal (Admin)" command.

2. Type (copy and paste) the following command in the window and hit Enter:

    winget install --id Python.PythonInstallManager --source winget

3. Wait for the display of "Successfully installed" and then type the
   following command and hit Enter:

    py install 3

The output for this command should be similar to-
-------
The signature for https://www.python.org/ftp/python/index-windows.json was
successfully verified.
Installing Python 3.15.2.
Extracting: ...............................................................✅

Global shortcuts directory is not on PATH. Add it for easy access to global Python aliases.
Directory to add: C:\Users\<user_name>\AppData\Local\Python\bin
-------

Ignore the last 2 lines. You won't need that functionality.


How to Uninstall Python

Use the Settings app in the Windows menu.
Go to Apps=>Installed apps
and find:
"Python Install Manager"
and
"Python 3.n.n"
and select Uninstall from the three dot menu to the right of the names for each item.

or use winget from the command terminal:
winget uninstall --id Python.PythonInstallManager
winget uninstall --id Python.Python.3.nn


For additional information, see the Python on Windows docs at-
https://docs.python.org/3.15/using/windows.html

=========================================================================DIV80==
APPENDIX  Troubleshooting

=========-
No Report File displayed

If the terminal windows displays the message: RM-Python-config.ini file contains
a format error, see the section below.

If no report file is generated, look at the terminal window for error messages
that will help you fix the problem. There may be something wrong with the config
file line- REPORT_FILE_PATH.

If the report is created, but not displayed, check the config
file line- REPORT_FILE_DISPLAY_APP

If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console, cd'ing to
the folder containing the py file and then running the py file from the
command line. The window will not close and you will be able to read any
error messages.

=========-
Error message:
RM-Python-config.ini file contains a format error

Examine the file visually and check to see that it follows the rules mentioned
above. If all else fails, start over with the supplied config file and make
sure that it works, Then make your edits one by one to identify the problem.
You may want to look at- https://en.wikipedia.org/wiki/INI_file


=========-
Multiline Values
Probably the trickiest part of the config file is the IGNORED_OBJECTS section.
The FOLDERS and FILENAMES keys are multi-line values.
Each line of the value should be on a separate line indented with at least 
one blank. An empty line generates an error.
Multi-line values may not contain comment lines (lines starting with a #).

examples-

correct format-

[IGNORED_OBJECTS]
FOLDERS =
  Folder1
  Folder2
  Folder3


incorrect format- (empty line not allowed)

[IGNORED_OBJECTS]
FOLDERS =
  Folder1

  Folder2
  Folder3


incorrect format (not indented)

[IGNORED_OBJECTS]
FOLDERS =
  Folder1
Folder2
  Folder3


incorrect format- (no comments allowed)

[IGNORED_OBJECTS]
FOLDERS =
  Folder1
# Folder2
  Folder3

incorrect format- (# comment indicator only allowed at start of line)

[IGNORED_OBJECTS]
FOLDERS =    # a comment
  Folder1
  Folder2
  Folder3

incorrect format (no empty lines)

[IGNORED_OBJECTS]
FOLDERS =

  Folder1
  Folder2
  Folder3


=========================================================================DIV80==
TODO

*  Add code to find duplicate files represented by different relative paths
   in database.
*  ?? what would you find useful?


=========================================================================DIV80==
Feedback

The author appreciates comments and suggestions regarding this software.
RichardJOtter@gmail.com

Public comments and bug reports may be made at-
https://github.com/ricko2001/Genealogy-scripts/discussions


Also see:
My website containing other RootsMagic relevant information:
https://RichardOtter.github.io

My Linked-In profile at-
https://www.linkedin.com/in/richardotter/


=========================================================================DIV80==
Distribution

Everyone is free to use this utility. However, instead of
distributing it yourself, please instead distribute the URL
of my website where I describe it- https://RichardOtter.github.io
or a link to the GitHub repo:
https://github.com/RichardOtter/Genealogy-scripts






================================================================================
Suite Version: 1.2.0 BETA
Utility Version: 1.9.0 BETA
Built: 2026-11-27 15:20:16
================================================================================
