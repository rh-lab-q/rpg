Name:           rpg
Version:        0.0.3
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
BuildRequires:  python3-sphinx
BuildRequires:  qt5-qtbase-gui
BuildRequires:  coreutils
BuildRequires:  file
BuildRequires:  makedepend
BuildRequires:  rpmdevtools
BuildRequires:  python3-copr
BuildRequires:  python3-hawkey
BuildRequires:  mock
BuildArch:      noarch

Requires:       python3 >= 3.4
Requires:       python3-qt5
Requires:       qt5-qtbase-gui
Requires:       coreutils
Requires:       file
Requires:       makedepend
Requires:       rpmdevtools
Requires:       mock
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
make doc-man

%post
activate-global-python-argcomplete
exec bash

%install
%make_install

%check
make ARGS="-V" test-unit
make ARGS="-V" test-long

%files
%{_bindir}/rpg
%{python3_sitelib}/rpg/
%{_mandir}/man8/rpg.8.gz

%changelog
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

