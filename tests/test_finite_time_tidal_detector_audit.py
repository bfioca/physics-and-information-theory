import json
from pathlib import Path

from experiments.finite_time_tidal_detector_audit import OUTPUT, build_record


def test_source_hashed_finite_time_tidal_detector_artifact() -> None:
    expected = json.loads(Path(OUTPUT).read_text(encoding="ascii"))
    actual = build_record()
    assert json.loads(json.dumps(actual)) == expected
    assert actual["status"] == "pass"
    assert all(actual["certified_claims"].values())
    assert "does not derive" in actual["claim_boundary"]
