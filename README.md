# Drop Python

[![Build Status](https://travis-ci.org/hugovk/drop-python.svg?branch=master)](https://travis-ci.org/hugovk/drop-python)

It's about time to drop support for old Pythons.

## How to use

```bash
$ python generate.py -h
usage: generate.py [-h] [-n NUMBER] [-v VERSION]

Generate

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        Number of packages to chart (default: 360)
  -v VERSION, --version VERSION
                        Python version to check (default: 2.6)
```

For example:
```bash
$ python generate.py

$ python generate.py -n 3.2 -n 100
```
See also build.sh.

## How to test locally

In another terminal:
```bash
$ python -m SimpleHTTPServer 8000
```

Then visit http://localhost:8000/

## Thanks

This is derivative work from [Python Wheels](pythonwheels.com), a site that tracks progress in the new Python package distribution standard called [Wheels](https://pypi.python.org/pypi/wheel). Thanks also to [Python 3 Wall of Superpowers](https://python3wos.appspot.com/) for the concept and making their code open source, and see also [Python 3 Readiness](py3readiness.org).
