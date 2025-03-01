#!/bin/bash

# Prevents script from running if there are any errors
set -e

# Info
python3 --version

# Install dependencies
python3 -m pip install -r requirements.txt

# Update
git pull origin main

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages.min.json -O top-pypi-packages.json

# Fetch Python EOL dates
wget https://endoflife.date/api/python.json -O python-eol.json

# TEMP workaround
# https://github.com/nodejs/node/issues/43132#issuecomment-1130503287
export OPENSSL_CONF=/dev/null

# Generate the files
python3 generate.py --version 2.{0,1,2,3,4,5,6,7} 3.{0,1,2,3,4,5,6,7,8,9}

# Create index.html files from the template
python3 template.py --version 2.{0,1,2,3,4,5,6,7} 3.{0,1,2,3,4,5,6,7,8,9}

# Make output directory, don't fail if it exists
mkdir -p build

# Copy to output directory
cp -R {2.{0,1,2,3,4,5,6,7},3.{0,1,2,3,4,5,6,7,8,9},all.html,index.html,results.json,style.css,wheel.css} build

# Remove templated index.html files
rm {2.{0,1,2,3,4,5,6,7},3.{0,1,2,3,4,5,6,7,8,9}}/index.html
