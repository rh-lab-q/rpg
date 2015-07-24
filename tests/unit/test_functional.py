from tests.support import RpgTestCase
from rpg import Base


class FunctionalTest(RpgTestCase):

    def test_c_project(self):
        base = Base()
        base.load_plugins()
        base.load_project_from_url(
            self.test_project_dir / "hello_project/hello-1.4.tar.gz")
        base.spec.Name = "hello"
        base.spec.Version = "1.4"
        base.spec.Release = "1%{?dist}"
        base.spec.License = "GPLv2"
        base.spec.Summary = "Hello World test program"
        base.spec.description = "desc"
        base.spec.build = "make"
        base.run_raw_sources_analysis()
        base.run_patched_sources_analysis()
        expected_required_files = {
            "/usr/include/gnu",
            "/usr/include",
            "/usr/include/sys",
            "/usr/include/bits"
        }
        expected_build_required_files = {
            "/usr/include/gnu",
            "/usr/include",
            "/usr/include/sys",
            "/usr/include/bits"
        }
        dirs = [
            "Makefile",
            "hello.c",
            "hello"
        ]
        base.run_installed_analysis()
        self.assertEqual(set(["make"]), base.spec.BuildRequires)
        self.assertEqual(expected_required_files,
                         set(base.spec.required_files))
        self.assertEqual(expected_build_required_files,
                         set(base.spec.build_required_files))
        self.assertExistInDir(["Makefile", "hello.c"], base.extracted_dir)
        base.build_project()
        self.assertExistInDir(dirs, base.compiled_dir)
        base.run_compiled_analysis()
        base.install_project()
        base.run_installed_analysis()
        self.assertEqual([
            ("/hello", None, None),
            ("/__pycache__/", r"%exclude", None)
        ].sort(), base.spec.files.sort())
        base.build_srpm()
        self.assertTrue(base.srpm_path.exists())
