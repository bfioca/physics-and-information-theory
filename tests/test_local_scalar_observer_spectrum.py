import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from experiments.local_scalar_observer_spectrum import (
    galerkin_cost_estimate,
    vacuum_piecewise_constant_matrix,
)
from qgtoy.local_scalar_observer_cost import sharp_observer_cost_characterization


ROOT = Path(__file__).resolve().parents[1]
DATA = (
    ROOT
    / "paper/local_scalar_observer_cost/data/observer_cost_spectrum.json"
)
FIGURE = (
    ROOT
    / "paper/local_scalar_observer_cost/figures/observer_cost_spectrum.pdf"
)
PREVIEW = (
    ROOT
    / "paper/local_scalar_observer_cost/figures/observer_cost_spectrum.svg"
)


def test_exact_vacuum_cell_matrix_is_symmetric_and_positive() -> None:
    matrix = vacuum_piecewise_constant_matrix(16)
    assert np.max(np.abs(matrix - matrix.T)) < 1.0e-14
    assert np.min(matrix) > 0.0
    assert np.linalg.eigvalsh(matrix)[-1] > 0.0


def test_galerkin_cost_sits_inside_the_rigorous_bracket() -> None:
    support_ratio = 0.3
    cost, profile = galerkin_cost_estimate(
        support_ratio,
        cell_count=32,
        quadrature_order=8,
    )
    bounds = sharp_observer_cost_characterization(
        support_ratio,
        static_patch_radius=1.0,
    )
    assert cost >= bounds["rigorous_lower_coefficient"]
    assert cost <= bounds["exact_row_schur_upper_coefficient"]
    assert np.min(profile) > 0.0


def test_frozen_spectrum_records_convergence_and_provenance() -> None:
    record = json.loads(DATA.read_text(encoding="ascii"))
    assert record["status"] == "numerical_convergence_pass_nonrigorous"
    assert record["checks"]["all_curve_estimates_inside_rigorous_bracket"]
    assert record["checks"]["nested_resolution_estimates_monotone"]
    assert record["checks"]["maximum_last_resolution_relative_step"] < 5.1e-5
    assert record["checks"]["maximum_quadrature_relative_difference"] < 1.0e-12
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected
    assert hashlib.sha256(FIGURE.read_bytes()).hexdigest() == record["figure"][
        "sha256"
    ]
    assert FIGURE.read_bytes().startswith(b"%PDF-1.4")
    assert hashlib.sha256(PREVIEW.read_bytes()).hexdigest() == record["figure"][
        "preview_sha256"
    ]
    assert PREVIEW.read_text(encoding="ascii").startswith("<svg")


@pytest.mark.parametrize(
    ("support_ratio", "expected"),
    ((0.1, 0.099726435765251), (1.0, 1.0295979905445), (10.0, 27.717036546097)),
)
def test_frozen_curve_contains_reference_values(
    support_ratio: float,
    expected: float,
) -> None:
    record = json.loads(DATA.read_text(encoding="ascii"))
    row = next(
        item
        for item in record["curve"]
        if item["support_ratio_y"] == support_ratio
    )
    assert row["galerkin_cost"] == pytest.approx(expected)
