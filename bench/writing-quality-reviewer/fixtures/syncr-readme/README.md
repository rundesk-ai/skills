# syncr

syncr is a powerful, seamless solution for file synchronization that leverages a robust architecture to deliver reliable transfers.

## Overview

In this section, we'll explore the various capabilities of syncr. It's worth noting that syncr was originally built for the v2 path, which informs many of its design decisions.

## Options

- `--preview`: shows what would be copied without copying anything.
- `--retries N`: number of retry attempts (default: 3).
- `--exclude GLOB`: skip files matching the glob.
- `--delete`: remove files from the bucket that no longer exist locally.

## Usage

The synchronization process is initiated by running syncr with a source directory and bucket name. Upload operations are then performed for changed files.

    syncr ./site s3://example-bucket

Simply run the command and everything will just work!
