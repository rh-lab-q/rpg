from rpg.command import Command
from rpg.plugin import Plugin
import logging


class SetuptoolsPlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "setup.py").is_file():
            spec.BuildRequires.add("python3-setuptools")
            logging.debug('setup.py found')
            spec.build = Command("python3 setup.py build")
            spec.install = Command(
                "python3 setup.py install "
                "--skip-build --root $RPM_BUILD_ROOT")
