from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
from rpg.gui.wizard import Wizard
import logging
import sys


def main():
    app = QApplication(sys.argv)
    wiz = Wizard()
    wiz.setObjectName("RPG")
    wiz.resize(850, 650)
    wiz.setMinimumSize(QtCore.QSize(850, 650))
    wiz.setMaximumSize(QtCore.QSize(850, 650))
    wiz.setBaseSize(QtCore.QSize(850, 650))
    wiz.show()

    logging.info('GUI loaded')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
