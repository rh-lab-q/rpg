from tests.support import PluginTestCase
from rpg.plugins.lang.python import PythonPlugin
from rpg.plugins.misc.find_patch import FindPatchPlugin, _is_patch
from rpg.plugins.misc.find_file import FindFilePlugin
from rpg.plugins.misc.find_translation import FindTranslationPlugin
from rpg.plugins.misc.find_library import FindLibraryPlugin
from rpg.plugins.misc.files_to_pkgs import FilesToPkgsPlugin
from rpg.utils import get_architecture
import sys
from rpg.plugins.lang.c import CPlugin
from rpg.spec import Spec
from unittest import mock
from rpg.plugins.project_builder.cmake import CMakePlugin
from rpg.plugins.project_builder.setuptools import SetuptoolsPlugin
from rpg.plugins.project_builder.autotools import AutotoolsPlugin


class MockSack:

    def query(self):
        return MockedDNFQuery()


class MockedPackage:

    def __init__(self, package):
        self.name = package

    files = []


class MockedLogging:

    called = 0

    @classmethod
    def log(cls, *args, **kwargs):
        cls.called += 1


class MockedDNFQuery:

    def filter(self, **kwd):
        if kwd["file"] == "/usr/lib/python3.4/site-packages/dnf/conf/read.py":
            return [MockedPackage("python3-dnf")]
        raise IndexError

    def available(self):
        return self


class FindPatchPluginTest(PluginTestCase):

    def setUp(self):
        self.spec = Spec()
        self.sack = None

    def test_is_patch(self):
        patch = self.test_project_dir / "patch" / "0.patch"
        not_patch = self.test_project_dir / "c" / "sourcecode.c"
        self.assertTrue(_is_patch(patch))
        self.assertFalse(_is_patch(not_patch))

    def test_find_patch(self):
        plugin = FindPatchPlugin()
        plugin.extracted(self.test_project_dir / "patch",
                         self.spec, self.sack)
        expected_patches = {'tests/project/patch/2.patch',
                            'tests/project/patch/0.patch',
                            'tests/project/patch/1.patch'}
        self.assertEqual(expected_patches, set(self.spec.Patch))

    def test_find_files(self):
        plugin = FindFilePlugin()
        plugin.installed(self.test_project_dir,
                         self.spec, self.sack)
        files = [('/patch/0.patch', None, None),
                 ('/patch/1.patch', None, None),
                 ('/patch/2.patch', None, None),
                 ('/c/sourcecode.c', None, None),
                 ('/hello_project/hello-1.4.tar.gz', None, None),
                 ('/py/plugin0.py', None, None),
                 ('/py/sourcecode.py', None, None),
                 ('/translation/CZ.mo', None, None),
                 ('/libs/libstatic.a', None, None),
                 ('/libs/libdynamic.so.1', None, None),
                 ('/srpm/test.src.rpm', None, None),
                 ('/srpm/fail.src.rpm', None, None),
                 ('/archives/sample.tar.gz', None, None),
                 ('/archives/sample.tar.xz', None, None),
                 ('/archives/rpg-0.0.2-1.tar.gz', None, None),
                 ('/Makefile', None, None),
                 ('/py/requires/sourcecode2.py', None, None),
                 ('/mock_project/mock-1.0.tar.gz', None, None),
                 ('/c/CMakeCache.txt', None, None),
                 ('/c/CMakeLists.txt', None, None),
                 ('/setuptools/setup.py', None, None),
                 ('/setuptools/testscript.py', None, None),
                 ('/autotools/configure.ac', None, None),
                 ('/autotools/Makefile.am', None, None)]
        excludes = [('/patch/__pycache__/', r'%exclude', None),
                    ('/c/__pycache__/', r'%exclude', None),
                    ('/hello_project/__pycache__/', r'%exclude', None),
                    ('/py/__pycache__/', r'%exclude', None),
                    ('/py/requires/__pycache__/', r'%exclude', None),
                    ('/translation/__pycache__/', r'%exclude', None),
                    ('/libs/__pycache__/', r'%exclude', None),
                    ('/archives/__pycache__/', r'%exclude', None),
                    ('/__pycache__/', r'%exclude', None),
                    ('/srpm/__pycache__/', '%exclude', None),
                    ('/mock_project/__pycache__/', '%exclude', None),
                    ('/setuptools/__pycache__/', '%exclude', None),
                    ('/autotools/__pycache__/', '%exclude', None)]
        sorted_files = sorted(files + excludes, key=lambda e: e[0])
        self.assertEqual(sorted(list(self.spec.files)),
                         sorted_files)

    def test_find_translation_file(self):
        plugin = FindTranslationPlugin()
        plugin.installed(self.test_project_dir,
                         self.spec, self.sack)
        translation_file = ("-f %{CZ.mo}.lang")
        self.assertTrue((translation_file, None, None) in self.spec.files)

    def test_find_library(self):
        plugin = FindLibraryPlugin()
        plugin.installed(self.test_project_dir,
                         self.spec, self.sack)
        lib = "-p /sbin/ldconfig"
        self.assertEqual(str(self.spec.post), lib)
        self.assertEqual(str(self.spec.postun), lib)

    def test_python_find_requires(self):
        # FIXME when ORed files considered
        plugin = PythonPlugin()
        plugin.patched(self.test_project_dir / "py" / "requires",
                       self.spec, self.sack)
        version = sys.version_info
        arch = get_architecture()
        if arch == 32:
            arch = ""
        imports = [("/usr/lib{0}/python{1}.{2}/" +
                    "lib-dynload/math.cpython-{1}{2}m.so")
                   .format(arch, version.major, version.minor)]
        self.assertEqual(self.spec.required_files, set(imports))

    @mock.patch("logging.log", new=MockedLogging.log)
    def test_files_to_pkgs(self):
        ftpp = FilesToPkgsPlugin()
        self.spec.required_files = {
            "/usr/lib/python3.4/site-packages/dnf/conf/read.py",
            "/usr/lib/python3.4/site-packages/dnf/yum/sqlutils.py",
            "/usr/lib/python3.4/site-packages/dnf/query.py"
        }
        ftpp.installed(None, self.spec, MockSack())
        self.assertEqual(len(self.spec.Requires), 1)
        self.assertEqual({"python3-dnf"}, self.spec.Requires)
        self.assertEqual(set(), self.spec.BuildRequires)
        self.assertEqual(MockedLogging.called, 2)
        self.spec.check.append("pwd")
        ftpp.installed(None, self.spec, MockSack())
        self.assertEqual({"python3-dnf"}, self.spec.BuildRequires)
        self.assertEqual(MockedLogging.called, 2)

    def test_c(self):
        c_plug = CPlugin()
        c_plug.patched(self.test_project_dir, self.spec, self.sack)
        expected = set([
            "/usr/include/stdc-predef.h",
            "/usr/include/stdlib.h",
            "/usr/include/features.h",
            "/usr/include/sys/cdefs.h",
            "/usr/include/bits/wordsize.h",
            "/usr/include/gnu/stubs.h",
            "/usr/include/gnu/stubs-64.h",
            "/usr/lib/gcc/x86_64-redhat-linux/5.1.1/include/stddef.h",
            "/usr/include/bits/stdlib-float.h",
            "/usr/include/stdio.h",
            "/usr/include/bits/types.h",
            "/usr/include/bits/typesizes.h",
            "/usr/include/libio.h",
            "/usr/include/_G_config.h",
            "/usr/include/wchar.h",
            "/usr/lib/gcc/x86_64-redhat-linux/5.1.1/include/stdarg.h",
            "/usr/include/bits/stdio_lim.h",
            "/usr/include/bits/sys_errlist.h"
        ])
        self.assertEqual(self.spec.required_files, expected)
        self.assertEqual(self.spec.build_required_files, expected)

    def test_cmake(self):
        cmakeplug = CMakePlugin()
        cmakeplug.patched(self.test_project_dir / "c", self.spec, self.sack)
        self.assertEqual(str(self.spec.check), "make test")
        expected = set(["/usr/bin/gmake", "/usr/bin/file",
                        "/usr/bin/makedepend", "/usr/bin/nosetests-3.4",
                        "/usr/bin/python3.4"])
        cmakeplug.compiled(self.test_project_dir / "c", self.spec, self.sack)
        self.assertEqual(self.spec.build_required_files, expected)
        self.assertEqual(self.spec.required_files, expected)

    def test_setuptools(self):
        setuptplug = SetuptoolsPlugin()
        setuptplug.patched(
            self.test_project_dir / "setuptools", self.spec, self.sack)
        self.assertEqual(self.spec.BuildRequires, {"python3-setuptools"})
        self.assertEqual(str(self.spec.build), "python3 setup.py build")
        self.assertEqual(
            str(self.spec.install),
            "python3 setup.py install --skip-build --root $RPM_BUILD_ROOT")

    def test_autotools(self):
        autotplug = AutotoolsPlugin()
        expected = set(["autoconf", "automake", "libtool",
                        "test1 >= 2.36.0", "test2.1 >= test1.0",
                        "test2.2", "test3.1 >= 0.4.6", "test3.2 >= 1.7.11",
                        "test3.3 >= 4.11.0", "test4 <= test5", "test5.1",
                        "test5.2", "test6 > test5", "test7.1", "test7.2",
                        "test7.3", "test8.1 = doNotKnowIfViableButItWorks",
                        "test8.2", "test9.1", "test9.2"])
        autotplug.patched(
            self.test_project_dir / "autotools", self.spec, self.sack)
        self.assertEqual(self.spec.BuildRequires, expected)
        self.assertEqual(
            str(self.spec.build),
            "autoreconf --install --force\n"
            "./configure\nmake")
        self.assertEqual(
            str(self.spec.install),
            "make install DESTDIR=$RPM_BUILD_ROOT")
