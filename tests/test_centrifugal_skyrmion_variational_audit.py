import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_variational_certificate.json"


def test_centrifugal_skyrmion_variational_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert record["result_type"] == "floating_weak_form_spectral_probe"
    assert all(record["verified_numerical_properties"].values())
    assert min(record["smallest_generalized_ritz_values"]) > 0.0
    assert record["weak_over_strong_maximum_scaled_solution_difference"] < 0.002
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
