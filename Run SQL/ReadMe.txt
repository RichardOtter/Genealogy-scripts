=========================================================================DIV80==
Run SQL commands on a RootsMagic database
RunSQL.py


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

This utility will run SQL statements and script files on a database 
and display the results in a text file.

This utility is meant to help the novice SQL user get the task done.
It attempts to eliminate most of the complications found using more
sophisticated off the shelf SQLite manager software.

The ability to run SQL script files can be used by even advanced users to
run database maintenance scripts which give predictable results and
don't need to show output.


=========================================================================DIV80==
Backups

VERY IMPORTANT
This utility makes changes to the RM database file. It can change a large number
of data items in a single run depending on the parameters specified.
You will likely not be satisfied with your first run of the utility and you will
want to try again, perhaps several times, each time making changes to your
configuration file.
You must run this script on a copy of your database file or have at least
multiple known-good backups.

Read about additional considerations in the Precautions section below.

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
folders- the "working folder".

==========-
*  Copy these items from the downloaded zip file to the working folder-
      RunSQL.py                        (file)
      RM-Python-config.ini             (file)
      RMpy                             (folder)

==========-
*  Download the SQLite extension file: unifuzz64.dll   -see below
   (This dll provides a RMNOCASE collation used by RM.)
   Move the unifuzz64.dll file to the working folder.

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
In that section, reside 4 key-value pairs, one of which is 
DB_PATH = TEST.rmtree

"DB_PATH" is the key, "TEST.rmtree" is the value.
key-value pairs are separated with a = character.


The utility needs to know where the RM database file is located, the output
report file name and its location.

The utility also needs to know where the unifuzz64.dll file is.  Its path
is give an the value of the key RMNOCASE.

If you followed the above instructions, no changes to any of the key-values in
the [FILE_PATHS] section are needed.

Save the config file but leave it open in Notepad.


=========-
Enter your SQL statement into the config file using key-value pairs in the
[SQL] section of the file.

The utility will run up to 99 SQL statements. They are written in the config
file as

For example:

[SQL]
SQL_STATEMENT_1 = SELECT PersonID FROM PersonTable


This section "SQL" has one key: "SQL_STATEMENT_1" which has the
value "SELECT PersonID FROM PersonTable".

This example, if run with the utility, will run the very simple SQL statement
and print out all of the RINs in the database.
The example SQL text is very simple and fits on the same line as the key name.
Real SQL will be more complex and require multiple lines.
Each line of a multi line Value must be indented at least one space.

for example:

[SQL]
SQL_STATEMENT_1 =
    -- simple example sql
    SELECT Given
    FROM NameTable
    WHERE Surname LIKE 'smith';

The SQL_STATEMENT_1  key specifies the SQL statement that will be run.
The statement may begin on the next line, as above, as long as the SQL lines
are all indented with white space. Blank lines are not allowed.
Use indented SQL comments (--) to add spacing for readability.
# style comments are not allowed within multi line values.

Note that the SQL_STATEMENT_1 key is required, while additional SQL_STATEMENTs 
are optional.

The the app will accept up to 99 SQL statements.-
   SQL_STATEMENT_1
   SQL_STATEMENT_2
   ...
   SQL_STATEMENT_99

This app will also run SQL script files. In this case, the file path is
specified, not the contents.
For example:

[SQL]
SQL_SCRIPT_1 = Maintenance-auto.sql

For this key, always place the file path on the same line as the key name,
as shown in the example.
To specify a second script file to run, add in another key name as:

SQL_SCRIPT_2 =  C:\my script folder\SecondScriptFile.sql

Up to 99 scripts can be run.

If you want none of the SQL Statements to run, just change the name of 
SQL_STATEMENT_1  to anything else, such as:
INACTIVE_SQL_STATEMENT_1 
Since the SQL_STATEMENT_1  won't be found, none of the other SQL_STATEMENTs 
will run.

Same for SQL script file keys. Renaming SQL_SCRIPT_1 will stop any scripts 
from running.


===========-
Database modification statements should usually be followed by a
SELECT changes(); statement to display how many rows were changed.


This utility will not help you write the SQL statement and is not a good
working environment in which to create your SQL statement.
Confirm you query works before running it in this utility. (Or get the SQL from
a source that has confirmed its results.)

=========-
Confirm the config file has the proper entries and that is has been saved.

=========-
Double click the "RunSQL.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands.

=========-
The terminal window is closed and the utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

=========-
IMPORTANT:
See notes below regarding SQL that refers to or updates column data collated by
the RMNOCASE collation.

=========-
Open the TEST.rmtree database in RM and confirm the desired changes have
been accomplished.

=========================================================================DIV80==
Notes

This utility automatically loads the collation sequence RMNOCASE from the 
unifuzz64.dll file.  That means that the RMNOCASE collation, used in many RM
tables is available. However, the collation sequence in unifuzz64 is not
identical to the one in the RM application.
Problems arise when accessing indexes created with one collation with SQL
using the other.

=========-
If your SQL makes any **changes** to an RMONCASE collated column, you must
run the SQL:
REINDEX RMNOCASE;
as SQL_STATEMENT_1 or at the start of your script file. 
Put your updating SQL in following statements. 
After running the SQL, run the RM "Rebuild Indexes" tool immediately after
opening the modified database in RM.
From Left hand icon panel, select the Tools icon to open the Tools listing,
then select Database Tools=>Rebuild indexes=>Run selected tool.

Queries that use but do not modify RMONCASE collated columns have two options-
1- do as above, first REINDEX RMNOCASE and then Rebuild indexes in RM
or
2 code the SQL to use the SQLite built-in NOCASE collation as an override 
to the RMNOCASE.

On the other hand...
Many users have not done this for read only queries and have not had a problem. 

=========-
On some occasions, the utility terminal window will display a "Database
Locked" message. In that case: Close the terminal window, Close RM and re-run
the utility, then re-open RM.
"Database locked" is a normal message encountered with SQLite.


=========================================================================DIV80==
Precautions before using the modified database

Once you are satisfied with the results of the modifications made by this
software, don't hurry to start using the resulting file for research.
Continue your work for several days using the original database to allow
further thought. Then run the utility again with your perfected config
file on a new copy of your now-current database. Inspect the results and then
use the modified database as your normal research file.

The week delay will give you time to think about what could go wrong. You should
consider unexpected changes to your data that you did not want.

If you start using the newly modified database immediately, you'll lose work
if you missed a problem only to find it later and have to revert to a backup
from before the database was modified.


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


=========-
Multiline Values

Probably the trickiest part of the config file is the SQL section.
The SQL_STATEMENT_1, SQL_STATEMENT_2 etc keys are multi-line values.
Each line of the value should be on a separate line indented with at least
one blank. An empty line terminates the value/statement.
generates an error.
Multi-line values may not contain # style comment lines, but they may
contain -- style SQL comments. These are just part of the value/statement.

examples-

===========-
correct format-
[SQL]
SQL_STATEMENT_1 =
   SELECT pt.PersonId
   FROM PersonTable AS pt
   INNER JOIN NameTable AS nt ON pt.PersonId = nt.OwnerId
   -- this kind of comment is OK
   WHERE nt.NameType = 5    -- married name
   AND nt.surname LIKE 'sm%'

===========-
incorrect format- (empty line not allowed)
[SQL]
SQL_STATEMENT_1 =
   SELECT pt.PersonId
   FROM PersonTable AS pt

   INNER JOIN NameTable AS nt ON pt.PersonId = nt.OwnerId
   WHERE nt.NameType = 5    -- married name
   AND nt.surname LIKE 'sm%'

===========-
incorrect format (not indented)
[SQL]
SQL_STATEMENT_1 =
SELECT pt.PersonId
FROM PersonTable AS pt
INNER JOIN NameTable AS nt ON pt.PersonId = nt.OwnerId
WHERE nt.NameType = 5    -- married name
AND nt.surname LIKE 'sm%'

===========-
incorrect format- (no # type comments allowed)
[SQL]
SQL_STATEMENT_1 =
   SELECT pt.PersonId
   # this is an non-allowed comment line
   FROM PersonTable AS pt
   INNER JOIN NameTable AS nt ON pt.PersonId = nt.OwnerId
   WHERE nt.NameType = 5    -- married name
   AND nt.surname LIKE 'sm%'

===========-
incorrect format- (empty line not allowed)
[SQL]
SQL_STATEMENT_1 =

   SELECT pt.PersonId
   FROM PersonTable AS pt
   INNER JOIN NameTable AS nt ON pt.PersonId = nt.OwnerId
   WHERE nt.NameType = 5    -- married name
   AND nt.surname LIKE 'sm%'





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
APPENDIX  unifuzz64.dll download

The SQLiteToolsforRootsMagic website has been around for many years and is run
by a trusted RM user. Many posts to public RootsMagic user forums mention use
of unifuzz64.dll from the SQLiteToolsforRootsMagic website. This author has
also used it for years.

direct download:
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

the link above is found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/


MD5 hash values are used to confirm the identity and integrity of files.

    MD5 hash                            File size         File name
    06a1f485b0fae62caa80850a8c7fd7c2    256,406 bytes    unifuzz64.dll

In Windows, to generate the MD5 hash of a file named [file name]:
Open a terminal window and enter:
certutil -hashfile [file name]  MD5

where [file name] is the fie you wish to compute the MD5 has for.

So, to verify the unifuzz file-
certutil -hashfile unifuzz64.dll  MD5


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

*  Consider adding execution of SQL scripts.
*  Consider fancier formatting of output.
*  Add ability to add additional database extensions besides RMNOCASE.
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
