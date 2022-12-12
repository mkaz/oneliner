# oneliner

A simple command-line tool for saving one line notes in plain text files.

## Example

![Demo GIF](https://user-images.githubusercontent.com/45363/206862140-a7fc3b36-a23e-40ea-8a0f-acfcc5636ecd.gif)

Use `oneliner` by adding note on the command-line

```
$ oneliner "Here is my note"
```

## Install

1.  a) Build from source, requires rust toolchain

    b) Download from [GitHub releases](https://github.com/mkaz/oneliner/releases)

    -   The binaries aren't signed, so Mac users will need to jump through [their hoops](https://support.apple.com/en-us/HT202491)

2.  Create oneliner.conf, see [Configuration below](#configuration)

## Usage

See `oneliner --help` for help.

## Configuration

The only required parameter in the `oneliner.conf` config is the `path` which specifies where to save the notes file. The other parameters, if not specified, will use their defaults.

You can generate a sample config using: `oneliner --gen-config`

The program looks for the config file using the following:

1. Command-line argument. Use `oneliner --config /path/to/oneliner.conf`

2. Environment variable: `ONELINER_CONFIG_FILE`

3. Look for platform config directory

    a. Linux: `${XDG_CONFIG_HOME}/oneliner.conf`

    b. Windows: `${APPDATA}/oneliner.conf`

4. Look for `${HOME}/.config/oneliner.conf`

5. Current directions `./oneliner.conf`

If not specified or found in any of the above locations, `oneliner` will error out with a message to set the configuration file.

### Sample Config

The config file is in TOML format, example:

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

# [journals]
# movies_filename = 'movies-%Y.txt'
# movies_path = '/Users/mkaz/Documents/Lists'

# For time parameters see:
# https://docs.rs/chrono/0.4.0/chrono/format/strftime/index.html
```

## License

Oneliner is open-source and free to use, it is licensed under a [MIT License](https://opensource.org/licenses/MIT)

I welcome contributions, but as a side project I may not always respond promptly. Please feel free to open an issues to report a bug, submit a feature, or even a pull request.
