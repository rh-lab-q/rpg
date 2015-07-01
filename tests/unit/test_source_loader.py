from os import makedirs
from os import path
from os import remove
from pathlib import Path
from rpg.command import Command
from rpg.source_loader import SourceLoader
from tests.support import RpgTestCase
from shutil import rmtree
from unittest import expectedFailure


class SourceLoaderTest(RpgTestCase):

    # FileNotFound hash
    FNF_MD5 = "d41d8cd98f00b204e9800998ecf8427e"

    def setUp(self):
        self._source_loader = SourceLoader()
        self._tar = None
        self._tar_dir = self.test_project_dir / "archives"
        self._tar_gz = self.test_project_dir / "archives" / "sample.tar.gz"
        self._tar_xz = self.test_project_dir / "archives" / "sample.tar.xz"
        self._tar_temp = Path("/var/tmp/rpg_test/")
        self._tar_extracted = self._tar_temp / "extracted"

        self._download = self._tar_temp / "download.tar.gz"

        if path.isdir(str(self._tar_temp)):
            rmtree(str(self._tar_temp))
        makedirs(str(self._tar_temp))
        makedirs(str(self._tar_extracted))

    def tearDown(self):
        if self._tar:
            remove(str(self._tar))
        if path.isdir(str(self._tar_temp)):
            rmtree(str(self._tar_temp))

    def md5Tar(self, t):
        mdsum = Command(
            "tar --list -f " + str(t) + " 2>/dev/null | "
            "awk -F/ '{ if($NF != \"\") print $NF }' | "
            r'sed -e "s/.*\///gm" | sort | md5sum'
        ).execute()
        self.assertNotEqual(self.FNF_MD5, mdsum)
        return mdsum

    def md5Dir(self, d):
        md5sum = Command(
            "find " + str(d) +
            r' -type f | sed -e "s/.*\///gm" | sort | md5sum'
        ).execute()
        self.assertNotEqual(self.FNF_MD5, md5sum)
        return md5sum

    def test_tar_gz_method(self):
        self.assertEqual(
            self._source_loader._get_compression_method(
                str(self._tar_gz)),
            ("tar", "gz"))

    def test_tar_xz_method(self):
        self.assertEqual(
            self._source_loader._get_compression_method(
                str(self._tar_xz)),
            ("tar", "xz"))

    def test_tar_gz_extract(self):
        self._source_loader.load_sources(
            self._tar_gz,
            self._tar_extracted)
        self.assertTrue(
            path.isdir(str(self._tar_extracted)))
        self.assertEqual(
            self.md5Tar(str(self._tar_gz)),
            self.md5Dir(str(self._tar_extracted)))
        self.assertExistInDir(["file"], self._tar_extracted)

    def test_tar_xz_extract(self):
        self._source_loader.load_sources(
            self._tar_xz,
            self._tar_extracted)
        self.assertTrue(
            path.isdir(str(self._tar_extracted)))
        self.assertEqual(
            self.md5Tar(str(self._tar_xz)),
            self.md5Dir(str(self._tar_extracted)))
        self.assertExistInDir(["file1", "file2"], self._tar_extracted)

    def test_dir_source_loader(self):
        self._source_loader.load_sources(
            self._tar_dir,
            self._tar_extracted)
        self.assertEqual(
            self.md5Dir(self._tar_extracted),
            self.md5Dir(self._tar_dir))
        self.assertExistInDir(["sample.tar.gz", "sample.tar.xz"],
                              self._tar_extracted)

    @expectedFailure
    def test_tar_xz_method_fail(self):
        self._tar_xz = self._tar_gz
        self.test_tar_xz_method()

    @expectedFailure
    def test_tar_gz_method_fail(self):
        self._tar_gz = self._tar_xz
        self.test_tar_gz_method()

    @expectedFailure
    def test_tar_gz_extract_fail(self):
        self._tar_gz = "NotAnArchive"
        self.test_tar_gz_extract()

    @expectedFailure
    def test_tar_xz_extract_fail(self):
        self._tar_xz = "NotAnArchive"
        self.test_tar_xz_extract()
