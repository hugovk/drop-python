from __future__ import print_function, unicode_literals

import datetime
import json
import os

import pytz
import requests
from pip._vendor.packaging import specifiers

BASE_URL = 'https://pypi.org/pypi'

EXCLUDED_PACKAGES = {
    # backports
    'argparse',
    'backports-abc',
    'backports-functools-lru-cache',
    'backports-shutil-get-terminal-size',
    'backports-ssl-match-hostname',
    'backports-weakref',
    'configparser',
    'contextlib2',
    'enum-compat',
    'enum34',
    'funcsigs',
    'functools32',
    'future',
    'futures',
    'linecache2',
    'mock',
    'monotonic',
    'ordereddict',
    'pathlib2',
    'singledispatch',
    'six',
    'subprocess32',
    'traceback2',
    'typing',
    'unittest2',

    # deprecated
    'BeautifulSoup',
    'distribute',
    'django-social-auth',
    'google-gax',
    'letsencrypt',
    'lockfile',
    'msgpack-python',
    'nose',
    'oauth2client',
    'pep8',
    'pycrypto',
    'sklearn',
    'tensorflow-tensorboard',
}

SESSION = requests.Session()

CLASSIFIER = 'Programming Language :: Python :: {}'


def create_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def get_json_url(package_name):
    return BASE_URL + '/' + package_name + '/json'


def requires_python_supports(requires_python, version):
    """
    Check if a given Python version matches the `requires_python` specifier.

    Returns "yes" if the version of Python matches the requirement.
    Returns "no" if the version of Python does not matches the requirement.
    Returns "maybe" if there's no requirement.

    Raises an InvalidSpecifier if `requires_python` have an invalid format.
    """
    if requires_python is None or requires_python == "":
        # The package provides no information
        return "maybe"
    requires_python_specifier = specifiers.SpecifierSet(requires_python)

    return "yes" if version in requires_python_specifier else "no"


def classifiers_support(classifiers, version):
    """Do these classifiers support this Python version?"""
    desired_classifier = CLASSIFIER.format(version)

    # Explicit support
    if desired_classifier in classifiers:
        return "yes"

    # Check if classifiers are explicit.
    # Only report "no" when at least one major.minor version is explicitly
    # supported (but not the desired one).
    for classifier in classifiers:
        if CLASSIFIER.format("2.") in classifier:
            return "no"
        if CLASSIFIER.format("3.") in classifier:
            return "no"

    # Otherwise?
    return "maybe"


def annotate_support(packages, versions=['2.6']):
    print('Getting support data...')
    num_packages = len(packages)
    for index, package in enumerate(packages):
        print(index + 1, num_packages, package['name'])
        url = get_json_url(package['name'])
        response = SESSION.get(url)
        if response.status_code != 200:
            print(' ! Skipping ' + package['name'])
            continue
        data = response.json()

        for version in versions:

            # Init
            package[version] = {}

            # First try with requires_python
            has_support = requires_python_supports(
                data['info']['requires_python'], version)

            # Second try with classifers
            if has_support == 'maybe':
                has_support = classifiers_support(
                    data['info']['classifiers'], version)

            if has_support == "yes":
                package[version]['dropped_support'] = "no"
            if has_support == "no":
                package[version]['dropped_support'] = "yes"
            if has_support == "maybe":
                package[version]['dropped_support'] = "maybe"

            # Display logic. I know, I'm sorry.
            package['value'] = 1
            if has_support == "no":
                package[version]['css_class'] = 'success'
                package[version]['icon'] = u'\u2713'  # Check mark
                title = "This package doesn't support Python {}."
            elif has_support == "yes":
                package[version]['css_class'] = 'default'
                package[version]['icon'] = u'\u2717'  # Ballot X
                title = 'This package supports Python {}.'
            else:  # "maybe"
                package[version]['css_class'] = 'default'
                package[version]['icon'] = '?'
                title = 'This package may support Python {}.'
            package[version]['title'] = title.format(version)


def get_top_packages():
    print('Getting packages...')

    with open('top-pypi-packages.json') as data_file:
        packages = json.load(data_file)['rows']

    # Rename keys
    for package in packages:
        package['downloads'] = package.pop('download_count')
        package['name'] = package.pop('project')

    return packages


def not_excluded(package):
    return package['name'] not in EXCLUDED_PACKAGES


def remove_irrelevant_packages(packages, limit):
    print('Removing cruft...')
    active_packages = list(filter(not_excluded, packages))
    return active_packages[:limit]


def save_to_file(packages, file_name):
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    with open(file_name, 'w') as f:
        f.write(json.dumps({
            'data': packages,
            'last_update': now.strftime('%A, %d %B %Y, %X %Z'),
        }))
