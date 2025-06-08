=========================================================================DIV80==
Color code people by group membership
ColorFromGroup

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third part tools is a major advantage
to using RM.
This software accesses that database directly to provide functionality not found
in the RootsMagic program.


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
You should run this script on a copy of your database file or at least
have multiple known-good backups until you are confident that the changes made
are the ones desired.


=========================================================================DIV80==
Compatibility

Tested with RootsMagic v 10
Tested with Python for Windows v3.13   64bit

The py file has not been tested on MacOS but could probably be easily
modified to work on MacOS with Python version 3 installed.


=========================================================================DIV80==
Overview

This program is what is called a "command line utility". 
To install and use the script:

*  Install Python for Windows x64  -see immediately below

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy these files and folder from downloaded zip file to the working folder-
      ColorFromGroup.py
      RM-Python-config.ini
      RMpy

*  Edit the file, RM-Python-config.ini (hereinafter referred to as the
   "config file") in the working folder.

   The utility needs to know where the RM database file is located, the output
   report file name and its location.

   The config file also tells the utility what actions to perform.

*  Double click the ColorFromGroup.py ile to run the utility and
   generate the report text file.

*  Examine the report file to confirm success.

*  Open the TEST database in RM and confirm the desired colorization results.


=========================================================================DIV80==
Python install-

Either install Python from the Microsoft Store
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

Direct link to recent (as of 2024-12) version installer-
https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


=========================================================================DIV80==
Config file: location, contents and editing

Name and location
The RM-Python-config.ini file will be recognized as the configuration file when
placed in the same directory as the Python script (.py file) for the utility.
The file uses the standard ini file format.

The configuration file name and location can also be specified on the command-line
as an argument to the script. This argument overrides the default configuration
file located in the current directory if it exists.

For example, if the script "RMutility.py" is executed from the folder
"C:\Users\me\Joe", it will use the configuration file 
 C:\Users\me\Joe\RM-Python-config.ini" if it exists.
However, if the utility is run with an explicit argument, such as:
  RMutility.py "C:\Users\me\Joe\documents\RM-Python-config.ini"
then the specified configuration file will be used instead of the default
Note that the file name is also not restricted to the default. 
For instance, running the utility with:
  RMutility.py "C:\Users\me\Joe\documents\Rmine.ini"
will instruct the utility to read Rmine.ini for its configuration parameters.

The configuration file might be named so as to convey its purpose.
A Windows shortcut can also be constructed with the above described argument
to allow execution from the desktop with a double mouse click.

Contents
The config file is made up of the elements: Sections, Keys, Values and
Comments. The names in square brackets are Section Names that identify the start
of a section. A Section contains Key = Value pairs. Names on the left of
the = sign are Keys. Text on the right side of the = is the Value of the Key.
Comment lines start with # and are only included to help the user read and
understand the file.

Encoding
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.


=========================================================================DIV80==
Running the utility in detail

==========-

=========================================================================DIV80==
Notes

Before starting, you will want to confirm that a group exists in your database
that will be the basis of the color operation. Make sure that you know the
exact spelling of the name and that there is only one group with that name.

Next, determine the color group that you wish to modify and the specific color 
number. To get the numbers, open the color coding window in RM. 
Looking at the "Current color code set" drop down menu at the top of the window,
the top-most item is set 1, the bottom is set 10. By default they are named
"Color code set 1"  etc.. If they have been renamed, you'll have to count.
Looking at the left hand column of colors, counting from the top color, Pink 
is 1, Slate is 27.

Next, determine whether there will be more than one action to perform. Usually,
if you want to make a group correspond to a color, you will want to reset/clear 
that color before assigning group members. This will take care of cases in which
people have been removed from groups.

To edit the config file, open NotePad and drag the config file onto the NotePad 
window.

The config file is made up of Sections, Keys, Values and Comments. The names
in square brackets are Section Names that identify the start of a section. A
Section contains Key = Value pairs. Names on the left of the = sign are Keys.
Text on the right side of the = is the Value of the Key. Comment lines start
with # and are only included to help the user read and understand the file.

[FILE_PATHS]
DB_PATH  = TEST.rmtree
REPORT_FILE_DISPLAY_APP  = C:\Windows\system32\Notepad.exe
REPORT_FILE_PATH  = Report_ColorFromGroup.txt

[OPTIONS]
COLOR_COMMAND = 
  Color_my_family_C
  Color_my_family_S

#-----------------------------------------------
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

Shown are four sections: FILE_PATHS, OPTIONS and Color_my_family_C and 
Color_my_family_S

These sections have varying numbers of keys-
section                  number of keys
FILE_PATHS                  3
OPTIONS                     1
Color_my_family_C           4
Color_my_family_S           4

The FILE_PATH keys are self explanatory. Just note that either absolute or 
relative paths may be used for any of the paths.

The COLOR_COMMAND key in OPTIONS list the sections that contain actions to execute.
The key can contain one section name, like
COLOR_COMMAND =   Color_my_family_C

or multiple section names, like-
COLOR_COMMAND = Color_my_family_C
  Color_my_family_S

  or, like
COLOR_COMMAND = 
  Color_my_family_C
  Color_my_family_S

Note that the second and following section names must be indented.

The last two sections are color commands. Each color command section must 
have the four shown keys.
The name of the color command section is set by the user. (You may want to use
the same name as the group.)

Your config file can contain multiple color command sections, but only those 
listed in COLOR_COMMAND will be executed. The others are ignored. You may want
to keep unused sections in the config file for future use. (Just like 
the GroupFromSQL utility.)

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


Less important notes.

=========-
This utility only changes the database's PersonTable.
If I add the feature of renaming colors, that will affect the Config table.

=========-
This utility will, if so configured, modify a pre-existing color coding 
that may be important to you. Take care when assigning the actions in the
config file.


=========================================================================DIV80==
=========================================================================DIV80==
=========================================================================DIV80==
Troubleshooting:

=========-
No Report File displayed

If the report is created, but not displayed, check the config
file line- REPORT_FILE_DISPLAY_APP

If no report file is generated, look at the black command
console window for error messages that will help you fix the problem.
There may be something wrong with the config file line- REPORT_FILE_PATH

If the black console windows displays the message-
RM-Python-config.ini file contains a format error
See the section below.

If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console and then
running the py file from the command line. The window will not close
and you'll be able to read any error messages.

=========-
Error message:
RM-Python-config.ini file contains a format error

Start over with the supplied config file and make sure that works, Then make your
edits one by one to identify the problem.
You may want to look at- https://en.wikipedia.org/wiki/INI_file

=========-
Multiline Values
Probably the trickiest part of the config file is the COLORS key in OPTIONS.
It may be assigned either a single or multi line value.
Each line of the value should be on a separate line indented with at least 
one blank. An empty line generates an error.
Multi-line values may not contain comment lines (lines starting with a #).

examples-

correct formats-

COLOR_COMMAND = GroupName1

COLOR_COMMAND =
  GroupName1

COLOR_COMMAND = GroupName1
  GroupName2
  GroupName3

COLOR_COMMAND =
  GroupName1
  GroupName2
  GroupName3


incorrect format- (empty line not allowed)

COLOR_COMMAND =
  GroupName1

  GroupName2
  GroupName3


incorrect format (not indented)

COLOR_COMMAND =
GroupName1
GroupName2
GroupName3

incorrect format (no commented lines in the multi line value)

COLOR_COMMAND =
  GroupName1
 #  GroupName2
  GroupName3


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
