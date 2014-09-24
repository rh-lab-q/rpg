from support import RpgTestCase
from rpg import Base


class BaseTest(RpgTestCase):

    def setUp(self):
        self.base = Base()

    def test_checksum(self):
        shasum = self.base.compute_checksum(self.test_project_dir / "patch")
        self.assertEqual("11cd391", shasum)
        shasum2 = self.base.compute_checksum(self.test_project_dir / "patch" /
                                             "0.patch")
        self.assertEqual("db72099", shasum2)

    def test_base_dir(self):
        self.assertRaises(RuntimeError, getattr, self.base, "base_dir")
        self.base.process_archive_or_dir(self.test_project_dir / "c")
        self.assertEqual("/tmp/rpg-c-2fd57e1", str(self.base.base_dir))
