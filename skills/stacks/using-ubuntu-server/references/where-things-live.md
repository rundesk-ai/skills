# Where things live

The usual places on Ubuntu 22.04, 24.04 and 26.04 with packages from the Ubuntu archive. A panel,
an image or a deploy script can move any of them, so confirm with the commands at the end before
you edit.

## The system

| What | Where |
|---|---|
| Release | `/etc/os-release`, `lsb_release -a` |
| Package sources | `/etc/apt/sources.list.d/ubuntu.sources` (deb822, 24.04+); `/etc/apt/sources.list` before 24.04; third-party repos beside it in `sources.list.d/` |
| Repository keys | `/etc/apt/keyrings/` or `/usr/share/keyrings/`, named by a source's `Signed-By` |
| Package history | `/var/log/apt/history.log` (what was run), `/var/log/apt/term.log`, `/var/log/dpkg.log`; on 26.04 also `apt history-list` |
| Automatic updates | `/etc/apt/apt.conf.d/50unattended-upgrades`, `20auto-upgrades`; logs in `/var/log/unattended-upgrades/` |
| Service restarts after upgrades | `/etc/needrestart/needrestart.conf`, `/etc/needrestart/conf.d/` |
| systemd units | vendor units in `/usr/lib/systemd/system/` (never edit); yours and overrides in `/etc/systemd/system/`, drop-ins in `/etc/systemd/system/<unit>.d/` |
| Timers and cron | `systemctl list-timers`; `/etc/crontab`, `/etc/cron.d/`, `/etc/cron.{daily,weekly}/`, per-user `crontab -l -u <user>` (stored in `/var/spool/cron/crontabs/`) |
| Logs | `journalctl` (persistent in `/var/log/journal/`); classic files in `/var/log/` (`syslog`, `auth.log`, `kern.log`); rotation in `/etc/logrotate.d/` |
| Network | `/etc/netplan/*.yaml` (`50-cloud-init.yaml` is cloud-init's); runtime `ip a`, `ip r` |
| DNS | `resolvectl status`; `/etc/resolv.conf` is a link to systemd-resolved's stub (`127.0.0.53`), not a file to edit; `/etc/hosts` |
| Hostname and time | `hostnamectl`, `timedatectl`; chrony on fresh 26.04 installs (`/etc/chrony/`), systemd-timesyncd before |
| Kernel parameters | `/etc/sysctl.d/*.conf`; kernel boot line in `/etc/default/grub` then `update-grub` |
| cloud-init | `/etc/cloud/cloud.cfg`, `/etc/cloud/cloud.cfg.d/`; what it did in `/var/log/cloud-init.log` |
| Users and sudo | `/etc/passwd`, `/etc/group`, `/etc/sudoers`, `/etc/sudoers.d/`; keys in `~/.ssh/authorized_keys` |
| SSH server | `/etc/ssh/sshd_config` and `/etc/ssh/sshd_config.d/*.conf` (first value wins, and the include sits at the top of the main file) |
| Firewall | `ufw status verbose`; rules in `/etc/ufw/`; `nft list ruleset` or `iptables -S` for everything else |
| Swap | `swapon --show`; `/swap.img` or `/swapfile` in `/etc/fstab` |
| Mounts | `/etc/fstab`, `findmnt`, `lsblk -f` |

## Common services

| Service | Config | Logs | Data or runtime |
|---|---|---|---|
| nginx | `/etc/nginx/nginx.conf`, `conf.d/`, sites in `sites-available/` linked from `sites-enabled/` | `/var/log/nginx/` | web roots usually `/var/www/` or a deploy user's home |
| Apache | `/etc/apache2/`, `sites-available/` via `a2ensite`, modules via `a2enmod` | `/var/log/apache2/` | `/var/www/` |
| PHP-FPM | `/etc/php/<v>/fpm/php.ini`, pools in `/etc/php/<v>/fpm/pool.d/`; the CLI has its own `/etc/php/<v>/cli/php.ini` | `/var/log/php<v>-fpm.log`, plus the pool's own `error_log` | socket `/run/php/php<v>-fpm.sock` |
| MySQL | `/etc/mysql/mysql.conf.d/mysqld.cnf`, `conf.d/` | `/var/log/mysql/error.log` | `/var/lib/mysql/` |
| MariaDB | `/etc/mysql/mariadb.conf.d/` | `/var/log/mysql/` or the journal | `/var/lib/mysql/` |
| PostgreSQL | `/etc/postgresql/<v>/main/` (`postgresql.conf`, `pg_hba.conf`); `pg_lsclusters` lists clusters | `/var/log/postgresql/` | `/var/lib/postgresql/<v>/main/` |
| Redis or Valkey | `/etc/redis/redis.conf` or `/etc/valkey/` | `/var/log/redis/` | `/var/lib/redis/` |
| Supervisor | `/etc/supervisor/supervisord.conf`, programs in `/etc/supervisor/conf.d/` | `/var/log/supervisor/`, each program's `stdout_logfile` | |
| Docker | `/etc/docker/daemon.json` (log limits, `live-restore`) | `journalctl -u docker`, `docker logs <c>`; files in `/var/lib/docker/containers/<id>/` | `/var/lib/docker/` (images, volumes; never delete by hand) |
| Certbot | `/etc/letsencrypt/` (`live/<domain>/` links into `archive/`; renewal settings in `renewal/`) | `/var/log/letsencrypt/` | renewal by `certbot.timer` or the snap's timer |
| Fail2ban | `/etc/fail2ban/jail.local`, `jail.d/` (never edit `jail.conf`) | `/var/log/fail2ban.log` | |
| Postfix | `/etc/postfix/main.cf` | `/var/log/mail.log` | `/var/spool/postfix/` |

Several PHP versions can run side by side (`php8.3-fpm` and `php8.4-fpm`), each with its own
`php.ini` and pool. The one a site uses is the socket its nginx `fastcgi_pass` names, and the one a
cron job or deploy uses is whatever `php` resolves to (`update-alternatives --display php`). Read
both before saying which version a site runs.

Node apps are often run by pm2 under a deploy user (`pm2 ls`, `~/.pm2/logs/`, started at boot by a
`pm2-<user>` unit) or by a systemd unit. Python apps usually run gunicorn or uvicorn from a
virtualenv under a systemd unit. Snap packages keep their files under `/snap/<name>/` and
`/var/snap/<name>/`, and refresh themselves (`snap refresh --list`, `snap changes`).

## Apps in containers

On a server run by a container platform (Coolify, Dokploy, CapRover) or by Docker Compose, the host
holds Docker and little else, and the usual places are inside containers:

| What | Where |
|---|---|
| What runs | `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"`; a panel names containers by an ID, so match them by image or by the panel's own listing |
| Which ports are public | the `0.0.0.0:` entries in `docker ps`; usually only the proxy should have any |
| Web server and TLS | the proxy container (Traefik, Caddy, nginx-proxy) holds 80 and 443, routes by container labels or the panel's config, and issues certificates itself |
| An app's logs | `docker logs --tail 100 <container>`, `--since 1h`; kept only up to the `log-opts` limits in `daemon.json`, and without limits they grow until the disk fills |
| An app's config | the panel's settings or the compose file and its `.env`; never the container's filesystem |
| Data | named volumes under `/var/lib/docker/volumes/` (`docker system df -v`); deleting a volume deletes the database |
| Inside a container | `docker exec <container> php -v`, `... php -i`, `... cat /etc/nginx/nginx.conf`: read-only checks only |
| The platform's own files | its data directory (Coolify uses `/data/coolify`); leave it to the platform |

`docker inspect` and `docker compose config` print every environment variable, secrets included;
don't run them where the output is shared. Restarting `docker.service` stops every container,
proxy included, unless `"live-restore": true` is set.

## Find it on this server

```sh
systemctl cat nginx                 # the unit, every drop-in, and the binary it runs
systemctl status php8.3-fpm         # main PID, recent log lines, whether it is enabled
sudo nginx -T | grep -n server_name # the whole loaded nginx config, includes resolved
dpkg -L php8.3-fpm | grep etc       # the files a package installed
dpkg -S /usr/sbin/nginx             # the package that owns a file
sudo ls -l /proc/<pid>/cwd /proc/<pid>/exe   # where a process runs from
sudo ss -tlnp | grep :3306          # which process holds a port
```
