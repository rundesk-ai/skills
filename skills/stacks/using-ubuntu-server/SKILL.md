---
name: using-ubuntu-server
description: Use when working on an Ubuntu or Debian server from a shell, including finding where config, logs and data live, packages, security updates, reboots and release upgrades, systemd services, timers, cron and workers, nginx, PHP-FPM, databases and Docker on the host, SSH, sudo, the firewall and networking, and a server that is down, slow, full or out of memory. It supplies a look-before-you-change workflow, the validate-then-reload command for each change, and the lockout and data-loss traps of current LTS releases. Do not use for a cloud provider's console or API, Kubernetes, or an application's own code.
---

# Use Ubuntu Server

A live server punishes the habits that are fine on a laptop. A restart that fails leaves a site
down, a firewall or SSH change can lock everyone out with no way back in, and a delete under
`/var/lib` is unrecoverable. Look first, change one thing, validate it before it takes effect,
and prove the service still answers.

## 1. Orient before you touch anything

These are read-only; run them first on any server you have not seen in this session:

```sh
cat /etc/os-release; uname -r; uptime          # release, running kernel, load, how long since boot
ls /var/run/reboot-required* 2>/dev/null       # a reboot is pending, and for which packages
systemctl --failed; systemctl list-units --type=service --state=running
ss -tlnp                                       # what listens on which port, and which process
df -h -x overlay -x tmpfs; df -i; free -h      # disk without Docker's mounts, inodes, memory, swap
journalctl -p warning -b --no-pager | tail -50 # this boot's warnings and errors
tail -20 /var/log/apt/history.log              # what changed recently
docker ps 2>/dev/null                          # whether the apps run in containers
```

An agent's shell has no one to answer a prompt, so a command that waits for input hangs the run:
pass `--no-pager` to `systemctl` and `journalctl` (or set `SYSTEMD_PAGER=cat`), never run `-f`,
`top`, `watch`, `less` or an editor, use `sudo -n` so a password prompt fails instead of waiting,
and give `mysql`/`psql` the query with `-e`/`-c`. When a command does stop at a password,
passphrase or `[y/N]` prompt, hand it to the person rather than answering it.

Then find out **who owns the configuration**. A hosting panel (Forge, Ploi, RunCloud, cPanel, or a
container platform such as Coolify, Dokploy or CapRover), configuration management (Ansible,
Puppet, Chef), cloud-init, the cloud provider's agent (DigitalOcean's `droplet-agent`, the AWS SSM
agent) or a deploy script may write the file you are about to edit, and will overwrite your edit on
its next run. Look for a comment at the top of the file, a panel's agent or containers among the
services, `/etc/cloud/`, and the project's docs. When something else owns it, change it there, or
tell the person.

**When `docker ps` shows the app, its database and a proxy (Traefik, Caddy, nginx) in containers**,
the host has no nginx, PHP or database config to edit, and certbot is not what issues the
certificates: the proxy container does. Read logs with `docker logs --tail 100 <container>`, look
inside with a read-only `docker exec <container> <command>`, and make every change (environment,
domains, ports, restarts) through the panel or the compose file, because a container changed by
hand is replaced on the next deploy. Never run `docker inspect` where its output is shared: it
prints every environment variable, secrets included. Read the containers section of
[where things live](references/where-things-live.md).

Find a service's files from the system rather than from memory: `systemctl cat <unit>` shows the
unit and every drop-in, `dpkg -L <package>` lists what a package installed, `dpkg -S <path>` names
the package that owns a file, and `ps -o user,cmd -p <pid>` shows who a process runs as.
[Where things live](references/where-things-live.md) maps the usual places.

## 2. Change one thing, validate, then apply

1. **Copy the file first:** `sudo cp -a file file.bak.$(date +%F-%H%M)`. A backup left inside an
   include directory is loaded whenever the include glob matches it (nginx's `sites-enabled/*`
   matches everything, so the old site loads twice), so keep backups of those outside the directory.
2. **Prefer a drop-in to editing a vendor file.** `systemctl edit <unit>` for units;
   `/etc/ssh/sshd_config.d/`, `/etc/php/<v>/fpm/pool.d/`, `/etc/sysctl.d/`, `/etc/sudoers.d/`,
   `/etc/apt/apt.conf.d/` for the rest. A package upgrade then has nothing of yours to conflict
   with, and the change is one file to read or remove.
3. **Validate before it takes effect**, every time: the validator fails safely, a reload of a bad
   file does not.

   | Changed | Validate | Apply |
   |---|---|---|
   | nginx | `sudo nginx -t` | `sudo systemctl reload nginx` |
   | Apache | `sudo apachectl configtest` | `sudo systemctl reload apache2` |
   | PHP-FPM | `sudo php-fpm<v> -t` | `sudo systemctl reload php<v>-fpm` |
   | sshd | `sudo sshd -t` | `sudo systemctl reload ssh` |
   | sudoers | `sudo visudo -c` (edit with `visudo -f`) | immediate |
   | a systemd unit | `systemd-analyze verify <unit>` | `sudo systemctl daemon-reload`, then restart it |
   | netplan | `sudo netplan generate` | `sudo netplan try`, never `apply` remotely |
   | sysctl | read the value back | `sudo sysctl --system` |
   | crontab | `crontab -l` after | immediate |

4. **Reload rather than restart** where the service supports it: a reload keeps serving and a
   failed reload keeps the old config; a failed restart leaves nothing running.
5. **Prove it:** `systemctl status <unit>`, `journalctl -u <unit> -n 50 --no-pager`, and a real
   request (`curl -sI https://<host>/`, a login over a new SSH session, a queue job processed).
   Report what you saw, not that the command exited zero.

## 3. Changes that can lock you out

Before an SSH, firewall, network, sudo or PAM change, **keep the current session open and test from
a second one**; close the first only after the second logs in and runs `sudo -v`. The open session
is the only way back in when the console needs a provider login you do not have.

- **Firewall:** many cloud servers run with ufw inactive and filter at the provider's cloud
  firewall, which the shell cannot see; ask before calling a port open or closed. Enabling ufw:
  allow SSH first (`sudo ufw allow OpenSSH`, or the real port), then `sudo ufw enable`. `ufw status`
  lists only ufw's rules; Docker's published ports bypass it.
- **SSH port on 22.10 and later:** sshd is socket-activated, so the port can come from
  `ssh.socket`, not `sshd_config`. Read [access and networking](references/access-and-network.md)
  before changing the port or address.
- **Network:** `netplan try` reverts after 120 seconds unless confirmed. `netplan apply` does not.

## 4. Ask first

Stop and get the person's go-ahead, saying what it will do and how it is undone, before: a reboot;
a release upgrade; restarting a database, Docker, or anything users are connected to at a busy
hour; `apt purge`, `apt autoremove` or removing a package other packages depend on; deleting
anything under `/var/lib`, `/etc` or a data directory; a recursive `chown`/`chmod`; enabling or
resetting the firewall; changing SSH, sudo or the network; killing a process you did not start;
anything touching disks, partitions or the boot loader. Read-only commands need no permission.

## Traps

| Symptom | Cause | Do instead |
|---|---|---|
| `apt upgrade` restarted MySQL, PHP-FPM or workers mid-day (24.04+) | needrestart runs after every apt transaction, unattended upgrades included, and now restarts affected services without asking | Upgrade in a window; exclude a unit in `/etc/needrestart/conf.d/` only with the person's agreement |
| Disk 100% full, but `du` finds far less | a deleted file still held open (a rotated log) | `sudo lsof +L1`, then reload that service or truncate it via `/proc/<pid>/fd/<n>` |
| "No space left" with free space showing | inodes exhausted (sessions, cache files) | `df -i`, then find the directory with the most files |
| A process vanished with no error | the kernel OOM killer | `journalctl -k \| grep -i -e oom -e killed`; fix the memory, add swap |
| Edit to a netplan or hostname file reverts on reboot | cloud-init regenerates it | change it in the cloud-init config or disable its network config |
| A container's port is reachable from the internet despite `ufw deny` | Docker writes its own iptables rules ahead of ufw | publish on `127.0.0.1:<port>:<port>` and proxy through nginx, or filter in `DOCKER-USER` |
| A script behaves differently on 26.04 | `sudo` is sudo-rs and `ls`, `date`, `sort` are Rust coreutils | `sudo visudo -c` before upgrading; GNU tools remain as `gnuls`, `gnudate` |
| `apt` in a script warns or prompts | `apt` is for people | `apt-get -y` with `DEBIAN_FRONTEND=noninteractive` in scripts |
| `Could not get lock /var/lib/dpkg/lock-frontend` | another apt or unattended upgrade is running and holds it | wait for that process (`ps -p <pid>` from the message); never delete a lock file, which lets two dpkg runs corrupt the package database |
| `dpkg was interrupted` | an earlier install died part way | show the person, then `sudo dpkg --configure -a` |
| `The following packages have been kept back` | Ubuntu is phasing the update in gradually (security updates never are), or it needs new or removed dependencies | wait for phasing rather than forcing it with `apt install <pkg>`; read `apt full-upgrade`'s removal list before running it |
| Restarting Docker took every site down | containers stop with the daemon unless `live-restore` is set in `/etc/docker/daemon.json` | treat a Docker restart, and an update that triggers one, as downtime for every container |

## Load focused depth

| The work | Read |
|---|---|
| Finding a config, log, data directory, site, socket or container | [where things live](references/where-things-live.md) |
| Adding a site, switching PHP version, Node with nvm, a fresh server, growing a disk, database backups | [common jobs](references/common-jobs.md) |
| Updates, unattended upgrades, reboots, PPAs and third-party repos, holds, release upgrades, what changed in 24.04 and 26.04 | [packages and updates](references/packages-and-updates.md) |
| Writing or fixing a systemd unit, timer, cron job, queue worker, or reading logs | [services and logs](references/services-and-logs.md) |
| SSH, users, sudo, keys, the firewall, Docker and ufw, netplan, DNS | [access and networking](references/access-and-network.md) |
| A server that is down, slow, full, out of memory, failing TLS, refusing a key, or returning 413, 502 or 504 | [troubleshooting](references/troubleshooting.md) |
| A claim here is challenged, or a release may have changed it | [sources](references/sources.md) |
