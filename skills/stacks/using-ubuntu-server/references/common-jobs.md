# Common jobs

Each of these changes the server, so each starts with the person's go-ahead and ends with proof
that it works. On a container platform, do the same jobs through the panel instead.

## A fresh server

In this order, so no step can lock you out of the next:

1. `sudo apt update && sudo apt upgrade`, then reboot if `/var/run/reboot-required` exists.
2. Create the admin or deploy user (`adduser`, `usermod -aG sudo`), put the person's public key in
   its `~/.ssh/authorized_keys` (mode 600, `~/.ssh` 700), and log in as it from a second session.
3. Only then, in `/etc/ssh/sshd_config.d/`: `PasswordAuthentication no`, `PermitRootLogin no` (or
   `prohibit-password`). Check the cloud image's own drop-ins do not override them (`sshd -T`),
   `sshd -t`, reload, and test a new login.
4. Firewall: the provider's, or ufw with SSH allowed before `ufw enable`, then 80 and 443.
5. Confirm unattended upgrades are on (`/etc/apt/apt.conf.d/20auto-upgrades`) and agree when
   reboots happen.
6. Swap when there is none (see troubleshooting), timezone (`timedatectl set-timezone UTC` unless
   the person wants another), hostname.

## Add a site behind nginx

1. DNS for the domain points at the server (`dig +short <domain>`); certificate issuance fails
   otherwise.
2. A server block in `/etc/nginx/sites-available/<domain>`, copied from a working site on the same
   server rather than written from memory, with `server_name`, `root` and the PHP-FPM socket or
   `proxy_pass` it needs.
3. `sudo ln -s /etc/nginx/sites-available/<domain> /etc/nginx/sites-enabled/`, `sudo nginx -t`,
   `sudo systemctl reload nginx`.
4. `sudo certbot --nginx -d <domain> -d www.<domain>` issues the certificate, edits the block and
   sets up renewal; `sudo certbot renew --dry-run` proves renewal.
5. `curl -sI https://<domain>/` returns the app's status, not nginx's default page.

## Switch a site to another PHP version

1. List what the current version has: `php<old> -m` and `dpkg -l 'php<old>*'`. Install the new
   `php<new>-fpm` with the same extensions (from the same source: the archive or the PPA already in
   use).
2. Carry over the pool (`/etc/php/<old>/fpm/pool.d/`) and the `php.ini` settings the site changed.
3. Point the site's `fastcgi_pass` at `/run/php/php<new>-fpm.sock`, `nginx -t`, reload, and test.
4. The CLI is separate: cron jobs, queue workers and deploy scripts use whatever `php` resolves to
   (`sudo update-alternatives --config php`) or a full path. Move them too, and restart the
   workers.
5. Leave the old FPM running until the person agrees nothing uses it.

## Node with nvm

nvm installs Node under one user's `~/.nvm/versions/node/`, and only that user's interactive shells
load it. systemd units, cron and `sudo` do not, so a unit or job needs the full path to that
version's `node`, or Node from a system-wide source (the distribution, or the NodeSource apt
repository) instead. pm2 keeps the Node it was started with: after a Node upgrade, the apps run on
the old one until pm2 restarts them, and its boot unit must be regenerated with `pm2 startup`.

## Grow the disk after the provider resizes it

```sh
lsblk                                  # the disk is bigger than the partition
sudo growpart /dev/vda 1               # grow partition 1 to fill the disk
sudo resize2fs /dev/vda1               # ext4; for XFS: sudo xfs_growfs /
df -h /
```

Read the real device and partition names from `lsblk` first; on cloud images cloud-init grows the
root partition at boot, so a reboot may already have done it.

## Database backups

- MySQL: `mysqldump --single-transaction --routines --triggers <db> | gzip > <file>.sql.gz`, so
  InnoDB tables are dumped consistently without locking. PostgreSQL: `pg_dump -Fc <db> > <file>.dump`
  as the `postgres` user, restored with `pg_restore`. In a container, run the same tool through
  `docker exec`.
- Keep the password out of the command line, where `ps` and the shell history show it: use
  `~/.my.cnf` or `~/.pgpass`, mode 600.
- A backup on the same disk dies with the server. Copy it off the machine, keep several days, and
  check each file is not empty.
- A backup nobody has restored is a guess. Restore one into a scratch database and count rows in a
  table that matters.
