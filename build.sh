#!/bin/bash

# Prevents script from running if there are any errors
set -e

# Update
git pull origin master

# Generate the files
python generate.py --version 2.6
python generate.py --version 3.2
python generate.py --version 3.3

# Make output directory, don't fail if it exists
mkdir -p build

# Copy to output directory
cp -R {2.6,3.2,3.3,index.html,wheel.css} build
