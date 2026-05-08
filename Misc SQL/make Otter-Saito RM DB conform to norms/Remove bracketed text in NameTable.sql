-- Remove [] bracketed text from name table.
-- Must rebuild indexes in RootsMagic afterward
-- Remove uncertain places first. This will remove their markers at the start of name.

REINDEX RMNOCASE;

SELECT
    NameID,
    -- Surname
    Surname AS OldSurname,
    TRIM(regexp_replace(Surname, '\[[^]]*\]', '')) AS NewSurname,
    -- Given
    Given AS OldGiven,
    TRIM(regexp_replace(Given, '\[[^]]*\]', '')) AS NewGiven,
    -- Prefix
    Prefix AS OldPrefix,
    TRIM(regexp_replace(Prefix, '\[[^]]*\]', '')) AS NewPrefix,
    -- Suffix
    Suffix AS OldSuffix,
    TRIM(regexp_replace(Suffix, '\[[^]]*\]', '')) AS NewSuffix,
    -- Nickname
    Nickname AS OldNickname,
    TRIM(regexp_replace(Nickname, '\[[^]]*\]', '')) AS NewNickname
        -- SurnameMP
    SurnameMP AS OldSurnameMP,
    TRIM(regexp_replace(SurnameMP, '\[[^]]*\]', '')) AS NewSurnameMP
        -- GivenMP
    GivenMP AS OldGivenMP,
    TRIM(regexp_replace(GivenMP, '\[[^]]*\]', '')) AS NewGivenMP
        -- NicknameMP
    NicknameMP AS OldNicknameMP,
    TRIM(regexp_replace(NicknameMP, '\[[^]]*\]', '')) AS NewNicknameMP
FROM NameTable
WHERE
       (Surname    LIKE '%[%')
    OR (Given      LIKE '%[%')
    OR (Prefix     LIKE '%[%')
    OR (Suffix     LIKE '%[%')
    OR (Nickname   LIKE '%[%')
    OR (SurnameMP  LIKE '%[%')
    OR (GivenMP    LIKE '%[%')
    OR (NicknameMP LIKE '%[%');


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

UPDATE NameTable
SET SurnameMP = TRIM(regexp_replace(SurnameMP, '\[[^]]*\]', ''))
WHERE SurnameMP LIKE '%[%';

UPDATE NameTable
SET GivenMP = TRIM(regexp_replace(GivenMP, '\[[^]]*\]', ''))
WHERE GivenMP LIKE '%[%';

UPDATE NicknameMP
SET NicknameMP = TRIM(regexp_replace(NicknameMP, '\[[^]]*\]', ''))
WHERE NicknameMP LIKE '%[%';
