import csv
import os
import tempfile
from pathlib import Path
from typing import Any, Callable

import anyio

from xmr.config import settings
from xmr.constants import CLICKHOUSE_CSV
from xmr.log import get_logger


class Xmr:
    def __init__(self, logger=None) -> None:
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.upload = Path(settings.ENV_UPLOAD)
        self.logger = get_logger() if not logger else logger

    def get_upload_folder(self, folder: str) -> Path:
        folder = self.upload / folder
        self.logger.info(f"source folder {folder}")
        return folder

    def _store_rows_sync(self, rows: list, fmt: dict = CLICKHOUSE_CSV) -> str:
        # In python3 csv write takes as input str objects
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as csv_file:
            csv_writer = csv.writer(csv_file, **fmt)
            csv_writer.writerows(rows)
            return csv_file.name

    async def store_rows(self, rows: list, fmt: dict = CLICKHOUSE_CSV) -> str:
        file_path = await anyio.to_thread.run_sync(
            self._store_rows_sync(rows, fmt)
        )
        return file_path

    def walk(
        self,
        path: Path,
        subfolders: list = [],
        condition: Callable[[Any], bool] = None,
    ):
        total, use, skip = 0, 0, 0

        for root, dirs, files in os.walk(path):
            if subfolders:
                dirs[:] = subfolders
                # dirs = subfolders.copy()

            for filename in files:
                total += 1
                filepath = str(Path(root).joinpath(filename))

                if condition and not condition(filename):
                    skip += 1
                    self.logger.debug(f"walk skip: {filepath}")
                    continue

                use += 1
                ext = None
                if "." in filename:
                    ext = filename.split(".")[-1]

                yield filepath, filename, ext

        self.logger.info(f"walk fs: total {total}, user {use}, skip {skip}")
