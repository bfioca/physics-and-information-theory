import json
from fractions import Fraction
from pathlib import Path

from experiments.centrifugal_skyrmion_liouville_origin_audit import (
    OUTPUT,
    build_record,
)


def test_source_hashed_origin_liouville_artifact() -> None:
    expected = json.loads(Path(OUTPUT).read_text(encoding="ascii"))
    actual = build_record()
    assert json.loads(json.dumps(actual)) == expected
    assert actual["summary"]["coercivity_verified"] is True
    assert Fraction(actual["summary"]["minimum_scaled_first_minor"]) > 0
    assert Fraction(actual["summary"]["minimum_scaled_determinant"]) > 0
    assert "remain open" in actual["claim_boundary"]
