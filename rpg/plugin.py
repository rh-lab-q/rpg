class Plugin:
    """ Class from which are plugins derived

        def extraction(self, source, dest):
            pass

        def extracted(self, project_dir, spec, sack):
            pass

        def patched(self, project_dir, spec, sack):
            pass

        def compiled(self, project_dir, spec, sack):
            pass

        def installed(self, project_dir, spec, sack):
            pass

        def package_build(self, package_path, spec, sack):
            pass

        def mock_recover(self, log, spec):
            pass
    """
