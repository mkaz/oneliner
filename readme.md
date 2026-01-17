# oneliner

A simple command-line tool for saving one line notes in plain text files.

## Example

![Demo GIF](https://user-images.githubusercontent.com/45363/206862140-a7fc3b36-a23e-40ea-8a0f-acfcc5636ecd.gif)

Use `oneliner` by adding note on the command-line

```
$ oneliner "Here is my note"
```

## Install

**Step 1:** Install - Three options to install

```
python3 -m pip install git+https://github.com/mkaz/oneliner
```


**Step 2:** Create config.toml, see [Configuration below](#configuration)

## Usage

See `oneliner --help` for help.

Add one line note to default file with today's date

```
    oneliner 'This is my note'
```

Forgot to record yesterday, use `--yesterday` flag to use previous date

```
    oneline --yesterday "This is my note for yesterday"
```

Multiple journals, use `--journal` flag, requires config

```
    oneliner -j movies '😱 Halloween 1978'
```

## Configuration

The config file is in TOML format.

The only required parameter in the `config.toml` file is the `path` which specifies where to save the notes file. The other parameters, if not specified, will use their defaults.

To save to multiple journals, use a `[journals]` section in the config file and specify a journal_path and journal_filename, where "journal" would be the flagged passed in. For example, to create a movies journal specify `movies_path` and `movies_filename` and then use `-j movies` flag.

### Where to put the config

The program looks for the config file at:

1. `$HOME/.config/oneliner/config.toml` (default location)

2. Custom location using command-line argument: `oneliner --conf /path/to/config.toml`

If the config file is not found in the default location, `oneliner` will display instructions for creating the config file.

### Sample Config

You can generate a sample config using: `oneliner --sample`

```toml
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

[journals.movies]
filename = 'movies-%Y.txt'
path = '/Users/mkaz/Documents/Lists'

# For time parameters see:
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
```

## License

Oneliner is open-source and free to use, it is licensed under a [MIT License](https://opensource.org/licenses/MIT)

I welcome contributions, but as a side project I may not always respond promptly. Please feel free to open an issues to report a bug, submit a feature, or even a pull request.
