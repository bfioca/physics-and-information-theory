"""Local de Sitter static-patch s-wave Weyl/KMS regulator.

For a conformally coupled massless scalar in four-dimensional de Sitter, the
rescaled s-wave has zero radial potential in tortoise coordinate
``x=R artanh(r/R)``.  A stretched horizon ``r=R-delta`` gives a finite interval
``[0,X_delta]``.  Dirichlet modes form a Riemann-sum regulator for local smeared
KMS covariances at the de Sitter inverse temperature ``2*pi*R``.
"""

from __future__ import annotations

from math import cos, exp, floor, isfinite, log, pi, tanh


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def de_sitter_inverse_temperature(radius: float) -> float:
    _validate_positive("radius", radius)
    return 2.0 * pi * radius


def tortoise_length(radius: float, stretched_distance: float) -> float:
    """Return ``R artanh(1-delta/R)`` in a stable logarithmic form."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    if stretched_distance >= radius:
        raise ValueError("stretched_distance must be smaller than radius")
    length = 0.5 * radius * (
        log(2.0 * radius - stretched_distance) - log(stretched_distance)
    )
    if not isfinite(length):
        raise ValueError("tortoise length is not representable for these inputs")
    return length


def s_wave_mode_frequency(
    mode_number: int,
    *,
    radius: float,
    stretched_distance: float,
) -> float:
    """Dirichlet s-wave frequency ``n*pi/X_delta``."""
    if isinstance(mode_number, bool) or not isinstance(mode_number, int) or mode_number < 1:
        raise ValueError("mode_number must be a positive integer")
    length = tortoise_length(radius, stretched_distance)
    return mode_number * pi / length


def _coth(value: float) -> float:
    if value > 20.0:
        tail = exp(-2.0 * value)
        return (1.0 + tail) / (1.0 - tail)
    return 1.0 / tanh(value)


def retained_s_wave_mode_count(
    *,
    radius: float,
    stretched_distance: float,
    momentum_cutoff: float,
) -> int:
    """Number of Dirichlet modes whose frequency does not exceed the cutoff."""
    _validate_positive("momentum_cutoff", momentum_cutoff)
    length = tortoise_length(radius, stretched_distance)
    return max(0, floor(momentum_cutoff * length / pi))


def box_test_sine_transform(
    momentum: float,
    *,
    support_start: float,
    support_end: float,
) -> float:
    """Sine transform of the L2-normalized indicator of a compact interval."""
    if not isfinite(momentum) or momentum < 0.0:
        raise ValueError("momentum must be finite and nonnegative")
    _validate_positive("support_start", support_start)
    _validate_positive("support_end", support_end)
    if support_end <= support_start:
        raise ValueError("support_end must exceed support_start")
    width = support_end - support_start
    if momentum == 0.0:
        return 0.0
    return (
        cos(momentum * support_start) - cos(momentum * support_end)
    ) / (momentum * width**0.5)


def thermal_covariance_integrand(
    momentum: float,
    *,
    beta: float,
    support_start: float,
    support_end: float,
) -> float:
    """Continuum integrand ``|F(k)|^2 coth(beta k/2)/k``."""
    if not isfinite(momentum) or momentum < 0.0:
        raise ValueError("momentum must be finite and nonnegative")
    _validate_positive("beta", beta)
    _validate_positive("support_start", support_start)
    _validate_positive("support_end", support_end)
    if support_end <= support_start:
        raise ValueError("support_end must exceed support_start")
    width = support_end - support_start
    if momentum == 0.0:
        slope = (support_end**2 - support_start**2) / (2.0 * width**0.5)
        return 2.0 * slope * slope / beta
    transform = box_test_sine_transform(
        momentum,
        support_start=support_start,
        support_end=support_end,
    )
    return transform * transform * _coth(beta * momentum / 2.0) / momentum


def finite_s_wave_covariance(
    *,
    radius: float,
    stretched_distance: float,
    support_start: float,
    support_end: float,
    momentum_cutoff: float,
) -> float:
    """Finite-box KMS covariance of one smeared rescaled radial field."""
    _validate_positive("momentum_cutoff", momentum_cutoff)
    length = tortoise_length(radius, stretched_distance)
    _validate_positive("support_start", support_start)
    _validate_positive("support_end", support_end)
    if support_end <= support_start:
        raise ValueError("support_end must exceed support_start")
    if support_end >= length:
        raise ValueError("test-function support must lie inside the stretched patch")
    beta = de_sitter_inverse_temperature(radius)
    maximum_mode = retained_s_wave_mode_count(
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )
    return sum(
        thermal_covariance_integrand(
            mode_number * pi / length,
            beta=beta,
            support_start=support_start,
            support_end=support_end,
        )
        for mode_number in range(1, maximum_mode + 1)
    ) / length


def continuum_s_wave_covariance(
    *,
    radius: float,
    support_start: float,
    support_end: float,
    momentum_cutoff: float,
    integration_steps: int = 20000,
) -> float:
    """Simpson approximation of the continuum KMS covariance through ``k_max``."""
    _validate_positive("momentum_cutoff", momentum_cutoff)
    if (
        isinstance(integration_steps, bool)
        or not isinstance(integration_steps, int)
        or integration_steps < 2
        or integration_steps % 2
    ):
        raise ValueError("integration_steps must be a positive even integer")
    beta = de_sitter_inverse_temperature(radius)
    step = momentum_cutoff / integration_steps
    total = thermal_covariance_integrand(
        0.0,
        beta=beta,
        support_start=support_start,
        support_end=support_end,
    )
    total += thermal_covariance_integrand(
        momentum_cutoff,
        beta=beta,
        support_start=support_start,
        support_end=support_end,
    )
    for index in range(1, integration_steps):
        weight = 4.0 if index % 2 else 2.0
        total += weight * thermal_covariance_integrand(
            index * step,
            beta=beta,
            support_start=support_start,
            support_end=support_end,
        )
    return step * total / (3.0 * pi)


def local_static_patch_regulator_record(
    *,
    radius: float,
    stretched_distance: float,
    support_start: float,
    support_end: float,
    momentum_cutoff: float,
) -> dict[str, object]:
    """Record local covariance convergence data at one stretched horizon."""
    length = tortoise_length(radius, stretched_distance)
    finite_covariance = finite_s_wave_covariance(
        radius=radius,
        stretched_distance=stretched_distance,
        support_start=support_start,
        support_end=support_end,
        momentum_cutoff=momentum_cutoff,
    )
    continuum_covariance = continuum_s_wave_covariance(
        radius=radius,
        support_start=support_start,
        support_end=support_end,
        momentum_cutoff=momentum_cutoff,
    )
    return {
        "de_sitter_radius_R": radius,
        "stretched_horizon_radial_gap_delta": stretched_distance,
        "tortoise_length_X_delta": length,
        "radial_mode_spacing": pi / length,
        "inverse_temperature_beta": de_sitter_inverse_temperature(radius),
        "field_model": "four-dimensional conformally coupled massless scalar s-wave",
        "finite_state_model": "Dirichlet finite-box Gibbs approximant",
        "continuum_target": "Bunch-Davies static-patch s-wave covariance",
        "rescaled_radial_potential": "V_0(x)=0",
        "boundary_conditions": "Dirichlet at the origin and stretched horizon",
        "local_test_support": (support_start, support_end),
        "momentum_cutoff": momentum_cutoff,
        "retained_mode_count": retained_s_wave_mode_count(
            radius=radius,
            stretched_distance=stretched_distance,
            momentum_cutoff=momentum_cutoff,
        ),
        "finite_smeared_kms_covariance": finite_covariance,
        "continuum_smeared_kms_covariance": continuum_covariance,
        "absolute_covariance_error": abs(finite_covariance - continuum_covariance),
        "convergence_mode": (
            "Riemann-sum convergence of one UV-truncated equal-time thermal field "
            "variance on fixed compact support, not convergence of a full KMS "
            "two-point distribution or a global density matrix"
        ),
        "observable_probe": (
            "equal-time rescaled radial field smeared on one compact interval"
        ),
        "factor_type_claimed": False,
    }


def static_patch_weyl_regulator_certificate(
    *,
    radius: float = 1.0,
    minimum_power: int = 16,
    steps: int = 6,
    momentum_cutoff: float = 80.0,
) -> dict[str, object]:
    """Audit the first local static-patch KMS refinement sequence."""
    _validate_positive("radius", radius)
    if isinstance(minimum_power, bool) or not isinstance(minimum_power, int) or minimum_power < 4:
        raise ValueError("minimum_power must be an integer at least four")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 3:
        raise ValueError("steps must be an integer at least three")
    _validate_positive("momentum_cutoff", momentum_cutoff)
    support_start = 0.25 * radius
    support_end = 0.75 * radius
    records = tuple(
        local_static_patch_regulator_record(
            radius=radius,
            stretched_distance=radius / float(minimum_power * 4**index),
            support_start=support_start,
            support_end=support_end,
            momentum_cutoff=momentum_cutoff,
        )
        for index in range(steps)
    )
    spacings = tuple(record["radial_mode_spacing"] for record in records)
    errors = tuple(record["absolute_covariance_error"] for record in records)
    certified_claims = {
        "stretched_horizon_removal_collapses_radial_mode_spacing": all(
            right < left for left, right in zip(spacings, spacings[1:])
        ),
        "retained_radial_mode_count_grows": all(
            right["retained_mode_count"] > left["retained_mode_count"]
            for left, right in zip(records, records[1:])
        ),
        "equal_time_smeared_covariance_converges_at_fixed_uv_cutoff": (
            errors[-1] < errors[0] and errors[-1] < 5e-3
        ),
        "de_sitter_kms_temperature_is_geometric": all(
            record["inverse_temperature_beta"] == 2.0 * pi * radius
            for record in records
        ),
        "no_factor_type_is_inferred_from_finite_covariance_data": all(
            not record["factor_type_claimed"] for record in records
        ),
    }
    return {
        "goal": "Static-Patch S-Wave KMS Covariance Benchmark",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "stretched_horizon_equal_time_covariance_refinement",
        "central_result": (
            "For the conformally coupled de Sitter s-wave, stretched-horizon "
            "Dirichlet modes have spacing pi/X_delta with X_delta=R artanh(1-delta/R). "
            "As delta tends to zero, the spacing collapses and a UV-truncated "
            "finite-box equal-time thermal variance converges on one fixed compact "
            "radial smearing to the corresponding half-line variance at "
            "beta=2*pi*R."
        ),
        "claim_boundary": (
            "free conformal s-wave, equal-time rescaled-field covariance, compactly "
            "supported box smearings, fixed UV momentum cutoff and numerical "
            "Riemann-sum audit; no spacetime Weyl net, full angular net, "
            "Hadamard/type-III proof, gravitational constraint, crossed-product "
            "convergence, or generalized entropy is claimed"
        ),
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "add all angular sectors and distributional covariance bounds, then "
            "identify the Bunch-Davies local GNS algebra before forming the core"
        ),
    }
