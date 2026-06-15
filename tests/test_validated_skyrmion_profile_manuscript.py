import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "paper/validated_skyrmion_profile/audit_package.py"
AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"


def _run_audit(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(AUDIT), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_checked_manuscript_package_passes_audit() -> None:
    completed = _run_audit()
    assert completed.returncode == 0, completed.stdout + completed.stderr
    report = json.loads(completed.stdout)
    assert report["status"] == "pass"
    assert report["checked_manuscript_files"] == 13
    assert report["checked_proof_certificates"] == 2
    assert report["checked_proof_inputs"] == 1
    assert report["checked_claim_bounds"] == 3


def test_au2_replay_ignores_only_volatile_provenance(tmp_path: Path) -> None:
    replay = json.loads(AU2.read_text(encoding="ascii"))
    replay["command"] = ["different", "output", "path"]
    replay["dependency_versions"] = {
        "python": "another supported interpreter",
        "numpy": "not installed",
    }
    replay_path = tmp_path / "replay.json"
    replay_path.write_text(
        json.dumps(replay, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )

    completed = _run_audit("--replay-au2", str(replay_path))
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_au2_replay_rejects_mathematical_change(tmp_path: Path) -> None:
    replay = json.loads(AU2.read_text(encoding="ascii"))
    replay["exact_outputs"]["radius"] = "1/249"
    replay_path = tmp_path / "tampered.json"
    replay_path.write_text(
        json.dumps(replay, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )

    completed = _run_audit("--replay-au2", str(replay_path))
    assert completed.returncode != 0
    assert "AU.2 replay payload mismatch" in completed.stdout
