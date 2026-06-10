import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_membrane_stress_certificate.json"


def test_centrifugal_skyrmion_membrane_stress_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["result_type"] == (
        "exact_distributional_factorization_and_floating_wall_closure"
    )
    assert (
        max(
            item["maximum_distributional_conservation_coefficient"]
            for item in record["mesh_records"]
        )
        < 2.0e-12
    )
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
