import configparser
import importlib.util
import io
import sqlite3
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / 'CitationNameUpdater.py'
SPEC = importlib.util.spec_from_file_location('citation_name_updater', SCRIPT_PATH)
UPDATER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPDATER)


class DefaultCitationNameTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(':memory:')
        self.addCleanup(self.connection.close)
        self.connection.executescript('''
            CREATE TABLE SourceTemplateTable (
                TemplateID INTEGER PRIMARY KEY, Name TEXT, FieldDefs BLOB
            );
            CREATE TABLE SourceTable (
                SourceID INTEGER PRIMARY KEY, Name TEXT, TemplateID INTEGER
            );
            CREATE TABLE CitationTable (
                CitationID INTEGER PRIMARY KEY, SourceID INTEGER,
                CitationName TEXT, Fields BLOB
            );
        ''')
        definitions = b'''<Root><Fields>
            <Field><FieldName>Title</FieldName><Type>Text</Type>
                <CitationField>False</CitationField></Field>
            <Field><FieldName>Person</FieldName><Type>Name</Type>
                <CitationField>True</CitationField></Field>
            <Field><FieldName>Date</FieldName><Type>Date</Type>
                <CitationField>True</CitationField></Field>
            <Field><FieldName>Page</FieldName><Type>Text</Type>
                <CitationField>True</CitationField></Field>
            <Field><FieldName>Missing</FieldName><Type>Place</Type>
                <CitationField>True</CitationField></Field>
        </Fields></Root>'''
        fields = b'''<Root><Fields>
            <Field><Name>Person</Name><Value>John Doe</Value></Field>
            <Field><Name>Date</Name><Value>1900</Value></Field>
            <Field><Name>Page</Name><Value>42</Value></Field>
        </Fields></Root>'''
        self.connection.execute(
            'INSERT INTO SourceTemplateTable VALUES (?, ?, ?)',
            (1, 'Template', definitions))
        self.connection.execute('INSERT INTO SourceTable VALUES (1, ?, 1)', ('Source',))
        self.connection.execute(
            'INSERT INTO CitationTable VALUES (1, 1, ?, ?)', ('Old name', fields))

    def run_updater(self, make_changes, options=None, filters=None, report=None):
        config = configparser.ConfigParser(interpolation=None)
        config.read_dict({
            'FILTER': {'USE_REGEXP': 'off'},
            'CITATION_NAME_UPDATER': {
                'MAKE_CHANGES': make_changes,
                'TEMPLATE_DEFAULT': 'on',
            },
        })
        if options:
            config['CITATION_NAME_UPDATER'].update(options)
        if filters:
            config['FILTER'].update(filters)
        if report is None:
            report = io.StringIO()
        UPDATER.run_update_citation_name(config, self.connection, report)
        return report.getvalue()

    def add_source_and_citation(self, source_id, template_id, citation_id):
        self.connection.execute(
            'INSERT INTO SourceTable VALUES (?, ?, ?)',
            (source_id, f'Source {source_id}', template_id))
        self.connection.execute(
            'INSERT INTO CitationTable '
            'SELECT ?, ?, ?, Fields FROM CitationTable WHERE CitationID = 1',
            (citation_id, source_id, f'Old name {citation_id}'))

    def test_preview_includes_all_citation_fields_in_template_order(self):
        report = self.run_updater('off')
        self.assertIn("'John Doe; 1900; 42; [Missing]'", report)
        self.assertEqual(
            'Old name',
            self.connection.execute('SELECT CitationName FROM CitationTable').fetchone()[0])

    def test_update_writes_all_citation_fields(self):
        self.run_updater('on')
        self.assertEqual(
            'John Doe; 1900; 42; [Missing]',
            self.connection.execute('SELECT CitationName FROM CitationTable').fetchone()[0])

    def test_custom_template_rejects_multiple_templates_before_any_update(self):
        self.connection.execute(
            'INSERT INTO SourceTemplateTable '
            'SELECT 2, ?, FieldDefs FROM SourceTemplateTable WHERE TemplateID = 1',
            ('Template',))
        self.add_source_and_citation(2, 2, 2)
        options = {
            'TEMPLATE_DEFAULT': 'off',
            'TEMPLATE_FROM_SOURCE_TEMPLATE': 'off',
            'CUSTOM_TEMPLATE': '[Person]',
        }
        for mode in ('off', 'on'):
            with self.subTest(make_changes=mode):
                with self.assertRaisesRegex(
                        UPDATER.RMc.RM_Py_Exception, 'same source template'):
                    self.run_updater(mode, options)
                self.assertEqual(
                    [('Old name',), ('Old name 2',)],
                    self.connection.execute(
                        'SELECT CitationName FROM CitationTable ORDER BY CitationID'
                    ).fetchall())

    def test_custom_template_accepts_multiple_sources_with_same_template(self):
        self.add_source_and_citation(2, 1, 2)
        self.run_updater('on', {
            'TEMPLATE_DEFAULT': 'off',
            'TEMPLATE_FROM_SOURCE_TEMPLATE': 'off',
            'CUSTOM_TEMPLATE': '[Person]',
        })
        self.assertEqual(
            [('John Doe',), ('John Doe',)],
            self.connection.execute(
                'SELECT CitationName FROM CitationTable ORDER BY CitationID'
            ).fetchall())

    def test_template_validation_only_considers_filtered_citations(self):
        self.connection.execute(
            'INSERT INTO SourceTemplateTable '
            'SELECT 2, ?, FieldDefs FROM SourceTemplateTable WHERE TemplateID = 1',
            ('Other template',))
        self.add_source_and_citation(2, 2, 2)
        self.run_updater('on', {
            'TEMPLATE_DEFAULT': 'off',
            'TEMPLATE_FROM_SOURCE_TEMPLATE': 'off',
            'CUSTOM_TEMPLATE': '[Person]',
        }, {'SOURCE_NAME': 'Source'})
        self.assertEqual(
            [('John Doe',), ('Old name 2',)],
            self.connection.execute(
                'SELECT CitationName FROM CitationTable ORDER BY CitationID'
            ).fetchall())

    def test_custom_template_allows_empty_intersection(self):
        self.connection.execute(
            'INSERT INTO SourceTemplateTable '
            'SELECT 2, ?, FieldDefs FROM SourceTemplateTable WHERE TemplateID = 1',
            ('Other template',))
        self.add_source_and_citation(2, 2, 2)
        report = self.run_updater('on', {
            'TEMPLATE_DEFAULT': 'off',
            'TEMPLATE_FROM_SOURCE_TEMPLATE': 'off',
            'CUSTOM_TEMPLATE': '[Person]',
        }, {'SOURCE_TEMPLATE': 'Template', 'SOURCE_NAME': 'Source 2'})
        self.assertIn('Selected citations: 0', report)
        self.assertIn('No source templates selected.', report)
        self.assertEqual(
            [('Old name',), ('Old name 2',)],
            self.connection.execute(
                'SELECT CitationName FROM CitationTable ORDER BY CitationID'
            ).fetchall())

    def test_default_and_source_templates_allow_multiple_templates(self):
        self.connection.execute(
            'ALTER TABLE SourceTemplateTable ADD COLUMN CitationName TEXT')
        self.connection.execute(
            "UPDATE SourceTemplateTable SET CitationName = '[Person]'")
        self.connection.execute(
            'INSERT INTO SourceTemplateTable '
            'SELECT 2, ?, FieldDefs, CitationName FROM SourceTemplateTable WHERE TemplateID = 1',
            ('Other template',))
        self.add_source_and_citation(2, 2, 2)
        self.assertIn('Selected citations: 2', self.run_updater('off'))
        self.assertIn('Selected citations: 2', self.run_updater('off', {
            'TEMPLATE_DEFAULT': 'off',
            'TEMPLATE_FROM_SOURCE_TEMPLATE': 'on',
            'CUSTOM_TEMPLATE': 'ignored',
        }))

    def test_report_lists_each_selected_default_template_once_in_all_modes(self):
        self.connection.execute(
            'ALTER TABLE SourceTemplateTable ADD COLUMN CitationName TEXT')
        self.connection.execute(
            "UPDATE SourceTemplateTable SET CitationName = '[Person]'")
        self.connection.execute(
            'INSERT INTO SourceTemplateTable VALUES (?, ?, ?, ?)',
            (2, 'Other template', b'''<Root><Fields>
                <Field><FieldName>Location</FieldName><Type>Place</Type>
                    <CitationField>True</CitationField></Field>
                <Field><FieldName>Title</FieldName><Type>Text</Type>
                    <CitationField>False</CitationField></Field>
            </Fields></Root>''', '[Location]'))
        self.add_source_and_citation(2, 1, 2)
        self.add_source_and_citation(3, 2, 3)
        options_list = [
            {},
            {'TEMPLATE_DEFAULT': 'off', 'TEMPLATE_FROM_SOURCE_TEMPLATE': 'on',
             'CUSTOM_TEMPLATE': ''},
            {'TEMPLATE_DEFAULT': 'off', 'TEMPLATE_FROM_SOURCE_TEMPLATE': 'off',
             'CUSTOM_TEMPLATE': '[Person]'},
        ]
        for options in options_list:
            with self.subTest(options=options):
                report = io.StringIO()
                if options.get('TEMPLATE_FROM_SOURCE_TEMPLATE') == 'off':
                    with self.assertRaises(UPDATER.RMc.RM_Py_Exception):
                        self.run_updater('off', options, report=report)
                    text = report.getvalue()
                else:
                    text = self.run_updater('off', options, report=report)
                self.assertEqual(1, text.count('Source template 1: Template\n'))
                self.assertEqual(1, text.count('Source template 2: Other template\n'))
                self.assertIn('[Person]; [Date]; [Page]; [Missing]\n', text)
                self.assertIn('Source template 2: Other template\n[Location]\n', text)

        text = self.run_updater('off', filters={'SOURCE_NAME': 'Source'})
        self.assertIn('Source template 1: Template\n', text)
        self.assertNotIn('Source template 2: Other template\n', text)


if __name__ == '__main__':
    unittest.main()
