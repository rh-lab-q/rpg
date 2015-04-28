from os.path import expanduser
from subprocess import call, check_output, PIPE, Popen, STDOUT
from rpg.utils import copy_file
from rpg.command import Command


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

    @staticmethod
    def build_srpm(spec_file, tarball, srpm_output_path):
        p = PackageBuilder()
        call(["rpmdev-setuptree", ""])
        user_home = expanduser("~")
        copy_file(str(spec_file), user_home + "/rpmbuild/SPECS/")
        copy_file(str(tarball), user_home + "/rpmbuild/SOURCES/")
        output = Command("rpmbuild -bs " + user_home + "/rpmbuild/SPECS/" 
            + spec_file.name).execute()
        srpm_path = p._get_last_word(output)
        Command("mv " + str(srpm_path) + " " + str(srpm_output_path)).execute()
        
    def build_rpm(self, srpm_path, distro, arch):
        """builds RPM package in mock from given spec_file and tarball,
           returns None or string in case of error occurrence"""
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
    
    def build(self, spec_file, tarball, distro=None, arch=None):
        """builds RPM package with build_srpm and build_rpm"""
        # FIXME: completely broken
        
        # Get home directory
        srpm_output_path = expanduser("~")
        # Build srpm pakcage from given spec_file and tarball
        self.build_srpm(spec_file, tarball, srpm_output_path)
        # Build RPM package
        self.build_rpm(srpm_path, distro, arch)
