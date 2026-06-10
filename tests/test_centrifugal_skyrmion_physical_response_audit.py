import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (
    ROOT / "experiments/centrifugal_skyrmion_physical_response_certificate.json"
)


def test_centrifugal_skyrmion_physical_response_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["result_type"] == (
        "physical_state_dependent_skyrmion_master_amplitude"
    )
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
