import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/centrifugal_skyrmion_friedrichs_trace_certificate.json"


def test_centrifugal_skyrmion_friedrichs_trace_artifact() -> None:
    record = json.loads(ARTIFACT.read_text(encoding="ascii"))
    assert record["result_type"] == "local_solution_germ_friedrichs_admissibility"
    assert record["status"] == "pass"
    assert all(record["executable_checks"].values())
    assert record["finite_energy_homogeneous_powers"] == [1, 3]
    assert record["excluded_singular_powers"] == [-2, -4]
    assert record["homogeneous_solution_trace_dimension"] == 2
    assert "does not classify the entire form domain" in record["claim_boundary"]

    dependency = record["validated_physical_transfer_dependency"]
    dependency_path = ROOT / dependency["path"]
    assert (
        hashlib.sha256(dependency_path.read_bytes()).hexdigest() == dependency["sha256"]
    )
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
