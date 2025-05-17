#!/bin/bash

case "${1}" in
quickstart)
    if ! python3 -c "import sphinx" 2>/dev/null; then
        echo -e "sphinx not installed. Please install it with:\n pip install sphinx"
        exit 1
    fi

    if ! python3 -c "import sphinx_rtd_theme" 2>/dev/null; then
        echo -e "sphinx rtd theme not installed. Please install it with:\n pip install sphinx-rtd-theme"
        exit 1
    fi

    rm -rf docs && mkdir -p docs && cd docs && sphinx-quickstart
    
    conf="./source/conf.py"
    if [ -f $conf ]; then
        echo "Current directory: $(pwd)"
        ls -l source/conf.py
        sed -i 's/extensions = .*/extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]/' $conf
        sed -i "s/html_theme = .*/html_theme = 'sphinx_rtd_theme'/" $conf
        sed -i '1i\
import os, sys\
sys.path.insert(0, os.path.abspath("../.."))\
' "$conf"
    else
        echo "Error: config file not found. Reattempt the project."
        echo "Note: The project should have separate source and build folders"
    fi
    ;;

api-doc)
    echo "Current directory for api-doc: $(pwd)"

 
    sphinx-apidoc -o ./docs/source ./src

    index="./docs/source/index.rst"





    
if [ -f "$index" ]; then
    echo "Updating toctree block in $index"

    # Build the new block in a temp file
    tmpfile=$(mktemp)
    cat << EOF > "$tmpfile"
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
    echo "Current directory for build: $(pwd)"
    cd docs && rm -rf build && mkdir -p build && make html
    ;;
serve)
    python3 -m http.server 8000 --directory ./docs/build/html
    ;;

build-serve)
    ./doc.sh api-doc && ./doc.sh build && ./doc.sh serve
    ;;
*)
    echo "usage: $0 {quicksstart|api-doc|build|serve|build-serve}"
    exit 1
    ;;
esac
