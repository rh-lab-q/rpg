from os import makedirs
from os import path
from pathlib import Path
from rpg.source_loader import SourceLoader
from tests.support import RpgTestCase
from shutil import rmtree


class SourceLoaderLongTest(RpgTestCase):

    def setUp(self):
        self._source_loader = SourceLoader()
        self._tar_temp = Path("/var/tmp/rpg_test/")
        self._download = self._tar_temp / "download.tar.gz"

        if path.isdir(str(self._tar_temp)):
            rmtree(str(self._tar_temp))
        makedirs(str(self._tar_temp))


    def test_git_download(self):
        SourceLoader.download_git_repo(
            "https://github.com/rh-lab-q/rpg",
            self._download)
        self.assertTrue(Path(str(self._download)).exists())

    def test_download(self):
        SourceLoader.download_archive(
            "https://github.com/rh-lab-q/rpg/archive/master.tar.gz",
            self._download)
        self.assertTrue(Path(str(self._download)).exists())