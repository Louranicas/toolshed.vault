use rust_mastery_lab::{count_owned, count_reused};
use std::fs::File;
use std::io::{self, BufReader};

#[cfg(feature = "dhat-heap")]
#[global_allocator]
static ALLOC: dhat::Alloc = dhat::Alloc;

fn main() -> io::Result<()> {
    #[cfg(feature = "dhat-heap")]
    let _profiler = dhat::Profiler::new_heap();

    let args: Vec<_> = std::env::args().collect();
    if args.len() != 3 {
        return Err(io::Error::other(
            "usage: rust-mastery-lab owned|reused INPUT",
        ));
    }
    let reader = BufReader::new(File::open(&args[2])?);
    let counts = match args[1].as_str() {
        "owned" => count_owned(reader)?,
        "reused" => count_reused(reader)?,
        _ => return Err(io::Error::other("mode must be owned or reused")),
    };
    let total: u64 = counts.values().sum();
    println!("lines={total} distinct={}", counts.len());
    Ok(())
}
