class RPG(object):
    """Main class that is controlled by RPM GUI"""

    def __init__(self, arg):
        self.project_builder = ProjectBuilder()
        self.package_builder = PackageBuilder()
        self.plugin_engine = PluginEngine()
        self.source_loader = SourceLoader()
        self.copr_uploader = CoprUploader()
        self.spec = Spec()

    class Predictor:
        """Predictor class is used for autocompletion of field,
           every guess_* method takes prefix of result string
           and returns list of strings matched ordered by their rank"""

        def guess_name(self):
            pass
            
        def guess_provide(self):
            pass
            
        def guess_group(self):
            pass

        def guess_build_dependency(self):
            pass

        def guess_dependency(self):
            pass

        def guess_license(self):
            pass
