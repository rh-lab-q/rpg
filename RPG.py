from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from src.gui.wizard import Wizard

def main():
    import sys
 
    app = QApplication(sys.argv)
    wiz = Wizard()
    wiz.setObjectName("RPG")
    wiz.resize(847, 650)
    wiz.setMinimumSize(QtCore.QSize(847, 650))
    wiz.setMaximumSize(QtCore.QSize(847, 650))
    wiz.setBaseSize(QtCore.QSize(847, 650))
    wiz.show()
 
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()