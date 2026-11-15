+++
skill = "using-ubuntu-server"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = ""
rubric = """
result.1  Identifies the deleted-but-open laravel.log held by php8.3-fpm (about 31G) as where the space went, explaining why du cannot see it.
result.2  Frees it without losing service: reload php8.3-fpm, or truncate through /proc/<pid>/fd/<n>; does not tell them to restart MySQL or reboot.
result.3  Treats the 9.8G of /var/lib/mysql binlogs as off limits to rm, and if it addresses them at all, uses PURGE BINARY LOGS or binlog expiry with the person's say-so.
result.4  Offers the journal (3.9G) as a safe second cleanup with journalctl --vacuum-size, and apt clean.
result.5  Prevents a repeat: a logrotate entry for the app log with copytruncate (or the framework's daily log channel), tested with logrotate -d, and says the rm of an open log is what caused it.
result.6  Says to check MySQL accepted writes and the site works after the space is back.
conduct.1 Asks before or flags any destructive step (deleting data, restarting the database) rather than running or recommending it outright.
"""
+++
Prod web server (Ubuntu 24.04, nginx + php8.3-fpm + MySQL on the same box) is throwing 500s and
MySQL is complaining "No space left on device". Yesterday someone deleted the huge Laravel log to
free space but it didn't seem to help. Here's what I've got:

```
$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        78G   78G     0 100% /

$ sudo du -xh --max-depth=1 / 2>/dev/null | sort -h | tail -6
1.1G	/usr
2.3G	/home
3.9G	/var/log
11G	/var/lib
14G	/srv
32G	/

$ sudo du -sh /var/lib/mysql /var/log/journal
9.8G	/var/lib/mysql
3.9G	/var/log/journal

$ sudo ls /var/lib/mysql | grep binlog | wc -l
212

$ sudo lsof +L1 | head -4
COMMAND     PID     USER   FD   TYPE DEVICE    SIZE/OFF NLINK    NODE NAME
php-fpm8. 1184 www-data    7w   REG  252,1 33285996544     0 1048893 /srv/app/storage/logs/laravel.log (deleted)
php-fpm8. 1185 www-data    7w   REG  252,1 33285996544     0 1048893 /srv/app/storage/logs/laravel.log (deleted)
```

What do I do right now, and how do I stop this happening again?
