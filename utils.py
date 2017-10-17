from __future__ import print_function, unicode_literals
import datetime
import json
try:
    # Python 2.7
    import xmlrpclib
except ImportError:
    # Python 3
    import xmlrpc.client as xmlrpclib

import pytz
import requests


BASE_URL = 'https://pypi.python.org/pypi'

DEPRECATED_PACKAGES = set((
    'distribute',
    'django-social-auth',
    'BeautifulSoup'
))

SESSION = requests.Session()

CLASSIFIER = 'Programming Language :: Python :: {}'


def req_rpc(method, *args):
    payload = xmlrpclib.dumps(args, method)

    response = SESSION.post(
        BASE_URL,
        data=payload,
        headers={'Content-Type': 'text/xml'},
    )
    if response.status_code == 200:
        result = xmlrpclib.loads(response.content)[0][0]
        return result
    else:
        # Some error occurred
        pass


def get_json_url(package_name):
    return BASE_URL + '/' + package_name + '/json'


def supports(classifiers, version):
    """Do these classifiers support this Python version?"""
    desired_classifier = CLASSIFIER.format(version)

    # Explicit support
    if desired_classifier in classifiers:
        return "yes"

    # The explicit one has not been found

    # Check if classifiers are explicit.
    # Only report "no" when at least one major.minor version is explicitly
    # supported (but not the desired one).
    for classifier in classifiers:
        if CLASSIFIER.format("2.") in classifier:
            return "no"
        if CLASSIFIER.format("3.") in classifier:
            return "no"

    if version.startswith("2."):
        if CLASSIFIER.format("2 :: Only") in classifiers:
            return "maybe"

    if version.startswith("3."):
        if CLASSIFIER.format("3 :: Only") in classifiers:
            return "maybe"

    for classifier in classifiers:
        if " :: Only" in classifier:
            # We know it's the wrong version, because
            # we've already checked for the right version.
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
            package[version] = dict()

            has_support = supports(data['info']['classifiers'], version)
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
    packages = req_rpc('top_packages')
    return [{'name': n, 'downloads': d} for n, d in packages]


def not_deprecated(package):
    return package['name'] not in DEPRECATED_PACKAGES


def remove_irrelevant_packages(packages, limit):
    print('Removing cruft...')
    active_packages = list(filter(not_deprecated, packages))
    return active_packages[:limit]


def save_to_file(packages, file_name):
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    with open(file_name, 'w') as f:
        f.write(json.dumps({
            'data': packages,
            'last_update': now.strftime('%A, %d %B %Y, %X %Z'),
        }))
