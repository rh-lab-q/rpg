#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from rpg import Base
from rpg.gui.wizard import Wizard
import logging
import sys


def main():
    base = Base()
    app = QApplication(sys.argv)
    base.conf.parse_cmdline()
    base.load_plugins()
    wiz = Wizard(base)
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
