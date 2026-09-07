BEGIN TRANSACTION;

UPDATE AuxPlaceTable
SET Uncertain = CASE
  WHEN INSTR(UPPER(Orig_Name), 'VICINITY') > 0 THEN '_VICINITY'
  WHEN INSTR(UPPER(Orig_Name), 'REGION') > 0 THEN '_REGION'
  WHEN INSTR(Orig_Name, '~|') > 0 THEN '_EITHER'
  WHEN INSTR(Orig_Name, '~') > 0 THEN '_PROBABLY'
  WHEN INSTR(Orig_Name, '?') > 0 THEN '_UNCLEAR'
  WHEN INSTR(Orig_Name, '=') > 0 THEN '_NON-STD-PLACE'
    ELSE Uncertain
END
WHERE NULLIF(TRIM(Uncertain), '') IS NULL
  AND (
      INSTR(UPPER(Orig_Name), 'VICINITY') > 0
      OR INSTR(UPPER(Orig_Name), 'REGION') > 0
      OR INSTR(Orig_Name, '~') > 0
      OR INSTR(Orig_Name, '?') > 0
      OR INSTR(Orig_Name, '=') > 0
  );

COMMIT;
