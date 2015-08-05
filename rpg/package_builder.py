import logging
import re
from rpg.command import Command
import subprocess
import tempfile
from pathlib import Path


class PackageBuilder(object):
    regex = re.compile(r"[eE][rR][rR][oO][rR]|" +
                       r"[eE][xX][cC][eE][pP][tT][iI][oO][nN]|" +
                       r"[cC][oO][mM][mM][aA][nN][dD] [nN][oO][tT] " +
                       r"[fF][oO][uU][nN][dD]")

    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir())

    @staticmethod
    def build_srpm(spec_file, tarball, output_dir):
        """builds RPM package with build_srpm and build_rpm"""

        # Build srpm pakcage from given spec_file and tarball
        Command("rpmdev-setuptree").execute()
        Command("cp " + str(tarball) +
                ' $(rpm --eval "%{_topdir}")/SOURCES').execute()
        output = Command("rpmbuild -bs " + str(spec_file)).execute()
        Command("mv " + str(output.split()[-1]) +
                " " + str(output_dir)).execute()

    def check_logs(self):
        with open(str(self.temp_dir) + "/build.log") as build_log:
            for line in build_log.readlines():
                if PackageBuilder.regex.search(line):
                    yield line

    def build_rpm(self, srpm, distro, arch, output_dir):

        def check_output(proc):
            while proc.poll() is None:
                line = proc.stdout.readline().decode("utf-8")
                if PackageBuilder.regex.search(line):
                    yield line

        return list(
            check_output(
                subprocess.Popen(
                    [
                        "mock", "--no-clean",
                        "--no-cleanup-after",
                        "--verbose",
                        "--root", distro + '-' + arch,
                        "--rebuild", str(srpm),
                        "--resultdir=" + str(self.temp_dir)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
            )
        )
        Command("mv " + str(self.temp_dir.glob("*.rpm")[0]) +
                " " + str(output_dir)).execute()

    @staticmethod
    def fetch_repos(dist, arch):
        logging.info("New thread for fetch repos started")
        config_file = dist + '-' + arch
        Command("mock --init -r " + config_file).execute()
