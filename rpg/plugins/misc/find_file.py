from rpg.plugin import Plugin
from pathlib import PurePath


class FindFilePlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        self.files = []
        for item in list(project_dir.glob('**/*')):
            if (item.is_file() and '__pycache__' not in str(item)):
                self.files.append((str(PurePath(item)), None, None))
        sorted_files = sorted(self.files, key=lambda e: e[0])
        spec.files.append(sorted_files)
