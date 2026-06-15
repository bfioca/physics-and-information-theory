import json
from fractions import Fraction
from pathlib import Path

import pytest

from qgtoy.validated_rational_text import exact_fraction_from_text


ROOT = Path(__file__).resolve().parents[1]
RADIAL_CERTIFICATE = (
    ROOT / "experiments/skyrmion_full_radial_gap_exact_certificate.json"
)


def test_exact_fraction_from_text_parses_integer_and_fraction() -> None:
    assert exact_fraction_from_text("-42") == Fraction(-42)
    assert exact_fraction_from_text("+21/14") == Fraction(3, 2)


def test_exact_fraction_from_text_ignores_interpreter_digit_ceiling() -> None:
    numerator = "9" * 5_000
    value = exact_fraction_from_text(numerator + "/7")
    assert value.denominator == 7
    assert value.numerator % 10 == 9


@pytest.mark.parametrize("value", ["", "1/2/3", "not-a-number"])
def test_exact_fraction_from_text_rejects_malformed_input(value: str) -> None:
    with pytest.raises(ValueError):
        exact_fraction_from_text(value)


def test_exact_fraction_from_text_rejects_zero_denominator() -> None:
    with pytest.raises(ZeroDivisionError):
        exact_fraction_from_text("1/0")


def test_radial_certificate_pins_exact_rational_parser() -> None:
    certificate = json.loads(RADIAL_CERTIFICATE.read_text(encoding="ascii"))
    assert "qgtoy/validated_rational_text.py" in certificate["source_sha256"]
