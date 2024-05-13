from typing import Callable, Iterable, Optional, TypeVar

T = TypeVar("T")


def first(iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    try:
        return next(el for el in iterable if predicate(el))
    except StopIteration:
        return None


def find_idx(iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[int]:
    result = first(enumerate(iterable), lambda idx2el: predicate(idx2el[1]))
    if result is None:
        return None
    return result[0]
