import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_master_response_certificate.json"


def test_centrifugal_skyrmion_master_response_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["result_type"] == (
        "floating_conserved_skyrmion_zerilli_moncrief_response"
    )
    assert record["fine_mesh_maximum_relative_difference"] < 1.0e-3
    assert record["fine_origin_maximum_relative_difference"] < 1.0e-3
    assert record["fine_profile_maximum_relative_difference"] < 1.0e-4
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
