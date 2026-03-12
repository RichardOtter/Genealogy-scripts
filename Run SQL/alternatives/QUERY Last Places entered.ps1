function Main {

    $db = "C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"

    $sql = @"
SELECT PlaceID, Name
FROM (
    SELECT PlaceID, Name COLLATE NOCASE
    FROM PlaceTable
    WHERE PlaceType = 0
    ORDER BY PlaceID DESC
    LIMIT 30
)
ORDER BY PlaceID ASC;
"@

    Write-Host "The last nn places entered into RM`n"

    $rows = Invoke-SqliteQuery -DataSource $db -Query $sql

    foreach ($row in $rows) {
        "{0,6}  {1}" -f $row.PlaceID, $row.Name
    }

    if (Launched-FromExplorer) {
        Read-Host "`nPress Enter to exit..."
    }
}

# run once-   Install-Module PSSQLite
Import-Module PSSQLite

function Launched-FromExplorer {
    return -not $Host.UI.RawUI.KeyAvailable
}

Main

