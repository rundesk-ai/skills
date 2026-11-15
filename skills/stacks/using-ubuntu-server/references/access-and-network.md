# Access and networking

Every change here can end the only connection to the server. Keep the current session open, make
the change, log in from a **second** session, run `sudo -v` there, and only then close the first.

## SSH

- Put settings in `/etc/ssh/sshd_config.d/<name>.conf`. The main file includes that directory at
  its top, and sshd uses the **first** value it reads for most settings, so a drop-in beats a
  later line in `sshd_config`, and a cloud image's own drop-in (`50-cloud-init.conf` setting
  `PasswordAuthentication yes`) can beat yours. Check the setting in force with
  `sudo sshd -T | grep -i <setting>`.
- Validate with `sudo sshd -t`, then `sudo systemctl reload ssh`. Existing sessions survive a
  reload or restart; new logins use the new settings.
- Before `PasswordAuthentication no` or `PermitRootLogin no`, confirm a key login works for a user
  with sudo, from the second session.
- `authorized_keys` is ignored when the home directory, `~/.ssh` or the file is writable by others;
  the log line is `Authentication refused: bad ownership or modes`. Fix with `chmod 700 ~/.ssh`,
  `chmod 600 ~/.ssh/authorized_keys`, owned by the user.

### Changing the port on 22.10 and later

sshd is socket-activated: `ssh.socket` listens and starts sshd on the first connection. On 24.04 and
later a systemd generator reads `Port` and `ListenAddress` from `sshd_config` into the socket, so
after changing them:

```sh
sudo sshd -t
sudo systemctl daemon-reload          # regenerate the socket from sshd_config
sudo systemctl restart ssh.socket     # the socket now listens on the new port
sudo ss -tlnp | grep -e sshd -e systemd   # confirm the port before closing anything
```

Open the new port in the firewall **before** the restart, test a login on it from a second session,
and only then remove the old port's rule. A server upgraded from 22.10–23.10 may also carry
`/etc/systemd/system/ssh.socket.d/addresses.conf`, which wins over `sshd_config`; read
`systemctl cat ssh.socket` to see what the socket really uses.

## Users and sudo

```sh
sudo adduser deploy                    # interactive, makes the home directory
sudo usermod -aG sudo deploy           # -a appends; without it the user loses every other group
id deploy; getent group sudo
```

- `usermod -G` without `-a` replaces the user's groups, which can remove `sudo` from the only admin.
- Edit sudoers only with `sudo visudo -f /etc/sudoers.d/<name>`; it refuses to save a syntax error.
  A broken sudoers file locks every user out of sudo. Files in `sudoers.d` with a `.` or ending in
  `~` are ignored.
- A narrow rule names full paths: `deploy ALL=(root) NOPASSWD: /usr/bin/systemctl reload nginx`.
  A rule allowing an editor, a shell, `tee`, or a script the user can write gives full root.
- On 26.04 `sudo` is sudo-rs, which rejects directives it does not implement; run `sudo visudo -c`
  after any change.

## Firewall (ufw)

`Status: inactive` is common on cloud servers that filter at the provider's firewall instead. That
firewall is invisible from the shell, so ask the person whether one exists before saying a port is
or is not reachable, and test from outside (`nc -vz <host> <port>` from another machine).

```sh
sudo ufw status verbose                # inactive, or the rules and default policies
sudo ufw allow OpenSSH                 # or: sudo ufw allow 2222/tcp, before enabling
sudo ufw allow 'Nginx Full'            # 80 and 443; app profiles: sudo ufw app list
sudo ufw enable
sudo ufw status numbered; sudo ufw delete <n>
```

- `ufw enable` applies a default deny for incoming traffic at once. Without an SSH rule first, every
  new login is refused, and the session you are in becomes the only way back in.
- `ufw reset` removes every rule and disables the firewall; ask first.
- Limit admin and database ports to known addresses: `sudo ufw allow from 203.0.113.10 to any port
  3306 proto tcp`. A database listening on `0.0.0.0` with no rule is open to the internet; check
  `ss -tlnp`, and prefer binding it to `127.0.0.1` or a private address.
- A provider's cloud firewall sits in front of ufw; a port can be open in one and closed in the
  other.

### Docker and ufw

A container port published with `-p 8080:80` or `ports:` in compose is reachable from the internet
whatever ufw says: Docker routes the traffic through its own rules before ufw's INPUT rules see it,
and `ufw status` does not show them. Publish on loopback (`127.0.0.1:8080:80`) and put nginx in
front, or add filtering rules to Docker's `DOCKER-USER` chain. Never set Docker's `"iptables":
false` to fix it; container networking breaks. Prove the result with a scan from outside the
server, not from `ufw status`.

## Network and DNS

- Network config is netplan YAML in `/etc/netplan/`. Change it with `sudo netplan generate` (syntax)
  then `sudo netplan try`, which reverts after 120 seconds unless confirmed; `netplan apply` on a
  remote server has no way back. Files must be mode 600.
- cloud-init writes `50-cloud-init.yaml` from the provider's metadata and may rewrite it at boot.
  Put your change in a separate, higher-numbered file, or disable cloud-init's network config with
  `network: {config: disabled}` in a file in `/etc/cloud/cloud.cfg.d/`, as the person chooses.
- `/etc/resolv.conf` points at systemd-resolved (`127.0.0.53`). Set DNS servers in netplan
  (`nameservers:`) or `/etc/systemd/resolved.conf.d/`; an edit to `resolv.conf` is overwritten. Read
  the servers really used with `resolvectl status`; test with `resolvectl query <host>`.
- The hostname is `hostnamectl set-hostname <name>`, plus its line in `/etc/hosts`; cloud-init can
  reset it unless `preserve_hostname: true` is set.
