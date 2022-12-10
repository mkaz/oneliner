use serde::Deserialize;
use std::env;
use std::fs;
use std::path::Path;
use toml;

#[derive(Clone, Deserialize)]
pub struct Config {
    pub path: String,
    
    #[serde(default = "default_filename")]
    pub filename: String,
    
    #[serde(default = "default_prefix")]
    pub prefix: String,
}

fn default_filename() -> String {
    "oneliner-%Y.txt".to_string()
}

fn default_prefix() -> String {
    "%Y-%m-%d".to_string()
}

pub fn get_config(filearg: Option<&str>) -> Config {
    let filename = determine_filename(filearg);

    // check filename exists
    let config_path = Path::new(&filename);
    if !config_path.exists() {
        println!("Config file not found. {:?}", config_path);
        // TODO: better error message
        std::process::exit(1);
    }

    // Read and parse config
    let config_file = fs::read_to_string(filename).unwrap();
    return toml::from_str(&config_file).unwrap();
}

// Determine config file:
//   1. command-line parameter
//   2. ONELINER_CONFIG_HOME env variable
//   3. XDG_CONFIG_HOME env variable
//   4. $HOME/.config/oneliner.conf
//   5. Default current dir
fn determine_filename(filearg: Option<&str>) -> String {
    // from command-line
    if let Some(f) = filearg {
        return f.to_string();
    }

    // check environment variable
    if let Ok(val) = env::var("ONELINER_CONFIG_FILE") {
        return val;
    }

    // Linux
    if let Ok(xdg_dir) = env::var("XDG_CONFIG_HOME") {
        let filepath = Path::new(&xdg_dir).join("oneliner.conf");
        if filepath.exists() {
            match filepath.to_str() {
                Some(f) => return f.to_string(),
                None => {}
            };
        }
    }

    // Windows
    if let Ok(appdata) = env::var("APPDATA") {
        let filepath = Path::new(&appdata).join("oneliner.conf");
        if filepath.exists() {
            match filepath.to_str() {
                Some(f) => return f.to_string(),
                None => {}
            };
        } else {
            println!("Filepath does not exist: {:?}", filepath);
        }
    }

    if let Ok(home_dir) = env::var("HOME") {
        let filepath = Path::new(&home_dir).join(".config").join("oneliner.conf");
        if filepath.exists() {
            match filepath.to_str() {
                Some(f) => return f.to_string(),
                None => {}
            };
        }
    }

    // default
    return "oneliner.conf".to_string();
}
