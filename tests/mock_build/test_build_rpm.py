from rpg.package_builder import PackageBuilder, BuildException
from tests.support import RpgTestCase
from rpg.command import Command
from rpg.utils import path_to_str


class PackageBuilderTest(RpgTestCase):

    @classmethod
    def setUpClass(cls):
        cls.distro = "fedora-22"
        cls.arch = "x86_64"
        cls.package_builder = PackageBuilder()
        cls.package_builder.fetch_repos(cls.distro, cls.arch)

    def setUp(self):
        self.srpm = RpgTestCase.test_project_dir / "srpm"
        self.fail_srpm = self.srpm / "fail.src.rpm"
        self.test_srpm = self.srpm / "test.src.rpm"

    def test_build_rpm(self):
        with self.assertRaises(BuildException) as be:
            self.package_builder.build_rpm(self.test_srpm,
                                           PackageBuilderTest.distro,
                                           PackageBuilderTest.arch,
                                           self.srpm)
            self.assertEqual(
                be.errors,
                [])

    def test_build_rpm_fail(self):
        with self.assertRaises(BuildException) as be:
            self.package_builder.build_rpm(self.fail_srpm,
                                           PackageBuilderTest.distro,
                                           PackageBuilderTest.arch,
                                           self.srpm)
            self.assertNotEqual(
                be.errors,
                [])

    def tearDown(self):
        Command("rm -rf " + path_to_str(self.srpm) + "/mock_logs " +
                path_to_str(self.package_builder.temp_dir / "*.rpm")).execute()
