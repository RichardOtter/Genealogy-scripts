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
implements a file ignore feature similar to that used by git
Used in TestExternalFiles app

===========================================DIV50==
launcher.py
Used by all of my genealogy scripts.
Deals with the config file, finding it, parsing it,
some error checking.

===========================================DIV50==
RMDate.py
functions for dealing with RM dates and sort dates

RMDate      24 character string
RMSortDate  64 bit signed integer

functions:
now_RMDate()
now_RMSortDate()

to_RMDate(DateStr)
from_RMDate(RMDate, form)
to_RMSortDate(RMDate)
from_RMSortDate(RMSortDate : int) -> str


helpers:
get_num_from_enum
get_enum_from_symbol
get_offset_from_symbol
get_symbol_from_offset
get_str_1
get_str_2
get_enum_from_symbol
get_str
NumToMonth(MonthNum, style)



Testing status
Not supported
Quaker dates
Quarter dates

OK

now_RMDate()
now_RMSortDate()
to_RMDate(DateStr)      limited to ISO std dates
from_RMDate(RMDate, form)
to_RMSortDate(RMDate)

not working for all supported types

from_RMSortDate(RMSortDate : int) -> str


PROBLEMS

# 28                year
# 30          month            & 44
# 29      day month
# 77          month year
# 71      day month year

    (28, 	"_Std_1", 	"D.+19210000..+00000000..", 	6710926411914280972, 	"1921 || 1921 || STD no day or month"),
    (30, 	"_Std_1", 	"D.+00000100..+00000000..", 	9222844288452263948, 	"January || January || "),
    (29, 	"_Std_1", 	"D.+00000113..+00000000..", 	9222851435277844492, 	"13 January || 13 January  ||  no years"),

    (71, 	"_Std_1", 	"D.+19210113..+00000000..", 	6710968743111950348, 	"13 January 1921 || 13 January 1921||  STD"),



# 28                year
from_RMSortDate->RMDate     wrong              out_RMDate_from_SortDate='D.+19210000..+63830000..'
from_RMSortDate->std        wrong              out_std_fmt_from_DB_SortDate='19216383'
from_RMDate->std            OK
to_RMSortDate(RMDate)       OK

# 30          month
from_RMSortDate->RMDate     wrong               out_RMDate_from_SortDate='D.+63830100..+63830000..'
from_RMSortDate->std        wrong               out_std_fmt_from_DB_SortDate='January 63836383'
from_RMDate->std            OK
to_RMSortDate(RMDate)       OK

# 29      day month
from_RMSortDate->RMDate     wrong               out_RMDate_from_SortDate='D.+63830113..+63830000..'
from_RMSortDate->std        wrong               out_std_fmt_from_DB_SortDate='13 January 63836383'
from_RMDate->std            OK
to_RMSortDate(RMDate)       OK
but these came after printout
can only concatenate str (not "int") to str
can only concatenate str (not "int") to str

# 77          month year
never ran


# 71      day month year
from_RMSortDate->RMDate     wrong               out_RMDate_from_SortDate='D.+19210113..+63830000..'
from_RMSortDate->std        wrong               out_std_fmt_from_DB_SortDate='13 January 19216383'
from_RMDate->std            OK
to_RMSortDate(RMDate)       OK












in_DB_EvemtID=27
in_GUI_description='STD'
in_GUI_sort_date='January 1921'
out_RMDate_from_SortDate='D.+19210100..+63830000..'
out_std_fmt_from_DB_SortDate='January 19216383'

Compare normal format date derived from RMDate   vs. normal format as shown in RM GUI (tests from_RMDate)
   27     'January 1921'  ==  'January 1921'
Compare sort date derived from RMDate   vs. sort date from DB   (tests to_RMSortDate)
   27     '6710961596286369804'  ==  '6710961596286369804'
can only concatenate str (not "int") to str
can only concatenate str (not "int") to str
can only concatenate str (not "int") to str
can only concatenate str (not "int") to str
can only concatenate str (not "int") to str










RMSortDate is composed of
Structure
Part1
Part2
(confidence flag not used)

===========================================DIV50==
