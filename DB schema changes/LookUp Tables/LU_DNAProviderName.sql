CREATE TABLE LU_DNAProviderName (
    DNAProviderID INTEGER PRIMARY KEY,
    DNAProviderName TEXT NOT NULL
);

INSERT INTO LU_DNAProviderName (DNAProviderID, DNAProviderName) VALUES
  (0, "►unspecified◄"),
  (1, "23andme"),
  (2, "Ancestry"),
  (3, "FamilyTree DNA"),
  (4, "Living DNA"),
  (5, "MyHeritage"),
  (6, "GEDmatch"),
  (998, "Unknown"),
  (999. "Other");