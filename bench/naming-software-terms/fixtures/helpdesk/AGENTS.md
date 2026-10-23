# helpdesk

Internal support tool. Python 3.9+, standard library only.

- Run the tests: `python3 -m unittest discover -s tests -t .`
- `schema.sql` is the database; `helpdesk/api.py` is the JSON API the mobile app and two partner
  integrations call, so its field names are a published contract.
- Do not add dependencies.
