from os.path import expanduser
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QLineEdit, QCheckBox,
                             QGroupBox, QPushButton, QGridLayout,
                             QTextEdit, QFileDialog,
                             QComboBox, QWizard, QFrame)
from rpg.gui.dialogs import DialogImport
from rpg.utils import path_to_str
from pathlib import Path
from rpg.command import Command
import subprocess
import platform
from threading import Thread


class Wizard(QtWidgets.QWizard):

    ''' Main class that holds other pages, number of pages are in NUM_PAGES
        - to simply navigate between them
        - counted from 0 (PageIntro) to 12 (PageCoprFinal)
        - tooltips are from:
          https://fedoraproject.org/wiki/How_to_create_an_RPM_package '''

    NUM_PAGES = 13
    (PageIntro, PageImport, PageMandatory, PageSummary, PageScripts,
        PageInstall, PageRequires, PageUninstall, PageBuild, PageCoprLogin,
        PageCoprDistro, PageCoprBuild, PageCoprFinal) = range(NUM_PAGES)

    def __init__(self, base, parent=None):
        super(Wizard, self).__init__(parent)

        self.base = base
        self.base.tip_html_style = (
            "<html><head/><body><p><span style=\"font-size:12pt; " +
            "color:grey;\">%s</p></body></html>")
        self.setWindowTitle(self.tr("RPG"))
        self.setWizardStyle(self.ClassicStyle)
        btnList = ([QWizard.CancelButton, QWizard.Stretch,
                    QWizard.BackButton, QWizard.NextButton,
                    QWizard.FinishButton])
        self.setButtonLayout(btnList)
        self.setStyleSheet("QTextEdit { border-style: solid;" +
                           "border-width: 1px;" +
                           "border-color: rgb(178, 182, 178);" +
                           "border-radius: 3px;" +
                           "background-color:" +
                           "rgb(237, 237, 237);}")

        # Setting pages to wizard
        self.setPage(self.PageIntro, IntroPage(self))
        self.setPage(self.PageImport, ImportPage(self))
        self.setPage(self.PageMandatory, MandatoryPage(self))
        self.setPage(self.PageSummary, SummaryPage(self))
        self.setPage(self.PageScripts, ScriptsPage(self))
        self.setPage(self.PageInstall, InstallPage(self))
        self.setPage(self.PageRequires, RequiresPage(self))
        self.setPage(self.PageUninstall, UninstallPage(self))
        self.setPage(self.PageBuild, BuildPage(self))
        self.setPage(self.PageCoprLogin, CoprLoginPage(self))
        self.setPage(self.PageCoprDistro, CoprDistroPage(self))
        self.setPage(self.PageCoprBuild, CoprBuildPage(self))
        self.setPage(self.PageCoprFinal, CoprFinalPage(self))
        self.setStartId(self.PageIntro)


class IntroPage(QtWidgets.QWizardPage):

    def __init__(self, Wizard, parent=None):
        super(IntroPage, self).__init__(parent)

        self.base = Wizard.base

        self.textLabel = QLabel()
        self.textLabel.setText(
            "<html><head/><body><p><span style=\"font-size:14pt;\">" +
            "<h1>Welcome!</h1>" +
            "RPG - RPM Package Generator is tool, that guides you through" +
            " the creation of a RPM package.<br>" +
            "Please fill following details about your package.<br>For " +
            "more information use tool tips (under the labels).<br>" +
            "<strong>Note</strong>: All fields with the red asterisk " +
            "(<font color=\'#FF3333\'>*</font>) are required."
            "</p></body></html>")

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.textLabel, 0, 0, 1, 6)
        mainLayout.addSpacing(180)
        mainLayout.addLayout(grid)
        self.setLayout(mainLayout)

    def validatePage(self):
        return True

    def nextId(self):
        ''' [int] Function that determines the next page after the current one
            - returns integer value and then checks, which value is page"
            in NUM_PAGES'''

        return Wizard.PageImport


class ImportPage(QtWidgets.QWizardPage):

    def __init__(self, Wizard, parent=None):
        super(ImportPage, self).__init__(parent)

        self.base = Wizard.base
        self.redQLineEdit = ("QLineEdit { border-style: solid;" +
                             "border-width: 1px;" +
                             "border-color: #FF3333;" +
                             "border-radius: 3px;" +
                             "background-color:" +
                             "rgb(233,233,233);}")

        self.setTitle(self.tr("    Beginning"))
        self.setSubTitle(self.tr("Choose distribution and import " +
                                 "tarball or folder with source code"))

        self.importLabel = QLabel("Source<font color=\'#FF3333\'>*</font>")
        self.importEdit = QLineEdit()
        self.importEdit.setMinimumHeight(30)
        self.importLabel.setBuddy(self.importEdit)
        self.importLabelText = QLabel(
            self.base.tip_html_style %
            "Pristine source package (e.g. tarballs) and patches (required).")
        self.importEdit.textChanged.connect(self.checkPath)
        self.importEdit.setMinimumHeight(34)

        self.importButton = QPushButton("Import")
        self.importButton.setMinimumHeight(45)
        self.importButton.setMinimumWidth(115)
        self.importButton.clicked.connect(self.importPath)

        self.ArchLabel = QLabel("Architecture")
        self.ArchEdit = QComboBox()
        self.ArchEdit.setMinimumHeight(30)
        arch = platform.architecture()[0]
        if arch == "32bit":
            self.ArchEdit.addItem("i386")
            self.ArchEdit.addItem("x86_64")
        else:
            self.ArchEdit.addItem("x86_64")
            self.ArchEdit.addItem("i386")
        self.ArchLabel.setBuddy(self.ArchEdit)
        self.ArchLabelText = QLabel(
            self.base.tip_html_style %
            ("Choose target architecture (32 bit - i386 or 64 bit "
             "- x68_64)."))

        self.DistroLabel = QLabel("Distribution")
        self.DistroEdit = QComboBox()
        self.DistroEdit.setMinimumHeight(30)
        self.DistroEdit.addItem("fedora-22")
        self.DistroEdit.addItem("fedora-21")
        self.DistroEdit.addItem("fedora-20")
        self.DistroEdit.addItem("fedora-19")
        self.DistroEdit.addItem("fedora-rawhide")
        self.DistroEdit.addItem("epel-7")
        self.DistroEdit.addItem("epel-6")
        self.DistroEdit.addItem("epel-5")
        self.DistroLabel.setBuddy(self.DistroEdit)
        self.DistroLabelText = QLabel(
            self.base.tip_html_style %
            "Choose target distribution.")

        self.registerField("Source*", self.importEdit)

        mainLayout = QVBoxLayout()
        frame = QFrame()
        frameDistro = QFrame()
        frameArch = QFrame()
        frame.setFrameShape(QFrame.Panel)
        frame.setFrameShadow(QFrame.Sunken)
        frameDistro.setFrameShape(QFrame.Panel)
        frameDistro.setFrameShadow(QFrame.Sunken)
        frameArch.setFrameShape(QFrame.Panel)
        frameArch.setFrameShadow(QFrame.Sunken)
        gridArch = QGridLayout()
        gridImport = QGridLayout()
        gridDistro = QGridLayout()
        gridImport.addWidget(self.importLabel, 0, 0, 1, 1)
        gridImport.addWidget(self.importEdit, 0, 1, 1, 6)
        gridImport.addWidget(self.importButton, 0, 7, 1, 1)
        gridImport.addWidget(self.importLabelText, 1, 0, 1, 7)
        gridDistro.addWidget(self.DistroLabel, 0, 0, 1, 0)
        gridDistro.addWidget(self.DistroEdit, 0, 1, 1, 2)
        gridDistro.addWidget(self.DistroLabelText, 1, 0, 1, 7)
        gridArch .addWidget(self.ArchLabel, 0, 0, 1, 0)
        gridArch .addWidget(self.ArchEdit, 0, 1, 1, 2)
        gridArch .addWidget(self.ArchLabelText, 1, 0, 1, 7)
        mainLayout.addSpacing(25)
        frame.setLayout(gridImport)
        frameDistro.setLayout(gridDistro)
        frameArch.setLayout(gridArch)
        mainLayout.addWidget(frame)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameDistro)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameArch)
        self.setLayout(mainLayout)

    def checkPath(self):
        ''' Checks, if path to import is correct while typing'''
        path = Path(self.importEdit.text())
        if(path.exists()):
            self.importEdit.setStyleSheet("")
        else:
            self.importEdit.setStyleSheet(self.redQLineEdit)

    def importPath(self):
        ''' Returns path selected file or archive'''

        self.import_dialog = DialogImport()
        self.import_dialog.exec_()
        if (isinstance(self.import_dialog.filesSelected(), list)):
            path = self.import_dialog.filesSelected()
        else:
            path = self.import_dialog.selectedFiles()
        try:
            self.importEdit.setText(path[0])
        except IndexError:
            pass

    def validatePage(self):
        ''' [Bool] Function that invokes just after pressing the next button
            {True} - user moves to next page
            {False}- user blocked on current page
            ###### Setting up RPG class references ###### '''

        # Verifying path
        path = Path(self.importEdit.text())
        if(path.exists()):
            self.base.target_arch = self.ArchEdit.currentText()
            self.base.target_distro = self.DistroEdit.currentText()
            self.base.load_project_from_url(self.importEdit.text().strip())
            self.base.run_extracted_source_analysis()
            new_thread = Thread(
                target=self.base.fetch_repos, args=(self.base.target_distro,
                                                    self.base.target_arch))
            new_thread.start()
            self.importEdit.setStyleSheet("")
            return True
        else:
            self.importEdit.setStyleSheet(self.redQLineEdit)
            return False

    def nextId(self):
        ''' [int] Function that determines the next page after the current one
            - returns integer value and then checks, which value is page"
            in NUM_PAGES'''

        return Wizard.PageMandatory


class MandatoryPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.nameEdit.setText(str(self.base.spec.Name))
        self.versionEdit.setText(str(self.base.spec.Version))
        self.releaseEdit.setText("1")
        self.licenseEdit.setText(str(self.base.spec.License))
        self.URLEdit.setText(str(self.base.spec.URL))

    def __init__(self, Wizard, parent=None):
        super(MandatoryPage, self).__init__(parent)

        self.base = Wizard.base
        self.redQLineEdit = ("QLineEdit { border-style: solid;" +
                             "border-width: 1px;" +
                             "border-color: #FF3333;" +
                             "border-radius: 3px;" +
                             "background-color:" +
                             "rgb(233,233,233);}")

        self.setTitle(self.tr("    Mandatory fields"))
        self.setSubTitle(self.tr("Basic required information"))

        self.nameLabel = QLabel("Name<font color=\'#FF3333\'>*</font>")
        self.nameEdit = QLineEdit()
        self.nameEdit.setMinimumHeight(30)
        self.nameLabel.setBuddy(self.nameEdit)
        self.nameLabelText = QLabel(
            self.base.tip_html_style %
            ("The (base) name of the package, which should "
             "be unique (required)."))

        self.versionLabel = QLabel("Version<font color=\'#FF3333\'>*</font>")
        self.versionEdit = QLineEdit()
        self.versionEdit.textChanged.connect(self.checkVersion)
        self.versionEdit.setMinimumHeight(30)
        self.versionLabel.setBuddy(self.versionEdit)
        self.versionLabelText = QLabel(
            self.base.tip_html_style %
            ("The upstream version number, usually numbers "
             "separated by dots (e.g. 1.7.4) (required)."))

        self.releaseLabel = QLabel("Release<font color=\'#FF3333\'>*</font>")
        self.releaseEdit = QLineEdit()
        self.releaseEdit.setMinimumHeight(30)
        self.releaseLabel.setBuddy(self.releaseEdit)
        self.releaseLabelText = QLabel(
            self.base.tip_html_style %
            ("The initial value should be 1%{?dist}. "
             "Increment the number every time you release a new package "
             "(required)."))

        self.licenseLabel = QLabel("License<font color=\'#FF3333\'>*</font>")
        self.licenseEdit = QLineEdit()
        self.licenseEdit.setMinimumHeight(30)
        self.licenseLabel.setBuddy(self.licenseEdit)
        self.licenseLabelText = QLabel(
            self.base.tip_html_style %
            ("The license, which must be an open source software "
             "license (required)."))

        self.URLLabel = QLabel("URL: ")
        self.URLEdit = QLineEdit()
        self.URLEdit.setMinimumHeight(30)
        self.URLLabel.setBuddy(self.URLEdit)
        self.URLLabelText = QLabel(
            self.base.tip_html_style %
            ("The full URL for more information about the "
             "program (e.g. the project website)."))

        # Making mandatory fields:
        self.registerField("Name*", self.nameEdit)
        self.registerField("Version*", self.versionEdit)
        self.registerField("Release*", self.releaseEdit)
        self.registerField("License*", self.licenseEdit)

        mainLayout = QVBoxLayout()
        frameName = QFrame()
        frameVersion = QFrame()
        frameRelease = QFrame()
        frameLicense = QFrame()
        frameUrl = QFrame()
        frameName.setFrameShape(QFrame.Panel)
        frameName.setFrameShadow(QFrame.Sunken)
        frameVersion.setFrameShape(QFrame.Panel)
        frameVersion.setFrameShadow(QFrame.Sunken)
        frameRelease.setFrameShape(QFrame.Panel)
        frameRelease.setFrameShadow(QFrame.Sunken)
        frameLicense.setFrameShape(QFrame.Panel)
        frameLicense.setFrameShadow(QFrame.Sunken)
        frameUrl.setFrameShape(QFrame.Panel)
        frameUrl.setFrameShadow(QFrame.Sunken)
        gridName = QGridLayout()
        gridVersion = QGridLayout()
        gridRelease = QGridLayout()
        gridLicense = QGridLayout()
        gridUrl = QGridLayout()
        gridName.addWidget(self.nameLabel, 0, 0, 1, 1)
        gridName.addWidget(self.nameEdit, 0, 1, 1, 8)
        gridName.addWidget(self.nameLabelText, 1, 0, 1, 8)
        gridVersion.addWidget(self.versionLabel, 0, 0, 1, 1)
        gridVersion.addWidget(self.versionEdit, 0, 1, 1, 8)
        gridVersion.addWidget(self.versionLabelText, 1, 0, 1, 8)
        gridRelease.addWidget(self.releaseLabel, 0, 0, 1, 1)
        gridRelease.addWidget(self.releaseEdit, 0, 1, 1, 8)
        gridRelease.addWidget(self.releaseLabelText, 1, 0, 1, 8)
        gridLicense.addWidget(self.licenseLabel, 0, 0, 1, 1)
        gridLicense.addWidget(self.licenseEdit, 0, 1, 1, 8)
        gridLicense.addWidget(self.licenseLabelText, 1, 0, 1, 8)
        gridUrl.addWidget(self.URLLabel, 0, 0, 1, 1)
        gridUrl.addWidget(self.URLEdit, 0, 1, 1, 8)
        gridUrl.addWidget(self.URLLabelText, 1, 0, 1, 8)
        mainLayout.addSpacing(25)
        frameName.setLayout(gridName)
        frameVersion.setLayout(gridVersion)
        frameRelease.setLayout(gridRelease)
        frameLicense.setLayout(gridLicense)
        frameUrl.setLayout(gridUrl)
        mainLayout.addWidget(frameName)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameVersion)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameRelease)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameLicense)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameUrl)
        self.setLayout(mainLayout)

    def checkVersion(self):
        version = self.versionEdit.text()
        if '-' in version:
            self.versionEdit.setStyleSheet(self.redQLineEdit)
        else:
            self.versionEdit.setStyleSheet("")

    def validatePage(self):
        if '-' in self.versionEdit.text():
            self.versionEdit.setStyleSheet(self.redQLineEdit)
            return False
        else:
            self.versionEdit.setStyleSheet("")
            self.base.spec.Name = self.nameEdit.text()
            self.base.spec.Version = self.versionEdit.text()
            self.base.spec.Release = self.releaseEdit.text()
            self.base.spec.License = self.licenseEdit.text()
            self.base.spec.URL = self.URLEdit.text()
            return True

    def nextId(self):
        ''' [int] Function that determines the next page after the current one
            - returns integer value and then checks, which value is page"
            in NUM_PAGES'''
        return Wizard.PageSummary


class SummaryPage(QtWidgets.QWizardPage):

    def __init__(self, Wizard, parent=None):
        super(SummaryPage, self).__init__(parent)

        self.base = Wizard.base
        self.setTitle(self.tr("    Description fields"))
        self.setSubTitle(self.tr("Additional information"))

        self.summaryLabel = QLabel("Summary<font color=\'#FF3333\'>*</font>")
        self.summaryEdit = QLineEdit()
        self.summaryEdit.setMinimumHeight(30)
        self.summaryLabel.setBuddy(self.summaryEdit)
        self.summaryLabelText = QLabel(
            self.base.tip_html_style %
            ("A brief, one-line summary of the package. Use "
             "American English (required)."))

        self.descriptionLabel = QLabel("Description")
        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.setMinimumHeight(30)
        self.descriptionLabel.setBuddy(self.descriptionEdit)
        self.descriptionLabelText = QLabel(
            self.base.tip_html_style %
            "A longer, multi-line description of the program.")

        # Making mandatory fields:
        self.registerField("Summary*", self.summaryEdit)

        mainLayout = QVBoxLayout()
        frameSummary = QFrame()
        frameDescription = QFrame()
        frameSummary.setFrameShape(QFrame.Panel)
        frameSummary.setFrameShadow(QFrame.Sunken)
        frameDescription.setFrameShape(QFrame.Panel)
        frameDescription.setFrameShadow(QFrame.Sunken)
        gridSummary = QGridLayout()
        gridDescription = QGridLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        gridSummary.addWidget(self.summaryLabel, 0, 0, 1, 1)
        gridSummary.addWidget(self.summaryEdit, 0, 1, 1, 8)
        gridSummary.addWidget(self.summaryLabelText, 1, 0, 1, 8)
        gridDescription.addWidget(self.descriptionLabel, 0, 0, 1, 1)
        gridDescription.addWidget(self.descriptionEdit, 0, 1, 1, 8)
        gridDescription.addWidget(self.descriptionLabelText, 1, 0, 1, 8)
        mainLayout.addSpacing(25)
        frameSummary.setLayout(gridSummary)
        frameDescription.setLayout(gridDescription)
        mainLayout.addWidget(frameSummary)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameDescription)
        self.setLayout(mainLayout)

    def validatePage(self):
        if self.descriptionEdit.toPlainText() == '':
            self.base.spec.description = '%{summary}'
        else:
            self.base.spec.description = self.descriptionEdit.toPlainText()
        self.base.spec.Summary = self.summaryEdit.text()
        self.base.run_patched_source_analysis()
        return True

    def nextId(self):
        ''' [int] Function that determines the next page after the current one
            - returns integer value and then checks, which value is page"
            in NUM_PAGES'''
        return Wizard.PageScripts


class ScriptsPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.prepareEdit.setText(str(self.base.spec.prep))
        self.buildEdit.setText(str(self.base.spec.build))
        self.checkEdit.setText(str(self.base.spec.check))

    def __init__(self, Wizard, parent=None):
        super(ScriptsPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("    Package building information"))
        self.setSubTitle(self.tr(
            "Properties for building and testing of package"))

        self.textLabel = QLabel()
        self.textLabel.setText(
            "<html><head/><body><p><span style=\"font-size:12pt;\">" +
            "Please fill how extract sources, how compile them " +
            " and how run test if there are any.<br>" +
            "</p></body></html>")

        prepareLabel = QLabel("%prepare: ")
        self.prepareEdit = QTextEdit()
        prepareLabelText = QLabel(
            self.base.tip_html_style %
            ("Script commands to prepare the program (e.g. to "
             "uncompress it) so that it will be ready for building.<br>"
             "Typically this is just %autosetup; or "
             "%autosetup -n NAME if the source file unpacks into NAME."))

        buildLabel = QLabel("%build: ")
        self.buildEdit = QTextEdit()
        buildLabelText = QLabel(
            self.base.tip_html_style %
            ("Script commands to build the program (e.g. to compile it)"
             " and get it ready for installing."))

        checkLabel = QLabel("%check: ")
        self.checkEdit = QTextEdit()
        checkLabelText = QLabel(
            self.base.tip_html_style %
            "Script commands to test the program.")

        buildArchLabel = QLabel("BuildArch: ")
        self.buildArchCheckbox = QCheckBox("noarch")
        buildArchLabelText = QLabel(
            self.base.tip_html_style %
            ("If you're packaging files that are architecture-"
             "independent (e.g. shell scripts, data files), then add<br> "
             "BuildArch: noarch. The architecture for the binary RPM will "
             "then be noarch."))

        mainLayout = QVBoxLayout()
        framePrepare = QFrame()
        frameBuild = QFrame()
        frameCheck = QFrame()
        frameArch = QFrame()
        framePrepare.setFrameShape(QFrame.Panel)
        framePrepare.setFrameShadow(QFrame.Sunken)
        frameBuild.setFrameShape(QFrame.Panel)
        frameBuild.setFrameShadow(QFrame.Sunken)
        frameCheck.setFrameShape(QFrame.Panel)
        frameCheck.setFrameShadow(QFrame.Sunken)
        frameArch.setFrameShape(QFrame.Panel)
        frameArch.setFrameShadow(QFrame.Sunken)
        gridPrepare = QGridLayout()
        gridBuild = QGridLayout()
        gridCheck = QGridLayout()
        gridArch = QGridLayout()
        gridtext = QGridLayout()
        gridtext.addWidget(self.textLabel, 0, 0)
        gridPrepare.addWidget(prepareLabel, 0, 0, 1, 1)
        gridPrepare.addWidget(self.prepareEdit, 0, 1, 1, 8)
        gridPrepare.addWidget(prepareLabelText, 1, 0, 1, 8)
        gridBuild.addWidget(buildLabel, 0, 0, 1, 1)
        gridBuild.addWidget(self.buildEdit, 0, 1, 1, 8)
        gridBuild.addWidget(buildLabelText, 1, 0, 1, 8)
        gridCheck.addWidget(checkLabel, 0, 0, 1, 1)
        gridCheck.addWidget(self.checkEdit, 0, 1, 1, 8)
        gridCheck.addWidget(checkLabelText, 1, 0, 1, 8)
        gridArch.addWidget(buildArchLabel, 0, 0)
        gridArch.addWidget(self.buildArchCheckbox, 0, 1)
        gridArch.addWidget(buildArchLabelText, 1, 0, 1, 8)
        framePrepare.setLayout(gridPrepare)
        frameBuild.setLayout(gridBuild)
        frameCheck.setLayout(gridCheck)
        frameArch.setLayout(gridArch)
        mainLayout.addWidget(framePrepare)
        mainLayout.addWidget(frameBuild)
        mainLayout.addWidget(frameCheck)
        mainLayout.addWidget(frameArch)
        self.setLayout(mainLayout)

    def validatePage(self):
        self.base.spec.prep = Command(self.prepareEdit.toPlainText())
        self.base.spec.build = Command(self.buildEdit.toPlainText())
        self.base.spec.check = Command(self.checkEdit.toPlainText())
        if self.buildArchCheckbox.isChecked():
            self.base.spec.BuildArch = "noarch"
        self.base.build_project()
        self.base.run_compiled_source_analysis()
        return True

    def nextId(self):
        return Wizard.PageInstall


class InstallPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.installEdit.setText(str(self.base.spec.install))
        self.pretransEdit.setText(str(self.base.spec.pretrans))
        self.preEdit.setText(str(self.base.spec.pre))
        self.postEdit.setText(str(self.base.spec.post))

    def __init__(self, Wizard, parent=None):
        super(InstallPage, self).__init__(parent)

        self.base = Wizard.base
        self.setTitle(self.tr("    Package installation information"))
        self.setSubTitle(self.tr(
            "Properties for installation of package"))

        self.textLabel = QLabel()
        self.textLabel.setText(
            "<html><head/><body><p><span style=\"font-size:12pt;\">" +
            "Please fill commands to execute before installation, " +
            "how install your files and what to do after installation." +
            "</p></body></html>")

        pretransLabel = QLabel("%pretrans: ")
        self.pretransEdit = QTextEdit()
        pretransLabelText = QLabel(
            self.base.tip_html_style %
            "At the start of transaction.")

        preLabel = QLabel("%pre: ")
        self.preEdit = QTextEdit()
        preLabelText = QLabel(
            self.base.tip_html_style %
            "Before a package is installed.")

        installLabel = QLabel("%install: ")
        self.installEdit = QTextEdit()
        installLabelText = QLabel(
            self.base.tip_html_style %
            "Script commands to install the program.")

        postLabel = QLabel("%post: ")
        self.postEdit = QTextEdit()
        postLabelText = QLabel(
            self.base.tip_html_style %
            "After a package is installed.")

        mainLayout = QVBoxLayout()
        framePretrans = QFrame()
        framePre = QFrame()
        frameInstall = QFrame()
        framePost = QFrame()
        framePretrans.setFrameShape(QFrame.Panel)
        framePretrans.setFrameShadow(QFrame.Sunken)
        framePre.setFrameShape(QFrame.Panel)
        framePre.setFrameShadow(QFrame.Sunken)
        frameInstall.setFrameShape(QFrame.Panel)
        frameInstall.setFrameShadow(QFrame.Sunken)
        framePost.setFrameShape(QFrame.Panel)
        framePost.setFrameShadow(QFrame.Sunken)
        gridPretrans = QGridLayout()
        gridPre = QGridLayout()
        gridInstall = QGridLayout()
        gridPost = QGridLayout()
        gridtext = QGridLayout()
        gridtext.addWidget(self.textLabel, 0, 0)
        gridPretrans.addWidget(pretransLabel, 0, 0, 1, 1)
        gridPretrans.addWidget(self.pretransEdit, 0, 1, 1, 8)
        gridPretrans.addWidget(pretransLabelText, 1, 0, 1, 8)
        gridPre.addWidget(preLabel, 0, 0, 1, 1)
        gridPre.addWidget(self.preEdit, 0, 1, 1, 8)
        gridPre.addWidget(preLabelText, 1, 0, 1, 8)
        gridInstall.addWidget(installLabel, 0, 0, 1, 1)
        gridInstall.addWidget(self.installEdit, 0, 1, 1, 8)
        gridInstall.addWidget(installLabelText, 1, 0, 1, 8)
        gridPost.addWidget(postLabel, 0, 0, 1, 1)
        gridPost.addWidget(self.postEdit, 0, 1, 1, 8)
        gridPost.addWidget(postLabelText, 1, 0, 1, 8)
        mainLayout.addSpacing(25)
        framePretrans.setLayout(gridPretrans)
        framePre.setLayout(gridPre)
        frameInstall.setLayout(gridInstall)
        framePost.setLayout(gridPost)
        mainLayout.addLayout(gridtext)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(framePretrans)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(framePre)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameInstall)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(framePost)
        self.setLayout(mainLayout)

    def validatePage(self):
        self.base.spec.install = Command(self.installEdit.toPlainText())
        self.base.spec.pretrans = Command(self.pretransEdit.toPlainText())
        self.base.spec.pre = Command(self.preEdit.toPlainText())
        self.base.spec.post = Command(self.postEdit.toPlainText())
        self.base.install_project()
        self.base.run_installed_source_analysis()
        return True

    def nextId(self):
        return Wizard.PageRequires


class RequiresPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.bRequiresEdit.setText('\n'.join(self.base.spec.BuildRequires))
        self.requiresEdit.setText('\n'.join(self.base.spec.Requires))
        self.providesEdit.setText('\n'.join(self.base.spec.Provides))

    def __init__(self, Wizard, parent=None):
        super(RequiresPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("    Requires page"))
        self.setSubTitle(self.tr("Write requires and provides"))

        buildRequiresLabel = QLabel("BuildRequires: ")
        self.bRequiresEdit = QTextEdit()
        self.bRequiresEdit.setMaximumHeight(220)
        buildRequiresLabelText = QLabel(
            self.base.tip_html_style %
            ("A line-separated list of packages required for building "
             "(compiling) the program."))

        self.textLabel = QLabel()
        self.textLabel.setText(
            "<html><head/><body><p><span style=\"font-size:12pt;\">" +
            "Add required packages for compilation and run. <br> " +
            "</p></body><html>")

        requiresLabel = QLabel("Requires: ")
        self.requiresEdit = QTextEdit()
        self.requiresEdit.setMaximumHeight(220)
        requiresLabelText = QLabel(
            self.base.tip_html_style %
            ("A line-separate list of packages that are required "
             "when the program is installed."))

        providesLabel = QLabel("Provides: ")
        self.providesEdit = QTextEdit()
        providesLabelText = QLabel(
            self.base.tip_html_style %
            "List virtual package names that this package provides.")

        mainLayout = QVBoxLayout()
        frameBrequires = QFrame()
        frameRequires = QFrame()
        frameProvides = QFrame()
        frameBrequires.setFrameShape(QFrame.Panel)
        frameBrequires.setFrameShadow(QFrame.Sunken)
        frameRequires.setFrameShape(QFrame.Panel)
        frameRequires.setFrameShadow(QFrame.Sunken)
        frameProvides.setFrameShape(QFrame.Panel)
        frameProvides.setFrameShadow(QFrame.Sunken)
        gridBrequires = QGridLayout()
        gridRequires = QGridLayout()
        gridProvides = QGridLayout()
        gridtext = QGridLayout()
        gridtext.addWidget(self.textLabel, 0, 0)
        gridBrequires.addWidget(buildRequiresLabel, 0, 0, 1, 1)
        gridBrequires.addWidget(self.bRequiresEdit, 0, 1, 1, 8)
        gridBrequires.addWidget(buildRequiresLabelText, 1, 0, 1, 8)
        gridRequires.addWidget(requiresLabel, 0, 0, 1, 1)
        gridRequires.addWidget(self.requiresEdit, 0, 1, 1, 8)
        gridRequires.addWidget(requiresLabelText, 1, 0, 1, 8)
        gridProvides.addWidget(providesLabel, 0, 0, 1, 1)
        gridProvides.addWidget(self.providesEdit, 0, 1, 1, 8)
        gridProvides.addWidget(providesLabelText, 1, 0, 1, 8)
        mainLayout.addSpacing(25)
        frameBrequires.setLayout(gridBrequires)
        frameRequires.setLayout(gridRequires)
        frameProvides.setLayout(gridProvides)
        mainLayout.addLayout(gridtext)
        mainLayout.addWidget(frameBrequires)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameRequires)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameProvides)
        self.setLayout(mainLayout)

    def validatePage(self):
        self.base.spec.BuildRequires = self.bRequiresEdit.toPlainText()
        self.base.spec.Requires = self.requiresEdit.toPlainText()
        self.base.spec.Provides = self.providesEdit.toPlainText()
        self.base.spec.BuildRequires = set(
            self.base.spec.BuildRequires.splitlines())
        self.base.spec.Requires = set(self.base.spec.Requires.splitlines())
        self.base.spec.Provides = set(self.base.spec.Provides.splitlines())
        return True

    def nextId(self):
        return Wizard.PageUninstall


class UninstallPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.postunEdit.setText(str(self.base.spec.postun))
        self.preunEdit.setText(str(self.base.spec.preun))
        self.posttransEdit.setText(str(self.base.spec.posttrans))

    def __init__(self, Wizard, parent=None):
        super(UninstallPage, self).__init__(parent)

        self.base = Wizard.base
        self.setTitle(self.tr("    Package uninstallation information"))
        self.setSubTitle(self.tr(
            "Properties for uninstallation of package"))

        self.textLabel = QLabel()
        self.textLabel.setText(
            "<html><head/><body><p><span style=\"font-size:12pt;\">" +
            "Please fill commands to execute before uninstallation " +
            "and what to do after uninstallation.<br></p></body></html>")

        preunLabel = QLabel("%preun: ")
        self.preunEdit = QTextEdit()
        preunLabelText = QLabel(
            self.base.tip_html_style %
            "Before a package is uninstalled.")

        postunLabel = QLabel("%postun: ")
        self.postunEdit = QTextEdit()
        postunLabelText = QLabel(
            self.base.tip_html_style %
            "After a package is uninstalled.")

        posttransLabel = QLabel("%posttrans: ")
        self.posttransEdit = QTextEdit()
        posttransLabelText = QLabel(
            self.base.tip_html_style %
            "At the end of transaction.")

        mainLayout = QVBoxLayout()
        framePreun = QFrame()
        framePostun = QFrame()
        framePosttrans = QFrame()
        framePreun.setFrameShape(QFrame.Panel)
        framePreun.setFrameShadow(QFrame.Sunken)
        framePostun.setFrameShape(QFrame.Panel)
        framePostun.setFrameShadow(QFrame.Sunken)
        framePosttrans.setFrameShape(QFrame.Panel)
        framePosttrans.setFrameShadow(QFrame.Sunken)
        gridPreun = QGridLayout()
        gridPostun = QGridLayout()
        gridPosttrans = QGridLayout()
        gridtext = QGridLayout()
        gridtext.addWidget(self.textLabel, 0, 0)
        gridPreun.addWidget(preunLabel, 0, 0, 1, 1)
        gridPreun.addWidget(self.preunEdit, 0, 1, 1, 8)
        gridPreun.addWidget(preunLabelText, 1, 0, 1, 8)
        gridPostun.addWidget(postunLabel, 0, 0, 1, 1)
        gridPostun.addWidget(self.postunEdit, 0, 1, 1, 8)
        gridPostun.addWidget(postunLabelText, 1, 0, 1, 8)
        gridPosttrans.addWidget(posttransLabel, 0, 0, 1, 1)
        gridPosttrans.addWidget(self.posttransEdit, 0, 1, 1, 8)
        gridPosttrans.addWidget(posttransLabelText, 1, 0, 1, 8)
        mainLayout.addSpacing(25)
        framePreun.setLayout(gridPreun)
        framePostun.setLayout(gridPostun)
        framePosttrans.setLayout(gridPosttrans)
        mainLayout.addLayout(gridtext)
        mainLayout.addWidget(framePreun)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(framePostun)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(framePosttrans)
        self.setLayout(mainLayout)

    def validatePage(self):
        self.base.spec.postun = Command(self.postunEdit.toPlainText())
        self.base.spec.preun = Command(self.preunEdit.toPlainText())
        self.base.spec.posttrans = Command(self.posttransEdit.toPlainText())
        self.base.write_spec()
        return True

    def nextId(self):
        return Wizard.PageBuild


class BuildPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.buildLocationEdit.setText(expanduser("~"))
        self.distro = self.base.target_distro
        self.arch = self.base.target_arch
        index = self.BuildDistroEdit.findText(
            self.distro, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.BuildDistroEdit.setCurrentIndex(index)
        index = self.BuildArchEdit.findText(
            self.arch, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.BuildArchEdit.setCurrentIndex(index)

    def __init__(self, Wizard, parent=None):
        super(BuildPage, self).__init__(parent)

        self.base = Wizard.base
        self.Wizard = Wizard  # Main wizard of program
        self.setTitle(self.tr("    Build page"))
        self.setSubTitle(self.tr("Options to build"))

        specEditBox = QGroupBox()
        layoutspecEditBox = QGridLayout()
        buildPathBox = QGroupBox()
        layoutbuildPathBox = QGridLayout()
        buildSRPMBox = QGroupBox()
        layoutbuildSRPMBox = QGridLayout()
        buildRPMBox = QGroupBox()
        layoutbuildRPMBox = QGridLayout()

        specEditBox.setTitle("SPEC file")
        specWarningLabel = QLabel(
            self.base.tip_html_style %
            ("Edit manually the SPEC file that generates RPM package "
             "(advanced users)."))
        self.editSpecButton = QPushButton("Edit SPEC file")
        self.editSpecButton.clicked.connect(self.editSpecFile)
        self.editSpecButton.setMinimumHeight(40)
        self.editSpecButton.setMinimumWidth(180)
        self.editSpecButton.setMaximumHeight(40)
        self.editSpecButton.setMaximumWidth(180)
        layoutspecEditBox.addWidget(specWarningLabel, 0, 0)
        layoutspecEditBox.addWidget(self.editSpecButton, 1, 1)
        specEditBox.setLayout(layoutspecEditBox)

        buildPathBox.setTitle("Target build directory")
        buildPathLabel = QLabel(
            self.base.tip_html_style %
            "Build packages into selected directory.")
        self.buildLocationEdit = QLineEdit()
        self.buildLocationEdit.setMinimumHeight(35)
        self.buildToButton = QPushButton("Change path")
        self.buildToButton.setMinimumHeight(35)
        self.buildToButton.clicked.connect(self.openBuildPathFileDialog)
        layoutbuildPathBox.addWidget(buildPathLabel)
        layoutbuildPathBox.addWidget(self.buildLocationEdit, 1, 0)
        layoutbuildPathBox.addWidget(self.buildToButton, 1, 1)
        buildPathBox.setLayout(layoutbuildPathBox)

        buildSRPMLabel = QLabel(
            self.base.tip_html_style %
            ("Build packages containing source codes and spec files "
             "(not compiled to any specific architecture)."))
        self.textBuildSRPMLabel = QLabel()
        self.buildSRPMButton = QPushButton("Build source package")
        self.buildSRPMButton.setMinimumHeight(40)
        self.buildSRPMButton.setMinimumWidth(180)
        self.buildSRPMButton.setMaximumHeight(40)
        self.buildSRPMButton.setMaximumWidth(180)
        self.buildSRPMButton.clicked.connect(self.buildSrpm)
        layoutbuildSRPMBox.addWidget(buildSRPMLabel, 0, 0, 1, 2)
        layoutbuildSRPMBox.addWidget(self.textBuildSRPMLabel, 1, 0)
        layoutbuildSRPMBox.addWidget(self.buildSRPMButton, 1, 1)
        buildSRPMBox.setLayout(layoutbuildSRPMBox)

        buildRPMLabel = QLabel(
            self.base.tip_html_style %
            ("Build packages compiled for specific "
             "distribution and architecture."))
        self.textBuildRPMLabel = QLabel()
        self.BuildArchLabel = QLabel("    Architecture")
        self.BuildArchEdit = QComboBox()
        self.BuildArchEdit.setMaximumWidth(200)
        self.BuildArchEdit.setMinimumHeight(30)
        self.BuildArchEdit.addItem("i386")
        self.BuildArchEdit.addItem("x86_64")
        self.BuildArchLabel.setBuddy(self.BuildArchEdit)
        self.BuildArchLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.BuildArchLabel.setToolTip(
            "Choose architekture (32 bit - i386 or 64 bit - x68_64).")
        self.BuildDistroLabel = QLabel("    Distribution")
        self.BuildDistroEdit = QComboBox()
        self.BuildDistroEdit.setMaximumWidth(200)
        self.BuildDistroEdit.setMinimumHeight(30)
        self.BuildDistroEdit.addItem("fedora-22")
        self.BuildDistroEdit.addItem("fedora-21")
        self.BuildDistroEdit.addItem("fedora-20")
        self.BuildDistroEdit.addItem("fedora-19")
        self.BuildDistroEdit.addItem("fedora-rawhide")
        self.BuildDistroEdit.addItem("epel-7")
        self.BuildDistroEdit.addItem("epel-6")
        self.BuildDistroEdit.addItem("epel-5")
        self.BuildDistroLabel.setBuddy(self.BuildDistroEdit)
        self.BuildDistroLabel.setCursor(
            QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.BuildDistroLabel.setToolTip("Choose distribution")
        self.buildRPMButton = QPushButton("Build package")
        self.buildRPMButton.setMinimumHeight(40)
        self.buildRPMButton.setMinimumWidth(180)
        self.buildRPMButton.setMaximumHeight(40)
        self.buildRPMButton.setMaximumWidth(180)
        self.buildRPMButton.clicked.connect(self.buildRpm)
        layoutbuildRPMBox.addWidget(buildRPMLabel, 0, 0, 1, 6)
        layoutbuildRPMBox.addWidget(self.BuildArchLabel, 1, 0, 1, 1)
        layoutbuildRPMBox.addWidget(self.BuildArchEdit, 1, 1, 1, 2)
        layoutbuildRPMBox.addWidget(self.BuildDistroLabel, 2, 0, 1, 1)
        layoutbuildRPMBox.addWidget(self.BuildDistroEdit, 2, 1, 1, 2)
        layoutbuildRPMBox.addWidget(self.textBuildRPMLabel, 3, 0)
        layoutbuildRPMBox.addWidget(self.buildRPMButton, 3, 7)
        buildRPMBox.setLayout(layoutbuildRPMBox)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(specEditBox)
        mainLayout.addWidget(buildPathBox)
        mainLayout.addWidget(buildSRPMBox)
        mainLayout.addWidget(buildRPMBox)
        self.setLayout(mainLayout)

    def validatePage(self):
        return True

    def editSpecFile(self):
        '''If user clicked Edit SPEC file,
           default text editor with the file is open'''
        subprocess.call(('xdg-open', str(self.base.spec_path)))

    def openBuildPathFileDialog(self):
        brows = QFileDialog()
        self.getPath = brows.getExistingDirectory(self,
                                                  "Select Directory",
                                                  expanduser("~"),
                                                  QFileDialog.ShowDirsOnly)
        self.buildLocationEdit.setText(self.getPath)

    def buildSrpm(self):
        self.textBuildSRPMLabel.setText('Building SRPM...')
        self.textBuildSRPMLabel.repaint()
        self.base.build_srpm()
        Command("cp " + path_to_str(self.base.srpm_path) + " " +
                self.buildLocationEdit.text()).execute()
        self.base.final_path = self.buildLocationEdit.text()
        self.textBuildSRPMLabel.setText('Your source package was build in '
                                        + self.base.final_path)

    def buildRpm(self):
        self.textBuildRPMLabel.setText('Building RPM...')
        self.textBuildSRPMLabel.repaint()
        self.base.final_path = self.buildLocationEdit.text()
        arch = self.BuildArchEdit.currentText()
        distro = self.BuildDistroEdit.currentText()
        self.base.build_rpm_recover(distro, arch)
        packages = self.base.rpm_path
        for package in packages:
            Command("cp " + str(package) + " " +
                    self.base.final_path).execute()
        self.textBuildRPMLabel.setText(
            'Your package was build in ' + self.base.final_path)

    def nextId(self):
        return Wizard.PageCoprLogin


class CoprLoginPage(QtWidgets.QWizardPage):

    def __init__(self, Wizard, parent=None):
        super(CoprLoginPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("    Copr page"))
        self.setSubTitle(self.tr("Copr mandatory information"))

        self.textLoginLabel = QLabel()
        self.textLoginLabel.setText(
            "<html><head/><body><p align=\"left\"><span" +
            "style=\" font-size:24pt;\">For upload and " +
            "build package in Copr you need an account " +
            "on <a href=\"https://copr.fedoraproject.org/api\">" +
            "Copr API</a>. Please log in and copy your information.<br>" +
            " It will be saved on config file, but nowhere else." +
            "</span></p></body></html>")

        self.usernameLabel = QLabel("Username<font color=\'#FF3333\'>*</font>")
        self.usernameEdit = QLineEdit()
        self.usernameEdit.setMinimumHeight(30)
        self.usernameLabel.setBuddy(self.usernameEdit)
        self.usernameLabelText = QLabel(
            self.base.tip_html_style %
            "Your username from Copr API (required).")

        self.loginLabel = QLabel("Login<font color=\'#FF3333\'>*</font>")
        self.loginEdit = QLineEdit()
        self.loginEdit.setMinimumHeight(30)
        self.loginLabel.setBuddy(self.loginEdit)
        self.loginLabelText = QLabel(
            self.base.tip_html_style %
            "Your login (not username!) from Copr API (required).")

        self.tokenLabel = QLabel("Token<font color=\'#FF3333\'>*</font>")
        self.tokenEdit = QLineEdit()
        self.tokenEdit.setMinimumHeight(30)
        self.tokenLabel.setBuddy(self.tokenEdit)
        self.tokenLabelText = QLabel(
            self.base.tip_html_style %
            "Your token from Copr API (required).")

        self.packageNameLabel = QLabel("Name<font color=\'#FF3333\'>*</font>")
        self.packageNameEdit = QLineEdit()
        self.packageNameEdit.setMinimumHeight(30)
        self.packageNameLabel.setBuddy(self.packageNameEdit)
        self.packageNameLabelText = QLabel(
            self.base.tip_html_style %
            "Name of your package. It MUST be unique (required).")

        self.packageUrlLabel = QLabel("Url<font color=\'#FF3333\'>*</font>")
        self.packageUrlEdit = QLineEdit()
        self.packageUrlEdit.setMinimumHeight(30)
        self.packageUrlLabel.setBuddy(self.packageUrlEdit)
        self.packageUrlLabelText = QLabel(
            self.base.tip_html_style %
            ("An url of your package (a public web site). "
             "You can also use path of local package (required)."))

        self.importButton = QPushButton("Import")
        self.importButton.setMinimumHeight(45)
        self.importButton.setMinimumWidth(115)
        self.importButton.clicked.connect(self.importPath)

        # Making mandatory fields:
        self.registerField("Username*", self.usernameEdit)
        self.registerField("Login*", self.loginEdit)
        self.registerField("Token*", self.tokenEdit)
        self.registerField("PName*", self.packageNameEdit)
        self.registerField("Url*", self.packageUrlEdit)

        mainLayout = QVBoxLayout()
        frameUsername = QFrame()
        frameUsername.setFrameShape(QFrame.Panel)
        frameUsername.setFrameShadow(QFrame.Sunken)
        frameLogin = QFrame()
        frameLogin.setFrameShape(QFrame.Panel)
        frameLogin.setFrameShadow(QFrame.Sunken)
        frameToken = QFrame()
        frameToken.setFrameShape(QFrame.Panel)
        frameToken.setFrameShadow(QFrame.Sunken)
        frameName = QFrame()
        frameName.setFrameShape(QFrame.Panel)
        frameName.setFrameShadow(QFrame.Sunken)
        frameUrl = QFrame()
        frameUrl.setFrameShape(QFrame.Panel)
        frameUrl.setFrameShadow(QFrame.Sunken)
        gridLoginText = QGridLayout()
        gridLoginText.addWidget(self.textLoginLabel, 0, 1, 1, 1)

        gridUsername = QGridLayout()
        gridLogin = QGridLayout()
        gridToken = QGridLayout()
        gridName = QGridLayout()
        gridUrl = QGridLayout()
        gridUsername.addWidget(self.usernameLabel, 0, 0, 1, 1)
        gridUsername.addWidget(self.usernameEdit, 0, 1, 1, 8)
        gridUsername.addWidget(self.usernameLabelText, 1, 0, 1, 8)
        gridLogin.addWidget(self.loginLabel, 0, 0, 1, 1)
        gridLogin.addWidget(self.loginEdit, 0, 1, 1, 8)
        gridLogin.addWidget(self.loginLabelText, 1, 0, 1, 8)
        gridToken.addWidget(self.tokenLabel, 0, 0, 1, 1)
        gridToken.addWidget(self.tokenEdit, 0, 1, 1, 8)
        gridToken.addWidget(self.tokenLabelText, 1, 0, 1, 8)
        gridName.addWidget(self.packageNameLabel, 0, 0, 1, 1)
        gridName.addWidget(self.packageNameEdit, 0, 1, 1, 8)
        gridName.addWidget(self.packageNameLabelText, 1, 0, 1, 8)
        gridUrl.addWidget(self.packageUrlLabel, 0, 0, 1, 1)
        gridUrl.addWidget(self.packageUrlEdit, 0, 1, 1, 6)
        gridUrl.addWidget(self.importButton, 0, 7, 1, 1)
        gridUrl.addWidget(self.packageUrlLabelText, 1, 0, 1, 8)

        frameUsername.setLayout(gridUsername)
        frameLogin.setLayout(gridLogin)
        frameToken.setLayout(gridToken)
        frameName.setLayout(gridName)
        frameUrl.setLayout(gridUrl)
        mainLayout.addSpacing(25)
        mainLayout.addLayout(gridLoginText)
        mainLayout.addWidget(frameUsername)
        mainLayout.addWidget(frameLogin)
        mainLayout.addWidget(frameToken)
        mainLayout.addWidget(frameName)
        mainLayout.addWidget(frameUrl)
        self.setLayout(mainLayout)

    def importPath(self):
        ''' Returns path selected file or archive'''

        self.import_dialog = DialogImport()
        self.import_dialog.exec_()
        if (isinstance(self.import_dialog.filesSelected(), list)):
            path = self.import_dialog.filesSelected()
        else:
            path = self.import_dialog.selectedFiles()
        try:
            self.packageUrlEdit.setText(path[0])
        except IndexError:
            pass

    def validatePage(self):
        self.base.coprusername = self.usernameEdit.text()
        self.base.coprpackageName = self.packageNameEdit.text()
        self.base.coprpackageUrl = self.packageUrlEdit.text()
        self.base.coprlogin = self.loginEdit.text()
        self.base.coprtoken = self.tokenEdit.text()
        self.base.copr_set_config(self.base.coprusername,
                                  self.base.coprlogin, self.base.coprtoken)
        return True

    def nextId(self):
        return Wizard.PageCoprDistro


class CoprDistroPage(QtWidgets.QWizardPage):

    def __init__(self, Wizard, parent=None):
        super(CoprDistroPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("    Copr page"))
        self.setSubTitle(self.tr("Copr mandatory information"))

        self.Fedora22_CheckBox = QCheckBox("fedora-22")
        self.Fedora22_CheckBox.setCheckState(QtCore.Qt.Checked)
        self.Fedora21_CheckBox = QCheckBox("fedora-21")
        self.Fedora20_CheckBox = QCheckBox("fedora-20")
        self.Fedoraraw_CheckBox = QCheckBox("fedora-rawhide")
        self.EPEL7_CheckBox = QCheckBox("epel-7")
        self.EPEL6_CheckBox = QCheckBox("epel-6")
        self.EPEL5_CheckBox = QCheckBox("epel-5")
        self.i386_CheckBox = QCheckBox("i386")
        self.i386_CheckBox.setCheckState(QtCore.Qt.Checked)
        self.x64_CheckBox = QCheckBox("x86_64")
        self.x64_CheckBox.setCheckState(QtCore.Qt.Checked)

        grid = QGridLayout()
        grid = QGridLayout()
        framerelease = QFrame()
        framerelease.setFrameShape(QFrame.Panel)
        framerelease.setFrameShadow(QFrame.Sunken)

        releaseBoxLabel = QLabel("Choose distribution" +
                                 "<font color=\'#FF3333\'>*</font>")
        releaseArchBoxLabel = QLabel("Choose architecture" +
                                     "<font color=\'#FF3333\'>*</font>")
        grid.addWidget(releaseBoxLabel, 0, 0, 1, 1)
        grid.addWidget(self.Fedora22_CheckBox, 1, 1)
        grid.addWidget(self.Fedora21_CheckBox, 1, 2)
        grid.addWidget(self.Fedora20_CheckBox, 1, 3)
        grid.addWidget(self.EPEL7_CheckBox, 2, 1)
        grid.addWidget(self.EPEL6_CheckBox, 2, 2)
        grid.addWidget(self.EPEL5_CheckBox, 2, 3)
        grid.setVerticalSpacing(20)
        grid.addWidget(releaseArchBoxLabel, 3, 0, 1, 1)
        grid.addWidget(self.x64_CheckBox, 4, 1)
        grid.addWidget(self.i386_CheckBox, 4, 2)

        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(25)
        framerelease.setLayout(grid)
        mainLayout.addWidget(framerelease)
        self.setLayout(mainLayout)

    def validatePage(self):
        self.versionList = [
            self.Fedora22_CheckBox, self.Fedora21_CheckBox,
            self.Fedora20_CheckBox, self.Fedoraraw_CheckBox,
            self.EPEL7_CheckBox, self.EPEL6_CheckBox, self.EPEL5_CheckBox]
        self.archList = [self.i386_CheckBox, self.x64_CheckBox]
        self.base.coprversion = []
        for checkbox in self.versionList:
            if checkbox.isChecked():
                if self.i386_CheckBox.isChecked():
                    distro = checkbox.text() + '-i386'
                    self.base.coprversion.append(distro)
                else:
                    distro = checkbox.text() + '-x86_64'
                    self.base.coprversion.append(distro)

        if not self.base.coprversion:
            return False
        return True

    def nextId(self):
        return Wizard.PageCoprBuild


class CoprBuildPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.newproject = self.base.coprusername + \
            "/" + self.base.coprpackageName

        self.textBuildLabel.setText(
            "<html><head/><body><p align=\"left\"><span" +
            "style=\" font-size:24pt;\">" +
            "New project " + self.newproject +
            " will be created. <br>" +
            "You can also add descriptions and instructions" +
            " for your package. <br>" +
            "Next step will build package with Copr." +
            "</span></p></body></html>")

    def __init__(self, Wizard, parent=None):
        super(CoprBuildPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("    Copr build page"))
        self.setSubTitle(self.tr("Copr additional information"))

        self.textBuildLabel = QLabel()

        self.packageDescLabel = QLabel("Description ")
        self.packageDescEdit = QTextEdit()
        self.packageDescLabelText = QLabel(
            self.base.tip_html_style %
            "Description for your package, optional.")

        self.packageInstuctionLabel = QLabel("Instructions ")
        self.packageInstuctionEdit = QTextEdit()
        self.packageInstuctionLabelText = QLabel(
            self.base.tip_html_style %
            ("How install your project, where users can report bugs "
             "and issues. Or wiki link, optional."))

        mainLayout = QVBoxLayout()
        frameDesc = QFrame()
        frameInstuction = QFrame()
        frameDesc.setFrameShape(QFrame.Panel)
        frameDesc.setFrameShadow(QFrame.Sunken)
        frameInstuction.setFrameShape(QFrame.Panel)
        frameInstuction.setFrameShadow(QFrame.Sunken)
        gridBuildText = QGridLayout()
        gridBuildText.addWidget(self.textBuildLabel, 0, 1, 1, 1)

        gridDesc = QGridLayout()
        gridInstuction = QGridLayout()
        gridDesc.addWidget(self.packageDescLabel, 0, 0, 1, 1)
        gridDesc.addWidget(self.packageDescEdit, 0, 1, 1, 8)
        gridDesc.addWidget(self.packageDescLabelText, 1, 0, 1, 8)
        gridInstuction.addWidget(self.packageInstuctionLabel, 0, 0, 1, 1)
        gridInstuction.addWidget(self.packageInstuctionEdit, 0, 1, 1, 8)
        gridInstuction.addWidget(self.packageInstuctionLabelText, 1, 0, 1, 8)

        mainLayout.addSpacing(25)
        frameDesc.setLayout(gridDesc)
        frameInstuction.setLayout(gridInstuction)
        mainLayout.addLayout(gridBuildText)
        mainLayout.addWidget(frameDesc)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(frameInstuction)
        mainLayout.addSpacing(15)
        self.setLayout(mainLayout)

    def validatePage(self):
        self.textBuildLabel.setText(
            "<html><head/><body><p align=\"left\"><span" +
            "style=\" font-size:24pt;\">" +
            "Creating new project..." +
            "</span></p></body></html>")
        self.textBuildLabel.repaint()
        self.base.coprdesc = self.packageDescEdit.toPlainText()
        self.base.coprintro = self.packageInstuctionEdit.toPlainText()
        try:
            self.base.copr_create_project(self.base.coprpackageName,
                                          self.base.coprversion,
                                          self.base.coprdesc,
                                          self.base.coprintro)
        except subprocess.CalledProcessError:
            self.textBuildLabel.setText(
                "<html><head/><body><p align=\"left\"><span" +
                "style=\" font-size:24pt;\" font color=\'#FF3333\'>" +
                "Error in creating project!" +
                "<br> Please check your log in information" +
                "</span></p></body></html>")
            return False
        self.textBuildLabel.setText(
            "<html><head/><body><p align=\"left\"><span" +
            "style=\" font-size:24pt;\">" +
            "Creating new project - DONE<br>" +
            "Build proccess started...<br>" +
            "It takes a while, but it may be safely interrupted."
            "</span></p></body></html>")
        self.textBuildLabel.repaint()
        try:
            self.base.copr_build(
                self.base.coprpackageName, self.base.coprpackageUrl)
        except subprocess.CalledProcessError:
            self.textBuildLabel.setText(
                "<html><head/><body><p align=\"left\"><span" +
                "style=\" font-size:24pt;\" font color=\'#FF3333\'>" +
                "Error in building project!" +
                "<br> Please check your url information" +
                "</span></p></body></html>")
            return False
        return True

    def nextId(self):
        return Wizard.PageCoprFinal


class CoprFinalPage(QtWidgets.QWizardPage):

    def initializePage(self):
        self.newproject = self.base.coprusername + \
            "/" + self.base.coprpackageName
        self.webpage = "https://copr.fedoraproject.org/api/coprs/" + \
            self.newproject + "/detail"

        self.textFinalLabel.setText(
            "<html><head/><body><p align=\"left\"><span" +
            "style=\" font-size:24pt;\">" +
            "New project " + self.newproject + " was created. <br>" +
            "You can find it on website:</span></p>" +
            "<p align=\"center\"><a href=\"" + self.webpage +
            "\" font-size:24pt;\">" + self.webpage +
            "</a></p></body></html>")

    def __init__(self, Wizard, parent=None):
        super(CoprFinalPage, self).__init__(parent)

        self.base = Wizard.base
        CoprFinalPage.setFinalPage(self, True)
        self.setTitle(self.tr("    Copr final page"))
        self.setSubTitle(self.tr("Copr additional information"))

        self.textFinalLabel = QLabel()
        mainLayout = QVBoxLayout()
        gridFinalText = QGridLayout()
        gridFinalText.addWidget(self.textFinalLabel, 0, 1, 1, 1)

        mainLayout.addSpacing(190)
        mainLayout.addLayout(gridFinalText)
        mainLayout.addSpacing(190)
        self.setLayout(mainLayout)

    def validatePage(self):
        return True
