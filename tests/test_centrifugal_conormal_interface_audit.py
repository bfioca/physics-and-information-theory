import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_conormal_interface_certificate.json"


def test_conormal_interface_artifact_is_source_bound() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    assert record["certificates"]["primal"][
        "internal_conormal_jump_is_exactly_zero"
    ]
    assert record["certificates"]["adjoint"][
        "internal_conormal_jump_is_exactly_zero"
    ]
