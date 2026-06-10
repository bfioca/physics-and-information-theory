import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = (
    ROOT / "experiments/validated_centrifugal_conormal_remainder_certificate.json"
)


def test_validated_centrifugal_conormal_remainder_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == "validated_finite_cell_conormal_origin_transfer"
    assert record["status"] == "pass"
    assert all(record["executable_checks"].values())
    assert float(record["maximum_green_majorant"]["upper"]) < 0.51
    assert float(record["maximum_coefficient_variation_bound"]["upper"]) < 0.15
    assert float(record["maximum_contraction_bound"]["upper"]) < 0.075
    assert float(record["maximum_endpoint_state_error"]["upper"]) < 1e-4
    assert record["branch_order"] == [
        "linear_homogeneous",
        "cubic_homogeneous",
        "forced_particular",
    ]
    assert "physical (f,g,f',g')" in record["claim_boundary"]

    for dependency in record["dependencies"].values():
        path = ROOT / dependency["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == dependency["sha256"]
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
