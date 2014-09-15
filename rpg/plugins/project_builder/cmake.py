from rpg.command import Command
from rpg.plugin import Plugin
import logging


class CMakePlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "CMakeLists.txt").is_file():
            logging.debug('CMakeLists.txt found')
            cmd = Command()
            cmd.append_cmdlines("cmake " + str(project_dir))
            cmd.append_cmdlines("make")
            cmd.append_cmdlines("make install DESTDIR=$RPM_BUILD_ROOT")
            cmd.rpm_variables.append(("RPM_BUILD_ROOT",
                                      project_dir / "../installed"))
            spec.scripts["%build"] = cmd
