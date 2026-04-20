-- Must rebuild indexes in RootsMagic afterward
-- Remove uncertain places first. This will remove their markers at the start of name.

REINDEX RMNOCASE;

-- Preview the changes
SELECT Name,
       TRIM(
           regexp_replace(
               regexp_replace(
                   regexp_replace(Name, ',?\s*\[[^]]*\]', ''),
                   '\s{2,}', ' '
               ),
               ',\s*,', ','
           )
       ) AS Cleaned
FROM PlaceTable
WHERE PlaceType = 0
  AND Name LIKE '%[%';


UPDATE PlaceTable
SET Name = TRIM(
              regexp_replace(
                  regexp_replace(
                      regexp_replace(Name, ',?\s*\[[^]]*\]', ''),  -- remove [text] and optional ", "
                      '\s{2,}', ' '                               -- collapse double spaces
                  ),
                  ',\s*,', ','                                   -- collapse weird commas if any
              )
          )
WHERE PlaceType = 0
  AND Name LIKE '%[%';
  

