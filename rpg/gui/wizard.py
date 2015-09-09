from os.path import expanduser
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QLineEdit, QCheckBox,
                             QGroupBox, QPushButton, QGridLayout,
                             QTextEdit, QHBoxLayout, QFileDialog,
                             QComboBox, QWizard)
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
        - counted from 0 (PageIntro) to 9 (PageCoprFinal)
        - tooltips are from:
          https://fedoraproject.org/wiki/How_to_create_an_RPM_package '''

    NUM_PAGES = 11
    (PageIntro, PageImport, PageMandatory, PageScripts, PageInstall,
        PageRequires, PageUninstall, PageBuild, PageCoprLogin, PageCoprBuild,
        PageCoprFinal) = range(NUM_PAGES)

    def __init__(self, base, parent=None):
        super(Wizard, self).__init__(parent)

        self.base = base
        self.setWindowTitle(self.tr("RPG"))
        self.setWizardStyle(self.ClassicStyle)
        btnList = ([QWizard.CancelButton, QWizard.Stretch,
                    QWizard.BackButton, QWizard.NextButton,
                    QWizard.FinishButton])
        self.setButtonLayout(btnList)

        # Setting pages to wizard
        self.setPage(self.PageIntro, IntroPage(self))
        self.setPage(self.PageImport, ImportPage(self))
        self.setPage(self.PageMandatory, MandatoryPage(self))
        self.setPage(self.PageScripts, ScriptsPage(self))
        self.setPage(self.PageInstall, InstallPage(self))
        self.setPage(self.PageRequires, RequiresPage(self))
        self.setPage(self.PageUninstall, UninstallPage(self))
        self.setPage(self.PageBuild, BuildPage(self))
        self.setPage(self.PageCoprLogin, CoprLoginPage(self))
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
            "more information use tool tips (move the cursor on the label)." +
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

        self.setTitle(self.tr("    Beginning"))
        self.setSubTitle(self.tr("Choose distribution and import " +
                                 "tarball or folder with source code"))

        self.importLabel = QLabel("Source<font color=\'#FF3333\'>*</font>")
        self.importEdit = QLineEdit()
        self.importEdit.setMinimumHeight(30)
        self.importLabel.setBuddy(self.importEdit)
        self.importLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.importLabel.setToolTip(
            "Pristine source package (e.g. tarballs) and patches")
        self.importEdit.textChanged.connect(self.checkPath)
        self.importEdit.setMinimumHeight(34)

        self.importButton = QPushButton("Import")
        self.importButton.setMinimumHeight(45)
        self.importButton.setMinimumWidth(115)
        self.importButton.clicked.connect(self.importPath)

        self.ArchLabel = QLabel("Architecture<font color=\'#FF3333\'>*</font>")
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
        self.ArchLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.ArchLabel.setToolTip(
            "Choose target architecture (32 bit - i386 or 64 bit - x68_64)")

        self.DistroLabel = QLabel(
            "Distribution<font color=\'#FF3333\'>*</font>")
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
        self.DistroLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.DistroLabel.setToolTip("Choose target distribution")

        self.registerField("Source*", self.importEdit)

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.addWidget(self.importLabel, 1, 0, 1, 1)
        grid.addWidget(self.importEdit, 1, 1, 1, 6)
        grid.addWidget(self.importButton, 1, 7, 1, 1)
        grid.addWidget(self.DistroLabel, 2, 0, 1, 0)
        grid.addWidget(self.DistroEdit, 2, 1, 1, 2)
        grid.addWidget(self.ArchLabel, 3, 0, 1, 0)
        grid.addWidget(self.ArchEdit, 3, 1, 1, 2)
        mainLayout.addSpacing(25)
        mainLayout.addLayout(grid)
        self.setLayout(mainLayout)

    def checkPath(self):
        ''' Checks, if path to import is correct while typing'''
        path = Path(self.importEdit.text())
        if(path.exists()):
            self.importEdit.setStyleSheet("")
        else:
            self.importEdit.setStyleSheet("QLineEdit { border-style: solid;" +
                                          "border-width: 1px;" +
                                          "border-color: #FF3333;" +
                                          "border-radius: 3px;" +
                                          "background-color:" +
                                          "rgb(233,233,233);}")

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
            new_thread = Thread(
                target=self.base.fetch_repos, args=(self.base.target_distro,
                                                    self.base.target_arch))
            new_thread.start()
            self.importEdit.setStyleSheet("")
            return True
        else:
            self.importEdit.setStyleSheet("QLineEdit { border-style: solid;" +
                                          "border-width: 1px;" +
                                          "border-color: #FF3333;" +
                                          "border-radius: 3px;" +
                                          "background-color:" +
                                          "rgb(233,233,233);}")
            return False

    def nextId(self):
        ''' [int] Function that determines the next page after the current one
            - returns integer value and then checks, which value is page"
            in NUM_PAGES'''

        return Wizard.PageMandatory


class MandatoryPage(QtWidgets.QWizardPage):

    def __init__(self, Wizard, parent=None):
        super(MandatoryPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("    Mandatory fields"))
        self.setSubTitle(self.tr("Basic required information"))

        ''' Creating widgets and setting them to layout'''
        self.nameLabel = QLabel("Name<font color=\'#FF3333\'>*</font>")
        self.nameEdit = QLineEdit()
        self.nameEdit.setMinimumHeight(30)
        self.nameLabel.setBuddy(self.nameEdit)
        self.nameLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.nameLabel.setToolTip(
            "The (base) name of the package, " +
            "which should match the SPEC file name")

        self.versionLabel = QLabel("Version<font color=\'#FF3333\'>*</font>")
        self.versionEdit = QLineEdit()
        self.versionEdit.setMinimumHeight(30)
        self.versionLabel.setBuddy(self.versionEdit)
        self.versionLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.versionLabel.setToolTip(
            "The upstream version number, " +
            "usually numbers separated by dots (e.g. 1.7.4)")

        self.releaseLabel = QLabel("Release<font color=\'#FF3333\'>*</font>")
        self.releaseEdit = QLineEdit()
        self.releaseEdit.setMinimumHeight(30)
        self.releaseLabel.setBuddy(self.releaseEdit)
        self.releaseLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.releaseLabel.setToolTip(
            "The initial value should normally be 1%{?dist}. " +
            "Increment the number every time you release a new package")

        self.licenseLabel = QLabel("License<font color=\'#FF3333\'>*</font>")
        self.licenseEdit = QLineEdit()
        self.licenseEdit.setMinimumHeight(30)
        self.licenseLabel.setBuddy(self.licenseEdit)
        self.licenseLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.licenseLabel.setToolTip(
            "The license, which must be an open source software license")

        self.summaryLabel = QLabel("Summary<font color=\'#FF3333\'>*</font>")
        self.summaryEdit = QLineEdit()
        self.summaryEdit.setMinimumHeight(30)
        self.summaryLabel.setBuddy(self.summaryEdit)
        self.summaryLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.summaryLabel.setToolTip(
            "A brief, one-line summary of the package. Use American English")

        self.descriptionLabel = QLabel(
            "Description<font color=\'#FF3333\'>*</font> ")
        self.descriptionEdit = QLineEdit()
        self.descriptionEdit.setMinimumHeight(30)
        self.descriptionLabel.setBuddy(self.descriptionEdit)
        self.descriptionLabel.setCursor(QtGui.
                                        QCursor(QtCore.Qt.WhatsThisCursor))
        self.descriptionLabel.setToolTip(
            "A longer, multi-line description of the program")

        self.URLLabel = QLabel("URL: ")
        self.URLEdit = QLineEdit()
        self.URLEdit.setMinimumHeight(30)
        self.URLLabel.setBuddy(self.URLEdit)
        self.URLLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.URLLabel.setToolTip(
            "The full URL for more information about the " +
            "program (e.g. the project website)")

        # Making mandatory fields:
        self.registerField("Name*", self.nameEdit)
        self.registerField("Summary*", self.summaryEdit)
        self.registerField("Version*", self.versionEdit)
        self.registerField("Release*", self.releaseEdit)
        self.registerField("License*", self.licenseEdit)
        self.registerField("Description*", self.descriptionEdit)

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.addWidget(self.nameLabel, 0, 0)
        grid.addWidget(self.nameEdit, 0, 1)
        grid.addWidget(self.versionLabel, 1, 0)
        grid.addWidget(self.versionEdit, 1, 1)
        grid.addWidget(self.releaseLabel, 2, 0)
        grid.addWidget(self.releaseEdit, 2, 1)
        grid.addWidget(self.licenseLabel, 3, 0)
        grid.addWidget(self.licenseEdit, 3, 1)
        grid.addWidget(self.summaryLabel, 4, 0)
        grid.addWidget(self.summaryEdit, 4, 1)
        grid.addWidget(self.descriptionLabel, 5, 0)
        grid.addWidget(self.descriptionEdit, 5, 1)
        grid.addWidget(self.URLLabel, 6, 0)
        grid.addWidget(self.URLEdit, 6, 1)
        mainLayout.addSpacing(25)
        mainLayout.addLayout(grid)
        self.setLayout(mainLayout)

    def validatePage(self):
        ''' [Bool] Function that invokes just after pressing the next button
            {True} - user moves to next page
            {False}- user blocked on current page
            ###### Setting up RPG class references ###### '''

        self.base.spec.Name = self.nameEdit.text()
        self.base.spec.Version = self.versionEdit.text()
        self.base.spec.Release = self.releaseEdit.text()
        self.base.spec.License = self.licenseEdit.text()
        self.base.spec.URL = self.URLEdit.text()
        self.base.spec.Summary = self.summaryEdit.text()
        self.base.spec.description = self.descriptionEdit.text()
        self.base.run_extracted_source_analysis()
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
        prepareLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        prepareLabel.setToolTip(
            "Script commands to prepare the program (e.g. to uncompress it) " +
            "so that it will be ready for building.<br>Typically this is " +
            "just %autosetup; a common variation is %autosetup " +
            "-n NAME if the source file unpacks into NAME")

        buildLabel = QLabel("%build: ")
        self.buildEdit = QTextEdit()
        buildLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        buildLabel.setToolTip(
            "Script commands to build the program (e.g. to compile it) and " +
            "get it ready for installing")

        checkLabel = QLabel("%check: ")
        self.checkEdit = QTextEdit()
        checkLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        checkLabel.setToolTip("Script commands to test the program")

        buildArchLabel = QLabel("BuildArch: ")
        self.buildArchCheckbox = QCheckBox("noarch")
        buildArchLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        buildArchLabel.setToolTip(
            "If you're packaging files that are architecture-independent " +
            "(e.g. shell scripts, data files), then add BuildArch: noarch. " +
            "The architecture for the binary RPM will then be noarch")

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        gridtext = QGridLayout()
        grid.setVerticalSpacing(15)
        gridtext.addWidget(self.textLabel, 0, 0)
        grid.addWidget(prepareLabel, 1, 0, 1, 1)
        grid.addWidget(self.prepareEdit, 1, 1, 1, 1)
        grid.addWidget(buildLabel, 2, 0, 1, 1)
        grid.addWidget(self.buildEdit, 2, 1, 1, 1)
        grid.addWidget(checkLabel, 3, 0, 1, 1)
        grid.addWidget(self.checkEdit, 3, 1, 1, 1)
        grid.addWidget(buildArchLabel, 4, 0)
        grid.addWidget(self.buildArchCheckbox, 4, 1)
        mainLayout.addSpacing(25)
        mainLayout.addLayout(gridtext)
        mainLayout.addLayout(grid)
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
        pretransLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        pretransLabel.setToolTip("At the start of transaction")

        preLabel = QLabel("%pre: ")
        self.preEdit = QTextEdit()
        preLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        preLabel.setToolTip("Before a package is installed")

        installLabel = QLabel("%install: ")
        self.installEdit = QTextEdit()
        installLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        installLabel.setToolTip("Script commands to install the program")

        postLabel = QLabel("%post: ")
        self.postEdit = QTextEdit()
        postLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        postLabel.setToolTip("After a package is installed")

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        gridtext = QGridLayout()
        grid.setVerticalSpacing(15)
        gridtext.addWidget(self.textLabel, 0, 0)
        grid.addWidget(pretransLabel, 1, 0, 1, 1)
        grid.addWidget(self.pretransEdit, 1, 1, 1, 1)
        grid.addWidget(preLabel, 2, 0, 1, 1)
        grid.addWidget(self.preEdit, 2, 1, 1, 1)
        grid.addWidget(installLabel, 3, 0, 1, 1)
        grid.addWidget(self.installEdit, 3, 1, 1, 1)
        grid.addWidget(postLabel, 4, 0, 1, 1)
        grid.addWidget(self.postEdit, 4, 1, 1, 1)
        mainLayout.addSpacing(25)
        mainLayout.addLayout(gridtext)
        mainLayout.addSpacing(15)
        mainLayout.addLayout(grid)
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
        buildRequiresLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        buildRequiresLabel.setToolTip(
            "A line-separated list of packages required for building " +
            "(compiling) the program")

        self.textLabel = QLabel()
        self.textLabel.setText(
            "<html><head/><body><p><span style=\"font-size:12pt;\">" +
            "Add required packages for compilation and run. <br> " +
            "</p></body></html>")

        requiresLabel = QLabel("Requires: ")
        self.requiresEdit = QTextEdit()
        self.requiresEdit.setMaximumHeight(220)
        requiresLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        requiresLabel.setToolTip(
            "A line-separate list of packages that are required " +
            "when the program is installed")

        providesLabel = QLabel("Provides: ")
        self.providesEdit = QTextEdit()
        providesLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        providesLabel.setToolTip(
            "List virtual package names that this package provides")

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        gridtext = QGridLayout()
        grid.setVerticalSpacing(15)
        gridtext.addWidget(self.textLabel, 0, 0)
        grid.addWidget(buildRequiresLabel, 1, 0, 1, 1)
        grid.addWidget(self.bRequiresEdit, 1, 1, 1, 1)
        grid.addWidget(requiresLabel, 2, 0, 1, 1)
        grid.addWidget(self.requiresEdit, 2, 1, 1, 1)
        grid.addWidget(providesLabel, 3, 0, 1, 1)
        grid.addWidget(self.providesEdit, 3, 1, 1, 1)
        mainLayout.addSpacing(25)
        mainLayout.addLayout(gridtext)
        mainLayout.addLayout(grid)
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
        preunLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        preunLabel.setToolTip("Before a package is uninstalled")

        postunLabel = QLabel("%postun: ")
        self.postunEdit = QTextEdit()
        postunLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        postunLabel.setToolTip("After a package is uninstalled")

        posttransLabel = QLabel("%posttrans: ")
        self.posttransEdit = QTextEdit()
        posttransLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        posttransLabel.setToolTip("At the end of transaction")

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        gridtext = QGridLayout()
        grid.setVerticalSpacing(15)
        gridtext.addWidget(self.textLabel, 0, 0)
        grid.addWidget(preunLabel, 1, 0, 1, 1)
        grid.addWidget(self.preunEdit, 1, 1, 1, 1)
        grid.addWidget(postunLabel, 2, 0, 1, 1)
        grid.addWidget(self.postunEdit, 2, 1, 1, 1)
        grid.addWidget(posttransLabel, 3, 0, 1, 1)
        grid.addWidget(self.posttransEdit, 3, 1, 1, 1)
        mainLayout.addSpacing(25)
        mainLayout.addLayout(gridtext)
        mainLayout.addLayout(grid)
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
            "Edit manually the SPEC file that generates RPM package " +
            "(advanced users)")
        self.editSpecButton = QPushButton("Edit SPEC file")
        self.editSpecButton.clicked.connect(self.editSpecFile)
        self.editSpecButton.setMinimumHeight(45)
        self.editSpecButton.setMinimumWidth(180)
        self.editSpecButton.setMaximumHeight(45)
        self.editSpecButton.setMaximumWidth(180)
        layoutspecEditBox.addWidget(specWarningLabel, 1, 0)
        layoutspecEditBox.addWidget(self.editSpecButton, 1, 1)
        specEditBox.setLayout(layoutspecEditBox)

        buildPathBox.setTitle("Target build directory")
        buildPathLabel = QLabel(
            "Build packages into selected directory")
        self.buildLocationEdit = QLineEdit()
        self.buildLocationEdit.setMinimumHeight(35)
        self.buildToButton = QPushButton("Change path")
        self.buildToButton.setMinimumHeight(35)
        self.buildToButton.clicked.connect(self.openBuildPathFileDialog)
        layoutbuildPathBox.addWidget(buildPathLabel, 0, 0)
        layoutbuildPathBox.addWidget(self.buildLocationEdit, 1, 0)
        layoutbuildPathBox.addWidget(self.buildToButton, 1, 1)
        buildPathBox.setLayout(layoutbuildPathBox)

        buildSRPMLabel = QLabel(
            "Build packages containing source codes and spec files " +
            "(not compiled to any specific architecture)")
        self.textBuildSRPMLabel = QLabel()
        self.buildSRPMButton = QPushButton("Build source package")
        self.buildSRPMButton.setMinimumHeight(45)
        self.buildSRPMButton.setMinimumWidth(180)
        self.buildSRPMButton.setMaximumHeight(45)
        self.buildSRPMButton.setMaximumWidth(180)
        self.buildSRPMButton.clicked.connect(self.buildSrpm)
        layoutbuildSRPMBox.addWidget(buildSRPMLabel, 0, 0, 1, 2)
        layoutbuildSRPMBox.addWidget(self.textBuildSRPMLabel, 1, 0)
        layoutbuildSRPMBox.addWidget(self.buildSRPMButton, 1, 1)
        buildSRPMBox.setLayout(layoutbuildSRPMBox)

        buildRPMLabel = QLabel(
            "Build packages compiled for specific " +
            "distribution and architecture")
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
            "Choose architekture (32 bit - i386 or 64 bit - x68_64)")
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
        self.buildRPMButton.setMinimumHeight(45)
        self.buildRPMButton.setMinimumWidth(180)
        self.buildRPMButton.setMaximumHeight(45)
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
            "Copr API</a>.<br>Please log in and copy your information." +
            " It will be saved on config file, but nowhere else.<br>" +
            " You also need upload your package " +
            "on some public web site." +
            "</span></p></body></html>")

        self.usernameLabel = QLabel("Username<font color=\'#FF3333\'>*</font>")
        self.usernameEdit = QLineEdit()
        self.usernameEdit.setMinimumHeight(30)
        self.usernameLabel.setBuddy(self.usernameEdit)
        self.usernameLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.usernameLabel.setToolTip("Your username from Copr API")

        self.loginLabel = QLabel("Login<font color=\'#FF3333\'>*</font>")
        self.loginEdit = QLineEdit()
        self.loginEdit.setMinimumHeight(30)
        self.loginLabel.setBuddy(self.loginEdit)
        self.loginLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.loginLabel.setToolTip("Your login (not username!) from Copr API")

        self.tokenLabel = QLabel("Token<font color=\'#FF3333\'>*</font>")
        self.tokenEdit = QLineEdit()
        self.tokenEdit.setMinimumHeight(30)
        self.tokenLabel.setBuddy(self.tokenEdit)
        self.tokenLabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.tokenLabel.setToolTip("Your token from Copr API")

        self.packageNameLabel = QLabel("Name<font color=\'#FF3333\'>*</font>")
        self.packageNameEdit = QLineEdit()
        self.packageNameEdit.setMinimumHeight(30)
        self.packageNameLabel.setBuddy(self.packageNameEdit)
        self.packageNameLabel.setCursor(
            QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.packageNameLabel.setToolTip(
            "Name of your package. It MUST be unique!")

        self.packageUrlLabel = QLabel("Url<font color=\'#FF3333\'>*</font>")
        self.packageUrlEdit = QLineEdit()
        self.packageUrlEdit.setMinimumHeight(30)
        self.packageUrlLabel.setBuddy(self.packageUrlEdit)
        self.packageUrlLabel.setCursor(
            QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.packageUrlLabel.setToolTip(
            "An url of your package. It must be some public web site")

        self.Fedora22_i386_CheckBox = QCheckBox("fedora-22-i386")
        self.Fedora22_x64_CheckBox = QCheckBox("fedora-22-x86_64")
        self.Fedora21_i386_CheckBox = QCheckBox("fedora-21-i386")
        self.Fedora21_x64_CheckBox = QCheckBox("fedora-21-x86_64")
        self.Fedora20_i386_CheckBox = QCheckBox("fedora-20-i386")
        self.Fedora20_x64_CheckBox = QCheckBox("fedora-20-x86_64")
        self.Fedoraraw_i386_CheckBox = QCheckBox("fedora-rawhide-i386")
        self.Fedoraraw_x64_CheckBox = QCheckBox("fedora-rawhide-x86_64")
        self.EPEL7_x64_CheckBox = QCheckBox("epel-7-x86_64")
        self.EPEL6_x64_CheckBox = QCheckBox("epel-6-x86_64")
        self.EPEL6_i386_CheckBox = QCheckBox("epel-6-i386")
        self.EPEL5_x64_CheckBox = QCheckBox("epel-5-x86_64")
        self.EPEL5_i386_CheckBox = QCheckBox("epel-5-i386")

        # Making mandatory fields:
        self.registerField("Username*", self.usernameEdit)
        self.registerField("Login*", self.loginEdit)
        self.registerField("Token*", self.tokenEdit)
        self.registerField("PName*", self.packageNameEdit)
        self.registerField("Url*", self.packageUrlEdit)

        releaseBox = QGroupBox()
        layoutReleaseBox = QGridLayout()

        releaseBoxLabel = QLabel("Choose distribution<font color=\'#FF3333\'>*</font>")
        layoutReleaseBox.setColumnStretch(0, 1)
        layoutReleaseBox.setColumnStretch(1, 1)
        layoutReleaseBox.setColumnStretch(2, 1)
        layoutReleaseBox.setColumnStretch(3, 1)
        layoutReleaseBox.addWidget(self.EPEL7_x64_CheckBox, 0, 1)
        layoutReleaseBox.addWidget(self.EPEL6_i386_CheckBox, 1, 1)
        layoutReleaseBox.addWidget(self.EPEL6_x64_CheckBox, 2, 1)
        layoutReleaseBox.addWidget(self.EPEL5_i386_CheckBox, 3, 1)
        layoutReleaseBox.addWidget(self.EPEL5_x64_CheckBox, 4, 1)
        layoutReleaseBox.addWidget(self.Fedora22_i386_CheckBox, 0, 2)
        layoutReleaseBox.addWidget(self.Fedora22_x64_CheckBox, 1, 2)
        layoutReleaseBox.addWidget(self.Fedora21_i386_CheckBox, 2, 2)
        layoutReleaseBox.addWidget(self.Fedora21_x64_CheckBox, 3, 2)
        layoutReleaseBox.addWidget(self.Fedora20_i386_CheckBox, 4, 2)
        layoutReleaseBox.addWidget(self.Fedora20_x64_CheckBox, 5, 2)
        layoutReleaseBox.addWidget(self.Fedoraraw_i386_CheckBox, 0, 3)
        layoutReleaseBox.addWidget(self.Fedoraraw_x64_CheckBox, 1, 3)
        releaseBox.setLayout(layoutReleaseBox)

        mainLayout = QVBoxLayout()
        gridLoginText = QGridLayout()
        gridLoginText.addWidget(self.textLoginLabel, 0, 1, 1, 1)

        grid = QGridLayout()
        grid2 = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.addWidget(self.usernameLabel, 2, 0, 1, 1)
        grid.addWidget(self.usernameEdit, 2, 1, 1, 1)
        grid.addWidget(self.loginLabel, 3, 0, 1, 1)
        grid.addWidget(self.loginEdit, 3, 1, 1, 1)
        grid.addWidget(self.tokenLabel, 4, 0, 1, 1)
        grid.addWidget(self.tokenEdit, 4, 1, 1, 1)
        grid.addWidget(self.packageNameLabel, 5, 0, 1, 1)
        grid.addWidget(self.packageNameEdit, 5, 1, 1, 1)
        grid.addWidget(self.packageUrlLabel, 6, 0, 1, 1)
        grid.addWidget(self.packageUrlEdit, 6, 1, 1, 1)
        grid2.addWidget(releaseBoxLabel, 0, 0, 1, 1)

        lowerLayout = QHBoxLayout()
        lowerLayout.addWidget(releaseBox)

        mainLayout.addSpacing(25)
        mainLayout.addLayout(gridLoginText)
        mainLayout.addSpacing(15)
        mainLayout.addLayout(grid)
        mainLayout.addSpacing(15)
        mainLayout.addLayout(grid2)
        mainLayout.addLayout(lowerLayout)
        self.setLayout(mainLayout)

    def validatePage(self):
        self.base.coprusername = self.usernameEdit.text()
        self.base.coprpackageName = self.packageNameEdit.text()
        self.base.coprpackageUrl = self.packageUrlEdit.text()
        self.base.copr_set_config(self.base.coprusername,
                                  self.loginEdit.text(), self.tokenEdit.text())

        self.versionList = [
            self.Fedora22_i386_CheckBox, self.Fedora22_x64_CheckBox,
            self.Fedora21_i386_CheckBox, self.Fedora21_x64_CheckBox,
            self.Fedora20_i386_CheckBox, self.Fedora20_x64_CheckBox,
            self.Fedoraraw_i386_CheckBox, self.Fedoraraw_x64_CheckBox,
            self.EPEL7_x64_CheckBox,
            self.EPEL6_x64_CheckBox, self.EPEL6_i386_CheckBox,
            self.EPEL5_x64_CheckBox, self.EPEL5_i386_CheckBox
        ]
        self.base.coprversion = []
        for checkbox in self.versionList:
            if checkbox.isChecked():
                self.base.coprversion.append(checkbox.text())

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
        self.packageDescLabel.setCursor(
            QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.packageDescLabel.setToolTip(
            "Description for your package, optional")

        self.packageInstuctionLabel = QLabel("Instructions ")
        self.packageInstuctionEdit = QTextEdit()
        self.packageInstuctionLabel.setCursor(
            QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.packageInstuctionLabel.setToolTip(
            "How install your project, where users can report bugs " +
            "and issues. Or wiki link, optional")

        mainLayout = QVBoxLayout()
        gridBuildText = QGridLayout()
        gridBuildText.addWidget(self.textBuildLabel, 0, 1, 1, 1)

        grid = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.addWidget(self.packageDescLabel, 2, 0, 1, 1)
        grid.addWidget(self.packageDescEdit, 2, 1, 1, 1)
        grid.addWidget(self.packageInstuctionLabel, 3, 0, 1, 1)
        grid.addWidget(self.packageInstuctionEdit, 3, 1, 1, 1)

        mainLayout.addSpacing(25)
        mainLayout.addLayout(gridBuildText)
        mainLayout.addSpacing(15)
        mainLayout.addLayout(grid)
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
