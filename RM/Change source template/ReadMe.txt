=========================================================================DIV80==
Change the source template used by given sources
ChangeSourceTemplate.py


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

This utility works with structured sources and citations defined by source
templates. "Structured" meaning having defined data fields used to create
footnotes using the sentence language, as opposed to "free form" sources.
(See below "Template specified data fields" in the Notes section, below,
for further explanation)

RM users can create their own source templates. Those users often find that an
initial source template design needs updating after using it for a time and
gaining more experience. Changes to the source template are desired, but RM does
not provide a mechanism to propagate changes made to a source template back to
sources and citations already created from it. That's where this utility comes
in.

A common use case is to add to or rename the fields of a source template that's
already in use. The work flow using this utility, involves :
* Copy the in-use source template (using the "Copy" button in the RM source
  templates list window)
* Rename and edit the Source Template copy to have the desired fields
* Uses this utility to switch the sources that used the old template to
  instead use the newly created template.

See "All possible Source Template changes" in the Notes section before
proceeding. This utility may not be needed for your modifications.

This utility does not modify any source template. It modifies sources and
citations.

This utility does not move data BETWEEN source fields and citation fields.
Other utilities can do that. (see: LumpSources another utility in this suite.)


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
folders- the "working folder".

==========-
Copy these items from the downloaded zip file to the working folder-
      ChangeSourceTemplate.py          (file)
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
STEP 0		Option    All options = off

=========-
Look at the section of the config file containing options:
[OPTIONS]
CHECK_TEMPLATE_NAMES   = off
LIST_SOURCES           = off
LIST_TEMPLATE_DETAILS  = off
CHECK_MAPPING_DETAILS  = off
MAKE_CHANGES           = off

Confirm all 5 options are set to off.

The first four options tell the utility to execute validation runs.
Only the last option, when set to "on", will make changes to your database.
Please go through the validation runs as explained below. Error checking
is not re-done when running Make_Changes.
Either 0 or 1 of the five options may be "on" at one time in a run of the utility.
Save the config file, and leave the file open in the editor.

NOTE: only the first "on" action read from the list will be performed when
the utility is run, the remaining options are ignored. So, to avoid confusion,
always check that only one option is set to on.

Save the config file but leave it open in Notepad.

=========-
Double click the "ChangeSourceTemplate.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands and then the terminal window is closed and the
utility is exited.

=========-
The report file is displayed in Notepad for you inspection.


If the database file couldn't be found, fix the config file, save it and re-run
the utility until you get it right.

If the report file did not open in NotePad, read the section "APPENDIX
Troubleshooting" below.

==========-
STEP 1		Option CHECK_TEMPLATE_NAMES = on

Now you know what to expect when running the utility and how to configure the
config file. You're ready to start, but first, you need to figure out what needs
to be accomplished and tell the utility.

Assumed scenario: There is a source template in the RM file that is not quite right. You've used
it to create sources, and, because of the template, they're not quite right either.
Check your database and determine the exact name of the not-quite-right template.

Look at the config file, still open in NotePad and find the section :

[SOURCE_TEMPLATES]
TEMPLATE_OLD    = Sample_OldTemplateName
TEMPLATE_NEW    = Sample_NewTemplateName

You need to edit the config file so that Sample_OldTemplateName is replaced with
the exact name of the not-quite-right template The easiest way is to do this is
to find the template in the Source Template List in RM, click the edit button,
and copy the name into the clipboard, then paste into the config file.

There should also be another source template, that is similar to the
not-quite-right template, but that has the changes/corrections that you want.
Find its exact name, as above, and paste the name into the config file as
the value for the key TEMPLATE_NEW.

Your config file in NotePad should now have the new names:

[SOURCE_TEMPLATES]
TEMPLATE_OLD    = not-quite-right template name
TEMPLATE_NEW    = new and improved template name

Now look back at the OPTIONS section of the config file, and change the line-
CHECK_TEMPLATE_NAMES   = off
to
CHECK_TEMPLATE_NAMES   = on

Save the config file but leave it open in Notepad.

=========-
Double click the "ChangeSourceTemplate.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands and then the terminal window is closed and the
utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

Check that there are no error messages listed in the Report file.
If a source template name couldn't be found, fix the config file, save it and
re-run the utility until you get it right.

A common issue is that template names may an embedded space, a leading or
trailing space.
See NOTES section for details on how to enclose names in quotes to fix.

==========-
STEP 2		Option LIST_SOURCES = on

Now comes the question of which sources should have their SourceTemplate 
switched. A common use case will require that all of the sources using the old
template should be switched over to use the new template. Other situations 
are also possible in which only a subset of all sources using the old template 
should be switched over to the new template.

In the config file, look for the line:
[SOURCES]
SOURCE_NAME_LIKE  = %

This line specifies the matching pattern that determines the sources to be
switched. Leave it alone for now.

RM does not make it easy to get a list of sources that use a specific template,
the next utility run will generate that list.

Look at the OPTIONS section of the config file still open in NotePad, edit these
two lines so they are as shown:
CHECK_TEMPLATE_NAMES   = off
LIST_SOURCES           = on

Save the config file but leave it open in Notepad.

=========-
Double click the "ChangeSourceTemplate.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands and then the terminal window is closed and the
utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

Check that there are no error messages listed in the Report file. You should
see a list of all sources that were created using the Old Template.
Any or all of these listed sources may be converted to the new template.

If you want to convert all of them, you can go to the next step. If only some
are to be converted, you will need to edit the line SOURCE_NAME_LIKE = % and
rerun the utility to confirm that the correct sources are listed.

Note that SOURCE_NAME_LIKE can specify an exact match or a wildcard match.
The wildcard match may use the two SQL LIKE wildcard characters "%" and "_".
Note that the search is not case sensitive and more than one wildcard character
can be used in a search. See Notes for further ideas.

(for additional help, see, for instance: https://www.sqlitetutorial.net/sqlite-like/ )

==========-
STEP 3		Option LIST_TEMPLATE_DETAILS = on

Now the utility has to be told how the old template relates to the new one.

This is done with the FIELD_MAPPING section of the config file.
Many changes can be made to source templates that do not require this
utility. See the Notes section starting with "All possible Source Template changes".

The mapping is used to specify field renaming, field addition and field deletion.

Before the mapping value is edited, it's a good idea to get a clear listing of
the fields in both the old and new templates. This can be gotten from the RM
Source Template window, but it can be shown very quickly using this utility.

Look at the OPTIONS section of the config file still open in NotePad, edit these
two lines so they are as shown:
LIST_SOURCES           = off
LIST_TEMPLATE_DETAILS  = on

Save the config file but leave it open in Notepad.

=========-
Double click the "ChangeSourceTemplate.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands and then the terminal window is closed and the
utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

(Leave the report open in Notepad. It will be used in the next step.)

Check that there are no error messages listed in the Report file.
You will see a list of all the fields in the old and new templates.

As part of the process of designing a new template that fixes an
old one, it's important to map out how field names correspond.
That is what the mapping values are for. That mapping will be
inserted into the section [FIELD_MAP] as values for the
keys MAPPING_SOURCE and MAPPING_CITATION.

These values tell the utility how to transfer the information when
switching templates.

We'll create the mapping from the information in the report file just created.

Using the built-in source template "Birth Registration, state level"
as an example-

The report files lists its fields as-

OLD TEMPLATE
source     Text     "Repository"
source     Place    "RepositoryLoc"
citation   Text     "Name"
source     Text     "Jurisdiction"
citation   Text     "Form"
citation   Text     "CertificateNo"
citation   Date     "Date"

Assume that the new template already created has some field changes.
Its field listing is-

NEW TEMPLATE
source     Text     "RepositoryName"
source     Place    "RepositoryLoc"
citation   Text     "PersonName"
source     Text     "Jurisdiction"
citation   Text     "Form"
citation   Text     "CertificateNo"
citation   Date     "Date"
citation   Text     "ID-number"

The quotation marks are optional for most names. However names with spaces,
embedded, leading or trailing, must be enclosed in double quotes as shown.

First, copy the Old Template listing into a new text file and then move the
source fields to the top and the citation fields to the bottom and add a couple
of blank lines to separate them, as they are processed separately.

======
source     Text     "Repository"
source     Place    "RepositoryLoc"
source     Text     "Jurisdiction"


citation   Text     "Name"
citation   Text     "Form"
citation   Text     "CertificateNo"
citation   Date     "Date"
======

Next copy each of the field names from the New template listing and
place them on the corresponding line to the right of the old field.

This is the key point to determining the mapping. For each field in the old
template (the source), where does its data go (the destination)?

======
source      Text   "Repository"      "RepositoryName"
source      Place  "RepositoryLoc"   "RepositoryLoc"
source      Text   "Jurisdiction"


citation    Text  "Name"             "PersonName"
citation    Text  "Form"             "Form"
citation    Text  "CertificateNo"    "CertificateNo"
citation    Date  "Date"             "Date"
citation                             "ID-number"
======

Notice that 2 fields have been renamed, a new citation field
"ID-number" has been added, and 1 source field "Jurisdiction" has been deleted.

The mapping format for renames are simple, just have the old and new names
on the same line.

Deleted fields are described by inserting the word "NULL" as the destination as
shown here:

======
source      Text   "Repository"      "RepositoryName"
source      Place  "RepositoryLoc"   "RepositoryLoc"
source      Text   "Jurisdiction"     NULL


citation    Text  "Name"             "PersonName"
citation    Text  "Form"             "Form"
citation    Text  "CertificateNo"    "CertificateNo"
citation    Date  "Date"             "Date"
citation                             "ID-number"
======

For a field that is to be created, but which will be empty because there is no
existing data, use the word NULL in the source, as shown here:

======
source      Text   "Repository"      "RepositoryName"
source      Place  "RepositoryLoc"   "RepositoryLoc"
source      Text   "Jurisdiction"     NULL


citation    Text  "Name"             "PersonName"
citation    Text  "Form"             "Form"
citation    Text  "CertificateNo"    "CertificateNo"
citation    Date  "Date"             "Date"
citation           NULL              "ID-number"
======

Check to be sure that the data types match for the source & destination.
They do not have to match, but be convinced that you want to make the change.

Next, remove the first 2 columns. They are not used in the mapping.

======
  "Repository"      "RepositoryName"
  "RepositoryLoc"   "RepositoryLoc"
  "Jurisdiction"     NULL


  "Name"             "PersonName"
  "Form"             "Form"
  "CertificateNo"    "CertificateNo"
  "Date"             "Date"
   NULL              "ID-number"
======

Add the KEY names above each category of field names and
Insert a ">" character between the columns.

======
MAPPING_SOURCE =
  "Repository"     >   "RepositoryName"
  "RepositoryLoc"  >   "RepositoryLoc"
  "Jurisdiction"   >    NULL


MAPPING_CITATION =
  "Name"           >  "PersonName"
  "Form"           >  "Form"
  "CertificateNo"  >  "CertificateNo"
  "Date"           >  "Date"
   NULL            > "ID-number"
======

The rows with the field names must be indented with at least 1 space.
All the rows in a value must have the same indentation.
The space between the columns and the ">" is flexible.
There is one or more blank lines at the end of a value (MAPPING_SOURCE and
MAPPING_CITATION) separating it from the next item.

This text will be used in the next step.

==========-
STEP 4		Option CHECK_MAPPING_DETAILS = on

Look at the OPTIONS section of the config file still open in NotePad, edit these
two lines so they are as shown:
LIST_TEMPLATE_DETAILS  = off
CHECK_MAPPING_DETAILS  = on

Look at the [FIELD_MAP] section in the config file.
Replace the sample text in the [FIELD_MAP] section with the text created above.

Save the config file but leave it open in Notepad.

=========-
Double click the "ChangeSourceTemplate.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands and then the terminal window is closed and the
utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

Check that there are no error messages listed in the Report file.
If the mapping checks out as valid, you will see the message:
No problems detected in the specified mapping.

You may get a message saying that one of the fields could not be located.
If so, make the fix in the Mapping and rerun.

If the report file did not open in NotePad, read the section "APPENDIX
Troubleshooting" below. It's likely that a formatting error has been
introduced in to the config file after pasting in the new mapping text.

If everything checks out, you're ready to make the changes.

==========-
STEP 5		Option MAKE_CHANGES = on

Look at the OPTIONS section of the config file still open in NotePad, edit these
two lines so they are as shown:
CHECK_MAPPING_DETAILS  = off
MAKE_CHANGES  = on

Save the config file but leave it open in Notepad.

=========-
Double click the "ChangeSourceTemplate.py" file in the working folder
to start the utility.

=========-
A terminal window is momentarily displayed while the utility processes
the commands and then the terminal window is closed and the
utility is exited.

=========-
The report file is displayed in Notepad for you inspection.

Check that there are no error messages listed in the Report file.


If you see a message- Tried to create duplicate Name in XML, read the
section "APPENDIX  Troubleshooting" below.

=========-
Open the TEST.rmtree database in RM and confirm the desired changes have
been accomplished.

=========-
Consider whether to rename TEST.rmtree and use it as your research database.


=========================================================================DIV80==
Notes

===========-
Template specified data fields
Both sources and citations are each displayed in RM in 2 separate panels.
In RM, open the source tab to see the listing of all sources.
Click on one to select it.
On the right had side, see the panel labeled Edit Source. There are two
sub panels below it labeled "Master Source- xxxxxxx" and
"Master Source text, media etc." The top box, has a table with rows labeled
"Source Type", "Source Name" and others.
The "others" are the data fields defined for this particular source and they
are specified by the Source Template.
Open one of the source's citations (click on the ">" button to the right of
a source name in the left hand listing).
The right hand side now displays a panel labeled "Edit Citation".
The 3rd sub-panel header is labeled "Citation Details" and the 4th is 
"Citation Detail text, media etc."
The rows of the "Citation Details" table are "Citation Name" and others.
As above, the "others" are the data fields defined for this particular citation
and they are specified by the Source Template.


===========-
All possible Source Template changes

for Source template that are already in use by Sources and its Citations.

These alterations:
*    change source template name
*    change the order of the source fields
*    change field data type
*    change display name of a field
*    change brief hint for a field
*    change long hint for a field
*    change footnote template
*    change short footnote template
*    change bibliography template

May be made at anytime. No negative consequence. The changes will be immediately
seen in all new and existing source and citations. This utility is not needed.
Converting a field type from say, "name" type to "date" would not make much
sense if the field's existing data actually has name data in it. But it can be
done at any time.


The alteration:
*    change order of citation fields

May be made at any time, but existing citations whose Citation Names were
automatically generated will not be updated with what would be the new
auto generated name using the new order of citation fields.
If this is objectionable, one could open each citation, delete the existing
citation name and let it be auto generated using the new template information.
(Possible task for a new utility app?)


The alteration:
*    change state of check-box ("This is a source detail field")

This change implies movement of data from a source to a citation
or vice versa. This could be called "Lumping" or "Splitting" source info.
Do not use this utility. (See the suite site for the LumpSources utility.)


These alterations:
*    change field name
*    add new fields
*    delete fields

Use this utility to update existing source and citations to the new template
structure.

If the utility is not used and these changes are made:
*    change field name
Data is be invisible when accessed with the new name. The old date remains, but
is hidden. (it will still be accessible by the footnote templates, but the old
field will not show during data entry/edit.)
*    add new fields
New fields will not be correctly initialized, sentence language will not see the
new field as empty when tested by <> in the sentence language.
*    delete fields
Old data not removed, but is only hidden. This is not really a problem, but
it's not tidy.

===========-
It is not strictly necessary that all of the fields in the new source template
be listed as destinations (right hand) in the mappings, however, in order to
repair sources and citations that are missing fields, that field must appear
as a destination. So, best practice is to list all the fields in the 
new template as destinations even if there is no change, as was done above.

===========-
Selecting sources to be changed

If the SOURCE_NAME_LIKE variable does not give you the set of sources you
need, you can run the utility multiple times with different values of
 SOURCE_NAME_LIKE. Once a source has been updated, it won't show up in future
lists because it now uses a new template and the list only shows sources
using the old template.

Or, one could work with just one source at a time by giving the full source name
and not including a wild card, say
SOURCE_NAME_LIKE = BIRTH Helen Sauer
The list would probably include only the one source. After that source is successfully
converted, a different source could be converted in a new  MAKE_CHANGES run.
The error checking runs can be skipped since the other parameters are already
confirmed as accurate.

Or, you may consider renaming your sources (temporarily ?) so they fit an
easy to search-for pattern.

===========-
Mapping rules processing

* The mappings are processed in the order that they are listed.

* The order that the mappings are listed does not need to correspond to
 the order they are displayed in the source template.

* Each line describes how a field in the old template will be renamed
in the new template.

* If needed, one can use a temporary name for a field to avoid creating
duplication. This is fine, but the CHECK_MAPPING_DETAILS error checking step
will flag it as a possible error. If everything else checks out OK, go on to
the next step and ignore the warning.

* Data in a source field can't be renamed so as to make it a citation
field (and vice versa)

* NULL on the left side (old source template) means that the field on right
side will be empty but correctly initialized. Must be used when adding a new
field but without moving old data to it.
In RM v10, an uninitialized data field will not behave as expected in
the footnote sentence language. This may get fixed in a later RM release.

* NULL on right side (destination) means the data on left side field will not be
used and the old field and its data are deleted.

* The exact same name on the left and right side means that the mapping will
have no effect.

* If you want to switch names of fields that already exist, be careful
not create a duplicate field while in an intermediate mapping step.
The app will prevent this but it will stop the run and a new copy of the
database should be used after that.
One could create an intermediate temporary name and then change that to
the desired name in a later mapping.

===========-
Source Template Names and Field Names

For better or for worse source names, source template names, template field names
in RM are not required to be unique and can start with, end with or contain
space characters.

If you specify a name in the config file that is not unique, the report file
will show the problem. Simply rename the item in the database to make the name unique.
If you have duplicate field names that are of the same type (source vs
citation), I don't know what to say. You will find odd behavior. Good luck.

If the template name, field name or SOURCE_NAME_LIKE variable contains a
space character at the start or the end it will generally be invisible when
displayed. In any case you can quotation marks e.g. "Name ", or " Name" or "My Name".

===========-
Running the utility with MAKE_CHANGES = off does not make any changes to your
database. You can run it as many times as you need.

===========-
The utility fixes sources and citations that have missing XML field elements.
This happens when sources or citations have been created with a older template,
before a field was added.
Just be sure to list all fields in the mapping.

Symptom-
Say a template T1, has 2 fields, F1 and F2
Some sources S1 and S2 are created using template T1.

Now the template T1 is changed by editing it to add a field, F3.
The T1 template also has its footnote sentence adjusted to use the new field F3.
The edited template T1 is now called T1'.

Now some more sources, S3 and S4 are created using template T1'.
The user entered text for field F3 in S3, but left field F3 blank in S4.

Looking at the footnotes displayed in RM that are generated from T1',
one sees that source S3 and S4 look as expected. The F3 in S3 shows the text that
was entered for F3, and in S4, the F3 prints as blank.

However the footnotes from S1 and S2 are unexpected.
Those sources do not have data in field F3. In fact, they don't even have a
field F3. Any reference to F3 in the footnote sentence, by "[F3]" will,
in the footnote, print out as "[F3]" not as "" as expected.

To fix, this utility can add the empty field F3 to the existing source S1 and S2.

This can be accomplished by copying the Template T1' to T1'-copy.
The T1'-copy can have changes like better names, or no changes at all.
Just map all of the fields to themselves and run the utility.
Each source and citation will be checked for missing fields and fixed if necessary.

===========-
This may or may not be helpful...

To help understand how the system works- think of each source and citation
record as having a set of Key-Value pairs. These are the fields.
The source fields are in the source record and citation fields are in the citation record.
When you enter a source/citation that uses a template, RM displays the key names
and the user adds the values.
When a footnote needs to be created, RM uses the template to construct it from
the Key-Value pairs.
This app operates on source and citation records. It can-
Rename a Key
Delete a Key-Value pair
Add a new, Key-Value pair with a particular Key and an empty value.-


=========================================================================DIV80==
Precautions before using the modified database

Once you are satisfied with the results of the modifications made by this
software, don't hurry to start using the resulting file for research.
Continue your work for several days using the original database to allow
further thought. Then run the utility again with your perfected config
file on a new copy of your now-current database. Inspect the results and then
use the modified database as your normal research file.

The week delay will give you time to think about what could go wrong. You should
consider unexpected changes to your data that you did not expect.

If you start using the newly modified database immediately, you'll lose work
if you missed a problem only to find it later and have to revert to a backup
from before the database was modified.


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

KEY_NAME = Name1

KEY_NAME =
  Name1

KEY_NAME = Name1
  Name2
  Name3

KEY_NAME =
  Name1
  Name2
  Name3

incorrect format- (empty line not allowed)

KEY_NAME =
  Name1

  Name2
  Name3

incorrect format (not indented)

KEY_NAME =
Name1
Name2
Name3

incorrect format (not indented)

KEY_NAME = Name1
Name2
Name3

incorrect format (comment lines not allowed within a multi line value)

KEY_NAME =
  Name1
 #  Name2
  Name3

MAPPING_ value format

Values that this utility names "MAPPING_" have additional format requirements.

Each line must have 2 names- old field name and new field name, separated by
a ">" character. 
The word "NULL" may substitute for either old or new field name.

Names may be enclosed in double quotes.  Quotes are required when a name
contains a blank or ">" character at the beginning, end, or anywhere within it.

The white space between the names and ">" character is ignored.


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


===========-
Error Message:
Tried to create duplicate Name in XML.

This message will be shown when the first source is processed. It is generated
before any database change is made.

This problem can usually be avoided by reordering the lines in the mapping.

Example:
BAD
CITATION_MAPPING =
  Field_1     >     Field_2
  Field_2     >     Field_1

In this case, existing field 1 is attempted to be renamed to field 2. However,
there is already an existing field 2. That is not allowed and will stop
processing and generate the error message.

This can be avoided by using a temporary field, say "temp"

GOOD
CITATION_MAPPING =
  Field_1     >     temp
  Field_2     >     Field_1
  temp        >     Field_2
  temp        >     NULL


=========================================================================DIV80==
Developer Notes
(not needed to use utility)

The XML fields in the source and citation record are just a collection of
FieldName-Value pairs.
The order of these pairs in the XML is not significant.
The Template determines the order of the values in the display panel and in
the default citation name.
There is no point to reordering the data in the source and citation XML.

the three tables having  XML type data-
SourceTemplateTable      FieldDefs
SourceTable              Fields
CitationTable            Fields

===========-
XML tag info
SourceTemplate XML has Field Name, Display Name, Type, Hint, LongHint, and boolean for
field is in source or citation. Sources and Citations have XML that contain only
Field Name/Field Value pairs.

===========-
details of the XML format has changed format from v7 to v8

Old style XML  (possibly only remains in built-in SourceTemplate records ?)
...<?xml version="1.0" encoding="UTF-8"?>x0A<root> text </root>c0A
NOTE- when copying from SQLite expert BLOB editor, the leading 3 BOM bytes and
line feed 0A byes are copied as periods.

New style
<root> text </root>
No characters outside of root element. (no XML processing statement, no BOM,
no line feed chars. Much cleaner.

This app-
  Ignores the extraneous info and looks only at the root element.
  Modifies XML in Source and citation records only.
  Can rename a field, can add an empty field, can delete a field.

===========-
Odd cases of XML format found in my database:

Found an odd Fields value in CitationTable.
One Citation had just <root />
Fixed by adding a Fields empty element within Root, then continuing.

To do text search for start of root element, can't look for <Root> because at
least one entry had an empty Root element encoded by: <Root />
So look for "<Root"

===========-
LIKE (extract from SQLite doc- https://www.sqlite.org/lang_expr.html )

The LIKE operator does a pattern matching comparison. The operand to the right
of the LIKE operator contains the pattern and the left hand operand contains the
string to match against the pattern. A percent symbol ("%") in the LIKE pattern
matches any sequence of zero or more characters in the string. An
underscore ("_") in the LIKE pattern matches any single character in the string.
Any other character matches itself or its lower/upper case equivalent
(i.e. case-insensitive matching). Important Note: SQLite only understands
upper/lower case for ASCII characters by default. The LIKE operator is case
sensitive by default for unicode characters that are beyond the ASCII range.
For example, the expression 'a' LIKE 'A' is TRUE but 'æ' LIKE 'Æ' is FALSE.
The ICU extension to SQLite includes an enhanced version of the LIKE operator
that does case folding across all unicode characters.

If the optional ESCAPE clause is present, then the expression following the
ESCAPE keyword must evaluate to a string consisting of a single character.
This character may be used in the LIKE pattern to include literal percent or
underscore characters. The escape character followed by a percent symbol (%),
underscore (_), or a second instance of the escape character itself matches a
literal percent symbol, underscore, or a single escape character, respectively.


=========================================================================DIV80==
TODO

*  consider allowing text to be used in the left side of a mapping instead of
   existing text in an existing field.
*  allow the text mentioned above to come from a parsing of the note fields
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
