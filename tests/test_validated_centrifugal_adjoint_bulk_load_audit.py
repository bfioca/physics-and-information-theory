import json
from pathlib import Path

from experiments.validated_centrifugal_adjoint_bulk_load_audit import build_record


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/validated_centrifugal_adjoint_bulk_load.json"


def test_validated_adjoint_bulk_load_artifact_replays() -> None:
    assert build_record() == json.loads(ARTIFACT.read_text(encoding="ascii"))
