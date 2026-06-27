import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from utils import file_io


class FileIoResilienceTests(unittest.TestCase):
    def test_initialise_progress_backs_up_corrupt_file_before_resetting(self):
        with tempfile.TemporaryDirectory() as tmp:
            progress_path = Path(tmp) / "progress.json"
            progress_path.write_text("{not valid json", encoding="utf-8")

            with patch("utils.file_io.get_progress_path", return_value=str(progress_path)):
                file_io.initialise_progress_if_missing()

            self.assertEqual(json.loads(progress_path.read_text(encoding="utf-8")), file_io.DEFAULT_PROGRESS)
            backup_path = progress_path.with_suffix(progress_path.suffix + ".corrupt")
            self.assertEqual(backup_path.read_text(encoding="utf-8"), "{not valid json")


if __name__ == "__main__":
    unittest.main()
