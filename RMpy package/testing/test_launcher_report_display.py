import configparser
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import RMpy.launcher as launcher


class ReportDisplayTests(unittest.TestCase):
    def run_launcher(self, app_name):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            app = directory / app_name
            app.touch()
            db_path = directory / 'database.sqlite'
            sqlite3.connect(db_path).close()
            config = configparser.ConfigParser(interpolation=None)
            config['FILE_PATHS'] = {
                'DB_PATH': str(db_path),
                'REPORT_FILE_PATH': str(directory / 'report.txt'),
                'REPORT_FILE_DISPLAY_APP': f'{app}\n--new-window',
            }
            config_path = directory / 'config.ini'
            with config_path.open('w', encoding='utf-8') as config_file:
                config.write(config_file)
            utility_info = {
                'script_path': directory,
                'config_file_name': str(config_path),
                'utility_name': 'Test',
                'utility_version': '1',
                'run_features_function': lambda config, db, report: None,
                'allow_db_changes': False,
                'RMNOCASE_required': False,
                'RMNOCASE_optional': False,
                'RegExp_required': False,
                'RegExp_optional': False,
            }
            original_directory = os.getcwd()
            try:
                with patch.object(sys, 'argv', ['test']), \
                        patch.object(launcher.subprocess, 'run') as run, \
                        patch.object(launcher.subprocess, 'Popen') as popen:
                    self.assertEqual(0, launcher.launcher(utility_info))
                    return app, directory / 'report.txt', run, popen
            finally:
                os.chdir(original_directory)

    def test_waits_for_vscode_cli_to_complete(self):
        app, report, run, popen = self.run_launcher('code.cmd')
        run.assert_called_once_with([app, '--new-window', str(report)], check=True)
        popen.assert_not_called()

    def test_other_viewers_are_still_launched_asynchronously(self):
        app, report, run, popen = self.run_launcher('notepad.exe')
        popen.assert_called_once_with([app, '--new-window', str(report)])
        run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
