from tests.support import PluginTestCase
from rpg import plugin_engine as engine
from tests.project.py.plugin0 import TestPlugin
from unittest import mock
from rpg.plugins.lang.c import CPlugin
from rpg.spec import Spec


class PluginEngineTest(PluginTestCase):

    def setUp(self):
        self.plugin_engine = engine.PluginEngine(self.spec, self.sack)

    def test_load_plugins(self):
        self.plugin_dir = self.test_project_dir / "py"
        self.plugin_engine.load_plugins(self.plugin_dir)
        self.assertEqual(len(self.plugin_engine.plugins), 1)
        self.assertTrue(
            isinstance(self.plugin_engine.plugins.pop(), TestPlugin))

    def test_exclude_plugins(self):
        self.plugin_dir = self.test_project_dir / "py"
        self.plugin_engine.load_plugins(self.plugin_dir, ["TestPlugin"])
        self.assertEqual(len(self.plugin_engine.plugins), 0)

    def test_exclude_plugins_fail(self):
        self.plugin_dir = self.test_project_dir / "py"
        self.plugin_engine.load_plugins(self.plugin_dir, ["NotAPlugin"])
        self.assertEqual(len(self.plugin_engine.plugins), 1)

    def test_execute_phase(self):
        self.plugin_engine.plugins = [mock.MagicMock()]
        self.plugin_engine.execute_phase(
            engine.phases[0], self.test_project_dir)
        expected_call = [
            mock.call(self.test_project_dir, self.spec, self.sack)]
        plugin_call = getattr(
            self.plugin_engine.plugins[0], engine.phases[0]).call_args_list
        self.assertEqual(plugin_call, expected_call)
