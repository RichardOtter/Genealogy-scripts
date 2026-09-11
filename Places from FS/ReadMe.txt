
The RM UI shows name and normalized name
plus the other fields and note

Currently, the py script makes changes only to the AuxPlaceTable

after an update of the aux table, can run the apply tom place table script
which first stores all data from place table into aux and then applies FS data from aux
table to the place table

from rm UI, one could update/add the name field or better, the normalized name.

perhaps the script could format the name from the normalized name, using rules
It could create a yaml file for the note to keep the data structured.




Categories of place names

german
has ~|
has a ~
has [] text for placeholder level
has ?
has _skip in note
has County
has double lowest level (_GEMEINDE-ISSUE)



final auxplaetable should have
orig name  (fail safe)
returned fs name in english
retruned fs name in german
RJO modified name (has [] text for place holder ?)

parent id


Strategy
create the new AuxPlaceTable
along with any needed lookup tables.

Run the sql to populate it with the orig data in PlaceTable
update the FSPID from the Orig_Note
run sql to update the Uncertain column (if the orig name has a ~ or a ?)
Uncertain=_PROBABLY  if name has ~
         =_UNCLEAR   if name has ?
         =_REGION    if name has region
         =_VICINITY  if name has vicinity
--how about place holder text [IC] etc
run sql to update the Language column: en or de
run SQL to update NonFSPlace if currently has _SKIP


===========================================DIV50==
CREATE TABLE IF NOT EXISTS AuxPlaceTable (
    PlaceID INTEGER PRIMARY KEY,

    Language TEXT,
    Uncertain TEXT,
    FSPDesID INTEGER,
    FSPID INTEGER,
    NonFSPlace TEXT,
    FS_NameFull_en TEXT,
    FS_NameShort_en TEXT,
    FS_NameFull_de TEXT,
    FS_NameShort_de TEXT,
    FS_Abbrev TEXT,
    FS_Latitude INTEGER,
    FS_Longitude INTEGER,
    FS_YearStart INTEGER,
    FS_YearEnd INTEGER,
    FS_PlaceType TEXT,
    FS_PlaceStatus TEXT,
    FS_ParentID TEXT,
    FSMatchScore INTEGER,
    FS_LastUpdated FLOAT,
    FS_Status TEXT,
    FS_Error TEXT,

The "Orig_" fields are exactly related to the fields in the RM PlaceTable

Language TEXT,
    en or de  the languages are separate this shows which oto use for PlaceTable.Name
Uncertain TEXT,
     flag if name has ~/_PROBABLY, ?/_UNCLEAR, _REGION, or _VICINITY
FSPDesID INTEGER,
     FS Place description ID  (The ID on web page)
FSPID INTEGER,
     FS Place ID     (the placeID obtained from api)
NonFSPlace TEXT,
     flag if name has county/_COUNTY, ....
FS_NameFull TEXT,
     includes jurisdiction hierarchy
FS_NameShort TEXT,
    just the name of this place
FS_Abbrev TEXT,
    not used now
FS_Latitude INTEGER,
FS_Longitude INTEGER,
FS_YearStart INTEGER,
FS_YearEnd INTEGER,
FS_PlaceType TEXT,
FS_PlaceStatus TEXT,
    ready, or ?
FS_ParentID TEXT,
FSMatchScore INTEGER,
    accepted lookup score x10
FS_LastUpdated FLOAT,
FS_Status TEXT,
FS_Error TEXT


===========================================DIV50==

===========================================DIV50==
EXAMPLE

Wladzell
Primary ID=3864248

current time
FSPID=9835723
Jurisdiction / parent ID: 9286763 Parent: Steinfeld



https://api.familysearch.org/platform/places/3864248
gives all the descriptions.

===========================================DIV50==
