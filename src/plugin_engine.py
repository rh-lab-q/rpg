# phases:
BEFORE_PROJECT_BUILD, AFTER_PROJECT_BUILD = range(2)

class PluginEngine:
    """PluginEngine class is responsible for executing properly plugins"""

    def execute_phase(self, phase):
        """trigger all plugin methods that are subscribed to the phase"""
        pass
