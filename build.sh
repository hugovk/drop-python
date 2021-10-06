#!/bin/bash

# Prevents script from running if there are any errors
set -e

# Info
python3 --version

# Install dependencies
python3 -m pip install -r requirements.txt

# Update
git pull origin master

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json -O top-pypi-packages.json

# Fetch Python EOL dates
wget https://endoflife.date/api/python.json -O python-eol.json

# Generate the files
python3 generate.py --version 2.{0,1,2,3,4,5,6,7} 3.{0,1,2,3,4,5,6}

# Create index.html files from the template
python3 template.py --version 2.{0,1,2,3,4,5,6,7} 3.{0,1,2,3,4,5,6}

# Make output directory, don't fail if it exists
mkdir -p build

# Copy to output directory
cp -R {2.{0,1,2,3,4,5,6,7},3.{0,1,2,3,4,5,6},all.html,index.html,results.json,style.css,wheel.css} build

# Remove templated index.html files
rm {2.{0,1,2,3,4,5,6,7},3.{0,1,2,3,4,5,6}}/index.html
