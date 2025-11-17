=========================================================================DIV80==
Group persons by using SQL
GroupFromSQL.py


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

This utility uses SQL to query the database file and create a RM group in the
RM database independently of RM. Groups may be created with RootsMagic software,
of course, but the types of queries are much more limited.

This utility will update one or more RM groups from any SQL query that returns
a list of RINs/PersonIDs.


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

==========-
Install Python for Windows x64  -see "APPENDIX  Python install" below.

==========-
Create a folder on your computer that you will not confuse with other
folders- the "working folder".

==========-
*  Copy these items from the downloaded zip file to the working folder-
      GroupFromSQL.py                  (file)
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


==========-
Create or find a SQL statement that returns the RINs of the people you want
to put into a group.
for example, the SQL that returns all of the people in a database is-

SELECT PersonID FROM PersonTable

Enter the SQL statement into the config file so the utility can use it.

[OPTIONS]
GROUP_NAME = GroupEveryone

#-----------------------------------------------
[GroupEveryone]
SQL_QUERY = SELECT PersonID FROM PersonTable

#-----------------------------------------------

Shown are two sections: "OPTIONS" and "GroupEveryone".

Section "OPTIONS" has one key :"GROUP_NAME" which has the value "GroupEveryone".

Section "GroupEveryone" has one key: "SQL_QUERY" which has the
value "SELECT PersonID FROM PersonTable".

This example, if run with the utility, will update the group GroupEveryone, already 
existing in the database, using the SQL statement show.
The example SQL_QUERY is very simple and fits on the same line as the key name.
Real SQL will be much more complex and require multiple lines.
Each line of a multi line Value must be indented at least one space.

for example:

SQL_QUERY =
   --
   -- selects person whose married name starts with 'sm'
   SELECT pt.PersonId
   FROM PersonTable AS pt
   INNER JOIN NameTable AS nt ON pt.PersonId = nt.OwnerId
   WHERE nt.NameType = 5    -- married name
   AND nt.surname LIKE 'sm%'

The SQL_QUERY key specifies the SQL statement that will be run.
It must return a set of PersonID's. The statement may begin on the next line,
as above, as long as the SQL lines are all indented with white space.
Blank lines are not allowed.
Use indented SQL comments (--) to add spacing for readability.

# style comments are not allowed in multi line values.


The GROUP_NAME value in OPTIONS may also have multiple lines, that is
multiple group names. Each of those group will be updated in the same run
of the utility and listed separately in the report.

Your config file can contain multiple sections each with SQL statements.
Only the sections specified by [OPTIONS] GROUP_NAME will be used. The others
are ignored.

=========-
Double click the "GroupFromSQL.py" file in the working folder
to start the utility.

=========-
A terminal window is displayed while the utility processes
the commands.

=========-
The report file is displayed in Notepad for you inspection.

=========-
Open the TEST.rmtree database in RM and confirm the desired changes have
been accomplished.

=========-
Consider whether to rename TEST.rmtree and use it as your research database.


=========================================================================DIV80==
Notes

=========-
This utility will not help you write the SQL statement and is not a good
working environment in which to create your SQL statement.
Confirm you query works before running it in this utility. (Or get the SQL from
a source that has confirmed its results. This app is written so that incorrect
SQL will not damage your database, only give groups with unwanted members.)
It is suggested that you write and debug your SQL in a GUI SQLite manager app,
such as "SQLite Expert Personal", the 64bit version, a free app. Several others
are also available.

Note that the SQL statement is run in an environment that does not have the
RMNOCASE collation used by RM for most name type columns. Use "COLLATE NOCASE"
to avoid errors.

=========-
Also remember, that groups in RM, are always groups of Persons. So if you want
to find all RM facts with a certain characteristic, you need to create a group of
the people that have that fact attached. Once the group is created, you will
need to search each person's edit window for the fact you are interested in.

=========-
Due to technical issue regarding RMNOCASE, this utility will not actually create a
new group. Instead use RM to create the group name before using this utility.
The process is simple-
Open the database in RM,
Click the Command palette icon in the top right corner of the RM window.
Type "Group" and select the "Groups" command.
In the Add New Group window, type the name of the new group and hit Save.
Be sure the name is unique among group names.
Leave the Type set to "Simple" as is the default.

The same Add New Group window can be accessed by clicking the large plus icon in
the groups tab in the "Side View" which by default is on the left.

=========-
Updating the contents of a group while the database is open in RM works OK.
However, RM lists using group (simple style) filters do not have a refresh button,
so, for example, if you displaying People view filtered by the group that has been
updated, you'll need to switch to another group and then back again to see the
effect of the group having been updated.

=========-
On some occasions, the utility report file will display a "Database
Locked" message. In that case, close RM and re-run the utility, then re-open 
RM. It's not clear why this sometimes happens, but it is rare. 
For some reason, RM keeps an open transaction which prevents other processes
from making updates.
No database damage has ever been seem after many hundreds of uses. 
"Database locked" is a normal message encountered from SQLite.

Less important notes.

=========-
All SQL statements have not tested :)
The utility takes the input SQL and creates a temporary view based on it. If that
fails, an appropriate error is returned. That should protect against SQL that
modifies/deletes data. (This is not tested beyond simple cases.)

=========-
This utility will, if so configured, modify a pre-existing group that may be
important to you. Take care when assigning the group name: [OPTIONS] GROUP_NAME.

=========-
This utility only changes the GroupsTable in the database

=========-
This utility creates a temporary view named: PersonIdList_RJO_utils and
deletes it when done.

=========-
(For testing) To create a "database locked" situation, start a transaction
in an external SQLite tool, try to run this utility. Will get locked message 
until transaction in SQLite Expert is either committed or RolledBack.

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

* COLOR:  Consider adding color coding functions.
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
