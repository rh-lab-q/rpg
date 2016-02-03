CMAKE_MINIMUM_REQUIRED (VERSION 2.4)
PROJECT (RPG NONE)

OPTION(DISABLE_MOCK_TEST "Enables tests in tests/mock_build directory" OFF)
OPTION(DISABLE_UNIT_TEST "Enables tests in tests/unit directory" OFF)
OPTION(DISABLE_CONNECTION_TEST "Enables tests in tests/connection directory" OFF)
OPTION(WITH_MAN  "Enables installation of manual pages" OFF)

# Python search:
FIND_PACKAGE (PythonInterp 3.4 REQUIRED)

EXECUTE_PROCESS(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; sys.stdout.write('%s.%s' % (sys.version_info.major, sys.version_info.minor))" OUTPUT_VARIABLE PYTHON_MAJOR_DOT_MINOR_VERSION)

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
    FIND_PROGRAM (NOSETESTS_EXE nosetests-${PYTHON_MAJOR_DOT_MINOR_VERSION})
    IF (NOSETESTS_EXE)
        MESSAGE (STATUS "${NOSETESTS_EXE} found")
        ENABLE_TESTING ()
        ADD_SUBDIRECTORY (tests)
        ADD_CUSTOM_TARGET (test-unit COMMAND ${NOSETESTS_EXE} tests/unit WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
        ADD_CUSTOM_TARGET (test-connection COMMAND ${NOSETESTS_EXE} tests/connection WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
        ADD_CUSTOM_TARGET (test-mock COMMAND ${NOSETESTS_EXE} tests/mock_build WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
    ELSE ()
        MESSAGE (WARNING "Nosetests is missing! - no tests available - ${NOSETESTS_EXE}")
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

# Documentation:
ADD_SUBDIRECTORY (doc)
