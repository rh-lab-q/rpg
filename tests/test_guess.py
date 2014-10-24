from support import RpgTestCase
from rpg import Base


class GuessTest(RpgTestCase):

    def setUp(self):
        self.base = Base()

    def test_guess_name(self):
        self.base._input_name = self.test_project_dir
        self.assertEqual(str(self.base.guess_name()), str(self.test_project_dir))
        self.base._input_name = "vec.zip"
        self.assertEqual(str(self.base.guess_name()), "vec")
        self.base._input_name = "vec.tar.gz"
        self.assertEqual(str(self.base.guess_name()), "vec")
        self.base._input_name = "vec.zip.zip"
        self.assertEqual(str(self.base.guess_name()), "vec.zip")

    def test_guess_name_fail(self):
        self.base._input_name = self.test_project_dir / "NotADir"
        self.assertEqual(str(self.base.guess_name()), str(""))
