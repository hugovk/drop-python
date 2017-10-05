from __future__ import print_function
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


def annotate_support(packages, version='2.6'):
    print('Getting support data...')
    num_packages = len(packages)
    for index, package in enumerate(packages):
        print(index + 1, num_packages, package['name'])
        has_support = False
        url = get_json_url(package['name'])
        response = SESSION.get(url)
        if response.status_code != 200:
            print(' ! Skipping ' + package['name'])
            continue
        data = response.json()
        has_support = CLASSIFIER.format(version) in data['info']['classifiers']
        package['dropped_support'] = not has_support

        # Display logic. I know, I'm sorry.
        package['value'] = 1
        if not has_support:
            package['css_class'] = 'success'
            package['icon'] = u'\u2713'  # Check mark
            package['title'] = "This package doesn't support Python {}."
        else:
            package['css_class'] = 'default'
            package['icon'] = u'\u2717'  # Ballot X
            package['title'] = 'This package supports Python {}.'
    package['title'] = package['title'].format(version)


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
