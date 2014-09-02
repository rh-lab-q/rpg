from rpg.plugin import Plugin
from subprocess import call
import os

class CMakePlugin(Plugin):

    def patched(self, project_dir, spec, sack):
        if (project_dir / "CMakeLists.txt").is_file():
            compiled_dir = project_dir / "../compiled"
            os.mkdir(str(compiled_dir))
            os.chdir(str(compiled_dir))
            call(["cmake", str(project_dir)])
            spec.tags["build"] = "bla"
