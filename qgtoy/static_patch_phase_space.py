"""Finite-UV s-wave canonical phase-space and KMS convergence.

This module upgrades the one-observable covariance benchmark to projected
canonical phase-space data for compactly supported polynomial bumps.  At fixed
UV momentum cutoff, the finite Dirichlet box symplectic forms, quasifree
covariances, and unequal-time two-point functions are Riemann sums for the
half-line thermal theory.

The hard bandlimit is nonlocal.  No UV removal, all-angular Bunch-Davies net,
factor-type result, or gravitational observer algebra is inferred here.
"""

from __future__ import annotations

from cmath import exp as complex_exp
from dataclasses import dataclass
from functools import lru_cache
from math import ceil, comb, exp, expm1, factorial, isfinite, log, pi, sin, sqrt, tanh

from .static_patch_weyl_regulator import (
    de_sitter_inverse_temperature,
    retained_s_wave_mode_count,
    tortoise_length,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


@dataclass(frozen=True)
class CompactPolynomialBump:
    """L2-normalized compact polynomial bump on one interval."""

    support_start: float
    support_end: float
    power: int = 3

    def __post_init__(self) -> None:
        _validate_positive("support_start", self.support_start)
        _validate_positive("support_end", self.support_end)
        if self.support_end <= self.support_start:
            raise ValueError("support_end must exceed support_start")
        if (
            isinstance(self.power, bool)
            or not isinstance(self.power, int)
            or self.power < 3
            or self.power > 12
        ):
            raise ValueError("power must be an integer from three through twelve")


@dataclass(frozen=True)
class PhaseSpaceTest:
    """Compact equal-time Cauchy datum ``field_scale*f + momentum_scale*g``."""

    field_bump: CompactPolynomialBump | None = None
    momentum_bump: CompactPolynomialBump | None = None
    field_scale: float = 1.0
    momentum_scale: float = 1.0

    def __post_init__(self) -> None:
        if self.field_bump is None and self.momentum_bump is None:
            raise ValueError("at least one phase-space component is required")
        if not isfinite(self.field_scale) or not isfinite(self.momentum_scale):
            raise ValueError("phase-space scales must be finite")

    @property
    def support_end(self) -> float:
        return max(
            bump.support_end
            for bump in (self.field_bump, self.momentum_bump)
            if bump is not None
        )


def polynomial_bump_normalization(bump: CompactPolynomialBump) -> float:
    """Normalization for ``(x-a)^p(b-x)^p`` in ``L2(dx)``."""
    width = bump.support_end - bump.support_start
    beta_value = factorial(2 * bump.power) ** 2 / factorial(4 * bump.power + 1)
    return 1.0 / sqrt(width ** (4 * bump.power + 1) * beta_value)


def polynomial_bump_value(bump: CompactPolynomialBump, coordinate: float) -> float:
    if not isfinite(coordinate):
        raise ValueError("coordinate must be finite")
    if coordinate <= bump.support_start or coordinate >= bump.support_end:
        return 0.0
    return polynomial_bump_normalization(bump) * (
        (coordinate - bump.support_start) ** bump.power
        * (bump.support_end - coordinate) ** bump.power
    )


def polynomial_bump_moment(bump: CompactPolynomialBump, order: int) -> float:
    """Exact moment ``integral x^order bump(x) dx``."""
    if isinstance(order, bool) or not isinstance(order, int) or order < 0:
        raise ValueError("order must be a nonnegative integer")
    start = bump.support_start
    width = bump.support_end - start
    total = 0.0
    for index in range(order + 1):
        beta_value = (
            factorial(bump.power + index)
            * factorial(bump.power)
            / factorial(2 * bump.power + index + 1)
        )
        total += (
            comb(order, index)
            * start ** (order - index)
            * width ** (2 * bump.power + index + 1)
            * beta_value
        )
    return polynomial_bump_normalization(bump) * total


@lru_cache(maxsize=65536)
def unitary_sine_transform(
    momentum: float,
    bump: CompactPolynomialBump,
    quadrature_steps: int = 240,
) -> float:
    """Numerical unitary half-line sine transform of one compact bump."""
    if not isfinite(momentum) or momentum < 0.0:
        raise ValueError("momentum must be finite and nonnegative")
    if (
        isinstance(quadrature_steps, bool)
        or not isinstance(quadrature_steps, int)
        or quadrature_steps < 20
        or quadrature_steps % 2
    ):
        raise ValueError("quadrature_steps must be an even integer at least twenty")
    if momentum == 0.0:
        return 0.0
    width = bump.support_end - bump.support_start
    resolved_steps = max(
        quadrature_steps,
        ceil(16.0 * momentum * width / pi),
    )
    if resolved_steps % 2:
        resolved_steps += 1
    step = width / resolved_steps
    total = 0.0
    for index in range(resolved_steps + 1):
        coordinate = bump.support_start + index * step
        if index in (0, resolved_steps):
            weight = 1.0
        else:
            weight = 4.0 if index % 2 else 2.0
        total += weight * polynomial_bump_value(bump, coordinate) * sin(
            momentum * coordinate
        )
    return sqrt(2.0 / pi) * step * total / 3.0


def phase_space_spectral_components(
    momentum: float, test: PhaseSpaceTest
) -> tuple[float, float]:
    field = 0.0
    canonical_momentum = 0.0
    if test.field_bump is not None:
        field = test.field_scale * unitary_sine_transform(momentum, test.field_bump)
    if test.momentum_bump is not None:
        canonical_momentum = test.momentum_scale * unitary_sine_transform(
            momentum, test.momentum_bump
        )
    return field, canonical_momentum


def _coth(value: float) -> float:
    if value > 20.0:
        tail = exp(-2.0 * value)
        return (1.0 + tail) / (1.0 - tail)
    return 1.0 / tanh(value)


def _validate_box_support(length: float, *tests: PhaseSpaceTest) -> None:
    if any(test.support_end >= length for test in tests):
        raise ValueError("phase-space test support must lie inside the finite box")


def finite_phase_space_symplectic_form(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    radius: float,
    stretched_distance: float,
    momentum_cutoff: float,
) -> float:
    """Projected finite-box canonical symplectic form."""
    length = tortoise_length(radius, stretched_distance)
    _validate_box_support(length, first, second)
    mode_count = retained_s_wave_mode_count(
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )
    spacing = pi / length
    total = 0.0
    for mode_number in range(1, mode_count + 1):
        momentum = mode_number * spacing
        first_field, first_momentum = phase_space_spectral_components(momentum, first)
        second_field, second_momentum = phase_space_spectral_components(
            momentum, second
        )
        total += spacing * (
            first_field * second_momentum - first_momentum * second_field
        )
    return total


def finite_phase_space_covariance(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    radius: float,
    stretched_distance: float,
    momentum_cutoff: float,
) -> float:
    """Finite-box symmetric quasifree covariance at ``beta=2*pi*R``."""
    length = tortoise_length(radius, stretched_distance)
    _validate_box_support(length, first, second)
    beta = de_sitter_inverse_temperature(radius)
    mode_count = retained_s_wave_mode_count(
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )
    spacing = pi / length
    total = 0.0
    for mode_number in range(1, mode_count + 1):
        momentum = mode_number * spacing
        first_field, first_momentum = phase_space_spectral_components(momentum, first)
        second_field, second_momentum = phase_space_spectral_components(
            momentum, second
        )
        total += 0.5 * spacing * _coth(beta * momentum / 2.0) * (
            first_field * second_field / momentum
            + momentum * first_momentum * second_momentum
        )
    return total


def _simpson_integral(integrand, upper: float, steps: int) -> complex:
    _validate_positive("integration upper bound", upper)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 20 or steps % 2:
        raise ValueError("integration_steps must be an even integer at least twenty")
    spacing = upper / steps
    total = integrand(0.0) + integrand(upper)
    for index in range(1, steps):
        total += (4.0 if index % 2 else 2.0) * integrand(index * spacing)
    return spacing * total / 3.0


def continuum_phase_space_symplectic_form(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    momentum_cutoff: float,
    integration_steps: int = 1200,
) -> float:
    """Fixed-band half-line symplectic form."""
    def integrand(momentum: float) -> float:
        first_field, first_momentum = phase_space_spectral_components(momentum, first)
        second_field, second_momentum = phase_space_spectral_components(
            momentum, second
        )
        return first_field * second_momentum - first_momentum * second_field

    return float(_simpson_integral(integrand, momentum_cutoff, integration_steps))


def _zero_covariance_integrand(
    first: PhaseSpaceTest, second: PhaseSpaceTest, beta: float
) -> float:
    if first.field_bump is None or second.field_bump is None:
        return 0.0
    first_moment = first.field_scale * polynomial_bump_moment(first.field_bump, 1)
    second_moment = second.field_scale * polynomial_bump_moment(second.field_bump, 1)
    return 2.0 * first_moment * second_moment / (pi * beta)


def continuum_phase_space_covariance(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    radius: float,
    momentum_cutoff: float,
    integration_steps: int = 1200,
) -> float:
    """Fixed-band half-line symmetric quasifree covariance."""
    beta = de_sitter_inverse_temperature(radius)

    def integrand(momentum: float) -> float:
        if momentum == 0.0:
            return _zero_covariance_integrand(first, second, beta)
        first_field, first_momentum = phase_space_spectral_components(momentum, first)
        second_field, second_momentum = phase_space_spectral_components(
            momentum, second
        )
        return 0.5 * _coth(beta * momentum / 2.0) * (
            first_field * second_field / momentum
            + momentum * first_momentum * second_momentum
        )

    return float(_simpson_integral(integrand, momentum_cutoff, integration_steps))


def finite_uncertainty_margin(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    radius: float,
    stretched_distance: float,
    momentum_cutoff: float,
) -> float:
    """Return ``mu(F,F)mu(G,G)-sigma(F,G)^2/4``."""
    first_variance = finite_phase_space_covariance(
        first,
        first,
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )
    second_variance = finite_phase_space_covariance(
        second,
        second,
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )
    symplectic = finite_phase_space_symplectic_form(
        first,
        second,
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )
    return first_variance * second_variance - 0.25 * symplectic * symplectic


def finite_unequal_time_wightman(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    complex_time: complex,
    *,
    radius: float,
    stretched_distance: float,
    momentum_cutoff: float,
) -> complex:
    """Finite-box ``omega(A_F alpha_z(A_G))`` on the closed KMS strip."""
    length = tortoise_length(radius, stretched_distance)
    _validate_box_support(length, first, second)
    beta = de_sitter_inverse_temperature(radius)
    if not isfinite(complex_time.real) or not isfinite(complex_time.imag):
        raise ValueError("complex_time components must be finite")
    imaginary_time = complex_time.imag
    if imaginary_time < 0.0 or imaginary_time > beta:
        raise ValueError("complex_time must lie in the closed KMS strip")
    mode_count = retained_s_wave_mode_count(
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )
    spacing = pi / length
    total = 0.0j
    for mode_number in range(1, mode_count + 1):
        momentum = mode_number * spacing
        first_field, first_momentum = phase_space_spectral_components(momentum, first)
        second_field, second_momentum = phase_space_spectral_components(
            momentum, second
        )
        first_amplitude = (
            first_field / sqrt(2.0 * momentum)
            - 1j * sqrt(momentum / 2.0) * first_momentum
        )
        second_amplitude = (
            second_field / sqrt(2.0 * momentum)
            - 1j * sqrt(momentum / 2.0) * second_momentum
        )
        thermal_denominator = -expm1(-beta * momentum)
        forward_weight = exp(-momentum * imaginary_time) / thermal_denominator
        reverse_weight = exp(-momentum * (beta - imaginary_time)) / thermal_denominator
        real_phase = complex_exp(1j * momentum * complex_time.real)
        total += spacing * (
            forward_weight
            * first_amplitude
            * second_amplitude.conjugate()
            * real_phase
            + reverse_weight
            * first_amplitude.conjugate()
            * second_amplitude
            * real_phase.conjugate()
        )
    return total


def continuum_unequal_time_wightman(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    complex_time: complex,
    *,
    radius: float,
    momentum_cutoff: float,
    integration_steps: int = 1200,
) -> complex:
    """Fixed-band half-line ``omega(A_F alpha_z(A_G))`` on the KMS strip."""
    beta = de_sitter_inverse_temperature(radius)
    if not isfinite(complex_time.real) or not isfinite(complex_time.imag):
        raise ValueError("complex_time components must be finite")
    imaginary_time = complex_time.imag
    if imaginary_time < 0.0 or imaginary_time > beta:
        raise ValueError("complex_time must lie in the closed KMS strip")

    def integrand(momentum: float) -> complex:
        if momentum == 0.0:
            return complex(_zero_covariance_integrand(first, second, beta), 0.0)
        first_field, first_momentum = phase_space_spectral_components(momentum, first)
        second_field, second_momentum = phase_space_spectral_components(
            momentum, second
        )
        first_amplitude = (
            first_field / sqrt(2.0 * momentum)
            - 1j * sqrt(momentum / 2.0) * first_momentum
        )
        second_amplitude = (
            second_field / sqrt(2.0 * momentum)
            - 1j * sqrt(momentum / 2.0) * second_momentum
        )
        thermal_denominator = -expm1(-beta * momentum)
        forward_weight = exp(-momentum * imaginary_time) / thermal_denominator
        reverse_weight = exp(-momentum * (beta - imaginary_time)) / thermal_denominator
        real_phase = complex_exp(1j * momentum * complex_time.real)
        return (
            forward_weight
            * first_amplitude
            * second_amplitude.conjugate()
            * real_phase
            + reverse_weight
            * first_amplitude.conjugate()
            * second_amplitude
            * real_phase.conjugate()
        )

    return _simpson_integral(integrand, momentum_cutoff, integration_steps)


def finite_reverse_order_wightman(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    real_time: float,
    *,
    radius: float,
    stretched_distance: float,
    momentum_cutoff: float,
) -> complex:
    """Finite-box ``omega(alpha_t(A_G) A_F)``."""
    if not isfinite(real_time):
        raise ValueError("real_time must be finite")
    return finite_unequal_time_wightman(
        second,
        first,
        -real_time,
        radius=radius,
        stretched_distance=stretched_distance,
        momentum_cutoff=momentum_cutoff,
    )


def static_patch_phase_space_certificate(
    *,
    radius: float = 1.0,
    minimum_power: int = 64,
    steps: int = 5,
    momentum_cutoff: float = 20.0,
) -> dict[str, object]:
    """Audit fixed-UV s-wave phase-space and KMS convergence."""
    _validate_positive("radius", radius)
    if (
        isinstance(minimum_power, bool)
        or not isinstance(minimum_power, int)
        or minimum_power < 16
    ):
        raise ValueError("minimum_power must be an integer at least sixteen")
    if (
        isinstance(steps, bool)
        or not isinstance(steps, int)
        or steps < 3
        or steps > 8
    ):
        raise ValueError("steps must be an integer from three through eight")
    _validate_positive("momentum_cutoff", momentum_cutoff)
    maximum_log_scale = (2 ** (steps - 1)) * log(float(minimum_power))
    if maximum_log_scale > 680.0:
        raise ValueError("steps and minimum_power exceed stable floating range")

    field_bump = CompactPolynomialBump(0.25 * radius, 0.75 * radius, 3)
    momentum_bump = CompactPolynomialBump(0.9 * radius, 1.35 * radius, 3)
    first = PhaseSpaceTest(field_bump=field_bump, momentum_bump=momentum_bump)
    second = PhaseSpaceTest(
        field_bump=momentum_bump,
        momentum_bump=field_bump,
        field_scale=0.7,
        momentum_scale=-0.4,
    )
    continuum_symplectic = continuum_phase_space_symplectic_form(
        first, second, momentum_cutoff=momentum_cutoff
    )
    continuum_covariance = continuum_phase_space_covariance(
        first,
        second,
        radius=radius,
        momentum_cutoff=momentum_cutoff,
    )
    records = []
    beta = de_sitter_inverse_temperature(radius)
    comparison_time = 0.37 * radius + 0.4j * beta
    continuum_wightman = continuum_unequal_time_wightman(
        first,
        second,
        comparison_time,
        radius=radius,
        momentum_cutoff=momentum_cutoff,
    )
    for index in range(steps):
        log_scale = (2**index) * log(float(minimum_power))
        stretched_distance = radius * exp(-log_scale)
        finite_symplectic = finite_phase_space_symplectic_form(
            first,
            second,
            radius=radius,
            stretched_distance=stretched_distance,
            momentum_cutoff=momentum_cutoff,
        )
        finite_covariance = finite_phase_space_covariance(
            first,
            second,
            radius=radius,
            stretched_distance=stretched_distance,
            momentum_cutoff=momentum_cutoff,
        )
        real_time = 0.37 * radius
        kms_left = finite_unequal_time_wightman(
            first,
            second,
            real_time + 1j * beta,
            radius=radius,
            stretched_distance=stretched_distance,
            momentum_cutoff=momentum_cutoff,
        )
        kms_right = finite_reverse_order_wightman(
            first,
            second,
            real_time,
            radius=radius,
            stretched_distance=stretched_distance,
            momentum_cutoff=momentum_cutoff,
        )
        finite_wightman = finite_unequal_time_wightman(
            first,
            second,
            comparison_time,
            radius=radius,
            stretched_distance=stretched_distance,
            momentum_cutoff=momentum_cutoff,
        )
        records.append(
            {
                "stretched_horizon_radial_gap_delta": stretched_distance,
                "tortoise_length_X_delta": tortoise_length(
                    radius, stretched_distance
                ),
                "finite_symplectic_form": finite_symplectic,
                "continuum_symplectic_form": continuum_symplectic,
                "symplectic_error": abs(finite_symplectic - continuum_symplectic),
                "finite_cross_covariance": finite_covariance,
                "continuum_cross_covariance": continuum_covariance,
                "covariance_error": abs(finite_covariance - continuum_covariance),
                "uncertainty_margin": finite_uncertainty_margin(
                    first,
                    second,
                    radius=radius,
                    stretched_distance=stretched_distance,
                    momentum_cutoff=momentum_cutoff,
                ),
                "kms_boundary_residual": abs(kms_left - kms_right),
                "unequal_time_wightman_error": abs(
                    finite_wightman - continuum_wightman
                ),
            }
        )
    symplectic_errors = tuple(record["symplectic_error"] for record in records)
    covariance_errors = tuple(record["covariance_error"] for record in records)
    wightman_errors = tuple(record["unequal_time_wightman_error"] for record in records)
    certified_claims = {
        "numerical_audit_matches_projected_symplectic_riemann_limit": (
            symplectic_errors[-1] < symplectic_errors[0]
            and symplectic_errors[-1] < 2e-3
        ),
        "numerical_audit_matches_phase_space_covariance_riemann_limit": (
            covariance_errors[-1] < covariance_errors[0]
            and covariance_errors[-1] < 2e-3
        ),
        "finite_quasifree_uncertainty_condition_holds": all(
            record["uncertainty_margin"] >= -1e-10 for record in records
        ),
        "finite_unequal_time_kms_boundary_identity_holds": all(
            record["kms_boundary_residual"] < 1e-9 for record in records
        ),
        "numerical_audit_matches_unequal_time_riemann_limit": (
            wightman_errors[-1] < wightman_errors[0]
            and wightman_errors[-1] < 2e-3
        ),
    }
    return {
        "goal": "Static-Patch S-Wave Phase-Space KMS Regulator",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "fixed_uv_projected_quasifree_phase_space_convergence",
        "central_result": (
            "At fixed UV momentum cutoff, compactly supported s-wave Cauchy data "
            "have finite-box symplectic forms and quasifree covariances that "
            "converge as stretched-horizon Riemann sums to the half-line thermal "
            "forms. The projected finite states obey the uncertainty inequality "
            "and exact unequal-time KMS boundary identity at beta=2*pi*R."
        ),
        "claim_boundary": (
            "compact C2 polynomial bumps and a hard fixed UV bandlimit; the "
            "bandlimited quotient is spatially nonlocal, and no UV removal, "
            "all-angular Bunch-Davies identification, Hadamard/type-III theorem, "
            "continuous core, or generalized entropy is claimed"
        ),
        "certified_claims": certified_claims,
        "records": tuple(records),
        "next_physics_gate": (
            "remove the UV bandlimit on smooth data, add all angular radial "
            "operators, and identify the limiting Bunch-Davies local GNS net"
        ),
    }
