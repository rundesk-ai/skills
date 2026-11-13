+++
skill = "using-django"
cases_version = 1
kind = "routing"
fixture = "bookings"
expect = "fire"
rubric = "Loads the skill even though the request never names Django."
+++
Since we went live, the links in our API's pagination ("next") come back as http:// even though the
site is only served over https. Figure out why and fix it.
