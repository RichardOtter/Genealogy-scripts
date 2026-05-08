-- Added for reference only.
-- Will never be used directly in SQL.

CREATE TABLE IF NOT EXISTS LU_FKeyTarget (
    OwnerTypeID INTEGER PRIMARY KEY,
    FKeyTargetTable TEXT NOT NULL,
    FKeyTargetColumn TEXT NOT NULL
);

INSERT OR IGNORE INTO LU_FKeyTarget 
(OwnerTypeID, FKeyTargetTable, FKeyTargetColumn) VALUES
  (  0, "PersonTable",        "PersonID"),
  (  1, "FamilyTable",        "FamilyID"),
  (  2, "EventTable",         "EventID"),
  (  3, "SourceTable",        "SourceID"),
  (  4, "CitationTable",      "CitationID"),
  (  5, "PlaceTable",         "PlaceID"),
  (  6, "TaskTable",          "TaskID"),
  (  7, "NameTable",          "NameID"),
  (  8, "►nothing◄",          ""),
  ( 14, "PlaceTable",         "PlaceID"), -- place detail
  ( 15, "",                   ""),        -- not used in RM v>7
  ( 18, "Task Folder",        "TODO"),
  ( 19, "FANTable",           "FanID"),
  ( 20, "TagTable.TagValue",  "GroupTable.GroupID");  --TODO

