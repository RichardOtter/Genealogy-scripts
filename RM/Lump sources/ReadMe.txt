=========================================================================DIV80==
Lump sources that were entered as split sources
LumpSources

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third part tools is a major advantage
to using RM.
This software accesses that database directly to provide functionality not found
in the RootsMagic program.


=========================================================================DIV80==
Purpose

This utility will assist users in converting a set of "split" source to a set
of "lumped" sources.
The split sources must each have just one citation. The utility moves that
citation to another pre-existing "lumped" source.

=========================================================================DIV80==
Backups

VERY IMPORTANT
This utility makes changes to the RM database file. It can change a large number
of data items in a single run depending on the settings specified.
You will likely not be satisfied with your first run of the utility and you will
want to try again, perhaps several times, each time making changes to your
configuration file. 
You must run this script on a copy of your database file and have at least
multiple known-good backups.

Read about additional considerations in the Precautions section below.


=========================================================================DIV80==
Compatibility
CONSTANT  ???
=========================================================================DIV80==
Overview
Follows pattern with word changes for app names
=========================================================================DIV80==
Python installation
CONSTANT
=========================================================================DIV80==
Config file contents and editing

=========================================================================DIV80==
Precautions before using the modified database

Once you are satisfied with the results of the modifications made by this
software, don't hurry to start use the resulting file for research.
Continue your work for a week or so using the original database to allow
further consideration. Then run the utility again with your perfected config
file on a new copy of your now-current database and then use the modified
database as your normal work file.
The week delay will give you time to think about it. If you start
using the newly modified database immediately, you'll lose work if you miss
a problem and have to revert to a backup.


=========================================================================DIV80==
Notes
=========-
=========-
=========-

=========================================================================DIV80==
=========================================================================DIV80==
=========================================================================DIV80==
Troubleshooting:

=========================================================================DIV80==
TODO

=========================================================================DIV80==
Feedback
CONSTANT
=========================================================================DIV80==
Distribution
CONSTANT
=========================================================================DIV80==
