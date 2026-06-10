import json
from pathlib import Path

from experiments.centrifugal_skyrmion_riccati_coercivity_audit import (
    OUTPUT,
    build_record,
)


def test_source_hashed_riccati_route_artifact() -> None:
    expected = json.loads(Path(OUTPUT).read_text(encoding="ascii"))
    actual = build_record()
    assert json.loads(json.dumps(actual)) == expected
    assert actual["exact_identity"]["identity_verified"] is True
    assert actual["floating_candidate"]["candidate_passes_sampled_preflight"] is True
    assert "no continuum eigenvalue" in actual["claim_boundary"]
