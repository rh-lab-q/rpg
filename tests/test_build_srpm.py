from support import RpgTestCase
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
    spec.Source = "hello-1.4.tar.gz"


class BuildSrpmTest(RpgTestCase):

    def setUp(self):
        self.fbase = FakeBase()

    def test_build_srpm(self):
        self.fbase.build_srpm()
        self.fbase.srpm_path

    def tearDown(self):
        os.remove(str(self.fbase.srpm_path))
