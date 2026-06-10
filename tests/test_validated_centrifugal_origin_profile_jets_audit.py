import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "experiments/validated_centrifugal_origin_profile_jets_audit.py"
ARTIFACT = ROOT / "experiments/validated_centrifugal_origin_profile_jets.json"


def test_origin_profile_jet_audit_reproduces_committed_artifact() -> None:
    expected = ARTIFACT.read_bytes()
    subprocess.run([sys.executable, str(AUDIT)], cwd=ROOT, check=True)
    actual = ARTIFACT.read_bytes()

    assert actual == expected
    record = json.loads(actual)
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    assert hashlib.sha256(actual).hexdigest() == (
        "7924fb7da3bb96e92fb43f68cf9311b9ac9a6077292e69474fccf5579abab504"
    )
