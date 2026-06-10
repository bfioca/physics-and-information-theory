import numpy as np
import pytest

from qgtoy.centrifugal_skyrmion_variational import (
    assemble_centrifugal_quadrupole_variational_system,
    centrifugal_quadrupole_variational_convergence_record,
    centrifugal_quadrupole_variational_record,
)


def test_variational_assembly_is_symmetric_and_positive_on_default_space():
    assembled = assemble_centrifugal_quadrupole_variational_system(node_count=31)
    stiffness = assembled["stiffness_matrix"]
    mass = assembled["mass_matrix"]
    assert np.max(np.abs(stiffness - stiffness.T)) < 1.0e-12
    np.linalg.cholesky(stiffness)
    np.linalg.cholesky(mass)
    assert assembled["wall_boundary_form_coefficient"] > 0.0


def test_variational_solution_closes_stationarity_identity():
    record = centrifugal_quadrupole_variational_record(node_count=41)
    assert record["smallest_generalized_ritz_value"] > 0.0
    assert record["stationarity_work_defect"] < 1.0e-10
    assert record["maximum_absolute_radial_field"] < 1.0
    assert record["maximum_absolute_tangential_field"] < 1.0


def test_variational_mesh_probe_passes_with_explicit_claim_boundary():
    record = centrifugal_quadrupole_variational_convergence_record()
    assert record["status"] == "pass"
    assert all(record["verified_numerical_properties"].values())
    assert record["weak_over_strong_maximum_scaled_solution_difference"] < 0.002
    assert "do not prove coercivity" in record["claim_boundary"]


@pytest.mark.parametrize(
    "kwargs",
    (
        {"node_count": 4},
        {"quadrature_order": 1},
        {"wall_radius": 0.0},
        {"curvature": -1.0},
        {"wall_radius": 4.0, "curvature": 1.0},
    ),
)
def test_variational_assembly_rejects_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        assemble_centrifugal_quadrupole_variational_system(**kwargs)
