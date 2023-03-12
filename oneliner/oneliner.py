#!/usr/bin/env python3
"""
Oneliner - command-line tool to take one line notes.
"""
from config import init_args
from datetime import date, timedelta
from pathlib import Path
import sys


def main():
    args = init_args()

    # Setup date - check for yesterday
    if args["yesterday"]:
        dt = date.today() - timedelta(days=1)
    else:
        dt = date.today()

    # Convert filename using date
    filename = dt.strftime(args["filename"])
    dirpath = Path(args["path"])
    if not dirpath.is_dir():
        print(f"Notes directory not found: {dirpath}")
        print(
            """To make sure notes are not created in some random spot, the notes
            directory must already exist. Please create or change path config
            in oneliner.conf to an existing directory"""
        )
        sys.exit()

    filepath = Path(args["path"], filename)

    # display file content and exit
    if args["show"]:
        if not Path(filepath).is_file():
            print(f"File does not exist: {filepath}")
            sys.exit()

        with open(filepath, "r") as f:
            for line in f:
                print(line.rstrip())  # print doubles up
        sys.exit()

    # writing content out to file
    if not args["content"]:
        print("Nothing to write")
        sys.exit()

    prefix = dt.strftime(args["prefix"])
    content = " ".join(args["content"])
    data = prefix + " | " + content + "\n"

    # open file for appends
    with open(filepath, "a") as f:
        f.write(data)

    if args["info"]:
        print(f"Wrote new line to {filepath}")


if __name__ == "__main__":
    main()
