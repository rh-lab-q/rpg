import sys
import os
import re


_dirname = os.path.dirname(__file__)

sys.path.insert(0, _dirname)

AUTHORS=[u'See AUTHORS in RPG source distribution.']

extensions = []

templates_path = ['_templates']

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
    #('index', 'rpg', u'rpg Documentation',
    # AUTHORS, 1),
    ('command_ref', 'rpg', u'RPG Command Reference',
     AUTHORS, 8),
]

texinfo_documents = [
  ('index', 'rpg', u'rpg Documentation',
   AUTHORS[0], 'rpg', 'Tool used for creation of RPM packages',
   'Miscellaneous'),
]

