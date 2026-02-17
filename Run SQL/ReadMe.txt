=========================================================================DIV80==
Run SQL commands on a RootsMagic database
RunSQL.py


Utility application for use with RootsMagic databases

RootsMagic (RM) software (https://RootsMagic.com) uses a SQLite relational
database (https://sqlite.org) as its data storage file.

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
computer. "Installing python" is described in the appendix below for Windows
computers. MacOS computers already have it installed.

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

Tested with a RootsMagic v 11.0.4 database
using Python for Windows v3.14   64bit

The python script file has not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3.n installed.

=========================================================================DIV80==
General Overview

This program is what is called a "command line utility". It is in the form of a
single text file with a "py" file name extension ("MainScriptFile.py") along
with the package "RMpy" which is a folder included in the distribution zip file. 
The MainScriptFile relies on code in the RMpy folder.
These utilities are not installed in the traditional Windows sense, they are
simply copied to the computer.

The utilities are configured by editing a configuration file. This
configuration tells the utility which database to use and how to display the output.
(Some of the utilities use the command terminal to interact with the user.)
The default name of the configuration file (called, hereinafter, the
"config file") is "RM-Python-config.ini". It should be located in the same
folder as the MainScriptFile.py file and the RMpy folder.

To install and use the utility for the first time (specifics below):

*  Install Python for Windows x64.

*  Create a new folder on your computer, the "working folder".

*  Make a copy of your database, move the copy into the working folder.

*  Copy the required files from the downloaded zip file to the working folder.

*  Edit the config file in the working folder to tell the utility what to
   do and where to do it.

*  Double click the MainScriptFile.py file to run the utility.

*  A window (terminal window) with a black background and white text will appear.
Some utilities will keep this window open and request data, other utilities will
only show the window while the command is processing.

*  The terminal window will close and a summary report will be displayed
in NotePad.

The above procedure of making a copy of your database and operating on it in
the working folder is most prudent when a user is just getting familiar with
a new or updated utility.

Some utilities are read only and do not change the database at all, while others
affect only small amount of data.
Once the user has confidence in the operation of a low-impact utility, one
can start operating directly on the research (production) database, always
assuming that at least several known-good backups exist.

Other utilities that require more configuration and make larger changes should
always operate on databases copied into a working folder.

*****  Details follow below. *****

=========================================================================DIV80==
Running the utility - step by step

The steps listed here run the utility on a copy of your database created in a
new directory location. Always run this utility on a copy as shown here. It
is likely that several attempts will be needed to obtain satisfactory results.

==========-
Install Python for Windows x64  -see "APPENDIX  Python install" below.

==========-
Create a folder on your computer that you will not confuse with other
folders. It will be referred to as the "working folder".

You may want to create it within your home folder. Your home folder is
"C:\Users\me", where "me" is your user name. This is a safe location that will
not be taken over by OneDrive.

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

For example, in the sample config file, there is a section named [FILE_PATHS].
In that section, reside several key-value pairs, one of which is 
DB_PATH = TEST.rmtree

"DB_PATH" is the key, "TEST.rmtree" is the value. key-value pairs are separated
with an equals sign character.

The utility needs to know where the RM database file is located, the output
report file name and its location.

If you followed the above instructions, no changes to any of the key-values in
the [FILE_PATHS] section are needed.


The utility also needs to know where the unifuzz64.dll file is.  Its path
is give an the value of the key RMNOCASE.

Save the config file but leave it open in Notepad.
You will now be editing additional settings.

=========-
Enter your SQL statement into the config file using key-value pairs in the
[SQL] section of the file.

The utility will run up to 99 SQL statements. They are written in the config
file as, for example:

[SQL]
SQL_STATEMENT_1 = SELECT PersonID FROM PersonTable;


This section "SQL" has one key: "SQL_STATEMENT_1" which has the
value "SELECT PersonID FROM PersonTable;".

This example, if run with the utility, will run the very simple SQL statement
and print out all of the RINs in the database.
The example SQL text is very simple and fits on the same line as the key name.
Real SQL will be more complex and require multiple lines for human readability.

Each line of a multi line Value must be indented at least one space.
For example:

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
a source that has verified its results.)

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

This utility optionally loads the collation sequence RMNOCASE from the 
unifuzz64.dll file.  That means that the RMNOCASE collation, used in many RM
tables is available if the RMNOCASE key is set to the location of unifuzz64.dd.
However, the collation sequence in unifuzz64 is not identical to the one in the
RM application. Problems arise when accessing indexes created with one
collation with SQL using the other.

=========-
If your SQL makes any **changes** to an RMONCASE collated column, you must
run the SQL:
REINDEX RMNOCASE;
as SQL_STATEMENT_1 or at the start of your script file.
Put your updating SQL in following statements.

RootsMagic must be closed when the SQL is run.

After running the SQL, run the RM "Rebuild Indexes" tool immediately after
opening the modified database in RM.
From Left hand icon panel, select the Tools icon to open the Tools listing,
then select Database Tools=>Rebuild indexes=>Run selected tool.

Queries that use but do not modify RMONCASE collated columns have two options-
1- do as above, first REINDEX RMNOCASE and then Rebuild indexes in RM
or
2 code the SQL to use the SQLite built-in NOCASE collation as an override 
to the RMNOCASE.

=========-
On some occasions, the utility terminal window will display a "Database
Locked" message. In that case: Close the terminal window, Close RM and re-run
the utility, then re-open RM.
"Database locked" is a normal message encountered with SQLite.

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
APPENDIX  Config file: location, contents and editing

Name and location
The utility requires a configuration file. A file named "RM-Python-config.ini"
will be recognized as the utility's configuration file when placed in the same
directory as the MainScriptFile py file for the utility. Each utility is
distributed with a sample config file to get you started.

"MainScriptFile.py" refers to the py file having the name of the utility you
are running, for example, TestExternalFiles.py, ChangeSourceTemplate.py etc

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "MainScriptFile.py" is executed from a terminal window
which has the folder "C:\Users\me\TestFolder" as its 'current directory', it
will use the configuration file "C:\Users\me\TestFolder\RM-Python-config.ini"
if it exists. If the utility is run with an explicit argument, such as:
MainScriptFile.py "C:\Users\me\Documents\RM-Python-config.ini"
then the specified ini configuration file will be used instead.

Note also that the file name is not restricted to the default.
For instance, running the utility from a terminal window as:
MainScriptFile.py config_mine.ini
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
The config file uses the standard ini file format. The config file is made up
of the elements: Sections, Keys, Values and Comments.

A name in square brackets is a section name that identifies the start
of a section. A section continues until a new section starts. The order of
sections is a config file is not important, but all of the sample config files
start with the [FILE_PATHS] section.

A section contains one or more key-value pairs and comment lines. Every key
should be in a named section.

A name on the left side of a "=" sign is a key.
Text on the right side of a "=" is the value assigned to the key on the left.
Comment lines start with a "#" character and are only included to help
the human user read and understand the file. They are ignored by the utility
software. Comments may appear most anywhere in the config file.

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
generated but not displayed.

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

Install Python from either:
from the Microsoft Store (preferred)
or
from the Python.org web site

From Microsoft Store
From the Windows Start menu, open the Microsoft Store app.
In the search field at the top of the Store home page, 
enter "Python Install Manager".
You should then see the Python Install Manager / Python Software Foundation page.
Click the "Get" button and follow the instructions.


Python.org web site download and install
https://www.python.org/downloads/

Click on the button near the top of page: "Download Python install manager"
Click it and save the installer.
Go to the download location and run the installer using the default options.

Note: by default, the Python installer places the software in the user's
home folder in the standard location.

A Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard Windows method found in
Windows=>Settings=>Installed apps

=========================================================================DIV80==
APPENDIX  unifuzz64.dll download

The SQLiteToolsforRootsMagic website has been around for many years and is run
by a trusted RM user. Many posts to public RootsMagic user forums mention use
of unifuzz64.dll from the SQLiteToolsforRootsMagic website. The author has
also used it for years and can vouch for its safety.

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

So, for example, to display the MD5 of the unifuzz file, enter-
certutil -hashfile unifuzz64.dll  MD5

The path to the unifuzz64.dll file in the config file is given by the
RMNOCASE key. Same rules as for the DB_PATH key.

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
TODO

*  Consider adding execution of SQL scripts.
*  Consider fancier formatting of output.
*  Add ability to add additional database extensions besides RMNOCASE.
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

=========================================================================DIV80==
