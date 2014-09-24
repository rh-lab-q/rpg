import logging
from pathlib import Path
from rpg.plugin_engine import PluginEngine, phases
from rpg.project_builder import ProjectBuilder
from rpg.copr_uploader import CoprUploader
from rpg.package_builder import PackageBuilder
from rpg.source_loader import SourceLoader
from rpg.spec import Spec
from subprocess import check_output
import shutil


class Base(object):

    """Base class that is controlled by RPM GUI"""

    def __init__(self):
        self._setup_logging()
        self._project_builder = ProjectBuilder()
        self.spec = Spec()
        self.sack = None  # TODO dnf sack
        self._package_builder = PackageBuilder()
        self._plugin_engine = PluginEngine(self.spec, self.sack)
        self._source_loader = SourceLoader()
        self._copr_uploader = CoprUploader()
        self._plugin_engine.load_plugins(Path('rpg/plugins'))

    def _setup_logging(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s] {%(pathname)s:%(lineno)d} '
                                   '%(levelname)s - %(message)s',
                            handlers=[logging.FileHandler("rpg.log"),
                                      logging.StreamHandler()],
                            datefmt='%H:%M:%S')

    @property
    def base_dir(self):
        return Path("/tmp/rpg-" + self._hash)

    @property
    def extracted_dir(self):
        return self.base_dir / "extracted"

    @property
    def compiled_dir(self):
        return self.base_dir / "compiled"

    @property
    def installed_dir(self):
        return self.base_dir / "installed"

    @property
    def project_name(self):
        return self.spec.tags["name"]

    @property
    def spec_path(self):
        return self.base_dir / (self.project_name + ".spec")

    @property
    def tarball_path(self):
        return self.base_dir / (self.project_name + ".tar.gz")

    @property
    def rpm_path(self):
        return next(self.base_dir.glob(self.project_name + "*.rpm"))

    def process_archive_or_dir(self, path):
        """executed in background after dir/tarball/SRPM selection"""
        p = Path(path)
        self._hash = self.compute_checksum(p)
        self.setup_workspace()
        self._source_loader.load_sources(p, self.extracted_dir)

    def run_raw_sources_analysis(self):
        """executed in background after dir/tarball/SRPM selection"""
        self._plugin_engine.execute_phase(phases[0],
                                          self.extracted_dir)

    def apply_patches(self, ordered_patches):
        """executed in background after patch selection and reordering"""
        self._project_builder.apply_patches(ordered_patches)

    def run_patched_sources_analysis(self):
        """executed in background after patches are applied"""
        self._plugin_engine.execute_phase(phases[1],
                                          self.extracted_dir)

    def build_project(self):
        """executed in background after filled requires screen"""
        self._project_builder.build(self.extracted_dir,
                                    self.compiled_dir,
                                    self.spec.scripts["%build"])

    def run_compiled_analysis(self):
        """executed in background after patches are applied"""
        self._plugin_engine.execute_phase(phases[2],
                                          self.extracted_dir)

    def install_project(self):
        """executed in background after filled requires screen"""
        self._project_builder.install(self.compiled_dir,
                                      self.installed_dir,
                                      self.spec.scripts["%install"])

    def run_installed_analysis(self):
        """executed in background after successful project build"""
        self._plugin_engine.execute_phase(phases[3],
                                          self.compiled_dir)

    def build_packages(self, *distros):
        """builds packages for desired distributions"""
        for distro in distros:
            self._package_builder.build(self.spec_path, self.tarball_path,
                                        self.distro)

    @staticmethod
    def compute_checksum(sources):
        if sources.is_dir():
            cmd = "find %s -type f -print0 | sort -z | xargs " \
                  "-0 sha1sum | sha1sum" % sources.resolve()

            shasum = check_output(["/bin/sh", "-c", cmd])
        else:
            cmd = "sha1sum %s" % sources.resolve()
            shasum = check_output(["/bin/sh", "-c", cmd])
        return shasum.decode("utf-8")[:7]

    @property
    def all_dirs(self):
        return [
            self.extracted_dir,
            self.compiled_dir,
            self.installed_dir
        ]

    def setup_workspace(self):
        """make sure all directories used later will exist"""
        try:
            shutil.rmtree(str(self.base_dir))
        except FileNotFoundError:
            pass
        for d in self.all_dirs:
            d.mkdir(parents=True)

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
