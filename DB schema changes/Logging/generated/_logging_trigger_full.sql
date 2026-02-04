
    CREATE TRIGGER ChildTable_AuxChangeLogTable_update
    AFTER UPDATE ON ChildTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'ChildTable',
            OLD.RecID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'ChildID',  CASE WHEN OLD.ChildID  IS DISTINCT FROM NEW.ChildID   THEN json_object( 'old',OLD.ChildID,  'new',NEW.ChildID)   END,
              'FamilyID',  CASE WHEN OLD.FamilyID  IS DISTINCT FROM NEW.FamilyID   THEN json_object( 'old',OLD.FamilyID,  'new',NEW.FamilyID)   END,
              'RelFather',  CASE WHEN OLD.RelFather  IS DISTINCT FROM NEW.RelFather   THEN json_object( 'old',OLD.RelFather,  'new',NEW.RelFather)   END,
              'RelMother',  CASE WHEN OLD.RelMother  IS DISTINCT FROM NEW.RelMother   THEN json_object( 'old',OLD.RelMother,  'new',NEW.RelMother)   END,
              'ChildOrder',  CASE WHEN OLD.ChildOrder  IS DISTINCT FROM NEW.ChildOrder   THEN json_object( 'old',OLD.ChildOrder,  'new',NEW.ChildOrder)   END,
              'IsPrivate',  CASE WHEN OLD.IsPrivate  IS DISTINCT FROM NEW.IsPrivate   THEN json_object( 'old',OLD.IsPrivate,  'new',NEW.IsPrivate)   END,
              'ProofFather',  CASE WHEN OLD.ProofFather  IS DISTINCT FROM NEW.ProofFather   THEN json_object( 'old',OLD.ProofFather,  'new',NEW.ProofFather)   END,
              'ProofMother',  CASE WHEN OLD.ProofMother  IS DISTINCT FROM NEW.ProofMother   THEN json_object( 'old',OLD.ProofMother,  'new',NEW.ProofMother)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER CitationLinkTable_AuxChangeLogTable_update
    AFTER UPDATE ON CitationLinkTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'CitationLinkTable',
            OLD.LinkID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'CitationID',  CASE WHEN OLD.CitationID  IS DISTINCT FROM NEW.CitationID   THEN json_object( 'old',OLD.CitationID,  'new',NEW.CitationID)   END,
              'OwnerType',  CASE WHEN OLD.OwnerType  IS DISTINCT FROM NEW.OwnerType   THEN json_object( 'old',OLD.OwnerType,  'new',NEW.OwnerType)   END,
              'OwnerID',  CASE WHEN OLD.OwnerID  IS DISTINCT FROM NEW.OwnerID   THEN json_object( 'old',OLD.OwnerID,  'new',NEW.OwnerID)   END,
              'SortOrder',  CASE WHEN OLD.SortOrder  IS DISTINCT FROM NEW.SortOrder   THEN json_object( 'old',OLD.SortOrder,  'new',NEW.SortOrder)   END,
              'Quality',  CASE WHEN OLD.Quality  IS DISTINCT FROM NEW.Quality   THEN json_object( 'old',OLD.Quality,  'new',NEW.Quality)   END,
              'IsPrivate',  CASE WHEN OLD.IsPrivate  IS DISTINCT FROM NEW.IsPrivate   THEN json_object( 'old',OLD.IsPrivate,  'new',NEW.IsPrivate)   END,
              'Flags',  CASE WHEN OLD.Flags  IS DISTINCT FROM NEW.Flags   THEN json_object( 'old',OLD.Flags,  'new',NEW.Flags)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER ConfigTable_AuxChangeLogTable_update
    AFTER UPDATE ON ConfigTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'ConfigTable',
            OLD.RecID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'RecType',  CASE WHEN OLD.RecType  IS DISTINCT FROM NEW.RecType   THEN json_object( 'old',OLD.RecType,  'new',NEW.RecType)   END,
              'Title',  CASE WHEN OLD.Title  IS DISTINCT FROM NEW.Title   THEN json_object( 'old',OLD.Title,  'new',NEW.Title)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER EventTable_AuxChangeLogTable_update
    AFTER UPDATE ON EventTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'EventTable',
            OLD.EventID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'EventType',  CASE WHEN OLD.EventType  IS DISTINCT FROM NEW.EventType   THEN json_object( 'old',OLD.EventType,  'new',NEW.EventType)   END,
              'OwnerType',  CASE WHEN OLD.OwnerType  IS DISTINCT FROM NEW.OwnerType   THEN json_object( 'old',OLD.OwnerType,  'new',NEW.OwnerType)   END,
              'OwnerID',  CASE WHEN OLD.OwnerID  IS DISTINCT FROM NEW.OwnerID   THEN json_object( 'old',OLD.OwnerID,  'new',NEW.OwnerID)   END,
              'FamilyID',  CASE WHEN OLD.FamilyID  IS DISTINCT FROM NEW.FamilyID   THEN json_object( 'old',OLD.FamilyID,  'new',NEW.FamilyID)   END,
              'PlaceID',  CASE WHEN OLD.PlaceID  IS DISTINCT FROM NEW.PlaceID   THEN json_object( 'old',OLD.PlaceID,  'new',NEW.PlaceID)   END,
              'SiteID',  CASE WHEN OLD.SiteID  IS DISTINCT FROM NEW.SiteID   THEN json_object( 'old',OLD.SiteID,  'new',NEW.SiteID)   END,
              'Date',  CASE WHEN OLD.Date  IS DISTINCT FROM NEW.Date   THEN json_object( 'old',OLD.Date,  'new',NEW.Date)   END,
              'SortDate',  CASE WHEN OLD.SortDate  IS DISTINCT FROM NEW.SortDate   THEN json_object( 'old',OLD.SortDate,  'new',NEW.SortDate)   END,
              'IsPrimary',  CASE WHEN OLD.IsPrimary  IS DISTINCT FROM NEW.IsPrimary   THEN json_object( 'old',OLD.IsPrimary,  'new',NEW.IsPrimary)   END,
              'IsPrivate',  CASE WHEN OLD.IsPrivate  IS DISTINCT FROM NEW.IsPrivate   THEN json_object( 'old',OLD.IsPrivate,  'new',NEW.IsPrivate)   END,
              'Proof',  CASE WHEN OLD.Proof  IS DISTINCT FROM NEW.Proof   THEN json_object( 'old',OLD.Proof,  'new',NEW.Proof)   END,
              'Status',  CASE WHEN OLD.Status  IS DISTINCT FROM NEW.Status   THEN json_object( 'old',OLD.Status,  'new',NEW.Status)   END,
              'Sentence',  CASE WHEN OLD.Sentence  IS DISTINCT FROM NEW.Sentence   THEN json_object( 'old',OLD.Sentence,  'new',NEW.Sentence)   END,
              'Details',  CASE WHEN OLD.Details  IS DISTINCT FROM NEW.Details   THEN json_object( 'old',OLD.Details,  'new',NEW.Details)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER ExclusionTable_AuxChangeLogTable_update
    AFTER UPDATE ON ExclusionTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'ExclusionTable',
            OLD.RecID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'ExclusionType',  CASE WHEN OLD.ExclusionType  IS DISTINCT FROM NEW.ExclusionType   THEN json_object( 'old',OLD.ExclusionType,  'new',NEW.ExclusionType)   END,
              'ID1',  CASE WHEN OLD.ID1  IS DISTINCT FROM NEW.ID1   THEN json_object( 'old',OLD.ID1,  'new',NEW.ID1)   END,
              'ID2',  CASE WHEN OLD.ID2  IS DISTINCT FROM NEW.ID2   THEN json_object( 'old',OLD.ID2,  'new',NEW.ID2)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER FactTypeTable_AuxChangeLogTable_update
    AFTER UPDATE ON FactTypeTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'FactTypeTable',
            OLD.FactTypeID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'OwnerType',  CASE WHEN OLD.OwnerType  IS DISTINCT FROM NEW.OwnerType   THEN json_object( 'old',OLD.OwnerType,  'new',NEW.OwnerType)   END,
              'Name',  CASE WHEN OLD.Name  IS DISTINCT FROM NEW.Name   THEN json_object( 'old',OLD.Name,  'new',NEW.Name)   END,
              'Abbrev',  CASE WHEN OLD.Abbrev  IS DISTINCT FROM NEW.Abbrev   THEN json_object( 'old',OLD.Abbrev,  'new',NEW.Abbrev)   END,
              'GedcomTag',  CASE WHEN OLD.GedcomTag  IS DISTINCT FROM NEW.GedcomTag   THEN json_object( 'old',OLD.GedcomTag,  'new',NEW.GedcomTag)   END,
              'UseValue',  CASE WHEN OLD.UseValue  IS DISTINCT FROM NEW.UseValue   THEN json_object( 'old',OLD.UseValue,  'new',NEW.UseValue)   END,
              'UseDate',  CASE WHEN OLD.UseDate  IS DISTINCT FROM NEW.UseDate   THEN json_object( 'old',OLD.UseDate,  'new',NEW.UseDate)   END,
              'UsePlace',  CASE WHEN OLD.UsePlace  IS DISTINCT FROM NEW.UsePlace   THEN json_object( 'old',OLD.UsePlace,  'new',NEW.UsePlace)   END,
              'Sentence',  CASE WHEN OLD.Sentence  IS DISTINCT FROM NEW.Sentence   THEN json_object( 'old',OLD.Sentence,  'new',NEW.Sentence)   END,
              'Flags',  CASE WHEN OLD.Flags  IS DISTINCT FROM NEW.Flags   THEN json_object( 'old',OLD.Flags,  'new',NEW.Flags)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER FamilyTable_AuxChangeLogTable_update
    AFTER UPDATE ON FamilyTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'FamilyTable',
            OLD.FamilyID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'FatherID',  CASE WHEN OLD.FatherID  IS DISTINCT FROM NEW.FatherID   THEN json_object( 'old',OLD.FatherID,  'new',NEW.FatherID)   END,
              'MotherID',  CASE WHEN OLD.MotherID  IS DISTINCT FROM NEW.MotherID   THEN json_object( 'old',OLD.MotherID,  'new',NEW.MotherID)   END,
              'ChildID',  CASE WHEN OLD.ChildID  IS DISTINCT FROM NEW.ChildID   THEN json_object( 'old',OLD.ChildID,  'new',NEW.ChildID)   END,
              'HusbOrder',  CASE WHEN OLD.HusbOrder  IS DISTINCT FROM NEW.HusbOrder   THEN json_object( 'old',OLD.HusbOrder,  'new',NEW.HusbOrder)   END,
              'WifeOrder',  CASE WHEN OLD.WifeOrder  IS DISTINCT FROM NEW.WifeOrder   THEN json_object( 'old',OLD.WifeOrder,  'new',NEW.WifeOrder)   END,
              'IsPrivate',  CASE WHEN OLD.IsPrivate  IS DISTINCT FROM NEW.IsPrivate   THEN json_object( 'old',OLD.IsPrivate,  'new',NEW.IsPrivate)   END,
              'Proof',  CASE WHEN OLD.Proof  IS DISTINCT FROM NEW.Proof   THEN json_object( 'old',OLD.Proof,  'new',NEW.Proof)   END,
              'SpouseLabel',  CASE WHEN OLD.SpouseLabel  IS DISTINCT FROM NEW.SpouseLabel   THEN json_object( 'old',OLD.SpouseLabel,  'new',NEW.SpouseLabel)   END,
              'FatherLabel',  CASE WHEN OLD.FatherLabel  IS DISTINCT FROM NEW.FatherLabel   THEN json_object( 'old',OLD.FatherLabel,  'new',NEW.FatherLabel)   END,
              'MotherLabel',  CASE WHEN OLD.MotherLabel  IS DISTINCT FROM NEW.MotherLabel   THEN json_object( 'old',OLD.MotherLabel,  'new',NEW.MotherLabel)   END,
              'SpouseLabelStr',  CASE WHEN OLD.SpouseLabelStr  IS DISTINCT FROM NEW.SpouseLabelStr   THEN json_object( 'old',OLD.SpouseLabelStr,  'new',NEW.SpouseLabelStr)   END,
              'FatherLabelStr',  CASE WHEN OLD.FatherLabelStr  IS DISTINCT FROM NEW.FatherLabelStr   THEN json_object( 'old',OLD.FatherLabelStr,  'new',NEW.FatherLabelStr)   END,
              'MotherLabelStr',  CASE WHEN OLD.MotherLabelStr  IS DISTINCT FROM NEW.MotherLabelStr   THEN json_object( 'old',OLD.MotherLabelStr,  'new',NEW.MotherLabelStr)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER GroupTable_AuxChangeLogTable_update
    AFTER UPDATE ON GroupTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'GroupTable',
            OLD.RecID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'GroupID',  CASE WHEN OLD.GroupID  IS DISTINCT FROM NEW.GroupID   THEN json_object( 'old',OLD.GroupID,  'new',NEW.GroupID)   END,
              'StartID',  CASE WHEN OLD.StartID  IS DISTINCT FROM NEW.StartID   THEN json_object( 'old',OLD.StartID,  'new',NEW.StartID)   END,
              'EndID',  CASE WHEN OLD.EndID  IS DISTINCT FROM NEW.EndID   THEN json_object( 'old',OLD.EndID,  'new',NEW.EndID)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER MediaLinkTable_AuxChangeLogTable_update
    AFTER UPDATE ON MediaLinkTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'MediaLinkTable',
            OLD.LinkID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'MediaID',  CASE WHEN OLD.MediaID  IS DISTINCT FROM NEW.MediaID   THEN json_object( 'old',OLD.MediaID,  'new',NEW.MediaID)   END,
              'OwnerType',  CASE WHEN OLD.OwnerType  IS DISTINCT FROM NEW.OwnerType   THEN json_object( 'old',OLD.OwnerType,  'new',NEW.OwnerType)   END,
              'OwnerID',  CASE WHEN OLD.OwnerID  IS DISTINCT FROM NEW.OwnerID   THEN json_object( 'old',OLD.OwnerID,  'new',NEW.OwnerID)   END,
              'IsPrimary',  CASE WHEN OLD.IsPrimary  IS DISTINCT FROM NEW.IsPrimary   THEN json_object( 'old',OLD.IsPrimary,  'new',NEW.IsPrimary)   END,
              'Include1',  CASE WHEN OLD.Include1  IS DISTINCT FROM NEW.Include1   THEN json_object( 'old',OLD.Include1,  'new',NEW.Include1)   END,
              'Include2',  CASE WHEN OLD.Include2  IS DISTINCT FROM NEW.Include2   THEN json_object( 'old',OLD.Include2,  'new',NEW.Include2)   END,
              'Include3',  CASE WHEN OLD.Include3  IS DISTINCT FROM NEW.Include3   THEN json_object( 'old',OLD.Include3,  'new',NEW.Include3)   END,
              'Include4',  CASE WHEN OLD.Include4  IS DISTINCT FROM NEW.Include4   THEN json_object( 'old',OLD.Include4,  'new',NEW.Include4)   END,
              'SortOrder',  CASE WHEN OLD.SortOrder  IS DISTINCT FROM NEW.SortOrder   THEN json_object( 'old',OLD.SortOrder,  'new',NEW.SortOrder)   END,
              'RectLeft',  CASE WHEN OLD.RectLeft  IS DISTINCT FROM NEW.RectLeft   THEN json_object( 'old',OLD.RectLeft,  'new',NEW.RectLeft)   END,
              'RectTop',  CASE WHEN OLD.RectTop  IS DISTINCT FROM NEW.RectTop   THEN json_object( 'old',OLD.RectTop,  'new',NEW.RectTop)   END,
              'RectRight',  CASE WHEN OLD.RectRight  IS DISTINCT FROM NEW.RectRight   THEN json_object( 'old',OLD.RectRight,  'new',NEW.RectRight)   END,
              'RectBottom',  CASE WHEN OLD.RectBottom  IS DISTINCT FROM NEW.RectBottom   THEN json_object( 'old',OLD.RectBottom,  'new',NEW.RectBottom)   END,
              'Comments',  CASE WHEN OLD.Comments  IS DISTINCT FROM NEW.Comments   THEN json_object( 'old',OLD.Comments,  'new',NEW.Comments)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER MultimediaTable_AuxChangeLogTable_update
    AFTER UPDATE ON MultimediaTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'MultimediaTable',
            OLD.MediaID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'MediaType',  CASE WHEN OLD.MediaType  IS DISTINCT FROM NEW.MediaType   THEN json_object( 'old',OLD.MediaType,  'new',NEW.MediaType)   END,
              'MediaPath',  CASE WHEN OLD.MediaPath  IS DISTINCT FROM NEW.MediaPath   THEN json_object( 'old',OLD.MediaPath,  'new',NEW.MediaPath)   END,
              'MediaFile',  CASE WHEN OLD.MediaFile  IS DISTINCT FROM NEW.MediaFile   THEN json_object( 'old',OLD.MediaFile,  'new',NEW.MediaFile)   END,
              'URL',  CASE WHEN OLD.URL  IS DISTINCT FROM NEW.URL   THEN json_object( 'old',OLD.URL,  'new',NEW.URL)   END,
              'Caption',  CASE WHEN OLD.Caption  IS DISTINCT FROM NEW.Caption   THEN json_object( 'old',OLD.Caption,  'new',NEW.Caption)   END,
              'RefNumber',  CASE WHEN OLD.RefNumber  IS DISTINCT FROM NEW.RefNumber   THEN json_object( 'old',OLD.RefNumber,  'new',NEW.RefNumber)   END,
              'Date',  CASE WHEN OLD.Date  IS DISTINCT FROM NEW.Date   THEN json_object( 'old',OLD.Date,  'new',NEW.Date)   END,
              'SortDate',  CASE WHEN OLD.SortDate  IS DISTINCT FROM NEW.SortDate   THEN json_object( 'old',OLD.SortDate,  'new',NEW.SortDate)   END,
              'Description',  CASE WHEN OLD.Description  IS DISTINCT FROM NEW.Description   THEN json_object( 'old',OLD.Description,  'new',NEW.Description)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER NameTable_AuxChangeLogTable_update
    AFTER UPDATE ON NameTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'NameTable',
            OLD.NameID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'OwnerID',  CASE WHEN OLD.OwnerID  IS DISTINCT FROM NEW.OwnerID   THEN json_object( 'old',OLD.OwnerID,  'new',NEW.OwnerID)   END,
              'Surname',  CASE WHEN OLD.Surname  IS DISTINCT FROM NEW.Surname   THEN json_object( 'old',OLD.Surname,  'new',NEW.Surname)   END,
              'Given',  CASE WHEN OLD.Given  IS DISTINCT FROM NEW.Given   THEN json_object( 'old',OLD.Given,  'new',NEW.Given)   END,
              'Prefix',  CASE WHEN OLD.Prefix  IS DISTINCT FROM NEW.Prefix   THEN json_object( 'old',OLD.Prefix,  'new',NEW.Prefix)   END,
              'Suffix',  CASE WHEN OLD.Suffix  IS DISTINCT FROM NEW.Suffix   THEN json_object( 'old',OLD.Suffix,  'new',NEW.Suffix)   END,
              'Nickname',  CASE WHEN OLD.Nickname  IS DISTINCT FROM NEW.Nickname   THEN json_object( 'old',OLD.Nickname,  'new',NEW.Nickname)   END,
              'NameType',  CASE WHEN OLD.NameType  IS DISTINCT FROM NEW.NameType   THEN json_object( 'old',OLD.NameType,  'new',NEW.NameType)   END,
              'Date',  CASE WHEN OLD.Date  IS DISTINCT FROM NEW.Date   THEN json_object( 'old',OLD.Date,  'new',NEW.Date)   END,
              'SortDate',  CASE WHEN OLD.SortDate  IS DISTINCT FROM NEW.SortDate   THEN json_object( 'old',OLD.SortDate,  'new',NEW.SortDate)   END,
              'IsPrimary',  CASE WHEN OLD.IsPrimary  IS DISTINCT FROM NEW.IsPrimary   THEN json_object( 'old',OLD.IsPrimary,  'new',NEW.IsPrimary)   END,
              'IsPrivate',  CASE WHEN OLD.IsPrivate  IS DISTINCT FROM NEW.IsPrivate   THEN json_object( 'old',OLD.IsPrivate,  'new',NEW.IsPrivate)   END,
              'Proof',  CASE WHEN OLD.Proof  IS DISTINCT FROM NEW.Proof   THEN json_object( 'old',OLD.Proof,  'new',NEW.Proof)   END,
              'Sentence',  CASE WHEN OLD.Sentence  IS DISTINCT FROM NEW.Sentence   THEN json_object( 'old',OLD.Sentence,  'new',NEW.Sentence)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'BirthYear',  CASE WHEN OLD.BirthYear  IS DISTINCT FROM NEW.BirthYear   THEN json_object( 'old',OLD.BirthYear,  'new',NEW.BirthYear)   END,
              'DeathYear',  CASE WHEN OLD.DeathYear  IS DISTINCT FROM NEW.DeathYear   THEN json_object( 'old',OLD.DeathYear,  'new',NEW.DeathYear)   END,
              'Display',  CASE WHEN OLD.Display  IS DISTINCT FROM NEW.Display   THEN json_object( 'old',OLD.Display,  'new',NEW.Display)   END,
              'Language',  CASE WHEN OLD.Language  IS DISTINCT FROM NEW.Language   THEN json_object( 'old',OLD.Language,  'new',NEW.Language)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END,
              'SurnameMP',  CASE WHEN OLD.SurnameMP  IS DISTINCT FROM NEW.SurnameMP   THEN json_object( 'old',OLD.SurnameMP,  'new',NEW.SurnameMP)   END,
              'GivenMP',  CASE WHEN OLD.GivenMP  IS DISTINCT FROM NEW.GivenMP   THEN json_object( 'old',OLD.GivenMP,  'new',NEW.GivenMP)   END,
              'NicknameMP',  CASE WHEN OLD.NicknameMP  IS DISTINCT FROM NEW.NicknameMP   THEN json_object( 'old',OLD.NicknameMP,  'new',NEW.NicknameMP)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER PlaceTable_AuxChangeLogTable_update
    AFTER UPDATE ON PlaceTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'PlaceTable',
            OLD.PlaceID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'PlaceType',  CASE WHEN OLD.PlaceType  IS DISTINCT FROM NEW.PlaceType   THEN json_object( 'old',OLD.PlaceType,  'new',NEW.PlaceType)   END,
              'Name',  CASE WHEN OLD.Name  IS DISTINCT FROM NEW.Name   THEN json_object( 'old',OLD.Name,  'new',NEW.Name)   END,
              'Abbrev',  CASE WHEN OLD.Abbrev  IS DISTINCT FROM NEW.Abbrev   THEN json_object( 'old',OLD.Abbrev,  'new',NEW.Abbrev)   END,
              'Normalized',  CASE WHEN OLD.Normalized  IS DISTINCT FROM NEW.Normalized   THEN json_object( 'old',OLD.Normalized,  'new',NEW.Normalized)   END,
              'Latitude',  CASE WHEN OLD.Latitude  IS DISTINCT FROM NEW.Latitude   THEN json_object( 'old',OLD.Latitude,  'new',NEW.Latitude)   END,
              'Longitude',  CASE WHEN OLD.Longitude  IS DISTINCT FROM NEW.Longitude   THEN json_object( 'old',OLD.Longitude,  'new',NEW.Longitude)   END,
              'LatLongExact',  CASE WHEN OLD.LatLongExact  IS DISTINCT FROM NEW.LatLongExact   THEN json_object( 'old',OLD.LatLongExact,  'new',NEW.LatLongExact)   END,
              'MasterID',  CASE WHEN OLD.MasterID  IS DISTINCT FROM NEW.MasterID   THEN json_object( 'old',OLD.MasterID,  'new',NEW.MasterID)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'Reverse',  CASE WHEN OLD.Reverse  IS DISTINCT FROM NEW.Reverse   THEN json_object( 'old',OLD.Reverse,  'new',NEW.Reverse)   END,
              'fsID',  CASE WHEN OLD.fsID  IS DISTINCT FROM NEW.fsID   THEN json_object( 'old',OLD.fsID,  'new',NEW.fsID)   END,
              'anID',  CASE WHEN OLD.anID  IS DISTINCT FROM NEW.anID   THEN json_object( 'old',OLD.anID,  'new',NEW.anID)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER RoleTable_AuxChangeLogTable_update
    AFTER UPDATE ON RoleTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'RoleTable',
            OLD.RoleID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'RoleName',  CASE WHEN OLD.RoleName  IS DISTINCT FROM NEW.RoleName   THEN json_object( 'old',OLD.RoleName,  'new',NEW.RoleName)   END,
              'EventType',  CASE WHEN OLD.EventType  IS DISTINCT FROM NEW.EventType   THEN json_object( 'old',OLD.EventType,  'new',NEW.EventType)   END,
              'RoleType',  CASE WHEN OLD.RoleType  IS DISTINCT FROM NEW.RoleType   THEN json_object( 'old',OLD.RoleType,  'new',NEW.RoleType)   END,
              'Sentence',  CASE WHEN OLD.Sentence  IS DISTINCT FROM NEW.Sentence   THEN json_object( 'old',OLD.Sentence,  'new',NEW.Sentence)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER SourceTable_AuxChangeLogTable_update
    AFTER UPDATE ON SourceTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'SourceTable',
            OLD.SourceID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'Name',  CASE WHEN OLD.Name  IS DISTINCT FROM NEW.Name   THEN json_object( 'old',OLD.Name,  'new',NEW.Name)   END,
              'RefNumber',  CASE WHEN OLD.RefNumber  IS DISTINCT FROM NEW.RefNumber   THEN json_object( 'old',OLD.RefNumber,  'new',NEW.RefNumber)   END,
              'ActualText',  CASE WHEN OLD.ActualText  IS DISTINCT FROM NEW.ActualText   THEN json_object( 'old',OLD.ActualText,  'new',NEW.ActualText)   END,
              'Comments',  CASE WHEN OLD.Comments  IS DISTINCT FROM NEW.Comments   THEN json_object( 'old',OLD.Comments,  'new',NEW.Comments)   END,
              'IsPrivate',  CASE WHEN OLD.IsPrivate  IS DISTINCT FROM NEW.IsPrivate   THEN json_object( 'old',OLD.IsPrivate,  'new',NEW.IsPrivate)   END,
              'TemplateID',  CASE WHEN OLD.TemplateID  IS DISTINCT FROM NEW.TemplateID   THEN json_object( 'old',OLD.TemplateID,  'new',NEW.TemplateID)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER SourceTemplateTable_AuxChangeLogTable_update
    AFTER UPDATE ON SourceTemplateTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'SourceTemplateTable',
            OLD.TemplateID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'Name',  CASE WHEN OLD.Name  IS DISTINCT FROM NEW.Name   THEN json_object( 'old',OLD.Name,  'new',NEW.Name)   END,
              'Description',  CASE WHEN OLD.Description  IS DISTINCT FROM NEW.Description   THEN json_object( 'old',OLD.Description,  'new',NEW.Description)   END,
              'Favorite',  CASE WHEN OLD.Favorite  IS DISTINCT FROM NEW.Favorite   THEN json_object( 'old',OLD.Favorite,  'new',NEW.Favorite)   END,
              'Category',  CASE WHEN OLD.Category  IS DISTINCT FROM NEW.Category   THEN json_object( 'old',OLD.Category,  'new',NEW.Category)   END,
              'Footnote',  CASE WHEN OLD.Footnote  IS DISTINCT FROM NEW.Footnote   THEN json_object( 'old',OLD.Footnote,  'new',NEW.Footnote)   END,
              'ShortFootnote',  CASE WHEN OLD.ShortFootnote  IS DISTINCT FROM NEW.ShortFootnote   THEN json_object( 'old',OLD.ShortFootnote,  'new',NEW.ShortFootnote)   END,
              'Bibliography',  CASE WHEN OLD.Bibliography  IS DISTINCT FROM NEW.Bibliography   THEN json_object( 'old',OLD.Bibliography,  'new',NEW.Bibliography)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER TagTable_AuxChangeLogTable_update
    AFTER UPDATE ON TagTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'TagTable',
            OLD.TagID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'TagType',  CASE WHEN OLD.TagType  IS DISTINCT FROM NEW.TagType   THEN json_object( 'old',OLD.TagType,  'new',NEW.TagType)   END,
              'TagValue',  CASE WHEN OLD.TagValue  IS DISTINCT FROM NEW.TagValue   THEN json_object( 'old',OLD.TagValue,  'new',NEW.TagValue)   END,
              'TagName',  CASE WHEN OLD.TagName  IS DISTINCT FROM NEW.TagName   THEN json_object( 'old',OLD.TagName,  'new',NEW.TagName)   END,
              'Description',  CASE WHEN OLD.Description  IS DISTINCT FROM NEW.Description   THEN json_object( 'old',OLD.Description,  'new',NEW.Description)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER TaskLinkTable_AuxChangeLogTable_update
    AFTER UPDATE ON TaskLinkTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'TaskLinkTable',
            OLD.LinkID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'TaskID',  CASE WHEN OLD.TaskID  IS DISTINCT FROM NEW.TaskID   THEN json_object( 'old',OLD.TaskID,  'new',NEW.TaskID)   END,
              'OwnerType',  CASE WHEN OLD.OwnerType  IS DISTINCT FROM NEW.OwnerType   THEN json_object( 'old',OLD.OwnerType,  'new',NEW.OwnerType)   END,
              'OwnerID',  CASE WHEN OLD.OwnerID  IS DISTINCT FROM NEW.OwnerID   THEN json_object( 'old',OLD.OwnerID,  'new',NEW.OwnerID)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER TaskTable_AuxChangeLogTable_update
    AFTER UPDATE ON TaskTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'TaskTable',
            OLD.TaskID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'TaskType',  CASE WHEN OLD.TaskType  IS DISTINCT FROM NEW.TaskType   THEN json_object( 'old',OLD.TaskType,  'new',NEW.TaskType)   END,
              'RefNumber',  CASE WHEN OLD.RefNumber  IS DISTINCT FROM NEW.RefNumber   THEN json_object( 'old',OLD.RefNumber,  'new',NEW.RefNumber)   END,
              'Name',  CASE WHEN OLD.Name  IS DISTINCT FROM NEW.Name   THEN json_object( 'old',OLD.Name,  'new',NEW.Name)   END,
              'Status',  CASE WHEN OLD.Status  IS DISTINCT FROM NEW.Status   THEN json_object( 'old',OLD.Status,  'new',NEW.Status)   END,
              'Priority',  CASE WHEN OLD.Priority  IS DISTINCT FROM NEW.Priority   THEN json_object( 'old',OLD.Priority,  'new',NEW.Priority)   END,
              'Date1',  CASE WHEN OLD.Date1  IS DISTINCT FROM NEW.Date1   THEN json_object( 'old',OLD.Date1,  'new',NEW.Date1)   END,
              'Date2',  CASE WHEN OLD.Date2  IS DISTINCT FROM NEW.Date2   THEN json_object( 'old',OLD.Date2,  'new',NEW.Date2)   END,
              'Date3',  CASE WHEN OLD.Date3  IS DISTINCT FROM NEW.Date3   THEN json_object( 'old',OLD.Date3,  'new',NEW.Date3)   END,
              'SortDate1',  CASE WHEN OLD.SortDate1  IS DISTINCT FROM NEW.SortDate1   THEN json_object( 'old',OLD.SortDate1,  'new',NEW.SortDate1)   END,
              'SortDate2',  CASE WHEN OLD.SortDate2  IS DISTINCT FROM NEW.SortDate2   THEN json_object( 'old',OLD.SortDate2,  'new',NEW.SortDate2)   END,
              'SortDate3',  CASE WHEN OLD.SortDate3  IS DISTINCT FROM NEW.SortDate3   THEN json_object( 'old',OLD.SortDate3,  'new',NEW.SortDate3)   END,
              'Filename',  CASE WHEN OLD.Filename  IS DISTINCT FROM NEW.Filename   THEN json_object( 'old',OLD.Filename,  'new',NEW.Filename)   END,
              'Details',  CASE WHEN OLD.Details  IS DISTINCT FROM NEW.Details   THEN json_object( 'old',OLD.Details,  'new',NEW.Details)   END,
              'Results',  CASE WHEN OLD.Results  IS DISTINCT FROM NEW.Results   THEN json_object( 'old',OLD.Results,  'new',NEW.Results)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END,
              'Exclude',  CASE WHEN OLD.Exclude  IS DISTINCT FROM NEW.Exclude   THEN json_object( 'old',OLD.Exclude,  'new',NEW.Exclude)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER URLTable_AuxChangeLogTable_update
    AFTER UPDATE ON URLTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'URLTable',
            OLD.LinkID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'OwnerType',  CASE WHEN OLD.OwnerType  IS DISTINCT FROM NEW.OwnerType   THEN json_object( 'old',OLD.OwnerType,  'new',NEW.OwnerType)   END,
              'OwnerID',  CASE WHEN OLD.OwnerID  IS DISTINCT FROM NEW.OwnerID   THEN json_object( 'old',OLD.OwnerID,  'new',NEW.OwnerID)   END,
              'LinkType',  CASE WHEN OLD.LinkType  IS DISTINCT FROM NEW.LinkType   THEN json_object( 'old',OLD.LinkType,  'new',NEW.LinkType)   END,
              'Name',  CASE WHEN OLD.Name  IS DISTINCT FROM NEW.Name   THEN json_object( 'old',OLD.Name,  'new',NEW.Name)   END,
              'URL',  CASE WHEN OLD.URL  IS DISTINCT FROM NEW.URL   THEN json_object( 'old',OLD.URL,  'new',NEW.URL)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER WitnessTable_AuxChangeLogTable_update
    AFTER UPDATE ON WitnessTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'WitnessTable',
            OLD.WitnessID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'EventID',  CASE WHEN OLD.EventID  IS DISTINCT FROM NEW.EventID   THEN json_object( 'old',OLD.EventID,  'new',NEW.EventID)   END,
              'PersonID',  CASE WHEN OLD.PersonID  IS DISTINCT FROM NEW.PersonID   THEN json_object( 'old',OLD.PersonID,  'new',NEW.PersonID)   END,
              'WitnessOrder',  CASE WHEN OLD.WitnessOrder  IS DISTINCT FROM NEW.WitnessOrder   THEN json_object( 'old',OLD.WitnessOrder,  'new',NEW.WitnessOrder)   END,
              'Role',  CASE WHEN OLD.Role  IS DISTINCT FROM NEW.Role   THEN json_object( 'old',OLD.Role,  'new',NEW.Role)   END,
              'Sentence',  CASE WHEN OLD.Sentence  IS DISTINCT FROM NEW.Sentence   THEN json_object( 'old',OLD.Sentence,  'new',NEW.Sentence)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'Given',  CASE WHEN OLD.Given  IS DISTINCT FROM NEW.Given   THEN json_object( 'old',OLD.Given,  'new',NEW.Given)   END,
              'Surname',  CASE WHEN OLD.Surname  IS DISTINCT FROM NEW.Surname   THEN json_object( 'old',OLD.Surname,  'new',NEW.Surname)   END,
              'Prefix',  CASE WHEN OLD.Prefix  IS DISTINCT FROM NEW.Prefix   THEN json_object( 'old',OLD.Prefix,  'new',NEW.Prefix)   END,
              'Suffix',  CASE WHEN OLD.Suffix  IS DISTINCT FROM NEW.Suffix   THEN json_object( 'old',OLD.Suffix,  'new',NEW.Suffix)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER FANTypeTable_AuxChangeLogTable_update
    AFTER UPDATE ON FANTypeTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'FANTypeTable',
            OLD.FANTypeID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'Name',  CASE WHEN OLD.Name  IS DISTINCT FROM NEW.Name   THEN json_object( 'old',OLD.Name,  'new',NEW.Name)   END,
              'Role1',  CASE WHEN OLD.Role1  IS DISTINCT FROM NEW.Role1   THEN json_object( 'old',OLD.Role1,  'new',NEW.Role1)   END,
              'Role2',  CASE WHEN OLD.Role2  IS DISTINCT FROM NEW.Role2   THEN json_object( 'old',OLD.Role2,  'new',NEW.Role2)   END,
              'Sentence1',  CASE WHEN OLD.Sentence1  IS DISTINCT FROM NEW.Sentence1   THEN json_object( 'old',OLD.Sentence1,  'new',NEW.Sentence1)   END,
              'Sentence2',  CASE WHEN OLD.Sentence2  IS DISTINCT FROM NEW.Sentence2   THEN json_object( 'old',OLD.Sentence2,  'new',NEW.Sentence2)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER FANTable_AuxChangeLogTable_update
    AFTER UPDATE ON FANTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'FANTable',
            OLD.FanID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'ID1',  CASE WHEN OLD.ID1  IS DISTINCT FROM NEW.ID1   THEN json_object( 'old',OLD.ID1,  'new',NEW.ID1)   END,
              'ID2',  CASE WHEN OLD.ID2  IS DISTINCT FROM NEW.ID2   THEN json_object( 'old',OLD.ID2,  'new',NEW.ID2)   END,
              'FanTypeID',  CASE WHEN OLD.FanTypeID  IS DISTINCT FROM NEW.FanTypeID   THEN json_object( 'old',OLD.FanTypeID,  'new',NEW.FanTypeID)   END,
              'PlaceID',  CASE WHEN OLD.PlaceID  IS DISTINCT FROM NEW.PlaceID   THEN json_object( 'old',OLD.PlaceID,  'new',NEW.PlaceID)   END,
              'SiteID',  CASE WHEN OLD.SiteID  IS DISTINCT FROM NEW.SiteID   THEN json_object( 'old',OLD.SiteID,  'new',NEW.SiteID)   END,
              'Date',  CASE WHEN OLD.Date  IS DISTINCT FROM NEW.Date   THEN json_object( 'old',OLD.Date,  'new',NEW.Date)   END,
              'SortDate',  CASE WHEN OLD.SortDate  IS DISTINCT FROM NEW.SortDate   THEN json_object( 'old',OLD.SortDate,  'new',NEW.SortDate)   END,
              'Description',  CASE WHEN OLD.Description  IS DISTINCT FROM NEW.Description   THEN json_object( 'old',OLD.Description,  'new',NEW.Description)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER PayloadTable_AuxChangeLogTable_update
    AFTER UPDATE ON PayloadTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'PayloadTable',
            OLD.RecID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'RecType',  CASE WHEN OLD.RecType  IS DISTINCT FROM NEW.RecType   THEN json_object( 'old',OLD.RecType,  'new',NEW.RecType)   END,
              'OwnerType',  CASE WHEN OLD.OwnerType  IS DISTINCT FROM NEW.OwnerType   THEN json_object( 'old',OLD.OwnerType,  'new',NEW.OwnerType)   END,
              'OwnerID',  CASE WHEN OLD.OwnerID  IS DISTINCT FROM NEW.OwnerID   THEN json_object( 'old',OLD.OwnerID,  'new',NEW.OwnerID)   END,
              'Title',  CASE WHEN OLD.Title  IS DISTINCT FROM NEW.Title   THEN json_object( 'old',OLD.Title,  'new',NEW.Title)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER CitationTable_AuxChangeLogTable_update
    AFTER UPDATE ON CitationTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'CitationTable',
            OLD.CitationID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'SourceID',  CASE WHEN OLD.SourceID  IS DISTINCT FROM NEW.SourceID   THEN json_object( 'old',OLD.SourceID,  'new',NEW.SourceID)   END,
              'Comments',  CASE WHEN OLD.Comments  IS DISTINCT FROM NEW.Comments   THEN json_object( 'old',OLD.Comments,  'new',NEW.Comments)   END,
              'ActualText',  CASE WHEN OLD.ActualText  IS DISTINCT FROM NEW.ActualText   THEN json_object( 'old',OLD.ActualText,  'new',NEW.ActualText)   END,
              'RefNumber',  CASE WHEN OLD.RefNumber  IS DISTINCT FROM NEW.RefNumber   THEN json_object( 'old',OLD.RefNumber,  'new',NEW.RefNumber)   END,
              'Footnote',  CASE WHEN OLD.Footnote  IS DISTINCT FROM NEW.Footnote   THEN json_object( 'old',OLD.Footnote,  'new',NEW.Footnote)   END,
              'ShortFootnote',  CASE WHEN OLD.ShortFootnote  IS DISTINCT FROM NEW.ShortFootnote   THEN json_object( 'old',OLD.ShortFootnote,  'new',NEW.ShortFootnote)   END,
              'Bibliography',  CASE WHEN OLD.Bibliography  IS DISTINCT FROM NEW.Bibliography   THEN json_object( 'old',OLD.Bibliography,  'new',NEW.Bibliography)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END,
              'CitationName',  CASE WHEN OLD.CitationName  IS DISTINCT FROM NEW.CitationName   THEN json_object( 'old',OLD.CitationName,  'new',NEW.CitationName)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER PersonTable_AuxChangeLogTable_update
    AFTER UPDATE ON PersonTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'PersonTable',
            OLD.PersonID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'UniqueID',  CASE WHEN OLD.UniqueID  IS DISTINCT FROM NEW.UniqueID   THEN json_object( 'old',OLD.UniqueID,  'new',NEW.UniqueID)   END,
              'Sex',  CASE WHEN OLD.Sex  IS DISTINCT FROM NEW.Sex   THEN json_object( 'old',OLD.Sex,  'new',NEW.Sex)   END,
              'ParentID',  CASE WHEN OLD.ParentID  IS DISTINCT FROM NEW.ParentID   THEN json_object( 'old',OLD.ParentID,  'new',NEW.ParentID)   END,
              'SpouseID',  CASE WHEN OLD.SpouseID  IS DISTINCT FROM NEW.SpouseID   THEN json_object( 'old',OLD.SpouseID,  'new',NEW.SpouseID)   END,
              'Color',  CASE WHEN OLD.Color  IS DISTINCT FROM NEW.Color   THEN json_object( 'old',OLD.Color,  'new',NEW.Color)   END,
              'Color1',  CASE WHEN OLD.Color1  IS DISTINCT FROM NEW.Color1   THEN json_object( 'old',OLD.Color1,  'new',NEW.Color1)   END,
              'Color2',  CASE WHEN OLD.Color2  IS DISTINCT FROM NEW.Color2   THEN json_object( 'old',OLD.Color2,  'new',NEW.Color2)   END,
              'Color3',  CASE WHEN OLD.Color3  IS DISTINCT FROM NEW.Color3   THEN json_object( 'old',OLD.Color3,  'new',NEW.Color3)   END,
              'Color4',  CASE WHEN OLD.Color4  IS DISTINCT FROM NEW.Color4   THEN json_object( 'old',OLD.Color4,  'new',NEW.Color4)   END,
              'Color5',  CASE WHEN OLD.Color5  IS DISTINCT FROM NEW.Color5   THEN json_object( 'old',OLD.Color5,  'new',NEW.Color5)   END,
              'Color6',  CASE WHEN OLD.Color6  IS DISTINCT FROM NEW.Color6   THEN json_object( 'old',OLD.Color6,  'new',NEW.Color6)   END,
              'Color7',  CASE WHEN OLD.Color7  IS DISTINCT FROM NEW.Color7   THEN json_object( 'old',OLD.Color7,  'new',NEW.Color7)   END,
              'Color8',  CASE WHEN OLD.Color8  IS DISTINCT FROM NEW.Color8   THEN json_object( 'old',OLD.Color8,  'new',NEW.Color8)   END,
              'Color9',  CASE WHEN OLD.Color9  IS DISTINCT FROM NEW.Color9   THEN json_object( 'old',OLD.Color9,  'new',NEW.Color9)   END,
              'Relate1',  CASE WHEN OLD.Relate1  IS DISTINCT FROM NEW.Relate1   THEN json_object( 'old',OLD.Relate1,  'new',NEW.Relate1)   END,
              'Relate2',  CASE WHEN OLD.Relate2  IS DISTINCT FROM NEW.Relate2   THEN json_object( 'old',OLD.Relate2,  'new',NEW.Relate2)   END,
              'Flags',  CASE WHEN OLD.Flags  IS DISTINCT FROM NEW.Flags   THEN json_object( 'old',OLD.Flags,  'new',NEW.Flags)   END,
              'Living',  CASE WHEN OLD.Living  IS DISTINCT FROM NEW.Living   THEN json_object( 'old',OLD.Living,  'new',NEW.Living)   END,
              'IsPrivate',  CASE WHEN OLD.IsPrivate  IS DISTINCT FROM NEW.IsPrivate   THEN json_object( 'old',OLD.IsPrivate,  'new',NEW.IsPrivate)   END,
              'Proof',  CASE WHEN OLD.Proof  IS DISTINCT FROM NEW.Proof   THEN json_object( 'old',OLD.Proof,  'new',NEW.Proof)   END,
              'Bookmark',  CASE WHEN OLD.Bookmark  IS DISTINCT FROM NEW.Bookmark   THEN json_object( 'old',OLD.Bookmark,  'new',NEW.Bookmark)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER DNATable_AuxChangeLogTable_update
    AFTER UPDATE ON DNATable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'DNATable',
            OLD.RecID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'ID1',  CASE WHEN OLD.ID1  IS DISTINCT FROM NEW.ID1   THEN json_object( 'old',OLD.ID1,  'new',NEW.ID1)   END,
              'ID2',  CASE WHEN OLD.ID2  IS DISTINCT FROM NEW.ID2   THEN json_object( 'old',OLD.ID2,  'new',NEW.ID2)   END,
              'Label1',  CASE WHEN OLD.Label1  IS DISTINCT FROM NEW.Label1   THEN json_object( 'old',OLD.Label1,  'new',NEW.Label1)   END,
              'Label2',  CASE WHEN OLD.Label2  IS DISTINCT FROM NEW.Label2   THEN json_object( 'old',OLD.Label2,  'new',NEW.Label2)   END,
              'DNAProvider',  CASE WHEN OLD.DNAProvider  IS DISTINCT FROM NEW.DNAProvider   THEN json_object( 'old',OLD.DNAProvider,  'new',NEW.DNAProvider)   END,
              'SharedCM',  CASE WHEN OLD.SharedCM  IS DISTINCT FROM NEW.SharedCM   THEN json_object( 'old',OLD.SharedCM,  'new',NEW.SharedCM)   END,
              'SharedPercent',  CASE WHEN OLD.SharedPercent  IS DISTINCT FROM NEW.SharedPercent   THEN json_object( 'old',OLD.SharedPercent,  'new',NEW.SharedPercent)   END,
              'LargeSeg',  CASE WHEN OLD.LargeSeg  IS DISTINCT FROM NEW.LargeSeg   THEN json_object( 'old',OLD.LargeSeg,  'new',NEW.LargeSeg)   END,
              'SharedSegs',  CASE WHEN OLD.SharedSegs  IS DISTINCT FROM NEW.SharedSegs   THEN json_object( 'old',OLD.SharedSegs,  'new',NEW.SharedSegs)   END,
              'Date',  CASE WHEN OLD.Date  IS DISTINCT FROM NEW.Date   THEN json_object( 'old',OLD.Date,  'new',NEW.Date)   END,
              'Relate1',  CASE WHEN OLD.Relate1  IS DISTINCT FROM NEW.Relate1   THEN json_object( 'old',OLD.Relate1,  'new',NEW.Relate1)   END,
              'Relate2',  CASE WHEN OLD.Relate2  IS DISTINCT FROM NEW.Relate2   THEN json_object( 'old',OLD.Relate2,  'new',NEW.Relate2)   END,
              'CommonAnc',  CASE WHEN OLD.CommonAnc  IS DISTINCT FROM NEW.CommonAnc   THEN json_object( 'old',OLD.CommonAnc,  'new',NEW.CommonAnc)   END,
              'CommonAncType',  CASE WHEN OLD.CommonAncType  IS DISTINCT FROM NEW.CommonAncType   THEN json_object( 'old',OLD.CommonAncType,  'new',NEW.CommonAncType)   END,
              'Verified',  CASE WHEN OLD.Verified  IS DISTINCT FROM NEW.Verified   THEN json_object( 'old',OLD.Verified,  'new',NEW.Verified)   END,
              'Note',  CASE WHEN OLD.Note  IS DISTINCT FROM NEW.Note   THEN json_object( 'old',OLD.Note,  'new',NEW.Note)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER AuxDNATable_AuxChangeLogTable_update
    AFTER UPDATE ON AuxDNATable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'AuxDNATable',
            OLD.AuxDNATableID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'Sort1',  CASE WHEN OLD.Sort1  IS DISTINCT FROM NEW.Sort1   THEN json_object( 'old',OLD.Sort1,  'new',NEW.Sort1)   END,
              'Sort2',  CASE WHEN OLD.Sort2  IS DISTINCT FROM NEW.Sort2   THEN json_object( 'old',OLD.Sort2,  'new',NEW.Sort2)   END,
              'Info',  CASE WHEN OLD.Info  IS DISTINCT FROM NEW.Info   THEN json_object( 'old',OLD.Info,  'new',NEW.Info)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    
    CREATE TRIGGER AuxMultimediaTable_AuxChangeLogTable_update
    AFTER UPDATE ON AuxMultimediaTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLogTable (tableName, RowID, ChangeTime, ChangesJSON)
      SELECT *
        FROM (
          SELECT
            'AuxMultimediaTable',
            OLD.AuxMediaID,
            julianday('now') - 2415018.5,
            json_patch('{}', json_object(
              'FileSize',  CASE WHEN OLD.FileSize  IS DISTINCT FROM NEW.FileSize   THEN json_object( 'old',OLD.FileSize,  'new',NEW.FileSize)   END,
              'FileTimeCreation',  CASE WHEN OLD.FileTimeCreation  IS DISTINCT FROM NEW.FileTimeCreation   THEN json_object( 'old',OLD.FileTimeCreation,  'new',NEW.FileTimeCreation)   END,
              'FileTimeModification',  CASE WHEN OLD.FileTimeModification  IS DISTINCT FROM NEW.FileTimeModification   THEN json_object( 'old',OLD.FileTimeModification,  'new',NEW.FileTimeModification)   END,
              'HashType',  CASE WHEN OLD.HashType  IS DISTINCT FROM NEW.HashType   THEN json_object( 'old',OLD.HashType,  'new',NEW.HashType)   END,
              'Hash',  CASE WHEN OLD.Hash  IS DISTINCT FROM NEW.Hash   THEN json_object( 'old',OLD.Hash,  'new',NEW.Hash)   END,
              'UTCModDate',  CASE WHEN OLD.UTCModDate  IS DISTINCT FROM NEW.UTCModDate   THEN json_object( 'old',OLD.UTCModDate,  'new',NEW.UTCModDate)   END
    ) ) AS DIFF
        ) AS t
        WHERE t.diff IS NOT NULL
          AND t.diff <> '{}';
    END;
    



    