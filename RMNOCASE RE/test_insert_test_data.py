import contextlib
import io
import json
import sqlite3
import tempfile
import unittest
from functools import cmp_to_key
from pathlib import Path
from unittest.mock import patch

import insert_test_data
import query_sorted_data


class InsertTestDataTests(unittest.TestCase):
    def test_rmnocase_comparison(self):
        compare = insert_test_data.rmnocase
        self.assertEqual(compare("Apple", "APPLE"), 0)
        self.assertEqual(compare("Müller", "MÜLLER"), 0)
        self.assertLess(compare("", "a"), 0)
        self.assertGreater(compare("b", "A"), 0)
        self.assertEqual(compare("cafe", "café"), 0)
        self.assertEqual(compare("Montréal", "montreal"), 0)
        self.assertEqual(compare("é", "e\u0301"), 0)

    def test_order_matches_rootsmagic_rebuilt_index(self):
        expected_ids = [
            338, 339, 340, 348, 349, 350, 351, 352, 284, 286, 288, 283,
            281, 343, 345, 278, 285, 287, 282, 279, 280, 347, 306, 307,
            318, 319, 341, 342, 296, 297, 344, 346, 298, 299, 262, 263,
            264, 265, 300, 301, 293, 294, 295, 241, 242, 243, 244, 245,
            246, 247, 248, 249, 320, 321, 324, 325, 353, 354, 355, 356,
            289, 290, 291, 292, 326, 327, 328, 329, 256, 257, 258, 259,
            334, 335, 336, 337, 310, 311, 250, 251, 322, 323, 270, 271,
            272, 273, 252, 253, 312, 313, 274, 275, 276, 277, 314, 315,
            316, 317, 254, 255, 330, 331, 332, 333, 304, 305, 302, 303,
            266, 267, 268, 269, 308, 309, 260, 261,
        ]
        rows = list(enumerate(insert_test_data.TEST_DATA, 241))
        rows.sort(key=cmp_to_key(lambda a, b: insert_test_data.rmnocase(a[1], b[1])))
        self.assertEqual([place_id for place_id, _ in rows], expected_ids)

    def test_rootsmagic_paired_comparisons(self):
        pairs = [
            ("é", "e\u0301", 0), ("café", "cafe", 0),
            ("ﬁnale", "finale", 0), ("ä", "a", 0), ("ß", "ss", 0),
            ("œ", "oe", 1), ("Å", "a", 0), ("Ø", "O", 1),
            ("Ł", "L", 1), ("a-b", "ab", -1), ("a'b", "ab", -1),
        ]
        for index, (left, right, expected) in enumerate(pairs):
            with self.subTest(left=left, right=right):
                left, right = f"probe{index:02}-{left}", f"probe{index:02}-{right}"
                self.assertEqual(insert_test_data.rmnocase(left, right), expected)
                self.assertEqual(insert_test_data.rmnocase(right, left), -expected)

    def test_rootsmagic_punctuation_and_unicode_pairs(self):
        # Observed from a RootsMagic 12 Windows index, with each pair in both ID orders.
        pairs = [
            ("a b", "ab", -1), ("a-b", "a b", 1), ("a.b", "a-b", 1),
            ("a_b", "a-b", 1), ("a/b", "a-b", 1), ("a,b", "a.b", -1),
            ("a!b", "a#b", -1), ("a@b", "a_b", -1), ("a (b)", "a-b", -1),
            ("a--b", "a-b", -1), ("a b", "a  b", 1), ("a", "a ", -1),
            ("a", "a-", -1), ("a2", "a10", 1), ("2", "10", 1),
            ("02", "2", -1), ("a\tb", "a b", -1), ("a\nb", "a b", -1),
            ("a\u00a0b", "a b", 1), ("a’b", "a'b", 1), ("a–b", "a-b", 1),
            ("a—b", "a-b", 1), ("a.b", "ab", -1), ("a/b", "ab", -1),
            ("ab", "a_b", 1), ("ñ", "n", 0), ("ç", "c", 0), ("ý", "y", 0),
            ("ž", "z", 0), ("š", "s", 0), ("ğ", "g", 0), ("ð", "d", 1),
            ("þ", "th", 1), ("đ", "d", 1), ("ı", "i", 1), ("İ", "i", 0),
            ("æ", "ae", 1), ("œ", "oe", 1), ("ẞ", "ss", 0), ("ﬀ", "ff", 0),
            ("ﬃ", "ffi", 0), ("ﬄ", "ffl", 0), ("ﬆ", "st", 0), ("K", "k", 0),
            ("Å", "A", 0), ("å", "aa", -1), ("ø", "o", 1), ("ł", "l", 1),
            ("é", "e\u0301", 0), ("a\u0301", "a", 0),
            ("a\u0300\u0301", "a\u0301\u0300", 0), ("Ω", "ω", 0),
            ("Σ", "ς", 0), ("ά", "α", 0), ("й", "и", 0), ("ё", "е", 0),
            ("А", "а", 0), ("א", "ב", -1), ("ا", "أ", 0), ("か", "が", 0),
            ("カ", "か", 1), ("カ", "ｶ", -1), ("１", "1", 1), ("é", "f", -1),
            ("-", " ", 1), ("~", "z", 1), ("😀", "😁", -1), ("Ａ", "A", 1),
            ("①", "1", 1), ("ﬂ", "fl", 0), ("ſ", "s", 0), ("ẃ", "w", 0),
        ]
        for index, (left, right, expected) in enumerate(pairs):
            with self.subTest(left=left, right=right):
                left, right = f"probe{index:02}/{left}", f"probe{index:02}/{right}"
                self.assertEqual(insert_test_data.rmnocase(left, right), expected)
                self.assertEqual(insert_test_data.rmnocase(right, left), -expected)

    def test_rootsmagic_unicode_boundary_pairs(self):
        pairs = [
            ("a\u200bb", "ab", 1), ("a\u200cb", "ab", 1),
            ("a\u200db", "ab", 1), ("a\u2060b", "ab", 1),
            ("a\u00adb", "ab", 1), ("a\ufeffb", "ab", 1),
            ("a\ufe0fb", "ab", 0), ("a\u034fb", "ab", 0),
            ("a\u2003b", "a b", 1), ("a\u202fb", "a b", 1),
            ("a−b", "a-b", 1), ("\U00010000", "\ue000", 1),
            ("😀", "\ufffd", 1), ("😀", "\ue000", 1),
            ("İ", "i\u0307", 0), ("ϐ", "β", 0), ("ϲ", "ς", 1),
            ("µ", "μ", 0), ("Ω", "ω", 0), ("Å", "Å", 0),
            ("ẛ", "ṡ", 0), ("a\u0301", "a\u0308", 0), ("a\u0323", "a", 0),
        ]
        for index, (left, right, expected) in enumerate(pairs):
            with self.subTest(left=left, right=right):
                left, right = f"probe{index:04}/{left}", f"probe{index:04}/{right}"
                self.assertEqual(insert_test_data.rmnocase(left, right), expected)
                self.assertEqual(insert_test_data.rmnocase(right, left), -expected)

    def test_rootsmagic_seeded_pairs(self):
        fixture = Path(__file__).with_name("rmnocase_seeded_observations.json")
        with fixture.open(encoding="utf-8") as file:
            pairs = json.load(file)["pairs"]
        self.assertEqual(len(pairs), 1024)
        for left, right, expected in pairs:
            with self.subTest(left=left, right=right):
                self.assertEqual(insert_test_data.rmnocase(left, right), expected)
                self.assertEqual(insert_test_data.rmnocase(right, left), -expected)

    def test_rootsmagic_language_pairs(self):
        fixture = Path(__file__).with_name("rmnocase-language-observations.json")
        with fixture.open(encoding="utf-8") as file:
            pairs = json.load(file)["pairs"]
        self.assertEqual(len(pairs), 34776)
        for index, (group, kind, left, right, expected) in enumerate(pairs):
            prefix = f"case{index:06d}/"
            with self.subTest(group=group, kind=kind, left=left, right=right):
                self.assertEqual(insert_test_data.rmnocase(prefix + left, prefix + right), expected)
                self.assertEqual(insert_test_data.rmnocase(prefix + right, prefix + left), -expected)

    def test_inserts_into_database_with_rmnocase_index(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            db_path = Path(directory) / "test.rmtree"
            with contextlib.closing(sqlite3.connect(db_path)) as conn:
                conn.create_collation(
                    "RMNOCASE", lambda a, b: -insert_test_data.rmnocase(a, b)
                )
                conn.execute(
                    "CREATE TABLE PlaceTable (PlaceID INTEGER PRIMARY KEY, "
                    "PlaceType INTEGER, Name TEXT COLLATE RMNOCASE, "
                    "Abbrev TEXT, Normalized TEXT, Latitude INTEGER, "
                    "Longitude INTEGER, LatLongExact INTEGER, MasterID INTEGER, "
                    "Note TEXT, Reverse TEXT COLLATE RMNOCASE, fsID INTEGER, "
                    "anID INTEGER, UTCModDate FLOAT)"
                )
                conn.execute("CREATE INDEX idxPlaceName ON PlaceTable (Name)")
                conn.execute("CREATE INDEX idxReversePlaceName ON PlaceTable (Reverse)")
                conn.executemany(
                    "INSERT INTO PlaceTable (PlaceType, Name) VALUES (1, ?)",
                    [("seed-a",), ("seed-z",)],
                )
                conn.commit()

            names = insert_test_data.TEST_DATA
            with (
                patch.object(insert_test_data, "DB_PATH", str(db_path)),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertTrue(insert_test_data.insert_test_data())

            with contextlib.closing(sqlite3.connect(db_path)) as conn:
                conn.create_collation("RMNOCASE", insert_test_data.rmnocase)
                rows = conn.execute(
                    "SELECT Name, Abbrev, Normalized, Latitude, Longitude, "
                    "LatLongExact, MasterID, Note, Reverse, fsID, anID, UTCModDate "
                    "FROM PlaceTable WHERE PlaceType = 0 ORDER BY PlaceID"
                ).fetchall()
                self.assertEqual(conn.execute("PRAGMA integrity_check").fetchall(), [("ok",)])
            self.assertEqual([row[0] for row in rows], names)
            for name, abbrev, normalized, lat, lon, exact, master, note, reverse, fsid, anid, modified in rows:
                self.assertEqual((abbrev, normalized, note), ("", "", ""))
                self.assertEqual((lat, lon, exact, master, fsid, anid), (0, 0, 0, 0, 0, 0))
                self.assertEqual(reverse, name)
                self.assertGreater(modified, 0)

    def test_query_reads_existing_index_not_approximation(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            db_path = Path(directory) / "test.rmtree"
            with contextlib.closing(sqlite3.connect(db_path)) as conn:
                conn.create_collation(
                    "RMNOCASE", lambda a, b: -insert_test_data.rmnocase(a, b)
                )
                conn.execute(
                    "CREATE TABLE PlaceTable (PlaceID INTEGER PRIMARY KEY, "
                    "PlaceType INTEGER, Name TEXT COLLATE RMNOCASE)"
                )
                conn.execute("CREATE INDEX idxPlaceName ON PlaceTable (Name)")
                conn.executemany(
                    "INSERT INTO PlaceTable (PlaceType, Name) VALUES (?, ?)",
                    [(0, "a"), (0, "b"), (0, "c"), (1, "temple")],
                )
                conn.commit()
            original = db_path.read_bytes()
            with (
                patch.object(query_sorted_data, "DB_PATH", str(db_path)),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                self.assertTrue(query_sorted_data.query_sorted_data())
            output = (db_path.parent / "sorted_output.txt").read_text(encoding="utf-8")
            self.assertLess(output.index("Name='c'"), output.index("Name='b'"))
            self.assertLess(output.index("Name='b'"), output.index("Name='a'"))
            self.assertNotIn("temple", output)
            self.assertEqual(db_path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
