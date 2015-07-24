from rpg.plugin import Plugin
from modulefinder import ModuleFinder


class PythonPlugin(Plugin):

    def patched(self, project_dir, spec, sack):
            files = list(project_dir.glob('*.py'))
            files.extend(list(project_dir.glob('*/*.py')))

            mod = ModuleFinder()
            for item in files:
                mod.run_script(str(item))

            for _, mod in mod.modules.items():
                if mod.__file__ and mod.__file__.startswith("/usr/lib"):
                    spec.required_files.add(mod.__file__)
