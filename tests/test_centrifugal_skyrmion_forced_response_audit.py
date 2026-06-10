import json
from pathlib import Path

from experiments.centrifugal_skyrmion_forced_response_audit import (
    OUTPUT,
    build_record,
)


def test_source_hashed_nonzero_weak_response_artifact() -> None:
    expected = json.loads(Path(OUTPUT).read_text(encoding="ascii"))
    actual = build_record()
    assert json.loads(json.dumps(actual)) == expected
    assert actual["theorem"]["source_is_nonzero"] is True
    assert actual["theorem"]["weak_solution_is_nonzero"] is True
    assert actual["theorem"]["source_conjugate_susceptibility_positive"] is True
    assert actual["theorem"]["l2_inverse_bound_applies_directly"] is True
    assert actual["theorem"]["master_or_weyl_response_certified"] is False
