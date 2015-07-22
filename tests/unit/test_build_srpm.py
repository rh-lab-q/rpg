from tests.support import RpgTestCase
from rpg import Base
from rpg.package_builder import PackageBuilder
from rpg.spec import Spec
from pathlib import Path
import os


class FakeBase(Base):

    base_dir = Path(RpgTestCase.test_project_dir / "hello_project")
    project_name = "hello"

    def __init__(self):
        self._package_builder = PackageBuilder()
        self.spec = Spec()
        self.spec.Name = "hello"
        self.spec.Version = "1.4"
        self.spec.Release = "1%{?dist}"
        self.spec.Summary = "Hello World test program"
        self.spec.License = "GPLv2"
        self.spec.Source = "hello-1.4.tar.gz"
        self.spec.description = "Hello World C project for testing RPG."
        self.spec.prep = r'%autosetup'
        self.spec.build = "make"
        self.spec.install = r"make install DESTDIR=%{RPM_BUILD_ROOT}"


class BuildSrpmTest(RpgTestCase):

    def setUp(self):
        self.fbase = FakeBase()

    def test_build_srpm(self):
        self.fbase.build_srpm()
        self.fbase.srpm_path

    def tearDown(self):
        os.remove(str(self.fbase.srpm_path))
        os.remove(str(self.fbase.spec_path))
