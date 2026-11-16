import argparse


def main():
    p = argparse.ArgumentParser(prog="syncr", description="Copy changed files to a remote bucket.")
    p.add_argument("source")
    p.add_argument("bucket")
    p.add_argument("--dry-run", action="store_true", help="list what would be copied, copy nothing")
    p.add_argument("--retries", type=int, default=5)
    p.add_argument("--exclude", action="append", default=[], help="glob to skip; repeatable")
    p.parse_args()
    # Deletes in the bucket are never performed; syncr only adds and overwrites.


if __name__ == "__main__":
    main()
