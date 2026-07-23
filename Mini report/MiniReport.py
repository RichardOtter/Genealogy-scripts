#!/usr/bin/env python3
import sqlite3
import pyperclip
import re
from datetime import datetime

# ------------------------------------------------------------
# Hard‑coded RM database path
# ------------------------------------------------------------
DBPath = r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"

# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def format_rm_date(raw):
    """
    RM date example formats:
      D.+19550925..+00000000..  -> 25 Sep 1955
      D.+19500200..+00000000..  -> Feb 1950
      D.+19500000..+00000000..  -> 1950
      D.+00000000..+00000000..  -> ""
    """
    if not raw:
        return ""

    m = re.search(r"(\d{8})", raw)
    if not m:
        return raw

    ymd = m.group(1)
    year = int(ymd[0:4])
    month = int(ymd[4:6])
    day = int(ymd[6:8])

    # Year missing → nothing meaningful
    if year == 0:
        return ""

    # Month missing → year only
    if month == 0:
        return f"{year}"

    # Day missing → month + year
    if day == 0:
        try:
            dt = datetime(year, month, 1)
            return dt.strftime("%b %Y")
        except ValueError:
            return f"{year}"

    # Full date
    try:
        dt = datetime(year, month, day)
        return dt.strftime("%d %b %Y")
    except ValueError:
        # Fallback: partial formatting
        return f"{year}"

def get_primary_name(conn, person_id):
    cur = conn.execute("""
        SELECT Given, Surname
        FROM NameTable
        WHERE OwnerID = ?
          AND IsPrimary = 1
        LIMIT 1;
    """, (person_id,))
    row = cur.fetchone()
    if row:
        return row[0] or "", row[1] or ""
    return "", ""

def get_birth_death(conn, person_id):
    cur = conn.execute("""
        SELECT EventType, Date
        FROM EventTable
        WHERE OwnerType = 0
          AND OwnerID = ?
          AND (EventType = 1 OR EventType = 2);
    """, (person_id,))
    birth = ""
    death = ""
    for etype, date in cur.fetchall():
        if etype == 1:
            birth = format_rm_date(date or "")
        elif etype == 2:
            death = format_rm_date(date or "")
    return birth, death

def get_parents(conn, person_id):
    cur = conn.execute("""
        SELECT FamilyID
        FROM ChildTable
        WHERE ChildID = ?
        LIMIT 1;
    """, (person_id,))
    row = cur.fetchone()
    if not row:
        return None, None

    family_id = row[0]

    cur = conn.execute("""
        SELECT FatherID, MotherID
        FROM FamilyTable
        WHERE FamilyID = ?
        LIMIT 1;
    """, (family_id,))
    row = cur.fetchone()
    if row:
        return row[0], row[1]
    return None, None

def get_sex_word(conn, person_id):
    """
    Use LU_SexType to determine 'son' or 'daughter'.
    """
    cur = conn.execute("SELECT Sex FROM PersonTable WHERE PersonID = ?", (person_id,))
    row = cur.fetchone()
    if not row:
        return "child"

    sex_id = row[0]
    cur = conn.execute("SELECT SexType FROM LU_SexType WHERE SexID = ?", (sex_id,))
    row = cur.fetchone()
    if not row or not row[0]:
        return "child"

    sex_type = row[0].strip().lower()
    if sex_type.startswith("m"):
        return "son"
    elif sex_type.startswith("f"):
        return "daughter"
    return "child"

# ------------------------------------------------------------
# Main report generator
# ------------------------------------------------------------

def generate_report(conn, person_id):
    given, surname = get_primary_name(conn, person_id)
    birth, death = get_birth_death(conn, person_id)
    father_id, mother_id = get_parents(conn, person_id)

    father_name = ""
    mother_name = ""

    if father_id:
        fg, fs = get_primary_name(conn, father_id)
        father_name = f"{fg} {fs}".strip()

    if mother_id:
        mg, ms = get_primary_name(conn, mother_id)
        mother_name = f"{mg} {ms}".strip()

    relation_word = get_sex_word(conn, person_id)

    # Line 1
    line1 = f"{given} {surname}".strip()
    if birth or death:
        line1 += " "
        if birth:
            line1 += f"-b {birth}"
        if birth and death:
            line1 += ", "
        if death:
            line1 += f"-d {death}"
        line1 += ""

    # Line 2
    if father_name or mother_name:
        if father_name and mother_name:
            line2 = f"{relation_word} of {father_name} and {mother_name}"
        elif father_name:
            line2 = f"{relation_word} of {father_name}"
        else:
            line2 = f"{relation_word} of {mother_name}"
    else:
        line2 = ""

    return f"{line1}\n{line2}"

# ------------------------------------------------------------
# Entry point (double‑click friendly)
# ------------------------------------------------------------

def main():
    person_id = int(input("Enter PersonID: ").strip())

    conn = sqlite3.connect(DBPath)
    report = generate_report(conn, person_id)
    conn.close()

    pyperclip.copy(report)
    print("\nMini-report copied to clipboard:\n")
    print(report)

if __name__ == "__main__":
    main()
