use clap::Parser;

/// A simple CLI program
#[derive(Parser)]
#[command(name = "dotify")]
#[command(about = "A simple file processor", long_about = None)]
struct Cli {
    /// Input file to process
    input: String,

    /// Output file, stdout if not present
    output: Option<String>,

    /// Verbose mode
    #[arg(short, long)]
    verbose: bool,

    /// Number of jobs to run in parallel
    #[arg(short, long, default_value_t = 1)]
    jobs: usize,
}

fn main() {
    let cli = Cli::parse();

    println!("Input file: {}", cli.input);

    if let Some(output) = cli.output {
        println!("Output file: {}", output);
    }

    if cli.verbose {
        println!("Verbose mode enabled");
    }

    println!("Jobs: {}", cli.jobs);
}
