import pynotificator
import sphinx_rtd_theme

project = 'PyNotificator'
copyright = '2020, higurashi-takuto'
author = 'higurashi-takuto'
version = pynotificator.__version__
release = pynotificator.__version__

extensions = ['sphinx.ext.napoleon', 'sphinx_rtd_theme']

# templates_path = ['_templates']

language = 'ja'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# html_static_path = ['_static']

html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}

# Docstring
autodoc_member_order = 'bysource'
