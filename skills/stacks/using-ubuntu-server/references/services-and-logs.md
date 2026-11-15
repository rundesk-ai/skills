# Services and logs

## Reading a service

```sh
systemctl status <unit>                    # state, main PID, enabled at boot, last log lines
systemctl cat <unit>                       # the unit file and every drop-in, in load order
systemctl show <unit> -p User,ExecStart,Restart,MemoryMax
journalctl -u <unit> -n 100 --no-pager     # its log; -f to follow, --since "1 hour ago"
journalctl -u <unit> -b -1                 # the previous boot, for "it died overnight"
systemctl list-units --type=service --state=failed
```

`active (running)` means the process exists, not that it works. A worker can be running and stuck,
and a web server can run while every request fails. Prove the service by what it serves.

## Changing a unit

- **Override, don't edit.** `sudo systemctl edit <unit>` writes
  `/etc/systemd/system/<unit>.d/override.conf` and reloads systemd. A list setting such as
  `ExecStart=` is added to, not replaced, so clear it first with an empty `ExecStart=` line.
- **After editing any unit file by hand, run `sudo systemctl daemon-reload`.** Without it systemd
  keeps the old definition and warns that the unit changed on disk.
- `enable` decides boot; `start` decides now. `enable --now` does both. A service that works until
  the first reboot was started and never enabled.
- `mask` blocks every start, manual and dependency included; prefer `disable` unless the person
  wants it impossible to start.
- Restarting a unit others depend on reaches them too: restarting Docker stops every container
  unless `live-restore` is set, and restarting a database drops every connection. Read
  `systemctl list-dependencies --reverse <unit>` before restarting a shared one.

## A unit for an app or worker

```ini
# /etc/systemd/system/app-worker.service
[Unit]
Description=App queue worker
After=network-online.target mysql.service
Wants=network-online.target

[Service]
User=deploy
Group=deploy
WorkingDirectory=/srv/app/current
EnvironmentFile=/srv/app/shared/.env
ExecStart=/usr/bin/php artisan queue:work --sleep=3 --tries=3 --max-time=3600
Restart=always
RestartSec=5
KillSignal=SIGTERM
TimeoutStopSec=120

[Install]
WantedBy=multi-user.target
```

- Run as a dedicated user, never root. A web app writing as root leaves files the web user cannot
  write, and the next request fails.
- `TimeoutStopSec` longer than the longest job, so a deploy's restart lets a job finish instead of
  killing it half way.
- A worker loads the code once. After a deploy it runs the old code until restarted, so the deploy
  restarts it, or the framework's own signal does (`queue:restart`, `horizon:terminate`).
- `Restart=always` turns a crash at start into a restart loop that can look like `activating` or
  `active` between crashes. Read the journal, not just the state.

**Supervisor** (`/etc/supervisor/conf.d/*.conf`) is still common for PHP queue workers. After a
change: `sudo supervisorctl reread && sudo supervisorctl update`, then `supervisorctl status`.
`supervisorctl restart all` restarts every program on the box, not only yours.

**pm2** keeps a process list per user. Run it as the app's user (`sudo -iu deploy pm2 ls`), not as
root, or you start a second, empty pm2 daemon. `pm2 save` after a change, or the list is lost at
reboot; `pm2 reload` restarts cluster-mode apps one at a time, `restart` all at once.

## Scheduled jobs

| Choose | When |
|---|---|
| a systemd timer | a new job: logs in the journal, no overlap by default, `Persistent=true` catches a missed run, `systemctl list-timers` shows the next run |
| `/etc/cron.d/<name>` | the project already uses cron; one file per job set, with the user field |
| `crontab -e -u <user>` | a framework's single scheduler line, such as `* * * * * cd /srv/app/current && php artisan schedule:run` |

Cron traps: a job runs with a minimal `PATH` and no profile, so use full paths; an unescaped `%`
becomes a newline, so write `\%`; a line without a trailing newline is not run; a file in
`/etc/cron.d/` needs the user field, and Debian's `cron` skips a file whose name has a dot, so name
it with letters, digits, `-` and `_` only; output goes to local mail, so redirect it to a log. Cron
uses the server's timezone (`timedatectl`).

## Logs and disk

- The journal keeps up to 10% of the filesystem, capped at 4G, by default. Free space with
  `sudo journalctl --vacuum-size=500M`; set a lasting limit with `SystemMaxUse=` in a drop-in under
  `/etc/systemd/journald.conf.d/`.
- An application log that grows forever needs a `/etc/logrotate.d/<app>` entry. Use
  `copytruncate`, or a `postrotate` that tells the app to reopen its file, or the app keeps writing to
  the rotated, deleted file and the space never comes back. Test with `sudo logrotate -d
  /etc/logrotate.d/<app>`.
- `sudo journalctl -k` is the kernel's log: OOM kills, disk errors, network link changes.
