+++
skill = "using-ubuntu-server"
cases_version = 1
kind = "routing"
fixture = ""
expect = "fire"
rubric = "Loads the skill before diagnosing."
+++
Our queue worker box keeps "losing" the worker overnight. In the morning supervisorctl says it's
running but jobs pile up, and last week the whole MySQL process just disappeared at 3am with nothing
in its own error log. Where do I even look?
