from subprocess import check_output
import rpm


class Command:

    """representation of scripts in spec file"""

    def __init__(self, cmdline=None):
        """cmdline could be list of strings or string containing multiple lines
           """

        self.rpm_variables = []
        self._command_lines = []
        if cmdline:
            self.append(cmdline)

    def __str__(self):
        """join command lines together. Returns one string that will be saved
           in spec file"""

        return "\n".join(self._command_lines)

    def __repr__(self):
        return "Command(%s)" % repr(str(self))

    def __eq__(self, other):
        return self._command_lines == other._command_lines

    def append(self, cmdline):
        """adds cmdline at the end of command sequence
           cmdline could be list of strings or string containing multiple lines
           """

        if isinstance(cmdline, list):
            self._command_lines.extend(cmdline)
        elif isinstance(cmdline, str):
            self._command_lines.extend(cmdline.strip().split("\n"))
        else:
            msg = "Only list of command strings or command string is accepted"
            raise TypeError(msg)

    def execute(self, binary=False):
        """executes command in any dir, can raise CalledProcessError"""

        command_lines = self._assign_rpm_variables() + self._command_lines
        return cmd_output(command_lines, binary)

    def execute_from(self, work_dir):
        """executes command in work_dir (instance of pathlib.Path),
           can raise CalledProcessError"""

        cd_workdir = ["cd %s" % str(work_dir.resolve()).replace(" ", "\\ ")]
        command_lines = self._assign_rpm_variables() + cd_workdir + \
            [rpm.expandMacro(x) for x in self._command_lines]
        return cmd_output(command_lines)

    def _assign_rpm_variables(self):
        return ['%s="%s"' % (v, p) for (v, p) in self.rpm_variables]


def cmd_output(cmdlines, binary=False):
    output = check_output(["/bin/sh", "-c", " && ".join(cmdlines)])
    return output if binary else output.decode('utf-8')
