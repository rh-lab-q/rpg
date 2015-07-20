import logging
import re
from rpg.command import Command
import subprocess


class PackageBuilder(object):

    @staticmethod
    def build_srpm(spec_file, tarball, output_file):
        """builds RPM package with build_srpm and build_rpm"""

        # Build srpm pakcage from given spec_file and tarball
        Command("rpmdev-setuptree").execute()
        Command("cp " + str(tarball) +
                ' $(rpm --eval "%{_topdir}")/SOURCES').execute()
        output = Command("rpmbuild -bs " + str(spec_file)).execute()
        Command("mv " + str(output.split()[-1]) +
                " " + str(output_file)).execute()

    @staticmethod
    def build_rpm(srpm, distro, arch):

        def check_output(proc):
            while proc.poll() is None:
                line = proc.stdout.readline().decode("utf-8")
                print(line)
                if re.search(r"[eE][rR][rR][oO][rR]|" +
                             r"[eE][xX][cC][eE][pP][tT][iI][oO][nN]",
                             line):
                    yield line

        return list(
            check_output(
                subprocess.Popen(
                    [
                        "mock", "--no-clean",
                        "--no-cleanup-after",
                        "--verbose",
                        "--root", distro + '-' + arch,
                        "--rebuild", srpm
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
            )
        )

    @staticmethod
    def fetch_repos(dist, arch):
        logging.info("New thread for fetch repos started")
        config_file = dist + '-' + arch
        Command("mock --init -r " + config_file).execute()
