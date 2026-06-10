import json
from pathlib import Path

from experiments.centrifugal_skyrmion_friedrichs_form_audit import (
    OUTPUT,
    build_record,
)


def test_source_hashed_global_friedrichs_form_artifact() -> None:
    expected = json.loads(Path(OUTPUT).read_text(encoding="ascii"))
    actual = build_record()
    assert json.loads(json.dumps(actual)) == expected
    assert actual["theorem"]["closed"] is True
    assert actual["theorem"]["two_sided_inverse_exists"] is True
    assert actual["theorem"]["inverse_norm_upper_bound"] == "100"
    assert actual["theorem"]["compact_resolvent_claimed"] is False
    assert actual["theorem"]["kinetic_mode_gap_claimed"] is False
    assert "does not certify" in actual["claim_boundary"]
