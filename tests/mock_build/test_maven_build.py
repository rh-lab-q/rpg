from tests.support import RpgTestCase
from rpg import Base
import os


class MavenBuildTest(RpgTestCase):

    def test_maven_project(self):
        self.base = Base()
        self.base.sack = self.base.load_dnf_sack()
        self.base.load_plugins()
        self.base.load_project_from_url(
            r"https://github.com/apache/commons-compress/archive/rel/1.10.zip")
        self.base.spec.Name = "commonsCompress"
        self.base.spec.Version = "1.10"
        self.base.spec.Release = "1"
        self.base.spec.License = "ASL 2.0"
        self.base.spec.Summary = (
            "Commons Compress is a Java library for working with various"
            "compression and archiving formats.")
        self.base.spec.description = (
            "The Apache Commons Compress library defines an API for working "
            "with ar, cpio, Unix dump, tar, zip, gzip, XZ, Pack200, bzip2, "
            "7z, arj, lzma, snappy, DEFLATE and Z files.")
        self.base.spec.URL = (
            r"http://commons.apache.org/proper/commons-compress/")
        self.base.target_arch = "x86_64"
        self.base.target_distro = "fedora-22"
        self.base.fetch_repos(self.base.target_distro, self.base.target_arch)
        self.base.run_extracted_source_analysis()
        self.base.run_patched_source_analysis()
        self.base.build_project()
        self.base.run_compiled_source_analysis()
        self.base.install_project()
        self.base.run_installed_source_analysis()
        self.base.build_srpm()
        self.assertTrue(self.base.srpm_path.exists())
        self.base.build_rpm_recover(
            self.base.target_distro, self.base.target_arch)
        os.remove(str(self.base.srpm_path))
        os.remove(str(self.base.spec_path))
