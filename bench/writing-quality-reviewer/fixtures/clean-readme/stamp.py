"""stamp: add or update a "Last reviewed" date in Markdown front matter."""
import argparse
import datetime
import pathlib
import re
import sys

FIELD = re.compile(r"^last_reviewed: .*$", re.M)


def stamp(path, day, check):
    text = path.read_text()
    if not text.startswith("---\n"):
        print(f"{path}: no front matter, skipped", file=sys.stderr)
        return False
    end = text.index("\n---\n", 4)
    front, body = text[4:end], text[end:]
    line = f"last_reviewed: {day}"
    new_front = FIELD.sub(line, front) if FIELD.search(front) else front + "\n" + line
    if new_front == front:
        return False
    if not check:
        path.write_text("---\n" + new_front + body)
    print(path)
    return True


def main():
    p = argparse.ArgumentParser(prog="stamp")
    p.add_argument("paths", nargs="+", type=pathlib.Path)
    p.add_argument("--date", help="YYYY-MM-DD; default today")
    p.add_argument("--check", action="store_true", help="print what would change, write nothing, exit 1 if anything would")
    a = p.parse_args()
    day = a.date or datetime.date.today().isoformat()
    changed = [x for x in a.paths if stamp(x, day, a.check)]
    sys.exit(1 if a.check and changed else 0)


if __name__ == "__main__":
    main()
