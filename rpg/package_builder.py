from getpass import getuser
from subprocess import call, check_output, PIPE, Popen, STDOUT
from rpg.utils import move_file


class PackageBuilder:

    def _get_last_word(self, args):
        words = args.split()
        word_count = len(words)
        return words[word_count - 1]

    def _parse_error(self, log_path):
        _ret = []
        f = open(log_path + "/build.log", "r")
        write = False
        for line in f:
            if not write:
                write = "EXCEPTION" in str(line)
            if write:
                _ret.append(str(line).replace('\n', ''))
        return _ret

    def build(self, spec_file, tarball, distro=None, arch=None):
        """builds RPM package in mock from given spec_file and tarball,
           returns None or string in case of error occurrence"""
        call(["rpmdev-setuptree", ""])
        user = getuser()
        move_file(str(spec_file), "/home/" + user + "/rpmbuild/SPECS/")
        move_file(str(tarball), "/home/" + user + "/rpmbuild/SOURCES/")
        spec_name = self._get_last_word(str(spec_file))
        result = check_output(
            ["rpmbuild", "-bs", "/home/" + user + "/rpmbuild/SPECS/" + spec_name])
        srpm_path = self._get_last_word(result)
        p = Popen(
            ["mock", "-r", distro, srpm_path], stdout=PIPE, stderr=STDOUT)
        line = ""
        logs = ""
        while p.poll() is None:
            line = str(p.stdout.readline())
            if "INFO: Results and/or logs in:" in line:
                logs = line
        result = str(self._get_last_word(logs).replace("\\n'", ""))
        if not "Finish: run" in line:
            return self._parseError(result)
