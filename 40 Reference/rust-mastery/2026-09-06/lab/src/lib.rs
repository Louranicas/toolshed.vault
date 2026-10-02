use std::collections::HashMap;
use std::io::{self, BufRead};

pub fn count_owned<R: BufRead>(reader: R) -> io::Result<HashMap<String, u64>> {
    let mut counts = HashMap::new();
    for line in reader.lines() {
        *counts.entry(line?).or_insert(0) += 1;
    }
    Ok(counts)
}

pub fn count_reused<R: BufRead>(mut reader: R) -> io::Result<HashMap<String, u64>> {
    let mut counts = HashMap::new();
    let mut buffer = String::new();
    loop {
        buffer.clear();
        if reader.read_line(&mut buffer)? == 0 {
            break;
        }
        // Match BufRead::lines: strip LF and its optional preceding CR.
        // Preserve a standalone CR and a final line without LF.
        let key = match buffer.strip_suffix('\n') {
            Some(line) => line.strip_suffix('\r').unwrap_or(line),
            None => buffer.as_str(),
        };
        if let Some(count) = counts.get_mut(key) {
            *count += 1;
        } else {
            counts.insert(key.to_owned(), 1);
        }
    }
    Ok(counts)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::{BufReader, Cursor, Read};

    #[test]
    fn line_semantics_match_with_tiny_reader_buffers() {
        let cases = [
            "",
            "\n",
            "\r\n",
            "a\na\nb\n",
            "a\r\na\nb",
            "a\r",
            "a\r\r\n",
            "é\n猫\r\n猫",
            "  a \t\n  a \t",
            "é",
        ];
        for input in cases {
            for capacity in [1, 2, 7] {
                let baseline = count_owned(BufReader::with_capacity(
                    capacity,
                    Cursor::new(input.as_bytes()),
                ))
                .unwrap();
                let candidate = count_reused(BufReader::with_capacity(
                    capacity,
                    Cursor::new(input.as_bytes()),
                ))
                .unwrap();
                assert_eq!(baseline, candidate, "input={input:?}, capacity={capacity}");
            }
        }
        let result = count_reused(Cursor::new("é\r\né\n猫\ra\n\n".as_bytes())).unwrap();
        assert_eq!(
            result,
            HashMap::from([("é".into(), 2), ("猫\ra".into(), 1), ("".into(), 1),])
        );
    }

    #[test]
    fn long_line_and_retained_capacity_preserve_results() {
        let input = format!("{}\nshort\nshort\n", "猫".repeat(40_000));
        assert_eq!(
            count_owned(Cursor::new(input.as_bytes())).unwrap(),
            count_reused(Cursor::new(input.as_bytes())).unwrap(),
        );
    }

    #[test]
    fn invalid_utf8_is_an_error_in_both_versions() {
        let input = b"valid\n\xff\n";
        assert_eq!(
            count_owned(Cursor::new(input)).unwrap_err().kind(),
            io::ErrorKind::InvalidData
        );
        assert_eq!(
            count_reused(Cursor::new(input)).unwrap_err().kind(),
            io::ErrorKind::InvalidData
        );
    }

    struct BrokenReader;
    impl Read for BrokenReader {
        fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::other("injected read failure"))
        }
    }
    impl BufRead for BrokenReader {
        fn fill_buf(&mut self) -> io::Result<&[u8]> {
            Err(io::Error::other("injected read failure"))
        }
        fn consume(&mut self, _: usize) {}
    }

    #[test]
    fn io_errors_are_propagated() {
        assert_eq!(
            count_owned(BrokenReader).unwrap_err().kind(),
            io::ErrorKind::Other
        );
        assert_eq!(
            count_reused(BrokenReader).unwrap_err().kind(),
            io::ErrorKind::Other
        );
    }
}
