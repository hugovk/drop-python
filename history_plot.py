"""
Take history.jsonl from history_get.py and plot it

Usage:

# Prep
pip install -r history-requirements.txt
python3 history_get.py  # creates/updates history.jsonl

# All available data
python3 history_plot.py && open history.png

# Subset
python3 history_plot.py -v 2.6 2.7 3.3 3.4 3.5 && open history.png
"""
import argparse
import hashlib
from pprint import pprint  # noqa: F401

from termcolor import colored  # pip install termcolor

from history_get import load_jsonlines

EOL = {
    "2.7": "2020-01-01",
    "3.4": "2019-03-18",
    "3.5": "2020-09-30",
}


def dopplr(name):
    """
    Take the MD5 digest of a name,
    convert it to hex and take the
    first 6 characters as an RGB value.
    """
    # Tweak "2.8" because it's too close in colour to "3.5"
    if name == "2.8":
        name = "python 2.8"

    return "#" + hashlib.sha224(name.encode()).hexdigest()[:6]


def make_chart(dates, totals):
    # x: list of dates
    # y: totals for each version
    import matplotlib.pyplot as plt  # pip install matplotlib
    import matplotlib.ticker as plticker

    # "2020-01-26 22:35:22+02:00" -> "2020-01-26"
    dates = [date.split()[0] for date in dates]

    fig, ax = plt.subplots()

    print("Plot...")
    for version, v in totals.items():
        print(version)

        if version in EOL and EOL[version] in dates:
            # Add a vertical line to zero at EOL
            eol_pos = dates.index(EOL[version])
            # dates.insert(eol_pos, EOL[version])
            totals[version][eol_pos] = 0
            # breakpoint()

        ax.plot(dates, v, label=version, color=dopplr(version))

    ax.set_ylim(ymin=0, ymax=360)

    plt.xticks(rotation=90)

    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.2)

    # Shrink current axis by 20% so legend is outside chart
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    # Put a legend to the right of the current axis
    ax.legend(
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    # This locator puts ticks at regular intervals
    loc = plticker.MultipleLocator(base=50)
    ax.xaxis.set_major_locator(loc)
    loc = plticker.MultipleLocator(base=60)
    ax.yaxis.set_major_locator(loc)

    plt.suptitle("Dropped Python versions")
    plt.title("By the top 360 packages downloaded from PyPI", fontsize=10)
    plt.ylabel("Packages")

    outfile = "history.png"
    print(colored(outfile, "green"))
    plt.savefig(outfile, dpi=96 * 2.5)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-v", "--versions", nargs="+", help="Show only these versions")
    args = parser.parse_args()

    # Each line looks like:
    # {
    #  "date": "2020-01-26 23:35:22+02:00",
    #  "drop_totals": {"2.0": 348, "2.1": 348, "2.2": 348, "2.3": 348, "2.4": 342, ...}
    # }
    lines = load_jsonlines("history.jsonl")

    #  First 3-4 days of data is junk, ditch it
    lines = [line for line in lines if line["date"] > "2017-10-11 20:44:23+03:00"]

    # Ditch first few days for some due to bug fixes causing a sudden dip
    for line in lines:
        if line["date"] <= "2017-10-24 23:44:27+03:00":
            line["drop_totals"].pop("2.6", None)
            line["drop_totals"].pop("3.2", None)
        if line["date"] <= "2018-09-06 13:35:20+03:00":
            line["drop_totals"].pop("3.4", None)

    # Sort by date
    lines = sorted(lines, key=lambda k: k["date"])
    print("Number of lines:", len(lines))

    # First get a list of all versions, as not every data point has every version
    if args.versions:
        all_versions = args.versions
    else:
        all_versions = set()
        for line in lines:
            all_versions.update(line["drop_totals"].keys())
        all_versions = sorted(all_versions)
    print("All versions: ", all_versions)

    print("Prep data...")
    dates = []
    totals = dict()
    for line in lines:
        dates.append(line["date"])

        for version in all_versions:
            try:
                version_total = line["drop_totals"][version]
            except KeyError:
                version_total = None

            try:
                totals[version].append(version_total)
            except KeyError:
                totals[version] = [version_total]

    make_chart(dates, totals)


if __name__ == "__main__":
    main()
