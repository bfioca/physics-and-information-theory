import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_frobenius_certificate.json"


def test_centrifugal_skyrmion_frobenius_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == "exact_first_post_indicial_frobenius_recurrence"
    assert record["p5_recurrence_determinant_identity_verified"]
    assert record["all_exact_recurrence_checks_pass"]
    dependency = record["authenticated_profile_dependency"]
    assert dependency["reference_slope_is_inside"]
    interval = dependency["shooting_slope_interval"]
    reference = Fraction(record["reference_slope"])
    assert Fraction(interval["lower"]) <= reference <= Fraction(interval["upper"])
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
