"""Exterior metric and electric-Weyl reconstruction for static de Sitter.

In source-free ``ell=2`` Regge--Wheeler gauge, the repository master
normalization gives

``H0=H2=Psi'+3 Psi/r`` and ``K=N Psi'+3 Psi/r``.

Because pure de Sitter is conformally flat, its linearized Weyl tensor is
gauge invariant.  The radial electric component measured in the background
static orthonormal frame is

``delta C_(t r t r)=-6 Psi Y/r^3``.
"""

from __future__ import annotations

from math import isfinite, pi, sqrt

from .centrifugal_skyrmion_physical_response import (
    physical_skyrmion_master_response_record,
)
from .static_patch_l2_response import (
    l2_horizon_regular_solution,
    l2_horizon_regular_solution_derivative,
)


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _geometry(radius: float, static_patch_radius: float) -> tuple[float, float]:
    radius = _finite("radius", radius)
    patch = _finite("static_patch_radius", static_patch_radius)
    if radius <= 0.0 or patch <= 0.0 or radius >= patch:
        raise ValueError("radius must lie strictly inside a positive static patch")
    return 1.0 - radius**2 / patch**2, -2.0 * radius / patch**2


def vacuum_l2_rw_reconstruction_record(
    *,
    radius: float,
    static_patch_radius: float,
    master_field: float,
    master_field_derivative: float,
) -> dict[str, float | str]:
    """Reconstruct the source-free RW amplitudes and radial Weyl coefficient."""
    lapse, lapse_p = _geometry(radius, static_patch_radius)
    master = _finite("master_field", master_field)
    master_p = _finite("master_field_derivative", master_field_derivative)
    master_pp = (-lapse_p * master_p + 6.0 * master / radius**2) / lapse
    temporal = master_p + 3.0 * master / radius
    radial = temporal
    angular = lapse * master_p + 3.0 * master / radius
    temporal_p = master_pp + 3.0 * master_p / radius - 3.0 * master / radius**2
    angular_p = (
        lapse_p * master_p
        + lapse * master_pp
        + 3.0 * master_p / radius
        - 3.0 * master / radius**2
    )
    radial_angular_residual = lapse * (temporal_p - angular_p) + (
        -temporal + (1.0 - 2.0 * radius**2 / static_patch_radius**2) * radial
    ) / radius
    radial_einstein_residual = (
        -lapse * temporal_p / radius
        + (1.0 - 2.0 * radius**2 / static_patch_radius**2)
        * angular_p
        / radius
        + 3.0 * temporal / radius**2
        + (-1.0 + 3.0 * radius**2 / static_patch_radius**2)
        * radial
        / radius**2
        - 2.0 * angular / radius**2
    )
    master_roundtrip = radius * (
        angular + lapse * (radial - radius * angular_p) / 2.0
    ) / 3.0
    return {
        "temporal_metric_amplitude_H0": temporal,
        "radial_metric_amplitude_H2": radial,
        "angular_metric_amplitude_K": angular,
        "angular_metric_amplitude_derivative": angular_p,
        "vacuum_master_second_derivative": master_pp,
        "master_roundtrip": master_roundtrip,
        "master_roundtrip_error": master_roundtrip - master,
        "radial_angular_einstein_residual": radial_angular_residual,
        "radial_einstein_residual": radial_einstein_residual,
        "radial_electric_weyl_coefficient": -6.0 * master / radius**3,
        "identity": (
            "H0=H2=Psi'+3Psi/r; K=N Psi'+3Psi/r; "
            "delta C_(t r t r)=-6Psi Y/r^3"
        ),
    }


def direct_rw_radial_electric_weyl_coefficient(
    *,
    radius: float,
    static_patch_radius: float,
    temporal_metric_amplitude: float,
    temporal_metric_amplitude_derivative: float,
    temporal_metric_amplitude_second_derivative: float,
) -> float:
    """Return ``delta C_(t r t r)/Y`` directly from a vacuum RW metric."""
    lapse, _ = _geometry(radius, static_patch_radius)
    temporal = _finite("temporal_metric_amplitude", temporal_metric_amplitude)
    temporal_p = _finite(
        "temporal_metric_amplitude_derivative",
        temporal_metric_amplitude_derivative,
    )
    temporal_pp = _finite(
        "temporal_metric_amplitude_second_derivative",
        temporal_metric_amplitude_second_derivative,
    )
    return (
        -lapse * temporal_pp / 2.0
        + 2.0 * radius * temporal_p / static_patch_radius**2
        + temporal / static_patch_radius**2
    )


def horizon_regular_l2_weyl_record(
    *,
    radius: float,
    static_patch_radius: float,
    exterior_master_amplitude: float,
) -> dict[str, float | str]:
    """Reconstruct a horizon-regular exterior field ``Psi=A v(r/R)``."""
    _geometry(radius, static_patch_radius)
    amplitude = _finite("exterior_master_amplitude", exterior_master_amplitude)
    ratio = radius / static_patch_radius
    master = amplitude * l2_horizon_regular_solution(ratio)
    master_p = (
        amplitude
        * l2_horizon_regular_solution_derivative(ratio)
        / static_patch_radius
    )
    return {
        "exterior_master_amplitude": amplitude,
        "master_field": master,
        "master_field_derivative": master_p,
        **vacuum_l2_rw_reconstruction_record(
            radius=radius,
            static_patch_radius=static_patch_radius,
            master_field=master,
            master_field_derivative=master_p,
        ),
    }


def physical_skyrmion_exterior_weyl_record(
    *,
    skyrme_coupling: float,
    pion_decay_constant: float,
    newton_constant: float,
    spin: float,
    state_density_matrix: object,
    node_count: int = 401,
    observation_radii: tuple[float, ...] = (5.0, 10.0, 15.0),
    maximum_slow_rotation: float | None = None,
) -> dict[str, object]:
    """Return the physically normalized exterior radial tidal quadrupole."""
    response = physical_skyrmion_master_response_record(
        skyrme_coupling=skyrme_coupling,
        pion_decay_constant=pion_decay_constant,
        newton_constant=newton_constant,
        spin=spin,
        state_density_matrix=state_density_matrix,
        node_count=node_count,
        observation_radii=observation_radii,
        maximum_slow_rotation=maximum_slow_rotation,
    )
    units = response["physical_units"]
    wall = float(units["physical_wall_radius"])
    if any(
        float(sample["physical_radius"]) <= wall
        for sample in response["response_samples"]
    ):
        raise ValueError("Weyl reconstruction samples must lie outside the matter wall")
    samples = []
    exterior_amplitudes = []
    for sample in response["response_samples"]:
        radius = float(sample["physical_radius"])
        master_tensor = sample["physical_master_tensor_Psi_ab"]
        factor = -6.0 / radius**3
        weyl_tensor = tuple(
            tuple(factor * float(value) for value in row) for row in master_tensor
        )
        norm_squared = sum(value**2 for row in weyl_tensor for value in row)
        angular_integral = 8.0 * pi * norm_squared / 15.0
        angular_rms = sqrt(2.0 * norm_squared / 15.0)
        dimensionless_radius = float(sample["dimensionless_radius_x"])
        ratio = dimensionless_radius / float(
            response["dimensionless_response_provenance"]["curvature_lambda"]
        ) ** (-0.5)
        exterior_amplitudes.append(
            float(sample["dimensionless_master_coefficient_psi0"])
            / l2_horizon_regular_solution(ratio)
        )
        samples.append(
            {
                "dimensionless_radius_x": dimensionless_radius,
                "physical_radius": radius,
                "physical_radial_electric_weyl_tensor_Err_ab": weyl_tensor,
                "physical_radial_electric_weyl_angular_integral": angular_integral,
                "physical_radial_electric_weyl_angular_rms": angular_rms,
                "physical_dimension": "inverse_length_squared",
            }
        )
    amplitude_spread = max(exterior_amplitudes) - min(exterior_amplitudes)
    return {
        "physical_units": units,
        "collective_state": response["collective_state"],
        "exterior_master_amplitudes_psi0": tuple(exterior_amplitudes),
        "exterior_master_amplitude_spread": amplitude_spread,
        "response_samples": tuple(samples),
        "observable": (
            "radial electric Weyl component measured by background static "
            "orthonormal observers outside the source"
        ),
        "claim_boundary": (
            "Gauge-invariant exterior linear tidal curvature on fixed pure de "
            "Sitter. It does not supply tensorial Israel matching, a "
            "self-gravitating background, or detector dynamics."
        ),
    }
