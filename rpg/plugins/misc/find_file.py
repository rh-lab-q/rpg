from rpg.plugin import Plugin


class FindFilePlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        """ Finds files that will be installed and
            appends them to files macro """
        for item in list(project_dir.glob('**/*')):
            if item.is_file():
                spec.files.add(("/" + str(item.relative_to(project_dir)),
                                None, None))
