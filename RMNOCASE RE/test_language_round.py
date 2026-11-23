import contextlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import language_round


class LanguageRoundTests(unittest.TestCase):
    def test_round_requires_rebuild_and_preserves_source(self):
        cases = [
            ["LATIN", "example", "Müller", "muller"],
            ["LATIN", "example", "a", "b"],
            ["JAPANESE", "example", "カ", "か"],
        ]
        with tempfile.TemporaryDirectory(dir=language_round.FOLDER) as directory:
            folder = Path(directory)
            source = folder / "source.rmtree"
            database = folder / "work.rmtree"
            plan = folder / "plan.json"
            observations = folder / "observations.json"
            with contextlib.closing(sqlite3.connect(source)) as conn:
                conn.create_collation("RMNOCASE", language_round.rmnocase)
                conn.execute(
                    "CREATE TABLE PlaceTable (PlaceID INTEGER PRIMARY KEY, "
                    "PlaceType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, "
                    "Normalized TEXT, Latitude INTEGER, Longitude INTEGER, "
                    "LatLongExact INTEGER, MasterID INTEGER, Note TEXT, "
                    "Reverse TEXT COLLATE RMNOCASE, fsID INTEGER, anID INTEGER, "
                    "UTCModDate FLOAT)"
                )
                conn.execute("CREATE INDEX idxPlaceName ON PlaceTable(Name)")
                conn.commit()
            original = source.read_bytes()
            with (
                patch.object(language_round, "SOURCE", source),
                patch.object(language_round, "DATABASE", database),
                patch.object(language_round, "PLAN", plan),
                patch.object(language_round, "OBSERVATIONS", observations),
                patch.object(language_round, "character_groups", return_value={}),
                patch.object(language_round, "make_cases", return_value=cases),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                language_round.prepare()
                with self.assertRaisesRegex(RuntimeError, "rebuild indexes"):
                    language_round.analyze()
                with contextlib.closing(sqlite3.connect(database)) as conn:
                    conn.create_collation("RMNOCASE", language_round.rmnocase)
                    conn.execute("REINDEX RMNOCASE")
                    conn.commit()
                language_round.analyze()
                with observations.open(encoding="utf-8") as file:
                    pairs = json.load(file)["pairs"]
                self.assertEqual([pair[-1] for pair in pairs], [0, -1, 1])
                with self.assertRaises(FileExistsError):
                    language_round.prepare()
            self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
