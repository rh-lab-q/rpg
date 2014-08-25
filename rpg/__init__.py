from rpg.plugin_engine import PluginEngine, phases
from rpg.project_builder import ProjectBuilder
from rpg.copr_uploader import CoprUploader
from rpg.package_builder import PackageBuilder
from rpg.source_loader import SourceLoader
from rpg.spec import Spec
from pathlib import Path


class Base(object):

    """Base class that is controlled by RPM GUI"""

    def __init__(self):
        self._project_builder = ProjectBuilder()
        self.spec = Spec()
        self.sack = None  # TODO dnf sack
        self._package_builder = PackageBuilder()
        self._plugin_engine = PluginEngine(self.spec, self.sack)
        self._source_loader = SourceLoader()
        self._copr_uploader = CoprUploader()
        self._plugin_engine.load_plugins(Path('rpg/plugins'))

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
        self._plugin_engine.execute_phase(phases[0],
                                          self.source_extraction_path)

    def apply_patches(self, ordered_patches):
        """executed in background after patch selection and reordering"""
        self._project_builder.apply_patches(ordered_patches)

    def run_pathed_sources_analysis(self):
        """executed in background after patches are applied"""
        self._plugin_engine.execute_phase(phases[1],
                                          self.source_extraction_path)

    def build_project(self):
        """executed in background after filled requires screen"""
        self._project_builder.build(self.source_extraction_path,
                                    self.project_build_path,
                                    self.spec.scripts["%build"])

    def run_installed_files_analysis(self):
        """executed in background after successful project build"""
        self._plugin_engine.execute_phase(phases[2],
                                          self.project_build_path)

    def build_packages(self, *distros):
        """builds packages for desired distributions"""
        for distro in distros:
            self._package_builder.build(self.spec_path, self.tarball_path,
                                        self.distro)

    # predictor methods are used for autocompletion of the field,
    # every guess_* method return list of strings matched ordered
    # by their rank

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
