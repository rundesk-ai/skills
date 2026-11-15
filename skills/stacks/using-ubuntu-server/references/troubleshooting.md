# Troubleshooting a live server

Gather before you fix: a restart destroys the evidence (the stuck process, the full queue, the log
in memory) and often brings the fault back an hour later. Note what you saw, then change one thing.

## The site is down

1. From outside: `curl -sv https://<host>/ -o /dev/null` — DNS, connection refused, TLS error, or an
   HTTP status each points somewhere different.
2. On the server: `systemctl status nginx php<v>-fpm`, `ss -tlnp | grep -e :80 -e :443`.
3. The web server's error log (`/var/log/nginx/error.log`) names the next hop: `connect() to
   unix:/run/php/php8.3-fpm.sock failed` is PHP-FPM down or a socket path for the wrong version;
   `upstream timed out` is a slow app or exhausted workers; `Permission denied` is file ownership.
4. The app's own log, then its dependencies: database, Redis, disk.
5. `502` with PHP-FPM up usually means every worker is busy: the FPM log says `server reached
   pm.max_children`. Raising `pm.max_children` needs the memory for it (each worker's RSS times the
   count), or the server swaps and gets slower.

6. **On a container host,** start at the proxy container's logs, then the app container's
   (`docker logs --tail 100 <container>`); `docker ps` shows a container restarting in a loop as
   `Restarting` or a recent `Up` time.

## 413, 504 and permission errors

- **413 Request Entity Too Large** on an upload: nginx's `client_max_body_size` (default 1m) is
  below the file. Raise it in the site's `server` block, and raise PHP's `upload_max_filesize` and
  `post_max_size` in the FPM `php.ini` to match, since each layer rejects on its own. Validate,
  then reload nginx and PHP-FPM.
- **504 Gateway Timeout** on a long request: nginx gave up first (`fastcgi_read_timeout` or
  `proxy_read_timeout`, default 60s). Raising it only helps when PHP's `max_execution_time` and the
  pool's `request_terminate_timeout` allow as long; a request that needs minutes belongs in a queue.
- **Permission denied writing files** (an app's storage, cache or uploads): the web user
  (`www-data` for nginx and PHP-FPM) cannot write where the deploy user, or root, created the
  files. `namei -l <path>` shows every directory's owner and mode on the way. Make the deploy user
  and `www-data` share a group, give the writable directories to that group with group write and
  the setgid bit (`chmod 2775`), and never fix it with `chmod 777` or by running the app as root.

## SSH refuses a key

`Permission denied (publickey)`: read the server's side with `sudo journalctl -u ssh -n 50
--no-pager`, and the client's with `ssh -v`. The usual causes: the key is in another user's
`authorized_keys`; `~/.ssh` or the file is writable by others; `AllowUsers` or `AllowGroups` in a
drop-in excludes the user; or the client offers an old key type the server no longer accepts
(`ssh-rsa` with SHA-1 is off since OpenSSH 8.8, DSA is gone in 10). Fix it from the session you
still have, and test from a new one.

## Disk full

```sh
df -h; df -i
sudo du -xh --max-depth=1 / 2>/dev/null | sort -h | tail
sudo lsof +L1                          # deleted files still held open, and by which process
journalctl --disk-usage
```

- Space `du` cannot find is usually a deleted file still open: a log removed with `rm` while the
  process writes on. Reload that service, or truncate it in place with `sudo truncate -s 0
  /proc/<pid>/fd/<n>`.
- **Safe to clear:** `sudo journalctl --vacuum-size=500M`, `sudo apt clean`, rotated `*.gz` logs the
  person does not need, old releases a deploy tool keeps.
- **Never delete by hand:** anything in `/var/lib/mysql`, `/var/lib/postgresql` (including `pg_wal`)
  or `/var/lib/docker`; MySQL binary logs (use `PURGE BINARY LOGS`); files in `/boot` (use `apt
  autoremove` for old kernels). Removing them corrupts the service that owns them.
- `docker system df` shows what Docker holds; `docker system prune` deletes stopped containers and
  unused images, and `--volumes` deletes data. Show the person what it will remove first.
- On a Docker host, container logs without `log-opts` limits in `/etc/docker/daemon.json` are the
  usual culprit: `sudo du -sh /var/lib/docker/containers/*/*-json.log`. Old images are next
  (`docker system df` shows what is reclaimable).
- A database stops writing, and may stop, when its disk fills. After freeing space, check its log
  and that it accepts writes.

## Memory and load

```sh
free -h; swapon --show
ps aux --sort=-%mem | head; ps aux --sort=-%cpu | head
journalctl -k | grep -i -e "out of memory" -e "killed process"
uptime; vmstat 1 5                      # load, run queue, swapping (si/so), I/O wait (wa)
```

- Load average counts processes waiting on disk as well as CPU. High load with idle CPU and high
  `wa` is I/O: a full disk, a backup, a database without an index. `iotop` (when installed) names
  the process.
- The OOM killer picks the largest process, often the database. Find what grew, cap it (PHP-FPM
  `pm.max_children`, worker counts, `MemoryMax=` in the unit), and add swap so a spike slows the
  server instead of killing it:

  ```sh
  sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
  sudo mkswap /swapfile && sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  ```

  Check `/etc/fstab` with `sudo findmnt --verify` after editing it; a bad line can stop the next
  boot.

## TLS certificates

```sh
sudo certbot certificates                       # each certificate, its domains and expiry
systemctl list-timers | grep -i certbot         # renewal is scheduled
sudo certbot renew --dry-run                    # renewal works, without changing anything
echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | openssl x509 -noout -dates
```

A renewal that fails usually cannot answer the HTTP challenge: port 80 closed in the firewall, an
nginx redirect or `deny` on `/.well-known/acme-challenge/`, or DNS no longer pointing at this
server. A renewed certificate is used only after nginx reloads; certbot's nginx plugin does that,
a `certonly` setup needs a deploy hook.

## Time and clocks

`timedatectl` shows whether the clock is synchronized. A clock that drifts breaks TLS, signed
tokens, two-factor codes and replication. On 26.04 fresh installs check `chronyc tracking`; before
it, `timedatectl timesync-status`.
