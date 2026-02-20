# SQL for creating Groups in RootsMagic

## Format

These SQL files are all suitable for pasting into a config
file and then being run with the GroupFromSQL utility.
These files are also in the Misc SQL folder, elsewhere in this distribution.

Most have the lines-
--[REL: cousin+spouses]
--SQL_QUERY =

which are required for use n the config file.

Remove the first 2 dash characters in those lines after pasting into the 
config file to conform to the ini file format.

The name within the square brackets is a suggested group name that must be
created in RootsMagic.

## Configuration
Many of these SQL statements need configuration parameters to be set for
your needs.

For example, the "List of cousins" file starts off with-
--[REL: cousin]
--SQL_QUERY =
  -- Configure 2 parameters in the lines immediately following
  WITH RECURSIVE
  Constants AS ( SELECT
     2361   AS C_StartPerson,     -- The RIN of the root person
        1   AS C_BirthParentOnly  -- 1 or 0, 1 means only birth parents included
    ),

That file contains 2 parameters that need to be set.
the two values are set in the file as 2361 and 1. 
Be careful when changing them, whitespace does not matter.


## The SQL Files

### List of ancestors.sql
All  ancestors

### List of cousins.sql
All cousins and ancestors, same as all ancestors and all descendants of
those ancestors.

### List of cousins with spouses.sql
As above, but includes each person's spouse (or spouses?)

### List of cousins with spouses and spouse parents.sql
As above, but includes each person's and each person's spouse's parents.

### People in a group with no person or fact sources.sql
Finds people who need source work.

### People who died before age 10.sql
Similar to what can be done by RM Advanced Search, but this takes the date
information from the events/facts while I believe advanced search use the
denormalized dates in the name column. The name column dates have only the date
and drop the modifiers like before, after etc.

### People who have immigrated.sql
Lists Immigration Facts ...TODO

### People with a shared fact with role.sql

### People with missing census fact.sql
Can be used to guide research in suggesting people who are missing a fact or
shared fact for a particular census year. Configure the census year, the date
of birth and birth location. TODO

### People with more than single birth-death fact.sql
To guide research..

