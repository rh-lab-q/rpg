from tests.support import RpgTestCase
from rpg.spec import Spec
from rpg.command import Command


class SpecTest(RpgTestCase):

    def setUp(self):
        self.spec = Spec()

    def test_spec_assignment(self):
        self.assertEqual("", self.spec.Name)
        self.assertTrue(isinstance(self.spec.build, Command))
        self.assertEqual("", str(self.spec.build))
        self.spec.build = Command(["cmake .", "make"])
        self.assertTrue(isinstance(self.spec.build, Command))
        self.spec.install = Command("make install")
        self.assertTrue(isinstance(self.spec.install, Command))
        self.spec.check = Command("make test")
        self.assertTrue(isinstance(self.spec.check, Command))

        self.assertTrue(isinstance(self.spec.Requires, set))
        self.spec.Requires.add("python3")
        self.assertTrue(isinstance(self.spec.Requires, set))
        self.spec.Requires.add("python3-qt5")

        self.spec.Requires = sorted(list(self.spec.Requires))

        expected = "Requires:\tpython3\n" \
            "Requires:\tpython3-qt5\n" \
            "%build\ncmake .\nmake\n\n" \
            "%install\nmake install\n\n" \
            "%check\nmake test\n\n"
        self.assertEqual(expected, str(self.spec))

        self.spec.files = [("f1", "a1", ""),
                           ("f2", "a2", ""),
                           ("f3", "a3", "")]
        expected += "%files\n" \
                    "a1 f1\n"  \
                    "a2 f2\n"  \
                    "a3 f3\n\n"
        self.assertEqual(expected, str(self.spec))
        

    def test_spec_getter_fail(self):
        self.assertRaises(AttributeError, getattr, self.spec, "bla")

