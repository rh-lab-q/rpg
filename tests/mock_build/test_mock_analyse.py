from rpg.package_builder import PackageBuilder
from rpg.command import Command
from rpg.spec import Spec
from rpg.utils import path_to_str
from rpg import Base
from tests.support import RpgTestCase
from pathlib import Path


class FakeConf(object):

    exclude = ""
    directories = []


class FakeBase(Base):

    base_dir = Path(RpgTestCase.test_project_dir / "mock_project")
    project_name = "mock"

    def __init__(self):
        self.spec = Spec()
        self.spec.Name = "mock"
        self.spec.Version = "1.0"
        self.spec.Release = "1%{?dist}"
        self.spec.Summary = "Hello World test program"
        self.spec.License = "GPLv2"
        self.spec.Source = "mock-1.0.tar.gz"
        self.spec.description = "Hello World C project for testing RPG."
        self.spec.prep = r'%autosetup'
        self.spec.build = "make"
        self.sack = self.load_dnf_sack()
        self._package_builder = PackageBuilder()
        self.conf = FakeConf()
        self.load_plugins()


class MockAnalyseTest(RpgTestCase):

    @classmethod
    def setUpClass(cls):
        PackageBuilder.fetch_repos("fedora-22", "x86_64")

    def setUp(self):
        self.base = FakeBase()

    def test_mock_analyse(self):
        self.base.build_rpm_recover("fedora-22",
                                    "x86_64")
        self.assertFalse(self.base.spec.build_required_files)
        self.assertFalse(self.base.spec.required_files)
        self.assertEqual(self.base.spec.Requires,
                         self.base.spec.BuildRequires)
        self.assertEqual(self.base.spec.BuildRequires,
                         set(['python3-nose', 'python-nose', 'doxygen']))
        Command("rm -rf " + path_to_str(FakeBase.base_dir) + "/*rpm " +
                path_to_str(FakeBase.base_dir) + "/*spec " +
                path_to_str(FakeBase.base_dir / "mock_logs")).execute()
