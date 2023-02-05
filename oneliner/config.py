from appdirs import AppDirs
import argparse
import os
from pathlib import Path
import sys
import toml
from typing import Dict

VERSION = "0.3.0"


def default_filename() -> str:
    return "oneliner-%Y.txt"


def default_prefix() -> str:
    return "%Y-%m-%d"


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

    ## get config file location
    if args["conf"]:
        conffile = args["conf"]
    else:
        conffile = find_conf_file()

    if args["info"]:
        print(f"Using {conffile}")

    ## read config
    config = toml.load(conffile)
    # @TODO

    if config["path"]:
        args["path"] = config["path"]

    if config["filename"]:
        args["filename"] = config["filename"]
    else:
        args["filename"] = default_filename()

    if config["prefix"]:
        args["prefix"] = config["prefix"]
    else:
        args["prefix"] = default_prefix()

    return args


def find_conf_file() -> str:
    """Find config file"""

    # check environment variable
    if os.environ.get("ONELINER_CONF_FILE"):
        return os.environ.get("ONELINER_CONF_FILE")

    # check for platform config directory
    dirs = AppDirs("Oneliner", "mkaz")
    if Path(dirs.user_config_dir, "oneliner.conf").is_file():
        return Path(dirs.user_config_dir, "oneliner.conf")

    home = os.environ.get("HOME")
    if not Path(home).is_dir():
        print("No home directory !?")
        sys.exit()

    # check .config
    hc = f"{home}/.config/oneliner.conf"
    if Path(hc).is_file():
        return Path(hc)

    # check .local
    lc = f"{home}/.local/oneliner.conf"
    if Path(lc).is_file():
        return Path(lc)

    # check current dir
    if Path("oneliner.conf").is_file():
        return Path("oneliner.conf")

    print("Can not locate oneliner.conf")
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


# Multiple Journals
# Use: oneliner -j movies '😱 Halloween 1978'

[journals]
movies_filename = 'movies-%Y.txt'
movies_path = '/Users/mkaz/Documents/Lists'


# For time parameters see:
# https://docs.rs/chrono/0.4.0/chrono/format/strftime/index.html
"""
