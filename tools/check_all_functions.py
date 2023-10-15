#!/usr/bin/env python3
from subprocess import run
from csv import DictReader

from common.util import config

VERSION = config.get_default_version()
DATA_PATH = config.get_versioned_data_path(VERSION)
TOOLS_PATH = config.get_repo_root() / "tools"

def get_csv_rows(file: str) -> list:
    rows: list = []
    with open(file, "r") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            rows.append(row)

    return rows

def main() -> None:
    funcs: list = get_csv_rows(DATA_PATH / "blitz_functions.csv")

    for i in range(len(funcs)):
        if funcs[i]["Address"] == funcs[i-1]["Address"]:
            continue
        run([TOOLS_PATH / "check", "--no-pager", funcs[i]["Name"]])


if __name__ == "__main__":
    main()
