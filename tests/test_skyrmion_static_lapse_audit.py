import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/skyrmion_static_lapse_exact_certificate.json"


def test_authenticated_static_lapse_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "complete_fixed_field_static_bulk_lapse_certificate"
    bounds = record["directed_bounds"]
    assert bounds["lapse_coefficient_D_upper_float"] > 0.0
    assert bounds["maximum_log_lapse_drop_float"] > 0.0
    assert 0.0 < bounds["minimum_gtt_ratio_float_diagnostic"] < 1.0
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
