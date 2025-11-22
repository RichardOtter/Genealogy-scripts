Documentation for the RMpy python package

This is distributed only with releases of the genealogy scripts, not
on a public package server

Used for common code used by the genealogy scripts

This doc is for internal use only.

Components-

__init_py
common.py
gitignore.py
launcher.py
RMDate.py



===========================================DIV50==
__init_py
presence indicate that this folder is a package/
Contains the package version number



===========================================DIV50==
common.py
some commonly use functions
currently-
create_db_connection
get_SQLite_library_version
time_stamp_now
reindex_RMNOCASE
q_str
pause_with_message
get_current_directory
RM_Py_Exception


===========================================DIV50==
gitignore.py
implements an file ignore feature similar to that used by git
Used in TestExternalFiles app

===========================================DIV50==
launcher.py
Used by all of my genealogy scripts.
Deals with the config file, finding it, parsing it,
some error checking.

===========================================DIV50==
RMDate.py
functions for dealing with RM dates and sort dates


===========================================DIV50==
