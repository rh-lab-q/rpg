class Rpg(object):
    """Main class that is controlled by RPM GUI"""

    # TODO paths will also contain hash of tarball or filename
    self.base_path = "/tmp/rpg-<hash>/%s" 
    self.source_extraction_path = self.base_path % "source"
    self.project_build_path = self.base_path % "projectbuild"
    self.rpm_stuff_path = self.base_path % "rpmstuff"

    def __init__(self, arg):
        self.project_builder = ProjectBuilder()
        self.package_builder = PackageBuilder()
        self.plugin_engine = PluginEngine()
        self.source_loader = SourceLoader(source_extraction_path)
        self.copr_uploader = CoprUploader()
        self.spec = Spec()

    @property
    def project_name():
        return self.spec.tags["name"]

    @property
    def spec_path():
        return rpm_stuff_path + '/' + self.project_name + ".spec"

    @property
    def tarball_path():
        return rpm_stuff_path + '/' + self.project_name + ".tar.gz"

    def process_archive_or_dir(path):
        """executed after dir/tarball/SRPM selection"""
        self.source_loader.load_sources(path)

    def run_sources_analysis():
        """executed in background before second screen (build commands)"""
        self.plugin_engine.execute_phase(BEFORE_PROJECT_BUILD)

    def build_project():
        """executed in background after patch selection and reordering"""
        self.plugin_engine.execute_phase(AFTER_PROJECT_BUILD)

    def run_installed_files_analysis():
        """executed in background after successful project build"""
        self.plugin_engine.execute_phase(AFTER_PROJECT_BUILD)

    def build_packages(*distros):
        """builds packages for desired distributions"""
        for distro in distros:
            self.package_builder.build(self.spec_path, self.tarball_path,
                                       self.distro)


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

        def guess_chagelog_data(self):
            # returns list of tuples (author, email)
            pass

        def guess_build_dependency(self):
            pass

        def guess_dependency(self):
            pass

        def guess_license(self):
            pass
