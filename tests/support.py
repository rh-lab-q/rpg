from pathlib import Path
from unittest import mock, TestCase
from rpg.spec import Spec


class RpgTestCase(TestCase):
    test_project_dir = Path("tests/project")
    
    def assertExistInDir(self, expected, pathlibobject):
        path = Path(pathlibobject)
        for files in expected:
            self.assertTrue((path / files).exists(), msg=files)

class PluginTestCase(RpgTestCase):
    sack = mock.MagicMock()
    spec = Spec()
