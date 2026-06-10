import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/skyrmion_rotational_backreaction_exact_certificate.json"


def test_authenticated_rotational_backreaction_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "complete_conditional_collective_backreaction_certificate"
    result = record["theorem_result"]
    assert result["maximum_mean_casimir_float"] > 0.0
    assert result["global_orientation_risk_lower_bound_float"] > 0.0
    assert record["directed_decimal_compression"]["static_bulk_mass_lower_float"] > 33.0
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
