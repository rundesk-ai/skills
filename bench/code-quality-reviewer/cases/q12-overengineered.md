+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "needless abstraction around one implementation, hiding a real bug in the indirection"
fixture = "notify"
cases_version = 2
key = """
must:
  M1 bug+rule  registry.get_notifier caches one notifier per kind and ignores the settings of every later call, so the first tenant's notifier (its from_address and its transport) sends every other tenant's mail: South's customer gets mail from hello@north.example through North's transport (reproduced). Breaks "Each tenant's mail goes out from that tenant's own address". The single test clears the cache and uses one tenant, so it cannot see this. Fix: build the notifier per call (it is cheap), or key the cache by tenant.
  M2 org       four layers for one email notifier: NotifierInterface, AbstractNotifierFactory, a factory registry and NotificationStrategy, each with exactly one implementation, and DefaultNotificationStrategy.dispatch only calls notifier.send. Any change to how mail is sent touches four files, and the indirection is what hid M1. Fix: send_welcome builds an EmailMessage with the tenant's address and hands it to the tenant's transport; delete interfaces.py, strategy.py and the registry.
  M3 org       flexibility nothing uses: NotifyConfig.retries, backoff_seconds, priority and plugin_paths are read nowhere, and plugins.load_plugins is never called (and would import any dotted path it is given). Fix: delete them until a requirement needs them.
good code:
  G1 transport.py: Transport with two real implementations, SmtpTransport (production) and OutboxTransport (tests and staging). This abstraction earns its place; proposing to remove it is a false positive.
  G2 SmtpTransport uses a timeout and STARTTLS.
decoys:
  D1 a default argument config=NotifyConfig() looks like the mutable-default trap, but the instance is never mutated; correct, though M3 removes it anyway. Reporting it as a mutable-default bug is a false positive.
taste:
  T1 ABC with ellipsis bodies; T2 module-level dicts for registries; T3 Dict typing imports.
extras:
  X1 send_welcome interpolates the tenant name into the subject without stripping newlines (EmailMessage rejects them, so this raises rather than injects).
  X2 SmtpTransport opens a new connection per message.
"""
+++
Review the `notify` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
