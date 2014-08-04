from rpg.plugin import Plugin
import inspect
import os.path

phases = ("before_patches_aplied", "after_patches_applied",
          "after_project_build")


class PluginEngine:

    """PluginEngine class is responsible for executing properly plugins.
       Plugin is class that implements methods which take file/dir and SPEC
       as params.
       There are threee main phases (BEFORE_PATCHES_APLIED,
       AFTER_PATCHES_APPLIED and AFTER_PROJECT_BUILD). These phases will
       decorate plugin methods, e.g. @before_project_build. Other filter
       decorators could be @each_file('regex'), @root_dir, @each_dir and
       @file('relative/path/from/project/root/dir') that will proceed only
       relevant files"""

    def __init__(self, spec, sack):
        self.spec = spec
        self.sack = sack
        self.plugins = set()

    def execute_phase(self, phase, project_dir):
        """trigger all plugin methods that are subscribed to the phase"""

        if phase not in phases:
            # TODO log warning
            return
        for plugin in self.plugins:
            try:
                method = getattr(plugin, phase)
            except AttributeError:
                continue
            if callable(method):
                # TODO log info execution of plugin
                try:
                    method(project_dir, self.spec, self.sack)
                except Exception:
                    pass  # TODO log error

    def load_plugins(self, path):
        """finds all plugins in dir and it's subdirectories"""

        pyfiles = path.rglob('*.py')
        for pyfile in pyfiles:
            splitted_path = _os_path_split(str(pyfile)[:-3])
            path_to_file = '.'.join(splitted_path[:-1])
            imported_path = __import__(
                path_to_file, fromlist=[splitted_path[-1]])
            imported_file = getattr(imported_path, splitted_path[-1])
            for var_name in dir(imported_file):
                attr = getattr(imported_file, var_name)
                if inspect.isclass(attr) and attr != Plugin and \
                   issubclass(attr, Plugin):
                    # TODO info log initialization of plugin
                    try:
                        self.plugins.add(attr())
                    except Exception:
                        pass  # TODO log error


def _os_path_split(path):
    parts = []
    while True:
        newpath, tail = os.path.split(path)
        if newpath == path:
            assert not tail
            if path:
                parts.append(path)
            break
        parts.append(tail)
        path = newpath
    parts.reverse()
    return parts
