from hashlib import md5
from os import makedirs
from os import path
from os import remove
from rpg.command import Command
from rpg.source_loader import SourceLoader
from support import RpgTestCase
from shutil import rmtree
from unittest import expectedFailure


class SourceLoaderTest(RpgTestCase):

    # FileNotFound hash
    FNF_MD5 = "d41d8cd98f00b204e9800998ecf8427e"

    def setUp(self):
        self._source_loader = SourceLoader()
        self._tar = False
        self._tar_dir = self.test_project_dir
        self._tar_gz = self.test_project_dir / "archives" / "sample.tar.gz"
        self._tar_xz = self.test_project_dir / "archives" / "sample.tar.xz"
        self._tar_temp = "/var/tmp/rpg_test/"
        self._tar_extracted = self._tar_temp + "sample"
        self._archive = self._tar_temp + "sample"
        self._hasher = None
        if path.isdir(self._tar_temp):
            rmtree(self._tar_temp)
        makedirs(self._tar_temp)

    def tearDown(self):
        if self._tar:
            remove(str(self._tar))

    def md5TarXz(self, t):
        mdsum = Command(
            "tar -J -xOf " + str(t) +
            " 2>/dev/null | md5sum | cut -b-32"
        ).execute()[:-1]
        self.assertNotEqual(self.FNF_MD5, mdsum)
        return mdsum

    def md5TarGz(self, t):
        mdsum = Command(
            "tar -xOzf " + str(t) +
            " 2>/dev/null | md5sum | cut -b-32"
        ).execute()[:-1]
        self.assertNotEqual(self.FNF_MD5, mdsum)
        return mdsum

    def md5Dir(self, d):
        mdsum = md5(
            Command(
                "find " + d + r" -type f -exec cat {} \;"
            ).execute(True)).hexdigest()
        self.assertNotEqual(self.FNF_MD5, mdsum)
        return mdsum

    def test_tar_gz_method(self):
        self.assertEqual(
            self._source_loader._get_compression_method(
                str(self._tar_gz)),
            "gz")

    def test_tar_xz_method(self):
        self.assertEqual(
            self._source_loader._get_compression_method(
                str(self._tar_xz)),
            "xz")

    def test_tar_gz_extract(self):
        self._source_loader.load_sources(
            self._tar_gz,
            self._tar_extracted)
        self.assertTrue(
            path.isdir(str(self._tar_extracted)))
        self.assertEqual(
            self.md5TarGz(str(self._tar_gz)),
            self.md5Dir(str(self._tar_extracted)))

    def test_tar_xz_extract(self):
        self._source_loader.load_sources(
            self._tar_xz,
            self._tar_extracted)
        self.assertTrue(
            path.isdir(str(self._tar_extracted)))
        self.assertEqual(
            self.md5TarXz(str(self._tar_xz)),
            self.md5Dir(str(self._tar_extracted)))

    def test_dir_source_loader(self):
        self._source_loader.load_sources(
            str(self.test_project_dir),
            self._tar_extracted)
        self.assertEqual(
            self.md5Dir(self._tar_extracted),
            self.md5Dir(str(self.test_project_dir)))

    def test_create_archive(self):
        self._tar = self._source_loader.create_archive(
            str(self._archive),
            str(self._tar_dir))
        self.assertEqual(
            self.md5TarGz(str(self._tar)),
            self.md5Dir(str(self._tar_dir)))

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

    @expectedFailure
    def test_create_archive_fail(self):
        self._tar_dir = "NonExistingDir"
        self.test_create_archive()
