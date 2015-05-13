from support import RpgTestCase
from rpg import Base
from rpg.package_builder import PackageBuilder
from rpg.command import Command
from rpg.spec import Spec
from pathlib import Path

class FakeBase(Base):
    
    def __init__(self):
        pass
    
    base_dir= Path(RpgTestCase.test_project_dir / "hello_project")
    project_name = "hello"
    spec = Spec()
    spec.Source = "hello-1.4.tar.gz"
        

class BuildSrpmTest(RpgTestCase):
    
    def test_build_srpm(self):
        fbase = FakeBase()
        PackageBuilder.build_srpm(fbase.spec_path, fbase.archive_path, fbase.base_dir)
        self.assertTrue(fbase.srpm_path.exists())
        
    def TearDown():
        base = Base()
        Command("rm -r", base.base_dir).execute()

            
