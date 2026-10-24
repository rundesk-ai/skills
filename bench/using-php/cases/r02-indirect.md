+++
skill = "using-php"
cases_version = 1
kind = "routing"
fixture = "billing"
deploy = ["using-php", "using-laravel"]
expect = "fire"
rubric = "Loads using-php though the request never names the language: the work is the runtime's version upgrade."
+++
Production moves to the newest runtime release next month. Check whether anything in this project
will break or start emitting deprecation notices, and tell me what you find.
