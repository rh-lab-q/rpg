import logging
from pathlib import Path
from rpg.plugin_engine import PluginEngine
from rpg.plugins.misc.files_to_pkgs import FilesToPkgsPlugin
from rpg.project_builder import ProjectBuilder
from copr.client import CoprClient
from rpg.package_builder import PackageBuilder, BuildException
from rpg.spec import Spec
from rpg.command import Command
from rpg.conf import Conf
from rpg.utils import path_to_str
from os.path import isdir, isfile
from os import makedirs, geteuid
import shutil
from shutil import rmtree
from tempfile import gettempdir, mkdtemp


class Base(object):
    """Base class that is controlled by RPM GUI

:Example:

>>> from rpg import Base
>>> base = Base()
>>> base.sack = base.load_dnf_sack()
>>> base.load_plugins()
>>> base.load_project_from_url("https://github.com/example/ex_repo")
>>> base.spec.Name = "Example"
>>> base.spec.Version = "0.6.11"
>>> base.spec.Release = "1%{?snapshot}%{?dist}"
>>> base.spec.License = "GPLv2"
>>> base.spec.Summary = "Example ..."
>>> base.spec.description = ("Example ...")
>>> base.spec.URL = "https://github.com/example/ex_repo"
>>> base.target_arch = "x86_64"
>>> base.target_distro = "fedora-22"
>>> base.fetch_repos(base.target_distro, base.target_arch)
>>> base.run_extracted_source_analysis()
>>> base.run_patched_source_analysis()
>>> base.build_project()
>>> base.run_compiled_source_analysis()
>>> base.install_project()
>>> base.run_installed_source_analysis()
>>> base.build_srpm()
>>> base.build_rpm_recover(self.base.target_distro, self.base.target_arch)
"""

    def __init__(self):
        self.conf = Conf()
        self._setup_logging()
        self._project_builder = ProjectBuilder()
        self.spec = Spec()
        self.sack = None
        self._package_builder = PackageBuilder()

    def load_dnf_sack(self):
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
        """ This method sets up plugin engine and loads them """
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
        _tar = Command("tar zcf " + path_to_str(self.archive_path) +
                       " -C " + path_to_str(self.extracted_dir) +
                       " . --transform='s/^\./" +
                       self.spec.Name + "-" + self.spec.Version + "/g'")
        _tar.execute()
        logging.debug(str(_tar))

    @property
    def base_dir(self):
        """ Returns path where compiled, extracted, installed
            directories are """
        try:
            return Path("/tmp/rpg-%s" % self._hash)
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
        """ Returns path to SRPM only, if it is created.
            You have to build srpm first. """
        try:
            return next(self.base_dir.glob(self.project_name + "*.src.rpm"))
        except StopIteration:
            raise RuntimeError(
                "Can't find '{}'! You need to call build_srpm first."
                .format(str(self.base_dir /
                        (self.project_name + "*.src.rpm"))))

    @property
    def rpm_path(self):
        """ This is the same as it is in srpm_path. But this returns
            list of rpms - there may be severals rpm packages like
            debuginfo, binary rpm and so on. """
        try:
            _ret = [
                _path
                for _path in self.base_dir.glob(self.project_name + "*.rpm")
                if not str(_path).endswith(".src.rpm")
            ]
            if not _ret:
                raise StopIteration
            return _ret
        except StopIteration:
            raise RuntimeError(
                "Can't find '{}'! You need to call build_rpm first."
                .format(str(self.base_dir / (self.project_name + "*.rpm"))))

    def load_project_from_url(self, path):
        """executed in background after dir/tarball/SRPM selection"""
        if not isdir(str(path)) and not isfile(str(path)):
            temp = Path(gettempdir()) / "rpg-download"
            self._plugin_engine.execute_download(path, temp)
            path = temp
        self.source_path = path = Path(path)
        self._hash = self._compute_checksum(path)
        self._setup_workspace()
        if isdir(str(path)):
            Command("cp -pr " + str(path) + " " + str(self.extracted_dir))\
                .execute()
        else:
            self._plugin_engine.execute_extraction(path, self.extracted_dir)
        direc = [str(f) for f in self.extracted_dir.iterdir()]
        if len(direc) == 1 and isdir(direc[0]):
            direc = direc[0]
            temp = mkdtemp()
            Command('mv ' + direc + '/* ' + temp +
                    ' && rm -rf ' + direc +
                    ' && mv ' + temp + '/* ' + str(self.extracted_dir))\
                .execute()
            rmtree(temp)
        logging.debug(str(direc))
        self.spec.prep = Command("%autosetup")

    def run_extracted_source_analysis(self):
        """executed in background after dir/tarball/SRPM selection"""
        self._plugin_engine.execute_phase(PluginEngine.phases[0],
                                          self.extracted_dir)

    def run_patched_source_analysis(self):
        """executed in background after patches are applied"""
        self._plugin_engine.execute_phase(PluginEngine.phases[1],
                                          self.extracted_dir)

    def run_compiled_source_analysis(self):
        """executed in background after patches are applied"""
        self._plugin_engine.execute_phase(PluginEngine.phases[2],
                                          self.compiled_dir)

    def install_project(self):
        """executed in background after filled requires screen"""
        self._project_builder.install(self.compiled_dir,
                                      self.installed_dir,
                                      self.spec.install)

    def run_installed_source_analysis(self):
        """executed in background after successful project build"""
        self._plugin_engine.execute_phase(PluginEngine.phases[3],
                                          self.installed_dir)

    def write_spec(self):
        """ Creates spec file or rewrites old one. """
        with open(path_to_str(self.spec_path), 'w') as spec_file:
            spec_file.write(str(self.spec))

    def build_srpm(self):
        """ Builds srpm into base directory. """
        if not self.spec.Source or not self.archive_path.exists():
            self.create_archive()
        self.write_spec()
        self._package_builder.build_srpm(
            self.spec_path, self.archive_path, self.base_dir)

    def build_rpm(self, target_distro, target_arch):
        """ Build rpm from srpm. If srpm does not exists,
            it will be created. """
        try:
            self.srpm_path
        except RuntimeError:
            self.build_srpm()
        self._package_builder.build_rpm(
            str(self.srpm_path), target_distro, target_arch, self.base_dir)

    def build_rpm_recover(self, distro, arch):
        """ Repeatedly build rpm with mock and finds all build errors.
            May raise RuntimeError on failed recover. """

        def build():
            self.build_srpm()
            self.build_rpm(distro, arch)

        def analyse():
            _files_to_pkgs.installed(self.base_dir, self.spec, self.sack)
            self.write_spec()

        _files_to_pkgs = FilesToPkgsPlugin()
        analyse()
        while True:
            try:
                build()
            except BuildException as be:
                if not self._plugin_engine.execute_mock_recover(be.errors):
                    if be.return_code:
                        raise RuntimeError(
                            "Build failed! See logs in '{}'"
                            .format(self._package_builder.mock_logs))
                    break
            Command("rm -rf {}".format(path_to_str(self.spec_path))).execute()
            analyse()

    def fetch_repos(self, dist, arch):
        """ Initialize mock - should be called before build_rpm_recover """
        self._package_builder.fetch_repos(dist, arch)

    def build_project(self):
        """ Executed in background after filled requires screen """
        self._project_builder.build(self.extracted_dir,
                                    self.compiled_dir,
                                    self.spec.build)

    def copr_set_config(self, username, login, token):
        """ Logs into copr with username, login and token.
            This has to be called before copr_create_project and copr_build
            To sign up on copr go here: http://copr.fedoraproject.org """
        self.cl = CoprClient(
            username, login, token, copr_url="http://copr.fedoraproject.org")

    def copr_create_project(self, name, chroots, desc, intro):
        """ Creates metadata about project - won't build until
            copr_build would be called """
        self.cl.create_project(
            name, chroots=chroots, description=desc, instructions=intro)

    def copr_build(self, name, url):
        """ Builds project on fedora copr server """
        self.cl.create_new_build(name, pkgs=[url, ])

    @staticmethod
    def _compute_checksum(sources):
        if sources.is_dir():
            cmd = "find %s -type f -print0 | sort -z | xargs " \
                  "-0 sha1sum | sha1sum" % path_to_str(sources.resolve())
        else:
            cmd = "cat %s | sha1sum" % path_to_str(sources.resolve())
        logging.error(str(cmd))
        return Command([cmd]).execute()[:7]

    @property
    def all_dirs(self):
        """ Returns Extracted, Compiled and Installed direcotry paths. """
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
        """ Returns guessed name from source path """
        return ""

    def guess_provide(self):
        """ returns list of all known provides """
        provides = set()
        for pkg in self.sack.query():
            provides.update(pkg.provides)
        return sorted(provides)

    def guess_changelog_data(self):
        """ returns list of tuples (author, email) from git """
        pass

    def guess_dependency(self):
        """ returns guess_provide() + all package names from repos """
        names = map(lambda pkg: pkg.name, self.sack.query())
        return sorted(set(names).union(set(self.guess_provide())))

    def guess_license(self):
        """ returns list of all known licenses """
        licenses = set()
        for pkg in self.sack.query():
            licenses.update(pkg.license)
        return sorted(licenses)
