import contextlib
import importlib.util
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import yaml


DEV_UTILS = Path(__file__).resolve().parents[1]


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


readme_build = load_script(
    "readme_build", DEV_UTILS / "Build doc" / "Build ReadMe files.py")
suite_build = load_script("suite_build", DEV_UTILS / "build-suite-release.py")


class BuildTypeTests(unittest.TestCase):
    def test_build_outputs_for_release_and_other_types(self):
        for build_type, suffix, marker in [
            ("RELEASE", "", ""),
            ("DEV", " DEV", "╋"),
            ("ALPHA", " ALPHA", "╋"),
            ("BETA", " BETA", ""),
        ]:
            with self.subTest(build_type=build_type), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                dev = root / "dev util scripts"
                source = root / "doc" / "doc-sources"
                project = root / "Example"
                for directory in (dev / "Build doc", source, project):
                    directory.mkdir(parents=True)

                config = {
                    "SuiteVersion": "1.2.0",
                    "BuildType": build_type,
                    "SuiteName": "Suite",
                    "ProjectRootDirPath": str(root),
                    "ProjectList": ["Example"],
                }
                (dev / "projects-to-build.yaml").write_text(
                    yaml.safe_dump(config), encoding="utf-8"
                )
                (project / "_util_info.yaml").write_text(yaml.safe_dump({
                    "Version": "2.3.4",
                    "UtilityName": "Example",
                    "DistributionFileList": ["Example.py"],
                    "DistributionFolderList": [],
                }), encoding="utf-8")
                (project / "Example.py").write_text(
                    'VERSION = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"\n',
                    encoding="utf-8",
                )
                (root / "doc" / "_ReadMe Top Level.txt").write_text(
                    "Overview\n", encoding="utf-8"
                )
                (source / "DocOutline_Example.txt").write_text(
                    "█_VARIABLES:\nNAME = Example\n█_END_VARIABLES\n"
                    "█_INCLUDE: SHARED\n", encoding="utf-8"
                )
                (root / "doc" / "docs-reusable-content.txt").write_text(
                    "=========================================================================DIV80==\n"
                    "SHARED\nHello {NAME}\n"
                    "=========================================================================DIV80==\n",
                    encoding="utf-8",
                )

                with patch.object(readme_build, "__file__", str(dev / "Build doc" / "build.py")), \
                        patch.object(readme_build, "pause_with_message"), \
                        contextlib.redirect_stdout(io.StringIO()):
                    readme_build.main()

                output = (root / "doc" / "docs-generated" / "ReadMe_Example.txt").read_text(
                    encoding="utf-8"
                )
                self.assertIn(f"{marker}Hello Example\n", output)
                self.assertIn(f"Suite Version: 1.2.0{suffix}\n", output)
                self.assertIn(f"Utility Version: 2.3.4{suffix}\n", output)
                if not marker:
                    self.assertNotIn("╋", output)

                def test_path(value):
                    if value == r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts":
                        return root
                    return Path(value)

                test_path.mkdir = Path.mkdir
                with patch.object(suite_build, "Path", test_path), \
                        patch.object(suite_build, "pause_with_message"), \
                        contextlib.redirect_stdout(io.StringIO()):
                    suite_build.main()

                release_dir, = root.glob("Release *")
                distribution = release_dir / f"Suite_v1.2.0{suffix}"
                self.assertTrue(distribution.is_dir())
                version_line = (distribution / "Example" / "Example.py").read_text(
                    encoding="utf-8"
                )
                self.assertIn(f'VERSION = "2.3.4{suffix}   ', version_line)
                archive = release_dir / f"Suite_v1.2.0{suffix}.zip"
                with zipfile.ZipFile(archive) as zipped:
                    self.assertIn(
                        f"Suite_v1.2.0{suffix}/Example/Example.py", zipped.namelist())

    def test_invalid_build_type_stops_before_changing_files(self):
        for build_type in (None, "", "release", "OTHER", False, ["ALPHA"], "missing"):
            with self.subTest(build_type=build_type), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                dev = root / "dev util scripts"
                (dev / "Build doc").mkdir(parents=True)
                staging = root / "doc" / "docs-generated"
                staging.mkdir(parents=True)
                sentinel = staging / "keep.txt"
                sentinel.write_text("unchanged", encoding="utf-8")
                config = {
                    "SuiteVersion": "1.2.0",
                    "SuiteName": "Suite",
                    "ProjectRootDirPath": str(root),
                    "ProjectList": [],
                }
                if build_type != "missing":
                    config["BuildType"] = build_type
                (dev / "projects-to-build.yaml").write_text(
                    yaml.safe_dump(config), encoding="utf-8"
                )

                def test_path(value):
                    if value == r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts":
                        return root
                    return Path(value)

                test_path.mkdir = Path.mkdir
                for script in (readme_build, suite_build):
                    with self.subTest(script=script.__name__), \
                            patch.object(readme_build, "__file__", str(dev / "Build doc" / "build.py")), \
                            patch.object(suite_build, "Path", test_path), \
                            patch.object(script, "pause_with_message"), \
                            contextlib.redirect_stdout(io.StringIO()) as output:
                        self.assertEqual(script.main(), 1)
                        self.assertIn(
                            "BuildType must be DEV, ALPHA, BETA, or RELEASE", output.getvalue())

                self.assertEqual(sentinel.read_text(
                    encoding="utf-8"), "unchanged")
                self.assertFalse((root / ".vscode").exists())
                self.assertEqual(list(root.glob("Release *")), [])


if __name__ == "__main__":
    unittest.main()
