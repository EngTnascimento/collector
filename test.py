from typing import Optional


def sum(a: int, b: int):
    return a + b


def double(n: int):
    return n * 2


a: Optional[int] = None
b: Optional[int] = 2

d = sum(a, b) if a and b else double(a or b)


print(d)
