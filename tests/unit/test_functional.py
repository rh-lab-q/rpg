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
        base.run_extracted_source_analysis()
        base.run_patched_source_analysis()
        expected = {
            '/usr/include/stdio.h',
        }
        dirs = [
            "Makefile",
            "hello.c",
            "hello"
        ]
        base.run_installed_source_analysis()
        self.assertEqual(set(["make"]), base.spec.BuildRequires)
        self.assertTrue([ele for ele in base.spec.required_files
                         if ele in expected])
        self.assertTrue([ele for ele in base.spec.build_required_files
                         if ele in expected])
        self.assertExistInDir(["Makefile", "hello.c"], base.extracted_dir)
        base.build_project()
        self.assertExistInDir(dirs, base.compiled_dir)
        base.run_compiled_source_analysis()
        base.install_project()
        base.run_installed_source_analysis()
        self.assertEqual(set([
            ("/hello", None, None)
        ]), base.spec.files)
        base.build_srpm()
        self.assertTrue(base.srpm_path.exists())
