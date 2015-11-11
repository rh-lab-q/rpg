from tests.support import RpgTestCase
from rpg import Base
from rpg.command import Command
import os


class BuildTest(RpgTestCase):

    def test_rpg_project(self):
        self.base = Base()
        self.base.sack = self.base.load_dnf_sack()
        self.base.load_plugins()
        self.base.load_project_from_url(
            "https://github.com/openSUSE/libsolv")
        self.base.spec.Name = "LibSolv"
        self.base.spec.Version = "0.6.11"
        self.base.spec.Release = "1%{?snapshot}%{?dist}"
        self.base.spec.License = "GPLv2"
        self.base.spec.Summary = "Library for solving repository info"
        self.base.spec.description = (
            "This is libsolv, a free package dependency solver "
            "using a satisfiability algorithm.")
        self.base.spec.URL = "https://github.com/openSUSE/libsolv"
        self.base.target_arch = "x86_64"
        self.base.target_distro = "fedora-22"
        self.base.fetch_repos(self.base.target_distro, self.base.target_arch)
        self.base.run_extracted_source_analysis()
        self.base.run_patched_source_analysis()
        self.base.spec.build = Command([
            r'cmake . -DCMAKE_BUILD_TYPE=RelWithDebInfo '
            r'-DENABLE_PERL=1 '
            r'-DENABLE_PYTHON=1 '
            r'-DENABLE_RUBY=1 '
            r'-DUSE_VENDORDIRS=1 '
            r'-DFEDORA=1 '
            r'-DENABLE_LZMA_COMPRESSION=1',
            "make"])
        self.base.build_project()
        self.base.run_compiled_source_analysis()
        self.base.install_project()
        self.base.run_installed_source_analysis()
        self.base.build_srpm()
        self.assertTrue(self.base.srpm_path.exists())
        self.base.build_rpm_recover(
            self.base.target_distro, self.base.target_arch)
        self.assertTrue(self.base.rpm_path)

    def tearDown(self):
        for _rpm in self.base.rpm_path:
            os.remove(str(_rpm))
        os.remove(str(self.base.srpm_path))
        os.remove(str(self.base.spec_path))
