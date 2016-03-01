from setuptools import setup, find_packages
setup(
    name="SetupToolsTestProject",
    version="0.1",
    description=("test description"),
    license="BSD",
    url="http://test.example",
    packages=find_packages(),
    scripts=['testscript.py'],
)
