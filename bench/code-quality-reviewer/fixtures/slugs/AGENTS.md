# AGENTS

`slugs` turns article titles into URL slugs for the publishing pipeline. Python 3.9+, standard
library only. It is finished: it has changed twice in three years, and every published URL depends
on its output staying exactly the same.

## Rules

- **Output never changes for an input that already works.** Published URLs are permanent.
- **ASCII only, by decision.** Letters outside ASCII are dropped, not transliterated: the editors
  write the slug by hand for those titles.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
