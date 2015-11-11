from rpg.plugin import Plugin
import inspect
import logging
import os.path
import traceback


class PluginEngine:
    """ PluginEngine class is responsible for executing properly plugins.
        Plugin class should implement one of methods named as phase
        it subscribes to. That method takes pathlib.Path instance of project
        root dir, spec object and dnf sack.

:Example:

>>> from rpg import base
>>> from rpg.spec import Spec
>>> from rpg.plugin_engine import PluginEngine
>>> base = Base()
>>> spec = Spec()
>>> sack = base.load_dnf_sack()
>>> plug_eng = PluginEngine(spec, sack)
>>> plug_eng.load_plugins("../plugin_dir", ["excluded plugin"])
>>> plug_eng.execute_phase(phase[0])
>>> try:
        build_mock_recover()
    except Exception as ex:
        plug_eng.execute_mock_recover(ex.logs)
"""

    phases = ("extracted", "patched", "compiled", "installed", "package_build")

    def __init__(self, spec, sack):
        self.spec = spec
        self.sack = sack
        self.plugins = set()

    def execute_download(self, source, dest):
        logging.info("plugin 'download' phase executed")
        for plugin in self.plugins:
            if self.call_method(
                    self.load_method(plugin, "download"), source, dest):
                return

    def execute_extraction(self, source, dest):
        """ Executes extraction of archive into destination directory """
        logging.info("plugin 'extraction' phase executed")
        for plugin in self.plugins:
            if self.call_method(self.load_method(
                                plugin, "extraction"), source, dest):
                return
        raise RuntimeError("No plugin to extract '{}'!".format(source))

    def execute_phase(self, phase, project_dir):
        """trigger all plugin methods that are subscribed to the phase"""

        if phase not in self.phases:
            logging.warn("tried to execute non-valid phase %s" % phase)
            return
        logging.info("plugin phase %s executed" % phase)
        for plugin in self.plugins:
            self.call_method(
                self.load_method(plugin, phase),
                project_dir, self.spec, self.sack)

    def execute_mock_recover(self, log):
        """ Executes all mock_recoved methods that checkout returned log
            from mock build and parse it to find repairable errors. """
        _ret_code = False
        for plugin in self.plugins:
            _ret_code |= self.call_method(
                self.load_method(plugin, "mock_recover"), log, self.spec)
        return _ret_code

    def load_plugins(self, path, excludes=[]):
        """finds all plugins in dir and it's subdirectories"""

        pyfiles = path.rglob('*.py')
        for pyfile in pyfiles:
            splitted_path = self._os_path_split(str(pyfile)[:-3])
            path_to_file = '.'.join(splitted_path[:-1])
            imported_path = __import__(
                path_to_file, fromlist=[splitted_path[-1]])
            imported_file = getattr(imported_path, splitted_path[-1])
            plugin_file = imported_file.__name__
            for var_name in dir(imported_file):
                attr = getattr(imported_file, var_name)
                if inspect.isclass(attr) and attr != Plugin and \
                   issubclass(attr, Plugin):
                    try:
                        plugin = attr()
                        plugin_name = plugin.__class__.__name__
                        if plugin_name not in excludes:
                            self.plugins.add(plugin)
                            logging.info("plugin %s loaded (%s)" %
                                         (plugin_name, plugin_file))
                        else:
                            logging.info("plugin %s was excluded (%s)" %
                                         (plugin_name, plugin_file))
                    except Exception:
                        logging.warn("plugin %s not loaded (%s)" %
                                     (plugin_name, plugin_file))

    @staticmethod
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

    @staticmethod
    def get_class(method):
        method_name = method.__name__
        classes = [method.__self__.__class__
                   if method.__self__ else
                   method.im_class]
        while classes:
            c = classes.pop()
            if method_name in c.__dict__:
                return c
            else:
                classes = list(c.__bases__) + classes
        return None

    @staticmethod
    def load_method(plugin, method):
        try:
            return getattr(plugin, method)
        except AttributeError:
            pass

    @staticmethod
    def call_method(method, *args, **kwargs):
        try:
            if callable(method):
                ret = method(*args, **kwargs)
                return ret if ret else False
        except Exception as err:
            logging.error(
                "error during executing plugin {}:\n{}".format(
                    PluginEngine.get_class(method).__name__, str(err) + "\n" +
                    ''.join(traceback.format_tb(err.__traceback__))))
        return False
