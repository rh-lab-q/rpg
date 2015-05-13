Name:           hello
Version:        1.4
Release:        1%{?dist}
Summary:        Hello World test program
License:        GPLv2
Source:         %{name}-%{version}.tar.gz

%description
Hello World C project for testing RPG.

%prep
%autosetup

%build
make

%install
make install DESTDIR=%{RPM_BUILD_ROOT}


