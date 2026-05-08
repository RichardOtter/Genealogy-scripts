CREATE TABLE IF NOT EXISTS LU_SexType (
    SexID INTEGER PRIMARY KEY,
    SexType TEXT NOT NULL
);

INSERT OR IGNORE INTO LU_SexType (SexID, SexType) VALUES
  (0, "Male"),
  (1, "Female"),
  (2, "►unknown◄");
