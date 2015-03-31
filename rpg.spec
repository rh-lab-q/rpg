Name:           RPG
Version:        0.1
Release:        1%{?snapshot}%{?dist}
Summary:        RPM Package Generator
#Group:
License:        GNU
#URL:
Source:         %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  python3-devel
BuildArch:      noarch

Requires:       python3 >= 3.4
Requires:       python3-qt5
Requires:       qt5-qtbase-gui
Requires:       coreutils
Requires:       file
Requires:       makedepend
Requires:       rpmdevtools

%description
RPG is tool, that guides people through the creation of a RPM
package. RPG makes packaging much easier due to the automatic analysis of
packaged files. Beginners can get familiar with packaging process or the
advanced users can use our tool for a quick creation of a package.

%prep
%autosetup

%build
%cmake .

%install
make install DESTDIR=%{RPM_BUILD_ROOT}
%make_install

%check
make test

%files
%{_bindir}/rpg
%{python3_sitelib}/rpg/__init__.py
%{python3_sitelib}/rpg/command.py
%{python3_sitelib}/rpg/conf.py
%{python3_sitelib}/rpg/copr_uploader.py
%{python3_sitelib}/rpg/gui/dialogs.py
%{python3_sitelib}/rpg/gui/wizard.py
%{python3_sitelib}/rpg/package_builder.py
%{python3_sitelib}/rpg/plugin.py
%{python3_sitelib}/rpg/plugin_engine.py
%{python3_sitelib}/rpg/plugins/lang/c.py
%{python3_sitelib}/rpg/plugins/lang/python.py
%{python3_sitelib}/rpg/plugins/misc/find_changelog.py
%{python3_sitelib}/rpg/plugins/misc/find_file.py
%{python3_sitelib}/rpg/plugins/misc/find_library.py
%{python3_sitelib}/rpg/plugins/misc/find_patch.py
%{python3_sitelib}/rpg/plugins/misc/find_translation.py
%{python3_sitelib}/rpg/plugins/project_builder/autotools.py
%{python3_sitelib}/rpg/plugins/project_builder/cmake.py
%{python3_sitelib}/rpg/plugins/project_builder/make.py
%{python3_sitelib}/rpg/project_builder.py
%{python3_sitelib}/rpg/source_loader.py
%{python3_sitelib}/rpg/spec.py
%{python3_sitelib}/rpg/utils.py
%{python3_sitelib}/rpg/__pycache__/__init__.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/__init__.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/command.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/command.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/conf.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/conf.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/copr_uploader.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/copr_uploader.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/package_builder.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/package_builder.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/plugin.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/plugin.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/plugin_engine.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/plugin_engine.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/project_builder.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/project_builder.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/source_loader.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/source_loader.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/spec.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/spec.cpython-34.pyo
%{python3_sitelib}/rpg/__pycache__/utils.cpython-34.pyc
%{python3_sitelib}/rpg/__pycache__/utils.cpython-34.pyo
%{python3_sitelib}/rpg/gui/__pycache__/dialogs.cpython-34.pyc
%{python3_sitelib}/rpg/gui/__pycache__/dialogs.cpython-34.pyo
%{python3_sitelib}/rpg/gui/__pycache__/wizard.cpython-34.pyc
%{python3_sitelib}/rpg/gui/__pycache__/wizard.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/lang/__pycache__/c.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/lang/__pycache__/c.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/lang/__pycache__/python.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/lang/__pycache__/python.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_changelog.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_changelog.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_file.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_file.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_library.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_library.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_patch.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_patch.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_translation.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/misc/__pycache__/find_translation.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/project_builder/__pycache__/autotools.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/project_builder/__pycache__/autotools.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/project_builder/__pycache__/cmake.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/project_builder/__pycache__/cmake.cpython-34.pyo
%{python3_sitelib}/rpg/plugins/project_builder/__pycache__/make.cpython-34.pyc
%{python3_sitelib}/rpg/plugins/project_builder/__pycache__/make.cpython-34.pyo

%changelog
