CREATE TABLE IF NOT EXISTS LU_FatherLabel (
    FatherLabelID INTEGER PRIMARY KEY,
    FatherLabel TEXT NOT NULL
);

INSERT OR IGNORE INTO LU_FatherLabel (FatherLabelID, FatherLabel) VALUES
  (0, "Father"),
  (1, "Husband"),
  (2, "Partner"),
  (3, "Other");
