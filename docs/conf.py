import os, sys
sys.path.insert(0, os.path.abspath(".."))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Static Website Generator'
copyright = '2025, JossCodes'
author = 'JossCodes'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc", "myst_parser"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
# -- Additonal configurations -------------------------------------------------

pygments_style = 'sphinx'
pygments_dark_style = 'monokai'

autosummary_generate = True  # Generate autosummary pages automatically

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_logo = '../copyrights/joss_codes.png'  # Path to your logo
html_favicon = None  # Path to your favicon

# -- Furo-specific options ---------------------------------------------------
html_theme_options = {
    'sidebar_hide_name': False,
    'navigation_with_keys': True,
    'top_of_page_buttons': ['view', 'edit'],
    'light_css_variables': {
        'color-brand-primary': 'red',
        'color-brand-content': '#CC3333',
        'color-admonition-background': 'orange',
    },
}

# -- Options for LaTeX output -------------------------------------------------
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
}

# -- Options for manual page output ------------------------------------------
man_pages = [
    ('index', 'myproject', 'My Project Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    ('index', 'MyProject', 'My Project Documentation',
     author, 'MyProject', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------
epub_title = project
epub_exclude_files = ['search.html']

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Todo extension options --------------------------------------------------
todo_include_todos = True

# -- Autodoc options ---------------------------------------------------------
autoclass_content = 'class'  # Include only class docstring and not __init__
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}




