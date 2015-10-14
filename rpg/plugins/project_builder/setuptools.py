from rpg.command import Command
from rpg.plugin import Plugin
from rpg.utils import str_to_pkgname
import logging
import re


class SetuptoolsPlugin(Plugin):

    def extracted(self, project_dir, spec, sack):
        if (project_dir / "setup.py").is_file():
            with (project_dir / "setup.py").open() as f:
                matches = re.findall(
                    r'(name|version|description|license|url)'
                    r'\s*=\s*\(?"(.*?)"\)?\s*,',
                    f.read(), re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match[0] == "name":
                    spec.Name = str_to_pkgname(match[1])
                elif match[0] == "version":
                    spec.Version = match[1]
                elif match[0] == "description":
                    spec.description = re.sub(r'\".*?\"', '', match[1])
                elif match[0] == "license":
                    spec.License = match[1]
                elif match[0] == "url":
                    spec.URL = match[1]

    def patched(self, project_dir, spec, sack):
        """ Appends commands to build Python project with
            Setuptools build system """
        if (project_dir / "setup.py").is_file():
            spec.BuildRequires.add("python3-setuptools")
            logging.debug('setup.py found')
            spec.build = Command("python3 setup.py build")
            spec.install = Command(
                "python3 setup.py install "
                "--skip-build --root $RPM_BUILD_ROOT")
