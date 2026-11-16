# Billing and the shared Postgres cluster

The billing service has shared a Postgres cluster with fourteen other services since it launched. That arrangement made sense when billing was small, and for a long time it caused no trouble.

October changed that. Twice, a runaway report query from the analytics service saturated the cluster, and billing timed out for 38 minutes the first time and 52 minutes the second. When billing times out, invoices fail to send, and someone in finance re-sends them by hand.

Giving billing its own cluster would take about three engineer-weeks. Hosting would add roughly 900 USD a month. The work itself is well understood: our platform team has moved two services this way before.

The billing team has four engineers. This quarter they are committed to the tax-rules project, which will take about six of their twelve weeks.

Waiting until next quarter has its own shape. The team would finish tax rules first, and the analytics team could add query limits in the meantime, which would make a repeat of October less likely without moving anything.

Both paths are reasonable. Each trades engineering time against the risk of another outage, and the right balance depends on how the organization weighs those.
