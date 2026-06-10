import json
from pathlib import Path

from experiments.centrifugal_affine_master_kernel_audit import OUTPUT, build_record


def test_source_hashed_affine_master_kernel_artifact() -> None:
    expected = json.loads(Path(OUTPUT).read_text(encoding="ascii"))
    actual = build_record()
    assert json.loads(json.dumps(actual)) == expected
    assert actual["status"] == "pass"
    assert all(actual["certified_claims"].values())
    assert "does not enclose" in actual["claim_boundary"]
