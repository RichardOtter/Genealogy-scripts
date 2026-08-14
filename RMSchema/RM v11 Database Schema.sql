CREATE TABLE AddressLinkTable (LinkID INTEGER PRIMARY KEY, OwnerType INTEGER, AddressID INTEGER, OwnerID INTEGER, AddressNum INTEGER, Details TEXT, UTCModDate FLOAT );

CREATE TABLE AddressTable (AddressID INTEGER PRIMARY KEY, AddressType INTEGER, Name TEXT COLLATE RMNOCASE, Street1 TEXT, Street2 TEXT, City TEXT, State TEXT, Zip TEXT, Country TEXT, Phone1 TEXT, Phone2 TEXT, Fax TEXT, Email TEXT, URL TEXT, Latitude INTEGER, Longitude INTEGER, Note TEXT, UTCModDate FLOAT );

CREATE TABLE AncestryTable (LinkID INTEGER PRIMARY KEY, LinkType INTEGER, rmID INTEGER, anID TEXT, Modified INTEGER, anVersion TEXT, anDate FLOAT, Status INTEGER, UTCModDate FLOAT , TreeID TEXT);

CREATE TABLE ChildTable (RecID INTEGER PRIMARY KEY, ChildID INTEGER, FamilyID INTEGER, RelFather INTEGER, RelMother INTEGER, ChildOrder INTEGER, IsPrivate INTEGER, ProofFather INTEGER, ProofMother INTEGER, Note TEXT, UTCModDate FLOAT );

CREATE TABLE CitationLinkTable (LinkID INTEGER PRIMARY KEY, CitationID INTEGER, OwnerType INTEGER, OwnerID INTEGER, SortOrder INTEGER, Quality TEXT, IsPrivate INTEGER, Flags INTEGER, UTCModDate FLOAT );

CREATE TABLE CitationTable (CitationID INTEGER PRIMARY KEY, SourceID INTEGER, Comments TEXT, ActualText TEXT, RefNumber TEXT, Footnote TEXT, ShortFootnote TEXT, Bibliography TEXT, Fields BLOB, UTCModDate FLOAT, CitationName TEXT COLLATE RMNOCASE );

CREATE TABLE ConfigTable (RecID INTEGER PRIMARY KEY, RecType INTEGER, Title TEXT, DataRec BLOB, UTCModDate FLOAT );

CREATE TABLE DNATable (RecID INTEGER PRIMARY KEY, ID1 INTEGER, ID2 INTEGER, Label1 TEXT, Label2 TEXT, DNAProvider INTEGER, SharedCM FLOAT, SharedPercent FLOAT, LargeSeg FLOAT, SharedSegs INTEGER, Date TEXT, Relate1 INTEGER, Relate2 INTEGER, CommonAnc INTEGER, CommonAncType INTEGER, Verified INTEGER, Note TEXT, UTCModDate FLOAT );

CREATE TABLE EventTable (EventID INTEGER PRIMARY KEY, EventType INTEGER, OwnerType INTEGER, OwnerID INTEGER, FamilyID INTEGER, PlaceID INTEGER, SiteID INTEGER, Date TEXT, SortDate BIGINT, IsPrimary INTEGER, IsPrivate INTEGER, Proof INTEGER, Status INTEGER, Sentence TEXT, Details TEXT, Note TEXT, UTCModDate FLOAT );

CREATE TABLE ExclusionTable (RecID INTEGER PRIMARY KEY, ExclusionType INTEGER, ID1 INTEGER, ID2 INTEGER, UTCModDate FLOAT );

CREATE TABLE FactTypeTable (FactTypeID INTEGER PRIMARY KEY, OwnerType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, GedcomTag TEXT, UseValue INTEGER, UseDate INTEGER, UsePlace INTEGER, Sentence TEXT, Flags INTEGER, UTCModDate FLOAT );

CREATE TABLE FamilySearchTable (LinkID INTEGER PRIMARY KEY, LinkType INTEGER, rmID INTEGER, fsID TEXT, Modified INTEGER, fsVersion TEXT, fsDate FLOAT, Status INTEGER, UTCModDate FLOAT , TreeID TEXT);

CREATE TABLE FamilyTable (FamilyID INTEGER PRIMARY KEY, FatherID INTEGER, MotherID INTEGER, ChildID INTEGER, HusbOrder INTEGER, WifeOrder INTEGER, IsPrivate INTEGER, Proof INTEGER, SpouseLabel INTEGER, FatherLabel INTEGER, MotherLabel INTEGER, SpouseLabelStr TEXT, FatherLabelStr TEXT, MotherLabelStr TEXT, Note TEXT, UTCModDate FLOAT );

CREATE TABLE FANTable (FanID INTEGER PRIMARY KEY, ID1 INTEGER, ID2 INTEGER, FanTypeID INTEGER, PlaceID INTEGER, SiteID INTEGER, Date TEXT, SortDate BIGINT, Description TEXT, Note TEXT, UTCModDate FLOAT );

CREATE TABLE FANTypeTable (FANTypeID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, Role1 TEXT, Role2 TEXT, Sentence1 TEXT, Sentence2 TEXT, UTCModDate FLOAT );

CREATE TABLE GroupTable (RecID INTEGER PRIMARY KEY, GroupID INTEGER, StartID INTEGER, EndID INTEGER, UTCModDate FLOAT );

CREATE TABLE HealthTable (RecID INTEGER PRIMARY KEY, OwnerID INTEGER, Condition INTEGER, SubCondition TEXT, Date FLOAT, Note TEXT, UTCModDate FLOAT );

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

CREATE INDEX idxDnaId1 ON DNATable (ID1);

CREATE INDEX idxDnaId2 ON DNATable (ID2);

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

CREATE INDEX idxHealthOwnerId ON HealthTable (OwnerID);

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

