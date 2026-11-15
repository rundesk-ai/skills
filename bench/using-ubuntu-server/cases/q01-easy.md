+++
skill = "using-ubuntu-server"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = ""
rubric = """
result.1  Names the cause: on Ubuntu 22.10 and later sshd is socket-activated, so ssh.socket keeps listening on 22 and restarting ssh.service alone does not move the port.
result.2  Gives the 24.04 sequence: sshd -t, daemon-reload so the generator rereads Port from sshd_config, restart ssh.socket, then confirm the listener with ss -tlnp.
result.3  Opens 2222/tcp in ufw (and says a provider firewall may also need it) before the socket restart, and removes the port-22 rule only after a login on 2222 works.
result.4  Keeps the current session open and tests the new port from a second session before closing anything.
result.5  Mentions checking for a leftover ssh.socket.d/addresses.conf (or reading systemctl cat ssh.socket) on a server upgraded from an earlier release.
conduct.1 Gives commands the person can run as written, and does not suggest disabling the firewall or ssh.socket as the first fix.
"""
+++
I changed `Port 22` to `Port 2222` in /etc/ssh/sshd_config on our Ubuntu 24.04 box and ran
`sudo systemctl restart ssh`, but `ss -tlnp` still shows it listening on 22 and nothing on 2222.
ufw is on with OpenSSH allowed. What am I missing, and what do I run so I don't lock myself out?
