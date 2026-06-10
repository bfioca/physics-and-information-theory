"""Finite-time noisy readout of an isotropically diffusing tidal quadrupole.

An ``SO(3)`` heat exposure ``Gamma=gamma*t`` multiplies a rank-``ell`` moment
by ``exp[-ell(ell+1) Gamma]``.  The exterior Skyrmion tidal contrast is rank
two, so in a quasi-static linear-response model

``a_frac(t)=a_frac(0) exp(-6 gamma t)``.

Linearized Jacobi evolution with unchanged zeroth-order proof-mass separation
then gives an exact double-integral transfer kernel.  This module keeps that
detector theorem separate from the still-open derivation of the diffusion
rate, Weyl interval, detector backreaction, and finite-separation remainder.
"""

from __future__ import annotations

from math import erfc, exp, expm1, isfinite, sqrt


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _nonnegative(name: str, value: float) -> float:
    value = _finite(name, value)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _positive(name: str, value: float) -> float:
    value = _finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def rank_two_heat_attenuation(exposure: float) -> float:
    """Return the exact heat multiplier of a quadrupole moment."""
    exposure = _nonnegative("exposure", exposure)
    return exp(-6.0 * exposure)


def constant_rate_rank_two_jacobi_kernel(
    interrogation_time: float,
    diffusion_rate: float,
) -> float:
    """Return ``integral_0^T (T-t) exp(-6 gamma t) dt``.

    The zero-rate value is its continuous limit ``T^2/2``.  A short-time
    series avoids cancellation when ``6 gamma T`` is tiny.
    """
    time = _nonnegative("interrogation_time", interrogation_time)
    rate = _nonnegative("diffusion_rate", diffusion_rate)
    if time == 0.0:
        return 0.0
    decay = 6.0 * rate
    if decay == 0.0:
        return time**2 / 2.0
    argument = decay * time
    if argument < 1.0e-4:
        # T^2 sum_{n>=0} (-aT)^n/[n!(n+1)(n+2)].
        term = time**2 / 2.0
        total = term
        for n in range(1, 12):
            term *= -argument / (n + 2)
            total += term
        return total
    return time / decay + expm1(-argument) / decay**2


def finite_time_tidal_readout_record(
    *,
    initial_fractional_acceleration_contrast: float,
    physical_proof_mass_separation: float,
    interrogation_time: float,
    diffusion_rate: float,
    displacement_readout_standard_deviation: float,
) -> dict[str, float | bool | str]:
    """Compose rank-two heat decay, Jacobi evolution, and Gaussian readout.

    The two hypotheses have the same initial proof-mass position and velocity.
    ``initial_fractional_acceleration_contrast`` is the difference of their
    ``ddot(xi)/xi`` values at ``t=0``.  The detector noise is a classical
    additive Gaussian with the same standard deviation under both hypotheses.
    """
    acceleration = _finite(
        "initial_fractional_acceleration_contrast",
        initial_fractional_acceleration_contrast,
    )
    separation = _positive(
        "physical_proof_mass_separation", physical_proof_mass_separation
    )
    time = _nonnegative("interrogation_time", interrogation_time)
    rate = _nonnegative("diffusion_rate", diffusion_rate)
    noise = _positive(
        "displacement_readout_standard_deviation",
        displacement_readout_standard_deviation,
    )
    exposure = rate * time
    kernel = constant_rate_rank_two_jacobi_kernel(time, rate)
    displacement = acceleration * separation * kernel
    signal_to_noise = abs(displacement) / noise
    error = 0.5 * erfc(signal_to_noise / (2.0 * sqrt(2.0)))
    endpoint_quadrupole = rank_two_heat_attenuation(exposure)
    rank_one = exp(-2.0 * exposure)
    upper_kernel = time**2 / 2.0
    lower_kernel = endpoint_quadrupole * upper_kernel
    return {
        "initial_fractional_acceleration_contrast": acceleration,
        "physical_proof_mass_separation": separation,
        "interrogation_time": time,
        "diffusion_rate": rate,
        "heat_exposure_Gamma": exposure,
        "rank_one_orientation_multiplier_at_readout": rank_one,
        "rank_two_tidal_multiplier_at_readout": endpoint_quadrupole,
        "rank_two_equals_rank_one_cubed_error": endpoint_quadrupole - rank_one**3,
        "integrated_rank_two_jacobi_kernel": kernel,
        "kernel_lower_bound": lower_kernel,
        "kernel_upper_bound": upper_kernel,
        "kernel_bounds_hold": lower_kernel <= kernel <= upper_kernel,
        "mean_displacement_contrast": displacement,
        "displacement_readout_standard_deviation": noise,
        "displacement_signal_to_noise_ratio": signal_to_noise,
        "equal_prior_optimal_gaussian_error_probability": error,
        "transfer_formula": (
            "Delta xi(T)=Delta a_frac(0)*xi0*"
            "[T/(6gamma)-(1-exp(-6gamma T))/(36gamma^2)]"
        ),
        "claim_boundary": (
            "quasi-static semiclassical rank-two mean field, constant-rate "
            "isotropic heat flow, Jacobi/Born limit, and additive Gaussian "
            "readout; no retardation, finite-separation remainder, detector "
            "backreaction, metric fluctuations, or microscopic rate theorem"
        ),
    }
