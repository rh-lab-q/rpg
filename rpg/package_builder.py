from os.path import expanduser
from subprocess import call
from rpg.utils import copy_file
from rpg.command import Command


class PackageBuilder(object):

    @staticmethod
    def _parse_error(log_path):
        _ret = []
        build_log = open(log_path + "/build.log", "r")
        write = False
        for line in build_log:
            if not write:
                write = "EXCEPTION" in str(line)
            if write:
                _ret.append(str(line).replace('\n', ''))
        return _ret

    @staticmethod
    def build_srpm(spec_file, tarball, output_file):
        """builds RPM package with build_srpm and build_rpm"""

        # Build srpm pakcage from given spec_file and tarball
        call(["rpmdev-setuptree", ""])
        Command("cp " + str(tarball) + " ~/rpmbuild/SOURCES").execute()
        output = Command("rpmbuild -bs " + str(spec_file)).execute()
        Command("mv " + str(output.split()[-1]) +
                " " + str(output_file)).execute()
                
    def fetch_repos(self, dist, arch):
        config_file = dist + '-' + arch
        Command("mock --init --no-clean -r " + config_file).execute()
