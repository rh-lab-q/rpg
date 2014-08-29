from pathlib import Path
from unittest import mock, TestCase


class RpgTestCase(TestCase):
    test_project_dir = Path("tests/project")


class PluginTestCase(RpgTestCase):
    sack = mock.MagicMock()
    spec = mock.MagicMock()
