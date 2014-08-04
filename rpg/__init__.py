class Base(object):
    """Base class that is controlled by RPM GUI"""

    def __init__(self):
        self._project_builder = ProjectBuilder()
        self._package_builder = PackageBuilder()
        self._plugin_engine = PluginEngine()
        self._source_loader = SourceLoader(source_extraction_path)
        self._copr_uploader = CoprUploader()
        self.spec = Spec()
        # TODO run "dnf makecache" in the background

    @property
    def source_extraction_path(self):
        return self.base_path % "source"

    @property
    def rpm_stuff_path(self):
        # directory with tarball and spec file
        return self.base_path % "rpmstuff"

    @property
    def project_build_path(self):
        return self.base_path % "projectbuild"

    @property
    def base_path(self):
        return "/tmp/rpg-" + self._hash + "/%s"

    @property
    def project_name(self):
        return self.spec.tags["name"]

    @property
    def spec_path(self):
        return self.rpm_stuff_path + '/' + self.project_name + ".spec"

    @property
    def tarball_path(self):
        return self.rpm_stuff_path + '/' + self.project_name + ".tar.gz"

    def process_archive_or_dir(self, path):
        """executed in background after dir/tarball/SRPM selection"""
        self._hash = "<hash>"  # TODO hash of tarball or filename
        self._source_loader.load_sources(path, self.source_extraction_path)

    def run_raw_sources_analysis(self):
        """executed in background after dir/tarball/SRPM selection"""
        self._plugin_engine.execute_phase(BEFORE_PATCHES_APLIED,
                                          self.source_extraction_path)

    def apply_patches(self, ordered_patches):
        """executed in background after patch selection and reordering"""
        self._project_builder.apply_patches(ordered_patches)

    def run_pathed_sources_analysis(self):
        """executed in background after patches are applied"""
        self._plugin_engine.execute_phase(AFTER_PATCHES_APLIED,
                                          self.source_extraction_path)

    def build_project(self):
        """executed in background after filled requires screen"""
        self._project_builder.build(self.source_extraction_path,
                                    self.project_build_path)

    def run_installed_files_analysis(self):
        """executed in background after successful project build"""
        self._plugin_engine.execute_phase(AFTER_PROJECT_BUILD,
                                          self.project_build_path)

    def build_packages(self, *distros):
        """builds packages for desired distributions"""
        for distro in distros:
            self._package_builder.build(self.spec_path, self.tarball_path,
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


class Plugin:
    """class from which are plugins derived"""
    pass
