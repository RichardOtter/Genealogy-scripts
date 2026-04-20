-- Remove [] bracketed text from name table.

UPDATE NameTable
SET Surname = TRIM(regexp_replace(Surname, '\[[^]]*\]', ''))
WHERE Surname LIKE '%[%';

UPDATE NameTable
SET Given = TRIM(regexp_replace(Given, '\[[^]]*\]', ''))
WHERE Given LIKE '%[%';


UPDATE NameTable
SET Prefix = TRIM(regexp_replace(Prefix, '\[[^]]*\]', ''))
WHERE Prefix LIKE '%[%';


UPDATE NameTable
SET Suffix = TRIM(regexp_replace(Suffix, '\[[^]]*\]', ''))
WHERE Suffix LIKE '%[%';


UPDATE NameTable
SET Nickname = TRIM(regexp_replace(Nickname, '\[[^]]*\]', ''))
WHERE Nickname LIKE '%[%';
