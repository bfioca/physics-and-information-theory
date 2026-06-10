"""Bunch-Davies scalar covariance test for a local common-mode bath.

For the conformally coupled scalar in the four-dimensional de Sitter static
patch, the optical Wightman spectral density between points at hyperbolic
distance ``d_H`` has spatial factor

    sin(k d_H) / [R sinh(d_H/R)].

Relative to the coincident factor ``k``, its zero-frequency limit is

    c_0(y) = y / sinh(y),       y = d_H/R.

This module inserts that exact local-bath covariance into the axial
common-mode mismatch witness.  It is a weak-coupling, zero-Bohr-frequency,
equal-redshift surrogate, not yet the full rotating field-top channel.
"""

from __future__ import annotations

from math import asinh, asin, exp, isfinite, log, log1p, pi, sin, sinh, sqrt, tan

from .common_mode_locality_mismatch import (
    axial_common_mode_mismatch_lower_bound,
    maximum_correlation_defect_for_mismatch,
)


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_dimension(dimension: int) -> None:
    if (
        isinstance(dimension, bool)
        or not isinstance(dimension, int)
        or dimension < 3
    ):
        raise ValueError("dimension must be an integer at least three")


def zero_frequency_scalar_correlation(optical_distance_over_radius: float) -> float:
    """Return ``c_0(y)=y/sinh(y)`` with stable endpoint evaluation."""
    y = optical_distance_over_radius
    _validate_nonnegative("optical_distance_over_radius", y)
    if y == 0.0:
        return 1.0
    if y < 1.0e-4:
        y2 = y * y
        return 1.0 - y2 / 6.0 + 7.0 * y2 * y2 / 360.0
    if y > 40.0:
        return 2.0 * y * exp(-y) / (1.0 - exp(-2.0 * y))
    return y / sinh(y)


def optical_radius_from_horizon_proper_distance(
    stretched_distance: float,
    *,
    radius: float,
) -> float:
    """Convert static-slice proper horizon distance ``rho`` to optical radius."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    if stretched_distance > 0.5 * pi * radius:
        raise ValueError("stretched_distance must be at most pi R/2")
    return -radius * log(tan(stretched_distance / (2.0 * radius)))


def same_shell_optical_distance_over_radius(
    stretched_distance: float,
    angular_separation: float,
    *,
    radius: float,
) -> float:
    """Return hyperbolic optical distance for two points on one static shell."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    if stretched_distance > 0.5 * pi * radius:
        raise ValueError("stretched_distance must be at most pi R/2")
    _validate_nonnegative("angular_separation", angular_separation)
    if angular_separation > pi:
        raise ValueError("angular_separation must be at most pi")
    cotangent = 1.0 / tan(stretched_distance / radius)
    half_sine = sin(0.5 * angular_separation)
    return 2.0 * asinh(abs(cotangent * half_sine))


def maximum_optical_distance_for_correlation_defect(
    maximum_defect: float,
) -> float:
    """Invert ``1-y/sinh(y)<=maximum_defect`` by monotone bisection."""
    _validate_nonnegative("maximum_defect", maximum_defect)
    if maximum_defect >= 1.0:
        return float("inf")
    if maximum_defect == 0.0:
        return 0.0
    target_correlation = 1.0 - maximum_defect
    low = 0.0
    high = 1.0
    while zero_frequency_scalar_correlation(high) > target_correlation:
        high *= 2.0
    for _ in range(96):
        middle = 0.5 * (low + high)
        if zero_frequency_scalar_correlation(middle) >= target_correlation:
            low = middle
        else:
            high = middle
    return low


def analytic_optical_distance_necessary_bound(maximum_defect: float) -> float:
    """Return the rigorous consequence ``y<=sqrt(6D/(1-D))``.

    It follows from ``sinh(y)>=y+y^3/6``, hence
    ``1-y/sinh(y)>=y^2/(6+y^2)``.
    """
    _validate_nonnegative("maximum_defect", maximum_defect)
    if maximum_defect >= 1.0:
        return float("inf")
    return sqrt(6.0 * maximum_defect / (1.0 - maximum_defect))


def maximum_same_shell_angular_separation(
    stretched_distance: float,
    maximum_optical_distance_over_radius: float,
    *,
    radius: float,
) -> float:
    """Translate an optical-distance bound into an angular co-location bound."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    if stretched_distance > 0.5 * pi * radius:
        raise ValueError("stretched_distance must be at most pi R/2")
    _validate_nonnegative(
        "maximum_optical_distance_over_radius",
        maximum_optical_distance_over_radius,
    )
    if maximum_optical_distance_over_radius == float("inf"):
        return pi
    if maximum_optical_distance_over_radius == 0.0:
        return 0.0
    tangent = tan(stretched_distance / radius)
    if tangent == 0.0:
        return 0.0
    half_distance = 0.5 * maximum_optical_distance_over_radius
    if half_distance < 20.0:
        log_sinh = log(sinh(half_distance))
    else:
        log_sinh = (
            half_distance
            - log(2.0)
            + log1p(-exp(-2.0 * half_distance))
        )
    log_argument = log_sinh + log(tangent)
    if log_argument >= 0.0:
        return pi
    return 2.0 * asin(exp(log_argument))


def static_patch_scalar_common_mode_record(
    dimension: int,
    *,
    radius: float,
    stretched_distance: float,
    angular_separation: float,
    mismatch_coefficient: float = 1.0,
    charge_gap: float = 1.0,
) -> dict[str, object]:
    """Compare a local Bunch-Davies scalar bath with the common-mode budget."""
    _validate_dimension(dimension)
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    _validate_nonnegative("angular_separation", angular_separation)
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    _validate_positive("charge_gap", charge_gap)
    target_mismatch = mismatch_coefficient / float(dimension)
    if target_mismatch >= 0.5:
        raise ValueError("mismatch_coefficient/dimension must be smaller than one half")

    dimensionless_time = 0.5 * log(float(dimension))
    optical_distance = same_shell_optical_distance_over_radius(
        stretched_distance,
        angular_separation,
        radius=radius,
    )
    correlation = zero_frequency_scalar_correlation(optical_distance)
    mismatch = axial_common_mode_mismatch_lower_bound(
        dimensionless_time,
        correlation=correlation,
        charge_gap=charge_gap,
    )
    maximum_defect = maximum_correlation_defect_for_mismatch(
        target_mismatch,
        dimensionless_time=dimensionless_time,
        charge_gap=charge_gap,
    )
    maximum_optical_distance = maximum_optical_distance_for_correlation_defect(
        maximum_defect
    )
    analytic_distance_bound = analytic_optical_distance_necessary_bound(
        maximum_defect
    )
    maximum_angular_separation = maximum_same_shell_angular_separation(
        stretched_distance,
        maximum_optical_distance,
        radius=radius,
    )
    return {
        "dimension_d": dimension,
        "radius_R": radius,
        "stretched_proper_distance_rho": stretched_distance,
        "angular_separation_theta": angular_separation,
        "optical_distance_over_radius_y": optical_distance,
        "zero_frequency_cross_spectral_correlation_c0": correlation,
        "dimensionless_protocol_time_s": dimensionless_time,
        "axial_charge_gap_Delta": charge_gap,
        "actual_axial_common_mode_mismatch_lower_bound": mismatch,
        "allocated_mismatch_A_over_d": target_mismatch,
        "passes_axial_common_mode_error_allocation": mismatch <= target_mismatch,
        "maximum_allowed_correlation_defect": maximum_defect,
        "maximum_allowed_optical_distance_over_radius": maximum_optical_distance,
        "analytic_necessary_optical_distance_bound": analytic_distance_bound,
        "maximum_allowed_same_shell_angular_separation": (
            maximum_angular_separation
        ),
        "local_interaction_surrogate": (
            "stationary H_I=lambda[q_T(0) phi(t,x_T)+q_R(0) phi(t,x_R)], "
            "with q_i(0) the zero-Bohr secular components"
        ),
        "spectral_derivation": (
            "the Bunch-Davies optical Wightman density has spatial ratio "
            "sin(k d_H)/(k R sinh(d_H/R)); its k->0 limit is y/sinh(y)"
        ),
        "scope": (
            "equal-redshift same-shell localized axial charges, weak-coupling "
            "stationary zero-Bohr-frequency Markov sector, pointlike spectral "
            "ratio or optical-narrow identical spatial smearings, equal coupling "
            "strength and charge normalization, "
            "inaccessible bath record, and the sufficient s=(1/2)log d schedule"
        ),
    }


def static_patch_scalar_common_mode_certificate(
    *,
    radius: float = 1.0,
    stretched_distance: float = 0.05,
    angular_separation: float = 0.1,
    maximum_dimension: int = 4096,
    mismatch_coefficient: float = 1.0,
    charge_gap: float = 1.0,
) -> dict[str, object]:
    """Audit the local Bunch-Davies scalar common-mode obstruction."""
    _validate_dimension(maximum_dimension)
    if maximum_dimension < 8:
        raise ValueError("maximum_dimension must be at least eight")
    dimensions = tuple(
        sorted(
            {
                dimension
                for dimension in (8, 32, 128, 512, maximum_dimension)
                if dimension <= maximum_dimension
            }
            | {maximum_dimension}
        )
    )
    records = tuple(
        static_patch_scalar_common_mode_record(
            dimension,
            radius=radius,
            stretched_distance=stretched_distance,
            angular_separation=angular_separation,
            mismatch_coefficient=mismatch_coefficient,
            charge_gap=charge_gap,
        )
        for dimension in dimensions
    )
    sample_distances = (0.0, 0.1, 0.5, 1.0, 3.0, 10.0)
    correlations = tuple(
        zero_frequency_scalar_correlation(distance)
        for distance in sample_distances
    )
    required_optical_distances = tuple(
        record["maximum_allowed_optical_distance_over_radius"]
        for record in records
    )
    required_angular_separations = tuple(
        record["maximum_allowed_same_shell_angular_separation"]
        for record in records
    )
    certified_claims = {
        "zero_frequency_correlation_is_one_only_at_coincidence": (
            correlations[0] == 1.0
            and all(0.0 < value < 1.0 for value in correlations[1:])
        ),
        "zero_frequency_correlation_decreases_with_optical_distance": all(
            right < left for left, right in zip(correlations, correlations[1:])
        ),
        "analytic_distance_bound_dominates_exact_inversion": all(
            record["analytic_necessary_optical_distance_bound"]
            >= record["maximum_allowed_optical_distance_over_radius"]
            for record in records
        ),
        "A_over_d_budget_forces_optical_colocation": all(
            right < left
            for left, right in zip(
                required_optical_distances,
                required_optical_distances[1:],
            )
        ),
        "near_horizon_same_shell_angular_window_shrinks": all(
            right < left
            for left, right in zip(
                required_angular_separations,
                required_angular_separations[1:],
            )
        ),
        "default_fixed_separation_eventually_fails_error_allocation": (
            not records[-1]["passes_axial_common_mode_error_allocation"]
        ),
    }
    return {
        "goal": "Static-Patch Scalar Common-Mode Test",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "bunch_davies_zero_frequency_common_mode_obstruction",
        "central_result": (
            "For two equal-redshift local axial couplings to the conformal "
            "Bunch-Davies scalar, the normalized zero-frequency cross spectrum "
            "is c0(y)=y/sinh(y). At any fixed nonzero optical separation, c0<1 "
            "and the common-mode mismatch tends to one half along growing "
            "s=(1/2)log d."
        ),
        "scaling_consequence": (
            "An A/d mismatch allocation requires optical separation "
            "d_H/R=O(1/(Delta sqrt(d log d))). On a shell at proper horizon "
            "distance rho, the allowed angular separation is asymptotically "
            "O((rho/R)/(Delta sqrt(d log d)))."
        ),
        "claim_boundary": (
            "this is a named local axial scalar-bath surrogate in the "
            "zero-Bohr-frequency Davies sector. It does not derive the hard "
            "angular target as a localized charge, a full isotropic SO(3) torque "
            "channel, a rigorous point-coupling Hamiltonian, finite switching or "
            "smearing errors, finite-memory errors, the diffusion rate, or "
            "backreaction."
        ),
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "replace the localized axial charges by the actual hard angular "
            "Bunch-Davies target and a finite spherical top, derive the torque "
            "spectral matrix with switching and smearing, and include Davies, "
            "lifetime, and stress-energy errors"
        ),
    }
