from support import RpgTestCase
from rpg.command import Command


class PluginEngineTest(RpgTestCase):

    def test_command_concat(self):
        cmd = Command("cd %s" % self.test_project_dir)
        cmd.append_cmdline("cmake ..")
        cmd.append_cmdline(["make", "make test"])
        expected = "cd %s\ncmake ..\nmake\nmake test" % self.test_project_dir
        self.assertEqual(expected, str(cmd))

    def test_command_execute(self):
        cmd = Command(["pwd", "cd c", "pwd"])
        output = cmd.execute(self.test_project_dir)
        path = self.test_project_dir.resolve()
        expected = "%s\n%s/c\n" % (path, path)
        self.assertEqual(expected, output)
