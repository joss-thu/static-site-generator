# save path
save_path="./code_metrics/code_metrics_$(date +'%Y-%m-%d %H:%M').txt"

# install dependencies
if ! python3 -c "import radon" 2>/dev/null; then
        echo "Radon not found; install it with sudo apt-get install radon"
        exit 1
fi

if ! python3 -c "import lizard" 2>/dev/null; then
        echo "Lizard not found; install it with sudo apt-get install Lizard"
        exit 1
fi
if ! python3 -c "import code2flow" 2>/dev/null; then
        echo "code2flow not found; install it with pip install code2flow"
        exit 1
fi

if ! python3 -c "import pylint" 2>/dev/null; then
        echo "pylint not found; install it with pip install pylint"
        exit 1
fi

# Add current date and timestamp
echo -e "Code Metrics Report - $(date)\n" > "$save_path"

# Radon cc metrics
echo -e "
--------------------------------------------------------------
Radon Cyclomatic Complexity Analysis
--------------------------------------------------------------
" >> "$save_path"

radon cc src -a >> "$save_path"

# Radon mi metrics
echo -e "
--------------------------------------------------------------
Radon Maintainability Index
--------------------------------------------------------------
" >> "$save_path"

radon mi src -s >> "$save_path"

# Lizard metrics
echo -e "
--------------------------------------------------------------
Lizard Metrics
--------------------------------------------------------------
" >> "$save_path"

lizard src >> "$save_path"

echo -e "
================================================================================================================
" >> "$save_path"

# Run coverage and generate HTML report
coverage run -m unittest discover ./tests
coverage html -d "./code_metrics/htmlcov_$(date +'%Y-%m-%d %H:%M')"

# Method dependencies and claass, package diagrams
code2flow --exclude-functions __init__ ./src/* -o ./code_metrics/method_dependencies.png
pyreverse -o png --colorized -p SSG -d ./code_metrics/ ./src/

#Documentation
./doc-furo-theme.sh create-build-serve
