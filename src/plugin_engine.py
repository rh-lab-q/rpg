# phases:
BEFORE_PROJECT_BUILD, AFTER_PROJECT_BUILD = range(2)

class PluginEngine:
    """PluginEngine class is responsible for executing properly plugins.
       Plugin is class that implements methods which take file/dir and SPEC
       as params.
       There are two main phases (BEFORE_PROJECT_BUILD
       and AFTER_PROJECT_BUILD). These phases will decorate plugin methods,
       e.g. @before_project_build. Other filter decorators could be
       @each_file('regex'), @root_dir, @each_dir and
       @file('relative/path/from/project/root/dir') that will proceed only
       relevant files"""

    def execute_phase(self, phase):
        """trigger all plugin methods that are subscribed to the phase"""
        pass
