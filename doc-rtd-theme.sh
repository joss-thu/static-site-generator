#!/bin/bash

case "${1}" in
quickstart)
    # -- ------------------------------------------------------------------------
    # Check if sphinx, sphinx_rtd_theme and myst_parser (optional) are installed
    # -- ------------------------------------------------------------------------
    if ! python3 -c "import sphinx" 2>/dev/null; then
        echo -e "sphinx not installed. Please install it with:\n pip install sphinx"
        exit 1
    fi

    if ! python3 -c "import sphinx_rtd_theme" 2>/dev/null; then
        echo -e "sphinx rtd theme not installed. Please install it with:\n pip install sphinx-rtd-theme"
        exit 1
    fi

    if ! python3 -c "import myst_parser" 2>/dev/null; then
        echo -e "myst parser (for markdown combatibility) not installed. Please install it with:\n pip install myst-parser"
        exit 1
    fi
    # -- ------------------------------------------------------------------------
    # Quickstart the sphinx project
    # -- ------------------------------------------------------------------------
    rm -rf docs && mkdir -p docs && cd docs && sphinx-quickstart
    
    # -- ------------------------------------------------------------------------
    # Edit the conf.py file.
    # Note:Edit the section below to suit the respective theme installed. Check sphinx themes for details
    # -- ------------------------------------------------------------------------
    conf="./conf.py"
    if [ -f $conf ]; then
        # echo "Current directory: $(pwd)"
        # ls -l source/conf.py
        
        # Add suitable extensions
        sed -i 's/extensions = .*/extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc", "myst_parser"]/' $conf
        
        # Specify theme
        sed -i "s/html_theme = .*/html_theme = 'sphinx_rtd_theme'/" $conf

        # Add path for src folder (where code is)
        sed -i '1i\
import os, sys\
sys.path.insert(0, os.path.abspath(".."))\
' "$conf"

    # Add additional theme specific configurations
echo -e "# -- Additonal configurations -------------------------------------------------

autosummary_generate = True  # Automatically generate autosummary pages

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_logo = '../../copyrights/joss_codes.png'  # Example: 'images/logo.png'
html_favicon = None  # Example: 'images/favicon.ico'

# -- ReadTheDocs theme options ------------------------------------------------
html_theme_options = {
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': 'white',
    'flyout_display': 'hidden',
    'version_selector': True,
    'language_selector': True,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Options for LaTeX output -------------------------------------------------
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
}

# -- Options for manual page output ------------------------------------------
man_pages = [
    ('index', 'projectname', 'Project Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    ('index', 'ProjectName', 'Project Documentation',
     author, 'ProjectName', 'Short project description.',
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
autoclass_content = 'class'  # Include only class and not __init__ docstrings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}" >> $conf
    else
        echo "Error: config file not found. Reattempt the project."
        echo "Note: The project should have separate source and build folders"
    fi
    ;;

api-doc)
    # -- ------------------------------------------------------------------------
    # api-doc the sphinx project
    # -- ------------------------------------------------------------------------
    sphinx-apidoc -o ./docs/source ./src
    
    # Delete the default content
    index="./docs/index.rst"
    sed -i '/Add your content/,/documentation for details./d' "$index"

    # -- ------------------------------------------------------------------------
    # Replace the toctree with customised content, including 'modules', so that it need not be included manually
    # -- ------------------------------------------------------------------------
if [ -f "$index" ]; then
    echo "Updating toctree block in $index"

    # Build the new block in a temp file
    tmpfile=$(mktemp)

    # Note: The project description should be changed depending on the project.
    cat << EOF > "$tmpfile"
This project is a static site generator built with Python.
It converts markdown and other source files into a complete, styled HTML documentation site using Sphinx.

.. toctree::
   :maxdepth: 2

   modules
EOF

    # Replace the block between .. toctree:: and the next empty line
    # Create a temp output file because inline replacement fails with multi-line text
    awk -v block="$(cat "$tmpfile")" '
        BEGIN { in_block=0 }
        /^\.\. toctree::/ { print block; in_block=1; next }
        in_block && /^$/ { in_block=0; next }
        !in_block { print }
    ' "$index" > "$index.tmp" && mv "$index.tmp" "$index"

    rm "$tmpfile"
else
    echo "Error: index.rst cannot be located!"
fi
    ;;

build)
    # -- ------------------------------------------------------------------------
    # Build the sphinx project
    # -- ------------------------------------------------------------------------
    cd docs && rm -rf build && make html
    ;;
serve)
    # -- ------------------------------------------------------------------------
    # Serve the sphinx project
    # -- ------------------------------------------------------------------------
    python3 -m http.server 8000 --directory ./docs/_build/html
    ;;

build-serve)
    # -- ------------------------------------------------------------------------
    # (Re)generate api-doc, build and serve again 
    # -- ------------------------------------------------------------------------
    ./doc-rtd-theme.sh build && ./doc-rtd-theme.sh serve
    ;;
create-build-serve)
    # -- ------------------------------------------------------------------------
    # Create, generate api doc, build and serve again 
    # -- ------------------------------------------------------------------------
    ./doc-rtd-theme.sh quickstart && ./doc-rtd-theme.sh api-doc && ./doc-rtd-theme.sh build && ./doc-rtd-theme.sh serve
    ;;
*)
    echo "usage: $0 {quickstart|api-doc|build|serve|build-serve|create-build-serve}"
    exit 1
    ;;
esac
