import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_origin_certificate.json"


def test_centrifugal_skyrmion_origin_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == "exact_rational_origin_indicial_identity"
    assert record["quartic_factorization_verified"]
    assert record["principal_block_positive_for_every_real_slope"]
    assert all(record["root_determinant_polynomials_vanish"].values())
    robin = record["leading_robin_matrix_enclosure"]
    assert all(Fraction(entry["lower"]) > 0 for row in robin for entry in row)
    dependency = record["authenticated_profile_dependency"]
    dependency_path = ROOT / dependency["path"]
    assert hashlib.sha256(dependency_path.read_bytes()).hexdigest() == dependency[
        "sha256"
    ]
    snapshot = json.loads(dependency_path.read_text(encoding="ascii"))
    assert snapshot["sharp_profile_recipe"]["shooting_slope_interval"] == record[
        "authenticated_slope_interval"
    ]
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
