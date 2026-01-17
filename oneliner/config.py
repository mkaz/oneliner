import argparse
import sys
from pathlib import Path
from typing import Dict

import toml

from . import __version__ as VERSION

DEFAULT_FILENAME = "oneliner-%Y.txt"
DEFAULT_PREFIX = "%Y-%m-%d"


def init_args() -> Dict:
    parser = argparse.ArgumentParser(description="oneliner")
    parser.add_argument("-c", "--conf", help="Configuration file")
    parser.add_argument("-i", "--info", help="Debug info", action="store_true")
    parser.add_argument("-j", "--journal", help="Alternate Journal file")
    parser.add_argument("--sample", help="Output a sample config", action="store_true")
    parser.add_argument("-s", "--show", help="Show entries", action="store_true")
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

    # get config file location
    if args["conf"]:
        conffile = args["conf"]
    else:
        conffile = find_conf_file()

    # args is what gets returned config items
    # will be merged over
    args["filename"] = DEFAULT_FILENAME
    args["prefix"] = DEFAULT_PREFIX

    # read config
    config = toml.load(conffile)

    # Merge config over args
    # anything in config will overwrite defaults
    args = args | config

    # If alternate journal specified, use config variables
    # for that journal to override
    if args["journal"]:
        journal = args["journal"]
        if journal not in config["journals"]:
            print(f"Journal '{journal}' not found in config {conffile}")
            sys.exit()

        if "filename" not in config["journals"][journal]:
            print(f"Filename not specified for '{journal}'")
            sys.exit()

        # merge journals config
        args = args | config["journals"][journal]

    return args


def find_conf_file() -> Path:
    """Find config file"""

    # check .config
    hc = Path.home() / ".config/oneliner/config.toml"
    if hc.is_file():
        return hc

    print("Did not find $HOME/.config/oneliner/config.toml")
    print("Create sample config using:")
    print("   > mkdir $HOME/.config/oneliner")
    print("   > oneliner --sample > $HOME/.config/oneliner/config.toml")
    sys.exit()


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


##----- Multiple Journals

# Use: oneliner -j movies '😱 Halloween 1978'

[journals]

[journals.movies]
filename = 'movies-%Y.txt'
path = '/Users/mkaz/Documents/Lists'


# For time parameters see:
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
"""
