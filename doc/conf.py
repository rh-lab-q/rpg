import sys
import os


sys.path.insert(0, os.path.abspath('../rpg'))

AUTHORS = [u'See AUTHORS in RPG source distribution.']

extensions = ['sphinx.ext.autodoc']

source_suffix = '.rst'

master_doc = 'index'

project = u'rpg'

copyright = u'2015, Red Hat, Licensed under GPLv2+'

version = '0.0.1'

release = '0.0.1'

exclude_patterns = []

pygments_style = 'sphinx'

html_theme = 'default'

htmlhelp_basename = 'rpgdoc'

latex_elements = {}

latex_documents = [
    ('index', 'rpg.tex', u'rpg Documentation',
     AUTHORS[0], 'manual'),
]

man_pages = [
    ('command_ref', 'rpg', u'RPG Command Reference',
     AUTHORS, 8),
]

texinfo_documents = [
    ('index', 'rpg', u'rpg Documentation',
     AUTHORS[0], 'rpg', 'Tool used for creation of RPM packages',
     'Miscellaneous'),
]

autodoc_mock_imports = [
    'pathlib',
    'copr',
    'copr.client',
    'urllib',
    'urllib.request',
    'urllib.parse',
    'urllib.error',
    'rpg',
    'rpg.plugin_engine',
    'rpg.command',
    'rpg.plugins',
    'rpg.plugins.misc',
    'rpg.plugins.misc.files_to_pkgs',
    'rpg.project_builder',
    'rpg.package_builder',
    'rpg.source_loader',
    'rpg.spec',
    'rpg.conf',
]
