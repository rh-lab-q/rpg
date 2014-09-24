from rpg.command import Command
from rpg.plugin import Plugin
import logging


class CMakePlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "CMakeLists.txt").is_file():
            logging.debug('CMakeLists.txt found')
            build = Command()
            build.append_cmdlines("cmake " + str(project_dir))
            build.append_cmdlines("make")
            install = Command("make install DESTDIR=$RPM_BUILD_ROOT")
            spec.scripts["%build"] = build
            spec.scripts["%install"] = install
