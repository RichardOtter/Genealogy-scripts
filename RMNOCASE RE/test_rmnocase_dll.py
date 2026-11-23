import json
import shutil
import sqlite3
import tempfile
import unittest
import unicodedata
from contextlib import closing
from functools import cmp_to_key
from pathlib import Path

import insert_test_data


FOLDER = Path(__file__).resolve().parent
DLL = FOLDER / "x64" / "Release" / "rmnocase.dll"


class RMNOCASEExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if unicodedata.unidata_version != "17.0.0":
            raise RuntimeError("The DLL comparison tests require Python Unicode 17.0.0")
        cls.db = sqlite3.connect(":memory:")
        cls.db.enable_load_extension(True)
        try:
            cls.db.load_extension(str(DLL))
        finally:
            cls.db.enable_load_extension(False)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def compare(self, a, b):
        return self.db.execute(
            "SELECT (? COLLATE RMNOCASE > ?) - (? COLLATE RMNOCASE < ?)",
            (a, b, a, b),
        ).fetchone()[0]

    def test_recorded_rootsmagic_comparisons(self):
        with (FOLDER / "rmnocase_seeded_observations.json").open(encoding="utf-8") as file:
            pairs = json.load(file)["pairs"]
        self.assertEqual(len(pairs), 1024)
        for a, b, expected in pairs:
            with self.subTest(a=a, b=b):
                self.assertEqual(self.compare(a, b), expected)
                self.assertEqual(self.compare(b, a), -expected)

    def test_recorded_language_comparisons(self):
        with (FOLDER / "rmnocase-language-observations.json").open(encoding="utf-8") as file:
            pairs = json.load(file)["pairs"]
        self.assertEqual(len(pairs), 34776)
        for index, (group, kind, a, b, expected) in enumerate(pairs):
            prefix = f"case{index:06d}/"
            with self.subTest(group=group, kind=kind, a=a, b=b):
                self.assertEqual(self.compare(prefix + a, prefix + b), expected)
                self.assertEqual(self.compare(prefix + b, prefix + a), -expected)

    def test_normalization_and_utf8_boundaries(self):
        strings = [
            "", "a", "A", "café", "CAFE", "e\u0301", "é",
            "x\u302e\u1715", "x\u1715\u302e",
            "x\u302e\u034f\u1715", "x\u1715\u034f\u302e",
            "x\u0301\u1715\u302e", "x\u302e\u0301\u1715",
            "\u1100\u1161", "가", "😀", "\ue000", "\U0010ffff",
            "a\0b", "a\0c", "a\0", "a",
        ]
        for a in strings:
            for b in strings:
                with self.subTest(a=a, b=b):
                    self.assertEqual(self.compare(a, b), insert_test_data.rmnocase(a, b))

    def test_sqlite_index_uses_extension_order(self):
        with closing(sqlite3.connect(":memory:")) as db:
            db.enable_load_extension(True)
            try:
                db.load_extension(str(DLL))
            finally:
                db.enable_load_extension(False)
            db.execute("CREATE TABLE places (id INTEGER PRIMARY KEY, name TEXT COLLATE RMNOCASE)")
            db.execute("CREATE INDEX place_name ON places(name)")
            db.executemany("INSERT INTO places(name) VALUES (?)", [(x,) for x in insert_test_data.TEST_DATA])
            actual = db.execute("SELECT name FROM places INDEXED BY place_name ORDER BY name").fetchall()
            expected = sorted(insert_test_data.TEST_DATA, key=cmp_to_key(insert_test_data.rmnocase))
            self.assertEqual([row[0] for row in actual], expected)
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchall(), [("ok",)])

    def test_invalid_utf8_has_deterministic_index_order(self):
        self.db.execute("CREATE TABLE invalid_test (name TEXT COLLATE RMNOCASE)")
        self.db.execute("CREATE INDEX invalid_test_name ON invalid_test(name)")
        self.db.execute("INSERT INTO invalid_test VALUES ('b'), ('a')")
        for encoded in ("FF", "61FF", "61FE", "C0AF", "EDA080", "F4908080", "C3"):
            self.db.execute(f"INSERT INTO invalid_test VALUES (CAST(X'{encoded}' AS TEXT))")
        actual = self.db.execute(
            "SELECT hex(name) FROM invalid_test INDEXED BY invalid_test_name ORDER BY name"
        ).fetchall()
        self.assertEqual(
            actual,
            [(value,) for value in ("61", "61FE", "61FF", "62", "C0AF", "C3",
                                    "EDA080", "F4908080", "FF")],
        )
        self.assertEqual(self.db.execute("PRAGMA integrity_check").fetchall(), [("ok",)])
        self.assertEqual(self.compare("a", "b"), -1)

    def test_extension_can_be_loaded_under_another_filename(self):
        with tempfile.TemporaryDirectory(dir=FOLDER) as directory:
            copy = Path(directory) / "renamed.dll"
            shutil.copyfile(DLL, copy)
            with closing(sqlite3.connect(":memory:")) as db:
                try:
                    db.enable_load_extension(True)
                    db.load_extension(str(copy))
                finally:
                    db.enable_load_extension(False)
                self.assertEqual(
                    db.execute("SELECT 'café' = 'CAFE' COLLATE RMNOCASE").fetchone()[0],
                    1,
                )


if __name__ == "__main__":
    unittest.main()
