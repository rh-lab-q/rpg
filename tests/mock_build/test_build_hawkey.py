from tests.support import RpgTestCase
from rpg import Base
import os


class BuildHawkeyTest(RpgTestCase):

    def test_hawkey_project(self):
        self.base = Base()
        self.base.sack = self.base.load_dnf_sack()
        self.base.load_plugins()
        self.base.load_project_from_url(
            r"https://github.com/rpm-software-management/"
            "hawkey/archive/hawkey-0.5.7-1.tar.gz")
        self.base.spec.Name = "hawkey"
        self.base.spec.Version = "0.6.0"
        self.base.spec.Release = "1%{?snapshot}%{?dist}"
        self.base.spec.License = "LGPLv2+"
        self.base.spec.Summary = ("Library providing simplified "
                                  "C and Python API to libsolv")
        self.base.spec.description = ("A Library providing simplified "
                                      "C and Python API to libsolv.")
        self.base.spec.URL = (r"https://github.com/rpm-"
                              "software-management/%{name}")
        self.base.target_arch = "x86_64"
        self.base.target_distro = "fedora-22"
        self.base.fetch_repos(self.base.target_distro, self.base.target_arch)
        self.base.run_extracted_source_analysis()
        self.base.run_patched_source_analysis()
        self.base.spec.build.append(["make doc-man"])
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
