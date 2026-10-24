+++
skill = "using-php"
cases_version = 1
kind = "routing"
fixture = "shop-laravel"
deploy = ["using-php", "using-laravel"]
expect = "no-fire"
rubric = "Leaves using-php unloaded: authorization policies and eager loading are Laravel framework work, which using-laravel owns."
+++
Only the customer an invoice belongs to should be able to open it, and the invoice index is slow
because of the line totals. Fix both.
