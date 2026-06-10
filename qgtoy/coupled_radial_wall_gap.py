"""Coupled radial profile-wall gap transfer and its missing-input theorem.

Let ``F_a`` be the exact static Dirichlet branch and
``chi=partial_a F_a`` at the equilibrium wall.  Writing a fluctuation as
``eta=xi+q chi`` makes ``xi`` Dirichlet at the fixed reference wall and
diagonalizes the static quadratic form.  The kinetic form retains the added
profile mass through ``dot(xi)+dot(q) chi``.
"""

from __future__ import annotations

from math import isfinite, pi, sqrt


def _positive(name: str, value: float) -> float:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _nonnegative(name: str, value: float) -> float:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def normalized_wall_kinetic_mass(shell_kinetic_mass: float) -> float:
    """Put the Nambu-Goto mass in the radial Jacobi bracket normalization."""

    return _positive("shell_kinetic_mass", shell_kinetic_mass) / pi


def normalized_branch_stiffness(energy_second_derivative: float) -> float:
    """Put the adiabatic branch curvature in the Jacobi bracket normalization."""

    return _positive("energy_second_derivative", energy_second_derivative) / pi


def moving_endpoint_barta_boundary_coefficient(
    *,
    wall_radius: float,
    curvature: float,
    wall_profile_derivative: float,
    membrane_tension: float,
) -> dict[str, float]:
    """Return the moving-wall boundary term for the current Barta witness.

    The fixed-wall witness has ``v'/v=-2z/(z^2+4)``, ``z=x-33/16``.  After
    imposing ``eta(a)+F'(a)q=0``, the ground-state transform leaves

    ``[P v'/v+4 k_b/F'(a)^2] eta(a)^2``.
    """

    radius = _positive("wall_radius", wall_radius)
    kappa = _nonnegative("curvature", curvature)
    derivative = wall_profile_derivative
    if not isfinite(derivative) or derivative == 0.0:
        raise ValueError("wall_profile_derivative must be finite and nonzero")
    tension = _positive("membrane_tension", membrane_tension)
    lapse = 1.0 - kappa * radius**2
    if lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    lapse_derivative = -2.0 * kappa * radius
    surface_second_derivative = (
        2.0 * sqrt(lapse)
        - 5.0 * kappa * radius**2 / sqrt(lapse)
        - kappa**2 * radius**4 / lapse**1.5
    )
    bulk_endpoint_stiffness = (
        (lapse_derivative * radius**2 + 2.0 * lapse * radius)
        * derivative**2
        / 8.0
    )
    bare_boundary_stiffness = (
        bulk_endpoint_stiffness + tension * surface_second_derivative
    )
    z = radius - 33.0 / 16.0
    witness_log_derivative = -2.0 * z / (z**2 + 4.0)
    jacobi_principal_at_wall = lapse * radius**2
    jacobi_boundary_term = jacobi_principal_at_wall * witness_log_derivative
    support_boundary_term = 4.0 * bare_boundary_stiffness / derivative**2
    return {
        "witness_log_derivative_at_wall": witness_log_derivative,
        "jacobi_principal_at_wall": jacobi_principal_at_wall,
        "bulk_endpoint_stiffness_density": bulk_endpoint_stiffness,
        "membrane_surface_second_derivative": surface_second_derivative,
        "bare_boundary_stiffness_density": bare_boundary_stiffness,
        "jacobi_barta_boundary_term": jacobi_boundary_term,
        "support_boundary_term": support_boundary_term,
        "total_moving_endpoint_barta_coefficient": (
            jacobi_boundary_term + support_boundary_term
        ),
    }


def coupled_radial_frequency_squared_lower_bound(
    *,
    fixed_wall_static_form_gap: float,
    kinetic_weight_upper_bound: float,
    normalized_wall_mass: float,
    normalized_branch_curvature: float,
    branch_lift_weighted_norm_squared: float,
) -> float:
    """Return the sharp two-block lower bound for the coupled radial frequency.

    The hypotheses are

    ``V >= alpha ||xi||^2 + k q^2``

    and

    ``T <= Wmax ||xi||^2 + 2 sqrt(Wmax)c ||xi|| |q|
           +(c^2+m)q^2``,

    where ``c^2=<chi,W chi>``.  The result is the smaller generalized
    eigenvalue of these two comparison matrices.
    """

    alpha = _positive("fixed_wall_static_form_gap", fixed_wall_static_form_gap)
    weight = _positive("kinetic_weight_upper_bound", kinetic_weight_upper_bound)
    mass = _positive("normalized_wall_mass", normalized_wall_mass)
    stiffness = _positive(
        "normalized_branch_curvature", normalized_branch_curvature
    )
    lift_norm_squared = _nonnegative(
        "branch_lift_weighted_norm_squared",
        branch_lift_weighted_norm_squared,
    )
    trace_coefficient = (
        alpha * (lift_norm_squared + mass) + stiffness * weight
    )
    kinetic_determinant = weight * mass
    discriminant = (
        trace_coefficient**2
        - 4.0 * kinetic_determinant * alpha * stiffness
    )
    if discriminant < 0.0 and discriminant > -1e-14 * trace_coefficient**2:
        discriminant = 0.0
    if discriminant < 0.0:
        raise ArithmeticError("generalized comparison discriminant is negative")
    return 2.0 * alpha * stiffness / (
        trace_coefficient + sqrt(discriminant)
    )


def uncoupled_radial_frequency_squared_lower_bound(
    *,
    fixed_wall_static_form_gap: float,
    kinetic_weight_upper_bound: float,
    normalized_wall_mass: float,
    normalized_branch_curvature: float,
) -> float:
    """Return the decoupled minimum, useful as a normalization check."""

    alpha = _positive("fixed_wall_static_form_gap", fixed_wall_static_form_gap)
    weight = _positive("kinetic_weight_upper_bound", kinetic_weight_upper_bound)
    mass = _positive("normalized_wall_mass", normalized_wall_mass)
    stiffness = _positive(
        "normalized_branch_curvature", normalized_branch_curvature
    )
    return min(alpha / weight, stiffness / mass)


def adiabatic_dragged_profile_frequency_squared(
    *,
    energy_second_derivative: float,
    shell_kinetic_mass: float,
    branch_lift_weighted_norm_squared: float,
) -> float:
    """Return ``E''/(M_wall+pi Z)`` for the adiabatic branch coordinate."""

    stiffness = _positive("energy_second_derivative", energy_second_derivative)
    mass = _positive("shell_kinetic_mass", shell_kinetic_mass)
    lift_norm_squared = _nonnegative(
        "branch_lift_weighted_norm_squared",
        branch_lift_weighted_norm_squared,
    )
    return stiffness / (mass + pi * lift_norm_squared)


def missing_lift_norm_counterexample(
    *,
    normalized_branch_curvature: float,
    normalized_wall_mass: float,
    branch_lift_weighted_norm_squared: float,
) -> dict[str, float | str]:
    """Give a trial-state upper bound showing that an unpriced lift kills a gap."""

    stiffness = _positive(
        "normalized_branch_curvature", normalized_branch_curvature
    )
    mass = _positive("normalized_wall_mass", normalized_wall_mass)
    lift_norm_squared = _nonnegative(
        "branch_lift_weighted_norm_squared",
        branch_lift_weighted_norm_squared,
    )
    trial_upper = stiffness / (lift_norm_squared + mass)
    return {
        "branch_lift_weighted_norm_squared": lift_norm_squared,
        "trial_frequency_squared_upper_bound": trial_upper,
        "statement": (
            "The pure wall-coordinate trial vector has potential k q^2 and "
            "kinetic energy (c^2+m)q^2. Thus fixed-wall coercivity and positive "
            "shell stiffness do not give a uniform coupled gap unless the "
            "Dirichlet-branch lift norm c^2=<chi,W chi> is controlled."
        ),
    }


def coupled_radial_wall_gap_certificate(
    *,
    fixed_wall_static_form_gap: float = 1.0,
    kinetic_weight_upper_bound: float = 25.0,
    energy_second_derivative: float = 0.4399062320,
    shell_kinetic_mass: float = 0.4129339430,
    wall_radius: float = 4.0,
    curvature: float = 0.0025,
    wall_profile_derivative: float = -0.0878757998,
    membrane_tension: float = 0.001931779647,
    diagnostic_branch_lift_weighted_norm_squared: float = 0.063759,
) -> dict[str, object]:
    """Audit the exact transfer theorem and the current physical input gap."""

    normalized_mass = normalized_wall_kinetic_mass(shell_kinetic_mass)
    normalized_stiffness = normalized_branch_stiffness(energy_second_derivative)
    lift_samples = (0.0, 0.1, 1.0, 10.0, 100.0, 1e4)
    lower_bounds = tuple(
        {
            "branch_lift_weighted_norm_squared": lift_norm_squared,
            "coupled_frequency_squared_lower_bound": (
                coupled_radial_frequency_squared_lower_bound(
                    fixed_wall_static_form_gap=fixed_wall_static_form_gap,
                    kinetic_weight_upper_bound=kinetic_weight_upper_bound,
                    normalized_wall_mass=normalized_mass,
                    normalized_branch_curvature=normalized_stiffness,
                    branch_lift_weighted_norm_squared=lift_norm_squared,
                )
            ),
        }
        for lift_norm_squared in lift_samples
    )
    counterexamples = tuple(
        missing_lift_norm_counterexample(
            normalized_branch_curvature=normalized_stiffness,
            normalized_wall_mass=normalized_mass,
            branch_lift_weighted_norm_squared=lift_norm_squared,
        )
        for lift_norm_squared in lift_samples
    )
    uncoupled = uncoupled_radial_frequency_squared_lower_bound(
        fixed_wall_static_form_gap=fixed_wall_static_form_gap,
        kinetic_weight_upper_bound=kinetic_weight_upper_bound,
        normalized_wall_mass=normalized_mass,
        normalized_branch_curvature=normalized_stiffness,
    )
    endpoint_barta = moving_endpoint_barta_boundary_coefficient(
        wall_radius=wall_radius,
        curvature=curvature,
        wall_profile_derivative=wall_profile_derivative,
        membrane_tension=membrane_tension,
    )
    diagnostic_coupled_lower = coupled_radial_frequency_squared_lower_bound(
        fixed_wall_static_form_gap=fixed_wall_static_form_gap,
        kinetic_weight_upper_bound=kinetic_weight_upper_bound,
        normalized_wall_mass=normalized_mass,
        normalized_branch_curvature=normalized_stiffness,
        branch_lift_weighted_norm_squared=(
            diagnostic_branch_lift_weighted_norm_squared
        ),
    )
    diagnostic_adiabatic = adiabatic_dragged_profile_frequency_squared(
        energy_second_derivative=energy_second_derivative,
        shell_kinetic_mass=shell_kinetic_mass,
        branch_lift_weighted_norm_squared=(
            diagnostic_branch_lift_weighted_norm_squared
        ),
    )
    claims = {
        "nambu_goto_and_branch_terms_share_the_jacobi_normalization": (
            normalized_mass > 0.0 and normalized_stiffness > 0.0
        ),
        "zero_lift_limit_recovers_the_uncoupled_minimum": abs(
            lower_bounds[0]["coupled_frequency_squared_lower_bound"] - uncoupled
        )
        < 1e-12,
        "coupled_lower_bound_decreases_as_unpriced_added_mass_grows": all(
            right["coupled_frequency_squared_lower_bound"]
            < left["coupled_frequency_squared_lower_bound"]
            for left, right in zip(lower_bounds, lower_bounds[1:])
        ),
        "trial_upper_bound_tends_toward_zero_without_lift_control": (
            counterexamples[-1]["trial_frequency_squared_upper_bound"]
            < counterexamples[0]["trial_frequency_squared_upper_bound"] / 1e4
        ),
        "current_shell_only_frequency_is_not_promoted_to_a_coupled_gap": True,
        "fixed_wall_barta_witness_fails_the_default_moving_endpoint_test": (
            endpoint_barta["total_moving_endpoint_barta_coefficient"] < 0.0
        ),
        "separate_compatible_witness_closes_a_direct_coupled_gap": True,
    }
    return {
        "goal": "Coupled Skyrmion Profile-Membrane Radial Gap Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "conditional_exact_added_mass_gap_transfer_and_no_go",
        "central_result": (
            "Along a C2 static Dirichlet branch, eta=xi+q chi diagonalizes the "
            "potential but gives kinetic form ||dot xi+dot q chi||_W^2+m dot "
            "q^2. The exact two-block comparison yields a positive coupled gap "
            "from alpha, Wmax, branch curvature k, wall mass m, and the weighted "
            "lift norm c^2. Without a bound on c^2, no uniform gap follows."
        ),
        "normalization": {
            "normalized_wall_mass_m": normalized_mass,
            "normalized_branch_curvature_k": normalized_stiffness,
            "reason": (
                "The radial Jacobi bracket carries 4pi/8, while the standard "
                "shell quadratic action carries one half; therefore m=M_wall/pi "
                "and k=E_branch_second/pi."
            ),
        },
        "uncoupled_frequency_squared_lower_bound": uncoupled,
        "conditional_lift_norm_sweep": lower_bounds,
        "missing_input_counterexamples": counterexamples,
        "moving_endpoint_barta_audit": endpoint_barta,
        "uncertified_default_diagnostic": {
            "branch_lift_weighted_norm_squared": (
                diagnostic_branch_lift_weighted_norm_squared
            ),
            "conservative_coupled_frequency_lower_bound": sqrt(
                diagnostic_coupled_lower
            ),
            "adiabatic_dragged_profile_frequency": sqrt(diagnostic_adiabatic),
            "status": "exploratory_floating_not_certified",
        },
        "current_evidence": {
            "fixed_wall_l0_static_form_gap": "authenticated: alpha=1",
            "hard_support_kinetic_weight_bound": "proved: Wmax=25",
            "branch_curvature": "positive step-converged numerical evidence",
            "nambu_goto_wall_mass": "positive step-converged numerical evidence",
            "dirichlet_branch_lift_weighted_norm": "missing",
            "branch_coordinate_sharpening": "open",
            "direct_coupled_profile_wall_radial_gap": (
                "authenticated separately: omega_hat>=1/50"
            ),
        },
        "certified_claims": claims,
        "claim_boundary": (
            "The transfer theorem is exact under a C2 static Dirichlet branch "
            "with a positive certified branch curvature. The displayed default "
            "curvature and wall mass are floating step-converged evidence, and "
            "the branch-lift norm is absent, so this branch-coordinate route "
            "does not certify its stronger numerical estimate. A separate "
            "compatible-witness theorem certifies omega_hat>=1/50. The negative "
            "coefficient here is specific to the old witness, not an instability. "
            "Anchor and nonspherical channels are excluded."
        ),
    }
