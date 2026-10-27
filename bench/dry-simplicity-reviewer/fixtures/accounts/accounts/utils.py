from typing import Iterable, List, TypeVar

T = TypeVar("T")


def chunks(items: List[T], size: int) -> List[List[T]]:
    """Split `items` into lists of at most `size`."""
    out = []
    for start in range(0, len(items), size):
        out.append(items[start:start + size])
    return out


def flatten(lists: Iterable[List[T]]) -> List[T]:
    out = []
    for inner in lists:
        for item in inner:
            out.append(item)
    return out
