import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_deformation_certificate.json"


def test_centrifugal_skyrmion_deformation_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["result_type"] == ("rank_two_quadrupole_deformation_and_wall_gate")
    assert record["coupled_mirror_tension_boundary"]["normal_force_is_balanced"]
    assert (
        abs(record["rotational_source_covector"]["tangential_field_coefficient"])
        > 1.0e-12
    )
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
