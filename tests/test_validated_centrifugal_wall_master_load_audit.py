import hashlib
import json
from fractions import Fraction
from pathlib import Path

from experiments.validated_centrifugal_wall_master_load_audit import build_record
from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    rational_response_trial_pair_from_record,
)
from qgtoy.validated_centrifugal_response_residual import (
    validated_wall_conormal_coefficients,
)
from qgtoy.validated_centrifugal_wall_master_load import (
    DEFAULT_WALL_SLOPE,
    loaded_adjoint_wall_residual,
    validated_wall_master_load,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/validated_centrifugal_wall_master_load.json"


def test_wall_master_load_artifact_replays_exactly() -> None:
    archived = json.loads(ARTIFACT.read_text())
    assert build_record() == archived
    for source, expected in archived["source_sha256"].items():
        assert hashlib.sha256((ROOT / source).read_bytes()).hexdigest() == expected


def test_archived_adjoint_has_certified_loaded_wall_residual() -> None:
    archive = json.loads(
        (ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json").read_text()
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    load = validated_wall_master_load()
    coefficients = validated_wall_conormal_coefficients(DEFAULT_WALL_SLOPE)
    residual = loaded_adjoint_wall_residual(
        trial=pair.adjoint.positive_radius_cells[-1],
        coefficients=coefficients,
        master_load=load,
    )
    assert residual.lower > 0
    assert residual.upper < Fraction(1, 150)
