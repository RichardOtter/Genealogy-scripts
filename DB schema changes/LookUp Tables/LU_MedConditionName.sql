CREATE TABLE IF NOT EXISTS LU_MedConditionName (
    MedConditionNameID INTEGER PRIMARY KEY,
    MedConditionName TEXT NOT NULL
);

INSERT OR IGNORE INTO LU_MedConditionName (MedConditionNameID, MedConditionName) VALUES
  (   5, "Cancer"),
  (  12, "Cardiovascular"),
  (  17, "Congenital anomalies"),
  (   7, "Diabetes"),
  (  13, "Digestive diseases"),
  (  11, "Ear condition"),
  (   6, "Endocrine, blood, and immune disorders"),
  (  10, "Eye conditions"),
  (   1, "Infections and parasitic disease"),
  (  20, "Injuries and accidents"),
  (   8, "Mental health"),
  (  16, "Musculoskeletal diseases"),
  (   9, "Neurological"),
  (   4, "Nutritional deficiency"),
  (  18, "Oral disease"),
  (  14, "Renal and Urogenital"),
  (   3, "Reproductive health and childbirth"),
  (   2, "Respiratory disease"),
  (  19, "Sexual health"),
  (  15, "Skin disease"),
  ( 999, "Other");