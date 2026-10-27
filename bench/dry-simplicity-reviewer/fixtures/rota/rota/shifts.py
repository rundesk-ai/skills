"""A shop's week of shifts, in the order they are shown and swapped."""

from dataclasses import dataclass, field


@dataclass
class Shift:
    person: str
    start: int  # minutes from midnight
    end: int


@dataclass
class Week:
    shifts: list[Shift] = field(default_factory=list)
    log: list[str] = field(default_factory=list)

    def add(self, shift: Shift) -> None:
        if shift.end <= shift.start:
            raise ValueError("a shift must end after it starts")
        self.shifts.append(shift)

    def move_earlier(self, index: int) -> bool:
        """Swaps a shift with the one before it; False at the start of the week."""
        if index <= 0 or index >= len(self.shifts):
            return False
        here, other = self.shifts[index], self.shifts[index - 1]
        self.shifts[index - 1], self.shifts[index] = here, other
        self.log.append(f"{here.person} swapped with {other.person}")
        return True

    def move_later(self, index: int) -> bool:
        """Swaps a shift with the one after it; False at the end of the week."""
        if index < 0 or index >= len(self.shifts) - 1:
            return False
        here, other = self.shifts[index], self.shifts[index + 1]
        self.shifts[index + 1], self.shifts[index] = here, other
        self.log.append(f"{here.person} swapped with {other.person}")
        return True

    def hours(self, person: str) -> float:
        if not person:
            raise ValueError("person is required")
        return sum(s.end - s.start for s in self.shifts if s.person == person) / 60

    def split_shift(self, index: int, at: int) -> None:
        """Cuts a shift in two at minute `at`, both halves kept by the same person."""
        shift = self.shifts[index]
        if not shift.start < at < shift.end:
            raise ValueError("the cut must fall inside the shift")
        self.shifts[index] = Shift(shift.person, shift.start, at)
        self.shifts.insert(index + 1, Shift(shift.person, at, shift.end))
