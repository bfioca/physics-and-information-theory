import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/orientation_stabilizer_risk_exact_certificate.json"


def test_orientation_stabilizer_risk_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert (
        record["spin_two_anticoherent_example"]["global_chordal_risk_lower_bound_exact"]
        == "1/2"
    )
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
