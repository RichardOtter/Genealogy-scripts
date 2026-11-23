"""
Insert comprehensive test data into PlaceTable for RMNOCASE collation analysis.
This creates diverse Unicode test cases to understand RM's collation behavior.

The RMNOCASE implementation is an approximation, not the RootsMagic collation.
Close the database in RootsMagic before running this script. Use a disposable
test database and rebuild its indexes in RootsMagic after insertion.
"""

import sqlite3
import unicodedata

# Database path
DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\RMNOCASE RE\RM_12.0.0-win64 New-empty.rmtree"

# Comprehensive test data for RMNOCASE collation analysis
TEST_DATA = [
    # Basic ASCII - case variations
    "apple",
    "Apple",
    "APPLE",
    "apples",
    
    # Accented characters - same base letter, different accents
    "café",
    "Café",
    "CAFÉ",
    "cafe",
    "Cafe",
    
    # Various accented characters
    "naïve",
    "Naïve",
    "résumé",
    "Résumé",
    "zoë",
    "Zoë",
    
    # Other languages with diacritics
    "müller",
    "Müller",
    "MÜLLER",
    "muller",
    "Łódź",
    "łódź",
    "Åland",
    "åland",
    "Ångström",
    "ångström",
    "Ørsted",
    "ørsted",
    "Østersund",
    "østersund",
    
    # Special character combinations
    "O'Brien",
    "o'brien",
    "O'BRIEN",
    "obrien",
    "Smith-Jones",
    "smith-jones",
    "SMITH-JONES",
    "smithjones",
    
    # Numbers and ordinals
    "1st",
    "2nd",
    "3rd",
    "10th",
    "21st",
    "100th",
    "1",
    "2",
    "10",
    "21",
    "100",
    
    # Mixed case and accents
    "LjUbLjAnA",
    "LJUBLJANA",
    "ljubljana",
    "Ljubljana",
    
    # German umlauts
    "äöü",
    "ÄÖÜ",
    "aou",
    
    # French accents
    "àâäæéèêëïîôœùûüç",
    "ÀÂÄÆÉÈÊËÏÎÔŒÙÛÜÇ",
    
    # Spanish accents
    "áéíóú",
    "ÁÉÍÓÚ",
    
    # Portuguese
    "ãõ",
    "ÃÕ",
    
    # Scandinavian
    "ø",
    "Ø",
    "æ",
    "Æ",
    "å",
    "Å",
    
    # Polish
    "ł",
    "Ł",
    "ń",
    "Ń",
    "ś",
    "Ś",
    "ź",
    "Ź",
    "ż",
    "Ż",
    "ą",
    "Ą",
    "ę",
    "Ę",
    "ó",
    "Ó",
    
    # Duplicates with different normalization (combining marks vs precomposed)
    "é",  # precomposed U+00E9
    "e\u0301",  # e + combining acute U+0301
    
    # More complex examples
    "Montréal",
    "montreal",
    "MONTRÉAL",
    "Montreal",
    
    "Zürich",
    "zurich",
    "ZÜRICH",
    "Zurich",
    
    "München",
    "munchen",
    "MÜNCHEN",
    "Munchen",
    
    # Edge cases
    "",  # empty string
    " ",  # space
    "  ",  # multiple spaces
    "a",  # single character
    "A",
    
    # Numbers with letters
    "123abc",
    "abc123",
    "123ABC",
    "ABC123",
    
    # Special characters
    "@symbol",
    "#hash",
    "$dollar",
    "%percent",
    "&and",
    "*star",
    
    # Ligatures (if supported)
    "ﬁnale",  # fi ligature
    "finale",  # regular fi
    "ﬂoor",   # fl ligature
    "floor",  # regular fl
]

# RootsMagic 12 left these capital letters unchanged in the language probes.
ROOTSMAGIC_CASEFOLD_IDENTITY = frozenset(
    "\u1c89\ua7cb\ua7cc\ua7ce\ua7d2\ua7d4\ua7da\ua7dc"
)


def rmnocase_key(value):
    """Approximate the observed case- and accent-insensitive ordering."""
    folded = "".join(
        char if char in ROOTSMAGIC_CASEFOLD_IDENTITY else char.casefold()
        for char in value
    )
    return "".join(
        char for char in unicodedata.normalize("NFD", folded)
        if unicodedata.category(char) != "Mn"
    )


def rmnocase(a, b):
    """Compare using an approximation of RootsMagic's RMNOCASE."""
    a, b = rmnocase_key(a), rmnocase_key(b)
    return (a > b) - (a < b)


def insert_test_data():
    """Insert test data into PlaceTable."""
    conn = None
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        conn.create_collation("RMNOCASE", rmnocase)
        cursor = conn.cursor()
        
        print(f"Connected to database: {DB_PATH}")
        print("Close this database in RootsMagic before running the insert.")
        print("Using an approximate RMNOCASE; rebuild indexes in RootsMagic after insertion.")
        print(f"Inserting {len(TEST_DATA)} test records...\n")

        cursor.execute("BEGIN IMMEDIATE")
        cursor.execute("REINDEX RMNOCASE")
        
        # Insert each test place
        for idx, place_name in enumerate(TEST_DATA, 1):
            cursor.execute(
                """INSERT INTO PlaceTable
                   (PlaceType, Name, Abbrev, Normalized, Latitude, Longitude,
                    LatLongExact, MasterID, Note, Reverse, fsID, anID, UTCModDate)
                   VALUES (0, ?, '', '', 0, 0, 0, 0, '', ?, 0, 0,
                           julianday('now') - 2415018.5)""",
                (place_name, place_name)
            )
        
        conn.commit()
        print(f"Successfully inserted {len(TEST_DATA)} records.")
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM PlaceTable")
        total = cursor.fetchone()[0]
        print(f"Total records in PlaceTable: {total}")
        
        # Show first 20 records
        print("\nFirst 20 records as inserted:")
        cursor.execute("SELECT PlaceID, Name FROM PlaceTable LIMIT 20")
        for place_id, name in cursor.fetchall():
            print(f"  {place_id}: {name!r}")
        
        conn.close()
        conn = None
        print("\nDatabase closed.")
        print("\nNext steps:")
        print("1. Open the database in RootsMagic")
        print("2. Have RootsMagic 'Rebuild Indexes' (Tools > Database Tools)")
        print("3. Run query_sorted_data.py to see RM's sort order")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn is not None:
            conn.close()
    
    return True

if __name__ == "__main__":
    if not insert_test_data():
        raise SystemExit(1)
