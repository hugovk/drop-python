import datetime as dt
import json
import os
from zoneinfo import ZoneInfo  # Python 3.9+

import requests
from packaging import specifiers

BASE_URL = "https://pypi.org/pypi"

EXCLUDED_PACKAGES = {
    # backports
    "argparse",
    "backports-abc",
    "backports-entry-points-selectable",
    "backports-functools-lru-cache",
    "backports-shutil-get-terminal-size",
    "backports-ssl-match-hostname",
    "backports-tempfile",
    "backports-weakref",
    "backports-zoneinfo",
    "configparser",
    "contextlib2",
    "enum-compat",
    "enum34",
    "funcsigs",
    "functools32",
    "future",
    "futures",
    "importlib-metadata",
    "ipaddress",
    "linecache2",
    "mock",
    "monotonic",
    "ordereddict",
    "pathlib",
    "pathlib2",
    "scandir",
    "simplejson",
    "singledispatch",
    "six",
    "subprocess32",
    "traceback2",
    "typing",
    "typing-extensions",
    "unicodecsv",
    "unittest2",
    "zipp",
    # deprecated
    "BeautifulSoup",
    "boto",
    "bs4",
    "distribute",
    "django-social-auth",
    "gitdb2",
    "google-gax",
    "jws",
    "letsencrypt",
    "lockfile",
    "msgpack-python",
    "nose",
    "oauth2client",
    "pep8",
    "py",
    "pycrypto",
    "raven",
    "retrying",
    "sklearn",
    "simplegeneric",
    "smmap2",
    "tensorflow-tensorboard",
    # deleted after violating PyPI AUP
    "pypular",
}

SESSION = requests.Session()

CLASSIFIER = "Programming Language :: Python :: {}"


def create_dir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)


def get_json_url(package_name):
    return BASE_URL + "/" + package_name + "/json"


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
    major, minor = version.split(".")

    # Explicit major.minor support
    if desired_classifier in classifiers:
        return "yes"

    # Check if classifiers are explicit.
    # Only report "no" when at least one other major.minor version is explicitly
    # supported (but not the desired one).
    # ie. major and major.other present, but major.minor is missing.
    if any(f"{major}." in c for c in classifiers):
        return "no"

    python_any = any("Programming Language :: Python ::" in c for c in classifiers)
    python = "Programming Language :: Python" in classifiers
    # python2 = "Programming Language :: Python :: 2" in classifiers
    python3 = "Programming Language :: Python :: 3" in classifiers
    python2x = any("Programming Language :: Python :: 2." in c for c in classifiers)
    python3x = any("Programming Language :: Python :: 3." in c for c in classifiers)

    # No major.minor listed
    if major == "2" and python and python3 and not python3x:
        return "maybe"

    if major == "2" and python3x and not python2x:
        return "no"

    # We have at least some version listed, but not even this major
    if python_any and CLASSIFIER.format(major) not in classifiers:
        return "no"

    # Otherwise?
    return "maybe"


def annotate_support(packages, versions=["2.6"]):
    print("Getting support data...")
    num_packages = len(packages)
    for index, package in enumerate(packages):
        print(index + 1, num_packages, package["name"])
        url = get_json_url(package["name"])
        response = SESSION.get(url)
        if response.status_code != 200:
            print(" ! Skipping " + package["name"])
            continue
        data = response.json()

        for version in versions:
            # Init
            package[version] = {}

            # First try with requires_python
            has_support = requires_python_supports(
                data["info"]["requires_python"], version
            )

            # Second try with classifers
            if has_support == "maybe":
                has_support = classifiers_support(data["info"]["classifiers"], version)

            if has_support == "yes":
                package[version]["dropped_support"] = "no"
            if has_support == "no":
                package[version]["dropped_support"] = "yes"
            if has_support == "maybe":
                package[version]["dropped_support"] = "maybe"

            # Display logic. I know, I'm sorry.
            package["value"] = 1
            if has_support == "no":
                package[version]["css_class"] = "success"
                package[version]["icon"] = "\u2713"  # Check mark
                title = "This package doesn't support Python {}."
            elif has_support == "yes":
                package[version]["css_class"] = "default"
                package[version]["icon"] = "\u2717"  # Ballot X
                title = "This package supports Python {}."
            else:  # "maybe"
                package[version]["css_class"] = "default"
                package[version]["icon"] = "?"
                title = "This package may support Python {}."
            package[version]["title"] = title.format(version)


def get_top_packages():
    print("Getting packages...")

    with open("top-pypi-packages.json") as data_file:
        packages = json.load(data_file)["rows"]

    # Rename keys
    for package in packages:
        package["downloads"] = package.pop("download_count")
        package["name"] = package.pop("project")

    return packages


def not_excluded(package):
    return package["name"] not in EXCLUDED_PACKAGES


def remove_irrelevant_packages(packages, limit):
    print("Removing cruft...")
    active_packages = list(filter(not_excluded, packages))
    return active_packages[:limit]


def save_to_file(packages, file_name):
    now = dt.datetime.utcnow().replace(tzinfo=ZoneInfo("UTC"))
    with open(file_name, "w") as f:
        f.write(
            json.dumps(
                {"data": packages, "last_update": now.strftime("%A, %d %B %Y, %X %Z")}
            )
        )
