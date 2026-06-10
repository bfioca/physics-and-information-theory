import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_bvp_certificate.json"


def test_centrifugal_skyrmion_bvp_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["result_type"] == "unvalidated_two_channel_bvp_mesh_convergence"
    assert record["fine_over_medium_maximum_scaled_difference"] < 0.001
    assert record["fine_over_medium_origin_maximum_scaled_difference"] < 0.001
    assert record["fine_over_medium_profile_maximum_scaled_difference"] < 0.001
    finest = record["finest_record"]
    assert finest["maximum_absolute_radial_field"] < 1.0
    assert finest["maximum_absolute_tangential_field"] < 1.0
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
