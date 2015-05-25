from support import RpgTestCase
from rpg import Base
from rpg.package_builder import PackageBuilder
from rpg.spec import Spec
from pathlib import Path
import shutil


class FakeBase(Base):

    def __init__(self):
        pass

    base_dir = Path(RpgTestCase.test_project_dir / "hello_project")
    project_name = "hello"
    spec = Spec()
    spec.Source = "hello-1.4.tar.gz"


class BuildSrpmTest(RpgTestCase):

    def setUp(self):
        self.fbase = FakeBase()

    def test_build_srpm(self):
        PackageBuilder.build_srpm(
            self.fbase.spec_path, self.fbase.archive_path, self.fbase.base_dir)
        self.assertTrue(self.fbase.srpm_path.exists())

    def TearDown(self):
        shutil.rmtree(str(self.fbase.base_dir))
