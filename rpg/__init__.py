import logging
import platform
from pathlib import Path
from rpg.plugin_engine import PluginEngine, phases
from rpg.project_builder import ProjectBuilder
from rpg.copr_uploader import CoprUploader
from rpg.package_builder import PackageBuilder
from rpg.source_loader import SourceLoader
from rpg.spec import Spec
from rpg.command import cmd_output
from rpg.conf import Conf
from os.path import isdir
import shutil


class Base(object):

    """Base class that is controlled by RPM GUI"""

    def __init__(self):
        self.conf = Conf()
        self._setup_logging()
        self._project_builder = ProjectBuilder()
        self.spec = Spec()
        self.sack = None  # TODO dnf sack
        self._package_builder = PackageBuilder()
        self._plugin_engine = PluginEngine(self.spec, self.sack)
        self._source_loader = SourceLoader()
        self._copr_uploader = CoprUploader()

    def _setup_logging(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s] {%(pathname)s:%(lineno)d} '
                                   '%(levelname)s - %(message)s',
                            handlers=[logging.FileHandler("rpg.log"),
                                      logging.StreamHandler()],
                            datefmt='%H:%M:%S')

    def load_plugins(self):
        self._plugin_engine.load_plugins(
            Path('rpg/plugins'),
            self.conf.exclude)
        for directory in self.conf.directories:
            self._plugin_engine.load_plugins(
                Path(directory),
                self.conf.exclude)

    @property
    def base_dir(self):
        try:
            return Path("/tmp/rpg-%s-%s" % (self._input_name, self._hash))
        except AttributeError:
            msg = "`process_archive_or_dir` method needs to be called first"
            raise RuntimeError(msg)

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
        return self.spec.Name

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
        self._input_name = p.name
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
                                    self.spec.build)

    def run_compiled_analysis(self):
        """executed in background after patches are applied"""
        self._plugin_engine.execute_phase(phases[2],
                                          self.extracted_dir)

    def install_project(self):
        """executed in background after filled requires screen"""
        self._project_builder.install(self.compiled_dir,
                                      self.installed_dir,
                                      self.spec.install)

    def run_installed_analysis(self):
        """executed in background after successful project build"""
        self._plugin_engine.execute_phase(phases[3],
                                          self.installed_dir)

    def create_spec_and_archive(self):
        self._source_loader.create_archive(self.base_dir, self.extracted_dir)
        with open(str(self.spec_path), 'w') as spec_file:
            spec_file.write(str(self.spec))

    def build_packages(self, distros, archs=platform.machine()):
        """builds packages for desired distributions"""
        for arch in archs:
            for distro in distros:
                self._package_builder.build(self.spec_path, self.tarball_path,
                                            distro, arch)

    @staticmethod
    def compute_checksum(sources):
        if sources.is_dir():
            cmd = "find %s -type f -print0 | sort -z | xargs " \
                  "-0 sha1sum | sha1sum" % sources.resolve()
        else:
            cmd = "sha1sum %s" % sources.resolve()
        return cmd_output([cmd])[:7]

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
        name = str(self._input_name)
        if isdir(name):
            return name
        else:
            if name[-4:] == ".zip":
                return name[:-4]
            else:
                if "tar" in name:
                    return name.split(".tar")[0]
        return ""

    def guess_provide(self):
        # returns list of all known provides
        provides = set()
        for pkg in self.sack.query():
            provides.update(pkg.provides)
        return sorted(provides)

    def guess_changelog_data(self):
        # returns list of tuples (author, email) from git
        pass

    def guess_dependency(self):
        # returns guess_provide() + all package names from repos
        names = map(lambda pkg: pkg.name, self.sack.query())
        return sorted(set(names).union(set(self.guess_provide())))

    def guess_license(self):
        # returns list of all known licenses
        licenses = set()
        for pkg in self.sack.query():
            licenses.update(pkg.license)
        return sorted(licenses)
