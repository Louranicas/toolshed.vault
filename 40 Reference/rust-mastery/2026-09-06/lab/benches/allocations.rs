use criterion::{BenchmarkId, Criterion, Throughput, criterion_group, criterion_main};
use rust_mastery_lab::{count_owned, count_reused};
use std::hint::black_box;
use std::io::Cursor;

fn allocations(c: &mut Criterion) {
    let mut group = c.benchmark_group("line_counts");
    for n in [100, 10_000] {
        for kind in ["repeated", "unique"] {
            let input = match kind {
                "repeated" => "same value\n".repeat(n),
                _ => (0..n)
                    .map(|i| format!("value-{i:08}\n"))
                    .collect::<String>(),
            };
            // Validate complete results outside the timed region.
            assert_eq!(
                count_owned(Cursor::new(input.as_bytes())).unwrap(),
                count_reused(Cursor::new(input.as_bytes())).unwrap(),
            );
            group.throughput(Throughput::Bytes(input.len() as u64));
            group.bench_with_input(
                BenchmarkId::new(format!("owned/{kind}"), n),
                &input,
                |b, input| {
                    b.iter(|| {
                        black_box(count_owned(Cursor::new(black_box(input.as_bytes()))).unwrap())
                    })
                },
            );
            group.bench_with_input(
                BenchmarkId::new(format!("reused/{kind}"), n),
                &input,
                |b, input| {
                    b.iter(|| {
                        black_box(count_reused(Cursor::new(black_box(input.as_bytes()))).unwrap())
                    })
                },
            );
        }
    }
    group.finish();
}

criterion_group!(benches, allocations);
criterion_main!(benches);
