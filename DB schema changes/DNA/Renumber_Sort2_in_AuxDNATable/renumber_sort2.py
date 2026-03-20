import sqlite3

#  Add error checking for locked DB
# assume from from explorer, so pause at end and give summary


def main():
    # DB_path = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\DB schema changes\DNA\Renumber_Sort2_in_AuxDNATable\DB\TEST-Renumber_Sort2_in_AuxDNATable.rmtree"
    DB_path= r"\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"


    #  | 23andme        | 1   |
    #  | Ancestry       | 2   |
    #  | MyHeritage     | 5   |

    # 17 Roman, 4 Rose, 1 RJO, 6 GCS, 12 EAI, 1530 TSC

    #   Ancestry-   Everyone = RJO, RHO, RJM, GCS, EAI, TSC
    #   23andMe-    Only RJO & GCS
    #   MyHeritage- Only RJO, RHO, RJM

    #  tuples are (PersonID, DNAProviderID)
    
    combos = [
    (1,  2),
    (17, 2),
    (4,  2),
    (6,  2),
    (12, 2),
    (1530, 2),

    (1,  5),
    (17, 5),
    (4,  5),

    (1, 1),
    (6, 1)
    ]

    # Example usage:
    # renumber_sort2("mydatabase.sqlite", combos)

    renumber_sort2(DB_path, combos)
    

    input("\n\n\nHit enter to close window")

# ===================================================DIV60==
def renumber_sort2(db_path, combos):
    sql = """
    WITH qualified AS (
        SELECT
            adt.AuxDNATableID,
            adt.Sort1,
            adt.Sort2,
            ROW_NUMBER() OVER (
                PARTITION BY adt.Sort1
                ORDER BY adt.Sort1 DESC, adt.Sort2 ASC, adt.AuxDNATableID ASC
            ) AS rn
        FROM AuxDNATable adt
        JOIN DNATable d ON d.RecID = adt.AuxDNATableID
        WHERE d.ID1 = ?
          AND d.DNAProvider = ?
    )
    UPDATE AuxDNATable
    SET Sort2 = (
        SELECT rn * 10
        FROM qualified
        WHERE qualified.AuxDNATableID = AuxDNATable.AuxDNATableID
    )
    WHERE AuxDNATableID IN (SELECT AuxDNATableID FROM qualified);
    """

    print (db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    for matcher, provider in combos:
        print(f"Processing ID1={matcher}, DNAProvider={provider}...")
        cur.execute(sql, (matcher, provider))
        conn.commit()
        print("  Done.")

    conn.close()
    print("All renumbering operations completed.")

# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==