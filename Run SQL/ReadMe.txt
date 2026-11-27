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

RM 7 and later and much earlier version of Python, say after 3.10 will
also probably work but have not been recently tested.

The python script file has also not been tested on MacOS but could probably be
modified to work on a Macintosh with Python version 3.n installed.

=========================================================================DIV80==
General Overview

This program is what is called a "command line utility". It is in the form of a
single text file with a "py" file name extension ("RunSQL.py")
along with the package "RMpy" which is a folder included in the 
distribution zip file.
The RunSQL.py file relies on code in the RMpy folder.
These utilities are not installed in the traditional Windows sense, they are
simply copied to the computer.

The utilities are told what to do by editing a configuration file. This
configuration tells the utility which database to use and how to display the
output.

The default name of the configuration file (called, hereinafter, the
"config file") is "RM-Python-config.ini". For now, it should be located in the
same folder as the MainScriptFile.py file and the RMpy folder.

How it works
Run SQL is started by the user, a terminal window is displayed,
the program processes the configuration data and the database, a report file
is displayed in Notepad, the terminal window closes and the program exits.


Getting Started     *****  Details follow immediately below. *****

To install and use the utility for the first time:

*  Install Python for Windows x64.

*  Create a new folder on your computer, the "working folder" to contain
   a copy of your database, the program files and the config file.

*  Edit the config file in the working folder to tell the utility what to
   do and how to do it.

*  Double click the RunSQL.py file to run the utility.

*  A terminal window with a black background and white text will appear.

*  The terminal window will close and a summary report will be displayed
   in Notepad.

=========================================================================DIV80==
Running the utility - detailed step by step

The steps listed here run the utility on a copy of your database created in a
new directory location. Always run this utility on a copy as shown here. It
is likely that several attempts will be needed to obtain satisfactory results.

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
     (file)     RunSQL.py
     (file)     RM-Python-config.ini
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
     (file)     RunSQL.py
     (file)     RM-Python-config.ini
     (file)     RMNOCASE_surrogate.dll
     (file)     regexp.dll
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

Name and folder location
The utility requires a configuration file. A file named "RM-Python-config.ini"
will be recognized as the utility's configuration file when placed in the same
directory as the RunSQL.py file. Each utility is distributed with
a sample config file to get you started.

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "RunSQL.py" is executed from a terminal
window which has the folder "C:\Users\me\TestFolder" as its 'current directory',
it will use the configuration file "C:\Users\me\TestFolder\RM-Python-config.ini"
if it exists. If the utility is run with an explicit argument, such as:
RunSQL.py "C:\Users\me\Documents\RM-Python-config.ini" then the
specified ini configuration file will be used instead.

Note also that the file name is not restricted to the default.
For instance, running the utility from a terminal window as:
RunSQL.py config_mine.ini
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

Text Encoding
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an umlauted ä in the first line comment to
force it to be in the correct format.
Text encoding can be found in the file format option in the "Save file" dialog
box in NotePad.

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
APPENDIX  RMNOCASE_surrogate.dll and unifuzz64.dll

The path to the dll file in the config file is given by the RMNOCASE key.

=======================DIV30==
There are two recommended sources for the dll that can provide the needed
RMNOCASE SQLite collation.

https://github.com/RichardOtter/RMNOCASE_surrogate/releases/latest
and
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

The dll from Github.com and included in this distribution is named
RMNOCASE_surrogate.dll I recently created it with the help of Copilot AI with
the goal of matching the functionality of RMNOCASE. No one outside of RootsMagic
Inc knows exactly how their RMNOCASE works, but anyone can test what it does and
make a matching function. For Unicode character sorting, there are about 150,000
characters. The process used to create RMNOCASE_surrogate used about 100,000
different characters.  These were not random, but selected as most probable in
name type data (Egyptian hieroglyphs were not included).

The other dll is named unifuzz64.dll and available at the
SQLiteToolsforRootsMagic website. It has been used for many years, but often
with an annoying handicap. It just asked Windows to compare the characters. That
would be fine, but it is not what RMNOCASE does.

The problem with using unifuzz64.dll is that often, when making large numbers of
database updates to fields that have name type data, the database needs to be
reindexed when it is first opened in RootsMagic. This is easy, but adds an extra
step that may be forgotten. (Even if it is forgotten, I have not seen any damage
occur. What happens is that RM pops up a frightening dialog saying that the
database is corrupted. The solution is to close RM, reopen the same database
file, and then immediately run the database tool "Rebuild indexes" In my
experience, this has always fixed the problem.) This temporary corruption
happens because the collation defined in RMNOCASE, used inside RootsMagic and
the collation in unifuzz64.dll are not the same in ways that are often
triggered. This probably has to do with the kind of data in your name fields. I
have several languages in my database so maybe that is why unifuzz64 fails to
match RMNOCASE so often in my hands.

Using RMNOCASE_surrogate.dll however, has not required reindexing. This is
confirmed by running the Integrity check tool after opening an updated database.

Again, RMNOCASE_surrogate is not proven to be the same as RMNOCASE, but for my
data any differences have not triggered the index mis-match problem.

A conservative approach is to recommend that the RMNOCASE_PATH be set to
RMNOCASE_surrogate.dll and when the changed file is opened in RootsMagic, the
user should run the database tool "Integrity check". If there is anything listed
besides "Integrity check results: ok", then run the Rebuild indexes tool and let
me know, because I haven't seen that happen yet.

Another advantage to the new RMNOCASE_surrogate.dll is that the full source code
is available on GitHub, it can be improved, if necessary,  licensing terms are
clear (MIT), and it is clear what it does.



The RMNOCASE_surrogate.dll
This file is in this distribution so an external source is not needed, but this
is where it lives-
https://github.com/RichardOtter/rmnocase-surrogate/releases/tag/ver-0.1.0

MD5 hash
2906df88c3771b68507ad68c6f93a35d	236,480 bytes	rmnocase_surrogate.dll


=======================DIV30==
The unifuzz64.dll
The SQLiteToolsforRootsMagic website has been around for many years and is run
by a trusted RM user. Many posts to public RootsMagic user forums mention use of
unifuzz64.dll from the SQLiteToolsforRootsMagic website. The author has also
used it for years and can vouch for its safety.

direct download:
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

the link above is found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

MD5 hash values are used to confirm the identity and integrity of files.

    MD5 hash                            File size         File name
    06a1f485b0fae62caa80850a8c7fd7c2    256,406 bytes    unifuzz64.dll

=======================DIV30==
MD5 calculation
In Windows, to generate the MD5 hash of a file named [file name]:
Open a terminal window and enter:
certutil -hashfile [file name]  MD5

where [file name] is the file you wish to compute the MD5 has for.

So, for example, to display the MD5 of the unifuzz file, enter-
certutil -hashfile unifuzz64.dll  MD5


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
or a link to the GitHub repo:
https://github.com/RichardOtter/Genealogy-scripts






================================================================================
Suite Version: 1.2.0 BETA
Utility Version: 1.2.2 BETA
Built: 2026-11-27 15:20:16
================================================================================
