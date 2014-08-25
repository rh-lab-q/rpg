from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QLineEdit, QCheckBox,
                             QGroupBox, QComboBox, QPushButton, QGridLayout,
                             QPlainTextEdit, QListWidget, QHBoxLayout,
                             QDialog, QFileDialog)
from rpg.gui.dialogs import DialogChangelog, DialogSubpackage
from rpg import Base


class Wizard(QtWidgets.QWizard):
    ''' Main class that holds other pages, number of pages are in NUM_PAGES
        - to simply navigate between them
        - counted from 0 (PageGreetings) to 10 (PageFinal)'''

    NUM_PAGES = 11
    (PageGreetings, PageImport, PageScripts, PagePatches, PageRequires,
        PageScriplets, PageSubpackages, PageDocsChangelog, PageBuild, PageCopr,
        PageFinal) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)

        self.base = Base()
        self.setWindowTitle(self.tr("RPG"))
        self.setWizardStyle(self.ClassicStyle)

        # Setting pages to wizard
        self.setPage(self.PageGreetings, GreetingsPage())
        self.setPage(self.PageImport, ImportPage(self))
        self.setPage(self.PageScripts, ScriptsPage(self))
        self.setPage(self.PagePatches, PatchesPage(self))
        self.setPage(self.PageRequires, RequiresPage(self))
        self.setPage(self.PageScriplets, ScripletsPage(self))
        self.setPage(self.PageSubpackages, SubpackagesPage(self))
        self.setPage(self.PageDocsChangelog, DocsChangelogPage(self))
        self.setPage(self.PageBuild, BuildPage(self))
        self.setPage(self.PageCopr, CoprPage(self))
        self.setPage(self.PageFinal, FinalPage(self))
        self.setStartId(self.PageGreetings)


class GreetingsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(GreetingsPage, self).__init__(parent)
        self.setTitle(self.tr("RPG"))
        self.setSubTitle(self.tr("RPM package generator"))

        greetingsLabel = QLabel("<html><head/><body><p align=\"center\">" +
                                "<span style=\" font-size:36pt;\">PRG - " +
                                "RPM Package Generator</span></p></body>" +
                                "</html><p align=\"center\">RPG is tool," +
                                " that guides people through the creation" +
                                "of a RPM package.</p><p align=\"center\">" +
                                "RPG makes packaging much easier due to" +
                                " the automatic analysis of packaged" +
                                "files.</p><p align=\"center\">" +
                                "Beginners can get familiar with" +
                                "packaging process </p><p align=\"center\">" +
                                "or the advanced users can use our tool for" +
                                "a quick creation of a package.</p>")
        grid = QVBoxLayout()
        grid.addSpacing(150)
        grid.addWidget(greetingsLabel)
        self.setLayout(grid)

    def nextId(self):
            return Wizard.PageImport


class ImportPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(ImportPage, self).__init__(parent)

        self.base = Wizard.base
        self.setTitle(self.tr("Beginning"))
        self.setSubTitle(self.tr("Fill in fields and import" +
                                 "your SRPM or source folder"))

        ''' Creating widgets and setting them to layout'''
        nameLabel = QLabel("Name: ")
        self.nameEdit = QLineEdit()
        self.nameEdit.setMinimumHeight(30)
        nameLabel.setBuddy(self.nameEdit)

        versionLabel = QLabel("Version: ")
        self.versionEdit = QLineEdit()
        self.versionEdit.setMinimumHeight(30)
        versionLabel.setBuddy(self.versionEdit)

        releaseLabel = QLabel("Release: ")
        self.releaseEdit = QLineEdit()
        self.releaseEdit.setMinimumHeight(30)
        releaseLabel.setBuddy(self.releaseEdit)

        licenseLabel = QLabel("License: ")
        self.licenseEdit = QLineEdit()
        self.licenseEdit.setMinimumHeight(30)
        licenseLabel.setBuddy(self.licenseEdit)

        URLLabel = QLabel("URL: ")
        self.URLEdit = QLineEdit()
        self.URLEdit.setMinimumHeight(30)
        URLLabel.setBuddy(self.URLEdit)

        groupLabel = QLabel("Group: ")
        self.groupEdit = QComboBox()
        self.groupEdit.addItem("First")
        self.groupEdit.addItem("Second")
        self.groupEdit.addItem("Third")
        self.groupEdit.setMinimumHeight(30)
        groupLabel.setBuddy(self.groupEdit)

        summaryLabel = QLabel("Summary: ")
        self.summaryEdit = QLineEdit()
        self.summaryEdit.setMinimumHeight(30)
        summaryLabel.setBuddy(self.summaryEdit)

        descriptionLabel = QLabel("Description: ")
        self.descriptionEdit = QLineEdit()
        self.descriptionEdit.setMinimumHeight(30)
        descriptionLabel.setBuddy(self.descriptionEdit)

        vendorLabel = QLabel("Vendor: ")
        self.vendorEdit = QLineEdit()
        self.vendorEdit.setMinimumHeight(30)
        vendorLabel.setBuddy(self.vendorEdit)

        packagerLabel = QLabel("Packager: ")
        self.packagerEdit = QLineEdit()
        self.packagerEdit.setMinimumHeight(30)
        packagerLabel.setBuddy(self.packagerEdit)

        importLabel = QLabel("Path: ")
        self.importEdit = QLineEdit()
        self.importEdit.setMinimumHeight(30)
        importLabel.setBuddy(self.importEdit)
        self.importButton = QPushButton("Import")
        self.importButton.setMinimumHeight(30)
        self.importButton.clicked.connect(self.openImportPageFileDialog)

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0, 1, 1)
        grid.addWidget(self.nameEdit, 0, 1, 1, 2)
        grid.addWidget(versionLabel, 1, 0, 1, 1)
        grid.addWidget(self.versionEdit, 1, 1, 1, 2)
        grid.addWidget(releaseLabel, 2, 0, 1, 1)
        grid.addWidget(self.releaseEdit, 2, 1, 1, 2)
        grid.addWidget(licenseLabel, 3, 0, 1, 1)
        grid.addWidget(self.licenseEdit, 3, 1, 1, 2)
        grid.addWidget(URLLabel, 4, 0, 1, 1)
        grid.addWidget(self.URLEdit, 4, 1, 1, 2)
        grid.addWidget(groupLabel, 5, 0, 1, 1)
        grid.addWidget(self.groupEdit, 5, 1, 1, 2)
        grid.addWidget(summaryLabel, 6, 0, 1, 1)
        grid.addWidget(self.summaryEdit, 6, 1, 1, 2)
        grid.addWidget(descriptionLabel, 7, 0, 1, 1)
        grid.addWidget(self.descriptionEdit, 7, 1, 1, 2)
        grid.addWidget(vendorLabel, 8, 0, 1, 1)
        grid.addWidget(self.vendorEdit, 8, 1, 1, 2)
        grid.addWidget(packagerLabel, 9, 0, 1, 1)
        grid.addWidget(self.packagerEdit, 9, 1, 1, 2)
        grid.addWidget(importLabel, 10, 0, 1, 1)
        grid.addWidget(self.importEdit, 10, 1, 1, 1)
        grid.addWidget(self.importButton, 10, 2, 1, 1)
        mainLayout.addSpacing(40)
        mainLayout.addLayout(grid)
        self.setLayout(mainLayout)

    def openImportPageFileDialog(self):
        ''' Open file browser in new dialog window'''
        brows = QFileDialog()
        #brows.setFileMode(QFileDialog.Directory)
        brows.getExistingDirectory(self, "Choose source folder or archive",
                                   "~/")

    def validatePage(self):
        ''' [Bool] Function that invokes just after pressing the next button
            {True} - user moves to next page
            {False}- user blocked on current page
            ###### Setting up RPG class references ###### '''

        self.base.spec.tags['Name'] = self.nameEdit.text()
        self.base.spec.tags['Version'] = self.versionEdit.text()
        self.base.spec.tags['Release'] = self.releaseEdit.text()
        self.base.spec.tags['License'] = self.licenseEdit.text()
        self.base.spec.tags['URL'] = self.URLEdit.text()
        self.base.spec.tags['Group'] = self.groupEdit.currentText()
        self.base.spec.tags['Summary'] = self.summaryEdit.text()
        self.base.spec.scripts['%description'] = self.descriptionEdit.text()
        self.base.spec.tags['Vendor'] = self.vendorEdit.text()
        self.base.spec.tags['Packager'] = self.packagerEdit.text()
        self.base.spec.tags['Path'] = self.importEdit.text()
        self.base.process_archive_or_dir()  # TODO add dir

        return True

    def nextId(self):
        ''' [int] Function that determines the next page after the current one
            - returns integer value and then checks, which value is page"
            in NUM_PAGES'''

        return Wizard.PageScripts


class ScriptsPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(ScriptsPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("Scripts page"))
        self.setSubTitle(self.tr("Write scripts"))

        prepareLabel = QLabel("%prepare: ")
        self.prepareEdit = QPlainTextEdit()

        buildLabel = QLabel("%build: ")
        self.buildEdit = QPlainTextEdit()

        installLabel = QLabel("%install: ")
        self.installEdit = QPlainTextEdit()

        checkLabel = QLabel("%check: ")
        self.checkEdit = QPlainTextEdit()

        grid = QGridLayout()
        grid.addWidget(prepareLabel, 0, 0)
        grid.addWidget(self.prepareEdit, 0, 1)
        grid.addWidget(buildLabel, 1, 0)
        grid.addWidget(self.buildEdit, 1, 1)
        grid.addWidget(installLabel, 2, 0)
        grid.addWidget(self.installEdit, 2, 1)
        grid.addWidget(checkLabel, 3, 0)
        grid.addWidget(self.checkEdit, 3, 1)
        self.setLayout(grid)

    def validatePage(self):
        self.base.spec.scripts['%prep'] = self.prepareEdit.toPlainText()
        self.base.spec.scripts['%build'] = self.buildEdit.toPlainText()
        self.base.spec.scripts['%install'] = self.installEdit.toPlainText()
        self.base.spec.scripts['%check'] = self.checkEdit.toPlainText()
        return True

    def nextId(self):
        self.base.spec.scripts["%build"] = self.buildEdit.text
        return Wizard.PagePatches


class PatchesPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(PatchesPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("Patches page"))
        self.setSubTitle(self.tr("Select patches"))

        self.addButton = QPushButton("+")
        self.removeButton = QPushButton("-")
        patchesLabel = QLabel("Patches")
        self.listPatches = QListWidget()
        self.addButton.setMaximumWidth(68)
        self.addButton.setMaximumHeight(60)
        self.addButton.clicked.connect(self.openPatchesPageFileDialog)
        self.removeButton.setMaximumWidth(68)
        self.removeButton.setMaximumHeight(60)

        grid = QGridLayout()
        grid.addWidget(patchesLabel, 0, 0)
        grid.addWidget(self.addButton, 0, 1,)
        grid.addWidget(self.removeButton, 0, 2)
        grid.addWidget(self.listPatches, 1, 0, 1, 0)

        self.setLayout(grid)

    def openPatchesPageFileDialog(self):
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def nextId(self):
        self.base.apply_patches()  # TODO pass list of paths (strings)
        self.base.run_pathed_sources_analysis()
        self.base.build_project()
        self.base.run_installed_files_analysis()
        return Wizard.PageRequires


class RequiresPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(RequiresPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("Requires page"))
        self.setSubTitle(self.tr("Write requires and provides"))

        buildRequiresLabel = QLabel("BuildRequires: ")
        self.bRequiresEdit = QPlainTextEdit()
        self.bRequiresEdit.setMaximumHeight(40)

        requiresLabel = QLabel("Requires: ")
        self.requiresEdit = QPlainTextEdit()
        self.requiresEdit.setMaximumHeight(40)

        preovidesLabel = QLabel("Provides: ")
        self.previdesEdit = QPlainTextEdit()

        grid = QGridLayout()
        grid.addWidget(buildRequiresLabel, 0, 0)
        grid.addWidget(self.bRequiresEdit, 1, 0)
        grid.addWidget(requiresLabel, 2, 0)
        grid.addWidget(self.requiresEdit, 3, 0,)
        grid.addWidget(preovidesLabel, 4, 0)
        grid.addWidget(self.previdesEdit, 5, 0)
        self.setLayout(grid)

    def validatePage(self):
        self.base.spec.tags["BuildRequires"] = self.bRequiresEdit.toPlainText()
        self.base.spec.tags["Requires"] = self.requiresEdit.toPlainText()
        self.base.spec.tags["Provides"] = self.previdesEdit.toPlainText()
        return True

    def nextId(self):
        return Wizard.PageScriplets


class ScripletsPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(ScripletsPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("Scriplets page"))
        self.setSubTitle(self.tr("Write scriplets"))

        pretransLabel = QLabel("%pretrans: ")
        self.pretransEdit = QPlainTextEdit()

        preLabel = QLabel("%pre: ")
        self.preEdit = QPlainTextEdit()

        postLabel = QLabel("%post: ")
        self.postEdit = QPlainTextEdit()

        postunLabel = QLabel("%postun: ")
        self.postunEdit = QPlainTextEdit()

        preunLabel = QLabel("%preun: ")
        self.preunEdit = QPlainTextEdit()

        posttransLabel = QLabel("%posttrans: ")
        self.posttransEdit = QPlainTextEdit()

        grid = QGridLayout()
        grid.addWidget(pretransLabel, 0, 0)
        grid.addWidget(self.pretransEdit, 0, 1)
        grid.addWidget(preLabel, 1, 0)
        grid.addWidget(self.preEdit, 1, 1,)
        grid.addWidget(postLabel, 2, 0)
        grid.addWidget(self.postEdit, 2, 1)
        grid.addWidget(postunLabel, 3, 0)
        grid.addWidget(self.postunEdit, 3, 1)
        grid.addWidget(preunLabel, 4, 0)
        grid.addWidget(self.preunEdit, 4, 1,)
        grid.addWidget(posttransLabel, 5, 0)
        grid.addWidget(self.posttransEdit, 5, 1)
        self.setLayout(grid)

    def validatePage(self):
        self.base.spec.scripts["%pretrans"] = self.pretransEdit.toPlainText()
        self.base.spec.scripts["%pre"] = self.preEdit.toPlainText()
        self.base.spec.scripts["%post"] = self.postEdit.toPlainText()
        self.base.spec.scripts["%postun"] = self.postunEdit.toPlainText()
        self.base.spec.scripts["%preun"] = self.preunEdit.toPlainText()
        self.base.spec.scripts["%posttrans"] = self.posttransEdit.toPlainText()
        return True

    def nextId(self):
        return Wizard.PageSubpackages


class SubpackagesPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(SubpackagesPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("Subpackages page"))
        self.setSubTitle(self.tr("Choose subpackages"))

        filesLabel = QLabel("Files")
        subpackagesLabel = QLabel("Subpackages ")

        self.addPackButton = QPushButton("+")
        self.addPackButton.setMaximumWidth(68)
        self.addPackButton.setMaximumHeight(60)
        self.addPackButton.clicked.connect(self.openSubpackageDialog)

        self.removePackButton = QPushButton("-")
        self.removePackButton.setMaximumWidth(68)
        self.removePackButton.setMaximumHeight(60)

        self.transferButton = QPushButton("->")
        self.transferButton.setMaximumWidth(120)
        self.transferButton.setMaximumHeight(20)

        self.filesListWidget = QListWidget()
        self.subpackagesListWidget = QListWidget()

        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        lowerLayout = QHBoxLayout()
        upperLayout.addSpacing(150)
        upperLayout.addWidget(filesLabel)
        upperLayout.addSpacing(190)
        upperLayout.addWidget(subpackagesLabel)
        upperLayout.addWidget(self.addPackButton)
        upperLayout.addWidget(self.removePackButton)
        lowerLayout.addWidget(self.filesListWidget)
        lowerLayout.addWidget(self.transferButton)
        lowerLayout.addWidget(self.subpackagesListWidget)
        mainLayout.addLayout(upperLayout)
        mainLayout.addLayout(lowerLayout)
        self.setLayout(mainLayout)

    def openSubpackageDialog(self):
        subpackageWindow = QDialog()
        subpackage = DialogSubpackage(subpackageWindow, self)
        subpackage.exec_()

    def nextId(self):
        return Wizard.PageDocsChangelog


class DocsChangelogPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(DocsChangelogPage, self).__init__(parent)

        self.base = Wizard.base
        self.setTitle(self.tr("Document files page"))
        self.setSubTitle(self.tr("Add documentation files"))

        documentationFilesLabel = QLabel("Documentation files ")
        self.addDocumentationButton = QPushButton("+")
        self.addDocumentationButton.clicked.connect(self.openDocsFileDialog)
        self.removeDocumentationButton = QPushButton("-")
        self.openChangelogDialogButton = QPushButton("Changelog")
        self.openChangelogDialogButton.clicked.connect(
            self.openChangeLogDialog)
        self.documentationFilesList = QListWidget()

        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        midleLayout = QHBoxLayout()
        lowerLayout = QHBoxLayout()
        upperLayout.addWidget(self.addDocumentationButton)
        upperLayout.addWidget(self.removeDocumentationButton)
        upperLayout.addWidget(documentationFilesLabel)
        upperLayout.addSpacing(500)
        midleLayout.addWidget(self.documentationFilesList)
        lowerLayout.addWidget(self.openChangelogDialogButton)
        lowerLayout.addSpacing(700)
        mainLayout.addLayout(upperLayout)
        mainLayout.addLayout(midleLayout)
        mainLayout.addLayout(lowerLayout)
        self.setLayout(mainLayout)

    def openChangeLogDialog(self):
        changelogWindow = QDialog()
        changelog = DialogChangelog(changelogWindow, self)
        changelog.exec_()

    def openDocsFileDialog(self):
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def nextId(self):
        return Wizard.PageBuild


class BuildPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(BuildPage, self).__init__(parent)

        self.base = Wizard.base

        self.Wizard = Wizard  # Main wizard of program
        self.nextPageIsFinal = True  # BOOL to determine which page is next one
        self.setTitle(self.tr("Build page"))
        self.setSubTitle(self.tr("Options to build"))

        self.x86_CheckBox = QCheckBox("x86")
        self.x64_CheckBox = QCheckBox("x64")
        self.Fedora20_CheckBox = QCheckBox("Fedora 20")
        self.Fedora19_CheckBox = QCheckBox("Fedora 19")
        self.Fedora18_CheckBox = QCheckBox("Fedora 18")
        self.Fedora17_CheckBox = QCheckBox("Fedora 17")
        self.Fedora16_CheckBox = QCheckBox("Fedora 16")
        self.RHEL3_CheckBox = QCheckBox("RHEL 3")
        self.RHEL4_CheckBox = QCheckBox("RHEL 4")
        self.RHEL5_CheckBox = QCheckBox("RHEL 5")
        self.RHEL6_CheckBox = QCheckBox("RHEL 6")
        self.RHEL7_CheckBox = QCheckBox("RHEL 7")

        self.buildToButton = QPushButton("Build to")
        self.buildToButton.clicked.connect(self.openBuildPathFileDialog)
        self.uploadToCOPR_Button = QPushButton("Upload to COPR")
        self.editSpecButton = QPushButton("Edit SPEC file")
        self.uploadToCOPR_Button.clicked.connect(self.switchToCOPR)
        self.uploadToCOPR_Button.clicked.connect(self.Wizard.next)
        specWarningLabel = QLabel("* Edit SPEC file on your own risk")
        self.buildLocationEdit = QLineEdit()

        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        upper2Layout = QHBoxLayout()
        midleLayout = QHBoxLayout()
        lowerLayout = QHBoxLayout()
        releaseBox = QGroupBox()
        archBox = QGroupBox()
        layoutReleaseBox = QGridLayout()
        layoutArchBox = QGridLayout()

        releaseBox.setTitle('Choose distribution')
        layoutReleaseBox.setColumnStretch(0, 1)
        layoutReleaseBox.setColumnStretch(1, 1)
        layoutReleaseBox.setColumnStretch(2, 1)
        layoutReleaseBox.setColumnStretch(3, 1)
        layoutReleaseBox.setColumnStretch(4, 1)
        layoutReleaseBox.addWidget(self.Fedora20_CheckBox, 0, 1)
        layoutReleaseBox.addWidget(self.Fedora19_CheckBox, 1, 1)
        layoutReleaseBox.addWidget(self.Fedora18_CheckBox, 2, 1)
        layoutReleaseBox.addWidget(self.Fedora17_CheckBox, 3, 1)
        layoutReleaseBox.addWidget(self.Fedora16_CheckBox, 4, 1)
        layoutReleaseBox.addWidget(self.RHEL7_CheckBox, 0, 3)
        layoutReleaseBox.addWidget(self.RHEL6_CheckBox, 1, 3)
        layoutReleaseBox.addWidget(self.RHEL5_CheckBox, 2, 3)
        layoutReleaseBox.addWidget(self.RHEL4_CheckBox, 3, 3)
        layoutReleaseBox.addWidget(self.RHEL3_CheckBox, 4, 3)
        releaseBox.setLayout(layoutReleaseBox)

        archBox.setTitle('Choose architecture')
        layoutArchBox.setColumnStretch(0, 1)
        layoutArchBox.setColumnStretch(1, 1)
        layoutArchBox.setColumnStretch(2, 1)
        layoutArchBox.setColumnStretch(3, 1)
        layoutArchBox.setColumnStretch(4, 1)
        layoutArchBox.addWidget(self.x64_CheckBox, 0, 1)
        layoutArchBox.addWidget(self.x86_CheckBox, 0, 3)
        archBox.setLayout(layoutArchBox)

        upperLayout.addWidget(releaseBox)
        upper2Layout.addWidget(archBox)
        midleLayout.addWidget(self.editSpecButton)
        midleLayout.addWidget(specWarningLabel)
        midleLayout.addSpacing(330)
        midleLayout.addWidget(self.uploadToCOPR_Button)
        lowerLayout.addWidget(self.buildToButton)
        lowerLayout.addWidget(self.buildLocationEdit)
        mainLayout.addSpacing(30)
        mainLayout.addLayout(upperLayout)
        mainLayout.addSpacing(40)
        mainLayout.addLayout(upper2Layout)
        mainLayout.addSpacing(60)
        mainLayout.addLayout(midleLayout)
        mainLayout.addSpacing(10)
        mainLayout.addLayout(lowerLayout)
        self.setLayout(mainLayout)

    def validatePage(self):
        print(" ---- Tags: ---- ")
        print(self.base.spec.tags)
        print("\n ----- Scripts: ----- ")
        print(self.base.spec.scripts)
        return True

    def switchToCOPR(self):
        '''If user clicked uplodad to copr button, so next page is not final'''
        self.nextPageIsFinal = False

    def openBuildPathFileDialog(self):
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def nextId(self):
        if (self.nextPageIsFinal):
            self.base.build_packages()
            return Wizard.PageFinal
        else:
            self.nextPageIsFinal = True
            return Wizard.PageCopr


class CoprPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(CoprPage, self).__init__(parent)

        self.base = Wizard.base

        self.setTitle(self.tr("Copr page"))
        self.setSubTitle(self.tr("COPR repository setting and uploading"))

        COPRLabel = QLabel("<html><head/><body><p align=\"center\">You are" +
                           " going to upload your package to COPR." +
                           "</p><p align=\"center\">Copr is designed to be" +
                           " a lightweight buildsystem that allows " +
                           "</p><p align=\"center\">contributors to create" +
                           " packages, put them in repositories, </p>" +
                           "<p align=\"center\">and make it easy for" +
                           " users toinstall the packages </p>" +
                           "<p align=\"center\">onto their system." +
                           " Within the Fedora Project it </p>" +
                           "<p align=\"center\">is used toallow" +
                           "packagers to create third party repositories." +
                           "</p><p align=\"center\"><br/>For more " +
                           "information,please visit <a href=\"" +
                           "https://copr.fedoraproject.org/\"><span style=\"" +
                           " text-decoration: underline;color:#0000ff;\">" +
                           "https://copr.fedoraproject.org/</span></a></p>" +
                           "</body></html>")

        self.createCOPRButton = QPushButton("Create COPR repository")
        self.chooseCONFButton = QPushButton("Choose .conf file")
        self.chooseCONFButton.clicked.connect(self.openChooseCONFFileDialog)
        releaserLabel = QLabel("Releaser: ")
        self.releaserEdit = QLineEdit()
        projectNameLabel = QLabel("Project name: ")
        self.projectNameEdit = QLineEdit()
        uploadCommandLabel = QLabel("Upload command: ")
        self.uploadCommandEdit = QLineEdit()
        remoteLocationLabel = QLabel("Remote location: ")
        self.remoteLocationEdit = QLineEdit()

        self.releaserEdit.setMinimumHeight(30)
        releaserLabel.setBuddy(self.releaserEdit)

        self.projectNameEdit.setMinimumHeight(30)
        projectNameLabel.setBuddy(self.projectNameEdit)

        self.uploadCommandEdit.setMinimumHeight(30)
        uploadCommandLabel.setBuddy(self.uploadCommandEdit)

        self.remoteLocationEdit.setMinimumHeight(30)
        remoteLocationLabel.setBuddy(self.remoteLocationEdit)

        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        midleLayout = QHBoxLayout()
        lowerLayout = QGridLayout()
        upperLayout.addWidget(COPRLabel)
        midleLayout.addSpacing(170)
        midleLayout.addWidget(self.createCOPRButton)
        midleLayout.addSpacing(50)
        midleLayout.addWidget(self.chooseCONFButton)
        midleLayout.addSpacing(170)
        lowerLayout.addWidget(releaserLabel, 0, 0)
        lowerLayout.addWidget(self.releaserEdit, 0, 1)
        lowerLayout.addWidget(projectNameLabel)
        lowerLayout.addWidget(self.projectNameEdit)
        lowerLayout.addWidget(uploadCommandLabel)
        lowerLayout.addWidget(self.uploadCommandEdit)
        lowerLayout.addWidget(remoteLocationLabel)
        lowerLayout.addWidget(self.remoteLocationEdit)
        mainLayout.addLayout(upperLayout)
        mainLayout.addSpacing(30)
        mainLayout.addLayout(midleLayout)
        mainLayout.addSpacing(30)
        mainLayout.addLayout(lowerLayout)
        self.setLayout(mainLayout)

    def openChooseCONFFileDialog(self):
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def nextId(self):
        return Wizard.PageFinal


class FinalPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(FinalPage, self).__init__(parent)

        self.base = Wizard.base
        ''' On this page will be "Finish button" instead of "Next" '''
        FinalPage.setFinalPage(self, True)

        self.setTitle(self.tr("Final page"))
        self.setSubTitle(self.tr("Your package was successfully created"))
        finalLabel = QLabel("<html><head/><body><p align=\"center\"><span" +
                            "style=\" font-size:24pt;\">Thank you for " +
                            "using RPG!</span></p><p align=\"center\">" +
                            "<span style=\" font-size:24pt;\">Your" +
                            " package was built in:</span></p></body></html>")
        self.finalEdit = QLineEdit()
        grid = QGridLayout()
        grid.addWidget(finalLabel, 0, 0)
        grid.addWidget(self.finalEdit, 1, 0)

        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(190)
        mainLayout.addWidget(finalLabel)
        mainLayout.addSpacing(190)
        mainLayout.addWidget(self.finalEdit)
        mainLayout.addSpacing(190)

        self.setLayout(mainLayout)
