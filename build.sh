# build for deploy
# This script is called in the deploy-site.yml

python3 -m src.main "/static-site-generator/" # While deploying via github pages
python3 -m src.main "/" # While deploying via netlify/vercel pages
