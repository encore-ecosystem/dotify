use anyhow::Result;
mod args;
mod commands;
mod dotconfig;
use clap::Parser;

fn main() -> Result<()> {
    // Read config
    let config = dotconfig::DotifyConfig::load()?;

    // Load plguins
    for plugin in config.include_plugins.iter() {
        println!("Plugin: {plugin}")
    }

    // Parse cli arguments
    let cli = args::Cli::parse();

    if cli.verbose {
        println!("Verbose mode enabled");
    }

    match cli.command {
        args::Commands::Init { name, force } => {
            commands::cmd_init()?;
        }
        args::Commands::Apply { dry_run } => {
            commands::cmd_apply()?;
        }
    }

    Ok(())
}
