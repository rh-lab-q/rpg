from rpg.command import Command
from rpg.plugin import Plugin
import logging


class CMakePlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "CMakeLists.txt").is_file():
            spec.BuildRequires.add("cmake")
            logging.debug('CMakeLists.txt found')
            build = Command()
            build.append("cmake .")
            build.append("make")
            install = Command("make install DESTDIR=$RPM_BUILD_ROOT")
            spec.build = build
            spec.install = install
