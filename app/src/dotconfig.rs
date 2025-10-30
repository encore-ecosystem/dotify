use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize)]
pub struct DotifyConfig {
    pub include_plugins: Vec<String>,
}

impl Default for DotifyConfig {
    fn default() -> Self {
        Self {
            include_plugins: vec!["git".to_string(), "yay".to_string()],
        }
    }
}

impl DotifyConfig {
    pub fn config_path() -> PathBuf {
        let home = std::env::var("HOME").expect("HOME not set");
        PathBuf::from(home)
            .join(".config")
            .join("dotify")
            .join("config.toml")
    }

    pub fn load() -> Result<Self> {
        let path = Self::config_path();
        if path.exists() {
            let content = fs::read_to_string(path)?;
            let config: DotifyConfig = toml::from_str(&content)?;
            Ok(config)
        } else {
            Ok(Self::default())
        }
    }

    pub fn save(&self) -> Result<()> {
        let path = Self::config_path();
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)?;
        }
        let toml = toml::to_string_pretty(self)?;
        fs::write(path, toml)?;
        Ok(())
    }
}
