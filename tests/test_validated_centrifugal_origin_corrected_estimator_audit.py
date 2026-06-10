import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "experiments/validated_centrifugal_origin_corrected_estimator_audit.py"
ARTIFACT = ROOT / "experiments/validated_centrifugal_origin_corrected_estimator.json"


def test_origin_corrected_estimator_audit_reproduces_artifact() -> None:
    expected = ARTIFACT.read_bytes()
    subprocess.run([sys.executable, str(AUDIT)], cwd=ROOT, check=True)
    actual = ARTIFACT.read_bytes()

    assert actual == expected
    record = json.loads(actual)
    assert record["status"] == "pass"
    assert record["result_type"] == "validated_origin_corrected_estimator_terms"
    assert all(record["certified_claims"].values())
    assert hashlib.sha256(actual).hexdigest() == (
        "f7ce2946b2cc2c97bbe75cb5dbc379975a2fc7985efd0ce2ed2953c776189156"
    )
