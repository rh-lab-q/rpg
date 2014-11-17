from rpg.plugin import Plugin


class FindFilePlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        self.files = []
        for item in list(project_dir.glob('**/*')):
            if (item.is_file() and '__pycache__' not in str(item)):
                self.files.append(("/" + str(item.relative_to(project_dir)),
                                   None, None))
        sorted_files = sorted(self.files, key=lambda e: e[0])
        for one_file in sorted_files:
            spec.files.append(one_file)
