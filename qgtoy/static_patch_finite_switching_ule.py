"""Finite switch-on and burn-in correction for the stationary ULE route.

Nathan--Rudner bound the missing bath history at finite initialization by a
rate correction proportional to ``Gamma tau / age``.  For an interaction
amplitude that reaches a stationary plateau, a finite ramp contributes an
effective lead time.  Integrating the rate correction under the unital ULE
semigroup gives a logarithmic finite-preparation error.

This is a proof adaptation of their Appendix A.6 and Appendix C, not a theorem
quoted verbatim from that paper.
"""

from __future__ import annotations

from math import exp, expm1, isfinite, log, log1p, pi, sqrt

from .static_patch_overlapping_ule import (
    smeared_gradient_zero_frequency_spectrum,
)
from .static_patch_worldtube_ule import (
    ancilla_stable_ule_spectral_residual_bound,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def switch_effective_lead_time_lower_bound(
    maximum_switch_slope: float,
) -> float:
    """Return ``1/||chi'||_infinity`` for a plateau-reaching amplitude ramp.

    If ``delta(z)=1-chi(t_s-z)``, Lipschitz continuity and ``chi(t_s)=1`` give
    ``delta(z)<=||chi'||_infinity z``.  Hence the exact effective lead
    ``inf z/delta(z)`` is at least the returned value.  A linear ramp saturates
    this bound.
    """
    _validate_positive("maximum_switch_slope", maximum_switch_slope)
    return 1.0 / maximum_switch_slope


def ancilla_stable_finite_switch_ule_residual_bound(
    spin: int,
    lapse: float,
    coupling: float,
    elapsed_time: float,
    burn_in: float,
    switch_effective_lead: float,
    jump_l1_bound: float,
    jump_first_moment_bound: float,
) -> float:
    """Return the stationary ULE residual including finite bath history.

    The additional term is
    ``Gamma tau log(1+T/(B+T_chi))``.  The stationary ULE is initialized at the
    actual physical state after the amplitude has reached its plateau and the
    declared burn-in has elapsed.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_nonnegative("coupling", coupling)
    _validate_nonnegative("elapsed_time", elapsed_time)
    _validate_nonnegative("burn_in", burn_in)
    _validate_nonnegative("switch_effective_lead", switch_effective_lead)
    _validate_positive("jump_l1_bound", jump_l1_bound)
    _validate_nonnegative(
        "jump_first_moment_bound", jump_first_moment_bound
    )
    effective_age = burn_in + switch_effective_lead
    if effective_age <= 0.0:
        raise ValueError("burn_in + switch_effective_lead must be positive")
    stationary = ancilla_stable_ule_spectral_residual_bound(
        spin,
        lapse,
        coupling,
        elapsed_time,
        jump_l1_bound,
        jump_first_moment_bound,
    )
    gamma_tau_bound = (
        144.0
        * coupling**2
        * spin**2
        * jump_l1_bound
        * jump_first_moment_bound
        / lapse**2
    )
    return stationary + gamma_tau_bound * log1p(elapsed_time / effective_age)


def minimum_burn_in_for_switch_error(
    elapsed_time: float,
    switch_effective_lead: float,
    gamma_tau_bound: float,
    switch_error_budget: float,
) -> float:
    """Return the minimum plateau burn-in for a switch-transient budget."""
    _validate_nonnegative("elapsed_time", elapsed_time)
    _validate_nonnegative("switch_effective_lead", switch_effective_lead)
    _validate_positive("gamma_tau_bound", gamma_tau_bound)
    _validate_positive("switch_error_budget", switch_error_budget)
    if elapsed_time == 0.0:
        return 0.0
    ratio = switch_error_budget / gamma_tau_bound
    if ratio < 1.0:
        required_age = elapsed_time / expm1(ratio)
    else:
        decay = exp(-ratio)
        required_age = elapsed_time * decay / (1.0 - decay)
    return max(0.0, required_age - switch_effective_lead)


def required_effective_age_for_bounded_heat_coefficient(
    spin: int,
    lapse: float,
    coupling: float,
    jump_l1_bound: float,
    *,
    burnin_rate_multiples: float = 10.0,
) -> float:
    """Return the preparation age required by the bounded heat estimate.

    With ``G<=jump_l1_bound``, set
    ``Gamma_bar=144 lambda^2 L^2 G_bar^2/N^2``.  Requiring
    ``B+T_chi>=beta/Gamma_bar`` makes the bounded finite-history contribution
    at most ``(Gamma^2 tau)_bar T/beta`` because
    ``(Gamma tau)_bar Gamma_bar=(Gamma^2 tau)_bar``.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_nonnegative("coupling", coupling)
    _validate_positive("jump_l1_bound", jump_l1_bound)
    _validate_positive("burnin_rate_multiples", burnin_rate_multiples)
    if coupling == 0.0:
        # With no interaction there is no switching transient to prepare away.
        return 0.0
    gamma_upper_bound = (
        144.0
        * coupling**2
        * spin**2
        * jump_l1_bound**2
        / lapse**2
    )
    return burnin_rate_multiples / gamma_upper_bound


def finite_switch_logarithmic_heat_ule_residual_bound(
    spin: int,
    lapse: float,
    coupling: float,
    jump_l1_bound: float,
    jump_first_moment_bound: float,
    *,
    burnin_rate_multiples: float = 10.0,
    radius: float = 1.0,
    zero_frequency_spectrum: float | None = None,
) -> float:
    """Return the heat-time residual with ``B+T_chi>=beta/Gamma_bar``.

    The finite-history term changes the long-time coefficient by
    ``1+1/(2 beta)`` and leaves the large-d coupling exponent unchanged.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_nonnegative("coupling", coupling)
    _validate_positive("jump_l1_bound", jump_l1_bound)
    _validate_positive(
        "jump_first_moment_bound", jump_first_moment_bound
    )
    _validate_positive("burnin_rate_multiples", burnin_rate_multiples)
    _validate_positive("radius", radius)
    if zero_frequency_spectrum is None:
        zero_spectrum = smeared_gradient_zero_frequency_spectrum(radius=radius)
    else:
        _validate_positive("zero_frequency_spectrum", zero_frequency_spectrum)
        zero_spectrum = zero_frequency_spectrum
    dimension = 2 * spin + 1
    first = (
        288.0
        * jump_l1_bound
        * jump_first_moment_bound
        * coupling**2
        * spin**2
        / lapse**2
    )
    second = (
        20_736.0
        * (1.0 + 1.0 / (2.0 * burnin_rate_multiples))
        / (pi * zero_spectrum)
        * jump_l1_bound**3
        * jump_first_moment_bound
        * coupling**2
        * spin**4
        * log(float(dimension))
        / lapse**2
    )
    return first + second


def finite_switch_logarithmic_heat_ule_coupling_cap(
    spin: int,
    lapse: float,
    spectral_residual_budget: float,
    jump_l1_bound: float,
    jump_first_moment_bound: float,
    *,
    burnin_rate_multiples: float = 10.0,
    radius: float = 1.0,
    zero_frequency_spectrum: float | None = None,
) -> float:
    """Return the sufficient heat-time coupling cap with finite switch-on."""
    _validate_positive("spectral_residual_budget", spectral_residual_budget)
    unit = finite_switch_logarithmic_heat_ule_residual_bound(
        spin,
        lapse,
        1.0,
        jump_l1_bound,
        jump_first_moment_bound,
        burnin_rate_multiples=burnin_rate_multiples,
        radius=radius,
        zero_frequency_spectrum=zero_frequency_spectrum,
    )
    return sqrt(spectral_residual_budget / unit)


def _collective_heat_time(
    spin: int,
    lapse: float,
    coupling: float,
    zero_frequency_spectrum: float,
) -> float:
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_positive("coupling", coupling)
    _validate_positive("zero_frequency_spectrum", zero_frequency_spectrum)
    dimension = 2 * spin + 1
    return (
        lapse**2
        * log(float(dimension))
        / (2.0 * pi * coupling**2 * zero_frequency_spectrum)
    )


def static_patch_finite_switching_ule_certificate(
    *,
    maximum_spin: int = 4096,
    radius: float = 1.0,
    burnin_rate_multiples: float = 10.0,
) -> dict[str, object]:
    """Audit finite preparation without changing the ULE scaling exponent."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 256:
        raise ValueError("maximum_spin must be at least two hundred fifty-six")
    _validate_positive("radius", radius)
    _validate_positive("burnin_rate_multiples", burnin_rate_multiples)
    jump_l1_bound = 3.0 / radius**1.5
    jump_first_moment_bound = 1.0 / radius**0.5
    zero_spectrum = smeared_gradient_zero_frequency_spectrum(radius=radius)
    spins = tuple(
        sorted(
            {spin for spin in (64, 256, 1024, maximum_spin) if spin <= maximum_spin}
            | {maximum_spin}
        )
    )
    records = []
    for spin in spins:
        dimension = 2 * spin + 1
        lapse = 1.0 / dimension
        schedule_records = {}
        for name, budget, scaling_power in (
            ("constant_obstruction", 1.0 / (4.0 * dimension), 3.5),
            ("heat_matching", 1.0 / (4.0 * dimension**2), 4.0),
        ):
            switched_cap = finite_switch_logarithmic_heat_ule_coupling_cap(
                spin,
                lapse,
                budget,
                jump_l1_bound,
                jump_first_moment_bound,
                burnin_rate_multiples=burnin_rate_multiples,
                radius=radius,
            )
            stationary_cap = finite_switch_logarithmic_heat_ule_coupling_cap(
                spin,
                lapse,
                budget,
                jump_l1_bound,
                jump_first_moment_bound,
                burnin_rate_multiples=1.0e300,
                radius=radius,
            )
            gamma_upper_bound = (
                144.0
                * switched_cap**2
                * spin**2
                * jump_l1_bound**2
                / lapse**2
            )
            required_age = required_effective_age_for_bounded_heat_coefficient(
                spin,
                lapse,
                switched_cap,
                jump_l1_bound,
                burnin_rate_multiples=burnin_rate_multiples,
            )
            heat_time = _collective_heat_time(
                spin,
                lapse,
                switched_cap,
                zero_spectrum,
            )
            witness_residual = ancilla_stable_finite_switch_ule_residual_bound(
                spin,
                lapse,
                switched_cap,
                heat_time,
                required_age,
                0.0,
                jump_l1_bound,
                jump_first_moment_bound,
            )
            age_power = 2.0 * scaling_power - 4.0
            schedule_records[name] = {
                "spectral_residual_budget": budget,
                "finite_switch_coupling_cap": switched_cap,
                "stationary_coupling_cap": stationary_cap,
                "finite_switch_to_stationary_cap_ratio": (
                    switched_cap / stationary_cap
                ),
                "scaled_finite_switch_cap": (
                    switched_cap
                    * dimension**scaling_power
                    * sqrt(log(float(dimension)))
                ),
                "gamma_rate_upper_bound_at_cap": gamma_upper_bound,
                "required_bound_level_effective_age": required_age,
                "heat_time_at_cap": heat_time,
                "finite_burnin_witness_residual": witness_residual,
                "scaled_required_age": (
                    required_age
                    / (dimension**age_power * log(float(dimension)))
                ),
                "scaled_age_to_heat_time_ratio": (
                    required_age
                    / heat_time
                    * dimension**2
                    * log(float(dimension))
                ),
            }
        records.append(
            {
                "spin_L": spin,
                "dimension_d": dimension,
                "lapse_N": lapse,
                "constant_obstruction_schedule": schedule_records[
                    "constant_obstruction"
                ],
                "heat_matching_schedule": schedule_records["heat_matching"],
            }
        )
    first = records[0]
    last = records[-1]
    schedule_names = ("constant_obstruction_schedule", "heat_matching_schedule")
    expected_cap_ratio = 1.0 / sqrt(
        1.0 + 1.0 / (2.0 * burnin_rate_multiples)
    )
    executable_checks = {
        "lipschitz_linear_ramp_lead_is_exact": abs(
            switch_effective_lead_time_lower_bound(0.25) - 4.0
        )
        < 1.0e-15,
        "finite_switch_caps_are_positive": all(
            record[name]["finite_switch_coupling_cap"] > 0.0
            for record in records
            for name in schedule_names
        ),
        "scaling_audit_uses_at_least_two_distinct_spins": len(records) >= 2,
        "finite_burnin_witnesses_satisfy_budgets": all(
            record[name]["finite_burnin_witness_residual"]
            <= record[name]["spectral_residual_budget"]
            for record in records
            for name in schedule_names
        ),
        "finite_switch_penalty_matches_coefficient": all(
            abs(
                record[name]["finite_switch_to_stationary_cap_ratio"]
                - expected_cap_ratio
            )
            < 1.0e-6
            for record in records
            for name in schedule_names
        ),
        "finite_switch_preserves_d_minus_seven_halves_scaling": abs(
            last["constant_obstruction_schedule"]["scaled_finite_switch_cap"]
            / first["constant_obstruction_schedule"]["scaled_finite_switch_cap"]
            - 1.0
        )
        < 0.08,
        "finite_switch_preserves_d_minus_four_scaling": abs(
            last["heat_matching_schedule"]["scaled_finite_switch_cap"]
            / first["heat_matching_schedule"]["scaled_finite_switch_cap"]
            - 1.0
        )
        < 0.08,
        "required_age_scalings_are_visible": all(
            abs(
                last[name]["scaled_required_age"]
                / first[name]["scaled_required_age"]
                - 1.0
            )
            < 0.12
            for name in schedule_names
        ),
        "age_to_heat_time_ratio_has_common_scaling": all(
            abs(
                last[name]["scaled_age_to_heat_time_ratio"]
                / first[name]["scaled_age_to_heat_time_ratio"]
                - 1.0
            )
            < 0.12
            for name in schedule_names
        ),
    }
    return {
        "goal": "Finite Switch-On And Burn-In ULE Gate",
        "status": "pass" if all(executable_checks.values()) else "fail",
        "result_type": "conditional_finite_preparation_schedule_audit",
        "central_result": (
            "After a prescribed amplitude ramp reaches a stationary plateau, the "
            "missing bath history contributes at most Gamma tau times "
            "log(1+T/(B+T_chi)). The exact theorem uses "
            "B+T_chi>=beta/Gamma. The executable bounded corollary reports "
            "beta/Gamma_bar and constructs a burn-in witness for each of the "
            "two sufficient large-d coupling schedules."
        ),
        "burnin_rate_multiples": burnin_rate_multiples,
        "preparation_condition_status": (
            "mathematical witnesses evaluated at B=beta/Gamma_bar and T_chi=0; "
            "no physical protocol is asserted to realize these often very "
            "large preparation ages"
        ),
        "default_three_percent_penalty_diagnostic": (
            burnin_rate_multiples == 10.0
            and 1.0 - expected_cap_ratio < 0.03
        ),
        "analytic_theorem_results": (
            "a linear ramp contributes its full duration to effective lead time",
            "the finite-history bound is stable under an arbitrary inert memory",
            "a separately smooth switch-on and later smooth switch-off can give compact time support without affecting plateau readout",
        ),
        "executable_checks": executable_checks,
        "records": tuple(records),
        "claim_boundary": (
            "This adapts the Nathan-Rudner finite-initialization and modified-"
            "state proofs to a prescribed Lipschitz amplitude switch with "
            "0<=chi<=1. "
            "It applies after the stationary plateau begins, assumes a "
            "stationary zero-mean Gaussian bath and factorization before "
            "switch-on, and is not a diamond-norm or nonzero-Bohr theorem."
        ),
        "next_physics_gate": (
            "derive the switching profile from the finite worldtube action and "
            "solve the genuine held-off-center matter deformation"
        ),
    }
