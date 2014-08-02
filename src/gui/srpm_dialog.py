from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_srpmModal(object):
    def setupUi(self, srpmModal):
        srpmModal.setObjectName("srpmModal")
        srpmModal.resize(500, 150)
        srpmModal.setMinimumSize(QtCore.QSize(500, 150))
        srpmModal.setMaximumSize(QtCore.QSize(500, 150))
        srpmModal.setBaseSize(QtCore.QSize(500, 150))
        self.label = QtWidgets.QLabel(srpmModal)
        self.label.setGeometry(QtCore.QRect(110, 50, 271, 21))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(srpmModal)
        self.widget.setGeometry(QtCore.QRect(10, 110, 481, 33))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.retranslateUi(srpmModal)
        QtCore.QMetaObject.connectSlotsByName(srpmModal)

    def retranslateUi(self, srpmModal):
        _translate = QtCore.QCoreApplication.translate
        srpmModal.setWindowTitle(_translate("srpmModal", "Source\'s modification"))
        self.label.setText(_translate("srpmModal", "Do you wish to modificate source codes?"))
        self.pushButton_2.setText(_translate("srpmModal", "Choose"))
        self.pushButton.setText(_translate("srpmModal", "OK / Cancel"))

