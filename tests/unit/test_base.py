from tests.support import RpgTestCase
from rpg import Base
import re


class BaseTest(RpgTestCase):

    def setUp(self):
        self.base = Base()

    def test_checksum(self):
        shasum = self.base.compute_checksum(self.test_project_dir / "patch")
        self.assertTrue(re.match(r"^[0-9a-fA-F]{7}$",
                                 shasum))
        shasum2 = self.base.compute_checksum(self.test_project_dir / "patch" /
                                             "0.patch")
        self.assertTrue(re.match(r"^[0-9a-fA-F]{7}$",
                                 shasum2))

    def test_base_dir(self):
        self.assertRaises(RuntimeError, getattr, self.base, "base_dir")
        self.base.load_project_from_url(self.test_project_dir / "c")
        self.assertTrue(re.match(r"^\/tmp\/rpg-c-[0-9a-fA-F]+$",
                                 str(self.base.base_dir)))
