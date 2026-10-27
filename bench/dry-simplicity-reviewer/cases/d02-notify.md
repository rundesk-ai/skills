+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "code-quality-reviewer/notify"
cases_version = 1
key = """
must:
  M1 cplx  four layers for one email notifier: NotifierInterface, AbstractNotifierFactory, the FACTORIES registry and NotificationStrategy each have exactly one implementation, and DefaultNotificationStrategy.dispatch only calls notifier.send. Simplify to send_welcome building the message and handing it to the tenant's transport; delete interfaces.py, strategy.py and the registry.
  M2 cplx  flexibility nothing uses: NotifyConfig.retries, backoff_seconds, priority and plugin_paths are read nowhere, and plugins.load_plugins is never called. Delete them.
good code:
  G1 transport.py: Transport has two real implementations, SmtpTransport and OutboxTransport (tests and staging). Removing or merging it is a false positive.
decoys:
  D1 EmailNotifier.send sets four headers in four lines; nothing to consolidate.
taste:
  T1 ABC with ellipsis bodies; T2 module-level dicts; T3 typing imports.
extras (not required of this reviewer; neither hit nor false positive):
  X1 get_notifier caches the first tenant's notifier and sends every tenant's mail from it (a real bug, and a good catch for this reviewer).
  X2 SmtpTransport opens a connection per message.
"""
+++
Look for duplication, redundancy and needless complexity in the `notify` package, and tell me what is worth consolidating or simplifying.
