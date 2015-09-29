from rpg.plugin import Plugin


class FindFilePlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        for item in list(project_dir.glob('**/*')):
            if item.is_file():
                spec.files.add(("/" + str(item.relative_to(project_dir)),
                                None, None))
