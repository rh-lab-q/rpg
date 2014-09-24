from support import PluginTestCase
from rpg.plugins.misc.find_patch import FindPatchPlugin, _is_patch
from rpg.plugins.misc.find_file import FindFilePlugin
from rpg.plugins.misc.find_translation import FindTranslationPlugin
from rpg.plugins.misc.find_library import FindLibraryPlugin
from unittest import mock


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
        patch_order = ['tests/project/patch/0.patch',
                       'tests/project/patch/1.patch',
                       'tests/project/patch/2.patch']
        self.assertEqual(self.spec.tags.__setitem__.call_args_list,
                         [mock.call('patch', patch_order)])

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
        self.assertEqual(self.spec.files.append.call_args_list,
                         [mock.call(sorted_files)])

    def test_find_translation_file(self):
        plugin = FindTranslationPlugin()
        plugin.installed(self.test_project_dir,
                         self.spec, self.sack)
        translation_file = ("-f %{CZ.mo}.lang")
        self.assertEqual(self.spec.files.insert.call_args,
                         mock.call(0, translation_file))

    def test_find_library(self):
        plugin = FindLibraryPlugin()
        plugin.installed(self.test_project_dir,
                         self.spec, self.sack)
        lib = "-p /sbin/ldconfig"
        self.assertEqual(self.spec.scripts.__setitem__.call_args_list,
                         [mock.call('post', lib), mock.call('postun', lib)])
