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

