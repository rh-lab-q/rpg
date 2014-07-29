from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QLineEdit, QCheckBox, QGroupBox,
    QComboBox, QPushButton, QGridLayout, QPlainTextEdit, QListWidget, QHBoxLayout)
from src.gui.changelog_dialog import Ui_ChangeLog  
from src.rpg import Rpg

class Wizard(QtWidgets.QWizard):
    ''' Main class that holds other pages, number of pages are in NUM_PAGES 
        - to simply navigate between them
        - counted from 0 (PageGreetings) to 10 (PageFinal)'''

    NUM_PAGES = 11
    (PageGreetings, PageImport, PageScripts, PagePatches, PageRequires, PageScriplets, PageSubpackages,
        PageDocsChangelog, PageBuild, PageCopr, PageFinal) = range(NUM_PAGES)
 
    def __init__(self, parent=None):
        super(Wizard, self).__init__(parent)
        ''' Initialization of class - setting up pages and the look of wizard itself'''

        self.setWindowTitle(self.tr("RPG"))
        self.setWizardStyle(self.ClassicStyle)
        
        # Setting pages to wizard
        self.setPage(self.PageGreetings, GreetingsPage(self))
        self.setPage(self.PageImport, ImportPage())
        self.setPage(self.PageScripts, ScriptsPage())
        self.setPage(self.PagePatches, PatchesPage())
        self.setPage(self.PageRequires, RequiresPage())
        self.setPage(self.PageScriplets, ScripletsPage())
        self.setPage(self.PageSubpackages, SubpackagesPage())
        self.setPage(self.PageDocsChangelog, DocsChangelogPage())
        self.setPage(self.PageBuild, BuildPage(self))
        self.setPage(self.PageCopr, CoprPage())
        self.setPage(self.PageFinal, FinalPage())
        self.setStartId(self.PageGreetings)

class GreetingsPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(GreetingsPage, self).__init__(parent)
        self.Wizard = Wizard
        self.setTitle(self.tr("RPG"))
        self.setSubTitle(self.tr("RPM package generator"))

        self.greetingsLabel = QLabel("<html><head/><body><p align=\"center\">" + 
                                     "<span style=\" font-size:36pt;\">PRG - RPM Package Generator</span></p></body></html>"+
                                     "<p align=\"center\">RPG is tool, that guides people through the creation of a RPM package.</p>"+ 
                                     "<p align=\"center\">RPG makes packaging much easier due to the automatic analysis of packaged files.</p>"+ 
                                     "<p align=\"center\">Beginners can get familiar with packaging process </p>"+ 
                                     "<p align=\"center\">or the advanced users can use our tool for a quick creation of a package.</p>")
        grid = QVBoxLayout()
        grid.addSpacing(150)
        grid.addWidget(self.greetingsLabel)
        self.setLayout(grid)

    def nextId(self):
            return Wizard.PageImport
 
class ImportPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ImportPage, self).__init__(parent)

        self.setTitle(self.tr("Beginning"))
        self.setSubTitle(self.tr("Fill in fields and import your SRPM or source folder"))

        ''' Creating widgets and setting them to layout'''
        self.nameLabel = QLabel("Name: ")
        self.nameEdit = QLineEdit()
        self.nameEdit.setMinimumHeight(30)
        self.nameLabel.setBuddy(self.nameEdit)

        self.versionLabel = QLabel("Version: ")
        self.versionEdit = QLineEdit()
        self.versionEdit.setMinimumHeight(30)
        self.versionLabel.setBuddy(self.versionEdit)

        self.releaseLabel = QLabel("Release: ")
        self.releaseEdit = QLineEdit()
        self.releaseEdit.setMinimumHeight(30)
        self.releaseLabel.setBuddy(self.releaseEdit)

        self.licenseLabel = QLabel("License: ")
        self.licenseEdit = QLineEdit()
        self.licenseEdit.setMinimumHeight(30)
        self.licenseLabel.setBuddy(self.licenseEdit)

        self.URLLabel = QLabel("URL: ")
        self.URLEdit = QLineEdit()
        self.URLEdit.setMinimumHeight(30)
        self.URLLabel.setBuddy(self.URLEdit)

        self.groupLabel = QLabel("Group: ")
        self.groupEdit = QComboBox()
        self.groupEdit.addItem("First")
        self.groupEdit.addItem("Second")
        self.groupEdit.addItem("Third")
        self.groupEdit.setMinimumHeight(30)
        self.groupLabel.setBuddy(self.groupEdit)

        self.summaryLabel = QLabel("Summary: ")
        self.summaryEdit = QLineEdit()
        self.summaryEdit.setMinimumHeight(30)
        self.summaryLabel.setBuddy(self.summaryEdit)

        self.descriptionLabel = QLabel("Description: ")
        self.descriptionEdit = QLineEdit()
        self.descriptionEdit.setMinimumHeight(30)
        self.descriptionLabel.setBuddy(self.descriptionEdit)

        self.vendorLabel = QLabel("Vendor: ")
        self.vendorEdit = QLineEdit()
        self.vendorEdit.setMinimumHeight(30)
        self.vendorLabel.setBuddy(self.vendorEdit)

        self.packagerLabel = QLabel("Packager: ")
        self.packagerEdit = QLineEdit()
        self.packagerEdit.setMinimumHeight(30)
        self.packagerLabel.setBuddy(self.packagerEdit)

        self.importLabel = QLabel("Path: ")
        self.importEdit = QLineEdit()
        self.importEdit.setMinimumHeight(30)
        self.importLabel.setBuddy(self.importEdit)
        self.importButton = QPushButton("Import")
        self.importButton.setMinimumHeight(30)
        self.importButton.clicked.connect(self.openImportPageFileDialog)

        mainLayout = QVBoxLayout()
        grid = QGridLayout()
        grid.addWidget(self.nameLabel, 0, 0, 1, 1)
        grid.addWidget(self.nameEdit, 0, 1, 1, 2)
        grid.addWidget(self.versionLabel, 1, 0, 1, 1)
        grid.addWidget(self.versionEdit, 1, 1, 1, 2)
        grid.addWidget(self.releaseLabel, 2, 0, 1, 1)
        grid.addWidget(self.releaseEdit, 2, 1, 1, 2)
        grid.addWidget(self.licenseLabel, 3, 0, 1, 1)
        grid.addWidget(self.licenseEdit, 3, 1, 1, 2)
        grid.addWidget(self.URLLabel, 4, 0, 1, 1)
        grid.addWidget(self.URLEdit, 4, 1, 1, 2)
        grid.addWidget(self.groupLabel, 5, 0, 1, 1)
        grid.addWidget(self.groupEdit, 5, 1, 1, 2)
        grid.addWidget(self.summaryLabel, 6, 0, 1, 1)
        grid.addWidget(self.summaryEdit, 6, 1, 1, 2)
        grid.addWidget(self.descriptionLabel, 7, 0, 1, 1)
        grid.addWidget(self.descriptionEdit, 7, 1, 1, 2)
        grid.addWidget(self.vendorLabel, 8, 0, 1, 1)
        grid.addWidget(self.vendorEdit, 8, 1, 1, 2)
        grid.addWidget(self.packagerLabel, 9, 0, 1, 1)
        grid.addWidget(self.packagerEdit, 9, 1, 1, 2)
        grid.addWidget(self.importLabel, 10, 0, 1, 1)
        grid.addWidget(self.importEdit, 10, 1, 1, 1)
        grid.addWidget(self.importButton, 10, 2, 1, 1)
        mainLayout.addSpacing(40)
        mainLayout.addLayout(grid)
        self.setLayout(mainLayout)

    def openImportPageFileDialog(self):
        ''' Open file browser in new dialog window'''
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def validatePage(self):
        ''' [Bool] Function that invokes just after pressing the next button
            {True} - user moves to next page
            {False}- user blocked on current page
            ###### Setting up RPG class references ###### '''

        Rpg.license = self.licenseEdit.text()
        Rpg.url = self.URLEdit.text()
        Rpg.vendor = self.vendorEdit.text()
        Rpg.packager = self.packagerEdit.text()

        return True

    def nextId(self):
        ''' [int] Function that determines the next page after the current one
            - returns integer value and then checks, which value is page in NUM_PAGES'''

        return Wizard.PageScripts

class ScriptsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ScriptsPage, self).__init__(parent)
 
        self.setTitle(self.tr("Scripts page"))
        self.setSubTitle(self.tr("Please write something here"))

        self.prepareLabel = QLabel("%prepare: ")
        self.prepareEdit = QPlainTextEdit()

        self.configLabel = QLabel("%config: ")
        self.configEdit = QPlainTextEdit()

        self.buildLabel = QLabel("%build: ")
        self.buildEdit = QPlainTextEdit()

        self.installLabel = QLabel("%install: ")
        self.installEdit = QPlainTextEdit()

        self.checkLabel = QLabel("%check: ")
        self.checkEdit = QPlainTextEdit()

        grid = QGridLayout()
        grid.addWidget(self.prepareLabel, 0, 0)
        grid.addWidget(self.prepareEdit, 0, 1)
        grid.addWidget(self.configLabel, 1, 0)
        grid.addWidget(self.configEdit, 1, 1)
        grid.addWidget(self.buildLabel, 2, 0)
        grid.addWidget(self.buildEdit, 2, 1)
        grid.addWidget(self.installLabel, 3, 0)
        grid.addWidget(self.installEdit, 3, 1)
        grid.addWidget(self.checkLabel, 4, 0)
        grid.addWidget(self.checkEdit, 4, 1)
        self.setLayout(grid)

    def validatePage(self):
        ''' ###### Setting up RPG class references ###### '''
        return True
 
    def nextId(self):
        return Wizard.PagePatches
 
class PatchesPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(PatchesPage, self).__init__(parent)
 
        self.setTitle(self.tr("Patches page"))
        self.setSubTitle(self.tr("Please write something here"))
        
        self.addButton = QPushButton("+")
        self.removeButton = QPushButton("-")
        self.patchesLabel = QLabel("Patches")
        self.listPatches = QListWidget()
        self.addButton.setMaximumWidth(68)
        self.addButton.setMaximumHeight(60)
        self.addButton.clicked.connect(self.openPatchesPageFileDialog)
        self.removeButton.setMaximumWidth(68)
        self.removeButton.setMaximumHeight(60)

        grid = QGridLayout()
        grid.addWidget(self.patchesLabel, 0, 0)
        grid.addWidget(self.addButton, 0, 1,)
        grid.addWidget(self.removeButton, 0, 2)
        grid.addWidget(self.listPatches, 1, 0, 1, 0)

        self.setLayout(grid)

    def openPatchesPageFileDialog(self):
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def nextId(self):
        return Wizard.PageRequires
 
class RequiresPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(RequiresPage, self).__init__(parent)
 
        self.setTitle(self.tr("Requires page"))
        self.setSubTitle(self.tr("Please write something here"))

        self.buildRequiresLabel = QLabel("BuildRequires: ")
        self.buildRequiresEdit = QPlainTextEdit()
        self.buildRequiresEdit.setMaximumHeight(40)

        self.requiresLabel = QLabel("Requires: ")
        self.requiresEdit = QPlainTextEdit()
        self.requiresEdit.setMaximumHeight(40)

        self.preovidesLabel = QLabel("Provides: ")
        self.previdesEdit = QPlainTextEdit()

        grid = QGridLayout()
        grid.addWidget(self.buildRequiresLabel, 0, 0)
        grid.addWidget(self.buildRequiresEdit, 1, 0)
        grid.addWidget(self.requiresLabel, 2, 0)
        grid.addWidget(self.requiresEdit, 3, 0,)
        grid.addWidget(self.preovidesLabel, 4, 0)
        grid.addWidget(self.previdesEdit, 5, 0)
        self.setLayout(grid)
    
    def nextId(self):
        return Wizard.PageScriplets

class ScripletsPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(ScripletsPage, self).__init__(parent)
 
        self.setTitle(self.tr("Scriplets page"))
        self.setSubTitle(self.tr("Please write something here"))
        
        self.pretransLabel = QLabel("%pretrans: ")
        self.pretransEdit = QPlainTextEdit()
        
        self.preLabel = QLabel("%pre: ")
        self.preEdit = QPlainTextEdit()
        
        self.postLabel = QLabel("%post: ")
        self.postEdit = QPlainTextEdit()
        
        self.postunLabel = QLabel("%postun: ")
        self.postunEdit = QPlainTextEdit()
        
        self.preunLabel = QLabel("%preun: ")
        self.preunEdit = QPlainTextEdit()
        
        self.posttransLabel = QLabel("%posttrans: ")
        self.posttransEdit = QPlainTextEdit()

        grid = QGridLayout()
        grid.addWidget(self.pretransLabel, 0, 0)
        grid.addWidget(self.pretransEdit, 0, 1)
        grid.addWidget(self.preLabel, 1, 0)
        grid.addWidget(self.preEdit, 1, 1,)
        grid.addWidget(self.postLabel, 2, 0)
        grid.addWidget(self.postEdit, 2, 1)
        grid.addWidget(self.postunLabel, 3, 0)
        grid.addWidget(self.postunEdit, 3, 1)
        grid.addWidget(self.preunLabel, 4, 0)
        grid.addWidget(self.preunEdit, 4, 1,)
        grid.addWidget(self.posttransLabel, 5, 0)
        grid.addWidget(self.posttransEdit, 5, 1)
        self.setLayout(grid)

    def nextId(self):
        return Wizard.PageSubpackages

class SubpackagesPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(SubpackagesPage, self).__init__(parent)
 
        self.setTitle(self.tr("Subpackages page"))
        self.setSubTitle(self.tr("Please write something here"))
        self.filesLabel = QLabel("Files")
        self.subpackagesLabel = QLabel("Subpackages ")
        self.addPackButton = QPushButton("+")
        self.removePackButton = QPushButton("-")
        self.removePackButton.setMaximumWidth(68)
        self.removePackButton.setMaximumHeight(60)
        self.addPackButton.setMaximumWidth(68)
        self.addPackButton.setMaximumHeight(60)
        self.transferButton = QPushButton("->")
        self.transferButton.setMaximumWidth(120)
        self.transferButton.setMaximumHeight(20)
        self.filesListWidget = QListWidget()
        self.subpackagesListWidget = QListWidget()
        
        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        lowerLayout = QHBoxLayout()
        upperLayout.addSpacing(150)
        upperLayout.addWidget(self.filesLabel)
        upperLayout.addSpacing(190)
        upperLayout.addWidget(self.subpackagesLabel)
        upperLayout.addWidget(self.addPackButton)
        upperLayout.addWidget(self.removePackButton)
        lowerLayout.addWidget(self.filesListWidget)
        lowerLayout.addWidget(self.transferButton)
        lowerLayout.addWidget(self.subpackagesListWidget)
        mainLayout.addLayout(upperLayout)
        mainLayout.addLayout(lowerLayout)
        self.setLayout(mainLayout)
        
    def nextId(self):
        return Wizard.PageDocsChangelog

class DocsChangelogPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(DocsChangelogPage, self).__init__(parent)
 
        self.setTitle(self.tr("Document files page"))
        self.setSubTitle(self.tr("Please write something here"))

        self.documentationFilesLabel = QLabel("Documentation files ")
        self.addDocumentationButton = QPushButton("+")
        self.addDocumentationButton.clicked.connect(self.openAddDocumentationFileDialog)
        self.removeDocumentationButton = QPushButton("-")
        self.openChangelogDialogButton = QPushButton("Changelog")
        self.openChangelogDialogButton.clicked.connect(self.openChangeLogDialog)
        self.documentationFilesList = QListWidget()

        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        midleLayout = QHBoxLayout()
        lowerLayout = QHBoxLayout()
        upperLayout.addWidget(self.addDocumentationButton)
        upperLayout.addWidget(self.removeDocumentationButton)
        upperLayout.addWidget(self.documentationFilesLabel)
        upperLayout.addSpacing(500)
        midleLayout.addWidget(self.documentationFilesList)
        lowerLayout.addWidget(self.openChangelogDialogButton)
        lowerLayout.addSpacing(700)
        mainLayout.addLayout(upperLayout)
        mainLayout.addLayout(midleLayout)
        mainLayout.addLayout(lowerLayout)
        self.setLayout(mainLayout)

    def openChangeLogDialog(self):
        changelog_window = QDialog()
        changelog_ui = Ui_ChangeLog()
        changelog_ui.setupUi(changelog_window)
        changelog_window.exec_()

    def openAddDocumentationFileDialog(self):
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def nextId(self):
        return Wizard.PageBuild

class BuildPage(QtWidgets.QWizardPage):
    def __init__(self, Wizard, parent=None):
        super(BuildPage, self).__init__(parent)
        
        self.Wizard = Wizard # Main wizard of program
        self.nextPageIsFinal = True # BOOL to determine which page is next one
        self.setTitle(self.tr("Build page"))
        self.setSubTitle(self.tr("Please write something here"))

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
        self.specWarningLabel = QLabel("* Edit SPEC file on your own risk")
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
        midleLayout.addWidget(self.specWarningLabel)
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

    def switchToCOPR(self):
        # If user clicked uplodad to copr button, so next page is not final

        self.nextPageIsFinal = False

    def openBuildPathFileDialog(self):
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def nextId(self):
        if (self.nextPageIsFinal):
            return Wizard.PageFinal
        else:
            self.nextPageIsFinal = True
            return Wizard.PageCopr

class CoprPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(CoprPage, self).__init__(parent)
 
        self.setTitle(self.tr("Copr page"))
        self.setSubTitle(self.tr("Please write something here"))

        self.COPRLabel = QLabel("<html><head/><body><p align=\"center\">You are going to upload your package to COPR."+
                                "</p><p align=\"center\">Copr is designed to be a lightweight buildsystem that allows "+
                                "</p><p align=\"center\">contributors to create packages, put them in repositories, </p>"+
                                "<p align=\"center\">and make it easy for users toinstall the packages </p><p align=\"center\">"+
                                "onto their system. Within the Fedora Project it </p><p align=\"center\">is used toallow"+
                                "packagers to create third party repositories.</p><p align=\"center\"><br/>For more information,"+
                                "please visit <a href=\"https://copr.fedoraproject.org/\"><span style=\" text-decoration: underline;"+
                                "color:#0000ff;\">https://copr.fedoraproject.org/</span></a></p></body></html>")

        self.createCOPRButton = QPushButton("Create COPR repository")
        self.chooseCONFButton = QPushButton("Choose .conf file")
        self.chooseCONFButton.clicked.connect(self.openChooseCONFFileDialog)
        self.releaserLabel = QLabel("Releaser: ")
        self.releaserEdit = QLineEdit()
        self.projectNameLabel = QLabel("Project name: ")
        self.projectNameEdit = QLineEdit()
        self.uploadCommandLabel = QLabel("Upload command: ")
        self.uploadCommandEdit = QLineEdit()
        self.remoteLocationLabel = QLabel("Remote location: ")
        self.remoteLocationEdit = QLineEdit()

        self.releaserEdit.setMinimumHeight(30)
        self.releaserLabel.setBuddy(self.releaserEdit)

        self.projectNameEdit.setMinimumHeight(30)
        self.projectNameLabel.setBuddy(self.projectNameEdit)

        self.uploadCommandEdit.setMinimumHeight(30)
        self.uploadCommandLabel.setBuddy(self.uploadCommandEdit)

        self.remoteLocationEdit.setMinimumHeight(30)
        self.remoteLocationLabel.setBuddy(self.remoteLocationEdit)

        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        midleLayout = QHBoxLayout()
        lowerLayout = QGridLayout()
        upperLayout.addWidget(self.COPRLabel)
        midleLayout.addSpacing(170)
        midleLayout.addWidget(self.createCOPRButton)
        midleLayout.addSpacing(50)
        midleLayout.addWidget(self.chooseCONFButton)
        midleLayout.addSpacing(170)
        lowerLayout.addWidget(self.releaserLabel, 0, 0)
        lowerLayout.addWidget(self.releaserEdit, 0, 1)
        lowerLayout.addWidget(self.projectNameLabel)
        lowerLayout.addWidget(self.projectNameEdit)
        lowerLayout.addWidget(self.uploadCommandLabel)
        lowerLayout.addWidget(self.uploadCommandEdit)
        lowerLayout.addWidget(self.remoteLocationLabel)
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
    def __init__(self, parent=None):
        super(FinalPage, self).__init__(parent)
 
        self.setTitle(self.tr("Final page"))
        self.setSubTitle(self.tr("Please write something here"))
        self.finalLabel = QLabel("<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">" +
                                 "Thank you for using RPG!</span></p><p align=\"center\">" +
                                 "<span style=\" font-size:24pt;\">Your package was built in:</span></p></body></html>")
        self.finalEdit = QLineEdit()
        grid = QGridLayout()
        grid.addWidget(self.finalLabel, 0, 0)
        grid.addWidget(self.finalEdit, 1, 0)

        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(190)
        mainLayout.addWidget(self.finalLabel)
        mainLayout.addSpacing(190)
        mainLayout.addWidget(self.finalEdit)
        mainLayout.addSpacing(190)

        self.setLayout(mainLayout)
