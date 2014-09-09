from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import (QLabel, QPushButton, QPlainTextEdit,
                             QDialogButtonBox, QLineEdit, QVBoxLayout,
                             QCalendarWidget, QHBoxLayout, QFileDialog,
                             QComboBox)


class DialogChangelog(QtGui.QDialog):
    def __init__(self, Dialog, Wizard, parent=None):
        super(DialogChangelog, self).__init__(parent)

        # Reference to wizard
        self.wizard = Wizard

        # Setting dialog's size
        self.setMinimumSize(QtCore.QSize(350, 500))
        self.setMaximumSize(QtCore.QSize(850, 650))

        # Labels and QLineEdits for input
        nameLabel = QLabel("Name")
        emailLabel = QLabel("Email")
        dateLabel = QLabel("Pick a date")
        messageLabel = QLabel("Message")

        self.nameEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.messageEdit = QPlainTextEdit()
        self.datePicker = QCalendarWidget()

        # Button box with "OK" and "Cancel buttons"
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.boxButtons = QDialogButtonBox(parent=Wizard)
        self.boxButtons.addButton(self.okButton, 0)
        self.boxButtons.addButton(self.cancelButton, 1)
        self.boxButtons.accepted.connect(self.acceptIt)
        self.boxButtons.rejected.connect(self.reject)

        # Import button
        self.importCvsButton = QPushButton("Import from CVS")
        self.importCvsButton.clicked.connect(self.importFromCVS)

        # Setting layout
        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()
        upperLayout.addWidget(nameLabel)
        upperLayout.addWidget(self.importCvsButton)
        mainLayout.addLayout(upperLayout)
        mainLayout.addWidget(self.nameEdit)
        mainLayout.addWidget(emailLabel)
        mainLayout.addWidget(self.emailEdit)
        mainLayout.addWidget(dateLabel)
        mainLayout.addWidget(self.datePicker)
        mainLayout.addWidget(messageLabel)
        mainLayout.addWidget(self.messageEdit)
        mainLayout.addWidget(self.boxButtons)
        self.setLayout(mainLayout)

    def acceptIt(self):
        ''' If user clicked "OK" button '''
        self.accept()

    def importFromCVS(self):
        ''' If user clicked "Import from CVS" button '''
        pass


class DialogError(QtGui.QDialog):
    def __init__(self, Dialog, Wizard, parent=None):
        super(DialogError, self).__init__(parent)

        # Setting dialog's size
        self.setMinimumSize(QtCore.QSize(350, 150))
        self.setMaximumSize(QtCore.QSize(500, 300))

        # Setting labels and tet
        errorLabel = QLabel("Error!")
        self.errorText = QLabel("Here will be text of error message")

        # Setting button
        self.okButton = QPushButton("OK")
        boxButtons = QDialogButtonBox(parent=Wizard)
        boxButtons.addButton(self.okButton, 0)
        boxButtons.accepted.connect(self.acceptIt)

        # Setting layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(errorLabel)
        mainLayout.addWidget(self.errorText)
        mainLayout.addWidget(boxButtons)
        self.setLayout(mainLayout)

    def someError(self):
        ''' If error appeared somewhere during wizard flow '''
        pass

    def coprError(self):
        ''' If error appeared while uploading to COPR repo '''
        pass

    def acceptIt(self):
        ''' If user clicked "OK" button '''
        self.aceept()


class DialogSRPM(QtGui.QDialog):
    def __init__(self, Dialog, Wizard, parent=None):
        super(DialogSRPM, self).__init__(parent)

        # Setting
        self.setMinimumSize(QtCore.QSize(350, 150))
        self.setMaximumSize(QtCore.QSize(500, 300))

        # Setting label
        SrpmLabel = QLabel("Do you wish to edit source code?")

        # Setting buttons
        self.editButton = QPushButton("Edit")
        self.editButton.clicked.connect(self.openFileBrowser)

        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.boxButtons = QDialogButtonBox(parent=Wizard)
        self.boxButtons.addButton(self.okButton, 0)
        self.boxButtons.addButton(self.cancelButton, 1)
        self.boxButtons.accepted.connect(self.acceptIt)
        self.boxButtons.rejected.connect(self.reject)

        # Setting layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(SrpmLabel)
        mainLayout.addWidget(self.editButton)
        mainLayout.addWidget(self.boxButtons)
        self.setLayout(mainLayout)

    def openFileBrowser(self):
        ''' If user clicked "Edit" button'''
        brows = QFileDialog()
        brows.getOpenFileName(self, "/home")

    def acceptIt(self):
        ''' If user clicked "OK" button '''
        self.accept()


class DialogSubpackage(QtGui.QDialog):
    def __init__(self, Dialog, Wizard, parent=None):
        super(DialogSubpackage, self).__init__(parent)

        self.wizard = Wizard

        # Settings
        self.setMinimumSize(QtCore.QSize(350, 150))
        self.setMaximumSize(QtCore.QSize(500, 600))

        # Setting labels
        nameLabel = QLabel("Name")
        groupLabel = QLabel("Group")
        summaryLabel = QLabel("Summary")
        descriptionLabel = QLabel("Description")

        # Setting text editors
        self.nameEdit = QLineEdit()
        self.groupEdit = QComboBox()
        self.summaryEdit = QLineEdit()
        self.descriptionEdit = QPlainTextEdit()

        # Setting buttons
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.boxButtons = QDialogButtonBox(parent=Wizard)
        self.boxButtons.addButton(self.okButton, 0)
        self.boxButtons.addButton(self.cancelButton, 1)
        self.boxButtons.accepted.connect(self.acceptIt)
        self.boxButtons.rejected.connect(self.reject)

        # Setting layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(nameLabel)
        mainLayout.addWidget(self.nameEdit)
        mainLayout.addWidget(groupLabel)
        mainLayout.addWidget(self.groupEdit)
        mainLayout.addWidget(summaryLabel)
        mainLayout.addWidget(self.summaryEdit)
        mainLayout.addWidget(descriptionLabel)
        mainLayout.addWidget(self.descriptionEdit)
        mainLayout.addWidget(self.boxButtons)
        self.setLayout(mainLayout)

    def acceptIt(self):
        self.wizard.tree.addSubpackage(self.nameEdit.text())
        self.accept()

"""
class DialogImport(QtGui.QFileSystemModel):
    def __init__(self, Wizard, parent=None):
        super(DialogImport, self).__init__(parent)

        self.wizard = Wizard
        self.setRootPath(QtCore.QDir.currentPath())
        self.urls = []
        '''self.urls.append(QtCore.QUrl.
                         fromLocalFile(str(QtCore.QStandardPaths.
                                           DesktopLocation)))
        self.urls.append(QtCore.QUrl.
                         fromLocalFile(str(QtCore.QStandardPaths.
                                           DocumentsLocation)))'''
        self.mfiledialog = QtGui.QFileDialog()
        self.mfiledialog.setSidebarUrls(self.urls)
        self.mfiledialog.setFileMode(QtGui.QFileDialog.AnyFile)
        self.mfiledialog.setViewMode(QtGui.QFileDialog.Detail)
        self.mfiledialog.currentChanged.connect(self.ondialogChanged)
        self.mfiledialog.exec_()
        self.pathList = self.mfiledialog.selectedFiles()
        self.path = self.pathList[0]
        self.wizard.importEdit.setText(self.path)

    def ondialogChanged(self, filedir):
        finfo = QtCore.QFileInfo(filedir)
        if(finfo.isDir()):
            self.mfiledialog.setFileMode(QFileDialog.Directory)
        else:
            self.mfiledialog.setFileMode(QFileDialog.AnyFile)
"""

class ImportDialog(QtGui.QFileDialog):
    def __init__(self, Wizard, *args):
        self.wizard = Wizard
        QtGui.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        btns = self.findChildren(QtGui.QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QtGui.QTreeView)

    def openClicked(self):
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column() == 0:
                files.append(os.path.join(str(self.directory().absolutePath()),str(i.data().toString())))
        self.selectedFiles = files
        self.hide()

    def filesSelected(self):
        return str(self.selectedFiles()[0])