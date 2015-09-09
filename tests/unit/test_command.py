from pathlib import Path
from tests.support import RpgTestCase
from rpg.command import Command
from rpg.utils import path_to_str
import subprocess


class PluginEngineTest(RpgTestCase):

    def test_command_concat(self):
        cmd = Command("cd %s" % path_to_str(self.test_project_dir))
        cmd.append("cmake ..")
        cmd.append(["make", "make test"])
        self.assertRaises(TypeError, cmd.append, 4)
        expected = "cd %s\ncmake ..\nmake\nmake test" %\
            path_to_str(self.test_project_dir)
        self.assertEqual(expected, str(cmd))

    def test_command_execute_from(self):
        cmd = Command("pwd\ncd c 2>/dev/null\npwd")
        output = cmd.execute_from(self.test_project_dir)
        path = path_to_str(self.test_project_dir.resolve())
        expected = "%s\n%s/c\n" % (path, path)
        self.assertEqual(expected, output)

        # doesn't add 'cd work_dir' during execute to command lines
        cur_dir = Path('.')
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            cmd.execute_from(cur_dir)
        expected = "Command '['/bin/sh', '-c', 'cd %s "\
                   "&& pwd && cd c 2>/dev/null && pwd']' "\
                   "returned non-zero exit status 1"\
                   % path_to_str(cur_dir.resolve())
        self.assertEqual(expected, str(ctx.exception))

    def test_execute(self):
        cmd = Command("echo bla")
        output = cmd.execute()
        self.assertEqual("bla\n", output)

    def test_compare(self):
        cmd1 = Command("test")
        cmd2 = Command("test")
        self.assertEqual(cmd1, cmd2)

    def test_new_line(self):
        cmd = Command("a\nb\n")
        self.assertEqual("a\nb", str(cmd))
