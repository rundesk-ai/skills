# Data

A parcel row holds the recipient's name and home address. That is personal data: it is never
logged, never put in an error message, and never copied into a fixture.

Fees are stored as integers in the currency's minor unit, in `fee_minor`, beside `currency`.

The staging database is shared by the whole team and by the customer's acceptance testers.
