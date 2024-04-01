"""
Go through the drop-python commit history and create history.jsonl of lines like this:

{"date": "2017-10-22 18:44:21+03:00", "drop_totals": {"3.2":204, "3.3":102, "2.6":105}}
{"date": "2017-10-22 17:44:22+03:00", "drop_totals": {"3.2":203, "3.3":102, "2.6":105}}

Usage:
pip install -r history-requirements.txt
python3 history_get.py  # creates/updates history.jsonl
"""

import argparse
import json

import git  # pip install gitpython
import jsonlines  # pip install jsonlines
from tqdm import tqdm  # pip install tqdm

# from pprint import pprint  # noqa: F401


def load_from_file(file_name):
    try:
        with open(file_name) as f:
            packages = json.load(f)
        return packages

    except json.decoder.JSONDecodeError:
        return None


def do_json_file():
    data = load_from_file("results.json")
    do_json(data)


def do_json(data):
    packages = data["data"]

    drop_totals = dict()
    for package in packages:
        for key, value in package.items():
            if key in ["downloads", "name", "value"]:
                continue
            thingy = int(value["dropped_support"] == "yes")
            try:
                drop_totals[key] += thingy
            except KeyError:
                drop_totals[key] = thingy

    return drop_totals


def load_jsonlines(file_name):
    with jsonlines.open(file_name) as reader:
        lines = [line for line in reader]
    return lines


def append_jsonlines(file_name, lines):
    with jsonlines.open(file_name, mode="a") as writer:
        for line in lines:
            writer.write(line)


DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        help="Number of commits to process. For testing, default: all",
    )
    args = parser.parse_args()
    print(args.number)

    try:
        old_lines = load_jsonlines("history.jsonl")
    except FileNotFoundError:
        old_lines = []
    old_dates = {d["date"] for d in old_lines}

    repo = git.Repo(".")
    origin = repo.remote("origin")
    print("Fetch origin/gh-pages...")
    origin.fetch("gh-pages")

    print("Get data...")
    new_lines = []

    commits = list(repo.iter_commits("origin/gh-pages"))
    if args.number:
        commits = commits[: args.number]
    commits.reverse()  # oldest first
    for commit in tqdm(commits):
        if str(commit.authored_datetime) in old_dates:
            continue

        try:
            target_file = commit.tree / "results.json"
        except KeyError:
            # eg. "Blob or Tree named 'results.json' not found"
            continue
        data = target_file.data_stream.read()
        data = json.loads(data)
        drop_totals = do_json(data)
        new_lines.append(
            {"date": str(commit.authored_datetime), "drop_totals": drop_totals}
        )

    append_jsonlines("history.jsonl", new_lines)
    print(f"Updated with {len(new_lines)} commits")


if __name__ == "__main__":
    main()
