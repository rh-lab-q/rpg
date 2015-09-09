import logging
import re
from rpg.command import Command
from rpg.utils import path_to_str
from shutil import copytree
import subprocess
import tempfile
from pathlib import Path
import sys


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
        Command("cp " + path_to_str(tarball) +
                ' $(rpm --eval "%{_topdir}")/SOURCES').execute()
        output = Command("rpmbuild -bs " + path_to_str(spec_file)).execute()
        Command("mv " + path_to_str(output.split()[-1]) +
                " " + path_to_str(output_dir)).execute()

    def check_logs(self):
        with open(str(self.mock_logs) + "/build.log") as build_log:
            for line in build_log.readlines():
                if PackageBuilder.regex.search(line):
                    yield line

    def build_rpm(self, srpm, distro, arch, output_dir):

        def move_files(output, files):
            if not output.exists() and not output.is_dir():
                Command("mkdir " + path_to_str(output)).execute()
            for _out in files:
                try:
                    Command("cp -rf " + path_to_str(_out) + " " +
                            path_to_str(output)).execute()
                except:
                    pass

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
                        "--verbose",
                        "--root", distro + '-' + arch,
                        "--rebuild", path_to_str(srpm),
                        "--resultdir=" + path_to_str(self.temp_dir)
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
