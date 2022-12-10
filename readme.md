# oneliner

A simple command-line tool for saving one line notes in plain text files.

## Install

1. Build from source.

2. Create oneliner.conf, see [Configuration below](#configuration)

    - `default_path` is only required config

## Usage

See `oneliner --help` for help.

### Add note

Use `oneliner` with note as the command-line argument

```
$ oneliner "Here is my note"
```

## Configuration

You need to set the `default_path` in the `oneliner.conf` config file.

The config file location can be specified various ways, `oneliner` will look in the following order to determine where the config file is:

1. Command-line argument. Use `oneliner --config /path/to/oneliner.conf`

2. Environment variable: `ONELINER_CONFIG_FILE`

3. Look for platform config directory

    a. Linux: `${XDG_CONFIG_HOME}/oneliner.conf`

    b. Windows: `${APPDATA}/oneliner.conf`

4. Look for `${HOME}/.config/oneliner.conf`

If not specified or found in any of the above locations, `oneliner` will error out with a message to set the configuration file.

The config file is in TOML format, example:

```toml

# oneliner config file

# Base directory that all notes are stored
# Use full path for directory
path = '/Users/mkaz/Documents/'

# Default filename
filename = 'oneliner-%Y.txt'

# Format for data prefix before each line
# 2022-12-01 | YOUR NOTE HERE
prefix = '%Y-%m-%d'


# For time parameters see:
# https://docs.rs/chrono/0.4.0/chrono/format/strftime/index.html
```


## License

Oneliner is open-source and free to use, it is licensed under a [MIT License](https://opensource.org/licenses/MIT)

I welcome contributions, but as a side project I may not always respond promptly. Please feel free to open an issues to report a bug, submit a feature, or even a pull request.
