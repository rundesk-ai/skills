+++
skill = "using-php"
cases_version = 1
kind = "routing"
fixture = "billing"
deploy = ["using-php", "using-laravel"]
expect = "fire"
rubric = "Loads using-php to review plain PHP for loose comparisons and type juggling; using-laravel stays unloaded."
+++
Review the PHP in src/ for loose comparisons and type juggling. Report what you find; do not change
anything yet.
