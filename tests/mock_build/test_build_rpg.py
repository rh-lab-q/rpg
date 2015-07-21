from tests.support import RpgTestCase
from rpg import Base
import os


class BuildTest(RpgTestCase):

    def test_rpg_project(self):
        self.base = Base()
        self.base.sack = self.base.dnf_load_sack()
        self.base.load_plugins()
        self.base.load_project_from_url(
            self.test_project_dir / "archives/rpg-0.0.2-1.tar.gz")
        self.base.spec.Name = "rpg"
        self.base.spec.Version = "0.0.2"
        self.base.spec.Release = "1%{?snapshot}%{?dist}"
        self.base.spec.License = "GPLv2"
        self.base.spec.Summary = "RPM Package Generator"
        self.base.spec.description = (
            "RPG is tool, that guides people through"
            "the creation of a RPM package. RPG makes packaging much easier"
            "due to the automatic analysis of packaged files. Beginners can"
            "get familiar with packaging process or the advanced users can"
            "use our tool for a quick creation of a package.")
        self.base.spec.URL = "https://github.com/rh-lab-q/rpg"
        self.base.target_arch = "i386"
        self.base.target_distro = "fedora-22"
        self.base.spec.check.append(["make test"])
        self.base.spec.Requires.union(['makedepend', 'mock'])
        self.base.spec.BuildRequires.union(['makedepend', 'mock'])
        self.base.fetch_repos(self.base.target_distro, self.base.target_arch)
        self.base.run_raw_sources_analysis()
        self.base.run_patched_sources_analysis()
        self.base.build_project()
        self.base.run_compiled_analysis()
        self.base.install_project()
        self.base.run_installed_analysis()
        self.base.build_srpm()
        self.assertTrue(self.base.srpm_path.exists())
        self.base.build_rpm_recover(
            self.base.target_distro, self.base.target_arch)

    def tearDown(self):
        os.remove(str(self.base.srpm_path))
        os.remove(str(self.base.spec_path))
