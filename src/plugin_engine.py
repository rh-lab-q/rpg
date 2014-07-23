# phases:
BEFORE_PATCHES_APLIED, AFTER_PATCHES_APPLIED, AFTER_PROJECT_BUILD = range(3)

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

    def execute_phase(self, phase, project_root_dir):
        """trigger all plugin methods that are subscribed to the phase"""
        pass

    def load_plugins(dir):
        """finds all plugins in dir and it's subdirectories"""
        pass
