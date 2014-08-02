from support import PluginTestCase
from rpg.plugins.misc.find_patch import FindPatchPlugin, _is_patch
from unittest import mock

class FindPatchPluginTest(PluginTestCase):
    def test_is_patch(self):
        patch = self.test_project_dir / "patch" / "0.patch"
        not_patch = self.test_project_dir / "c" / "sourcecode.c"
        self.assertTrue(_is_patch(patch))
        self.assertFalse(_is_patch(not_patch))

    def test_find_patch(self):
        plugin = FindPatchPlugin()
        plugin.before_patches_applied(self.test_project_dir / "patch",
            self.spec, self.sack)
        patch_order = ['tests/project/patch/0.patch',
            'tests/project/patch/1.patch', 'tests/project/patch/2.patch']
        self.assertEqual(self.spec.tags.__setitem__.call_args_list,
                         [mock.call('patch', patch_order)])
