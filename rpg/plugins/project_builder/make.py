from rpg.command import Command
from rpg.plugin import Plugin
import logging


class MakePlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "Makefile").is_file():
            spec.BuildRequires.add("make")
            logging.debug('Makefile found')

            cmd_build = Command("make")
            cmd_install = Command("make install DESTDIR=$RPM_BUILD_ROOT")

            spec.build = cmd_build
            spec.install = cmd_install
