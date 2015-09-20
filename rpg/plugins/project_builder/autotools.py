from rpg.command import Command
from rpg.plugin import Plugin
from rpg.utils import str_to_pkgname
import logging
import re


class AutotoolsPlugin(Plugin):

    re_CHECK_MODULES = re.compile(
        r"PKG_CHECK_MODULES\s*\(.*?,\s*(.*?)\s*?[,\)]", re.DOTALL)

    re_CHECK_PROGS = re.compile(
        r"((?:(?:/bin/)|(?:/usr)(?:/bin/)?)[\w/\.-]+)", re.DOTALL)

    re_CHECK_MAKEFILE = re.compile(
        r"(/[\w/\.-]+\.h)", re.DOTALL)

    def extracted(self, project_dir, spec, sack):
        if (project_dir / "configure.ac").is_file():
            regex = re.compile(
                r"AC_INIT\s*\(\s*\[?\s*?(.*?)\s*\]?\s*,\s*"
                r"\[?\s*?(.*?)\s*\]?\s*?[,)]",
                re.IGNORECASE | re.DOTALL)
            with (project_dir / "configure.ac").open() as f:
                result = regex.search(f.read())
                if result.group(1):
                    spec.Name = str_to_pkgname(result.group(1))
                if result.group(2):
                    spec.Version = result.group(2)

    def patched(self, project_dir, spec, sack):
        """ Appends commands to build project with Autotools build system
            and appends dependencies """
        if (project_dir / "configure").is_file():
            logging.debug('configure found')
            spec.build.append(["%{configure}", "%{make_build}"])
            spec.install.append(['make install DESTDIR="$RPM_BUILD_ROOT"'])
        elif ((project_dir / "configure.ac").is_file() and
              (project_dir / "Makefile.am").is_file()):
            logging.debug('configure.ac and Makefile.am found')
            spec.BuildRequires.update(["autoconf", "automake", "libtool"])
            build = Command()
            if (project_dir / "autogen.sh").is_file():
                logging.debug('autogen.sh found')
                build.append("./autogen.sh")
            else:
                build.append("autoreconf --install --force")
            build.append("%{configure}")
            build.append("%{make_build}")
            spec.build = build
            spec.install = Command("make install DESTDIR=\"$RPM_BUILD_ROOT\"")
        elif (project_dir / "configure.ac").is_file():
            logging.warning('configure.ac found, Makefile.am missing')
        elif (project_dir / "Makefile.am").is_file():
            logging.warning('Makefile.am found, configure.ac missing')

    def compiled(self, project_dir, spec, sack):
        """ Find all files from config.log that may be dependencies to this
            project. """
        config_log = project_dir / "config.log"
        if config_log.is_file():
            spec.build_required_files.update(_extract_log_deps(
                self.re_CHECK_PROGS, config_log.open()))
        for deps in list(project_dir.glob("**/*.Po")):
            with deps.open() as d:
                spec.build_required_files.update(
                    _extract_dependencies(
                        self.re_CHECK_MAKEFILE, d.read(), project_dir))


def _extract_log_deps(regex, file):
    for match in regex.findall(file.read()):
        yield match


def _extract_dependencies(regex, makefile, project_dir):
    return [match for match in regex.findall(makefile)]
