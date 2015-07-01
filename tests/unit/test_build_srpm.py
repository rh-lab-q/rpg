from tests.support import RpgTestCase
from rpg import Base
from rpg.package_builder import PackageBuilder
from rpg.spec import Spec
from pathlib import Path
import os


class FakeBase(Base):

    def __init__(self):
        pass

    base_dir = Path(RpgTestCase.test_project_dir / "hello_project")
    _package_builder = PackageBuilder()
    project_name = "hello"
    spec = Spec()
    spec.Name = "hello"
    spec.Version = "1.4"
    spec.Release = "1%{?dist}"
    spec.Summary = "Hello World test program"
    spec.License = "GPLv2"
    spec.Source = "hello-1.4.tar.gz"
    spec.description = "Hello World C project for testing RPG."
    spec.prep = r'%autosetup'
    spec.build = "make"
    spec.install = r"make install DESTDIR=%{RPM_BUILD_ROOT}"


class BuildSrpmTest(RpgTestCase):

    def setUp(self):
        self.fbase = FakeBase()

    def test_build_srpm(self):
        self.fbase.build_srpm()
        self.fbase.srpm_path

    def tearDown(self):
        os.remove(str(self.fbase.srpm_path))
        os.remove(str(self.fbase.spec_path))
