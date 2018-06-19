# Drop Python

[![Build Status](https://travis-ci.org/hugovk/drop-python.svg?branch=master)](https://travis-ci.org/hugovk/drop-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

It's about time to drop support for old Pythons.

## How to use

```bash
usage: generate.py [-h] [-n NUMBER] [-v VERSION [VERSION ...]]

Generate

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        Number of packages to chart (default: 360)
  -v VERSION [VERSION ...], --version VERSION [VERSION ...]
                        Python version or versions to check (default: ['2.6',
                        '3.2', '3.3'])
```

For example:
```bash
$ python generate.py

$ python generate.py -v 3.2 -n 100

$ python generate.py -v 2.6
```
See also build.sh.

Gets list of packages from [Top PyPI Packages](https://hugovk.github.io/top-pypi-packages/).

## How to test locally

In another terminal:
```bash
$ python3 -m http.server 8000

# Or:

$ python2 -m SimpleHTTPServer 8000

# Or:

python -m $(python -c 'import sys; print("http.server" if sys.version_info[:2] > (2, 7) else "SimpleHTTPServer")') 8000
```

Then visit http://localhost:8000/

## How to deploy

Run something like this hourly from cron:

```bash
set -e
cd ~/github/drop-python
git checkout master
git pull origin master # Makes sure build.sh is up-to-date
./build.sh             # Generate files from master branch, copy them to a build subdirectory
./deploy.sh            # Check out gh-pages, copy build files back, commit and push to GitHub Pages
```

## Thanks

This is derivative work from [Python Wheels](https://pythonwheels.com), a site that tracks progress in the new Python package distribution standard called [Wheels](https://pypi.org/project/wheel). Thanks also to [Python 3 Wall of Superpowers](https://python3wos.appspot.com/) for the concept and making their code open source, and see also [Python 3 Readiness](http://py3readiness.org).
