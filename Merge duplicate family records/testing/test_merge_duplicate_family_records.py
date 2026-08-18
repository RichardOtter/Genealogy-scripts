import importlib.util
import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / (
    'MergeDuplicateFamilyRecords.py')
SPEC = importlib.util.spec_from_file_location(
    'merge_duplicate_families', SCRIPT_PATH)
MERGE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MERGE
SPEC.loader.exec_module(MERGE)


class MergeDuplicateFamilyRecordsTests(unittest.TestCase):

    def test_shared_and_unique_children_are_merged(self):
        connection = sqlite3.connect(':memory:')
        connection.executescript('''
            CREATE TABLE ChildTable (
                RecID INTEGER PRIMARY KEY,
                ChildID INTEGER,
                FamilyID INTEGER
            );
        ''')
        connection.executemany(
            'INSERT INTO ChildTable (RecID, ChildID, FamilyID) VALUES (?, ?, ?)',
            [(1, 10, 100), (2, 10, 101), (3, 11, 101)],
        )

        changed = MERGE.child_reference_updates(connection, 101, 100)

        self.assertEqual(
            [('Redirected', 'ChildTable', 'FamilyID', 1),
             ('Removed duplicate', 'ChildTable', 'FamilyID', 1)],
            changed,
        )
        self.assertEqual(
            [(10, 100), (11, 100)],
            connection.execute(
                'SELECT ChildID, FamilyID FROM ChildTable ORDER BY RecID'
            ).fetchall(),
        )

    def test_person_family_references_are_redirected(self):
        connection = sqlite3.connect(':memory:')
        connection.executescript('''
            CREATE TABLE PersonTable (
                PersonID INTEGER PRIMARY KEY,
                ParentID INTEGER,
                SpouseID INTEGER
            );
            INSERT INTO PersonTable VALUES (1, 101, 101);
            INSERT INTO PersonTable VALUES (2, 101, 0);
        ''')

        changed = MERGE.family_reference_updates(connection, 101, 100)

        self.assertIn(('Redirected', 'PersonTable', 'ParentID', 2), changed)
        self.assertIn(('Redirected', 'PersonTable', 'SpouseID', 1), changed)
        self.assertEqual(
            [(1, 100, 100), (2, 100, 0)],
            connection.execute(
                'SELECT PersonID, ParentID, SpouseID FROM PersonTable '
                'ORDER BY PersonID'
            ).fetchall(),
        )

    def test_owner_type_and_online_links_only_redirect_family_links(self):
        connection = sqlite3.connect(':memory:')
        connection.executescript('''
            CREATE TABLE MediaLinkTable (
                LinkID INTEGER PRIMARY KEY,
                OwnerType INTEGER,
                OwnerID INTEGER
            );
            CREATE TABLE AncestryTable (
                LinkID INTEGER PRIMARY KEY,
                LinkType INTEGER,
                rmID INTEGER
            );
            INSERT INTO MediaLinkTable VALUES (1, 1, 101);
            INSERT INTO MediaLinkTable VALUES (2, 0, 101);
            INSERT INTO AncestryTable VALUES (1, 1, 101);
            INSERT INTO AncestryTable VALUES (2, 0, 101);
        ''')

        MERGE.family_reference_updates(connection, 101, 100)

        self.assertEqual(
            [(1, 1, 100), (2, 0, 101)],
            connection.execute(
                'SELECT LinkID, OwnerType, OwnerID FROM MediaLinkTable '
                'ORDER BY LinkID'
            ).fetchall(),
        )
        self.assertEqual(
            [(1, 1, 100), (2, 0, 101)],
            connection.execute(
                'SELECT LinkID, LinkType, rmID FROM AncestryTable ORDER BY LinkID'
            ).fetchall(),
        )

    def test_backup_merges_without_removed_family_references(self):
        database_path = Path(__file__).parents[1] / 'DB' / (
            'BACKUP_TEST-Merge duplicate family records.rmtreeBU')
        if not database_path.exists():
            self.skipTest('pre-merge backup fixture is not available')

        with tempfile.NamedTemporaryFile(suffix='.rmtree') as temporary_file:
            temporary_file.close()
            connection = sqlite3.connect(temporary_file.name)
            source = sqlite3.connect(database_path)
            source.backup(connection)
            source.close()

            groups = MERGE.duplicate_family_groups(connection)
            removed_ids = MERGE.duplicate_family_ids(groups)
            report = io.StringIO()
            MERGE.merge_records(None, connection, report)

            self.assertEqual(3, len(removed_ids))
            self.assertEqual([], MERGE.remaining_references(
                connection, removed_ids))
            self.assertIsNone(connection.execute(
                'SELECT 1 FROM ChildTable GROUP BY ChildID, FamilyID '
                'HAVING COUNT(*) > 1 LIMIT 1'
            ).fetchone())


if __name__ == '__main__':
    unittest.main()
