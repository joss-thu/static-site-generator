#!/bin/bash

case "${1}" in
quickstart)
    # -- ------------------------------------------------------------------------
    # Check if sphinx, sphinx_rtd_theme and myst_parser (optional) are installed
    # -- ------------------------------------------------------------------------
    echo -e "
Welcome to the Sphinx Documentation project !!
==============================================
NOTE: 
- Select NO when prompted to create separate source and build folders.

    "
    if ! python3 -c "import sphinx" 2>/dev/null; then
        echo -e "sphinx not installed. Please install it with:\n pip install sphinx"
        exit 1
    fi

    if ! python3 -c "import furo" 2>/dev/null; then
        echo -e "sphinx furo theme not installed. Please install it with:\n pip install furo"
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
        sed -i "s/html_theme = .*/html_theme = 'furo'/" $conf

        # Add path for src folder (where code is)
        sed -i '1i\
import os, sys\
sys.path.insert(0, os.path.abspath(".."))\
' "$conf"

    # Add additional theme specific configurations
echo -e "# -- Additonal configurations -------------------------------------------------

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



" >> $conf
    else
        echo "Error: config file not found. Reattempt the project."
        echo "Note: The project should NOT have separate source and build folders"
    fi
    ;;

api-doc)
    # -- ------------------------------------------------------------------------
    # api-doc the sphinx project
    # -- ------------------------------------------------------------------------
    sphinx-apidoc -o ./docs/ ./src
    
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

It takes raw content files (like Markdown and images) and turns them into a static website (a mix of HTML and CSS files).

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
    fuser -k 8000/tcp 2>/dev/null
    python3 -m http.server 8000 --directory ./docs/_build/html
    ;;

build-serve)
    # -- ------------------------------------------------------------------------
    # (Re)generate api-doc, build and serve again 
    # -- ------------------------------------------------------------------------
    ./doc-furo-theme.sh build && ./doc-furo-theme.sh serve
    ;;
create-build-serve)
    # -- ------------------------------------------------------------------------
    # Create, generate api doc, build and serve again 
    # -- ------------------------------------------------------------------------
    ./doc-furo-theme.sh quickstart && ./doc-furo-theme.sh api-doc && ./doc-furo-theme.sh build && ./doc-furo-theme.sh serve
    ;;
*)
    echo "usage: $0 {quickstart|api-doc|build|serve|build-serve|create-build-serve}"
    exit 1
    ;;
esac
