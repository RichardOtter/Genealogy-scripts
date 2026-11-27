=========================================================================DIV80==
Update Citation Names in selected citations using standard or custom templates
CitationNameUpdater.py


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

This utility is designed to update a citation's "citation name" in a bulk
operation.
A set of filters may be specified and applied to limit which
citations are to be modified, then rules are followed to determine the new
citation name for each citation.
If the results look satisfactory, the utility is then instructed to actually
save the changes to the database in another run of the software.

This utility will work with versions 8 and later of RootsMagic database.
It is aware of the new option in RM v12 that allows users to create their own
custom citation name template in the source template edit window.

=========================================================================DIV80==
Backups

IMPORTANT
This utility modifies the RM database file.
You should run this script on a copy of your database file (or at least
have multiple known-good backups) until you are confident that the changes made
are the ones desired.

Use the preview mode to be clear on what is in scope to be changed.

This utility only changes citation names. Citation names are derived from the
citation data. If the first run of the utility gives a result that is not
desired, a second run can fix it. No genealogical data can be modified or lost
running this utility.

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

The two SQLite helper files used by this utility are distributed as binary dll
files. They are both open source and can be regenerated from source by any
experienced user. Their code may also be reviewed and explained by AI.

They are both used by SQLite to provide additional functionality, they are not
run by the Python scripts directly.

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
single text file with a "py" file name extension ("CitationNameUpdater.py")
along with the package "RMpy" which is a folder included in the 
distribution zip file.
The CitationNameUpdater.py file relies on code in the RMpy folder.
These utilities are not installed in the traditional Windows sense, they are
simply copied to the computer.

The utilities are told what to do by editing a configuration file. This
configuration tells the utility which database to use and how to display the
output.

The default name of the configuration file (called, hereinafter, the
"config file") is "RM-Python-config.ini". For now, it should be located in the
same folder as the MainScriptFile.py file and the RMpy folder.

How it works
Citation Name Updater is started by the user, a terminal window is displayed,
the program processes the configuration data and the database, a report file
is displayed in Notepad, the terminal window closes and the program exits.


Getting Started     *****  Details follow immediately below. *****

To install and use the utility for the first time:

*  Install Python for Windows x64.

*  Create a new folder on your computer, the "working folder" to contain
   a copy of your database, the program files and the config file.

*  Edit the config file in the working folder to tell the utility what to
   do and how to do it.

*  Double click the CitationNameUpdater.py file to run the utility.

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
     (file)     CitationNameUpdater.py
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

The RMNOCASE_PATH and REGEXP_PATH keys, also in the [FILE_PATHS] section, point
to helper files needed by the utility to make SQLite operate as needed.

If you followed the above instructions exactly, no changes to the key-values in
the [FILE_PATHS] section are needed.

More details are in "APPENDIX  Config file: location, contents and editing".

The 2 dll helper files and described in the appendixes-
APPENDIX  RMNOCASE_surrogate.dll and unifuzz64.dll
and
APPENDIX  regexp.dll SQLite extension, source and information

==========-
The first settings specific to the Citation Name Updater are those in the
[FILTER] section.

[FILTER]
SOURCE_TEMPLATE = example source template name
SOURCE_NAME =
CITATION_NAME =
USE_REGEXP = off

These settings determine which citation names will be updated.

SOURCE_TEMPLATE
Filter 1: allows specification of a particular source template name.
If you leave it blank, as it is, then there will be no selection based on
source templates. All citations, no matter which source template was used to
create their source will be passed to the next filter.

SOURCE_NAME =
Filter 2: allows specification of a particular source name.
If you leave it blank, as it is, then there will be no selection based on
source name. All citations passed from the first filter, no matter which
source the citation is part of will be passed to the next filter.

CITATION_NAME =
Filter 3: allows specification of a particular existing citation name.
If you leave it blank, as it is, then there will be no selection based on
the existing citation name and all citations passed from the second filter,
no matter what their names, will be updated.

An example
Say that you have a source template which you have modified by adding a
citation name template to the details of the template as can be done in RM12.
New citations will use the template, but existing ones are not changed and still
use the default template. (a semicolon separated list of all citation data items
in the order they are listed in the SourceTemplate.)
Let's assume that you have created several sources using that source template.
If you want to update the citation name to reflect your new custom template
for all of the citations that use that template, set SOURCE_TEMPLATE to the
source template name. Leave SOURCE_NAME set to blank.
If you want to change only some of the sources, then set SOURCE_NAME to the
source name whose citations are to be updated.

Specifying the citation name is an option that you probably will not use
often, especially without the RegExp feature.

USE_REGEXP = off
For now, leave this off.
The setting is explained in the Notes section below.

==========-
Next up is the CITATION_NAME_UPDATER section:

[CITATION_NAME_UPDATER]
MAKE_CHANGES = off
TEMPLATE_DEFAULT = on
TEMPLATE_FROM_SOURCE_TEMPLATE = off
CUSTOM_TEMPLATE =

This section's parameters tell the utility how the new citation names will be
constructed.

MAKE_CHANGES  on / off
The first is not really a format control, but a master switch that determines
whether any changes should be made to the database.

Always leave this off for the first run.
With this set to off, no changes will be made to the database, but the report
will show exactly what your filter selections have done.

It will also list the default template for all source templates encountered.
This section of text will be very helpful when writing your own templates as it
gives the names of all the citation data fields.

TEMPLATE_DEFAULT  on / off
If on, then the default template defined by the citations name's source template
is used to update the citations selected by the FILTER section parameters.
It overrides the next two parameters, TEMPLATE_FROM_SOURCE_TEMPLATE and
CUSTOM_TEMPLATE.

If TEMPLATE_DEFAULT is off, the the other options are considered.

TEMPLATE_FROM_SOURCE_TEMPLATE  on / off
If on, then for each citation, its source template is examined. If the source
template has a RM v12 custom template defined (or at least the value in
non-blank), then it will be used for all its citations.
If the source template does not have a citation name template, then the citation
name is changed to blank.
"on" for this parameter overrides the next option.

CUSTOM_TEMPLATE may be set to a text string.
Probably only useful when using a pre-RM V12 database.
This is only considered when TEMPLATE_FROM_SOURCE_TEMPLATE is off.
Since only a single template can be specified in the config file, this
should be used only when the filtering generates a list of citations all
based on one source template.

Values in config file sections [FILTER] and [CITATION_NAME_UPDATER] may be
in quotes.

==========-
Save the config file but leave it open in Notepad.

=========-
Double click the "CitationNameUpdater.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands.

=========-
The terminal window closes and the report file is displayed in Notepad for
your inspection.

=========-
Check the report to see what the proposed citation name changes are.
Rer-run the utility after making config file changes.
When satisfied, change the config setting MAKE_CHANGES to on and run again.

=========-
IMPORTANT
After a run of CitationNameUpdater in which changes have been saved to the
database, it is important to check the file integrity of the database when
opening the file in RootsMagic. This is very easily done. Upon first loading the
database within RootsMagic, before doing anything else, click the Tools icon on
the left hand tab panel, and run the "Integrity check" database tool. It's the
third item from the top. If the result is anything besides "Integrity check
results: ok", then run the "Rebuild indexes" database tool right above it.

If Integrity check shows problems and the indexes are not rebuilt you will at
some point get a scary "database disk image is malformed" error and RootsMagic
will stop. Don't panic if that happens. Just close  (or kill) RM, reopen the
same file in RM and before doing anything else, run the Rebuild indexes tool.
This is expected behavior.
If you get a non-ok integrity check, the author would appreciate a message
describing the languages used in your database.

=========-
Examine the changed database in RM and confirm the desired changes have
been accomplished.

=========-
Consider whether to use the TEST.rmtree database as your new research database.



=========================================================================DIV80==
Notes

===========-
The utility can operate in a Preview mode in which the database is not altered.
Running the utility in this mode allows one to work on the filter options to
determine the correct set of citation names to update.

It also displays, in the report, the default citation name template for each
SourceTemplate under consideration. This default template lists all citation
data fields and is of assistance when writing your own template.

===========-
Start out with the filters set to limit the number of citation names to update
to a small, manageable number. That will allow you to inspect them and not be
overwhelmed.
Later, when you become more confident, you may consider removing the filters and
regenerating all citation names.

===========-
A list of data field names that could not be found (if any) will be printed at
the end of the report. Be sure to check it.

===========-
USE_REGEXP = on

SQLite does not provide regular expression matching by default. To be able
to use regular expression matching, one must load an extension dll.

This requires that the REGEXP_PATH be set to a SQLite extension library that
implements RegExp matching.

This utility has been tested with the free sqlean regexp extension distributed
with this software.

RegExp examples

using the SOURCE_TEMPLATE setting as an example-
If the value is set to 'string':
Any source template name that has "string" anywhere within the name will
match.

To match either of 2 strings:
(name1|name2)

Match all source templates except those that contain string1 in their name
^(?!.*string1).*$

exclude if contains string1 or string2
^(?!.*(string1|string2)).*$

exclude if contains a YYYY > 1900
^(?!.*(190[1-9]|19[1-9][0-9]|[2-9][0-9]{3})).*$

The regexp language features implemented are described in-
https://github.com/nalgeon/sqlean/blob/main/README.md

AI is a great resource to help you create regular expressions.
Just mention that you are using "sqlean regexp".


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
directory as the CitationNameUpdater.py file. Each utility is distributed with
a sample config file to get you started.

Alternatively, the configuration file name and location can be specified
on the command-line as an argument to the script. This argument overrides
the default configuration file name and location.

For example, if the script "CitationNameUpdater.py" is executed from a terminal
window which has the folder "C:\Users\me\TestFolder" as its 'current directory',
it will use the configuration file "C:\Users\me\TestFolder\RM-Python-config.ini"
if it exists. If the utility is run with an explicit argument, such as:
CitationNameUpdater.py "C:\Users\me\Documents\RM-Python-config.ini" then the
specified ini configuration file will be used instead.

Note also that the file name is not restricted to the default.
For instance, running the utility from a terminal window as:
CitationNameUpdater.py config_mine.ini
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

Text Encoding
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an umlauted ä in the first line comment to
force it to be in the correct format.
Text encoding can be found in the file format option in the "Save file" dialog
box in NotePad.

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
APPENDIX  regexp.dll SQLite extension, source and information

It has been downloaded from-
https://github.com/nalgeon/sqlean/releases/tag/0.29.0

Documentation is at-
https://github.com/nalgeon/sqlean/blob/main/README.md

MD5                               size          name
74d4fc356e55c5cd721576e68a2f6f6b	482,220 bytes	regexp.dll


=========================================================================DIV80==
TODO

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




===========================================DIV50==
===========================================DIV50==
Licenses reference

===========================================DIV50==
All .py files

MIT License

Copyright (c) 2026 Richard J Otter  <https://github.com/RichardOtter/Genealogy-scripts>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

===========================================DIV50==
RMNOCASE_surrogate.dll

MIT License

Copyright (c) 2026 Richard J Otter  <https://github.com/RichardOtter/RMNOCASE_surrogate>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

===========================================DIV50==
regexp.dll

MIT License

Copyright (c) 2021+ Anton Zhiyanov <https://github.com/nalgeon/sqlean>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

===========================================DIV50==






================================================================================
Suite Version: 1.2.0 BETA
Utility Version: 0.9 BETA
Built: 2026-11-27 15:20:16
================================================================================
