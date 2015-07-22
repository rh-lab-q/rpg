from rpg.package_builder import PackageBuilder
from tests.support import RpgTestCase


class PackageBuilderTest(RpgTestCase):

    @classmethod
    def setUpClass(cls):
        cls.distro = "fedora-22"
        cls.arch = "x86_64"
        PackageBuilder.fetch_repos(cls.distro, cls.arch)

    def setUp(self):
        self.fail_srpm = RpgTestCase.test_project_dir / "srpm" / "fail.src.rpm"
        self.test_srpm = RpgTestCase.test_project_dir / "srpm" / "test.src.rpm"

    def test_build_rpm(self):
        self.assertEqual(
            PackageBuilder.build_rpm(self.test_srpm,
                                     PackageBuilderTest.distro,
                                     PackageBuilderTest.arch),
            [])

    def test_build_rpm_fail(self):
        self.assertNotEqual(
            PackageBuilder.build_rpm(self.fail_srpm,
                                     PackageBuilderTest.distro,
                                     PackageBuilderTest.arch),
            [])
