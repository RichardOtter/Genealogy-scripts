CREATE TRIGGER EventTable_AuxLogUpdate
AFTER UPDATE ON EventTable
FOR EACH ROW
BEGIN
    INSERT INTO AuxChangeLog (TableName, RowID, ChangeTime, ChangesJSON)
    SELECT
        'EventTable',
        OLD.EventID,
        julianday('now') - 2415018.5,

        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
        json_patch(
            '{}',

            CASE WHEN CAST(OLD.EventType AS TEXT) <> CAST(NEW.EventType AS TEXT)
                 THEN json_object('EventType', json_object('old', OLD.EventType, 'new', NEW.EventType))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.OwnerType AS TEXT) <> CAST(NEW.OwnerType AS TEXT)
                 THEN json_object('OwnerType', json_object('old', OLD.OwnerType, 'new', NEW.OwnerType))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.OwnerID AS TEXT) <> CAST(NEW.OwnerID AS TEXT)
                 THEN json_object('OwnerID', json_object('old', OLD.OwnerID, 'new', NEW.OwnerID))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.FamilyID AS TEXT) <> CAST(NEW.FamilyID AS TEXT)
                 THEN json_object('FamilyID', json_object('old', OLD.FamilyID, 'new', NEW.FamilyID))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.PlaceID AS TEXT) <> CAST(NEW.PlaceID AS TEXT)
                 THEN json_object('PlaceID', json_object('old', OLD.PlaceID, 'new', NEW.PlaceID))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.SiteID AS TEXT) <> CAST(NEW.SiteID AS TEXT)
                 THEN json_object('SiteID', json_object('old', OLD.SiteID, 'new', NEW.SiteID))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD."Date" AS TEXT) <> CAST(NEW."Date" AS TEXT)
                 THEN json_object('Date', json_object('old', OLD."Date", 'new', NEW."Date"))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.SortDate AS TEXT) <> CAST(NEW.SortDate AS TEXT)
                 THEN json_object('SortDate', json_object('old', OLD.SortDate, 'new', NEW.SortDate))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.IsPrimary AS TEXT) <> CAST(NEW.IsPrimary AS TEXT)
                 THEN json_object('IsPrimary', json_object('old', OLD.IsPrimary, 'new', NEW.IsPrimary))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.IsPrivate AS TEXT) <> CAST(NEW.IsPrivate AS TEXT)
                 THEN json_object('IsPrivate', json_object('old', OLD.IsPrivate, 'new', NEW.IsPrivate))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.Proof AS TEXT) <> CAST(NEW.Proof AS TEXT)
                 THEN json_object('Proof', json_object('old', OLD.Proof, 'new', NEW.Proof))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.Status AS TEXT) <> CAST(NEW.Status AS TEXT)
                 THEN json_object('Status', json_object('old', OLD.Status, 'new', NEW.Status))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.Sentence AS TEXT) <> CAST(NEW.Sentence AS TEXT)
                 THEN json_object('Sentence', json_object('old', OLD.Sentence, 'new', NEW.Sentence))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.Details AS TEXT) <> CAST(NEW.Details AS TEXT)
                 THEN json_object('Details', json_object('old', OLD.Details, 'new', NEW.Details))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.Note AS TEXT) <> CAST(NEW.Note AS TEXT)
                 THEN json_object('Note', json_object('old', OLD.Note, 'new', NEW.Note))
                 ELSE '{}' END
        ),
            CASE WHEN CAST(OLD.UTCModDate AS TEXT) <> CAST(NEW.UTCModDate AS TEXT)
                 THEN json_object('UTCModDate', json_object('old', OLD.UTCModDate, 'new', NEW.UTCModDate))
                 ELSE '{}' END
        )
     AS diff

    WHERE diff <> '{}';
END;
