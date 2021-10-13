#!/usr/bin/env bash
set -e

date

# Install dependencies
python3 -m pip install -r requirements.txt

git checkout master
git pull origin master
