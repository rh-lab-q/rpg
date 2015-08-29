from rpg.plugin import Plugin


class FindTranslationPlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        translation_file = list(project_dir.glob('**/*.mo'))
        if translation_file and translation_file[0].is_file():
            spec.files.add((("-f %%{%s}.lang"
                             % translation_file[0].name), None, None))
