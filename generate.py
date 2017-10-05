import argparse
import os
from svg_wheel import generate_svg_wheel
from utils import (annotate_support, get_top_packages,
                   remove_irrelevant_packages, save_to_file)


def main(to_chart=360, version="2.6"):
    packages = remove_irrelevant_packages(get_top_packages(), to_chart)
    annotate_support(packages, version)
    results_json = os.path.join(version, 'results.json')
    save_to_file(packages, results_json)
    generate_svg_wheel(packages, to_chart, version)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-n", "--number", default=360, type=int,
        help="Number of packages to chart")
    parser.add_argument(
        "-v", "--version", default="2.6",
        help="Python version to check")
    args = parser.parse_args()

    main(args.number, args.version)
