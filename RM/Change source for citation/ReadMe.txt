=========================================================================DIV80==
Change the source for a given citation
ChangeSrcForCitation.py

Utility application for use with RootsMagic databases

RootsMagic (RM) software (https://RootsMagic.com) uses a SQLite relational
database (https://Sqlite.org) as its data storage file. Having access to
the RM data file via third party tools is a major advantage over other
genealogy project management applications.

This software accesses the database directly to provide functionality not
found in the RootsMagic program.

This utility is part of a suite of utilities that has been written to
perform analysis or data modification not available within the RM application.
See https://RichardOtter.github.io

This software is written using the Python language (https://Python.org) and
is distributed as a text ".py" file along with a folder, RMpy, of common Python
code, called a python package. The user can simply open the file or package
files in a text editor to read all implementation details and access safety.

A Python py script file is executed using the Python language interpreter.
The interpreter is a separate piece of software easily installed on your computer.


=========================================================================DIV80==
Purpose

RootsMagic has Sources and Citations. Sources are also called "Master Sources".
Citations are also called "Source Details".

Sources are created using a Source Template. If 2 sources are created
from the same source template, they will have the same fundamental structure.

A Citation is created as a child of a Source. Citations of different sources
created using the same source template will have the same fundamental
structure as each other.

This simple utility will move a citation from one source to another source,
but only if the 2 sources were created using the same source template.

For example, if you lump obituary sourced by newspaper, you will have a
number of sources (newspapers) all based on the same source template.
When entering a citation, you may accidentally cite a source set up for the
wrong newspaper. Instead of deleting and recreating the citation, use this
utility to move the citation to the correct source.
The utility will carry along all of the uses of the citation.


=========================================================================DIV80==
Backups

IMPORTANT
This utility modifies the RM database file.
You should run this script on a copy of your database file (or at least
have multiple known-good backups) until you are confident that the changes made
are the ones desired.

=========================================================================DIV80==
Compatibility

Tested with a RootsMagic v 10.0.5 database
using Python for Windows v3.13.4   64bit

The py file has not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3 installed.

=========================================================================DIV80==
Overview

This program is what is called a "command line utility". 
It is in the form of a single text file with a "py" file name extension,
referred to, below, as "MainScriptFile.py". The utility also needs the
Python package RMpy, which is a folder included in the distribution zip file.

Most input to the utility is through the configuration file. (Some utilities
in this suite also take user input from the command line console window.)
The the default name of the configuration file (called, hereinafter the
"config file") is "RM-Python-config.ini". It should be located in the
same folder as the MainScriptFile py script file and the RMpy folder.
At a minimum, the config file gives the name and location of the database on
which to operate. 

One config file can be shared among other RM utilities in the suite. Each
utility will extract the information it needs from the config file.

To install and use the script for the first time:

*  Install Python for Windows x64  -see APPENDIX below

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy these files and the folder from the downloaded zip file to the working folder-

      file:    MainScriptFile.py     (MainScriptFile is the name of this utility)
      folder:  RMpy
      file:    RM-Python-config.ini

*  Edit the config file, RM-Python-config.ini, that was copied into the working folder.

   The utility needs to know where the RM database file is located, the output
   report file name and its location.

*  Double click the MainScriptFile.py file to run the utility. 

*  A summary report will be displayed in NotePad.

*****  Details follow below. *****


=========================================================================DIV80==
Running the utility in detail

While the database name and location is specified in the config file, the actual
instructions for which citations and sources to modify are entered at a series
of prompts in the black command shell window.

=========-
Make sure that the "ChangeSrcForCitation.py" file is in the same folder as
the folder "RMpy" and "RM-Python-config.ini"

=========-
Check that the config file is pointing to the desired database.

=========-
Double click the "ChangeSrcForCitation.py" file to start the utility.

=========-
The command shell window will open and prompt you to enter the name of
the citation to move and the source that it should be moved to.
In both cases, only enough of the name needs to be
entered to make it unique among all citations for all sources.

It is suggested that you copy and paste from the RM source edit window.
There is no need to manually type input.

The standard 'SQL Like' wild card characters % and _ may be used.
% matches 0 or more characters, _ matches one character.
This utility always adds a % to the end of the citation name and
source names entered.

If the full citation name is not unique, then as a workaround, you
could add some text to the citation name of the citation you want
to modify to make the name unique.

=========-
After the source name is entered, either a confirmation or error message
is displayed. In either case, a prompt to change another citation is
shown.

=========-
If n is entered in response to the "another" prompt,  the command
line window is closed and a report file is displayed summarizing the changes made.

=========================================================================DIV80==
Notes

All entered information is verified before it is used. It is unlikely that
random data would be accepted by the utility.

Checks made by the utility:
1- User is asked for the citation name of the citation to modify.
    a) the name must be found.
    b) the name must be unique among all citations for all sources.
   You will be made aware of problems.
2- User is asked for the source that is to be used as the new parent of
   the citation.
    a) the source name must be found.
    b) the source name must be unique.
    c) the existing source used by the citation and the new source
       specified must both use the same source template.
   You will be made aware of problems.


=========================================================================DIV80==
APPENDIX  Config file: location, contents and editing

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
Note that the file name is not restricted to the default.
For instance, running the utility with:
  RMutility.py Rmine.ini
will instruct the utility to read Rmine.ini in the current directory 
for its configuration parameters.

The configuration file might be named so as to convey its purpose.
A Windows shortcut can also be constructed with the above described argument
to allow execution from the desktop with a double mouse click.

Editing
Use any text editor to edit the configuration file. The builtin-to-Windows
app "Notepad" works well.
To edit the configuration file, first open the Notepad app and then use the
mouse to drag the configuration file onto the open Notepad window.

Contents
The config file is made up of the elements: Sections, Keys, Values and
Comments. The names in square brackets are Section Names that identify the start
of a section. A Section contains one or more Key = Value pairs. Names on the left of
the = sign are Keys. Text on the right side of the = is the Value of the Key.
Comment lines start with # and are only included to help the user read and
understand the file.


KEYs used by all of the RM utilities:

[FILE_PATHS]
DB_PATH         = TEST.rmtree
REPORT_FILE_PATH  = Report_ColorFromGroup.txt
REPORT_FILE_DISPLAY_APP  = C:\Windows\system32\Notepad.exe

These KEYS are all in the [FILE_PATHS] section and all require file paths as values.

The file path may be absolute, as in REPORT_FILE_DISPLAY_APP
above, or it may be relative to the current directory, as in DB_PATH and 
REPORT_FILE_PATH above.

The DB_PATH points to the database that is to be analyzed/modified.
See the sections "Backups" and "Running the utility in detail", above, for help
in deciding which database to use. New users will always want to point to a
copy of the main database.

The utilities all generate a textual report file. The file's name
and location can be specified by REPORT_FILE_PATH

If REPORT_FILE_DISPLAY_APP is specified, then the report file will be
automatically displayed by the named application.


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

Web site download and install
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
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


=========================================================================DIV80==
APPENDIX  Troubleshooting

=========-
No Report File displayed

If the report is created, but not displayed, check the config
file line- REPORT_FILE_DISPLAY_APP

If no report file is generated, look at the black command
console window for error messages that will help you fix the problem.
There may be something wrong with the config file line- REPORT_FILE_PATH

If the black console windows displays the message-
RM-Python-config.ini file contains a format error, see the section below.

If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console, cd'ing to
the folder containing the py file and then running the py file from the
command line. The window will not close and you will be able to read any
error messages.

=========-
Error message:
RM-Python-config.ini file contains a format error

Start over with the supplied config file and make sure that works, Then make your
edits one by one to identify the problem.
You may want to look at- https://en.wikipedia.org/wiki/INI_file

=========================================================================DIV80==
TODO

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
