from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Error1(object):
    def setupUi(self, Error1):
        Error1.setObjectName("Error1")
        Error1.resize(500, 150)
        Error1.setMinimumSize(QtCore.QSize(500, 150))
        Error1.setMaximumSize(QtCore.QSize(500, 150))
        Error1.setBaseSize(QtCore.QSize(500, 150))
        self.pushButton = QtWidgets.QPushButton(Error1)
        self.pushButton.setGeometry(QtCore.QRect(390, 110, 94, 29))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Error1)
        self.label.setGeometry(QtCore.QRect(40, 20, 431, 21))
        self.label.setObjectName("label")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Error1)
        self.plainTextEdit.setGeometry(QtCore.QRect(40, 40, 441, 61))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(Error1)
        QtCore.QMetaObject.connectSlotsByName(Error1)

    def retranslateUi(self, Error1):
        _translate = QtCore.QCoreApplication.translate
        Error1.setWindowTitle(_translate("Error1", "Error!"))
        self.pushButton.setText(_translate("Error1", "OK"))
        self.label.setText(_translate("Error1", "An error detected in:"))

