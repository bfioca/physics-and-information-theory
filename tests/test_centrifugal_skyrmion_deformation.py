from math import cos, sin

import pytest

from qgtoy.centrifugal_skyrmion_deformation import (
    centrifugal_deformation_kinematics_certificate,
    comoving_pure_tension_quadrupole_boundary,
    direct_vector_deformation_invariants,
    equivariant_deformation_multipoles,
    fixed_spherical_wall_quadrupole_traction,
    hard_wall_background_pressure_derivative,
    hata_quadrupole_physical_fields,
    ideal_mirror_pullback_residuals,
    pure_tension_wall_shape_balance,
    quadrupole_static_hessian_density,
    quadrupole_static_hessian_matrix,
    required_comoving_wall_displacement,
    rotational_quadrupole_source_covector,
    scalar_quadrupole_restricted_equation,
    static_patch_shell_shape_curvature_coefficient,
)


def test_equivariant_deformation_has_two_independent_quadrupole_channels():
    record = equivariant_deformation_multipoles(
        radius=2.0,
        function_a=3.0,
        function_b=0.5,
        function_c=1.0,
    )
    assert record["radial_monopole_coefficient"] == pytest.approx(8.0 / 3.0)
    assert record["radial_quadrupole_coefficient"] == pytest.approx(-16.0)
    assert record["tangential_quadrupole_coefficient"] == pytest.approx(8.0)
    assert record["quadrupole_response_rank"] == 2
    assert record["quadrupole_coefficient_map_determinant"] == -1.0


def test_direct_deformation_matches_multipole_decomposition():
    radius = 1.7
    omega_squared = 2.3
    omega_dot_direction = 0.8
    a_value = 0.7
    b_value = -0.2
    c_value = 0.4
    direct = direct_vector_deformation_invariants(
        radius=radius,
        omega_squared=omega_squared,
        omega_dot_direction=omega_dot_direction,
        function_a=a_value,
        function_b=b_value,
        function_c=c_value,
    )
    multipoles = equivariant_deformation_multipoles(
        radius=radius,
        function_a=a_value,
        function_b=b_value,
        function_c=c_value,
    )
    p2 = omega_dot_direction**2 - omega_squared / 3.0
    reconstructed = (
        multipoles["radial_monopole_coefficient"] * omega_squared
        + multipoles["radial_quadrupole_coefficient"] * p2
    )
    assert direct["radial_displacement"] == pytest.approx(reconstructed)


def test_fixed_wall_conditions_cancel_both_pullback_sectors():
    record = ideal_mirror_pullback_residuals(
        wall_radius=4.0,
        function_a_at_wall=0.75,
        function_b_at_wall=0.0,
        function_c_at_wall=0.75,
    )
    assert record["ideal_mirror_pullback_is_satisfied"]
    assert record["monopole_pullback_residual"] == 0.0
    assert record["quadrupole_pullback_residual"] == 0.0


def test_comoving_wall_cancels_arbitrary_boundary_deformation():
    record = required_comoving_wall_displacement(
        wall_radius=3.0,
        function_a_at_wall=0.9,
        function_b_at_wall=-0.2,
        function_c_at_wall=0.1,
    )
    assert record["pullback_check_passes"]


def test_fixed_spherical_wall_generically_needs_quadrupole_reaction():
    record = fixed_spherical_wall_quadrupole_traction(
        wall_radius=4.0,
        wall_metric_factor=0.96,
        wall_profile_derivative=-0.0878757998,
        derivative_of_a_minus_c_at_wall=0.2,
    )
    expected = -0.96 * 0.0878757998**2 * 4.0**3 * 0.2 / 4.0
    assert record["quadrupole_radial_pressure_coefficient"] == pytest.approx(expected)
    assert not record["unanchored_fixed_spherical_wall_is_force_balanced"]


def test_flat_shell_shape_jacobi_coefficients():
    radius = 5.0
    records = tuple(
        static_patch_shell_shape_curvature_coefficient(
            wall_radius=radius,
            curvature=0.0,
            ell=ell,
        )
        for ell in range(3)
    )
    assert records[0]["shape_curvature_coefficient"] == pytest.approx(-2.0 / radius**2)
    assert records[1]["shape_curvature_coefficient"] == pytest.approx(0.0)
    assert records[2]["shape_curvature_coefficient"] == pytest.approx(4.0 / radius**2)


def test_pure_tension_quadrupole_shape_can_balance_intrinsic_pressure():
    pressure_derivative = hard_wall_background_pressure_derivative(
        wall_radius=4.0,
        curvature=0.0025,
        wall_profile_derivative=-0.0878757998,
    )["background_pressure_radial_derivative"]
    trial = pure_tension_wall_shape_balance(
        wall_radius=4.0,
        curvature=0.0025,
        ell=2,
        membrane_tension=0.001931779647,
        background_pressure_radial_derivative=pressure_derivative,
        intrinsic_pressure_multipole=0.0001,
        wall_displacement_coefficient=0.0,
    )
    assert trial["shape_curvature_coefficient"] > 0.0
    assert trial["required_wall_displacement_coefficient"] is not None
    balanced = pure_tension_wall_shape_balance(
        wall_radius=4.0,
        curvature=0.0025,
        ell=2,
        membrane_tension=0.001931779647,
        background_pressure_radial_derivative=pressure_derivative,
        intrinsic_pressure_multipole=0.0001,
        wall_displacement_coefficient=trial["required_wall_displacement_coefficient"],
    )
    assert balanced["normal_force_is_balanced"]


def test_hard_wall_background_pressure_derivative_uses_local_profile_equation():
    record = hard_wall_background_pressure_derivative(
        wall_radius=4.0,
        curvature=0.0025,
        wall_profile_derivative=-0.0878757998,
    )
    derivative_squared = 0.0878757998**2
    expected = 0.0025 * 4.0 * derivative_squared / 4.0 - (
        0.96 * derivative_squared / 8.0
    )
    assert record["background_pressure_radial_derivative"] == pytest.approx(expected)


def test_scalar_quadrupole_source_matches_rigid_radial_conservation_defect():
    from qgtoy.rigid_skyrmion_stress_conservation import (
        rigid_skyrmion_l2_conservation_residuals,
    )

    inputs = {
        "radius": 1.3,
        "metric_factor": 0.92,
        "profile": 1.1,
        "profile_derivative": -0.37,
        "profile_second_derivative": 0.16,
    }
    scalar = scalar_quadrupole_restricted_equation(
        **inputs,
        metric_factor_derivative=-0.0065,
        pion_mass=1.0,
    )
    rigid = rigid_skyrmion_l2_conservation_residuals(
        **inputs,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=1.0,
    )
    assert scalar["rigid_radial_conservation_residual_coefficient"] == pytest.approx(
        rigid["radial_conservation_residual_coefficient"]
    )
    assert scalar["rigid_angular_conservation_residual_coefficient"] == pytest.approx(
        rigid["angular_conservation_residual_coefficient"]
    )
    assert scalar["radial_hilbert_identity_residual"] == pytest.approx(0.0)


def test_hata_map_exhibits_radial_and_tangential_physical_fields():
    record = hata_quadrupole_physical_fields(
        radius=2.0,
        profile=1.0,
        profile_derivative=-0.5,
        function_a_minus_c=0.25,
        function_c=0.75,
    )
    assert record["radial_profile_field_f"] == pytest.approx(1.0)
    assert record["tangential_orientation_field_g"] == pytest.approx(3.0 * sin(1.0))


def test_comoving_mirror_and_pure_tension_give_robin_boundary_condition():
    trial = comoving_pure_tension_quadrupole_boundary(
        wall_radius=4.0,
        curvature=0.0025,
        membrane_tension=0.001931779647,
        wall_profile_derivative=-0.0878757998,
        function_a_minus_c_at_wall=0.01,
        derivative_of_a_minus_c_at_wall=0.0,
    )
    assert trial["mirror_required_wall_quadrupole_displacement"] == pytest.approx(0.64)
    balanced = comoving_pure_tension_quadrupole_boundary(
        wall_radius=4.0,
        curvature=0.0025,
        membrane_tension=0.001931779647,
        wall_profile_derivative=-0.0878757998,
        function_a_minus_c_at_wall=0.01,
        derivative_of_a_minus_c_at_wall=trial[
            "required_derivative_of_a_minus_c_at_wall"
        ],
    )
    assert balanced["normal_force_is_balanced"]


def test_coupled_hessian_radial_principal_block_matches_scalar_jacobi_form():
    radius = 1.4
    metric_factor = 0.91
    profile = 1.0
    profile_derivative = -0.43
    density = quadrupole_static_hessian_density(
        radius=radius,
        metric_factor=metric_factor,
        profile=profile,
        profile_derivative=profile_derivative,
        radial_field=0.0,
        tangential_field=0.0,
        radial_field_derivative=1.0,
        tangential_field_derivative=0.0,
        pion_mass=1.0,
    )
    expected = 4.0 / 45.0 * metric_factor * (radius**2 + 8.0 * sin(profile) ** 2) / 4.0
    assert density == pytest.approx(expected)


def test_coupled_hessian_matrix_is_symmetric_and_has_positive_principal_block():
    record = quadrupole_static_hessian_matrix(
        radius=1.4,
        metric_factor=0.91,
        profile=1.0,
        profile_derivative=-0.43,
        pion_mass=1.0,
    )
    matrix = record["symmetric_hessian_matrix"]
    for row in range(4):
        for column in range(4):
            assert matrix[row][column] == pytest.approx(matrix[column][row])
    assert record["radial_field_principal_coefficient"] > 0.0
    assert record["tangential_field_principal_coefficient"] > 0.0


def test_rotational_source_covector_contains_required_tangential_forcing():
    radius = 1.4
    metric_factor = 0.91
    profile = 1.0
    profile_derivative = -0.43
    record = rotational_quadrupole_source_covector(
        radius=radius,
        metric_factor=metric_factor,
        profile=profile,
        profile_derivative=profile_derivative,
    )
    q_squared_average = 4.0 / 45.0
    sine = sin(profile)
    cosine = cos(profile)
    h_f = (
        radius**2
        * sine
        * cosine
        * (1.0 / (4.0 * metric_factor) + profile_derivative**2)
        + 2.0 * sine**3 * cosine / metric_factor
    )
    h_f_prime = radius**2 * sine**2 * profile_derivative
    assert record["radial_field_coefficient"] == pytest.approx(-q_squared_average * h_f)
    assert record["radial_field_derivative_coefficient"] == pytest.approx(
        -q_squared_average * h_f_prime
    )
    assert abs(record["tangential_field_coefficient"]) > 1.0e-12


def test_coupled_hessian_scalar_schur_block_reproduces_ell2_potential():
    radius = 1.4
    metric_factor = 0.91
    metric_factor_derivative = -0.007
    profile = 1.0
    profile_derivative = -0.43
    profile_second_derivative = 0.18
    pion_mass = 1.0
    step = 1.0e-6

    center = quadrupole_static_hessian_matrix(
        radius=radius,
        metric_factor=metric_factor,
        profile=profile,
        profile_derivative=profile_derivative,
        pion_mass=pion_mass,
    )["symmetric_hessian_matrix"]
    plus = quadrupole_static_hessian_matrix(
        radius=radius + step,
        metric_factor=metric_factor + metric_factor_derivative * step,
        profile=(
            profile
            + profile_derivative * step
            + profile_second_derivative * step**2 / 2.0
        ),
        profile_derivative=profile_derivative + profile_second_derivative * step,
        pion_mass=pion_mass,
    )["symmetric_hessian_matrix"]
    minus = quadrupole_static_hessian_matrix(
        radius=radius - step,
        metric_factor=metric_factor - metric_factor_derivative * step,
        profile=(
            profile
            - profile_derivative * step
            + profile_second_derivative * step**2 / 2.0
        ),
        profile_derivative=profile_derivative - profile_second_derivative * step,
        pion_mass=pion_mass,
    )["symmetric_hessian_matrix"]
    mixed_derivative = (plus[0][2] - minus[0][2]) / (2.0 * step)
    scalar_operator = scalar_quadrupole_restricted_equation(
        radius=radius,
        metric_factor=metric_factor,
        metric_factor_derivative=metric_factor_derivative,
        profile=profile,
        profile_derivative=profile_derivative,
        profile_second_derivative=profile_second_derivative,
        pion_mass=pion_mass,
    )
    expected = (4.0 / 45.0) * scalar_operator["ell2_jacobi_potential"] / 4.0
    assert center[0][0] - mixed_derivative == pytest.approx(
        expected, rel=1.0e-8, abs=1.0e-10
    )


def test_kinematic_certificate_passes():
    record = centrifugal_deformation_kinematics_certificate()
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())


@pytest.mark.parametrize(
    "kwargs",
    (
        {"radius": 0.0, "omega_squared": 1.0, "omega_dot_direction": 0.0},
        {"radius": 1.0, "omega_squared": -1.0, "omega_dot_direction": 0.0},
        {"radius": 1.0, "omega_squared": 1.0, "omega_dot_direction": 2.0},
    ),
)
def test_direct_deformation_rejects_invalid_invariants(kwargs):
    with pytest.raises(ValueError):
        direct_vector_deformation_invariants(
            **kwargs,
            function_a=0.0,
            function_b=0.0,
            function_c=0.0,
        )
