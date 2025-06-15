=========================================================================DIV80==
Convert an existing fact from one fact type to another
ConvertFact.py


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
Compatibility

Tested with a RootsMagic v 10.0.5 database
using Python for Windows v3.13.4   64bit

The py file has not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3 installed.

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
Running the utility in detail

==========-
Create a folder on your computer that you will not confuse with other
folders. It will be referred to as the "working folder".

==========-
Copy these items from the downloaded zip file to the working folder-
      ConvertFact.py                   (file)
      RM-Python-config.ini             (file)
      RMpy                             (folder)

==========-
Make a copy of your database, move the copy into the working folder.

Rename the database copy to "TEST.rmtree" in order to prevent any confusion 
about the purpose of the copy.

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

==========-
Look at the [CV_PARAMS] section of the config file containing keys for the 
parameters needed to describe the desired changes:

FACTTYPE_CURRENT
FACTTYPE_NEW
ROLE

Now look at the [SOURCE_FILTER] section which contains the keys that specify
which sources are changed.

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
The config file must be edited to indicate the conversion that should be done.

The task is specified by the key value pairs. or example-

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
description), no data is lost in the conversion.

===========-
Fact types in RM come in two categories: Individual and Family.

Facts of the Individual type are linked to a single person while facts of the
family type are linked to a database family.
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

There maybe situations in which only a subset of Facts should be changed to a
new fact type. One can limit the facts by fields that describe them- 
the Description and the Date-

Some examples-

[SOURCE_FILTER]
DESC              = %New York%
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
only the ones that are in use. ConvertFact will tell you which ones.


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
