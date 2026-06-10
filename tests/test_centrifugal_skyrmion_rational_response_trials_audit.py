import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    rational_response_trial_pair_from_record,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"


def test_rational_response_trial_artifact_is_source_bound_and_replays() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    pair = rational_response_trial_pair_from_record(record["trial_archive"])
    pair.validate()
    probe = record["positive_radius_primal_residual_probe"]
    assert probe["cell_count"] == 344
    assert probe["exact_subdivisions_per_authenticated_cell"] == 8
    assert probe["l2_squared_upper_float"] < 4
    convergence = record["positive_radius_primal_residual_convergence"]
    assert [entry["cell_count"] for entry in convergence] == [43, 86, 172, 344]
    assert all(
        left["l2_squared_upper_float"] > right["l2_squared_upper_float"]
        for left, right in zip(convergence, convergence[1:])
    )
    wall = record["primal_wall_conormal"]
    assert wall["residual"]["absolute_upper_float"] < 0.002
    assert float(Fraction(wall["wall_trace_margin"]["lower"])) > 0.2
    assert "no zero exclusion" in record["claim_boundary"]
