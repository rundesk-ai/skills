# tally

Count lines, words and bytes in files.

```sh
tally notes.txt            # 12  85  530  notes.txt
tally --json notes.txt     # [{"file":"notes.txt","lines":12,"words":85,"bytes":530}]
```

The JSON output is parsed by other people's scripts: its keys and their order do not change within
a major version.

## Develop

```sh
npm test
npm run lint
```

Releases are cut by the maintainer with `npm run release`.
