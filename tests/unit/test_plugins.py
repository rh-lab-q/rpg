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


class MockSack:

    def query(self):
        return MockedDNFQuery()


class MockedPackage:
    name = "python3-dnf"


class MockedDNFQuery:

    def filter(self, **kwd):
        return [MockedPackage()]

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
                 ('/Makefile', None, None),
                 ('/py/requires/sourcecode2.py', None, None)]
        excludes = [('/patch/__pycache__/', r'%exclude', None),
                    ('/c/__pycache__/', r'%exclude', None),
                    ('/hello_project/__pycache__/', r'%exclude', None),
                    ('/py/__pycache__/', r'%exclude', None),
                    ('/py/requires/__pycache__/', r'%exclude', None),
                    ('/translation/__pycache__/', r'%exclude', None),
                    ('/libs/__pycache__/', r'%exclude', None),
                    ('/archives/__pycache__/', r'%exclude', None),
                    ('/__pycache__/', r'%exclude', None),
                    ('/srpm/__pycache__/', '%exclude', None)]
        sorted_files = sorted(files + excludes, key=lambda e: e[0])
        self.assertEqual(self.spec.files,
                         sorted_files)

    def test_find_translation_file(self):
        plugin = FindTranslationPlugin()
        plugin.installed(self.test_project_dir,
                         self.spec, self.sack)
        translation_file = ("-f %{CZ.mo}.lang")
        self.assertEqual(self.spec.files[0],
                        (translation_file, None, None))

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

    def test_files_to_pkgs(self):
        ftpp = FilesToPkgsPlugin()
        self.spec.required_files = set([
            "/usr/lib/python3.4/site-packages/dnf/conf/read.py",
            "/usr/lib/python3.4/site-packages/dnf/yum/sqlutils.py",
            "/usr/lib/python3.4/site-packages/dnf/query.py"
        ])
        ftpp.installed(None, self.spec, MockSack())
        self.assertEqual(len(self.spec.Requires), 1)
        self.assertEqual(set(["python3-dnf"]), self.spec.Requires)

    def test_c(self):
        c_plug = CPlugin()
        c_plug.patched(self.test_project_dir, self.spec, self.sack)
        expected = set(['/usr/include', '/usr/include/bits',
                        '/usr/include/gnu', '/usr/include/sys'])
        self.assertEqual(self.spec.required_files, expected)
        self.assertEqual(self.spec.build_required_files, expected)
