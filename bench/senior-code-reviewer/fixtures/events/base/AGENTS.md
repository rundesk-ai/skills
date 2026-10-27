# AGENTS

`events` is the calendar store behind a community centre's booking app. Python 3.9+, standard
library only. `data/events.json` holds every booking the centre has taken, going back years.

## Rules

- **Existing bookings must keep loading** after any change; there is no other copy.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
