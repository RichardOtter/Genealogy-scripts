
-- create table for logging data
CREATE TABLE AuxChangeLogTable (
    ChangeLogID INTEGER PRIMARY KEY,
    TableName TEXT NOT NULL,
    RowID INTEGER NOT NULL,
    ChangeTime REAL NOT NULL,
    ChangesJSON TEXT NOT NULL
);

-- create triggers on the tables to monitor
CREATE TRIGGER PersonTable_AuxChangeLogTable_update
AFTER UPDATE ON PersonTable
FOR EACH ROW
BEGIN
    INSERT INTO ChangeLog (TableName, RowID, ChangeTime, ChangesJSON)
    SELECT
        'PersonTable',
        OLD.PersonID,
        julianday('now') - 2415018.5,
        json_object(
            /* Only include keys when values changed */
            'Given',    CASE WHEN OLD.Given    <> NEW.Given    THEN NEW.Given    END,
            'Surname',  CASE WHEN OLD.Surname  <> NEW.Surname  THEN NEW.Surname  END,
            'BirthYear',CASE WHEN OLD.BirthYear<> NEW.BirthYear THEN NEW.BirthYear END
        )
    WHERE
        /* Only insert a log row if something actually changed */
        OLD.Given     <> NEW.Given
        OR OLD.Surname  <> NEW.Surname
        OR OLD.BirthYear<> NEW.BirthYear;
END;

-- or

drop TRIGGER EventTable_AuxChangeLogTable;

CREATE TRIGGER EventTable_AuxChangeLogTable
AFTER UPDATE ON EventTable
FOR EACH ROW
BEGIN
    INSERT INTO AuxChangeLog (TableName, RowID, ChangeTime, ChangesJSON)
    VALUES (
        'EventTable',
        OLD.EventID,
        julianday('now') - 2415018.5,
        json_object(
            'EventType',   NEW.EventType,
            'OwnerType',   NEW.OwnerType,
            'OwnerID',     NEW.OwnerID,
            'FamilyID',    NEW.FamilyID,
            'PlaceID',     NEW.PlaceID,
            'SiteID',      NEW.SiteID,
            'Date',        NEW."Date",
            'SortDate',    NEW.SortDate,
            'IsPrimary',   NEW.IsPrimary,
            'IsPrivate',   NEW.IsPrivate,
            'Proof',       NEW.Proof,
            'Status',      NEW.Status,
            'Sentence',    NEW.Sentence,
            'Details',     NEW.Details,
            'Note',        NEW.Note,
            'UTCModDate',  NEW.UTCModDate
        )
    );
END;