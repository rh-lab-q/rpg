CMAKE_MINIMUM_REQUIRED (VERSION 3.0)
PROJECT (RPG)

# Python search:
FIND_PACKAGE (PythonInterp 3.4 REQUIRED)

# QT5 search:
EXECUTE_PROCESS (COMMAND bash -c "find /lib64 /usr /lib /etc -name qt5 2>/dev/null | tr '\n' ' '" OUTPUT_VARIABLE QT5_SEARCH)
IF (QT5_SEARCH)
    MESSAGE (STATUS "QT5 exists")
ELSE ()
    MESSAGE (FATAL_ERROR "QT5 is missing!")
ENDIF ()

# QT5Base search:
EXECUTE_PROCESS (COMMAND bash -c "find /lib64 /usr /lib /etc -path '*qt5*qtbase*' 2>/dev/null | tr '\n' ' '" OUTPUT_VARIABLE QT5BASE_SEARCH)
IF (QT5BASE_SEARCH)
    MESSAGE (STATUS "QT5Base exists")
ELSE ()
    MESSAGE (FATAL_ERROR "QT5Base is missing!")
ENDIF ()

# Python3QT5 search:
EXECUTE_PROCESS (COMMAND bash -c "find /lib64 /usr /lib /etc -name python3-qt5 2>/dev/null | tr '\n' ' '" OUTPUT_VARIABLE PYTHON3QT5_SEARCH)
IF (PYTHON3QT5_SEARCH)
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
EXECUTE_PROCESS (COMMAND bash -c "find /lib64 /usr /lib /etc -name coreutils 2>/dev/null | tr '\n' ' '" OUTPUT_VARIABLE COREUTILS_SEARCH)
IF (COREUTILS_SEARCH)
    MESSAGE (STATUS "CoreUtils exists")
ELSE ()
    MESSAGE (FATAL_ERROR "CoreUtils is missing!")
ENDIF ()

# rpmdevtools search:
EXECUTE_PROCESS (COMMAND bash -c "find /lib64 /usr /lib /etc -path '*rpmdevtools' 2>/dev/null | tr '\n' ' '" OUTPUT_VARIABLE RPMDEVTOOLS_SEARCH)
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
INSTALL (PROGRAMS "RPG.py" DESTINATION bin RENAME rpg)
