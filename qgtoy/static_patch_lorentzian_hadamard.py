"""Lorentzian conformal static-patch kernel and Hadamard benchmark.

The explicit strip kernel identifies the all-angular continuum target with the
Bunch-Davies two-point function.  Regulator-to-net convergence and local factor
classification use analytic theorems documented alongside this module; the
certificate only audits identities and stable numerical representatives.
"""

from __future__ import annotations

from cmath import cosh as complex_cosh
from cmath import exp as complex_exp
from math import acos, acosh, cosh, exp, expm1, isfinite, pi, sin, sinh, tanh

from .static_patch_all_angular import (
    bunch_davies_euclidean_kernel,
    hyperbolic_cosh_distance,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_point(
    *,
    radius: float,
    first_tortoise_coordinate: float,
    second_tortoise_coordinate: float,
    cosine_angle: float,
) -> None:
    _validate_positive("radius", radius)
    _validate_positive("first_tortoise_coordinate", first_tortoise_coordinate)
    _validate_positive("second_tortoise_coordinate", second_tortoise_coordinate)
    if not isfinite(cosine_angle) or cosine_angle < -1.0 or cosine_angle > 1.0:
        raise ValueError("cosine_angle must lie in [-1,1]")


def _sech(argument: float) -> float:
    if argument > 20.0:
        small = exp(-argument)
        return 2.0 * small / (1.0 + small * small)
    return 1.0 / cosh(argument)


def optical_kms_strip_kernel(
    complex_time_separation: complex,
    *,
    radius: float,
    first_tortoise_coordinate: float,
    second_tortoise_coordinate: float,
    cosine_angle: float,
) -> complex:
    """Holomorphic optical kernel on ``-2*pi*R < Im z < 0``."""
    _validate_point(
        radius=radius,
        first_tortoise_coordinate=first_tortoise_coordinate,
        second_tortoise_coordinate=second_tortoise_coordinate,
        cosine_angle=cosine_angle,
    )
    if not isfinite(complex_time_separation.real) or not isfinite(
        complex_time_separation.imag
    ):
        raise ValueError("complex_time_separation must be finite")
    beta = 2.0 * pi * radius
    if not -beta < complex_time_separation.imag < 0.0:
        raise ValueError("complex time must lie in the open lower KMS strip")
    distance = hyperbolic_cosh_distance(
        radius=radius,
        first_tortoise_coordinate=first_tortoise_coordinate,
        second_tortoise_coordinate=second_tortoise_coordinate,
        cosine_angle=cosine_angle,
    )
    denominator = distance - complex_cosh(complex_time_separation / radius)
    if denominator == 0.0:
        raise ValueError("kernel is singular")
    return 1.0 / (8.0 * pi * pi * radius * radius * denominator)


def bunch_davies_kms_strip_kernel(
    complex_time_separation: complex,
    *,
    radius: float,
    first_tortoise_coordinate: float,
    second_tortoise_coordinate: float,
    cosine_angle: float,
) -> complex:
    """Bunch-Davies strip kernel in static coordinates."""
    optical_kms_strip_kernel(
        complex_time_separation,
        radius=radius,
        first_tortoise_coordinate=first_tortoise_coordinate,
        second_tortoise_coordinate=second_tortoise_coordinate,
        cosine_angle=cosine_angle,
    )
    first = first_tortoise_coordinate / radius
    second = second_tortoise_coordinate / radius
    invariant = (
        _sech(first)
        * _sech(second)
        * complex_cosh(complex_time_separation / radius)
        + tanh(first) * tanh(second) * cosine_angle
    )
    denominator = 1.0 - invariant
    if denominator == 0.0:
        raise ValueError("kernel is singular")
    return 1.0 / (8.0 * pi * pi * radius * radius * denominator)


def optical_strip_spectral_integral(
    complex_time_separation: complex,
    *,
    radius: float,
    first_tortoise_coordinate: float,
    second_tortoise_coordinate: float,
    cosine_angle: float,
    dimensionless_momentum_cutoff: float = 30.0,
    integration_steps: int = 8000,
) -> complex:
    """Midpoint audit of the exact optical thermal spectral integral."""
    optical_kms_strip_kernel(
        complex_time_separation,
        radius=radius,
        first_tortoise_coordinate=first_tortoise_coordinate,
        second_tortoise_coordinate=second_tortoise_coordinate,
        cosine_angle=cosine_angle,
    )
    _validate_positive("dimensionless_momentum_cutoff", dimensionless_momentum_cutoff)
    if (
        isinstance(integration_steps, bool)
        or not isinstance(integration_steps, int)
        or integration_steps < 100
    ):
        raise ValueError("integration_steps must be an integer at least one hundred")
    beta = 2.0 * pi * radius
    momentum_cutoff = dimensionless_momentum_cutoff / radius
    spacing = momentum_cutoff / integration_steps
    cosh_distance = hyperbolic_cosh_distance(
        radius=radius,
        first_tortoise_coordinate=first_tortoise_coordinate,
        second_tortoise_coordinate=second_tortoise_coordinate,
        cosine_angle=cosine_angle,
    )
    distance = radius * acosh(cosh_distance)
    total = 0.0j
    for index in range(integration_steps):
        momentum = (index + 0.5) * spacing
        if distance == 0.0:
            spatial_density = momentum / (4.0 * pi * pi)
        else:
            spatial_density = sin(momentum * distance) / (
                4.0 * pi * pi * radius * sinh(distance / radius)
            )
        thermal_numerator = complex_exp(
            -1j * momentum * complex_time_separation
        ) + complex_exp(
            -beta * momentum + 1j * momentum * complex_time_separation
        )
        thermal_denominator = -expm1(-beta * momentum)
        total += (
            spacing
            * spatial_density
            * thermal_numerator
            / thermal_denominator
        )
    return total


def spacelike_hadamard_leading_ratio(
    *,
    radius: float,
    first_tortoise_coordinate: float,
    second_tortoise_coordinate: float,
    cosine_angle: float = 1.0,
) -> float:
    """Return ``8*pi^2*sigma*Lambda`` for an equal-time spacelike pair."""
    _validate_point(
        radius=radius,
        first_tortoise_coordinate=first_tortoise_coordinate,
        second_tortoise_coordinate=second_tortoise_coordinate,
        cosine_angle=cosine_angle,
    )
    first = first_tortoise_coordinate / radius
    second = second_tortoise_coordinate / radius
    invariant = (
        _sech(first) * _sech(second)
        + tanh(first) * tanh(second) * cosine_angle
    )
    if not -1.0 < invariant < 1.0:
        raise ValueError("points must be distinct and joined by a short spacelike geodesic")
    geodesic_distance = radius * acos(invariant)
    synge_world_function = geodesic_distance * geodesic_distance / 2.0
    kernel = 1.0 / (8.0 * pi * pi * radius * radius * (1.0 - invariant))
    return 8.0 * pi * pi * synge_world_function * kernel


def static_patch_lorentzian_hadamard_certificate(
    *,
    radius: float = 1.0,
    integration_steps: int = 8000,
) -> dict[str, object]:
    """Audit the exact strip kernel and theorem-backed local-net route."""
    _validate_positive("radius", radius)
    first = 0.7 * radius
    second = 1.1 * radius
    cosine_angle = 0.3
    beta = 2.0 * pi * radius
    euclidean_times = (0.4 * radius, 1.2 * radius, 2.1 * radius)
    euclidean_records = []
    for euclidean_time in euclidean_times:
        strip_value = bunch_davies_kms_strip_kernel(
            -1j * euclidean_time,
            radius=radius,
            first_tortoise_coordinate=first,
            second_tortoise_coordinate=second,
            cosine_angle=cosine_angle,
        )
        euclidean_value = bunch_davies_euclidean_kernel(
            radius=radius,
            euclidean_time_separation=euclidean_time,
            first_tortoise_coordinate=first,
            second_tortoise_coordinate=second,
            cosine_angle=cosine_angle,
        )
        euclidean_records.append(
            {
                "euclidean_time_over_R": euclidean_time / radius,
                "strip_value": strip_value.real,
                "closed_euclidean_value": euclidean_value,
                "absolute_error": abs(strip_value - euclidean_value),
            }
        )
    sample_time = 0.8 * radius
    epsilon = 0.2 * radius
    lower_boundary = bunch_davies_kms_strip_kernel(
        sample_time - 1j * (beta - epsilon),
        radius=radius,
        first_tortoise_coordinate=first,
        second_tortoise_coordinate=second,
        cosine_angle=cosine_angle,
    )
    reversed_boundary = bunch_davies_kms_strip_kernel(
        -sample_time - 1j * epsilon,
        radius=radius,
        first_tortoise_coordinate=second,
        second_tortoise_coordinate=first,
        cosine_angle=cosine_angle,
    )
    spectral_time = 0.8 * radius - 0.9j * radius
    spectral_closed = optical_kms_strip_kernel(
        spectral_time,
        radius=radius,
        first_tortoise_coordinate=first,
        second_tortoise_coordinate=second,
        cosine_angle=cosine_angle,
    )
    spectral_numeric = optical_strip_spectral_integral(
        spectral_time,
        radius=radius,
        first_tortoise_coordinate=first,
        second_tortoise_coordinate=second,
        cosine_angle=cosine_angle,
        integration_steps=integration_steps,
    )
    separations = (0.2, 0.1, 0.05, 0.025)
    hadamard_ratios = tuple(
        spacelike_hadamard_leading_ratio(
            radius=radius,
            first_tortoise_coordinate=0.8 * radius,
            second_tortoise_coordinate=(0.8 + separation) * radius,
        )
        for separation in separations
    )
    spectral_error = abs(spectral_numeric - spectral_closed)
    executable_checks = {
        "sampled_euclidean_restriction_matches_closed_identity": all(
            record["absolute_error"] < 1e-12 / (radius * radius)
            for record in euclidean_records
        ),
        "kms_opposite_boundary_identity_holds": abs(
            lower_boundary - reversed_boundary
        )
        < 1e-12 / (radius * radius),
        "spectral_integral_matches_closed_strip_kernel_at_sample": (
            spectral_error < 2e-8 / (radius * radius)
        ),
        "sampled_short_distance_ratio_approaches_one": (
            abs(hadamard_ratios[-1] - 1.0)
            < abs(hadamard_ratios[0] - 1.0)
            and abs(hadamard_ratios[-1] - 1.0) < 1e-4
        ),
    }
    return {
        "goal": "Lorentzian Hadamard Static-Patch Local-Net Benchmark",
        "status": "pass" if all(executable_checks.values()) else "fail",
        "status_scope": "sampled_executable_kernel_checks_only",
        "result_type": "analytic_strip_formulas_with_theorem_backed_consequences",
        "central_result": (
            "Analytic formulas give the positive-type optical thermal spectral "
            "representation, exact beta=2*pi*R KMS boundary relation, and conformal "
            "Bunch-Davies pullback. The executable status audits selected values; "
            "it does not numerically certify compact-test convergence, the "
            "Hadamard wavefront set, or factor type."
        ),
        "hadamard_dependency": (
            "The wavefront-set identification uses the standard equivalence of "
            "Hadamard form and the microlocal spectrum condition, plus the known "
            "Bunch-Davies Hadamard theorem; it is not inferred from the numerical "
            "short-distance sample."
        ),
        "local_factor_consequence": (
            "Once the limit is identified with the global de Sitter Bunch-Davies "
            "quasifree Hadamard net, Verch's theorem gives hyperfinite Type III_1 "
            "algebras for regular diamonds, including the static patch in that "
            "global representation. Their continuous cores are "
            "Type II_infinity, but this is not yet the CLPW gravitational observer "
            "corner or a generalized-entropy theorem."
        ),
        "theorem_backed_consequence_status": (
            "analytic argument plus named external theorems; excluded from the "
            "sampled executable pass/fail status"
        ),
        "pairwise_wall_limit_argument": (
            "Green reduction and finite propagation map each compact spacetime "
            "test pair to compact Cauchy data controlled by the all-angular "
            "equal-time theorem"
        ),
        "claim_boundary": (
            "exact free conformal strip kernel, KMS identity, compact-causal-hull "
            "pairwise finite-wall route, and theorem-backed Hadamard/local "
            "factor classification; no convergence of von Neumann closures from "
            "finite Type-I regulators, observer-clock constraint, positive-energy "
            "Type-II_1 corner, backreaction, or generalized entropy"
        ),
        "executable_checks": executable_checks,
        "certified_claims": executable_checks,
        "euclidean_records": tuple(euclidean_records),
        "kms_boundary_error": abs(lower_boundary - reversed_boundary),
        "spectral_integral_value": {
            "real": spectral_numeric.real,
            "imaginary": spectral_numeric.imag,
        },
        "closed_strip_value": {
            "real": spectral_closed.real,
            "imaginary": spectral_closed.imag,
        },
        "spectral_integral_error": spectral_error,
        "hadamard_leading_ratios": tuple(zip(separations, hadamard_ratios)),
        "primary_theorem_sources": (
            "https://arxiv.org/abs/gr-qc/9801099",
            "https://arxiv.org/abs/math-ph/0002021",
            "https://arxiv.org/abs/funct-an/9609004",
            "https://arxiv.org/abs/math-ph/0008029",
        ),
        "next_physics_gate": (
            "derive the observer clock/reference constraint on this local net, "
            "prove the positive-energy finite corner and trace, and test whether "
            "the redshifted missing-frame entropy becomes a gravitational index"
        ),
    }
