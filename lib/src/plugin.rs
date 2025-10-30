use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Plugin {
    name: String,
    hooks: Vec<Hook>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Hook {
    name: String,
    args: Vec<String>,
    command: String,
}
