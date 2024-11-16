import os
from pathlib import Path
import tempfile
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from xmr import Xmr


class TestXmr(IsolatedAsyncioTestCase):
    @patch("xmr.config.settings.ENV_UPLOAD", new="/mnt/mock_upload_path")
    def setUp(self):
        super().setUp()
        self.xmr = Xmr()

    def test_get_upload_folder(self):
        path = self.xmr.get_upload_folder("the_target_folder")

        self.assertEqual(path, Path("/mnt/mock_upload_path/the_target_folder"))

    def test_store_rows(self):
        rows = [
            ["index", "date", "value"],
            [1, "2024-11-07", 10],
            [2, "2024-11-07", 20],
        ]

        csv_file = self.xmr._store_rows_sync(
            rows,
            dict(
                delimiter="|",
                quotechar="'",
                lineterminator="\n",
            ),
        )

        expected_file_contents = "".join(
            [
                "index|date|value\n",
                "1|2024-11-07|10\n",
                "2|2024-11-07|20\n",
            ]
        )

        with open(csv_file, "r") as csv_file:
            data = csv_file.read()
            self.assertEqual(data, expected_file_contents)

    def test_walk(self):
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)

            os.mkdir(tempdir_path / "subfolder")
            (tempdir_path / "subfolder" / "mock.txt").touch()
            (tempdir_path / "subfolder" / "mock.zip").touch()
            (tempdir_path / "subfolder" / "mock_binary").touch()

            expected = [
                (f"{tempdir}/subfolder/mock.txt", "mock.txt", "txt"),
                (f"{tempdir}/subfolder/mock.zip", "mock.zip", "zip"),
                (f"{tempdir}/subfolder/mock_binary", "mock_binary", None),
            ]

            for filepath, filename, ext in self.xmr.walk(tempdir_path):
                self.assertIn((filepath, filename, ext), expected)

    def test_walk_specific_subfolders(self):
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)

            os.mkdir(tempdir_path / "ignore_subfolder")
            (tempdir_path / "ignore_subfolder" / "mock.txt").touch()

            os.mkdir(tempdir_path / "subfolder")
            (tempdir_path / "subfolder" / "mock.txt").touch()
            (tempdir_path / "subfolder" / "mock.zip").touch()
            (tempdir_path / "subfolder" / "mock_binary").touch()

            expected = [
                (f"{tempdir}/subfolder/mock.txt", "mock.txt", "txt"),
                (f"{tempdir}/subfolder/mock.zip", "mock.zip", "zip"),
                (f"{tempdir}/subfolder/mock_binary", "mock_binary", None),
            ]

            actual = []
            for filepath, filename, ext in self.xmr.walk(
                tempdir_path, subfolders=["subfolder"]
            ):
                actual.append((filepath, filename, ext))

            self.assertListEqual(sorted(actual), sorted(expected))

    def test_walk_with_condition(self):
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir_path = Path(tempdir)

            os.mkdir(tempdir_path / "subfolder_1")
            (tempdir_path / "subfolder_1" / "mock.txt").touch()

            os.mkdir(tempdir_path / "subfolder_2")
            (tempdir_path / "subfolder_2" / "mock.txt").touch()
            (tempdir_path / "subfolder_2" / "mock.zip").touch()
            (tempdir_path / "subfolder_2" / "mock_binary").touch()

            expected = [
                (f"{tempdir}/subfolder_1/mock.txt", "mock.txt", "txt"),
                (f"{tempdir}/subfolder_2/mock.txt", "mock.txt", "txt"),
            ]

            def condition(filename):
                return filename.lower().endswith(".txt")

            actual = []
            for filepath, filename, ext in self.xmr.walk(
                tempdir_path, condition=condition
            ):
                actual.append((filepath, filename, ext))

            self.assertListEqual(sorted(actual), sorted(expected))
