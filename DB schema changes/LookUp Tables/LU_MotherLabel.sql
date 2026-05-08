CREATE TABLE IF NOT EXISTS LU_MotherLabel (
    MotherLabelID INTEGER PRIMARY KEY,
    MotherLabel TEXT NOT NULL
);

INSERT OR IGNORE INTO LU_MotherLabel (MotherLabelID, MotherLabel) VALUES
  (0, "Mother"),
  (1, "Wife"),
  (2, "Partner"),
  (3, "Other");
