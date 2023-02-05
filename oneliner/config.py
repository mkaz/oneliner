import argparse
import sys
from typing import Dict

VERSION = "0.3.0"


def default_filename() -> str:
    return "oneliner-%Y.txt"


def default_prefix() -> str:
    return "%Y-%m-%d"


def init_args() -> Dict:
    parser = argparse.ArgumentParser(description="oneliner")
    parser.add_argument("-c", "--config", help="Configuration file")
    parser.add_argument("--sample", help="Output a sample config", action="store_true")
    parser.add_argument("-j", "--journal", help="Alternate Journal file")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "-y", "--yesterday", help="Use yesterday's date", action="store_true"
    )
    parser.add_argument("content", nargs=argparse.REMAINDER)
    args = vars(parser.parse_args())

    if args["version"]:
        print(f"oneliner v{VERSION}")
        sys.exit()

    if args["sample"]:
        print(sample_config())
        sys.exit()

    ## read config file to get info
    args["path"] = "/Users/mkaz/Documents"
    args["filename"] = "oneliner-%Y.txt"
    args["prefix"] = "%Y-%m-%d"

    return args


def sample_config() -> str:
    return """
# oneliner config file

# Base directory that all notes are stored
# Use full path for directory
path = '/Users/mkaz/Documents/'

# Default filename
filename = 'oneliner-%Y.txt'

# Format for date prefix before each line
# 2022-12-01 | YOUR NOTE HERE
prefix = '%Y-%m-%d'


# Multiple Journals
# Use: oneliner -j movies '😱 Halloween 1978'

[journals]
movies_filename = 'movies-%Y.txt'
movies_path = '/Users/mkaz/Documents/Lists'


# For time parameters see:
# https://docs.rs/chrono/0.4.0/chrono/format/strftime/index.html
"""
