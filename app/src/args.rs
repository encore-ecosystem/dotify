use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "dotify")]
#[command(about = "A dotfile management tool", version)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,

    #[arg(short, long, global = true)]
    pub verbose: bool,
}

#[derive(Subcommand)]
pub enum Commands {
    Init {
        #[arg(long)]
        name: Option<String>,

        #[arg(short, long)]
        force: bool,
    },
    Apply {
        #[arg(short, long)]
        dry_run: bool,
    },
}
