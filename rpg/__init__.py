import hawkey
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
from rpg.command import Command
from rpg.conf import Conf
from os.path import isdir
from os import makedirs
from os import geteuid
from os import remove
import shutil


class Base(object):

    """Base class that is controlled by RPM GUI"""

    def __init__(self):
        self.conf = Conf()
        self._setup_logging()
        self._project_builder = ProjectBuilder()
        self.spec = Spec()
        self.sack = None
        self._package_builder = PackageBuilder()
        self._source_loader = SourceLoader()
        self._copr_uploader = CoprUploader()

    def dnf_load_sack(self):
        logging.info('DNF sack is loading')
        import dnf
        with dnf.Base() as self._dnf_base:
            self._dnf_base.conf.releasever = dnf.rpm.detect_releasever(
                self._dnf_base.conf.installroot)
            self._dnf_base.read_all_repos()
            self._dnf_base.fill_sack()
            return self._dnf_base.sack

    def _setup_logging(self):
        if geteuid() == 0:
            log_dir = "/var/log/rpg/"
        else:
            log_dir = "/var/tmp/rpg/"
        if not isdir(log_dir):
            makedirs(log_dir)
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(asctime)s] {%(pathname)s:%(lineno)d} '
                                   '%(levelname)s - %(message)s',
                            handlers=[logging.FileHandler(log_dir + "rpg.log"),
                                      logging.StreamHandler()],
                            datefmt='%H:%M:%S')

    def load_plugins(self):
        self._plugin_engine = PluginEngine(self.spec, self.sack)
        self._plugin_engine.load_plugins(
            Path('rpg/plugins'),
            self.conf.exclude)
        for directory in self.conf.directories:
            self._plugin_engine.load_plugins(
                Path(directory),
                self.conf.exclude)

    def create_archive(self):
        """ Creates archive (archvie_path) from Source folder """
        self.spec.Source = self.spec.Name + "-" + self.spec.Version + ".tar.gz"
        _tar = Command("tar zcf " + str(self.archive_path) +
                       " -C " + str(self.extracted_dir) +
                       " . --transform='s/^\./" +
                       self.spec.Name + "-" + self.spec.Version + "/g'")
        _tar.execute()
        logging.debug(str(_tar))

    @property
    def base_dir(self):
        try:
            return Path("/tmp/rpg-%s-%s" % (self._input_name, self._hash))
        except AttributeError:
            msg = "`load_project_from_url` method needs to be called first"
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
    def archive_path(self):
        return self.base_dir / self.spec.Source

    @property
    def srpm_path(self):
        try:
            return next(self.base_dir.glob(self.project_name + "*src.rpm"))
        except StopIteration:
            raise RuntimeError(
                "Can't find '{}'! You need to call build_srpm first."
                .format(str(self.base_dir / (self.project_name + "*src.rpm"))))

    def load_project_from_url(self, path):
        """executed in background after dir/tarball/SRPM selection"""
        path = Path(path)
        temp_arch = "downloaded_archive.tar.gz"
        if "github" in str(path):
            self._source_loader.download_git_repo(str(path), temp_arch)
        elif str(path).startswith("http"):
            self._source_loader.download_archive(str(path), temp_arch)
        else:
            temp_arch = None
        self._hash = self.compute_checksum(path)
        self._input_name = path.name
        self._setup_workspace()
        self._source_loader.load_sources(path, self.extracted_dir)
        self.spec.prep = Command("%autosetup")
        if temp_arch:
            remove(temp_arch)

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

    def write_spec(self):
        with open(str(self.spec_path), 'w') as spec_file:
            spec_file.write(str(self.spec))

    def build_srpm(self):
        if not self.spec.Source or not self.archive_path.exists():
            self.create_archive()
        self.write_spec()
        self._package_builder.build_srpm(
            self.spec_path, self.archive_path, self.base_dir)
            
    def fetch_repos(self, dist, arch):
        self._package_builder.fetch_repos(dist, arch)

    def build_project(self):
        """executed in background after filled requires screen"""
        self._project_builder.build(self.extracted_dir,
                                    self.compiled_dir,
                                    self.spec.build)

    def copr_set_config(self, username, login, token):
        self.copr = CoprUploader()
        self.copr.setup_config(username, login, token)

    def copr_create_project(self, name, chroots, desc, intro):
        self.copr = CoprUploader()
        self.copr.create_copr(name, chroots, desc, intro)

    def copr_build(self, name, url):
        self.copr = CoprUploader()
        self.copr.build_copr(name, url)

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

    def _setup_workspace(self):
        """make sure all directories used later will exist"""
        shutil.rmtree(str(self.base_dir), True)
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
