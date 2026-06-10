import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/skyrmion_tidal_reference_discriminator_certificate.json"


def test_skyrmion_tidal_reference_discriminator_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert record["result_type"] == (
        "instantaneous_exterior_tidal_gradiometer_contrast"
    )
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
