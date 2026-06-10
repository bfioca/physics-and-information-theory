import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (
    ROOT / "experiments/centrifugal_skyrmion_transformed_origin_certificate.json"
)


def test_centrifugal_skyrmion_transformed_origin_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == "exact_transformed_origin_density_identity"
    assert record["negative_powers_of_t_in_H_hat"] == 0
    assert all(record["exact_fraction_center_checks"])
    assert record["forced_cubic_compatibility"]["source_is_in_range_of_K3"]
    assert record["maximum_floating_direct_replay_relative_error"] < 2.0e-15
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
