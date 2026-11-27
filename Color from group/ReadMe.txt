=========================================================================DIV80==
Color code people by group membership
ColorFromGroup.py


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

This utility will change the color coding/color high-lighting of people in
the database based on their group membership.
While this is easily done with RM, this utility allows a series of commands
to be executed with one run.
It is a perfect complement to the utility GroupFromSQL.
First run GroupFromSQL to update a set of groups, then run ColorFromGroup to
update the colors. Two double clicks and you're done.

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
single text file with a "py" file name extension ("ColorFromGroup.py")
along with the package "RMpy" which is a folder included in the 
distribution zip file.
The ColorFromGroup.py file relies on code in the RMpy folder.
These utilities are not installed in the traditional Windows sense, they are
simply copied to the computer.

The utilities are told what to do by editing a configuration file. This
configuration tells the utility which database to use and how to display the
output.

The default name of the configuration file (called, hereinafter, the
"config file") is "RM-Python-config.ini". For now, it should be located in the
same folder as the MainScriptFile.py file and the RMpy folder.

How it works
Color from Group is started by the user, a terminal window is displayed,
the program processes the configuration data and the database, a report file
is displayed in Notepad, the terminal window closes and the program exits.


Getting Started     *****  Details follow immediately below. *****

To install and use the utility for the first time:

*  Install Python for Windows x64.

*  Create a new folder on your computer, the "working folder" to contain
   a copy of your database, the program files and the config file.

*  Edit the config file in the working folder to tell the utility what to
   do and how to do it.

*  Double click the ColorFromGroup.py file to run the utility.

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
     (file)     ColorFromGroup.py
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
You will be editing additional settings.

==========-
Before running the utility, you will want to confirm that a group exists
in your database that will be the subject of the color operation.
Make sure that you know the exact spelling of the name and that there
is only one group with that name.

==========-
Next, determine the color set group that you wish to modify and the specific
color number. 
To get the set number:
Open the color coding window in RM.
Looking at the "Current color code set" drop down list at the top of the window,
the top-most item is set 1, the bottom is set 10. By default they are named
"Color code set 1"  etc.. If they have been renamed, count down the groups
to determine the set number.

To get the color's number:
Looking at the left hand table of colors,
Count down from the top color, Pink is color 1, Slate is color 27.

==========-
Next, determine what actions you wish to perform.
If you want to highlight a group of people with a color, and you want that
color to indicate that a person is a group member, you will want to
reset/clear that color before assigning group members. This will take care of 
cases in which people have been removed from groups.
So for every group that you want to color, you will want to do a clear and then
a set color operation on that group.

==========-
Next, tell the utility what color operations to perform.
This is done by making further edits to the config file started earlier.

The edits require a bit of explanation, most of which is in the Notes
section,below.

****
**** For now, using a test database, just try something simple, understand what
happens, then move on to more sophisticated operations with the test database.

Each color operation is contained in a separate section of the config file
called a color operation section. 
The list of color operations to be performed is in the COLOR_COMMAND key
within the OPTIONS section.

So for example, the sample config file contains-

[OPTIONS]
COLOR_COMMAND = Relatives_C

[Relatives_C]
ACTION = set
COLOR_CODE_SET = 10
COLOR = 10
GROUP = MyCousins

The section [Relatives_C] is a color operation section. It has 4 key/value pairs
that determine what it will do.

The COLOR_COMMAND in the OPTIONS section, lists the name(s) of the
color operation section(s) to execute. In this case, just the one
operation, Relatives_C.

If the utility is run with this config, all people in the group MyCousins will
be highlighted by color 10 (red) when color set 10 is active.

To try it out in your test database, make sure that GROUP is set to the name
of a real group and that the group has members, and that the choice of color
set and color will result in a change that you will be able to observe
and verify.

See Notes section for details on each of the 4 key/value pairs in a color 
operation section and the COLOR_COMMAND listing of operations to run.

==========-
After confirming that your edits to the config file are saved:
Double click the "ColorFromGroup.py" file in the working folder to run
the utility.

=========-
A terminal window is displayed while the utility processes the commands.

=========-
The terminal terminal window closes and the report file is displayed
in Notepad for you inspection.

=========-
Open the TEST.rmtree database in RM and confirm the desired changes have
been accomplished.

=========-
Consider whether to rename TEST.rmtree and use it as your research database.


=========================================================================DIV80==
Notes

=========- 
Color operation section name 

Most any name should work.
To help keep things organized, I use a naming system where the operation section
name start with the group to be operated on followed by either _C or _S,
depending on whether it will clear or set a color.

You can create as many of these sections as you wish. 
Color operation section names not listed in the COLOR_COMMAND are ignored.
You may want to keep unused sections in the config file for future use. 

=========-
Color operation section key/values pairs required

Each color operation section must contain 4 key=value pairs. 

The names and meanings of the keys are:
ACTION can be one of: set, clearAny, clearOnlyIf, or setOnlyIf.
COLOR_CODE_SET takes a value of 1 to 10
COLOR takes a value of 1 to 27
GROUP takes a name of an existing group or "_ALL" 
      which indicates all people in the database. 
      The "_ALL" option is only allowed for use
      with the clearAny and ClearOnlyIf actions.

Taken together, these 4 parameters give all of the necessary information 
for a color operation.

=========-
Creating a COLOR_COMMAND

The key's value correspond to one or more of the section names you created
earlier to contain the color action parameters.
The section names listed in the COLOR_COMMAND are the color operations that 
will actually be performed by a run of the utility.
The color operations in a utility run are performed in the order that
they are listed in the COLOR_COMMAND's value.


When COLOR_COMMAND needs to specify more than one section name, it is entered
as a multi-line value. There are 3 rules for multi-line values:
1 each section name is on a separate line
2 each line, after the first, must be indented with at least one space.
3 the value can not contain an empty line.

examples-
The key might contain one section name, like
COLOR_COMMAND =   Color_my_family_C

or multiple section names, like-
COLOR_COMMAND = Color_my_family_C
  Color_my_family_S

or

COLOR_COMMAND =
  Color_my_family_C
  Color_my_family_S


Also see: APPENDIX  Config file: location, contents and editing
for more details in editing the config file.

=========-
Another example:

#-----------------------------------------------
[OPTIONS]
COLOR_COMMAND =
  FamGroup_C
  FamGroup_S

[FamGroup_C]
ACTION = clear
COLOR_CODE_SET = 5
COLOR = 10
GROUP = FamGroup

[FamGroup_S]
ACTION = set
COLOR_CODE_SET = 5
COLOR = 10
GROUP = FamGroup
#-----------------------------------------------

In this example, there are 3 sections: OPTIONS, FamGroup_C, 
and FamGroup_S.

The COLOR_COMMAND key in OPTIONS lists the sections that contain actions 
to execute.

=========-
The distinctions between the ACTIONs set vs. setOnlyIf and clearAny vs.
ClearOnlyIf is a bit subtle.

set vs. setOnlyIf
The set action will always color code the people under consideration (either 
a group or all) no matter what color they are currently coded as.
The setOnlyIf action has an extra criterion, for the people under consideration
(either a group or all), only those people who currently have no color code
will be color coded with the specified COLOR.

clearAny vs. ClearOnlyIf
ClearAny is simplest. For the people under consideration (either a group or all)
the person's color code is cleared (set to 0).
ClearOnlyIf has an extra criterion, for the people under consideration (either
a group or all), only those people who are currently color coded by the color
indicated by the COLOR parameter, have their color code cleared (set to 0).
Note that the COLOR value is ignored for the clearAny operation.


The choice between each ACTION pair will depend on the exact circumstances: 
what other color operations have been performed and the order in which they
were done. The same considerations apply when using the RM user interface to
do color coding.

RM's command "Clear Color for people selected above" does the 
equivalent of the clearAny option in this utility. No matter what color happens
to be selected, the color of the selected people is cleared.

=========-
Updating the colorization of a group while the database is open in RM
works OK. However, RM will not refresh the screen based on an external update.
So, switch screens and then return to see the updated color coding.

=========-
On some occasions, the utility report file will display a "Database
Locked" message. In that case, close RM and re-run the utility, then re-open
RM. It's not clear why this sometimes happens, but it is rare.
No database damage has ever been seem after many hundreds of uses.
"Database locked" is a normal operating message encountered from SQLite.

=========-
This utility changes only the database's PersonTable.

=========-
CAUTION

This utility will, if so configured, modify a pre-existing color coding
that may be important to you. Especially if it was created manually.
Take care when assigning the actions in the config file.

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
directory as the ColorFromGroup.py file. Each utility is distributed with
a sample config file to get you started.

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "ColorFromGroup.py" is executed from a terminal
window which has the folder "C:\Users\me\TestFolder" as its 'current directory',
it will use the configuration file "C:\Users\me\TestFolder\RM-Python-config.ini"
if it exists. If the utility is run with an explicit argument, such as:
ColorFromGroup.py "C:\Users\me\Documents\RM-Python-config.ini" then the
specified ini configuration file will be used instead.

Note also that the file name is not restricted to the default.
For instance, running the utility from a terminal window as:
ColorFromGroup.py config_mine.ini
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
TODO

*  Consider adding abilities:
*  to specify color by name, color set by name.
*  to rename a color to the group that it represents
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
Utility Version: 1.1.0 BETA
Built: 2026-11-27 15:20:16
================================================================================
