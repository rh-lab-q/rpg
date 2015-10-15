import logging
from rpg.plugin import Plugin


class FilesToPkgsPlugin(Plugin):

    _TRANSLATED = {}
    _IGNORE = []

    def installed(self, project_dir, spec, sack):
        """ Resolves files in (Build) requires into packages """
        def _resolve(files, query):
            for _file in files:
                try:
                    if _file in self._IGNORE:
                        continue
                    elif _file in self._TRANSLATED:
                        yield self._TRANSLATED[_file]
                    else:
                        pckg = query.filter(file__glob=_file)[0]
                        self._TRANSLATED[_file] = pckg.name
                        for _f in pckg.files:
                            self._TRANSLATED[_f] = pckg.name
                        yield pckg.name
                except IndexError:
                    self._IGNORE.append(_file)
                    logging.log(logging.WARN,
                                "For '{}' have not been found any package"
                                .format(_file))

        if sack:
            _query = sack.query().available()
            logging.info("Resolving Requires")
            spec.Requires.update(
                set(_resolve(spec.required_files, _query)))
            logging.info("Resolving BuildRequires")
            spec.BuildRequires.update(
                set(_resolve(spec.build_required_files, _query)))
            spec.required_files = set()
            spec.build_required_files = set()
            if str(spec.check):
                spec.BuildRequires.update(spec.Requires)
