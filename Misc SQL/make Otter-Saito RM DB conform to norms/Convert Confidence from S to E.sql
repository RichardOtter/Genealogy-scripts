-- Convert the Confidence indicator in RM Dates from Say to Est
-- Used to create a reporting database compatible with GEDCOM 5.1
-- Not desirable for normal RM use because
-- "Say" dates are not the same as "Est" dates.
-- Six tables have a Date column

UPDATE EventTable
SET "Date" =
      -- position 13 replacement
      SUBSTR("Date", 1, 12) ||
      CASE WHEN SUBSTR("Date", 13, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 13, 1) END ||
      SUBSTR("Date", 14, 10) ||
      -- position 24 replacement
      CASE WHEN SUBSTR("Date", 24, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 24, 1) END
WHERE SUBSTR("Date", 1, 1) IN ('D','Q','R')
  AND (SUBSTR("Date", 13, 1) = 'S'
       OR SUBSTR("Date", 24, 1) = 'S');

UPDATE NameTable
SET "Date" =
      -- position 13 replacement
      SUBSTR("Date", 1, 12) ||
      CASE WHEN SUBSTR("Date", 13, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 13, 1) END ||
      SUBSTR("Date", 14, 10) ||
      -- position 24 replacement
      CASE WHEN SUBSTR("Date", 24, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 24, 1) END
WHERE SUBSTR("Date", 1, 1) IN ('D','Q','R')
  AND (SUBSTR("Date", 13, 1) = 'S'
       OR SUBSTR("Date", 24, 1) = 'S');

UPDATE MultimediaTable
SET "Date" =
      -- position 13 replacement
      SUBSTR("Date", 1, 12) ||
      CASE WHEN SUBSTR("Date", 13, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 13, 1) END ||
      SUBSTR("Date", 14, 10) ||
      -- position 24 replacement
      CASE WHEN SUBSTR("Date", 24, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 24, 1) END
WHERE SUBSTR("Date", 1, 1) IN ('D','Q','R')
  AND (SUBSTR("Date", 13, 1) = 'S'
       OR SUBSTR("Date", 24, 1) = 'S');

UPDATE FANTable
SET "Date" =
      -- position 13 replacement
      SUBSTR("Date", 1, 12) ||
      CASE WHEN SUBSTR("Date", 13, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 13, 1) END ||
      SUBSTR("Date", 14, 10) ||
      -- position 24 replacement
      CASE WHEN SUBSTR("Date", 24, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 24, 1) END
WHERE SUBSTR("Date", 1, 1) IN ('D','Q','R')
  AND (SUBSTR("Date", 13, 1) = 'S'
       OR SUBSTR("Date", 24, 1) = 'S');

UPDATE DNATable
SET "Date" =
      -- position 13 replacement
      SUBSTR("Date", 1, 12) ||
      CASE WHEN SUBSTR("Date", 13, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 13, 1) END ||
      SUBSTR("Date", 14, 10) ||
      -- position 24 replacement
      CASE WHEN SUBSTR("Date", 24, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 24, 1) END
WHERE SUBSTR("Date", 1, 1) IN ('D','Q','R')
  AND (SUBSTR("Date", 13, 1) = 'S'
       OR SUBSTR("Date", 24, 1) = 'S');

UPDATE HealthTable
SET "Date" =
      -- position 13 replacement
      SUBSTR("Date", 1, 12) ||
      CASE WHEN SUBSTR("Date", 13, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 13, 1) END ||
      SUBSTR("Date", 14, 10) ||
      -- position 24 replacement
      CASE WHEN SUBSTR("Date", 24, 1) = 'S' THEN 'E' ELSE SUBSTR("Date", 24, 1) END
WHERE SUBSTR("Date", 1, 1) IN ('D','Q','R')
  AND (SUBSTR("Date", 13, 1) = 'S'
       OR SUBSTR("Date", 24, 1) = 'S');

-- END
