import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "experiments/validated_centrifugal_origin_adjoint_load_audit.py"
ARTIFACT = ROOT / "experiments/validated_centrifugal_origin_adjoint_load.json"


def test_origin_adjoint_load_audit_reproduces_committed_artifact() -> None:
    expected = ARTIFACT.read_bytes()
    subprocess.run([sys.executable, str(AUDIT)], cwd=ROOT, check=True)
    actual = ARTIFACT.read_bytes()

    assert actual == expected
    record = json.loads(actual)
    assert record["status"] == "pass"
    assert record["result_type"] == ("loaded_regular_origin_adjoint_strong_residual")
    assert all(record["certified_claims"].values())
    assert hashlib.sha256(actual).hexdigest() == (
        "0f6f5e42be8906eb863e11f827eb8b93d47d59ddc576be73acb185b13d91c52e"
    )
