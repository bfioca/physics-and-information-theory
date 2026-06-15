"""Exact parsing for archived rational endpoints."""

from __future__ import annotations

from fractions import Fraction


def _parse_unbounded_integer(value: str) -> int:
    """Parse a decimal integer without Python's long-string safety ceiling."""

    if not isinstance(value, str) or not value:
        raise ValueError("integer text must be nonempty")
    sign = -1 if value.startswith("-") else 1
    digits = value[1:] if value[:1] in {"-", "+"} else value
    if not digits or not digits.isdecimal():
        raise ValueError("invalid integer text")
    result = 0
    width = 1_000
    for start in range(0, len(digits), width):
        chunk = digits[start : start + width]
        result = result * 10 ** len(chunk) + int(chunk)
    return sign * result


def exact_fraction_from_text(value: str) -> Fraction:
    """Parse an archived exact rational, including endpoints with many digits."""

    if not isinstance(value, str) or not value:
        raise ValueError("fraction text must be nonempty")
    pieces = value.split("/")
    if len(pieces) == 1:
        return Fraction(_parse_unbounded_integer(pieces[0]))
    if len(pieces) != 2:
        raise ValueError("invalid fraction text")
    numerator = _parse_unbounded_integer(pieces[0])
    denominator = _parse_unbounded_integer(pieces[1])
    if denominator == 0:
        raise ZeroDivisionError("fraction denominator cannot vanish")
    return Fraction(numerator, denominator)
