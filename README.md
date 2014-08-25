===========================
RPG - RPM Package Generator
===========================

RPG is tool, that guides people through the creation of a RPM package.
RPG makes packaging much easier due to the automatic analysis of packaged files.
Beginners can get familiar with packaging process or the advanced users can use our tool for a quick creation of a package.


Building for Fedora
===================

Packages needed for the build, or the build requires:
* python3 >= 3.4 or pathlib python 3 module (`pip-python3 install pathlib`)
* python3-qt5
* file
* dnf
* rpmdevtools

Start RPG
=========
execute `python3 RPG.py` from project root directory


Running tests
=============

execute `nosetests-3.4 tests` from project root directory


Documentation
=============

For documentation, tutorials and examples check [github wiki pages](https://github.com/rh-lab-q/rpg/wiki/)


License
=======

All files inside project are under GNU General Public License v.2
