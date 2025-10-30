use anyhow::{Ok, Result};
use serde::{Deserialize, Serialize};
use std::default::Default;
use std::fs;
use std::path::PathBuf;
use std::{env, fmt::Debug};

#[derive(Debug, Serialize, Deserialize, Default)]
pub struct ProjectManifest {
    pub config: Config,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub name: String,
    pub description: String,
    pub version: String,
    pub authors: Vec<String>,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            name: "project".to_string(),
            description: "".to_string(),
            version: "0.0.1".to_string(),
            authors: vec!["".to_string()],
        }
    }
}

impl ProjectManifest {
    pub fn load(project_root: PathBuf) -> Result<Self> {
        let path = project_root.join("dotify.toml");
        if path.exists() {
            let content = fs::read_to_string(path)?;
            let config: Self = toml::from_str(&content)?;
            Ok(config)
        } else {
            Ok(Self::default())
        }
    }

    pub fn save(&self, project_root: PathBuf) -> Result<()> {
        let path = project_root.join("dotify.toml");
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)?;
        }
        let toml = toml::to_string_pretty(self)?;
        fs::write(path, toml)?;
        Ok(())
    }

    pub fn exists(project_root: &PathBuf) -> bool {
        project_root.join("dotify.toml").exists()
    }
}

pub fn cmd_init() -> Result<()> {
    let project_root = env::current_dir().unwrap();

    if ProjectManifest::exists(&project_root) {
        println!("Project already initialized! Found 'dotify.toml' in current directory.");
        return Ok(());
    }

    let mut manifest = ProjectManifest::default();
    manifest.config.name = project_root
        .file_name()
        .unwrap()
        .to_str()
        .unwrap()
        .to_string();

    match manifest.save(project_root) {
        Result::Ok(_) => {
            println!("Project initialized!");
        }
        Result::Err(e) => {
            println!("Error in manifest saving: {e}");
        }
    }
    Ok(())
}

pub fn cmd_apply() -> Result<()> {
    let project_root = env::current_dir().unwrap();
    if !ProjectManifest::exists(&project_root) {
        println!("[ERROR]: Project is not initialized!")
    }

    let manifest = ProjectManifest::load(project_root);

    Ok(())
}
