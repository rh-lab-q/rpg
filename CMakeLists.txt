CMAKE_MINIMUM_REQUIRED (VERSION 2.4)
PROJECT (RPG NONE)

# Python search:
FIND_PACKAGE (PythonInterp 3.4 REQUIRED)

# Python3QT5 search:
EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c 
    "from PyQt5 import QtWidgets, QtCore, QtGui\n"
    "from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QLineEdit,"
                                 "QCheckBox, QGroupBox, QPushButton,"
                                 "QGridLayout, QTextEdit, QListWidget,"
                                 "QHBoxLayout, QDialog, QFileDialog,"
                                 "QTreeWidget, QTreeWidgetItem)"
                RESULT_VARIABLE PYTHON3QT5_SEARCH)
IF (NOT PYTHON3QT5_SEARCH)
    MESSAGE (STATUS "Python3QT5 exists")
ELSE ()
    MESSAGE (FATAL_ERROR "Python3QT5 is missing!")
ENDIF ()

# Makedepend search:
FIND_PROGRAM (MakeDepProg makedepend)
IF (MakeDepProg)
    MESSAGE (STATUS "Makedepend exists")
ELSE ()
    MESSAGE (FATAL_ERROR "Makedepend is missing!")
ENDIF ()

# file search:
FIND_PROGRAM (FileProg file)
IF (FileProg)
    MESSAGE (STATUS "File exists")
ELSE ()
    MESSAGE (FATAL_ERROR "File is missing!")
ENDIF ()

# coreutils search:
FIND_PROGRAM (COREUTILS_SEARCH cat)
IF (COREUTILS_SEARCH)
    MESSAGE (STATUS "CoreUtils exists")
ELSE ()
    MESSAGE (FATAL_ERROR "CoreUtils is missing!")
ENDIF ()

# rpmdevtools search:
FIND_PROGRAM(RPMDEVTOOLS_SEARCH rpmbuild)
IF (RPMDEVTOOLS_SEARCH)
    MESSAGE (STATUS "Rpm developer tools exists")
ELSE ()
    MESSAGE (FATAL_ERROR "Rpm developer tools is missing!")
ENDIF ()

# nosetests search:
IF (EXISTS ${PROJECT_SOURCE_DIR}/tests)
    FIND_PROGRAM (NoseProg nosetests-3.4)
    IF (NoseProg)
        MESSAGE (STATUS "Nosestests exists")
        ENABLE_TESTING ()
        ADD_SUBDIRECTORY (tests)
    ELSE ()
        MESSAGE (WARNING "Nosetests is missing! - no tests available")
    ENDIF ()
ELSE ()
    MESSAGE (WARNING "No tests available")
ENDIF ()

# Set install directory:
EXECUTE_PROCESS (COMMAND ${PYTHON_EXECUTABLE} -c "from sys import stdout; from distutils import sysconfig; stdout.write(sysconfig.get_python_lib())" OUTPUT_VARIABLE PYTHON_INSTALL_DIR)
MESSAGE (STATUS "Installing to dir '${PYTHON_INSTALL_DIR}'")

# Installation:
ADD_SUBDIRECTORY (rpg)
INSTALL (PROGRAMS "rpg.py" DESTINATION bin RENAME rpg)
