"""Static spherical Skyrmion lapse control from the radial metric budget."""

from __future__ import annotations

from math import cos, exp, isfinite, sin


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def skyrmion_dimensionless_enthalpy(
    radius: float,
    profile: float,
    derivative: float,
    *,
    pion_mass: float,
    curvature: float,
) -> float:
    """Return ``rho_bar+p_r_bar`` from the static mass and pressure formulas."""
    _validate_positive("radius", radius)
    if not isfinite(profile) or not isfinite(derivative):
        raise ValueError("profile data must be finite")
    if not isfinite(pion_mass) or pion_mass < 0.0:
        raise ValueError("pion_mass must be finite and nonnegative")
    if not isfinite(curvature) or curvature < 0.0:
        raise ValueError("curvature must be finite and nonnegative")
    metric = 1.0 - curvature * radius**2
    if metric <= 0.0:
        raise ValueError("radius must lie inside the static patch")
    sine = sin(profile)
    energy_density = (
        metric * (radius**2 + 8.0 * sine**2) * derivative**2 / 8.0
        + sine**2 / 4.0
        + sine**4 / (2.0 * radius**2)
        + pion_mass**2 * radius**2 * (1.0 - cos(profile)) / 4.0
    ) / radius**2
    radial_pressure = (
        metric * derivative**2 / 8.0
        + metric * sine**2 * derivative**2 / radius**2
        - sine**2 / (4.0 * radius**2)
        - sine**4 / (2.0 * radius**4)
        - pion_mass**2 * (1.0 - cos(profile)) / 4.0
    )
    return energy_density + radial_pressure


def skyrmion_enthalpy_identity(
    radius: float,
    profile: float,
    derivative: float,
    *,
    curvature: float,
) -> float:
    """Return the simplified enthalpy ``A F'^2(1/4+2sin^2F/x^2)``."""
    _validate_positive("radius", radius)
    if not isfinite(profile) or not isfinite(derivative):
        raise ValueError("profile data must be finite")
    if not isfinite(curvature) or curvature < 0.0:
        raise ValueError("curvature must be finite and nonnegative")
    metric = 1.0 - curvature * radius**2
    if metric <= 0.0:
        raise ValueError("radius must lie inside the static patch")
    return metric * derivative**2 * (
        0.25 + 2.0 * sin(profile) ** 2 / radius**2
    )


def static_bulk_lapse_metric_record(
    *,
    radial_metric_budget: float,
    lapse_coefficient_upper: float,
    radial_shape_upper: float,
) -> dict[str, float | str]:
    """Compose a sufficient radial constraint with the static lapse equation.

    If ``alpha H<=beta``, then ``alpha D<=beta D/H``. Normalizing the exterior
    bulk lapse to one gives ``sigma>=exp(-alpha D)``.
    """
    for name, value in (
        ("radial_metric_budget", radial_metric_budget),
        ("lapse_coefficient_upper", lapse_coefficient_upper),
        ("radial_shape_upper", radial_shape_upper),
    ):
        _validate_positive(name, value)
    if radial_metric_budget >= 1.0:
        raise ValueError("radial_metric_budget must be smaller than one")
    maximum_log_lapse_drop = (
        radial_metric_budget * lapse_coefficient_upper / radial_shape_upper
    )
    minimum_lapse_multiplier = exp(-maximum_log_lapse_drop)
    minimum_gtt_ratio = (
        minimum_lapse_multiplier**2 * (1.0 - radial_metric_budget)
    )
    return {
        "radial_metric_budget_beta": radial_metric_budget,
        "maximum_log_lapse_drop": maximum_log_lapse_drop,
        "minimum_bulk_lapse_multiplier_sigma": minimum_lapse_multiplier,
        "minimum_gtt_magnitude_relative_to_de_sitter": minimum_gtt_ratio,
        "maximum_relative_gtt_magnitude_deficit": 1.0 - minimum_gtt_ratio,
        "theorem": (
            "For the fixed static Skyrmion field, rho+p_r is proportional to "
            "the radial metric factor, which cancels from sigma'/sigma. The "
            "same alpha H<=beta condition therefore controls the bulk lapse."
        ),
    }
