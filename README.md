# Drop Python

[![Test](https://github.com/hugovk/drop-python/actions/workflows/test.yml/badge.svg)](https://github.com/hugovk/drop-python/actions/workflows/test.yml)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

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
$ python3 generate.py

$ python3 generate.py -v 3.2 -n 100

$ python3 generate.py -v 2.6
```
See also build.sh.

Gets list of packages from [Top PyPI Packages](https://hugovk.github.io/top-pypi-packages/).

## How to test locally

In another terminal:
```bash
$ python3 -m http.server 8000
```

Then visit http://localhost:8000/

## How to deploy

Run crontas.sh hourly from cron.

## Thanks

This is derivative work from [Python Wheels](https://pythonwheels.com), a site that tracks progress in the new Python package distribution standard called [Wheels](https://pypi.org/project/wheel). Thanks also to [Python 3 Wall of Superpowers](https://python3wos.appspot.com/) for the concept and making their code open source, and see also [Python 3 Readiness](http://py3readiness.org).
