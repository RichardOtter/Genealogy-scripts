--error repro

CREATE TABLE EventTable (EventID INTEGER PRIMARY KEY, EventType INTEGER, OwnerType INTEGER, OwnerID INTEGER, FamilyID INTEGER, PlaceID INTEGER, SiteID INTEGER, Date TEXT, SortDate BIGINT, IsPrimary INTEGER, IsPrivate INTEGER, Proof INTEGER, Status INTEGER, Sentence TEXT, Details TEXT, Note TEXT, UTCModDate FLOAT );

CREATE INDEX idxOwnerEvent ON EventTable (OwnerID,EventType);

CREATE INDEX idxOwnerDate ON EventTable (OwnerID,SortDate);


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
    
