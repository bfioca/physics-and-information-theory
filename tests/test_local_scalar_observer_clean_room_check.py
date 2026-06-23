import ast
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.local_scalar_observer_clean_room_check import (
    build_record,
    midpoint_product_matrix,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/local_scalar_observer_clean_room_check.py"
RECORD = ROOT / "experiments/local_scalar_observer_clean_room_check.json"


def test_clean_room_matrix_is_symmetric_with_positive_top_vector() -> None:
    matrix = midpoint_product_matrix(24, 0.5, diagonal_order=12)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    vector = eigenvectors[:, -1]
    if np.sum(vector) < 0.0:
        vector = -vector
    assert np.max(np.abs(matrix - matrix.T)) < 1.0e-13
    assert eigenvalues[-1] > 0.0
    assert np.min(vector) > 0.0


def test_clean_room_checker_passes_without_production_imports() -> None:
    imported_roots = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(ast.parse(SOURCE.read_text(encoding="ascii")))
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".", 1)[0]
        for node in ast.walk(ast.parse(SOURCE.read_text(encoding="ascii")))
        if isinstance(node, ast.ImportFrom) and node.module
    )
    assert "qgtoy" not in imported_roots
    assert "local_scalar_observer_spectrum" not in SOURCE.read_text(encoding="ascii")
    record = build_record(cell_count=64, diagonal_order=16)
    assert record["status"] == "pass_independent_computation_nonrigorous"
    assert all(
        value is True
        for key, value in record["checks"].items()
        if key != "maximum_coarse_to_fine_relative_step"
    )


def test_frozen_clean_room_record_has_current_provenance() -> None:
    record = json.loads(RECORD.read_text(encoding="ascii"))
    assert record["status"] == "pass_independent_computation_nonrigorous"
    assert record["method"]["production_imports"] == []
    assert record["checks"]["small_support_remainder_bound_holds_on_grid"]
    assert record["checks"]["large_support_remainder_bound_holds_on_grid"]
    assert record["checks"]["coordinate_bound_strictly_below_momentum_lower_envelope"]
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
