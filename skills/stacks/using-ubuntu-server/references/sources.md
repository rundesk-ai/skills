# Ubuntu Server source basis

Checked against Ubuntu 24.04 LTS and 26.04.1 LTS documentation in November 2026. Read this when a
claim in the skill is challenged or a new release may have changed it. Nothing here was reproduced
on a live server for this skill; the claims rest on the documentation below.

## Ubuntu

- [Automatic updates](https://ubuntu.com/server/docs/how-to/software/automatic-updates/):
  unattended-upgrades enables only the release, `-security` and ESM origins; `-updates` is commented
  out; `Automatic-Reboot` defaults to `false`; config in `50unattended-upgrades` and
  `20auto-upgrades`; logs in `/var/log/unattended-upgrades`; `unattended-upgrade -v --dry-run`;
  `apt-daily.timer` and `apt-daily-upgrade.timer` with a random delay.
- [Package management](https://ubuntu.com/server/docs/how-to/software/package-management/): `apt`
  is for interactive use and `apt-get` for scripts; deb822 sources in
  `/etc/apt/sources.list.d/ubuntu.sources` from 24.04; `Signed-By`; `/var/log/dpkg.log`.
- [Upgrade your release](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/):
  `do-release-upgrade` on servers; LTS-to-LTS only after the first point release; third-party
  sources and PPAs disabled during the upgrade; back up first.
- [Upgrades from 24.04 LTS to 26.04.1 LTS now enabled](https://discourse.ubuntu.com/t/upgrades-from-ubuntu-24-04-lts-to-ubuntu-26-04-1-lts-now-enabled/88502):
  the 24.04 → 26.04 path opened with 26.04.1.
- [Ubuntu 26.04 LTS summary for LTS users](https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/):
  sudo-rs default, `sudo.ws`, `sudo-ldap` removed; rust-coreutils with `gnu`-prefixed GNU tools and
  the switch commands, `cp`/`mv`/`rm` still GNU; chrony on new installs and the migration commands;
  dracut; systemd 259, cgroup v1 removed, last release with SysV script compatibility; APT 3.1,
  `apt-key` removed, `apt history-*`; OpenSSH 10.2, DSA removed, `sshd.service` alias; MySQL 8.4
  and `mysql_native_password` accounts locked by default; PHP 8.5, Python 3.14, PostgreSQL 18,
  kernel 7.0.
- [needrestart changes in Ubuntu 24.04](https://discourse.ubuntu.com/t/needrestart-changes-in-ubuntu-24-04-service-restarts/44671):
  services restarted directly in interactive and non-interactive runs, unattended upgrades included;
  `$nrconf{override_rc}` and `/etc/needrestart/conf.d/` to exclude a unit; no supported blanket
  disable, control when updates are installed instead.
- [sshd socket-based activation, 22.10 and later](https://discourse.ubuntu.com/t/sshd-now-uses-socket-based-activation-ubuntu-22-10-and-later/30189):
  `ssh.socket`; `addresses.conf` migration on 22.10–23.10; a generator reads `Port` and
  `ListenAddress` from `sshd_config` on 24.04; `daemon-reload` and a socket restart to apply.
- [Ubuntu manpage: sshd_config(5)](https://manpages.ubuntu.com/manpages/noble/man5/sshd_config.5.html):
  the first obtained value is used; Debian's package includes `sshd_config.d/*.conf` at the start of
  the file, so options there override the main file.
- [Ubuntu manpage: sudoers(5)](https://manpages.ubuntu.com/manpages/noble/man5/sudoers.5.html):
  `@includedir` skips files ending in `~` or containing `.`.
- [Ubuntu manpage: crontab(5)](https://manpages.ubuntu.com/manpages/noble/man5/crontab.5.html):
  unescaped `%` becomes a newline; each entry must end in a newline; `SHELL` is `/bin/sh`.
- Debian's `cron(8)` (package `cron`): files in `/etc/cron.d` must follow run-parts naming
  (letters, digits, `_`, `-`). Not re-checked for this skill, because the Ubuntu manpage site now
  serves cronie's page; the skill's advice (no dots) is safe under both.

- [About apt upgrade and phased updates](https://ubuntu.com/server/docs/explanation/software/about-apt-upgrade-and-phased-updates/):
  "kept back" packages are usually phased; security updates are never phased; forcing them with
  `apt install` is not recommended.
- [OpenSSH 8.8 release notes](https://www.openssh.org/txt/release-8.8): "disables RSA signatures
  using the SHA-1 hash algorithm by default".

## systemd, netplan, cloud-init

- [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html): `edit`
  writes `override.conf` drop-ins, `--full`; `daemon-reload` reruns generators and re-reads units;
  `reload-or-restart`; `is-enabled`; `list-timers`; `mask` links to `/dev/null`.
- [journald.conf(5)](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html):
  `SystemMaxUse=` defaults to 10% of the filesystem, capped at 4G.
- [netplan try](https://netplan.readthedocs.io/en/stable/netplan-try/): applies and rolls back
  unless confirmed within 120 seconds by default; verify the revert after a timeout.
- [cloud-init network configuration](https://docs.cloud-init.io/en/latest/reference/network-config.html):
  disable with `network: {config: disabled}` in `/etc/cloud/cloud.cfg.d/` or `network-config=disabled`
  on the kernel line.

## Docker

- [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/):
  traffic to a published container port "gets diverted before it goes through the ufw firewall
  settings"; nftables backend is experimental.
- [ufw-docker README](https://github.com/chaifeng/ufw-docker): "Docker bypass the UFW rules and
  the published ports can be accessed from outside"; rejects disabling Docker's iptables; filters
  in the `DOCKER-USER` chain. Publishing on `127.0.0.1` behind a proxy is the common alternative in
  the practitioner guides.

- [Live restore](https://docs.docker.com/engine/daemon/live-restore/): off by default, so the
  daemon stops running containers when it terminates; `"live-restore": true` in `daemon.json`.

## nginx and Coolify

- [ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html):
  `client_max_body_size` defaults to `1m` and returns 413 when exceeded.
- [Coolify installation](https://coolify.io/docs/get-started/installation): the installer sets up
  its directories under `/data/coolify`.

## Observed on a server

A Coolify-managed Ubuntu 24.04.5 server on a cloud provider, read with read-only commands only in
November 2026, confirmed: deb822 `ubuntu.sources` beside third-party one-line `.list` files;
`99needrestart` calling needrestart with `-m u`; unattended upgrades enabled, with the two apt
timers; `ssh.socket` listening on 22; `50-cloud-init.conf` and `60-cloudimg-settings.conf` in
`sshd_config.d`; `50-cloud-init.yaml` as the only netplan file; the resolved stub link; ufw
inactive with filtering left to the provider; the proxy container publishing 80, 443 and 8080 on
`0.0.0.0`; no nginx, PHP, database or certbot on the host; Docker log limits set without
`live-restore`; `df -h` dominated by Docker's overlay mounts; no swap.

## Practitioner evidence

- [Ubuntu 24.04 to 26.04 on production servers](https://kexpiral.com/en/blog/ubuntu-24-04-to-26-04-server-upgrade/):
  the cgroup v1 upgrade refusal and `stat -fc %T /sys/fs/cgroup/`; `apt-key add` failing in
  provisioning scripts; config-file prompts dropping `sshd_config` changes. Its claims not found in
  the release notes (Apache JIT, PostgreSQL on kernel 7.0) are left out of the skill.
- [The backup SSH daemon before every do-release-upgrade](https://ma.ttias.be/backup-sshd-do-release-upgrade/):
  the port-1022 fallback sshd, which the firewall must allow, and running the upgrade in `tmux` or
  `screen`.
