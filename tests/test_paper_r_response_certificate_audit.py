import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "experiments/paper_r_response_certificate_audit.py"
ARTIFACT = ROOT / "experiments/paper_r_response_certificate.json"


def _load_audit():
    spec = importlib.util.spec_from_file_location("paper_r_response_audit", AUDIT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_paper_r_response_artifact_reproduces_and_applies_stop_rule() -> None:
    module = _load_audit()
    payload = ARTIFACT.read_bytes()
    expected = json.loads(payload)
    assert module.build_record() == expected

    assert expected["status"] == "pass"
    assert expected["decision"] == "INCONCLUSIVE_STOP"
    assert all(expected["certified_claims"].values())
    complete = expected["signed_estimator"]["complete"]
    assert Fraction(complete["upper_exact"]) < 0
    response = expected["full_response"]["exterior_amplitude"]
    assert Fraction(response["lower_exact"]) < 0 < Fraction(
        response["upper_exact"]
    )
    relative = Fraction(expected["full_response"]["relative_radius"]["exact"])
    assert 3 < relative <= 10
    assert not expected["full_response"]["excludes_zero"]
    assert not expected["weyl_and_state_transfer"][
        "state_sensitive_nonzero_conclusion"
    ]

    for relative_path, digest in expected["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest() == digest
    for name, digest in expected["component_artifact_sha256"].items():
        path = module.COMPONENTS[name]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    assert hashlib.sha256(payload).hexdigest() == (
        "bcbb4a1af96b445b84464ddeda83cb6a568b0061bbc5146dd8fc11e72e124292"
    )
