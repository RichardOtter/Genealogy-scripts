=========================================================================DIV80==
Change the source for a given citation
ChangeSrcForCitation.py


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

A RootsMagic database contains records for Sources and Citations. Sources are
also called "Master Sources". Citations are also called "Source Details".

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

The utility will carry along all of the uses of the citation, along with web
links and media.


=========================================================================DIV80==
Backups

IMPORTANT
This utility modifies the RM database file.
You should run this script on a copy of your database file (or at least
have multiple known-good backups) until you are confident that the changes made
are the ones desired.

=========================================================================DIV80==
Compatibility

Tested with a RootsMagic v 10.0.7 database
using Python for Windows v3.13.4   64bit

The py file has not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3.n installed.

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
MainScriptFile py file and the RMpy folder. At a minimum, the config
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

While the database name and location is specified in the config file, the actual
instructions for which citations and sources to modify are entered at a series
of prompts in the black terminal window.

==========-
Install Python for Windows x64  -see "APPENDIX  Python install" below.

==========-
Create a folder on your computer that you will not confuse with other
folders- the "working folder".

==========-
Copy these items from the downloaded zip file to the working folder-
      ChangeSrcForCitation.py          (file)
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
Open the TEST.rmtree database file in RootsMagic.
Having the file open in RM allows one to copy citation and source names, needed
by the utility, directly from the RM window.

=========-
Double click the "ChangeSrcForCitation.py" file in the working folder
to start the utility.

=========-
A terminal window will open and prompt you to enter the name of
the citation to move and the source that it should be moved to.

In both cases, only enough of the name needs to be
entered to make it unique among all citations for all sources.

It is suggested that you copy and paste from the RM source edit window.
There is no need to manually type input.

The standard 'SQL Like' wild card characters % and _ may be used.
% matches 0 or more characters, _ matches one character.
This utility silently adds a % to the end of the citation name  and
source name text entered.

=========-
After the source name is entered, either a confirmation or error message
is displayed.
In either case, a prompt to change another citation is shown. Respond with
either y or n.

=========-
If "n" is entered in response to the "Change another citation" prompt,
the terminal window is closed and the utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

=========-
Confirm the desired changes have been accomplished in RootsMagic

=========-
Consider whether to rename TEST.rmtree and use it as your research database.

=========================================================================DIV80==
Notes

=========-
If the full citation name is not unique, then as a workaround, you
could add some text to the citation name of the citation you want
to modify to make the name unique.

=========-
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
