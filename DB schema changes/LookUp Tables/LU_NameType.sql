CREATE TABLE LU_NameType (
    NameTypeID INTEGER PRIMARY KEY,
    NameType TEXT NOT NULL
);

INSERT INTO LU_NameType (NameTypeID, NameType) VALUES
  (0, "►unspecified◄"),
  (1, "AKA"),
  (2, "Birth"),
  (3, "Immigrant"),
  (4, "Maiden"),
  (5, "Married"),
  (6, "Nickname"),
  (7, "Other Spelling");