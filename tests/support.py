from pathlib import Path
from unittest import mock, TestCase

class PluginTestCase(TestCase):
    test_project_dir = Path("tests/project")
    sack = mock.MagicMock()
    spec = mock.MagicMock()
