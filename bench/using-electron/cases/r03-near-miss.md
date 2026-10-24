+++
skill = "using-electron"
cases_version = 1
kind = "routing"
fixture = "csvtotal"
expect = "no-fire"
rubric = "Fixes the string concatenation bug in the plain Node CLI without loading the Electron skill."
+++
`npm test` fails: csvtotal returns "01032" instead of 42 for a two-row file. Fix it.
