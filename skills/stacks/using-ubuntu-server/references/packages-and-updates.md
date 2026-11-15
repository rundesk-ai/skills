# Packages and updates

## Install, update and inspect

```sh
sudo apt update                       # refresh lists; read its warnings (expired key, missing suite)
apt list --upgradable                 # what an upgrade would change, before it does
sudo apt upgrade                      # never removes a package
sudo apt full-upgrade                 # may remove packages to resolve dependencies; read the list first
apt-cache policy <pkg>                # installed and candidate version, and which repo wins
apt-mark showhold                     # packages pinned in place
```

- **In scripts use `apt-get`**, with `-y`, `-q` and `DEBIAN_FRONTEND=noninteractive`. `apt`'s output
  and prompts are for people and may change between releases.
- **Read the removal list.** An install that also removes packages (a conflicting PHP extension, a
  MySQL replaced by MariaDB) prints them before asking. Stop and show the person.
- **`apt autoremove`** removes what nothing depends on, including old kernels, and occasionally a
  library a hand-built binary needs. Show its list before running it.
- **Hold a package** the person wants frozen: `sudo apt-mark hold <pkg>`; undo with `unhold`. A held
  package also holds back what depends on it, so say what the hold costs.
- **Never install a `.deb` from the web or pipe a script into a shell as root** without the person
  saying so. Prefer the archive, then the vendor's signed repository.

## Third-party repositories and PPAs

A third-party source (a PPA for newer PHP, the vendor's repo for Docker, Node, PostgreSQL or MySQL)
is a file in `/etc/apt/sources.list.d/` that names its key with `Signed-By`. `apt-key` is
deprecated and is gone in 26.04, so a provisioning step that calls `apt-key add` fails there:

```text
Types: deb
URIs: https://repo.example.com/apt
Suites: noble
Components: main
Signed-By: /etc/apt/keyrings/example.gpg
```

Three consequences an agent misses:

- **Unattended upgrades install only security updates from Ubuntu** by default. Packages from a PPA
  or a vendor repo (PHP from a PPA, Docker, Node) get no automatic updates unless their origin is
  added to `50unattended-upgrades`. Say so when the person assumes the server patches itself.
- **A release upgrade disables every third-party source** and does not turn it back on. Each must
  be re-pointed at the new suite (`noble` → `resolute`) after checking the vendor supports it.
- **The suite must match the release.** A source for the wrong codename installs packages built for
  another release.

## Security updates and reboots

The defaults on Ubuntu Server: `unattended-upgrades` runs once a day from `apt-daily-upgrade.timer`
with a random delay, installs only the release's `-security` pocket (and ESM when attached), and
**never reboots** (`Unattended-Upgrade::Automatic-Reboot "false"`). Check what it did in
`/var/log/unattended-upgrades/` and preview with `sudo unattended-upgrade -v --dry-run`.

**needrestart restarts services for you (24.04 and later).** After every apt transaction, unattended
ones included, it restarts each service whose process still uses a replaced library, without
asking. A libc or OpenSSL security update therefore restarts nginx, PHP-FPM, the database and the
workers on its own schedule. Ubuntu considers this a security feature and offers no supported
blanket off switch:

- Control when updates land (move the timer to a quiet hour with `systemctl edit
  apt-daily-upgrade.timer`) rather than stopping restarts.
- A unit that must never restart unannounced can be excluded through `$nrconf{override_rc}` in a
  file in `/etc/needrestart/conf.d/`; that leaves it running old code until a planned restart, so
  agree it with the person and say who restarts it.
- See what still needs a restart: `sudo needrestart -r l` lists without restarting.
- On a Docker host, check whether `docker.service` and `containerd.service` are excluded in
  `/etc/needrestart/needrestart.conf` and `conf.d/`. If they are not, a library update can restart
  the daemon, and without `live-restore` that stops every container at the update's random time.

**A kernel update needs a reboot to take effect.** `/var/run/reboot-required` exists when one is
pending and `/var/run/reboot-required.pkgs` names why; `uname -r` against the newest installed
`linux-image-*` confirms it. Livepatch, where the person has it, covers some kernel fixes until the
reboot. Before rebooting: confirm the person agreed, that services are enabled to start at boot
(`systemctl is-enabled`), that `/etc/fstab` mounts nothing that might be missing (a bad line drops
the boot to emergency mode, with no SSH), and that you know how to reach the console if it does not
come back. After: `systemctl --failed`, `ss -tlnp` compared with before, and a real request.

## Release upgrades

LTS-to-LTS upgrades are offered only from the first point release (24.04 → 26.04 opened with
26.04.1). Use `sudo do-release-upgrade` on servers, never a hand edit of the sources to the new
codename. Before it, with the person's approval and a window:

1. A tested backup or a provider snapshot. The upgrade can fail half way.
2. `sudo apt update && sudo apt full-upgrade`, then reboot onto the current release's newest kernel.
3. Run it inside `tmux` or `screen`, so a dropped SSH connection does not kill it. Over SSH it
   offers a second sshd on port 1022, which the firewall must allow to be any use.
4. At each "modified configuration file" prompt, keeping your version keeps your settings but not
   the new defaults; taking the maintainer's drops your changes. Settings already in drop-ins
   survive either answer, which is a reason to move them there first.
5. After: re-enable third-party sources for the new suite, `systemctl --failed`, the services'
   versions (a new PHP or PostgreSQL major is a separate migration), and a real request.

## What changed in recent releases

**24.04 (noble):** deb822 `ubuntu.sources`; needrestart restarts services by default; sshd is
socket-activated (since 22.10); PHP 8.3, Python 3.12, PostgreSQL 16, MySQL 8.0.

**26.04 (resolute)**, from its release notes:

- `sudo` is **sudo-rs**; the original is `sudo.ws`, and `sudo-ldap` is gone. Unsupported sudoers
  directives are refused, so run `sudo visudo -c` and read the sudoers drop-ins before upgrading.
- Core utilities come from **rust-coreutils**; GNU versions stay as `gnuls`, `gnudate` and so on, and
  `cp`, `mv` and `rm` remain GNU. A script parsing `ls` or using GNU-only flags can break.
- **chrony** replaces systemd-timesyncd on fresh installs; upgraded servers keep timesyncd.
- **dracut** replaces initramfs-tools; **cgroup v1 is removed**, and a server still booting with it
  is refused the upgrade (check `stat -fc %T /sys/fs/cgroup/` prints `cgroup2fs`).
- 26.04 is the last release with System V init-script compatibility; move any `/etc/init.d` script
  to a unit.
- **APT 3.1**: `apt-key` removed; `apt history-list`, `history-info` and `history-undo` added.
- **OpenSSH 10.2**: DSA keys removed; `sshd.service` is an alias of `ssh.service`.
- **MySQL 8.4**: accounts on `mysql_native_password` are locked out by default; move them to
  `caching_sha2_password` before upgrading, or the application cannot connect.
- PHP 8.5, Python 3.14 (virtualenvs built on 3.12 must be rebuilt), PostgreSQL 18 (an existing
  cluster stays on its old major until upgraded with `pg_upgradecluster`), kernel 7.0.
