RM Utilities Overview

This zip file contains the current versions of all of my released
RootsMagic utility programs.


These utilities are written in the Python programming language, currently the
most popular computer language in use. To run them, the Python language must
be installed on the computer. See the instructions labeled
"APPENDIX  Python install"
included in each of the utility's ReadMe files.

Code common to each of the utilities is contained in the Python 
package named: RMpy. This is the folder named RMpy in each of the utility
folders. The RMpy folder and its contents are exactly the same in each utility
folder. The folder has been copied to each utility folder as a convenience.

If you use multiple utilities, place the corresponding utility py files, one
copy of the RMpy folder, and a single RM-Python-config.ini file into a folder.
The various utility apps share the RM-Python-config.ini file and the RMpy folder.


Some utilities, such as TestExternalFile, GroupFromSQL, ColorFromGroup, 
ListCitationsForPersonID, CitationSortOrder and ConvertFact are most conveniently
used directly on the production database. Others, like ChangeSourceTemplate,
usually require several attempts to get the desired results due to their more
complicated setup requirements. So these should always be run on a database copy.
As mentioned in the individual ReadMe files, always run the utility on a database
copy *until* you are confident of the results and affect on the database- and even
then. make sure you have backups.

Version numbers
The collection of utilities, RM Utilities Suite, has a version number
and each of the individual utilities also has a separate version
number (displayed in the report file header.)

If a utility is updated or a new one is created, a new collection (or suite)
with a new version number will be created and released on GitHub.


