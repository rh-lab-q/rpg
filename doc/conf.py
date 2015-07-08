import sys
import os
import re

sys.path.insert(0,os.path.abspath('../rpg'))

AUTHORS=[u'See AUTHORS in RPG source distribution.']

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


# Fix of module ImportErrors
class Mock(object):
    def __init__(self, *args):
        pass
 
    def __getattr__(self, name):
        return Mock
 
for mod_name in ('pathlib', 'copr', 'copr.client', 'urllib', 'urllib.request'):
    sys.modules[mod_name] = Mock()


