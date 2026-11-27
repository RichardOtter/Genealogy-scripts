=========================================================================DIV80==
Convert an existing fact from one fact type to another
ConvertFact.py


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

This utility can convert existing facts of one fact type to facts of a different
fact type. e.g. "Residence (fam)" to "Residence", or "Census" to "Census 1950".

Simply changing the fact type for an existing fact is trivial using SQL.
Complications arise when a family fact is converted to a Individual fact or when
the fact to be changed has witnesses (was shared).
ConvertFact will test all of these cases and guide you.

ConvertFact will not create new fact types or roles. That can't be helpfully
automated and remains a task to be done by the user within RM.

ConvertFact can be configured to convert only a subset of the facts of a certain
fact type based on the date of the fact and/or the description of the fact.


=========================================================================DIV80==
Backups

IMPORTANT
This utility modifies the RM database file.
You should run this script on a copy of your database file (or at least
have multiple known-good backups) until you are confident that the changes made
are the ones desired.

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

RM 8 and later and much earlier version of Python, say after 3.10 will
also probably work but have not been recently tested.

The python script file has also not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3.n installed.

=========================================================================DIV80==
General Overview

This program is what is called a "command line utility". It is in the form of a
single text file with a "py" file name extension ("ConvertFact.py")
along with the package "RMpy" which is a folder included in the 
distribution zip file.
The ConvertFact.py file relies on code in the RMpy folder.
These utilities are not installed in the traditional Windows sense, they are
simply copied to the computer.

The utilities are told what to do by editing a configuration file. This
configuration tells the utility which database to use and how to display the
output.

The default name of the configuration file (called, hereinafter, the
"config file") is "RM-Python-config.ini". For now, it should be located in the
same folder as the MainScriptFile.py file and the RMpy folder.

How it works
Convert Fact is started by the user, a terminal window is displayed,
the program processes the configuration data and the database, a report file
is displayed in Notepad, the terminal window closes and the program exits.


Getting Started     *****  Details follow immediately below. *****

To install and use the utility for the first time:

*  Install Python for Windows x64.

*  Create a new folder on your computer, the "working folder" to contain
   a copy of your database, the program files and the config file.

*  Edit the config file in the working folder to tell the utility what to
   do and how to do it.

*  Double click the ConvertFact.py file to run the utility.

*  A terminal window with a black background and white text will appear.

*  The terminal window will close and a summary report will be displayed
   in Notepad.

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
     (file)     ConvertFact.py
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


==========-
The [CV_PARAMS] section of the config file contains keys for the 
parameters needed to describe the desired changes:

FACTTYPE_CURRENT
FACTTYPE_NEW
ROLE

The [SOURCE_FILTER] section contains the keys that specify
which facts are to be changed.

DESC
DATE

Full details of how to specify the parameters are in the Notes section below.

==========-
Save the config file but leave it open in Notepad.

=========-
Double click the "ConvertFact.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands.

=========-
The terminal window closes and the report file is displayed in Notepad for
your inspection.

=========-
Open the TEST.rmtree database in RM and confirm the desired changes have
been accomplished.

=========-
Consider whether to rename TEST.rmtree and use it as your research database.


=========================================================================DIV80==
Notes

===========-
The config file must be edited to specify the conversion to be executed.

The task is specified by the key value pairs:

[CV_PARAMS]
FACTTYPE_CURRENT  = Census (family)
FACTTYPE_NEW      = Census
ROLE              = Spouse

Note that the value can have embedded spaces.
Space characters between the = and the value are ignored.

===========-
Fact Type name lists

Fact Type full names are listed in RM by the "Fact types" window found in
several places in the RM user interface-
  In the Edit Person window upon clicking the + button (Add fact button or Alt+A)
  In the three dot menu in the Person tab.
  In the command pallet. (type in "fact")

This window also displays, in the right side panel -
* Whether the fact type is Individual or Family.
* The full fact type name and its assigned abbreviation.
The specification of fact types in the config file uses the full fact type name,
not the abbreviation.

===========-
Fact Type fields used

It is best to check the fields used in both fact types before making the change.
If the fields used by the current and new fact types differ (date, place,
description), no data is lost in the conversion. But visibility of the field must
be manually set.

===========-
Fact types in RM come in two categories: Individual and Family.

Facts of the Individual type are linked to a single person while facts of the
family type are linked to a "family", or couple.
An RM database family consists either 2 or 1 persons, labeled internally as
Father and Mother. Either the father or mother may be "unknown"
(and thus set to 0 in the database). Database families, by design, do not
include any offspring.

===========-
Supported fact type conversions:

Individual => Individual
Family => Individual
Family => Family

Not allowed:
Individual => Family


Configuration items in config file required for each type conversion:

* Individual => Individual
FACTTYPE_CURRENT (full name of the fact type of the facts that that 
                  should be converted)
FACTTYPE_NEW (full name of the fact type that existing facts should 
                 be converted to)
(ROLE is ignored)

* Family => Individual
FACTTYPE_CURRENT
FACTTYPE_NEW
ROLE (name of an existing role associated with the FACTTYPE_NEW)

* Family => Family
FACTTYPE_CURRENT
FACTTYPE_NEW
(ROLE is ignored)

===========-
Limiting which Facts are changed

There may be situations in which only a subset of facts should be changed to a
new fact type. One can limit the facts by fields that describe them- 
the Description and the Date-

Some examples-

[SOURCE_FILTER]
DESC              = New York
DATE              = 1930

if you want to convert only facts whose descriptions start with the
words "New York", then enter-

[SOURCE_FILTER]
DESC              = New York%
DATE              =

notice the trailing percent sign.
If the fact descriptions should only contain "New York" somewhere in the text,
enter-

[SOURCE_FILTER]
DESC              = %New York%
DATE              =

The percent sign % wildcard matches any sequence of zero or more characters.
The underscore _ wildcard matches any single character.

To limit the facts converted by their Date, use the DATE value.
The DATE value is always a four digit year.
For example-

[SOURCE_FILTER]
DESC              = 
DATE              = 1930

The values for DESC and DATE are optional. If all facts of a certain type are to be converted,
leave these fields blank-

[SOURCE_FILTER]
DESC              = 
DATE              = 

===========-
Complications handled by this utility

The first complication comes with converting a Family fact to a Individual fact.

A family fact is linked to a father-mother couple. If the father is know, then
the new Individual fact will be linked to the father. If the mother is also
known, the mother will be added as a witness to the new Individual fact.
Her role is specified in the config file as "ROLE =".

If the father is not known then the new Individual fact will be linked to the
mother. There is no new witness added, so the ROLE config file item is ignored.


The second complication arises when the facts of FACTTYPE_CURRENT have witnesses.

Background: Every witness is assigned a role in RM when the fact is shared.
Each fact type has its own set of roles. Many of the roles have the same name,
for instance "Witness" however they are still separate and the sentence assigned
to each of the roles are probably different.

If the original fact type, say Census (fam) had a role named "Spouse", and that
fact type is to be converted to "Census", then the fact of type census will
have the former witness transferred to it maintaining the former role, in this
case "Spouse". If "Census" does not have already have a role named Spouse,
the utility will complain and request that you create such a role for "Census"
before the conversion can be completed.

You don't have to recreate all of the roles that exist for the FACTTYPE_CURRENT,
only the ones that are in use. The ConvertFact report will tell you which ones.


=========================================================================DIV80==
Precautions before using the modified database

Once you are satisfied with the results of the modifications made by this
software, don't hurry to start using the resulting file for research.
Continue your usual work for several days using the original database to allow
further thought. Then run the utility again with your perfected config
file on a new copy of your now-current database. Inspect the results and then
use the modified database as your normal research file.

The week delay will give you time to think about what could go wrong. You should
consider unexpected changes to your data that you did not want.

If you start using the newly modified database immediately, you'll lose work
if you missed a problem only to find it later and have to revert to a backup
from before the database was modified.

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

=========================================================================DIV80==
APPENDIX  Config file: location, contents and editing

Name and folder location
The utility requires a configuration file. A file named "RM-Python-config.ini"
will be recognized as the utility's configuration file when placed in the same
directory as the ConvertFact.py file. Each utility is distributed with
a sample config file to get you started.

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "ConvertFact.py" is executed from a terminal
window which has the folder "C:\Users\me\TestFolder" as its 'current directory',
it will use the configuration file "C:\Users\me\TestFolder\RM-Python-config.ini"
if it exists. If the utility is run with an explicit argument, such as:
ConvertFact.py "C:\Users\me\Documents\RM-Python-config.ini" then the
specified ini configuration file will be used instead.

Note also that the file name is not restricted to the default.
For instance, running the utility from a terminal window as:
ConvertFact.py config_mine.ini
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

Text Encoding
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an umlauted ä in the first line comment to
force it to be in the correct format.
Text encoding can be found in the file format option in the "Save file" dialog
box in NotePad.

=========================================================================DIV80==
TODO

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
Utility Version: 1.2.0 BETA
Built: 2026-11-27 15:20:16
================================================================================
