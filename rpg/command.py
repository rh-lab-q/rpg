from subprocess import check_output


class Command:
    """representation of scripts in spec file"""

    def __init__(self, cmdline=None):
        self.command_lines = []
        if cmdline:
            self.append_cmdline(cmdline)

    def __str__(self):
        """join command lines together. Returns one string that will be saved
           in spec file"""
        return "\n".join(self.command_lines)

    def append_cmdline(self, cmdline):
        # adds cmdline at the end of command sequence
        if isinstance(cmdline, list):
            self.command_lines.extend(cmdline)
        elif isinstance(cmdline, str):
            self.command_lines.append(cmdline)
        else:
            msg = "Only list of command strings or command string is accepted"
            raise TypeError(msg)

    def execute(self, work_dir):
        # executes command in target directory
        self.command_lines.insert(0, "cd %s" % work_dir.resolve())
        o = check_output(["/bin/sh", "-c", " && ".join(self.command_lines)])
        return o.decode('utf-8')
