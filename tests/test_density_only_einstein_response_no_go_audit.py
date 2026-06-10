import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/density_only_einstein_response_no_go_certificate.json"


def test_density_only_einstein_response_no_go_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["density_only_counterexample"]["energy_density_norm"] == 0.0
    assert record["density_only_counterexample"][
        "nonzero_curvature_at_zero_energy_density"
    ]
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
