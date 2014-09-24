from rpg.plugin import Plugin
import inspect
import logging
import os.path

phases = ("extracted", "patched", "compiled", "installed", "package_build")


class PluginEngine:

    """PluginEngine class is responsible for executing properly plugins.
       Plugin class should implement one of methods named as phase
       it subscribes to. That method takes pathlib.Path instance of project
       root dir, spec object and dnf sack."""

    def __init__(self, spec, sack):
        self.spec = spec
        self.sack = sack
        self.plugins = set()

    def execute_phase(self, phase, project_dir):
        """trigger all plugin methods that are subscribed to the phase"""

        if phase not in phases:
            logging.warn("tried to execute non-valid phase %s" % phase)
            return
        logging.info("plugin phase %s executed" % phase)
        for plugin in self.plugins:
            try:
                method = getattr(plugin, phase)
            except AttributeError:
                continue
            if callable(method):
                plugin_name = plugin.__class__.__name__
                try:
                    method(project_dir, self.spec, self.sack)
                except Exception as e:
                    logging.warn(
                        "error during executing plugin %s: %s"
                        % (plugin_name, e))
                else:
                    logging.info("plugin %s executed" % plugin_name)

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
                    plugin_file = imported_file.__name__
                    try:
                        plugin = attr()
                        self.plugins.add(plugin)
                    except Exception:
                        logging.warn("plugin %s not loaded" % plugin_file)
                    else:
                        logging.info("plugin %s loaded" % plugin_file)


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
