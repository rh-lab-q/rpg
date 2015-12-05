Name:           rpg
Version:        0.0.5
Release:        1%{?snapshot}%{?dist}
Summary:        RPM Package Generator
License:        GPLv2
URL:            https://github.com/rh-lab-q/rpg
Source:         %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  python3-qt5
BuildRequires:  qt5-qtbase-gui
BuildArch:      noarch

Requires:       python3-qt5
Requires:       qt5-qtbase-gui
Requires:       python3-rpg = %{version}-%{release}

%package -n python3-rpg
Summary:    Python3 interface for RPG.
%{?python_provide:%python_provide python3-rpg}
BuildRequires:  python3-nose
BuildRequires:  python3-devel
BuildRequires:  python3 >= 3.4
BuildRequires:  python3-sphinx
BuildRequires:  python3-hawkey
BuildRequires:  python3-javapackages
BuildRequires:  coreutils
BuildRequires:  file
BuildRequires:  makedepend
BuildRequires:  rpmdevtools
BuildRequires:  python3-copr >= 1.58
BuildRequires:  mock
Requires:       python3 >= 3.4
Requires:       mock
Requires:       python3-javapackages
Requires:       coreutils
Requires:       file
Requires:       makedepend
Requires:       rpmdevtools
%if 0%{?fedora} >= 21
Recommends:     python3-argcomplete
Recommends:     python3-dnf
Recommends:     python3-copr >= 1.58
%endif
%description -n python3-rpg
Python3 interface for RPG.

%description
RPG is tool, that guides people through the creation of a RPM
package. RPG makes packaging much easier due to the automatic analysis of
packaged files. Beginners can get familiar with packaging process or the
advanced users can use our tool for a quick creation of a package.

%prep
%setup -q -n rpg-%{version}

%build
%cmake . -DWITH_MAN=1 -DDISABLE_MOCK_TEST=1 -DDISABLE_CONNECTION_TEST=1
make doc-man

%install
%make_install

%check
make ARGS="-V" test

%files
%{_mandir}/man8/rpg.8.gz
%{_bindir}/rpg

%files -n python3-rpg
%{python3_sitelib}/rpg/

%changelog
* Wed Nov 25 2015 Jan Silhan <jsilhan@redhat.com> 0.0.5-1
- tito: added releasers (Jan Silhan)
- Fix new docker image (Pavol Vican)
- command: removed execute_from (Jan Silhan)
- spec: remove unused methods and attribute (fix #333) (Jan Silhan)
- add flake8-diff error code (fix #344) (Pavol Vican)
- Autotools macro corrections (fix #312) (Miroslav Cibulka)
- Separated packages rpg and python3-rpg (fix #275) (regeciovad)
- Unit test for maven (fix #341) (xslouk02)
- prefil of the mandatory page (fix #295) (Lukas Slouka)
- AUTHORS added (Miroslav Cibulka)
- Documenting code and some minor refactoring (Miroslav Cibulka)
- libhif test (fix #327) (Miroslav Cibulka)
- Extention of hawkey test (Miroslav Cibulka)
- Ignore not found files in translating files to packages (Miroslav Cibulka)
- apt-get yes to all - travis build fix (Miroslav Cibulka)
- autotools: log-checking compiled-phase added (#334) (Miroslav Cibulka)
- add parameter -y of command apt-get (Pavol Vican)
- fix mock build test (Pavol Vican)
- disable long test in spec file (fix #330) (Pavol Vican)
- Fix test in TRAVIS CI + upload SRPM (fix #316) (fix #308) (fix #213) (Pavol
  Vican)
- Maven plugin (#fix #130) (LukasSlouka)
- Changed long tests to connection tests (fix #329) (yousifd)

* Wed Oct 07 2015 Jan Silhan <jsilhan@redhat.com> 0.0.4-1
- Gui - meaning of asterisk added (fix #320) (regeciovad)
- Changed gcc/g++ to makedepend, resolves system-depend tests (fix #296)
  (Miroslav Cibulka)
- Fixed bad parse of mock logs (Miroslav Cibulka)
- Find file now find all installed files (fix #319) (Miroslav Cibulka)
- Python now compiles installed directory if py file is found (fix #253)
  (Miroslav Cibulka)
- CMake macro correction (fix #313) (Miroslav Cibulka)
- Gui - Copr pages text and spacing changes (regeciovad)
- Copr - upload of local srpms (fix #309) (regeciovad)
- Gui - Build page tips (regeciovad)
- Gui - new CoprDistro page (fix #317) (regeciovad)
- Gui - all tips are visible (fix #264) (regeciovad)
- Gui - new coprLogin and coprDistro pages (fix #268) (regeciovad)
- Gui - new distro selection (fix #292) (regeciovad)
- Gui - fill of empty description (fix #289) (regeciovad)
- Gui - split of mandatory page (fix #293) (regeciovad)
- Gui - version tag validation (fix #301) (regeciovad)
- Gui - prefill spec attributes (fix #280) (regeciovad)
- build_rpm now throws error instead of return (fix #278) (Miroslav Cibulka)
- C plugin is now extended with mock_recover (fix #303) (Miroslav Cibulka)
- Find file test now watch directory for new files (fix #281) (Miroslav
  Cibulka)
- make test_build_rpg pass (fix #274) (Miroslav Cibulka)
- Escaping spaces with path_to_str function (fix #245) (Miroslav Cibulka)
- (build)requiredfiles may now be glob expression (Miroslav Cibulka)
- Test for building libsovl (fix #62) (Miroslav Cibulka)
- Verbose make test - mock tests removed from test suite (Miroslav Cibulka)
- make check resolved by CMakePlugin (LukasSlouka)
- expand build/install fields via rpm (Fixes #285) (Igor Gnatenko)
- packaging: drop twice execution of make install (Igor Gnatenko)
- postun & post ldconfig fix (Miroslav Cibulka)
- Cplugin repair + added support for C++ (fix #249) (Miroslav Cibulka)
- Compiled phase had wrong directory as argument (Miroslav Cibulka)
- Report error on failed mock_recover (Miroslav Cibulka)
- caching files from resolved packages (optimization of files_to_pkgs plugin)
  (Miroslav Cibulka)
- Gui - build page refactor (fix #267) (regeciovad)
- Gui - intro page added (fix #266) (regeciovad)
- Gui - asterisk in lighter red (fix #265) (regeciovad)
- Gui - cancel button moved to the left corner (fix #263) (regeciovad)
- Gui - page titles shifted to the right (fix #262) (regeciovad)
- Copy rpms to the destination (fix #241) (regeciovad)
- Update README.md (Jan Šilhan)
- Update README.md (Jan Šilhan)
- README: link to readthedocs (Jan Silhan)
- build_rpm_recover is now general (fix #240) (Miroslav Cibulka)
- CMake plugin upgrade (fix #256) (LukasSlouka)
- spec.files refactor to set (fix #272) (LukasSlouka)
- Requires set to list bug (fix #271) (LukasSlouka)
- Autotools plugin implemented (fix #15) (LukasSlouka)
- Setuptools plugin + short test (fix #131) (LukasSlouka)
- Hawkey package test (fix #76) (LukasSlouka)
- RPG fo newbies (fix #216) (regeciovad)
- rpm_path + errors connected with this (Miroslav Cibulka)

* Tue Aug 18 2015 Jan Silhan <jsilhan@redhat.com> 0.0.3-1
- SourceLoader + load_project_from_url refactored (Miroslav Cibulka)
- Gui building page redesign (fix #226) (regeciovad)
- test: really update spec set attr (Jan Silhan)
- cosmetic: union -> update (Jan Silhan)
- make install fix (fix #247) (LukasSlouka)
- Base method plugin calls refactor (fix #248) (LukasSlouka)
- failing tests fix (Miroslav Cibulka)
- Build RPG test (fix #206) (regeciovad)
- Subpackages page removed (fix #190) (regeciovad)
- Writing plugins doc (fix #123) (LukasSlouka)
- Docs warning (fix #237) (LukasSlouka)
- cmake.py extended: get dependencies from CMakeCache (fix #191) (FLuptak)
- Base.build_rpm: move result rpm to base_dir (Jan Silhan)
- Base.srpm_path search for more proper srpm file name (Jan Silhan)
- call build_rpm in build_rpm_recover (Jan Silhan)
- builds srpm if does not exists during Base.build_rpm (Jan Silhan)
- Base: renamed dnf_load_sack to load_dnf_sack (Jan Silhan)
- Base.compute_checksum madew private (Jan Silhan)
- removed: apply patches (Jan Silhan)
- Spec tags documentation (fix #188) (LukasSlouka)
- Subpackage documentation (#fix 219) (LukasSlouka)
- merging Requires and BuildRequires if spec.check is not empty (fix #228)
  (Miroslav Cibulka)
- loading archives bug fixed (fix #229) (Miroslav Cibulka)
- ReadTheDocs (fix #231) (LukasSlouka)
- Spec tags as instance attributes (fix #219) (LukasSlouka)
- Flake8 errors fixed (mostly) with Pep8 (fix #222) (Miroslav Cibulka)
- Build rpm in GUI(fix #218) (regeciovad)
- Base build_rpm (#218) (regeciovad)
- Speeding up files_to_pkgs with dictionary + flake8 errors (Miroslav Cibulka)
- make plugin now search for Makefile and makefile (Miroslav Cibulka)
- Mock project analyse + mock-test + unit-test (without mock) (fix #184)
  (Miroslav Cibulka)
- mock_build test suite added (fix #211) (Miroslav Cibulka)
- Spec attributes refactoring (fix #219) (LukasSlouka)
- git rebase CI PR (fix #215) (Pavol Vican)
- Documentation fix for python3-sphinx (fix #121) (LukasSlouka)
- Conf.py fix (LukasSlouka)
- Print replacement (LukasSlouka)
- Documentation for Base and Spec (fix #188) (LukasSlouka)
- Comments removal (fix #121) (LukasSlouka)
- CLI options documentation (fix #198) (LukasSlouka)
- Doc setup (fix #121) (LukasSlouka)
- load_project_from_url regex checking of github url (Miroslav Cibulka)
- rpg.package_builder.build_rpm implemented + long tests (fix #175) (fix #176)
  (Miroslav Cibulka)
- spec file: redundant python3-copr removed (regeciovad)
- Extra parameter removed from download_git_repo - callback (fix #207)
  (Miroslav Cibulka)
- Mock init cleans cache (regeciovad)
- command: ignore new line at the end (Jan Silhan)
- Gui - moved build_project (regeciovad)
- consmetic: conf: move import statement (Jan Silhan)
- README to install rpg (fix #200) (Pavol Vican)
- fix the COPR builds (Pavol Vican)
- add log flake8 (fix #171) (Pavol Vican)
- Upload srpm + run copr (fix #159) (Pavol Vican)

* Fri Jul 03 2015 Jan Silhan <jsilhan@redhat.com> 0.0.2-1
- yum install added to travis (Miroslav Cibulka)
- python3-corp added to mock rpg.cfg (Miroslav Cibulka)
- download_archive has now 10 tries till exception (Miroslav Cibulka)
- active waiting 'till mock ends (Miroslav Cibulka)
- spec: all Requires added to BuildRequires (Jan Silhan)
- Copr_uploader deleted (fix #185) (regeciovad)
- Python-copr instead of copr-cli (#185) (regeciovad)
- gui fix (regeciovad)
- fetch_repos in new thread (fix #154) (regeciovad)
- Waiter for mock - yum update - Travis (#172) (Miroslav Cibulka)
- long test separation (Fix #156) (LukasSlouka)
- spec: added BuilRequires (Jan Silhan)
- Expansion of ~ replaced by rpm macro eval (Miroslav Cibulka)
- files_to_pkgs plugin checks existence of sack (cibo94)
- Command() error is now more verbose (/dev/null should be used locally)
  (cibo94)
- Finding libs and programs are now universal (cibo94)
- (Build)Required files are now attribute (fix #177) (cibo94)
- Python file excludes added (fix #169) (cibo94)
- New first page and PagePatches deleted (fix #152) (regeciovad)
- Spec file is removed on tearDown (fix #172) (cibo94)
- Home path is now absolute (#172) (cibo94)
- files_to_pkgs plugin implemented + test (fix #128) (cibo94)
- Copr: new ToolTips (fix #9) (regeciovad)
- Mock fetch_repos (#153) (regeciovad)
- Build srpm output path fix (fix #160) (regeciovad)
- tests: remove hello.spec from find files (see 24bd61e) (Jan Silhan)
- README: cosmetic: removed hr (Jan Silhan)
- README: added travis CI build status (Jan Silhan)
- spec: print verbose test errors (Jan Silhan)
- this fixes the rpg rpm building (Pavol Vican)
- Add travis (fix #141) (Pavol Vican)
- plugin: python: exclude project py files (fix #165) (Jan Silhan)
- tar was packing files with full-path (cibo94)
- Duplicate '%%autosetup' removed (cibo94)
- installed phase moved to the page before (Build)Requires (fix #167) (cibo94)
- DNF stack was initialized before plugin engine was (fix #168) (cibo94)
- shutil.rmtree doesn't throw FileNotFoundError and errors can be supressed
  (cibo94)
- Always build with newly generated specfile (fix #161) (cibo94)
- spec: ignore weak deps for < f21 (Jan Silhan)
- Creating archive bug fixed + copy of tarball added to builder (cibo94)
- fixed wrong order of writing spec file (Miroslav Cibulka)
- process_archive_or_dir to load_project_from_url (fix #149) (Miroslav Cibulka)
- Tito fix regression from 634d4a2 (LukasSlouka)
- build_srpm calls create_archive (Jan Silhan)
- self.Source is ${name}-${version}.tar.gz (fix #155) (Miroslav Cibulka)
- test_functional - package builder correction (#117) (xcibul10)
- Spec file refactored (fix #124) (xcibul10)
- Copr: GUI added (#9) (regeciovad)
- Copr_uploader methods (#9) (regeciovad)
- Functional test added (#117) (regeciovad)
- spec: rpg package name is lowercase (Jan Silhan)
- spec.Source + write_spec + buildLocationEdit fix (fix #150) (regeciovad)
- Package builder refactored (xcibul10)
- Description should be macro (fix #144) (xcibul10)
- hello_project in test/project added to test_find_files (xcibul10)
- import project from github and url implemented (fix #126) (fix #127)
  (xcibul10)
- create_archive() implemented (fix #137) (fix #89) (xcibul10)
- SourceLoader refactored (fix #96) (xcibul10)
