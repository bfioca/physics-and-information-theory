import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (
    ROOT / "experiments/centrifugal_skyrmion_indicial_majorant_certificate.json"
)


def test_centrifugal_skyrmion_indicial_majorant_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == "exact_post_germ_indicial_inverse_majorant"
    assert record["uniform_bound_below_79_over_1000"]
    dependency = record["authenticated_profile_dependency"]
    dependency_path = ROOT / dependency["path"]
    assert hashlib.sha256(dependency_path.read_bytes()).hexdigest() == dependency[
        "sha256"
    ]
    snapshot = json.loads(dependency_path.read_text(encoding="ascii"))
    assert snapshot["sharp_profile_recipe"]["shooting_slope_interval"] == record[
        "slope_interval"
    ]
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
