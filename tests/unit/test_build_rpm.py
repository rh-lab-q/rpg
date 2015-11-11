from rpg.package_builder import PackageBuilder, BuildException
from tests.support import RpgTestCase
from unittest import mock
from pathlib import Path


class MockedSTDOUT(object):

    def __init__(self, string):
        self.string = string

    def readline(self):
        return self.string


class MockedSubprocess(object):

    PIPE = None
    STDOUT = None

    MockedText = [
        b'INFO: EXCEPTION: Command failed. See logs for output.\n',
        b' # bash --login -c /usr/bin/rpmbuild -bb --target x86_64 --nodeps' +
        b'  /builddir/build/SPECS/a.spec \n',
        b'Traceback (most recent call last):\n',
        b'  File "/usr/lib/python3.4/site-packages/mockbuild/' +
        b'trace_decorator.py", line 84, in trace\n',
        b'    result = func(*args, **kw)\n',
        b'  File "/usr/lib/python3.4/site-packages/mockbuild/util.py",' +
        b' line 494, in do\n',
        b'    raise exception.Error("Command failed. See logs for output.\\n' +
        b' # %s" % (command,), child.returncode)\n',
        b'mockbuild.exception.Error: Command failed. See logs for output.\n',
        b' # bash --login -c /usr/bin/rpmbuild -bb --target x86_64 --nodeps' +
        b'  /builddir/build/SPECS/a.spec \n',
        b'INFO: LEAVE do --> EXCEPTION RAISED\n',
    ]

    ErrorText = [
        b'INFO: EXCEPTION: Command failed. See logs for output.\n',
        b'    raise exception.Error("Command failed. ' +
        b'See logs for output.\\n # %s" % (command,), child.returncode)\n',
        b'mockbuild.exception.Error: Command failed. See logs for output.\n',
        b'INFO: LEAVE do --> EXCEPTION RAISED\n',
    ]

    def __init__(self, cmd):
        self.cmd = cmd
        self.poll_ite = 10

    @staticmethod
    def Popen(cmd, **kwargs):
        return MockedSubprocess(cmd)

    def poll(self):
        self.poll_ite -= 1
        self.stdout = MockedSTDOUT(MockedSubprocess.MockedText[self.poll_ite])
        return None if self.poll_ite != -1 else True

    @staticmethod
    def returncode(self):
        return 1


class BuildLogParseTest(RpgTestCase):

    @mock.patch('subprocess.Popen', new=MockedSubprocess.Popen)
    @mock.patch('subprocess.PIPE', new=MockedSubprocess.PIPE)
    @mock.patch('subprocess.STDOUT', new=MockedSubprocess.STDOUT)
    @mock.patch('rpg.command.Command.execute', new=lambda *args: args)
    @mock.patch('rpg.package_builder.PackageBuilder._check_logs',
                new=lambda *args: args)
    def test_rpm_build_err_parse(self):
        with self.assertRaises(BuildException) as be:
            PackageBuilder().build_rpm(
                "", "", "", Path(""))
            self.assertEqual(
                sorted(be.errors),
                sorted([text.decode("utf-8")
                        for text in MockedSubprocess.ErrorText]))
