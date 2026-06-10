"""Exact transmission data for static ``ell=2`` de Sitter master sources.

For

``A_2 Psi=-(N Psi')'+6 Psi/r^2=D0 delta+D1 delta'+D2 delta''``

the literal metric-defined master field contains a contact ``c delta``.  The
remaining off-wall field is a standard transmission solution.  This module
records both descriptions and independently evaluates the Green-function
limits on the two sides of the wall.
"""

from __future__ import annotations

from math import isfinite

from .static_patch_l2_response import (
    l2_center_regular_solution,
    l2_center_regular_solution_derivative,
    l2_horizon_regular_solution,
    l2_horizon_regular_solution_derivative,
)


def _finite(name: str, value: float) -> float:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _geometry(wall_radius: float, static_patch_radius: float) -> tuple[float, float]:
    wall = _finite("wall_radius", wall_radius)
    patch = _finite("static_patch_radius", static_patch_radius)
    if wall <= 0.0 or patch <= 0.0 or wall >= patch:
        raise ValueError("wall must lie strictly inside a positive static patch")
    lapse = 1.0 - wall**2 / patch**2
    lapse_derivative = -2.0 * wall / patch**2
    return lapse, lapse_derivative


def l2_master_distribution_transmission_record(
    *,
    wall_radius: float,
    static_patch_radius: float,
    delta_coefficient: float,
    delta_prime_coefficient: float,
    delta_second_coefficient: float,
) -> dict[str, float | str]:
    """Convert a literal ``delta`` jet into contact and jump data.

    Jumps use ``[X]=X(a+)-X(a-)``.  The flux is ``N Psi_off'``.
    """
    lapse, lapse_p = _geometry(wall_radius, static_patch_radius)
    delta = _finite("delta_coefficient", delta_coefficient)
    delta_prime = _finite("delta_prime_coefficient", delta_prime_coefficient)
    delta_second = _finite("delta_second_coefficient", delta_second_coefficient)
    potential = 6.0 / wall_radius**2
    contact = -delta_second / lapse
    off_delta_prime = delta_prime + delta_second * lapse_p / lapse
    off_delta = delta + potential * delta_second / lapse
    field_jump = -off_delta_prime / lapse
    flux_jump = -off_delta

    recomposed_delta_second = -lapse * contact
    recomposed_delta_prime = -lapse * field_jump + lapse_p * contact
    recomposed_delta = -flux_jump + potential * contact
    residual = max(
        abs(recomposed_delta_second - delta_second),
        abs(recomposed_delta_prime - delta_prime),
        abs(recomposed_delta - delta),
    )
    return {
        "wall_lapse": lapse,
        "wall_lapse_derivative": lapse_p,
        "master_field_contact_delta_coefficient": contact,
        "contact_free_delta_prime_coefficient": off_delta_prime,
        "contact_free_delta_coefficient": off_delta,
        "off_wall_master_field_jump": field_jump,
        "off_wall_master_flux_jump": flux_jump,
        "recomposed_delta_second_coefficient": recomposed_delta_second,
        "recomposed_delta_prime_coefficient": recomposed_delta_prime,
        "recomposed_delta_coefficient": recomposed_delta,
        "distribution_recomposition_maximum_error": residual,
        "identity": (
            "Psi=c delta+Psi_off, c=-D2/N; "
            "[Psi_off]=-D1_off/N; [N Psi_off']=-D0_off"
        ),
    }


def l2_green_wall_transmission_record(
    *,
    wall_radius: float,
    static_patch_radius: float,
    contact_free_delta_coefficient: float,
    contact_free_delta_prime_coefficient: float,
) -> dict[str, float | str]:
    """Evaluate the exact two-sided Green response and its jumps at the wall."""
    lapse, _ = _geometry(wall_radius, static_patch_radius)
    delta = _finite(
        "contact_free_delta_coefficient", contact_free_delta_coefficient
    )
    delta_prime = _finite(
        "contact_free_delta_prime_coefficient", contact_free_delta_prime_coefficient
    )
    ratio = wall_radius / static_patch_radius
    center = l2_center_regular_solution(ratio)
    center_p = l2_center_regular_solution_derivative(ratio)
    horizon = l2_horizon_regular_solution(ratio)
    horizon_p = l2_horizon_regular_solution_derivative(ratio)
    green = 2.0 * static_patch_radius * center * horizon / 15.0
    source_p_left = 2.0 * center * horizon_p / 15.0
    source_p_right = 2.0 * center_p * horizon / 15.0
    mixed = 2.0 * center_p * horizon_p / (15.0 * static_patch_radius)
    radial_p_left = 2.0 * center_p * horizon / 15.0
    radial_p_right = 2.0 * center * horizon_p / 15.0

    field_left = delta * green - delta_prime * source_p_left
    field_right = delta * green - delta_prime * source_p_right
    derivative_left = delta * radial_p_left - delta_prime * mixed
    derivative_right = delta * radial_p_right - delta_prime * mixed
    field_jump = field_right - field_left
    flux_jump = lapse * (derivative_right - derivative_left)
    expected_field_jump = -delta_prime / lapse
    expected_flux_jump = -delta
    return {
        "off_wall_master_field_inner_limit": field_left,
        "off_wall_master_field_outer_limit": field_right,
        "off_wall_master_radial_derivative_inner_limit": derivative_left,
        "off_wall_master_radial_derivative_outer_limit": derivative_right,
        "off_wall_master_field_jump": field_jump,
        "off_wall_master_flux_jump": flux_jump,
        "expected_off_wall_master_field_jump": expected_field_jump,
        "expected_off_wall_master_flux_jump": expected_flux_jump,
        "field_jump_error": field_jump - expected_field_jump,
        "flux_jump_error": flux_jump - expected_flux_jump,
        "identity": (
            "D0 G-D1 d_a G has [Psi]=-D1/N and [N Psi']=-D0"
        ),
    }
