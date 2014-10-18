from pathlib import Path
from unittest import mock, TestCase
from rpg.spec import Spec


class RpgTestCase(TestCase):
    test_project_dir = Path("tests/project")


class PluginTestCase(RpgTestCase):
    sack = mock.MagicMock()
    spec = Spec()
