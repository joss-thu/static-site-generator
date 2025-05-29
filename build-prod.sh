# Production build
# This script is called in the deploy-site.yml

python3 -m src.main "/static-site-generator/" 

# Notes: 
# - While using github pages, choose the right build configurations from the pages settings
# - While using Netlify (or vercel) change the base directory to '/static-site-generator/', specific only to this project.

