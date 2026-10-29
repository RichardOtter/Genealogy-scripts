

@echo off

if not exist "validation-output" mkdir "validation-output"

py cemetery_file_validator.py "C:\Users\rotter\Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave\DE, Bayern, Main-Spessart\Waldzell\Friedhof Waldzell - Grave List.txt" >"validation-output\out-Waldzell.txt"

py cemetery_file_validator.py "C:\Users\rotter\Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave\DE, Bayern, Schweinfurt\Oberschwarzach\Friedhof Oberschwarzach - Grave List.txt" >"validation-output\out-Oberschwarzach.txt"


py cemetery_file_validator.py "C:\Users\rotter\Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave\DE, Bayern, Main-Spessart\Hausen\Friedhof Hausen - Grave List.txt" >"validation-output\out-Hausen.txt"

py cemetery_file_validator.py "C:\Users\rotter\Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave\DE, Bayern, Main-Spessart\Unknown\Friedhof Unknown - Grave List.txt" >"validation-output\out-unknown.txt"

py cemetery_file_validator.py "C:\Users\rotter\Genealogy\GeneDB\RM_LinkedFiles\Sources\Grave\DE, Bayern, Main-Spessart\Urspringen\Friedhof Urspringen - Grave List.txt" >"validation-output\out-Urspringen.txt"
