# Decisions

## Two amount parsers

`ledger.importer.parse_amount` and `ledger.cli.parse_amount` look alike but are kept separate on
purpose. The CSV export from the old system writes amounts as `1234.56` with a dot always; the CLI
accepts what people type, including `1.234,56` from the firm's German office. Merging them broke
imports once (an export amount of `1,000` was read as one euro). Do not merge them.
