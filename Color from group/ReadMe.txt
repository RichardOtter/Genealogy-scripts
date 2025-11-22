=========================================================================DIV80==
Color code people by group membership
ColorFromGroup.py


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
files in a text editor to read all implementation details and assess safety.

A Python py script file is executed using the Python language interpreter.
The interpreter is a separate piece of software easily installed on your
computer. "Installing python" is described in the appendix below.


=========================================================================DIV80==
Purpose

This utility will change the color coding/color high-lighting of people in
the database based on their group membership.
While this is easily done with RM, this utility allows a series of commands
to be executed with one run.
It is a perfect complement to the utility GroupFromSQL.


=========================================================================DIV80==
Backups

IMPORTANT
This utility modifies the RM database file.
You should run this script on a copy of your database file (or at least
have multiple known-good backups) until you are confident that the changes made
are the ones desired.

=========================================================================DIV80==
Compatibility

Tested with a RootsMagic v 11.0.2 database
using Python for Windows v3.14   64bit

The python script file has not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3.n installed.

=========================================================================DIV80==
Overview

This program is what is called a "command line utility".
It is in the form of a single text file with a "py" file name extension
(referred to, in this section, as "MainScriptFile.py"). The utility also
needs the Python package RMpy, which is a folder included in the distribution
zip file.

Input to the utility is through the configuration file and. for some of the
utilities, the command terminal.
The the default name of the configuration file (called, hereinafter, the
"config file") is "RM-Python-config.ini". It should be located in the same
folder as the MainScriptFile py file and the RMpy folder. At a minimum, the config
file gives the name and location of the database on which the utility operates.

One config file can be shared among other RM utilities in the suite. Each
utility will extract the information it needs from the config file.

To install and use the script for the first time:

*  Install Python for Windows x64  -see "APPENDIX  Python install" below.

*  Create a new folder on your computer, perhaps within your home folder.
   This folder will be called the "working folder".

   (Your home folder is "C:\Users\me", where "me" is your user name.
   This is a safe location that will not be taken over by OneDrive.)

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy the program files/folder from the downloaded zip file to
   the working folder.

*  Copy the sample config file from the downloaded zip file to
   the working folder.

*  Edit the config file in the working folder to tell the utility what to
   do and where to do it.

*  Double click the MainScriptFile .py file to run the utility.

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

Other utilities that involve more configuration and make larger changes should
always operate on databases copied into a working folder.

*****  Details follow below. *****


=========================================================================DIV80==
Running the utility in detail

==========-
Install Python for Windows x64  -see "APPENDIX  Python install" below.

==========-
Create a folder on your computer that you will not confuse with other
folders. It will be referred to as the "working folder".

==========-
Copy these items from the downloaded zip file to the working folder-
      ColorFromGroup.py                (file)
      RM-Python-config.ini             (file)
      RMpy                             (folder)

==========-
Make a copy of your database, move the copy into the working folder.

Rename the database copy to "TEST.rmtree" in order to prevent any
confusion about the purpose of the copy.

==========-
Edit the RM-Python-config.ini file in the working folder.
(See the section "APPENDIX  Config file: location, contents and editing" if you need help)

Check that the DB_PATH key in the config file is pointing to the
desired database.
If the above steps were followed, the path in the sample config file
is already correct, i.e. TEST.rmtree

Save the config file but leave it open in Notepad.

==========-
Before running the utility, you will want to confirm that a group exists
in your database that will be the basis of the color operation.
Make sure that you know the exact spelling of the name and that there
is only one group with that name.

==========-
Next, determine the color group that you wish to modify and the specific
color number. To get the numbers, open the color coding window in RM.
Looking at the "Current color code set" drop down menu at the top of the window,
the top-most item is set 1, the bottom is set 10. By default they are named
"Color code set 1"  etc.. If they have been renamed, count down the groups
to get the set's number. Looking at the left hand column of colors,
counting from the top color, Pink is 1, Slate is 27.

Next, determine what actions you wish to perform.
Usually, if you want to make a group correspond to a color, you will want to
reset/clear that color before assigning group members. This will take care of 
cases in which people have been removed from groups.
So for every group that you want to color, you will want to do a clear and then
a color operation on that group.

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

==========-
Next, tell the utility what color operations to perform.
This requires a bit of explanation.
Each operation is contained in a separate section of the config file.
In a color operation section, reside 4 key=value pairs. These 4 items
define a color code operation.

ACTION can be one of: set, clearAny, clearOnlyIf, or setOnlyIf.
COLOR_CODE_SET takes a value of 1 to 10
COLOR takes a value of 1 to 27
GROUP takes a name of a group or "_ALL" which indicates all people in
      the database. The "_ALL" option is only usable
      with the clearAny and ClearOnlyIf actions.

Taken together, these 4 parameters give all of the necessary information 
for a color operation.

The distinctions between set vs setOnlyIf  and clearAny vs. ClearOnlyIf is
a bit subtle.

set vs setOnlyIf
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


As mentioned above, each set of color operation parameters is in its own 
section. The section name is completely arbitrary, but you may want to use 
a name that is similar to the group and add a character at the end to 
indicate Set or Clear. See the sample config file.

You can create as many of these sections as you wish. Each of these sections
will have all four color operation parameters (key-value pairs).

The last item to cover is the OPTIONS section.
It contains one key named: COLOR_COMMAND. It's value can be a single name, 
or it can be a multi-line value containing multiple names.

The key's value correspond to the section names you created earlier to
contain the 4 color parameters.
The section names listed in the COLOR_COMMAND are the color operations that 
will actually be performed by a run of the utility.

The color operations in a utility run are performed in the order that
they are listed in the COLOR_COMMAND's value.

Example:

#-----------------------------------------------
[OPTIONS]
COLOR_COMMAND =
  Color_my_family_C
  Color_my_family_S

[Color_my_family_C]
ACTION = clear
COLOR_CODE_SET = 5
COLOR = 1
GROUP = _ALL

[Color_my_family_S]
ACTION = set
COLOR_CODE_SET = 5
COLOR = 1
GROUP = FamGroup
#-----------------------------------------------

In this example, there are 3 sections: OPTIONS, Color_my_family_C, 
and Color_my_family_S.

The COLOR_COMMAND key in OPTIONS lists the sections that contain actions 
to execute.

When COLOR_COMMAND needs to specify more than one section name, it is entered
as a multi-line value. There are 3 rules for multi-line values:
1 each section name is on a separate line
2 each line, after the first, must be indented with at least one space.
3 the value can not contain an empty line.


The key can contain one section name, like
COLOR_COMMAND =   Color_my_family_C

or multiple section names, like-
COLOR_COMMAND = Color_my_family_C
  Color_my_family_S

or

COLOR_COMMAND =
  Color_my_family_C
  Color_my_family_S


Your config file can contain multiple color action sections, but only those
listed in COLOR_COMMAND will be executed. The others are ignored. 

You may want to keep unused sections in the config file for future use. 

The keys in the color command section are ACTION, COLOR_CODE_SET, COLOR, and GROUP.
ACTION is either set or clear
COLOR_CODE_SET is a number from 1 to 10.
COLOR is the color to use 1-27
GROUP is the RM group name that specifies which people are to have their code
code set.
If the ACTION is clear, then the GROUP should be set to "_ALL".
If ACTION is set, then GROUP must be the name of an existing RM group.

ACTION clear only clears a particular color in a particular color code set.
It does this for all people (thus the group name placeholder "_ALL")

The utility does not allow clearing all colors in a color code set or
clearing colors in multiple color code sets.

==========-
After confirming that your edits to the config file are saved,

Double click the "ColorFromGroup.py" file in the working folder to run
the utility.

=========-
A terminal window is displayed while the utility processes
the commands.

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
The GROUP key specifies which people in the database the color operation 
is to be performed on. It can be either the name of a RM person group or "_ALL".

_ALL will operate on all people in the database. It may only be used 
for clear color operations.

=========-
ACTION can be one of: set, clearAny, ClearOnlyIf, or setOnlyIf.

COLOR_CODE_SET takes a value of 1 to 10

COLOR takes a value of 1 to 27

GROUP takes a name of a group or "_ALL" which indicates all people in
      the database. The "_ALL" option is only usable
      with the clearAny and ClearOnlyIf actions.

Taken together, these 4 parameters give all of the necessary information 
for a color operation.

The distinctions between set vs setOnlyIf  and clearAny vs. ClearOnlyIf is
a bit subtle.

set vs setOnlyIf
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

The choice between each pair will depend on the exact circumstances: what other
color operations have been performed and the order in which they were done.
The same considerations apply when using the RM user interface to do color
coding.

RM's command "Clear Color for people selected above" does the 
equivalent of the clearAny option in this utility. No matter what color happens
to be selected, the color of the selected people is cleared.

The previous release of this software used the clearOnlyIf option.

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
This utility only changes the database's PersonTable.

=========-
This utility will, if so configured, modify a pre-existing color coding
that may be important to you. Take care when assigning the actions in the
config file.

=========================================================================DIV80==
APPENDIX  Config file: location, contents and editing

Name and location
The utility requires a configuration file. A file named "RM-Python-config.ini"
will be recognized as the utility's configuration file when placed in the same
directory as the MainScriptFile py file for the utility. Each utility is
distributed with a sample config file to get you started.

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "RMutility.py" is executed from a terminal window
which has the folder "C:\Users\me\TestFolder" as its 'current directory', it
will use the configuration file "C:\Users\me\TestFolder\RM-Python-config.ini"
if it exists. If the utility is run with an explicit argument, such as:
RMutility.py "C:\Users\me\Documents\RM-Python-config.ini"
then the specified configuration file will be used instead.

Note also that the file name is not restricted to the default.
For instance, running the utility from a terminal window as:
RMutility.py config_mine.ini
will instruct the utility to use config_mine.ini in the current directory
as its configuration file.

A configuration file that is used from the command line can be renamed so as
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

The utilities all generate a report file. The file's name and location can be
specified by REPORT_FILE_PATH key.

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
Download and install from the Python.org web site

From Microsoft Store
Run a command in Windows by pressing the keyboard key combination
"Windows + R", then in the small window, type Python.
Windows store will open in your browser and you will be be shown
the various versions of Python.
Click the Get button for the latest version.

Python.org web site download and install
https://www.python.org/downloads/

Click on the button near the top of page: "Download Python install manager"
Click it and save the installer.
Go to the download location and run the installer.

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard Windows method found in
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

Examine the file visually and check to see that it follows the rules mentioned
above. If all else fails, start over with the supplied config file and make
sure that it works, Then make your edits one by one to identify the problem.
You may want to look at- https://en.wikipedia.org/wiki/INI_file



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
