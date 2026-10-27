import threading
from typing import Dict


class Insufficient(Exception):
    pass


class UnknownAccount(Exception):
    pass


class Accounts:
    def __init__(self, balances: Dict[str, int]):
        self._balances = dict(balances)
        self._lock = threading.Lock()

    def balance(self, account: str) -> int:
        with self._lock:
            if account not in self._balances:
                raise UnknownAccount(account)
            return self._balances[account]

    def withdraw(self, account: str, cents: int) -> None:
        if cents <= 0:
            raise ValueError("a withdrawal must be positive")
        with self._lock:
            if account not in self._balances:
                raise UnknownAccount(account)
            if self._balances[account] < cents:
                raise Insufficient(account)
            self._balances[account] -= cents
