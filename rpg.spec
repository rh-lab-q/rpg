Name:           rpg
Version:        0.0.1
Release:        1%{?snapshot}%{?dist}
Summary:        RPM Package Generator
License:        GPLv2
URL:            https://github.com/rh-lab-q/rpg
Source:         %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  python3-nose
BuildRequires:  python3-devel
BuildRequires:  python3 >= 3.4
BuildRequires:  python3-qt5
BuildRequires:  python3-copr
BuildRequires:  qt5-qtbase-gui
BuildRequires:  coreutils
BuildRequires:  file
BuildRequires:  makedepend
BuildRequires:  rpmdevtools
BuildArch:      noarch

Requires:       python3 >= 3.4
Requires:       python3-qt5
Requires:       qt5-qtbase-gui
Requires:       coreutils
Requires:       file
Requires:       makedepend
Requires:       rpmdevtools
%if 0%{?fedora} >= 21
Recommends:     python3-argcomplete
Recommends:     python3-dnf
Recommends:     python3-copr
%endif

%description
RPG is tool, that guides people through the creation of a RPM
package. RPG makes packaging much easier due to the automatic analysis of
packaged files. Beginners can get familiar with packaging process or the
advanced users can use our tool for a quick creation of a package.

%prep
%setup -q -n rpg-%{version}

%build
%cmake .

%post
activate-global-python-argcomplete
exec bash

%install
make install DESTDIR=%{RPM_BUILD_ROOT}
%make_install

%check
make ARGS="-V" test

%files
%{_bindir}/rpg
%{python3_sitelib}/rpg/

%changelog
