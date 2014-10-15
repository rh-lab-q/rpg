from support import PluginTestCase
from rpg.command import Command
from rpg.plugins.lang.python import PythonPlugin
from rpg.plugins.misc.find_patch import FindPatchPlugin, _is_patch
from rpg.plugins.misc.find_file import FindFilePlugin
from rpg.plugins.misc.find_translation import FindTranslationPlugin
from rpg.plugins.misc.find_library import FindLibraryPlugin
from rpg.plugins.project_builder.make import MakePlugin
from rpg.utils import get_architecture
import sys


class FindPatchPluginTest(PluginTestCase):

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
        files = [('tests/project/patch/0.patch', None, None),
                 ('tests/project/patch/1.patch', None, None),
                 ('tests/project/patch/2.patch', None, None),
                 ('tests/project/c/sourcecode.c', None, None),
                 ('tests/project/py/plugin0.py', None, None),
                 ('tests/project/py/sourcecode.py', None, None),
                 ('tests/project/translation/CZ.mo', None, None),
                 ('tests/project/libs/libstatic.a', None, None),
                 ('tests/project/libs/libdynamic.so.1', None, None)]
        sorted_files = sorted(files, key=lambda e: e[0])
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
                   .format(arch, version.major, version.minor),
                   str(self.test_project_dir / "py" /
                       "requires" / "sourcecode2.py")]
        self.spec.Requires.sort()
        imports.sort()
        self.assertEqual(self.spec.Requires, imports)
