import argparse
import os
from string import Template

from utils import create_dir

SUBSTITUTIONS = {
    "2.0": {"template_eol": "2001-06-22"},
    "2.1": {"template_eol": "2002-04-08"},
    "2.2": {"template_eol": "2003-05-30"},
    "2.3": {"template_eol": "2008-03-11"},
    "2.4": {"template_eol": "19 December 2008"},
    "2.5": {"template_eol": "26 May 2011"},
    "3.0": {"template_eol": "27 June 2009"},
    "3.1": {"template_eol": "9 April 2012"},
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Template",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v",
        "--version",
        default=["2.6", "3.2", "3.3"],
        nargs="+",
        help="Python version or versions to check",
    )
    args = parser.parse_args()

    # Open the file
    with open("template/index.html") as infile:
        # Read it
        src = Template(infile.read())

        for version in args.version:

            # Document data
            print(version)
            major, minor = version.split(".")
            next_minor = int(minor) + 1
            next_version = "{}.{}".format(major, next_minor)
            substitutions = SUBSTITUTIONS[version]
            d = {
                "template_version": version,
                "template_eol": substitutions["template_eol"],
                "template_major": major,
                "template_minor": minor,
                "template_next_minor": next_minor,
                "template_next_version": next_version,
            }

            # Do the substitution
            result = src.safe_substitute(d)
            # print(result)

            # Save it
            outfile = os.path.join(version, "index.html")
            print(outfile)
            create_dir(version)
            with open(outfile, "w") as f:
                f.write(result)
