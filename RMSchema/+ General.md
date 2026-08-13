# RM v11.0.4

NOTE
Status: mostly just changed title to say ver 11 schema.
Not much in the data has yet been changed.

Information used in common by the individual table files

If a table has a column that has the same properties as a column used in another table, the
column will be labeled _STD (standard) and described once in this file.

Lookup tables are usually in a database schema to describe the meaning column contents.
For example, the sex column in PersonTable can have a value of 0,1 or 2. What do the
numbers mean? Check the Sex lookup table.

Similarly, lookup tables used by more than one table are described here. The columns that use
 them are also labeled _STD
 Lookup values used only once are labeled_LOOKUP and are described within that tables description file.

 DDL for creating lookup tables is in the folder "missing look-up tables".

 TODO indicates work to be done.

 Controlled Vocabulary- tokens that have a specific meaning within the document. Easily search for.

## Controlled Vocabulary

| token         | meaning                                                                               |
| ------------- | ------------------------------------------------------------------------------------- |
| RM            | RootsMagic                                                                            |
| GUI           | Graphical User Interface- what is displayed by RM                                     |
| _PK           | Primary key                                                                           |
| _FK           | foreign key                                                                           |
| _PFK          | polymorphic foreign key                                                               |
| _STD    | polymorphic foreign key type (where does PFK point)                                   |
| _STD          | standard column described here                                                        |
| _TEXT-SL      | text field designed for a single line string                                          |
| _TEXT-ML      | text field designed for multiple lines of text. Uses CR LF line end for Win and MacOS |
| _RMNC         | column is used in an index collated with proprietary collation RMNOCAASE              |
| _SPECIAL-CASE | marker used to indicate that special cases of _FK exist, usually 0.                   |
| _GUI-LAB      | set to the string used to label the data in the RM GUI                                |
| _NOT-IMP      | Not Implemented. No obvious use as of current release.                                |
| ### DONE 1    | marker indicating work is completed for that file to standard level "1"               |

## Notes

Polymorphic Associations. Using this design for polymorphism-

* can't use relational database referential integrity mechanisms.

Could use-\
unique indexes to enforce IsPrimary\
Triggers to do update of de-normalized data (BDate, DDate, Reverse (place), NameMP cols

## Standard Columns  _STD

### Note   TEXT

also named:  Comments, ActualText, Results

Multi line text. Both Windows and MacOS databases use CR LF for end of line. Both use UTF-8 encoding. The RM GUI
uses a special Note Editor for these fields.

### Sentence  TEXT

also named:  Sentence1, Sentence2, Footnote, ShortFootnote, Bibliography

Generally takes one line of text in the form of a template using the RM sentence template language,
but there is no prohibition against multiple lines.
The RM GUI does not use the note editor for sentence template editing.
Both Windows and MacOS databases use CR LF for end of line. Both use UTF-8 encoding.

### Date  TEXT

see:
[RM Date format](https://github.com/ricko2001/RootsMagic_Database_Design/blob/main/RM%20Dates.md)

### SortDate BIGINT (= INTEGER)

see:
[Sort Date investigations](https://github.com/ricko2001/RootsMagic_Database_Design/blob/main/RM%20Sort%20dates.md)

### Latitude     INTEGER

### Longitude    INTEGER

values stored as a signed integer with a scale factor
for example- Oakland, CA
stored value   scale    actual
378044389   *10e-7  = 37.8044389
-1222697194* 10e-7  = -122.2697194
W and S are negative

### UTCModDate FLOAT

Modified Julian date  

See file "UTCModDate" for more info.

### XML  BLOB

named:  Fields, FieldDefs

Newly created XML field column data in RM ver v8 and later, starts with <Root> element.
Old style started with a BOM, an XML declaration statement, a LF, then <Root> and ended with a LF.

This is a SQLite BLOB field, probably for historical reasons. All new data in these fields is
standard UTF-8 text and could be in a TEXT column.

In a new v9.1.3 database, old style XML format still used for Built-in Source Templates.

## Lookup tables

### OwnerType

OwnerID is a Polymorphic Foreign Key Type, OwnerType tells where it points.

| OwnerType | Links to        | Table.row                             |
| --------- | --------------- | ------------------------------------- |
| 0         | person          | PersonTable.PersonID                  |
| 1         | family/couple   | FamilyTable.FamilyID                  |
| 2         | fact/event      | EventTable.EventID                    |
| 3         | source          | SourceTable.SourceID                  |
| 4         | citation        | CitationTable.CitationID              |
| 5         | place           | PlaceTable.PlaceID                    |
| 6         | task            | TaskTable.TaskID                      |
| 7         | name            | NameTable.NameID                      |
| 8         | 0    TODO       | ►nothing◄  _SPECIAL-CASE              |
| 14        | place detail    | PlaceTable.PlaceID                    |
| 15        | _NOT-IMP RM v>7 |                                       |
| 18        | Task Folder     |                                       |
| 19        | association     | FANTable.FanID                        |
| 20        | TODO            | TagTable.TagValue, GroupTable.GroupID |

5 & 14 both point to PlaceTable.PlaceID \
PlaceTable.PlaceType distinguishes the 3 types of places.

### Proof

| Proof | level     |
| ----- | --------- |
| 0     | ►blank◄   |
| 1     | Proven    |
| 2     | Disproven |
| 3     | Disputed  |

### IsPrimary

| IsPrimary | primary ? |
| --------- | --------- |
| 0         | No        |
| 1         | Yes       |

### IsPrivate

| IsPrivate | private? |
| --------- | -------- |
| 0         | No       |
| 1         | Yes      |

## References

<https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form>

<https://www.sqlite.org/datatype3.html>
Should RM tables be declared STRICT ?  What would happen? Are there speed or storage advantages?

<https://stackoverflow.com/questions/7337882/what-is-the-difference-between-sqlite-integer-data-types-like-int-integer-bigi>
BIGINT is just a synonym for INTEGER. It cannot be used in all statements.
It is in no way bigger than INTEGER, it doesn't reserve more space.

<https://hashrocket.com/blog/posts/modeling-polymorphic-associations-in-a-relational-database>
Modeling Polymorphic Associations in a Relational Database

## Table DDL

For full database

``` SQL
CREATE TABLE AddressLinkTable (LinkID INTEGER PRIMARY KEY, OwnerType INTEGER, AddressID INTEGER, OwnerID INTEGER, AddressNum INTEGER, Details TEXT, UTCModDate FLOAT );

CREATE TABLE AddressTable (AddressID INTEGER PRIMARY KEY, AddressType INTEGER, Name TEXT COLLATE RMNOCASE, Street1 TEXT, Street2 TEXT, City TEXT, State TEXT, Zip TEXT, Country TEXT, Phone1 TEXT, Phone2 TEXT, Fax TEXT, Email TEXT, URL TEXT, Latitude INTEGER, Longitude INTEGER, Note TEXT, UTCModDate FLOAT );

CREATE TABLE AncestryTable (LinkID INTEGER PRIMARY KEY, LinkType INTEGER, rmID INTEGER, anID TEXT, Modified INTEGER, anVersion TEXT, anDate FLOAT, Status INTEGER, UTCModDate FLOAT );

CREATE TABLE ChildTable (RecID INTEGER PRIMARY KEY, ChildID INTEGER, FamilyID INTEGER, RelFather INTEGER, RelMother INTEGER, ChildOrder INTEGER, IsPrivate INTEGER, ProofFather INTEGER, ProofMother INTEGER, Note TEXT, UTCModDate FLOAT );

CREATE TABLE CitationLinkTable (LinkID INTEGER PRIMARY KEY, CitationID INTEGER, OwnerType INTEGER, OwnerID INTEGER, SortOrder INTEGER, Quality TEXT, IsPrivate INTEGER, Flags INTEGER, UTCModDate FLOAT );

CREATE TABLE CitationTable (CitationID INTEGER PRIMARY KEY, SourceID INTEGER, Comments TEXT, ActualText TEXT, RefNumber TEXT, Footnote TEXT, ShortFootnote TEXT, Bibliography TEXT, Fields BLOB, UTCModDate FLOAT, CitationName TEXT COLLATE RMNOCASE );

CREATE TABLE ConfigTable (RecID INTEGER PRIMARY KEY, RecType INTEGER, Title TEXT, DataRec BLOB, UTCModDate FLOAT );

CREATE TABLE EventTable (EventID INTEGER PRIMARY KEY, EventType INTEGER, OwnerType INTEGER, OwnerID INTEGER, FamilyID INTEGER, PlaceID INTEGER, SiteID INTEGER, Date TEXT, SortDate BIGINT, IsPrimary INTEGER, IsPrivate INTEGER, Proof INTEGER, Status INTEGER, Sentence TEXT, Details TEXT, Note TEXT, UTCModDate FLOAT );

CREATE TABLE ExclusionTable (RecID INTEGER PRIMARY KEY, ExclusionType INTEGER, ID1 INTEGER, ID2 INTEGER, UTCModDate FLOAT );

CREATE TABLE FactTypeTable (FactTypeID INTEGER PRIMARY KEY, OwnerType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, GedcomTag TEXT, UseValue INTEGER, UseDate INTEGER, UsePlace INTEGER, Sentence TEXT, Flags INTEGER, UTCModDate FLOAT );

CREATE TABLE FamilySearchTable (LinkID INTEGER PRIMARY KEY, LinkType INTEGER, rmID INTEGER, fsID TEXT, Modified INTEGER, fsVersion TEXT, fsDate FLOAT, Status INTEGER, UTCModDate FLOAT );

CREATE TABLE FamilyTable (FamilyID INTEGER PRIMARY KEY, FatherID INTEGER, MotherID INTEGER, ChildID INTEGER, HusbOrder INTEGER, WifeOrder INTEGER, IsPrivate INTEGER, Proof INTEGER, SpouseLabel INTEGER, FatherLabel INTEGER, MotherLabel INTEGER, SpouseLabelStr TEXT, FatherLabelStr TEXT, MotherLabelStr TEXT, Note TEXT, UTCModDate FLOAT );

CREATE TABLE FANTable (FanID INTEGER PRIMARY KEY, ID1 INTEGER, ID2 INTEGER, FanTypeID INTEGER, PlaceID INTEGER, SiteID INTEGER, Date TEXT, SortDate BIGINT, Description TEXT, Note TEXT, UTCModDate FLOAT );

CREATE TABLE FANTypeTable (FANTypeID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, Role1 TEXT, Role2 TEXT, Sentence1 TEXT, Sentence2 TEXT, UTCModDate FLOAT );

CREATE TABLE GroupTable (RecID INTEGER PRIMARY KEY, GroupID INTEGER, StartID INTEGER, EndID INTEGER, UTCModDate FLOAT );

CREATE TABLE MediaLinkTable (LinkID INTEGER PRIMARY KEY, MediaID INTEGER, OwnerType INTEGER, OwnerID INTEGER, IsPrimary INTEGER, Include1 INTEGER, Include2 INTEGER, Include3 INTEGER, Include4 INTEGER, SortOrder INTEGER, RectLeft INTEGER, RectTop INTEGER, RectRight INTEGER, RectBottom INTEGER, Comments TEXT, UTCModDate FLOAT );

CREATE TABLE MultimediaTable (MediaID INTEGER PRIMARY KEY, MediaType INTEGER, MediaPath TEXT, MediaFile TEXT COLLATE RMNOCASE, URL TEXT, Thumbnail BLOB, Caption TEXT COLLATE RMNOCASE, RefNumber TEXT COLLATE RMNOCASE, Date TEXT, SortDate BIGINT, Description TEXT, UTCModDate FLOAT );

CREATE TABLE NameTable (NameID INTEGER PRIMARY KEY, OwnerID INTEGER, Surname TEXT COLLATE RMNOCASE, Given TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE, Nickname TEXT COLLATE RMNOCASE, NameType INTEGER, Date TEXT, SortDate BIGINT, IsPrimary INTEGER, IsPrivate INTEGER, Proof INTEGER, Sentence TEXT, Note TEXT, BirthYear INTEGER, DeathYear INTEGER, Display INTEGER, Language TEXT, UTCModDate FLOAT, SurnameMP TEXT, GivenMP TEXT, NicknameMP TEXT );

CREATE TABLE PayloadTable (RecID INTEGER PRIMARY KEY, RecType INTEGER, OwnerType INTEGER, OwnerID INTEGER, Title TEXT, DataRec BLOB, UTCModDate FLOAT );

CREATE TABLE PersonTable (PersonID INTEGER PRIMARY KEY, UniqueID TEXT, Sex INTEGER, ParentID INTEGER, SpouseID INTEGER, Color INTEGER, Color1 INTEGER, Color2 INTEGER, Color3 INTEGER, Color4 INTEGER, Color5 INTEGER, Color6 INTEGER, Color7 INTEGER, Color8 INTEGER, Color9 INTEGER, Relate1 INTEGER, Relate2 INTEGER, Flags INTEGER, Living INTEGER, IsPrivate INTEGER, Proof INTEGER, Bookmark INTEGER, Note TEXT, UTCModDate FLOAT );

CREATE TABLE PlaceTable (PlaceID INTEGER PRIMARY KEY, PlaceType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, Normalized TEXT, Latitude INTEGER, Longitude INTEGER, LatLongExact INTEGER, MasterID INTEGER, Note TEXT, Reverse TEXT COLLATE RMNOCASE, fsID INTEGER, anID INTEGER, UTCModDate FLOAT );

CREATE TABLE RoleTable (RoleID INTEGER PRIMARY KEY, RoleName TEXT COLLATE RMNOCASE, EventType INTEGER, RoleType INTEGER, Sentence TEXT, UTCModDate FLOAT );

CREATE TABLE SourceTable (SourceID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, RefNumber TEXT, ActualText TEXT, Comments TEXT, IsPrivate INTEGER, TemplateID INTEGER, Fields BLOB, UTCModDate FLOAT );

CREATE TABLE SourceTemplateTable (TemplateID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, Description TEXT, Favorite INTEGER, Category TEXT, Footnote TEXT, ShortFootnote TEXT, Bibliography TEXT, FieldDefs BLOB, UTCModDate FLOAT );

CREATE TABLE TagTable (TagID INTEGER PRIMARY KEY, TagType INTEGER, TagValue INTEGER, TagName TEXT COLLATE RMNOCASE, Description TEXT, UTCModDate FLOAT );

CREATE TABLE TaskLinkTable (LinkID INTEGER PRIMARY KEY, TaskID INTEGER, OwnerType INTEGER, OwnerID INTEGER, UTCModDate FLOAT );

CREATE TABLE TaskTable (TaskID INTEGER PRIMARY KEY, TaskType INTEGER, RefNumber TEXT, Name TEXT COLLATE RMNOCASE, Status INTEGER, Priority INTEGER, Date1 TEXT, Date2 TEXT, Date3 TEXT, SortDate1 BIGINT, SortDate2 BIGINT, SortDate3 BITINT, Filename TEXT, Details TEXT, Results TEXT, UTCModDate FLOAT, Exclude INTEGER );

CREATE TABLE URLTable (LinkID INTEGER PRIMARY KEY, OwnerType INTEGER, OwnerID INTEGER, LinkType INTEGER, Name TEXT, URL TEXT, Note TEXT, UTCModDate FLOAT );

CREATE TABLE WitnessTable (WitnessID INTEGER PRIMARY KEY, EventID INTEGER, PersonID INTEGER, WitnessOrder INTEGER, Role INTEGER, Sentence TEXT, Note TEXT, Given TEXT COLLATE RMNOCASE, Surname TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE, UTCModDate FLOAT );

CREATE INDEX idxAddressName ON AddressTable (Name);

CREATE INDEX idxChildFamilyID ON ChildTable (FamilyID);

CREATE INDEX idxChildID ON ChildTable (ChildID);

CREATE INDEX idxChildOrder ON ChildTable (ChildOrder);

CREATE INDEX idxCitationLinkOwnerID ON CitationLinkTable (OwnerID);

CREATE INDEX idxCitationName ON CitationTable (CitationName);

CREATE INDEX idxCitationSourceID ON CitationTable (SourceID);

CREATE UNIQUE INDEX idxExclusionIndex ON ExclusionTable (ExclusionType, ID1, ID2);

CREATE INDEX idxFactTypeAbbrev ON FactTypeTable (Abbrev);

CREATE INDEX idxFactTypeGedcomTag ON FactTypeTable (GedcomTag);

CREATE INDEX idxFactTypeName ON FactTypeTable (Name);

CREATE INDEX idxFamilyFatherID ON FamilyTable (FatherID);

CREATE INDEX idxFamilyMotherID ON FamilyTable (MotherID);

CREATE INDEX idxFanId1 ON FANTable (ID1);

CREATE INDEX idxFanId2 ON FANTable (ID2);

CREATE INDEX idxFANTypeName ON FANTypeTable (Name);

CREATE INDEX idxGiven ON NameTable (Given);

CREATE INDEX idxGivenMP ON NameTable (GivenMP);

CREATE INDEX idxLinkAncestryanID ON AncestryTable (anID);

CREATE INDEX idxLinkAncestryRmId ON AncestryTable (rmID);

CREATE INDEX idxLinkfsID ON FamilySearchTable (fsID);

CREATE INDEX idxLinkRmId ON FamilySearchTable (rmID);

CREATE INDEX idxMediaFile ON MultimediaTable (MediaFile);

CREATE INDEX idxMediaOwnerID ON MediaLinkTable (OwnerID);

CREATE INDEX idxMediaURL ON MultimediaTable (URL);

CREATE INDEX idxNameOwnerID ON NameTable (OwnerID);

CREATE INDEX idxNamePrimary ON NameTable (IsPrimary);

CREATE INDEX idxOwnerDate ON EventTable (OwnerID,SortDate);

CREATE INDEX idxOwnerEvent ON EventTable (OwnerID,EventType);

CREATE INDEX idxPayloadType ON PayloadTable (RecType);

CREATE INDEX idxPlaceAbbrev ON PlaceTable (Abbrev);

CREATE INDEX idxPlaceName ON PlaceTable (Name);

CREATE INDEX idxRecType ON ConfigTable (RecType);

CREATE INDEX idxReversePlaceName ON PlaceTable (Reverse);

CREATE INDEX idxRoleEventType ON RoleTable (EventType);

CREATE INDEX idxSourceName ON SourceTable (Name COLLATE RMNOCASE) ;

CREATE INDEX idxSourceTemplateName ON SourceTemplateTable (Name);

CREATE INDEX idxSurname ON NameTable (Surname);

CREATE INDEX idxSurnameGiven ON NameTable (Surname, Given, BirthYear, DeathYear);

CREATE INDEX idxSurnameGivenMP ON NameTable (SurnameMP, GivenMP, BirthYear, DeathYear);

CREATE INDEX idxSurnameMP ON NameTable (SurnameMP);

CREATE INDEX idxTagType ON TagTable (TagType);

CREATE INDEX idxTaskName ON TaskTable (Name);

CREATE INDEX idxTaskOwnerID ON TaskLinkTable (OwnerID);

CREATE INDEX idxWitnessEventID ON WitnessTable (EventID);

CREATE INDEX idxWitnessPersonID ON WitnessTable (PersonID);
```

## RMNOCASE - found in DDL in these lines

``` SQL
CREATE TABLE AddressTable (AddressID INTEGER PRIMARY KEY, AddressType INTEGER, Name TEXT COLLATE RMNOCASE, Street1 TEXT, Street2 TEXT, City TEXT, State TEXT, Zip TEXT, Country TEXT, Phone1 TEXT, Phone2 TEXT, Fax TEXT, Email TEXT, URL TEXT, Latitude INTEGER, Longitude INTEGER, Note TEXT, UTCModDate FLOAT );

CREATE TABLE CitationTable (CitationID INTEGER PRIMARY KEY, SourceID INTEGER, Comments TEXT, ActualText TEXT, RefNumber TEXT, Footnote TEXT, ShortFootnote TEXT, Bibliography TEXT, Fields BLOB, UTCModDate FLOAT, CitationName TEXT COLLATE RMNOCASE );

CREATE TABLE FactTypeTable (FactTypeID INTEGER PRIMARY KEY, OwnerType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, GedcomTag TEXT, UseValue INTEGER, UseDate INTEGER, UsePlace INTEGER, Sentence TEXT, Flags INTEGER, UTCModDate FLOAT );

CREATE TABLE FANTypeTable (FANTypeID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, Role1 TEXT, Role2 TEXT, Sentence1 TEXT, Sentence2 TEXT, UTCModDate FLOAT );

CREATE TABLE MultimediaTable (MediaID INTEGER PRIMARY KEY, MediaType INTEGER, MediaPath TEXT, MediaFile TEXT COLLATE RMNOCASE, URL TEXT, Thumbnail BLOB, Caption TEXT COLLATE RMNOCASE, RefNumber TEXT COLLATE RMNOCASE, Date TEXT, SortDate BIGINT, Description TEXT, UTCModDate FLOAT );

CREATE TABLE NameTable (NameID INTEGER PRIMARY KEY, OwnerID INTEGER, Surname TEXT COLLATE RMNOCASE, Given TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE, Nickname TEXT COLLATE RMNOCASE, NameType INTEGER, Date TEXT, SortDate BIGINT, IsPrimary INTEGER, IsPrivate INTEGER, Proof INTEGER, Sentence TEXT, Note TEXT, BirthYear INTEGER, DeathYear INTEGER, Display INTEGER, Language TEXT, UTCModDate FLOAT, SurnameMP TEXT, GivenMP TEXT, NicknameMP TEXT );

CREATE TABLE PlaceTable (PlaceID INTEGER PRIMARY KEY, PlaceType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, Normalized TEXT, Latitude INTEGER, Longitude INTEGER, LatLongExact INTEGER, MasterID INTEGER, Note TEXT, Reverse TEXT COLLATE RMNOCASE, fsID INTEGER, anID INTEGER, UTCModDate FLOAT );

CREATE TABLE RoleTable (RoleID INTEGER PRIMARY KEY, RoleName TEXT COLLATE RMNOCASE, EventType INTEGER, RoleType INTEGER, Sentence TEXT, UTCModDate FLOAT );

CREATE TABLE SourceTable (SourceID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, RefNumber TEXT, ActualText TEXT, Comments TEXT, IsPrivate INTEGER, TemplateID INTEGER, Fields BLOB, UTCModDate FLOAT );

CREATE TABLE SourceTemplateTable (TemplateID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, Description TEXT, Favorite INTEGER, Category TEXT, Footnote TEXT, ShortFootnote TEXT, Bibliography TEXT, FieldDefs BLOB, UTCModDate FLOAT );

CREATE TABLE TagTable (TagID INTEGER PRIMARY KEY, TagType INTEGER, TagValue INTEGER, TagName TEXT COLLATE RMNOCASE, Description TEXT, UTCModDate FLOAT );

CREATE TABLE TaskTable (TaskID INTEGER PRIMARY KEY, TaskType INTEGER, RefNumber TEXT, Name TEXT COLLATE RMNOCASE, Status INTEGER, Priority INTEGER, Date1 TEXT, Date2 TEXT, Date3 TEXT, SortDate1 BIGINT, SortDate2 BIGINT, SortDate3 BITINT, Filename TEXT, Details TEXT, Results TEXT, UTCModDate FLOAT, Exclude INTEGER );

CREATE TABLE WitnessTable (WitnessID INTEGER PRIMARY KEY, EventID INTEGER, PersonID INTEGER, WitnessOrder INTEGER, Role INTEGER, Sentence TEXT, Note TEXT, Given TEXT COLLATE RMNOCASE, Surname TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE, UTCModDate FLOAT );

 Line 133: CREATE INDEX idxSourceName ON SourceTable (Name COLLATE RMNOCASE) ;
```

and isolated-

```
CREATE TABLE AddressTable (Name TEXT COLLATE RMNOCASE

CREATE TABLE CitationTable (CitationName TEXT COLLATE RMNOCASE

CREATE TABLE FactTypeTable (Name TEXT COLLATE RMNOCASE

CREATE TABLE FANTypeTable (Name TEXT COLLATE RMNOCASE

CREATE TABLE MultimediaTable (MediaFile TEXT COLLATE RMNOCASE, Caption TEXT COLLATE RMNOCASE, RefNumber TEXT COLLATE RMNOCASE, 

CREATE TABLE NameTable (Surname TEXT COLLATE RMNOCASE, Given TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE, Nickname TEXT COLLATE RMNOCASE

CREATE TABLE PlaceTable (Name TEXT COLLATE RMNOCASE, Reverse TEXT COLLATE RMNOCASE

CREATE TABLE RoleTable (RoleName TEXT COLLATE RMNOCASE

CREATE TABLE SourceTable (Name TEXT COLLATE RMNOCASE

CREATE TABLE SourceTemplateTable (Name TEXT COLLATE RMNOCASE

CREATE TABLE TagTable (TagName TEXT COLLATE RMNOCASE

CREATE TABLE TaskTable (Name TEXT COLLATE RMNOCASE

CREATE TABLE WitnessTable (Given TEXT COLLATE RMNOCASE, Surname TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE

 Line 133: CREATE INDEX idxSourceName ON SourceTable (Name COLLATE RMNOCASE) ;
```

This table is directly from:\
Pat Jones:\
<https://sqlitetoolsforrootsmagic.com/understanding-the-rootsmagic-8-database-ownership/>

| Owner Type Value | Owner Type                                        | URL | Place | Pl Detail | Media | Task | Address | Citation | Name | Child | Event |
| :--------------- | :------------------------------------------------ | :-- | :---- | :-------- | :---- | :--- | :------ | :------- | :--- | :---- | :---- |
| 0                | Person                                            | Y   |       |           | Y     | Y    | Y       | Y        | Y    |       | Y     |
| 1                | Family                                            |     |       |           | Y     | Y    | Y       | Y        |      | Y     | Y     |
| 2                | Event                                             |     | Y     | Y         | Y     | Y    |         | Y        |      |       |       |
| 3                | Source                                            | Y   |       |           | Y     |      | Y       | Y        |      |       |       |
| 4                | Citation                                          | Y   |       |           | Y     |      |         |          |      |       |       |
| 5                | Place                                             | Y   |       | Y         | Y     | Y    |         |          |      |       |       |
| 6                | Task                                              | Y   |       |           | Y     |      | Y       | Y        |      |       |       |
| 7                | Name                                              |     |       |           | Y     | Y    |         | Y        |      |       |       |
| 8                | not used (was General task in RM7 with 0 ownerid) |     |       |           |       |      |         |          |      |       |       |
| 14               | Place Detail                                      | Y   |       |           | Y     | Y    |         |          |      |       |       |
| 15               | not used (was Research Item in RM7)               |     |       |           |       |      |         |          |      |       |       |
| 18               | Task Folder (update of Research Log)              |     |       |           |       | Y    |         |          |      |       |       |
| 19               | Association                                       |     |       |           |       |      |         |          |      |       |       |

```
Table sumary
Object   Can own these:
    0 1 2 3 4 5 6 7 8 14 15 18  19
URL    0     3 4 5 6     14
Place       2
PlaceDetail      2     5
Media   0 1 2 3 4 5 6 7   14       19
Task   0 1 2     5   7   14 15
Address   0 1   3     6
Citation  0 1 2 3     6     7
Name   0
Child     1
Eent   0 1
```

## Boilerplate

reused text

►◄
