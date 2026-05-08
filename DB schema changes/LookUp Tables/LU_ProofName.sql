CREATE TABLE IF NOT EXISTS LU_ProofName (
    ProofID INTEGER PRIMARY KEY,
    ProofName TEXT NOT NULL
);

INSERT OR IGNORE INTO LU_ProofName (ProofID, ProofName) VALUES
  (0, "►unspecified◄"),
  (1, "Proven"),
  (2, "Disproven"),
  (3, "Disputed"),
  (4, "Proposed");
