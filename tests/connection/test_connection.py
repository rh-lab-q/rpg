from rpg.plugins.source_loader.download import DownloadPlugin
from rpg.plugins.source_loader.github import GithubDownloadPlugin
from rpg import Base
from tests.support import RpgTestCase
from os import remove


class Conf():

    exclude = []
    directories = []


class FakeBase(Base):

    def __init__(self):
        self.spec = None
        self.sack = None
        self.conf = Conf()
        self.load_plugins()


class PluginConnectionTest(RpgTestCase):

    def setUp(self):
        self.base = FakeBase()

    def test_download(self):
        down = DownloadPlugin()
        down.download(
            "https://www.github.com/rh-lab-q/rpg/archive/master.zip",
            self.test_project_dir / "temp")
        self.assertTrue((self.test_project_dir / "temp").exists(),
                        msg="Missing: {}".format(
                            str(self.test_project_dir / "temp")))

    def test_download_github(self):
        if (self.test_project_dir / "temp").exists():
            remove(str(self.test_project_dir / "temp"))
        down = GithubDownloadPlugin()
        self.assertTrue(down.download(
            "https://www.github.com/rh-lab-q/rpg",
            self.test_project_dir / "temp"))
        self.assertTrue((self.test_project_dir / "temp").exists(),
                        msg="Missing: {}".format(
                            str(self.test_project_dir / "temp")))

    def test_download_pick(self):
        if (self.test_project_dir / "temp").exists():
            remove(str(self.test_project_dir / "temp"))
        self.base._plugin_engine.execute_download(
            "https://www.github.com/rh-lab-q/rpg",
            self.test_project_dir / "temp")
        self.assertTrue((self.test_project_dir / "temp").exists(),
                        msg="Missing: {}".format(
                            str(self.test_project_dir / "temp")))

    def test_download_pick_fail(self):
        if (self.test_project_dir / "temp").exists():
            remove(str(self.test_project_dir / "temp"))
        self.base._plugin_engine.execute_download(
            "https://www.github.com/",
            self.test_project_dir / "temp")
        self.assertFalse((self.test_project_dir / "temp").exists(),
                         msg="Should be missing: {}".format(
                             str(self.test_project_dir / "temp")))

    def tearDown(self):
        if (self.test_project_dir / "temp").exists():
            remove(str(self.test_project_dir / "temp"))
