+++
skill = "writing-implementation-plans"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "invoicer"
rubric = """
result.1  Every file path, function and command named exists in the fixture or is explicitly a new file; nothing is invented.
result.2  The approach reuses the existing model, store and id logic, and says so.
result.3  Plans no unrequested abstraction: no scheduler framework, plugin or strategy layer, generic recurrence engine or configuration system; any such option is listed as not built.
result.4  Tasks are ordered, each leaves a working state, and each has a concrete verify step with an expected result.
result.5  Writes no implementation code into the repository; the deliverable is the plan.
conduct.1 Reads the code before planning rather than planning from assumptions.
"""
+++
Write the implementation plan for recurring invoices: an invoice can repeat monthly or yearly, the next one is generated on the right date when we run the tool, and a recurring invoice can be paused. Don't build it yet.
