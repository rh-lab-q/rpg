from rpg.command import Command
from rpg.plugin import Plugin
import logging
import re


class AutotoolsPlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "configure").is_file():
            logging.debug('configure found')
            build = Command()
            build.append("./configure")
            build.append("make")
            spec.build = build
            spec.install = Command('make install DESTDIR="$RPM_BUILD_ROOT"')
        elif ((project_dir / "configure.ac").is_file() and
              (project_dir / "Makefile.am").is_file()):
            logging.debug('configure.ac and Makefile.am found')
            spec.BuildRequires.add("autoconf")
            spec.BuildRequires.add("automake")
            spec.BuildRequires.add("libtool")
            f = (project_dir / "configure.ac").open()
            regex = re.compile(
                r"PKG_CHECK_MODULES\s*\(.*?,\s*(.*?)\s*?[,\)]", re.DOTALL)
            deps = _extract_dependencies(regex, f)
            for dep in deps:
                spec.BuildRequires.add(dep)
            build = Command()
            if (project_dir / "autogen.sh").is_file():
                logging.debug('autogen.sh found')
                build.append("./autogen.sh")
            else:
                build.append("autoreconf --install --force")
            build.append("./configure")
            build.append("make")
            spec.build = build
            spec.install = Command("make install DESTDIR=\"$RPM_BUILD_ROOT\"")
        elif (project_dir / "configure.ac").is_file():
            logging.warning('configure.ac found, Makefile.am missing')
        elif (project_dir / "Makefile.am").is_file():
            logging.warning('Makefile.am found, configure.ac missing')


def _extract_dependencies(regex, file):
    regex2 = re.compile(r"\[?\s*(\S*\s*[><=]+\s*[^\s\]]*|[^\s\]]+)\s*\]?")
    file.seek(0)
    temps = []
    deps = []
    matches = regex.findall(file.read())
    for match in matches:
        temps += list(regex2.findall(match))
    for temp in temps:
        if temp[0] == '$':
            regex3 = re.compile(
                temp[1:] + r"\s*=\s*[\"\[]\s*(.*?)\s*?[\]\"]", re.DOTALL)
            deps += list(_extract_dependencies(regex3, file))
        else:
            deps.append(temp)
    return deps
