from rpg.plugin import Plugin


class FindTranslationPlugin(Plugin):

    def find(self, project_dir, spec, sack):
        translation_file = list(project_dir.glob('**/*.mo'))
        if translation_file[0].is_file():
            spec.files.insert(0, "-f %{%s}.lang" % translation_file.name())
