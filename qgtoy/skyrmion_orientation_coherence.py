"""Projective Skyrmion orientation risk under its matter-derived KMS spectrum."""

from __future__ import annotations

from math import isfinite

from .global_so3_reference_risk import (
    heat_attenuated_orientation_risk_lower_bound,
    maximum_coherence_time_from_initial_floor,
    projective_hard_cutoff_orientation_risk_lower_bound,
)
from .static_patch_pseudoscalar_gyroscope import (
    proper_time_bath_correlation_time,
    static_lapse_from_horizon_distance,
)
from .static_patch_skyrmion_bath import (
    skyrmion_current_gradient_spectrum,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def skyrmion_projective_heat_coherence_record(
    reference_cutoff: int,
    *,
    risk_budget: float,
    proper_protocol_time: float,
    coupling: float,
    horizon_distance: float,
    radius: float = 1.0,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    profile_step: float = 0.01,
    optical_correlation_time: float = 1.0,
) -> dict[str, object]:
    """Compose odd-sector risk with the matter-derived zero-mode spectrum.

    The convention is the one used by the repository's pseudoscalar Davies
    model: ``gamma_prop=g^2 S_prop(0)`` and
    ``S_prop(0)=N^-3 S_opt(0)``. AU.3a now bounds the global spectral moments;
    a separate finite-coupling ULE/Davies remainder is still required before
    this coefficient is a certified reduced-dynamics theorem.
    """
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    _validate_positive("risk_budget", risk_budget)
    if risk_budget >= 0.75:
        raise ValueError("risk_budget must be smaller than three quarters")
    _validate_nonnegative("proper_protocol_time", proper_protocol_time)
    _validate_positive("coupling", coupling)
    _validate_positive("radius", radius)
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("profile_step", profile_step)
    _validate_positive("optical_correlation_time", optical_correlation_time)

    lapse = static_lapse_from_horizon_distance(
        horizon_distance,
        radius=radius,
    )
    optical_zero_spectrum = skyrmion_current_gradient_spectrum(
        0.0,
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=profile_step,
    )
    proper_zero_spectrum = optical_zero_spectrum / lapse**3
    diffusion_rate = coupling**2 * proper_zero_spectrum
    proper_bath_time = proper_time_bath_correlation_time(
        lapse,
        optical_correlation_time=optical_correlation_time,
    )
    maximum_spin = reference_cutoff + 0.5
    maximum_casimir = maximum_spin * (maximum_spin + 1.0)
    loaded_markov_parameter = (
        diffusion_rate * proper_bath_time * maximum_casimir
    )
    initial_floor = projective_hard_cutoff_orientation_risk_lower_bound(
        reference_cutoff
    )
    dimensionless_time = diffusion_rate * proper_protocol_time
    time_floor = heat_attenuated_orientation_risk_lower_bound(
        initial_floor,
        dimensionless_time,
    )
    maximum_dimensionless_time = maximum_coherence_time_from_initial_floor(
        initial_floor,
        risk_budget,
    )
    maximum_proper_time = maximum_dimensionless_time / diffusion_rate
    return {
        "odd_reference_cutoff_J": reference_cutoff,
        "maximum_physical_spin": maximum_spin,
        "maximum_spin_casimir": maximum_casimir,
        "risk_budget_epsilon": risk_budget,
        "proper_protocol_time_T": proper_protocol_time,
        "static_lapse_N": lapse,
        "matter_optical_zero_frequency_spectrum": optical_zero_spectrum,
        "matter_proper_zero_frequency_spectrum": proper_zero_spectrum,
        "physical_coupling_g": coupling,
        "proper_orientation_diffusion_rate_gamma": diffusion_rate,
        "proper_bath_correlation_time": proper_bath_time,
        "loaded_markov_parameter_gamma_tauB_Cmax": loaded_markov_parameter,
        "initial_projective_global_risk_lower_bound": initial_floor,
        "dimensionless_diffusion_time_gamma_T": dimensionless_time,
        "global_risk_lower_bound_at_protocol_time": time_floor,
        "maximum_dimensionless_coherence_time": maximum_dimensionless_time,
        "maximum_proper_coherence_time": maximum_proper_time,
        "risk_budget_not_excluded": time_floor <= risk_budget,
        "davies_control_diagnostic": loaded_markov_parameter,
        "rate_convention": "gamma_prop=g^2 N^-3 j_Sky(0)",
        "claim_boundary": (
            "The zero-frequency coefficient follows from the leading rigid "
            "Skyrmion current and declared pseudoscalar Davies convention. "
            "AU.3a supplies conservative global spectral moments, but sharp "
            "AU.3b, finite-coupling dynamics, collective-band projection, "
            "isospin access, finite switching, stress, and lifetime errors "
            "are not included."
        ),
    }


def skyrmion_orientation_coherence_certificate() -> dict[str, object]:
    """Audit coupling and time scalings for the matter-derived rate."""
    base = skyrmion_projective_heat_coherence_record(
        8,
        risk_budget=0.1,
        proper_protocol_time=1.0,
        coupling=1.0e-3,
        horizon_distance=0.2,
    )
    doubled = skyrmion_projective_heat_coherence_record(
        8,
        risk_budget=0.1,
        proper_protocol_time=1.0,
        coupling=2.0e-3,
        horizon_distance=0.2,
    )
    late = skyrmion_projective_heat_coherence_record(
        8,
        risk_budget=0.1,
        proper_protocol_time=2.0 * base["maximum_proper_coherence_time"],
        coupling=1.0e-3,
        horizon_distance=0.2,
    )
    certified_claims = {
        "diffusion_rate_scales_quadratically_with_coupling": abs(
            doubled["proper_orientation_diffusion_rate_gamma"]
            / base["proper_orientation_diffusion_rate_gamma"]
            - 4.0
        )
        < 1.0e-12,
        "coherence_time_scales_inversely_with_rate": abs(
            doubled["maximum_proper_coherence_time"]
            / base["maximum_proper_coherence_time"]
            - 0.25
        )
        < 1.0e-12,
        "time_beyond_ceiling_is_excluded": not late["risk_budget_not_excluded"],
        "matter_spectrum_is_positive": (
            base["matter_optical_zero_frequency_spectrum"] > 0.0
        ),
    }
    return {
        "goal": "Skyrmion Matter-Derived Orientation Coherence Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "certified_claims": certified_claims,
        "base_record": base,
        "doubled_coupling_record": doubled,
        "late_time_record": late,
    }
