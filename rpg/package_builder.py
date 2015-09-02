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
        self.mock_logs = Path()
        self.mock_return_code = 0

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
        with open(str(self.mock_logs) + "/build.log") as build_log:
            for line in build_log.readlines():
                if PackageBuilder.regex.search(line):
                    yield line

    def build_rpm(self, srpm, distro, arch, output_dir):

        def move_files(output, files):
            if not output.is_dir():
                Command("mkdir " + str(output)).execute()
            for _out in files:
                Command("cp " + str(_out) +
                        " " + str(output)).execute()

        def check_output(proc):
            while proc.poll() is None:
                line = proc.stdout.readline().decode("utf-8")
                if PackageBuilder.regex.search(line):
                    yield line
            self.mock_return_code = proc.returncode

        _ret = list(
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
        move_files(output_dir, self.temp_dir.glob("*.rpm"))
        self.mock_logs = output_dir / "mock_logs"
        move_files(self.mock_logs, self.temp_dir.glob("*.log"))
        return _ret

    @staticmethod
    def fetch_repos(dist, arch):
        logging.info("New thread for fetch repos started")
        config_file = dist + '-' + arch
        Command("mock --init -r " + config_file).execute()
