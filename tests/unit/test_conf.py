import sys
from tests.support import RpgTestCase
from rpg.conf import Conf


class ConfTest(RpgTestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_include_dir(self):
        sys.argv = ["rpg", "--plugin-dir", str(self.test_project_dir / "py")]
        conf = Conf()
        conf.parse_cmdline()
        self.assertEqual(str(['tests/project/py']), str(conf.directories))

    def test_include_dir_fail(self):
        sys.argv = ["rpg", "--plugin-dir", str("NotADir")]
        conf = Conf()
        conf.parse_cmdline()
        self.assertEqual(str(["tests/project/py"]), str(conf.directories))

    def test_exclude_plug(self):
        sys.argv = ["rpg", "--disable-plugin", str("TestPlugin")]
        conf = Conf()
        conf.parse_cmdline()
        self.assertEqual(str(["TestPlugin"]), str(conf.exclude))
