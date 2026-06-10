"""Centered hard-wall Skyrmion collective-current moments.

Given the standard leading rigid-hedgehog collective-current density

    ell_i = (kappa/I) (delta_ij - n_i n_j) J_j.

For the centered inversion-symmetric profile its signed first spatial moment
vanishes componentwise, while its signed second moment is fixed by one radial
inertia-weighted mean-square radius.  Absolute norm-weighted moments do not
vanish; this module records conservative spin-sector bounds for them.
"""

from __future__ import annotations

from math import asin, isfinite, pi, sqrt

from .massive_skyrmion_profile import (
    dimensionless_inertia_density,
    static_patch_lapse,
)
from .massive_skyrmion_worldtube import (
    hard_wall_profile_integrals,
    solve_hard_wall_skyrmion_profile,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def proper_radial_coordinate(
    dimensionless_radius: float,
    *,
    curvature: float,
) -> float:
    """Return the centered static-slice proper radius in ``(e f_pi)^-1`` units."""
    _validate_nonnegative("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("curvature", curvature)
    if static_patch_lapse(dimensionless_radius, curvature) <= 0.0:
        raise ValueError("radius must lie strictly inside the static-patch horizon")
    if curvature == 0.0:
        return dimensionless_radius
    root_curvature = sqrt(curvature)
    return asin(root_curvature * dimensionless_radius) / root_curvature


def _trapezoid(
    points: tuple[tuple[float, float, float], ...],
    values: tuple[float, ...],
) -> float:
    return sum(
        (values[index] + values[index + 1])
        * (points[index + 1][0] - points[index][0])
        / 2.0
        for index in range(len(points) - 1)
    )


def signed_second_moment_tensor_coefficients(
    current_component: int,
    first_coordinate: int,
    second_coordinate: int,
    *,
    proper_mean_square_radius: float,
) -> tuple[float, float, float]:
    """Return coefficients of ``(J_0,J_1,J_2)`` in a signed second moment.

    The returned vector implements

    ``<rho^2>/10 (4 delta_kl J_i-delta_ki J_l-delta_li J_k)``.
    """
    for name, value in (
        ("current_component", current_component),
        ("first_coordinate", first_coordinate),
        ("second_coordinate", second_coordinate),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value not in range(3):
            raise ValueError(f"{name} must be one of 0, 1, 2")
    _validate_nonnegative("proper_mean_square_radius", proper_mean_square_radius)
    coefficient = proper_mean_square_radius / 10.0
    result = [0.0, 0.0, 0.0]
    if first_coordinate == second_coordinate:
        result[current_component] += 4.0 * coefficient
    if first_coordinate == current_component:
        result[second_coordinate] -= coefficient
    if second_coordinate == current_component:
        result[first_coordinate] -= coefficient
    return tuple(result)


def centered_current_moment_record(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, float]:
    """Return inertia-weighted radii and absolute current-moment bounds."""
    _validate_positive("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("step", step)
    _, points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    integrals = hard_wall_profile_integrals(
        points,
        pion_mass=pion_mass,
        curvature=curvature,
    )
    inertia_values = tuple(
        dimensionless_inertia_density(
            radius,
            profile,
            derivative,
            curvature=curvature,
        )
        for radius, profile, derivative in points
    )
    proper_radii = tuple(
        proper_radial_coordinate(radius, curvature=curvature)
        for radius, _, _ in points
    )
    inertia = _trapezoid(points, inertia_values)
    proper_mean_radius = _trapezoid(
        points,
        tuple(
            radius * density
            for radius, density in zip(proper_radii, inertia_values)
        ),
    ) / inertia
    proper_mean_square = _trapezoid(
        points,
        tuple(
            radius**2 * density
            for radius, density in zip(proper_radii, inertia_values)
        ),
    ) / inertia
    areal_mean_square = _trapezoid(
        points,
        tuple(
            point[0] ** 2 * density
            for point, density in zip(points, inertia_values)
        ),
    ) / inertia
    absolute_bound_factor = 9.0 * pi / 8.0
    return {
        "dimensionless_inertia_c_I": inertia,
        "profile_integral_inertia_c_I": integrals[
            "interior_dimensionless_inertia_c_I"
        ],
        "dimensionless_proper_mean_radius": proper_mean_radius,
        "dimensionless_proper_mean_square_radius": proper_mean_square,
        "dimensionless_proper_rms_radius": sqrt(proper_mean_square),
        "dimensionless_areal_mean_square_radius": areal_mean_square,
        "signed_dipole_operator_coefficient": 0.0,
        "signed_second_moment_tensor_coefficient": proper_mean_square / 10.0,
        "absolute_first_moment_bound_coefficient_per_spin": (
            absolute_bound_factor * proper_mean_radius
        ),
        "absolute_second_moment_bound_coefficient_per_spin": (
            absolute_bound_factor * proper_mean_square
        ),
    }


def skyrmion_current_moments_certificate(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, object]:
    """Certify centered collective-current parity and radial moments."""
    record = centered_current_moment_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    refined = centered_current_moment_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step / 2.0,
    )
    trace_coefficients = [0.0, 0.0, 0.0]
    for coordinate in range(3):
        coefficients = signed_second_moment_tensor_coefficients(
            1,
            coordinate,
            coordinate,
            proper_mean_square_radius=record[
                "dimensionless_proper_mean_square_radius"
            ],
        )
        trace_coefficients = [
            left + right
            for left, right in zip(trace_coefficients, coefficients)
        ]
    expected_trace = [
        0.0,
        record["dimensionless_proper_mean_square_radius"],
        0.0,
    ]
    relative_step_change = abs(
        refined["dimensionless_proper_mean_square_radius"]
        / record["dimensionless_proper_mean_square_radius"]
        - 1.0
    )
    certified_claims = {
        "radial_inertia_weight_is_internally_consistent": abs(
            record["dimensionless_inertia_c_I"]
            / record["profile_integral_inertia_c_I"]
            - 1.0
        )
        < 1.0e-13,
        "analytic_centered_parity_identity_is_encoded": (
            record["signed_dipole_operator_coefficient"] == 0.0
        ),
        "analytic_signed_second_moment_trace_identity_is_encoded": max(
            abs(left - right)
            for left, right in zip(trace_coefficients, expected_trace)
        )
        < 1.0e-13,
        "proper_second_moment_is_step_stable": relative_step_change < 1.0e-6,
        "absolute_first_and_second_moment_bounds_remain_nonzero": (
            record["absolute_first_moment_bound_coefficient_per_spin"] > 0.0
            and record["absolute_second_moment_bound_coefficient_per_spin"] > 0.0
        ),
    }
    return {
        "goal": "Centered Skyrmion Collective-Current Moment Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "analytic_collective_ansatz_with_converged_radial_moments",
        "central_result": (
            "Given the standard leading collective-current formula, the "
            "centered inversion-symmetric hard-wall profile has exact "
            "componentwise signed current-dipole cancellation. Its signed "
            "second moment and conservative absolute M1/M2 bounds are fixed "
            "by converged inertia-weighted radii."
        ),
        "profile": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius_x_w": wall_radius,
            "step": step,
        },
        "record": record,
        "refined_proper_mean_square_radius": refined[
            "dimensionless_proper_mean_square_radius"
        ],
        "relative_step_change": relative_step_change,
        "signed_second_moment_identity": (
            "int xi^k xi^l ell_i = <rho^2>_I "
            "(4 delta_kl J_i-delta_ki J_l-delta_li J_k)/10"
        ),
        "absolute_moment_bounds": (
            "M1_abs <= (9 pi/8) L <rho>_I and "
            "M2_abs <= (9 pi/8) L <rho^2>_I"
        ),
        "certified_claims": certified_claims,
        "claim_boundary": (
            "The executable artifact assumes the standard Noether-current "
            "compression to the leading rigid-rotor band and checks its angular "
            "consequences and radial integrals; it is not an independent "
            "derivation of that compression. The result is confined to the "
            "centered inversion-symmetric hard-wall profile. The signed "
            "dipole is not the absolute first moment. Off-center acceleration, "
            "wall deformation, vibrations, relativistic corrections, and a "
            "point-local bare-field coupling can regenerate additional moments "
            "or nonzero-Bohr sectors."
        ),
        "next_physics_gate": (
            "solve the supported off-center l=1 matter-membrane deformation and "
            "bound its regenerated current dipole in the channel norm"
        ),
    }
