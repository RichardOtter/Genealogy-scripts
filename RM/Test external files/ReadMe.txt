=========================================================================DIV80==
Test usage and status of external/media files
TestExternalFiles.py


Utility application for use with RootsMagic databases

RootsMagic (RM) software (https://RootsMagic.com) uses a SQLite relational
database (https://Sqlite.org) as its data storage file.

Access to the RM data file via third party tools is a major advantage RM
has over other genealogy project management applications.

This utility is part of a suite of utilities that has been written to
perform analysis or data modification not available within the RM application.
See https://RichardOtter.github.io

This software is written using the Python language (https://Python.org) and
is distributed as a text ".py" file along with a folder, RMpy, of common Python
code, called a python package. The user can simply open the file or package
files in a text editor to read all implementation details and access safety.

A Python py script file is executed using the Python language interpreter.
The interpreter is a separate piece of software easily installed on your 
computer.


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
It is recommended to run this script daily as part of your backup routine.

A Hash file might be generated annually and archived with the full dataset.


=========================================================================DIV80==
Backups

IMPORTANT
This script only reads the database file and makes no changes.
However, you should run this script on a copy of your database file or at least
have multiple known-good backups until you are confident that the the database
remains intact after use. At that point, run this utility of your
"production" database.

=========================================================================DIV80==
Compatibility

Tested with a RootsMagic v 10.0.5 database
using Python for Windows v3.13.4   64bit

The py file has not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3 installed.


Probably still works with RootsMagic v7, although it has not been
recently tested.

=========================================================================DIV80==
Performance

A database with 7,000 media files requires about 3 seconds run time for 5
features turned on without hash file.
Generating a hash file for 7,000 image files takes roughly a minute.


=========================================================================DIV80==
Overview

This program is what is called a "command line utility".
It is in the form of a single text file with a "py" file name extension
(referred to, in this section, as "MainScriptFile.py"). The utility also
needs the Python package RMpy, which is a folder included in the distribution
zip file.

Most input to the utility is through the configuration file. The the default
name of the configuration file (called, hereinafter, the "config file") is
 "RM-Python-config.ini". It should be located in the same folder as the
 MainScriptFile py script file and the RMpy folder. At a minimum, the config
file gives the name and location of the database on which the utility operates.

One config file can be shared among other RM utilities in the suite. Each
utility will extract the information it needs from the config file.

To install and use the script for the first time:

*  Install Python for Windows x64  -see APPENDIX below

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy the program files/folder from the downloaded zip file to
   the working folder.

*  Copy the sample config file  from the downloaded zip file to
   the working folder.

*  Edit the config file in the working folder to tell the utility what to
   do and where to do it.

*  Double click the main program .py file to run the utility.

*  A window titled "Command Prompt" with a black background and white text will
appear. Some utilities will keep this window open and request commands and 
information, other utilities will only show the window for a moment, others 
will have the window displayed for the length of the utility's processing time.

*  The terminal window will close and a summary report will be displayed
in NotePad.

The above procedure of making a copy of your database and operating on it in 
the working folder is most prudent when a user is just getting familiar with 
a new or updated utility. 
Some utilities are read only and do not change the database at all, while others
affect only small amount of data. Once the user has confidence in the operation
of such a low-impact utility, one can start operating directly on the research
(production) database, always assuming that at least several known-good backups
exist.
Other utilities that involve more configuration and make larger chnages should
always be copied and operated on in a working folder.

*****  Details follow below. *****


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

HASH_FILE
    Generates a text file containing a listing of each media file's name,
    location and HASH value, currently set to use MD5.
    https://en.wikipedia.org/wiki/MD5
    The HASH text file, when requested, is generated at the location
    specified in the config file.
    While MD5 is no longer considered secure for cryptography, it serves well
    for this purpose.


=========================================================================DIV80==
Running the utility in detail

==========-
Create a folder on your computer that you will not confuse with other
folders- the "working folder".

==========-
Copy these items from the downloaded zip file to the working folder-
      TestExternalFiles.py             (file)
      RM-Python-config.ini             (file)
      RMpy                             (folder)

==========-
Make a copy of your database, move the copy into the working folder.

Rename the database copy to "TEST.rmtree" in order to prevent any
confusion about the purpose of the copy.

==========-
Edit the sample RM-Python-config.ini file in the working folder.
(See the section "APPENDIX  Config file: location, contents and editing"
if you need help)

A summary of the config file structure:
The names in square brackets are section names.
The items in a section are key-value pairs.

For example, in the sample config file, there is a section named 
[FILE_PATHS].
In that section, reside 3 key-value pairs, one of which is 
DB_PATH = TEST.rmtree

"DB_PATH" is the key, "TEST.rmtree" is the value.
key-value pairs are separated with a = character.


The utility needs to know where the RM database file is located, the output
report file name and its location.

If you followed the above instructions, no changes to any of the key-values in
the [FILE_PATHS] section are needed.

Save the config file but leave it open in Notepad.

=========-
TODO
CONTINUE TO FILL IN TH CONFIG FILE

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
Switching between RM 8, RM 9 and RM 10
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
APPENDIX  Config file: location, contents and editing

Name and location
A file named "RM-Python-config.ini" will be recognized as the utility's 
configuration file when placed in the same directory as the Python 
script (.py file) for the utility. Each utility is distributed with a sample 
config file to get started.

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "RMutility.py" is executed from the folder
"C:\Users\me\Joe", it will use the configuration file
 C:\Users\me\Joe\RM-Python-config.ini" if it exists.
However, if the utility is run with an explicit argument, such as:
RMutility.py "C:\Users\me\Joe\documents\RM-Python-config.ini"
then the specified configuration file will be used instead of the default.

Note also that the file name is not restricted to the default.
For instance, running the utility as:
RMutility.py config_mine.ini
will instruct the utility to use config_mine.ini in the current directory
as its configuration file.

A configuration file that is used from the command line can be renamed so as
to convey its purpose. 
A Windows shortcut can also be constructed with the above described srciptname
with config file name argument to allow execution from the desktop with a
double mouse click.


Editing
Use any text editor to edit the configuration file. The Windows built-in
app "Notepad" is suitable.
To edit the configuration file, first open the Notepad app and then use the
mouse to drag the configuration file onto the open Notepad window.
(Becasue by default, files with the .ini extension are not associated with an
editor program.)


Format and conventions
The file uses the standard ini file format. The config file is made up of the
elements: Sections, Keys, Values and Comments.

A name in square brackets is a section name that identifies the start
of a section. A section continues until a new section starts. The order of 
sections is a config file is not important, but all of the sample config files
 start with the [FILE_PATHS] section.

A section contains one or more key-value pairs and comment lines. Every key 
should be in a named section.

A name on the left side of a "=" sign is a key.
Text on the right side of a "=" is the value assigned to the key on the left.
Comment lines start with a "#" character and are only included to help 
the user read and understand the file. They are ignored by the utility software.

For an example, here is a section containing 3 key-values used by all of the 
RM utilities:

[FILE_PATHS]
# this is the test database
DB_PATH         = TEST.rmtree
REPORT_FILE_PATH  = ..\Report_utilName.txt
REPORT_FILE_DISPLAY_APP  = C:\Windows\system32\Notepad.exe

The 3 keys, DB_PATH, REPORT_FILE_PATH, and REPORT_FILE_DISPLAY_APP are all
in the [FILE_PATHS] section. The utility requires that their values be file 
paths, as shown.
The second line is a comment.

The file path may be absolute, as in REPORT_FILE_DISPLAY_APP above, or it may
be relative to the current directory, as in DB_PATH and REPORT_FILE_PATH above.

The DB_PATH points to the database that is to be analyzed/modified.
See the sections "Backups" and "Running the utility in detail", above, for help
in deciding which database to use. New users will always want to point to a
copy of the main database.

The utilities all generate a textual report file. The file's name
and location can be specified by REPORT_FILE_PATH key.

If REPORT_FILE_DISPLAY_APP key has a valid value, then the report file will be
automatically displayed by the named application.


multi-line value

The ini file format used by the config file allows entry of multi-line values.
These are used when the key is to be assigned more than a single name or datum.
The multi line value is still just one value, but the values is split up into
multiple lines.

Each line of a value after the first, must be indented with at least one 
space character.

All the lines in a value should have the same indentation. Not required but
looks much more tidy and is easier to read.

There must be one or more blank lines at the end of a value separating it
from the next key or section marker or comment.

Comment lines are not allowed within a multi-line value.

Examples-
correct formats-

KEY_NAME = Name1

KEY_NAME =
  Name1

KEY_NAME = Name1
  Name2
  Name3

KEY_NAME =
  Name1
  Name2
  Name3

incorrect format- (empty line not allowed)

KEY_NAME =
  Name1

  Name2
  Name3

incorrect format (not indented)

KEY_NAME =
Name1
Name2
Name3

incorrect format (not indented)

KEY_NAME = Name1
Name2
Name3

incorrect format (comment lines not allowed within a multi line value)

KEY_NAME =
  Name1
 #  Name2
  Name3

Encoding
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.


=========================================================================DIV80==
APPENDIX  Python install

Either install Python from the Microsoft Store
or
download and install from Python.org web site

From Microsoft Store
Run a command in Windows by pressing the keyboard key combination
"Windows + R", then in the small window, type Python.
Windows store will open in your browser and you will be be shown
the various versions of Python.
Click the Get button for the latest version.

Python.org web site download and install
Download the current version of Python 3, (or see direct link below
for the current as of this date)
https://www.python.org/downloads/windows/

Click on the link near the top of page. Then ...
Find the link near bottom left side of the page, in the "Stable Releases"
section, labeled "Download Windows installer (64-bit)"
Click it and save the installer.

Direct link to recent (as of 2025-06) version installer-
https://www.python.org/ftp/python/3.13.4/python-3.13.4-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and is cleanly removed using the standard Windows method found in
Windows=>Settings=>Installed apps

Run the Python installer selecting all default options.
Note: by default, the Python installer places the software in the user's
home folder in the standard location.


=========================================================================DIV80==
APPENDIX  Troubleshooting

=========-
No Report File displayed

If the report is created, but not displayed, check the config
file line- REPORT_FILE_DISPLAY_APP

If no report file is generated, look at the terminal window for error messages
that will help you fix the problem. There may be something wrong with the config
file line- REPORT_FILE_PATH.

If the terminal windows displays the message: RM-Python-config.ini file contains
a format error, see the section below.

If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console, cd'ing to
the folder containing the py file and then running the py file from the
command line. The window will not close and you will be able to read any
error messages.

=========-
Error message:
RM-Python-config.ini file contains a format error
Examine th efile visually and chek to see that it follows the rules mentioned
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

Public comments may be made at-
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


=========================================================================DIV80==
