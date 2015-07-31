import logging
from rpg.plugin import Plugin


class FilesToPkgsPlugin(Plugin):

    def installed(self, project_dir, spec, sack):
        """ Resolves files in (Build) requires into packages """
        def _resolve(files, query):
            for _file in files:
                try:
                    yield query.filter(file=_file)[0].name
                except IndexError:
                    logging.log(logging.WARN,
                                "For '{}' have not been found any package"
                                .format(_file))

        if sack:
            _query = sack.query().available()
            logging.info("Resolving Requires")
            spec.Requires = spec.Requires.union(
                set(_resolve(spec.required_files, _query)))
            logging.info("Resolving BuildRequires")
            spec.BuildRequires = spec.BuildRequires.union(
                set(_resolve(spec.build_required_files, _query)))
            spec.required_files = set()
            spec.build_required_files = set()
            if str(spec.check):
                spec.BuildRequires = spec.BuildRequires.union(spec.Requires)
