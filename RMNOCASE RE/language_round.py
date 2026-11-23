"""Prepare and read a disposable RootsMagic collation experiment."""

import argparse
import json
import shutil
import sqlite3
import unicodedata
from collections import Counter
from contextlib import closing
from pathlib import Path

from insert_test_data import rmnocase, rmnocase_key
from query_sorted_data import INDEX_QUERY


FOLDER = Path(__file__).resolve().parent
SOURCE = FOLDER / "RM_12.0.0-win64 New-empty.rmtree"
DATABASE = FOLDER / "rmnocase-language-tests.rmtree"
PLAN = FOLDER / "rmnocase-language-plan.json"
OBSERVATIONS = FOLDER / "rmnocase-language-observations.json"
CONTROL = ("zzrmnocase-control/a", "zzrmnocase-control/b")
UNICODE_VERSION = "17.0.0"


def character_groups():
    if unicodedata.unidata_version != UNICODE_VERSION:
        raise RuntimeError(f"Python must use Unicode {UNICODE_VERSION}")
    groups = {name: [] for name in ("LATIN", "CYRILLIC", "GREEK", "JAPANESE")}
    for codepoint in range(0x110000):
        char = chr(codepoint)
        if not unicodedata.category(char).startswith("L"):
            continue
        name = unicodedata.name(char, "")
        for script in ("LATIN", "CYRILLIC", "GREEK"):
            if name.startswith(script + " "):
                groups[script].append(char)
                break
        if (
            0x3040 <= codepoint <= 0x30FF
            or 0x31F0 <= codepoint <= 0x31FF
            or 0x3400 <= codepoint <= 0x9FFF
            or 0xF900 <= codepoint <= 0xFAFF
            or 0xFF66 <= codepoint <= 0xFF9D
            or 0x2F800 <= codepoint <= 0x2FA1F
            or codepoint == 0x20BB7
        ):
            groups["JAPANESE"].append(char)
    return groups


def make_cases(groups):
    cases = []
    seen = set()

    def add(group, kind, a, b):
        if a != b and (a, b) not in seen:
            seen.add((a, b))
            cases.append([group, kind, a, b])

    for group, chars in groups.items():
        for previous, char in zip(chars, chars[1:]):
            add(group, "adjacent", previous, char)
        for char in chars:
            for kind, other in (
                ("casefold", char.casefold()),
                ("uppercase", char.upper()),
                ("decomposed", unicodedata.normalize("NFD", char)),
                ("unmarked", rmnocase_key(char)),
            ):
                add(group, kind, char, other)

    for a, b in (
        ("O'Brien", "O’Brien"), ("Smith-Jones", "Smith Jones"),
        ("Łódź", "Lodz"), ("Müller", "Mueller"), ("Москва", "МОСКВА"),
        ("Αθήνα", "ΑΘΗΝΑ"), ("か", "が"), ("は", "ぱ"),
        ("か", "カ"), ("カ", "ｶ"), ("ｶﾞ", "ガ"),
        ("高", "髙"), ("吉", "𠮷"), ("東京", "とうきょう"),
        ("大阪", "おおさか"), ("斉藤", "齋藤"), ("山田", "山﨑"),
    ):
        add("NAMES", "example", a, b)
    return cases


def index_order(conn):
    details = [row[3].upper() for row in conn.execute("EXPLAIN QUERY PLAN " + INDEX_QUERY)]
    if not any("IDXPLACENAME" in detail for detail in details) or any(
        "TEMP B-TREE" in detail for detail in details
    ):
        raise RuntimeError(f"Index-order query is unsafe: {details}")
    return [row[0] for row in conn.execute(INDEX_QUERY)]


def decode_order(ids, positions):
    try:
        order = tuple(sorted(range(4), key=lambda index: positions[ids[index]]))
    except KeyError as exc:
        raise RuntimeError(f"Missing test row {exc.args[0]}") from exc
    outcomes = {(0, 1, 2, 3): 0, (0, 3, 1, 2): -1, (1, 2, 0, 3): 1}
    if order not in outcomes:
        raise RuntimeError(f"Unexpected pair order for IDs {ids}: {order}")
    return outcomes[order]


def prepare():
    for path in (DATABASE, PLAN, OBSERVATIONS):
        if path.exists():
            raise FileExistsError(f"Will not overwrite {path}")
    cases = make_cases(character_groups())
    shutil.copyfile(SOURCE, DATABASE)
    with closing(sqlite3.connect(DATABASE)) as conn:
        conn.create_collation("RMNOCASE", rmnocase)
        if conn.execute("SELECT COUNT(*) FROM PlaceTable WHERE PlaceType=0").fetchone()[0]:
            raise RuntimeError("The supplied database is not empty of ordinary places")
        for (name, reverse) in conn.execute("SELECT Name, Reverse FROM PlaceTable"):
            if any(value and value.casefold().startswith("zzrmnocase-control/") for value in (name, reverse)):
                raise RuntimeError("Control prefix already occurs in the source database")
        conn.execute("PRAGMA temp_store=MEMORY")
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("REINDEX RMNOCASE")
        next_id = conn.execute("SELECT COALESCE(MAX(PlaceID), 0) + 1 FROM PlaceTable").fetchone()[0]
        first_id = next_id
        rows = []
        for index, (_, _, a, b) in enumerate(cases):
            prefix = f"case{index:06d}/"
            for value in (a, b, b, a):
                rows.append((next_id, prefix + value, prefix + value))
                next_id += 1
        control_ids = list(range(next_id, next_id + 4))
        for value in (CONTROL[0], CONTROL[1], CONTROL[1], CONTROL[0]):
            rows.append((next_id, value, value))
            next_id += 1
        conn.executemany(
            """INSERT INTO PlaceTable
               (PlaceID, PlaceType, Name, Abbrev, Normalized, Latitude, Longitude,
                LatLongExact, MasterID, Note, Reverse, fsID, anID, UTCModDate)
               VALUES (?, 0, ?, '', '', 0, 0, 0, 0, '', ?, 0, 0,
                       julianday('now') - 2415018.5)""",
            rows,
        )
        conn.commit()

        def reverse_control(a, b):
            if a in CONTROL and b in CONTROL:
                return -rmnocase(a, b)
            return rmnocase(a, b)

        conn.create_collation("RMNOCASE", reverse_control)
        conn.execute("REINDEX RMNOCASE")
        conn.commit()
        positions = {place_id: index for index, place_id in enumerate(index_order(conn))}
        if decode_order(control_ids, positions) != 1:
            raise RuntimeError("The deliberately reversed control was not installed")
    plan = {
        "unicode_version": UNICODE_VERSION,
        "first_id": first_id,
        "control_ids": control_ids,
        "cases": cases,
    }
    with PLAN.open("x", encoding="utf-8", newline="\n") as file:
        json.dump(plan, file, ensure_ascii=True, separators=(",", ":"))
        file.write("\n")
    print(f"Prepared {len(cases):,} pairs and {len(rows):,} rows in {DATABASE.name}.")
    print("The control is reversed; rebuild indexes in RootsMagic before analysis.")


def analyze():
    if OBSERVATIONS.exists():
        raise FileExistsError(f"Will not overwrite {OBSERVATIONS}")
    with PLAN.open(encoding="utf-8") as file:
        plan = json.load(file)
    with closing(sqlite3.connect(DATABASE.as_uri() + "?mode=ro", uri=True)) as conn:
        conn.create_collation("RMNOCASE", rmnocase)
        positions = {place_id: index for index, place_id in enumerate(index_order(conn))}
    if decode_order(plan["control_ids"], positions) != -1:
        raise RuntimeError("RootsMagic did not restore the reversed control; rebuild indexes first")
    observations = []
    mismatches = []
    groups = Counter()
    for index, (group, kind, a, b) in enumerate(plan["cases"]):
        first = plan["first_id"] + 4 * index
        observed = decode_order(range(first, first + 4), positions)
        prefix = f"case{index:06d}/"
        predicted = rmnocase(prefix + a, prefix + b)
        observations.append([group, kind, a, b, observed])
        groups[group] += 1
        if observed != predicted:
            mismatches.append((group, kind, a, b, observed, predicted))
    with OBSERVATIONS.open("x", encoding="utf-8", newline="\n") as file:
        json.dump(
            {"unicode_version": plan["unicode_version"], "pairs": observations},
            file, ensure_ascii=True, separators=(",", ":"),
        )
        file.write("\n")
    print(f"Verified the rebuild control and recorded {len(observations):,} pairs.")
    print("Pairs by group:", dict(groups))
    print(f"Mismatches: {len(mismatches):,}")
    for mismatch in mismatches[:30]:
        print(repr(mismatch))
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "analyze"))
    args = parser.parse_args()
    {"prepare": prepare, "analyze": analyze}[args.action]()
