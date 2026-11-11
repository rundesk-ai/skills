"""Strip trailing whitespace and make every file end with one newline.

    python3 tools/fmt.py --check DIR...   report files that would change; exit 1 if any
    python3 tools/fmt.py --write DIR...   rewrite them in place
"""
import os
import sys


def formatted(text):
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) < 2 or argv[0] not in ("--check", "--write"):
        sys.exit(__doc__)
    changed = []
    for top in argv[1:]:
        for dirpath, _, names in os.walk(top):
            for name in names:
                if not name.endswith((".py", ".html", ".sql")):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8") as f:
                    text = f.read()
                if formatted(text) != text:
                    changed.append(path)
                    if argv[0] == "--write":
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(formatted(text))
    for path in changed:
        print(("rewrote " if argv[0] == "--write" else "would rewrite ") + path)
    sys.exit(1 if changed and argv[0] == "--check" else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
