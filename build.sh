#!/bin/bash

# Prevents script from running if there are any errors
set -e

# Update
git pull origin master

# Fetch fresh copy of top packages
wget https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json -O top-pypi-packages.json

# Generate the files
python generate.py --version 2.6 3.2 3.3

# Make output directory, don't fail if it exists
mkdir -p build

# Copy to output directory
cp -R {2.6,3.2,3.3,index.html,results.json,wheel.css} build
