import numpy as np
import pytest

from qgtoy.centrifugal_skyrmion_bvp import (
    _block_tridiagonal_solve,
    centrifugal_quadrupole_mesh_convergence_record,
    solve_centrifugal_quadrupole_bvp,
)


def test_block_tridiagonal_solver_matches_dense_system():
    diagonal = np.asarray(
        (
            ((4.0, 0.2), (0.1, 3.5)),
            ((5.0, -0.1), (0.3, 4.5)),
            ((3.8, 0.4), (-0.2, 4.2)),
        )
    )
    lower = np.zeros_like(diagonal)
    upper = np.zeros_like(diagonal)
    lower[1] = ((-0.5, 0.1), (0.0, -0.4))
    lower[2] = ((-0.3, 0.0), (0.2, -0.6))
    upper[0] = ((-0.4, 0.0), (0.1, -0.2))
    upper[1] = ((-0.2, 0.3), (0.0, -0.5))
    rhs = np.asarray(((1.0, 2.0), (0.5, -1.0), (3.0, 0.25)))
    solution = _block_tridiagonal_solve(lower, diagonal, upper, rhs)

    dense = np.zeros((6, 6))
    for index in range(3):
        dense[2 * index : 2 * index + 2, 2 * index : 2 * index + 2] = diagonal[index]
        if index > 0:
            dense[2 * index : 2 * index + 2, 2 * index - 2 : 2 * index] = lower[index]
        if index < 2:
            dense[2 * index : 2 * index + 2, 2 * index + 2 : 2 * index + 4] = upper[
                index
            ]
    expected = np.linalg.solve(dense, rhs.reshape(-1)).reshape(3, 2)
    assert solution == pytest.approx(expected)


def test_default_centrifugal_bvp_closes_linear_and_wall_residuals():
    record = solve_centrifugal_quadrupole_bvp(node_count=81)
    assert record["linear_system_maximum_residual"] < 1.0e-8
    assert abs(record["wall_robin_residual"]) < 1.0e-10
    assert abs(record["wall_tangential_field"]) < 1.0e-12
    assert record["origin_regular_subspace"]["linear_mode_f_over_g"] == pytest.approx(
        -1.0, rel=1.0e-5
    )


def test_default_mesh_convergence_record_passes():
    record = centrifugal_quadrupole_mesh_convergence_record()
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())


@pytest.mark.parametrize(
    "kwargs",
    (
        {"node_count": 4},
        {"origin_radius": 0.0},
        {"origin_radius": 4.0},
        {"wall_radius": 50.0},
    ),
)
def test_centrifugal_bvp_rejects_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        solve_centrifugal_quadrupole_bvp(**kwargs)
