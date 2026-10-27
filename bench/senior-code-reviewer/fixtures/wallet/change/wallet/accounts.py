import threading
from typing import Dict


class Insufficient(Exception):
    pass


class Accounts:
    def __init__(self, balances: Dict[str, int]):
        self._balances = dict(balances)
        self._lock = threading.Lock()

    def balance(self, account: str) -> int:
        with self._lock:
            return self._balances[account]

    def deposit(self, account: str, cents: int) -> None:
        if cents <= 0:
            raise ValueError("a deposit must be positive")
        with self._lock:
            self._balances[account] += cents

    def withdraw(self, account: str, cents: int) -> None:
        """Takes `cents` from `account`; the check and the debit happen under one lock."""
        if cents <= 0:
            raise ValueError("a withdrawal must be positive")
        with self._lock:
            if self._balances[account] < cents:
                raise Insufficient(account)
            self._balances[account] -= cents

    def transfer(self, source: str, target: str, cents: int) -> None:
        """Moves `cents` from `source` to `target`."""
        if cents <= 0:
            raise ValueError("a transfer must be positive")
        if source == target:
            raise ValueError("cannot transfer to the same account")
        if self.balance(source) < cents:
            raise Insufficient(source)
        with self._lock:
            self._balances[source] -= cents
            self._balances[target] += cents
