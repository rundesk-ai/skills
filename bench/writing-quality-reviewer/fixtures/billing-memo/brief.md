Brief from the VP of Engineering: "I need a recommendation by Friday: do we move the billing service off the shared Postgres cluster this quarter, or wait until next quarter? Write me one page."

Facts gathered for the memo:
- Billing runs on the shared cluster with 14 other services.
- In October, two incidents on the shared cluster (a runaway report query from the analytics service) caused billing to time out, once for 38 minutes and once for 52.
- Moving billing to its own cluster: estimated 3 engineer-weeks, plus about 900 USD/month in hosting.
- The billing team has 4 engineers. This quarter's roadmap commits them to the tax-rules project, estimated at 6 of the quarter's 12 weeks.
- Invoices fail to send when billing times out; finance re-sends them by hand.
