# Dates

Read this before parsing, storing or doing arithmetic on a date or time. Type dates as
`DateTimeImmutable`: `DateTime` methods change the object every variable holding it shares.

## Month arithmetic overflows

`'+1 month'` lets the day spill over, so 31 March becomes 1 May, and `'-1 month'` from 31 March is
3 March. For "same day next month, or the last day when the month is shorter", clamp it yourself, and
keep the original day so a monthly date anchored on the 31st returns to the 31st after February:

```php
function addMonthsClamped(DateTimeImmutable $anchor, int $months): DateTimeImmutable
{
    $first = $anchor->modify('first day of this month')->modify("+{$months} months");
    $day = min((int) $anchor->format('j'), (int) $first->format('t'));
    return $first->setDate((int) $first->format('Y'), (int) $first->format('n'), $day);
}
// anchor 2026-01-31: +1 -> 2026-02-28, +2 -> 2026-03-31, +3 -> 2026-04-30
```

Compute each renewal from the anchor and a count, not from the previous renewal: chaining from 28
February gives 28 March forever.

## Parsing accepts nonsense

- `DateTimeImmutable::createFromFormat('Y-m-d', '2026-05-01')` fills the missing time fields from the
  current time, so two parses of the same string differ. Prefix the format with `!` (or end it with `|`)
  to zero them.
- An impossible date rolls over instead of failing: `2026-02-30` becomes 2 March, with only a warning in
  `DateTimeImmutable::getLastErrors()`. Reject it by checking those errors, or by formatting the result
  and comparing it with the input.
- Bad input gives `false` from `createFromFormat` and `strtotime`, and the constructor throws
  (`DateMalformedStringException` from 8.3). A `false` passed on becomes a `TypeError` far from the
  cause.
- A string with an offset (`+02:00`) or `@timestamp` ignores the default time zone.

## Time zones and daylight saving

There is no warning when no zone is configured: the default is UTC, and `date()` and `new DateTime()`
use whatever `date.timezone` or `date_default_timezone_set()` says on that machine, which can differ
between the command line and the web server.

Relative `modify()` with hours or seconds is wrong across a daylight-saving change. In
`America/New_York` on 8 March 2026, from 01:30, `modify('+24 hours')` lands 23 elapsed hours later, and
`'+2 hours'` lands one hour later. `add(new DateInterval('PT24H'))` and timestamp arithmetic give the
real 24 hours:

```php
$start = new DateTimeImmutable('2026-03-08 01:30', new DateTimeZone('America/New_York'));
echo ($start->modify('+24 hours')->getTimestamp() - $start->getTimestamp()) / 3600; // 23
echo ($start->add(new DateInterval('PT24H'))->getTimestamp() - $start->getTimestamp()) / 3600; // 24
```

Decide whether the rule is elapsed time (use an interval or timestamps) or wall-clock time (use calendar
units such as `+1 day`), and test it on a transition date in a named zone. `diff()` across that day
reports one day for 23 real hours.

ISO week numbers need the ISO year: `'o-W'`, not `'Y-W'` (30 December 2024 is week 1 of 2025).
