"""Certified normalized centered Skyrmion finite-switch ULE consequences.

This module consumes the directed AU.3b jump-factor moments without changing
their normalization. It reuses one declared coupling parameter in the
finite-switch and ULE formulas, uses normalized centered static-patch time, and
returns an ancilla-stable state operator-norm residual. The AU.2 radius remains
in dimensionless normalization, so both the physical unit map and the
same-action derivation are explicitly open. No diamond-distance or off-center
collective-projection claim is made here.
"""

from __future__ import annotations

from fractions import Fraction
from math import isfinite, sqrt

from .validated_interval import RationalInterval, pi_machin_interval
from .validated_skyrmion_au3 import _fraction_text
from .validated_skyrmion_au3b import ValidatedSkyrmionAU3BSharpCertificate


def _positive_fraction(name: str, value: Fraction) -> Fraction:
    if not isinstance(value, Fraction) or value <= 0:
        raise ValueError(f"{name} must be a positive Fraction")
    return value


def _nonnegative_fraction(name: str, value: Fraction) -> Fraction:
    if not isinstance(value, Fraction) or value < 0:
        raise ValueError(f"{name} must be a nonnegative Fraction")
    return value


def _spin_fraction(value: Fraction) -> Fraction:
    spin = _positive_fraction("spin", value)
    if spin.denominator not in (1, 2):
        raise ValueError("spin must be integer or half-integer")
    return spin


def _finite_float(value: Fraction) -> float | None:
    """Return a finite display-only float without weakening the exact API."""

    try:
        converted = float(value)
    except OverflowError:
        return None
    if not isfinite(converted) or (value != 0 and converted == 0):
        return None
    return converted


def _sqrt_float(value: Fraction) -> float | None:
    converted = _finite_float(value)
    return None if converted is None else sqrt(converted)


def _atanh_log_interval(value: Fraction, terms: int) -> RationalInterval:
    """Enclose ``log(value)`` for ``1<=value<2`` by an atanh series."""

    if not isinstance(terms, int) or isinstance(terms, bool) or terms < 1:
        raise ValueError("logarithm terms must be a positive integer")
    if value < 1 or value > 2:
        raise ValueError("range-reduced logarithm input must lie in [1,2]")
    z = (value - 1) / (value + 1)
    partial = sum(z ** (2 * index + 1) / (2 * index + 1) for index in range(terms))
    lower = 2 * partial
    tail = (
        Fraction(0)
        if z == 0
        else 2
        * z ** (2 * terms + 1)
        / ((2 * terms + 1) * (1 - z**2))
    )
    return RationalInterval(lower, lower + tail)


def rational_log_interval(
    value: Fraction,
    *,
    terms: int = 32,
) -> RationalInterval:
    """Return an exact rational enclosure of ``log(value)`` for ``value>=1``."""

    if not isinstance(value, Fraction) or value < 1:
        raise ValueError("logarithm input must be a Fraction at least one")
    exponent = max(0, value.numerator.bit_length() - value.denominator.bit_length())
    scale = Fraction(2**exponent)
    reduced = value / scale
    if reduced < 1:
        exponent -= 1
        scale /= 2
        reduced = value / scale
    elif reduced >= 2:
        exponent += 1
        scale *= 2
        reduced = value / scale
    log_two = _atanh_log_interval(Fraction(2), terms)
    log_reduced = _atanh_log_interval(reduced, terms)
    return log_two.scale(exponent) + log_reduced


def _certificate_moments(
    certificate: ValidatedSkyrmionAU3BSharpCertificate,
) -> tuple[Fraction, Fraction, Fraction, str, str]:
    if not isinstance(certificate, ValidatedSkyrmionAU3BSharpCertificate):
        raise TypeError("certificate must be a sharp AU.3b certificate")
    jump_l1 = _positive_fraction("jump_l1_upper_bound", certificate.jump_l1_upper_bound)
    jump_first = _positive_fraction(
        "jump_first_moment_upper_bound",
        certificate.jump_first_moment_upper_bound,
    )
    radius_upper = _positive_fraction(
        "physical_radius_upper_bound",
        certificate.physical_radius_upper_bound,
    )
    radius_lower = _positive_fraction(
        "physical_radius_lower_bound",
        certificate.physical_radius_lower_bound,
    )
    if radius_lower > radius_upper:
        raise ValueError("certificate physical-radius interval is inverted")
    provenance = certificate.physical_radius_provenance
    if not isinstance(provenance, str) or not provenance.strip():
        raise ValueError("certificate physical-radius provenance is missing")
    finite = certificate.finite_band_squared_h2_bounds
    tail = certificate.tail_squared_h2_bounds
    global_bounds = certificate.global_squared_h2_bounds
    q_norms = certificate.q_norm_upper_bounds
    if not all(len(values) == 3 for values in (finite, tail, global_bounds, q_norms)):
        raise ValueError("certificate spectral triples must have length three")
    for index, (finite_value, tail_value, global_value, q_norm) in enumerate(
        zip(finite, tail, global_bounds, q_norms)
    ):
        finite_checked = _nonnegative_fraction(
            f"finite_band_squared_h2_bounds[{index}]", finite_value
        )
        tail_checked = _nonnegative_fraction(
            f"tail_squared_h2_bounds[{index}]", tail_value
        )
        global_checked = _nonnegative_fraction(
            f"global_squared_h2_bounds[{index}]", global_value
        )
        q_checked = _positive_fraction(f"q_norm_upper_bounds[{index}]", q_norm)
        if global_checked != finite_checked + tail_checked:
            raise ValueError("certificate global spectral bound is inconsistent")
        if q_checked**2 < global_checked:
            raise ValueError("certificate q-norm does not enclose its squared bound")
    pi_upper = Fraction(22, 7)
    if jump_l1**2 < 2 * pi_upper * q_norms[0] * q_norms[1]:
        raise ValueError("certificate jump L1 bound is inconsistent with q norms")
    if jump_first**2 < 2 * pi_upper * q_norms[1] * q_norms[2]:
        raise ValueError(
            "certificate jump first-moment bound is inconsistent with q norms"
        )
    au2_digest = certificate.authenticated_au2_sha256
    snapshot_digest = certificate.authenticated_snapshot_sha256
    if (au2_digest is None) != (snapshot_digest is None):
        raise ValueError("certificate digest claims must be supplied together")
    for name, digest in (
        ("authenticated_au2_sha256", au2_digest),
        ("authenticated_snapshot_sha256", snapshot_digest),
    ):
        if digest is not None and (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise ValueError(f"{name} must be a lowercase SHA256")
    authentication = (
        "conditional_with_external_digest_claims"
        if au2_digest is not None
        else "conditional_unauthenticated_certificate"
    )
    return jump_l1, jump_first, radius_upper, provenance, authentication


def centered_pi_times_normalized_zero_spectrum_lower_bound(
    certificate: ValidatedSkyrmionAU3BSharpCertificate,
) -> Fraction:
    """Return normalized ``(pi j_Sky(0))_lower`` using ``H_Sky(0)>=1``."""

    _, _, radius_upper, _, _ = _certificate_moments(certificate)
    pi_upper = pi_machin_interval(terms=80).upper
    return Fraction(1, 24) / (pi_upper**2 * radius_upper**3)


def validated_centered_skyrmion_ule_residual(
    certificate: ValidatedSkyrmionAU3BSharpCertificate,
    *,
    spin: Fraction,
    declared_action_coupling_squared: Fraction,
    elapsed_normalized_time: Fraction,
    burn_in_normalized_time: Fraction,
    switch_lead_normalized_time: Fraction,
    logarithm_terms: int = 32,
) -> dict[str, object]:
    """Certify the normalized centered finite-switch operator-norm residual."""

    angular_momentum = _spin_fraction(spin)
    coupling_squared = _nonnegative_fraction(
        "declared_action_coupling_squared",
        declared_action_coupling_squared,
    )
    elapsed = _nonnegative_fraction("elapsed_normalized_time", elapsed_normalized_time)
    burn_in = _nonnegative_fraction("burn_in_normalized_time", burn_in_normalized_time)
    switch_lead = _nonnegative_fraction(
        "switch_lead_normalized_time",
        switch_lead_normalized_time,
    )
    effective_age = burn_in + switch_lead
    if effective_age <= 0:
        raise ValueError("burn-in plus switch lead must be positive")
    jump_l1, jump_first, _, radius_provenance, authentication = (
        _certificate_moments(certificate)
    )
    rate_scale = 144 * coupling_squared * angular_momentum**2
    initialization = 2 * rate_scale * jump_l1 * jump_first
    long_time = (
        2
        * rate_scale**2
        * jump_l1**3
        * jump_first
        * elapsed
    )
    history_log = rational_log_interval(
        1 + elapsed / effective_age,
        terms=logarithm_terms,
    ).upper
    finite_history = rate_scale * jump_l1 * jump_first * history_log
    total = initialization + long_time + finite_history
    return {
        "result_type": "validated_centered_prescribed_switch_ule_residual",
        "certificate_id": certificate.certificate_id,
        "certificate_authentication_status": authentication,
        "authenticated_au2_sha256": certificate.authenticated_au2_sha256,
        "authenticated_snapshot_sha256": certificate.authenticated_snapshot_sha256,
        "radius_provenance": radius_provenance,
        "units_status": "dimensionless_normalization; physical_length_map_required",
        "spin_L_exact": _fraction_text(angular_momentum),
        "dimension_d": int(2 * angular_momentum + 1),
        "declared_action_coupling_squared_exact": _fraction_text(coupling_squared),
        "elapsed_normalized_time_exact": _fraction_text(elapsed),
        "initialization_residual_upper_exact": _fraction_text(initialization),
        "long_time_residual_upper_exact": _fraction_text(long_time),
        "finite_history_residual_upper_exact": _fraction_text(finite_history),
        "total_residual_upper_exact": _fraction_text(total),
        "total_residual_upper": _finite_float(total),
        "norm_kind": "ancilla_stable_state_operator_norm",
        "clock": (
            "dimensionless_centered_static_patch_time; Killing_time_equals_"
            "center_proper_time_after_a_physical_unit_map"
        ),
        "single_declared_coupling_reused_by_construction": True,
        "claim_boundary": (
            "This is a dimensionless normalized consequence; an authenticated "
            "length/coupling unit map and a derivation of the declared coupling "
            "from one action are required before interpreting it as a physical "
            "time or coupling window. Conditional on the prescribed "
            "amplitude switch, exact zero-Bohr "
            "rigid collective projection, a stationary quasifree bath, remote-"
            "past preparation replaced by the displayed burn-in bound, and "
            "Casimir Lamb-shift control. This is not a diamond bound and does "
            "not control switching dynamics, collective-band leakage, access, "
            "off-center deformation, wall stress, lifetime, or gravity."
        ),
    }


def validated_centered_skyrmion_ule_heat_window(
    certificate: ValidatedSkyrmionAU3BSharpCertificate,
    *,
    spin: Fraction,
    residual_budget: Fraction,
    burnin_rate_multiples: Fraction,
    maximum_normalized_observation_time: Fraction | None = None,
    maximum_normalized_preparation_age: Fraction | None = None,
    logarithm_terms: int = 32,
) -> dict[str, object]:
    """Return an exact normalized coupling-squared window at heat time."""

    angular_momentum = _spin_fraction(spin)
    budget = _positive_fraction("residual_budget", residual_budget)
    beta = _positive_fraction("burnin_rate_multiples", burnin_rate_multiples)
    jump_l1, jump_first, _, radius_provenance, authentication = (
        _certificate_moments(certificate)
    )
    dimension = int(2 * angular_momentum + 1)
    log_dimension = rational_log_interval(
        Fraction(dimension),
        terms=logarithm_terms,
    )
    log_upper = log_dimension.upper
    zero_mode = centered_pi_times_normalized_zero_spectrum_lower_bound(certificate)
    coefficient = (
        288 * angular_momentum**2 * jump_l1 * jump_first
        + 20_736
        * (1 + 1 / (2 * beta))
        * angular_momentum**4
        * jump_l1**3
        * jump_first
        * log_upper
        / zero_mode
    )
    coupling_upper = budget / coefficient
    lower_candidates = [Fraction(0)]
    if maximum_normalized_observation_time is not None:
        deadline = _positive_fraction(
            "maximum_normalized_observation_time",
            maximum_normalized_observation_time,
        )
        lower_candidates.append(log_upper / (2 * zero_mode * deadline))
    if maximum_normalized_preparation_age is not None:
        preparation_age = _positive_fraction(
            "maximum_normalized_preparation_age",
            maximum_normalized_preparation_age,
        )
        lower_candidates.append(
            beta
            / (
                144
                * angular_momentum**2
                * jump_l1**2
                * preparation_age
            )
        )
    coupling_lower = max(lower_candidates)
    feasible = coupling_lower <= coupling_upper
    heat_time_at_upper = log_upper / (2 * coupling_upper * zero_mode)
    preparation_age_at_upper = beta / (
        144 * coupling_upper * angular_momentum**2 * jump_l1**2
    )
    return {
        "result_type": "validated_centered_prescribed_switch_ule_heat_window",
        "certificate_id": certificate.certificate_id,
        "certificate_authentication_status": authentication,
        "authenticated_au2_sha256": certificate.authenticated_au2_sha256,
        "authenticated_snapshot_sha256": certificate.authenticated_snapshot_sha256,
        "radius_provenance": radius_provenance,
        "units_status": "dimensionless_normalization; physical_length_map_required",
        "spin_L_exact": _fraction_text(angular_momentum),
        "dimension_d": dimension,
        "log_dimension_upper_exact": _fraction_text(log_upper),
        "pi_times_normalized_zero_spectrum_lower_bound_exact": _fraction_text(
            zero_mode
        ),
        "jump_l1_upper_bound_exact": _fraction_text(jump_l1),
        "jump_first_moment_upper_bound_exact": _fraction_text(jump_first),
        "residual_coefficient_upper_exact": _fraction_text(coefficient),
        "residual_budget_exact": _fraction_text(budget),
        "coupling_squared_lower_bound_exact": _fraction_text(coupling_lower),
        "coupling_squared_upper_bound_exact": _fraction_text(coupling_upper),
        "coupling_upper_diagnostic": _sqrt_float(coupling_upper),
        "coupling_window_nonempty": feasible,
        "heat_normalized_time_upper_at_coupling_cap_exact": _fraction_text(
            heat_time_at_upper
        ),
        "heat_center_normalized_proper_time_upper_at_coupling_cap_exact": (
            _fraction_text(heat_time_at_upper)
        ),
        "required_normalized_preparation_age_at_cap_exact": _fraction_text(
            preparation_age_at_upper
        ),
        "residual_at_coupling_cap_exact": _fraction_text(
            coefficient * coupling_upper
        ),
        "norm_kind": "ancilla_stable_state_operator_norm",
        "clock": (
            "dimensionless_centered_static_patch_time; Killing_time_equals_"
            "center_proper_time_after_a_physical_unit_map"
        ),
        "single_declared_coupling_reused_by_construction": True,
        "projective_spin_recovery_composition_status": (
            "half_integer_kinematics_only; a norm-matched projective recovery "
            "transfer remains open"
            if angular_momentum.denominator == 2
            else "integer-spin SO(3) recovery transfer available separately"
        ),
        "claim_boundary": (
            "This is a sufficient dimensionless normalized centered finite-"
            "switch ULE window for a "
            "prescribed amplitude-modulated charge-flux action. It assumes the "
            "rigid zero-Bohr collective projection, quasifree bath, preparation "
            "condition, and Lamb-shift control. It is not a diamond bound, an "
            "autonomous switching derivation, an off-center lapse theorem, or a "
            "bound on projection leakage, access, stress, lifetime, junctions, "
            "metric response, gravitational backreaction, the physical "
            "length/coupling unit map, or a same-action derivation of the "
            "declared coupling."
        ),
    }
