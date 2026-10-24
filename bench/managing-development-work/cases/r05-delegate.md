+++
skill = "managing-development-work"
cases_version = 1
kind = "routing"
fixture = "invoicer"
expect = "fire"
rubric = "Loads the skill to split the work across agents and integrate what they return, though the request never says plan, scope or slice."
+++
Get a couple of agents on this in parallel: `show` should print the due date, and `void` should
refuse an invoice that is already paid. Bring it together when they're done.
