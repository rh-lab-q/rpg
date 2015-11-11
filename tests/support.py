from pathlib import Path
from unittest import mock, TestCase
from rpg.spec import Spec
import tarfile


class RpgTestCase(TestCase):
    test_project_dir = Path("tests/project")

    def assertExistInDir(self, expected, pathlibobject):
        path = Path(pathlibobject)
        for files in expected:
            self.assertTrue((path / files).exists(), msg=files)

    def assertTarEqualDir(self, t, d):
        def _get_tar_files(t):
            with tarfile.open(str(t)) as tar:
                return set(tar.getnames())

        def _get_dir_files(d):
            return set([str(f.relative_to(d)) for f in d.glob("**/*")])

        self.assertEqual(_get_tar_files(Path(t)), _get_dir_files(Path(d)))


class PluginTestCase(RpgTestCase):
    sack = mock.MagicMock()
    spec = Spec()
