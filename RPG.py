from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from rpg.gui.wizard import Wizard
import logging


def main():
    import sys

    logging.basicConfig(filename='rpg.log', level=logging.INFO)
    logging.info('App started')

    app = QApplication(sys.argv)
    wiz = Wizard()
    wiz.setObjectName("RPG")
    wiz.resize(850, 650)
    wiz.setMinimumSize(QtCore.QSize(850, 650))
    wiz.setMaximumSize(QtCore.QSize(850, 650))
    wiz.setBaseSize(QtCore.QSize(850, 650))
    wiz.show()

    logging.info('App exiting')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
