[![Build Status](https://travis-ci.org/rh-lab-q/rpg.svg?branch=master)](https://travis-ci.org/rh-lab-q/rpg)

RPG - RPM Package Generator
===========================

RPG is tool, that guides people through the creation of a RPM package.
RPG makes packaging much easier due to the automatic analysis of packaged files.
Beginners can get familiar with packaging process or the advanced users can use our tool for a quick creation of a package.


Requirements
============

You need these packages in order to satisfy RPG dependencies:
* coreutils
* file
* makedepend
* python3 >= 3.4
* qt5-qtbase-gui
* python3-qt5
* rpmdevtools
* python3-nose (for tests)
* python3-argcomplete (optional)
* python3-dnf  (optional)
* python3-copr (optional)

Building in Fedora 21+
======================

To get project and satisfy all dependencies, run::

    git clone https://github.com/rh-lab-q/rpg
    cd rpg
    sudo dnf builddep rpg.spec

Start RPG
=========

From project root directory execute::

    python3 rpg.py


Running tests
=============

From project root directory execute::

    cmake .
    make test


Documentation
=============

For documentation, tutorials and examples check [github wiki pages](https://github.com/rh-lab-q/rpg/wiki/)


Contribution
============

Here's the most direct way to get your work merged into the project.

1. Fork the project
2. Clone down your fork
3. Create a feature branch
4. Hack away and add tests, not necessarily in that order
5. Make sure everything still passes by running tests
6. If necessary, rebase your commits into logical chunks without errors
7. Push the branch up to your fork
8. Send a pull request for your branch


License
=======

All files inside project are under GNU General Public License v.2
