Writing plugins
###############

Plugins are the main part of RPG. Their purpose is to append :doc:`Spec class  <api_spec>` with tags and scripts. Whole process of creating spec file from source code in RPG app is following:

* plugins are triggered in project directory - they set some tags/scripts in Spec instance
* guessed values from Spec are auto filled in GUI forms and user can modify them
* next spec command (``%prep``, ``%build``, ``%install``, ``%files``) is executed and new directory is created
* repeat steps for new directory

Plugin is a class that is derived from ``rpg.plugin.Plugin`` and overrides at least one of following methods: ``download``, ``extraction``, ``extracted``, ``patched``, ``compiled``, ``installed``, ``package_built``. Each of them takes ``(spec, current_dir, sack)`` parameters. ``spec`` is instance of :doc:`Spec class  <api_spec>`, ``sack`` is initialized sack from DNF and ``current_dir`` is pathlib.Path instance where are project files of future RPM package located. ``current_dir`` is different in each phase.

.. csv-table:: Phases
   :header: "Phase", "Description", "Base call"
   :widths: 10 60 30


   "download", "downloads archive from url. This is because url adress may be github repository - then plugin only add archive/master.zip to the url and downloads it", --
   "extraction", "method that extract files from archive. This exists because there are many types of archives like tar, zip, ...", --
   "extracted", "raw files are extracted from chosen archive or copied files from project working directory", :meth:`extracted source analysis <__init__.Base.run_extracted_source_analysis>`
   "patched", "after application of patches on source files", :meth:`patched source analysis <__init__.Base.run_patched_source_analysis>`
   "compiled", "after execution of ``%build`` script (e.g. calling ``make``)", :meth:`compiled source analysis <__init__.Base.run_compiled_source_analysis>`
   "installed", "directory containing files after ``make install``", :meth:`installed source analysis <__init__.Base.run_installed_source_analysis>`
   "package_built", "path to final rpm package", --
   "mock_recover", "after building project in mock enviroment, build errors (if there are any) are passed as parameter to this method. This should fix build by parsing the errors and finding the solution, i.e. append missing required files to build_required_files", --


Inside plugin can be helper methods that should not be named as any of the phase. It should follow conventions as any private Python method (e.g. ``_helper_method``).

For plugin examples take a look at `core plugins folder <https://github.com/rh-lab-q/rpg/tree/master/rpg/plugins>`_.
