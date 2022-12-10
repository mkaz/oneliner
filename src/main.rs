// extern crate toml;

use chrono::{DateTime, Duration, Utc};
use clap::{crate_version, Arg, Command};
use std::env;
use std::fs;
use std::io::prelude::*;
use std::path::Path;

mod config;

fn main() {
    let args = Command::new("oneliner")
        .version(crate_version!())
        .about("One line notes on the command-line")
        .author("Marcus Kazmierczak")
        .arg(
            Arg::new("config")
                .help("Configuration file")
                .short('c')
                .long("config")
                .takes_value(true),
        )
        .arg(
            Arg::new("yesterday")
                .help("Set with yesterday's date")
                .short('y')
                .long("yesterday"),
        )
        .arg(
            Arg::new("content")
                .help("Create note from command-line")
                .multiple_values(true),
        )
        .after_help(
            "Create notes:

        oneliner 'This is my note'",
        )
        .get_matches();

    let content: String;

    // read in config
    let config = config::get_config(args.value_of("config"));

    // create filename from config
    let dt: DateTime<Utc> = if args.is_present("yesterday") {
        Utc::now() - Duration::days(1)
    } else {
        Utc::now()
    };

    let notes_path = Path::new(&config.path).to_path_buf();
    let filename = dt.format(&config.filename).to_string();

    if !notes_path.exists() {
        println!("Notes directory not found: {:?}", notes_path);
        println!("To make sure notes are not created in some random spot, the notes directory must already exist. Please create or change path config in oneliner.conf to an existing directory");
        std::process::exit(1);
    }
    let file_path = notes_path.join(filename);

    // get file content from command-line
    match args.values_of("content") {
        Some(msg) => {
            let v: Vec<&str> = msg.collect();
            content = v.join(" ");
        }
        _ => {
            println!("Nothing to write. Try again.");
            std::process::exit(1);
        }
    };

    let mut file = match fs::OpenOptions::new()
        .read(true)
        .append(true)
        .create(true)
        .open(&file_path)
    {
        Ok(file) => file,
        Err(e) => panic!("Error creating file. {}", e),
    };

    // Date prefix
    let prefix = dt.format(&config.prefix).to_string();

    // We want to guarantee a newline but not double up
    // So subsequent notes don't append to same line

    // Strip line ending(s) it'll get added back next
    let content = content.strip_suffix("\n").unwrap_or(&content);

    // Build content with prefix and newline
    let content = prefix + " | " + &content.to_owned() + "\n";

    match file.write_all(content.as_bytes()) {
        Ok(_) => println!("Note added to: {}", file_path.to_str().unwrap()),
        Err(e) => panic!("Error writing to file. {}", e),
    }
}
