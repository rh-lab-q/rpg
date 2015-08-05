from rpg.command import Command
from rpg.plugin import Plugin
import logging
import re


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

    def compiled(self, project_dir, spec, sack):
        regex = re.compile(r":FILEPATH=(/\S*)")
        cache_files = list(project_dir.glob("**/CMakeCache.txt"))
        matches = []
        for p in cache_files:
            with p.open() as f:
                matches += regex.findall(f.read())
        matches = set(matches)
        spec.build_required_files = spec.build_required_files.union(matches)
        spec.required_files = spec.required_files.union(matches)
