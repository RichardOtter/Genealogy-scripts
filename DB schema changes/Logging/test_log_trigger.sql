

CREATE TABLE IF NOT EXISTS AuxChangeLog (
    ChangeLogID INTEGER PRIMARY KEY,
    TableName TEXT NOT NULL,
    RowID INTEGER NOT NULL,
    ChangeTime REAL NOT NULL,
    ChangesJSON TEXT NOT NULL
);

drop TRIGGER IF EXISTS EventTable_AuxLogUpdate;


    CREATE TRIGGER EventTable_AuxLogUpdate
    AFTER UPDATE ON EventTable
    FOR EACH ROW
    BEGIN
      INSERT INTO AuxChangeLog (tableName, RowID, ChangeTime, ChangesJSON)
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
    



update EventTable
set ownertype = 997
where eventid = 3;

update EventTable
set ownertype = 996
where eventid = 3;

SELECT * from AuxChangeLog;


--C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\Logging>sqlite3 "../DB/TEST-DB schema changes.rmtree" < event_trigger.sql
--1|tEST tABLE|111|1111.0|222
--2|EventTable|2|46056.0233837618|{"EventType":null,"OwnerType":null,"OwnerID":null,"FamilyID":null,"PlaceID":null,"SiteID":null,"Date":null,"SortDate":null,"IsPrimary":null,"IsPrivate":null,"Proof":null,"Status":null,"Sentence":null,"Details":null,"Note":null,"UTCModDate":null}

