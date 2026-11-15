+++
skill = "using-ubuntu-server"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = ""
rubric = """
result.1  States what unattended-upgrades does by default: Ubuntu security pocket only, daily via apt-daily-upgrade.timer, never reboots; and that PHP from the PPA and Docker from Docker's repo are not patched by it unless their origins are added.
result.2  Explains that on 24.04 needrestart restarts affected services after apt runs, unattended ones included, so a library update can restart php-fpm, MySQL, Redis and the workers at a random daily time; proposes moving the timer to a quiet window rather than disabling restarts, and treats excluding a unit as a trade-off.
result.3  Uses /var/run/reboot-required (and .pkgs) and the running versus installed kernel to decide whether a reboot is due.
result.4  Answers the auto-reboot question with a position grounded in their setup (one server per role, no redundancy, so a reboot is downtime; workers mid-job; Docker restarts containers) and the conditions under which Automatic-Reboot with a set time would be acceptable.
result.5  The runbook orders: snapshot or backup, apt update and review apt list --upgradable, drain or stop workers gracefully (queue:restart or supervisorctl stop), upgrade, restart or reboot, then verify: systemctl --failed, ss -tlnp compared with before, the site over HTTPS, a queue job processed, the containers running.
result.6  Flags that a PHP minor or major change from the PPA, a Docker engine upgrade restarting containers, and MySQL restarts are the risky items, and suggests holding or scheduling them separately.
result.7  Mentions apt-get (not apt) for any scripted part, and the upgrade logs to check (/var/log/apt/history.log, /var/log/unattended-upgrades).
conduct.1 Separates what is a default (verifiable on the box) from what they should check on their own servers, and gives the read-only commands to check it.
"""
+++
We run three Ubuntu 24.04 servers for a SaaS app: one web box (nginx, php8.3-fpm from the ondrej
PPA, Laravel), one worker box (same PHP, Laravel queue workers under supervisor, Redis), and one
database box (MySQL 8.0 from Ubuntu). A small analytics sidecar runs under Docker (from Docker's apt
repo) on the web box. Nothing is redundant. Nobody has a patching routine; I think
unattended-upgrades is on but I'm not sure what it actually does.

Write us a monthly patching runbook we can follow, and tell me straight whether we should just turn
on automatic reboots.
