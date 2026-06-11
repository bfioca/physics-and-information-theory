"""Locality-reference-leakage inequalities for finite SO(3) codes.

Microscopically commuting observables need not commute after compression to a
code.  The logical commutator is carried by excursions through the orthogonal
complement of the code.  This module records the exact norm bookkeeping,
composes it with the repository's global orientation-risk bounds, and provides
distributed ferromagnetic models that are pairwise sharp and state-weighted
within a constant factor.

The leakage quantities here are operator amplitudes.  They are not transition
probabilities or lifetimes until a normalized operation and dynamics are
specified.
"""

from __future__ import annotations

from fractions import Fraction
from math import asin, ceil, isfinite, pi, sqrt

from .global_so3_reference_risk import (
    hard_cutoff_orientation_risk_lower_bound,
    mean_casimir_orientation_risk_lower_bound,
)


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_probability(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0 or value > 1.0:
        raise ValueError(f"{name} must lie in (0, 1]")


def compression_commutator_budget(
    *,
    generator_commutator_norm: float,
    generator_norm_a: float,
    generator_norm_b: float,
    gain_a: float,
    gain_b: float,
    locality_defect: float = 0.0,
    leakage_a_out: float = 0.0,
    leakage_a_in: float = 0.0,
    leakage_b_out: float = 0.0,
    leakage_b_in: float = 0.0,
    compression_error_a: float = 0.0,
    compression_error_b: float = 0.0,
) -> dict[str, float | bool | str]:
    """Evaluate the directed locality-reference-leakage inequality.

    ``leakage_a_out`` is ``||Q A P||`` and ``leakage_a_in`` is
    ``||P A Q||``.  The target compressed actions are ``gain_a * J_a`` and
    ``gain_b * J_b``.  For bounded operators the theorem states

    ``signal <= locality + directed leakage products + approximation``.
    """
    values = {
        "generator_commutator_norm": generator_commutator_norm,
        "generator_norm_a": generator_norm_a,
        "generator_norm_b": generator_norm_b,
        "locality_defect": locality_defect,
        "leakage_a_out": leakage_a_out,
        "leakage_a_in": leakage_a_in,
        "leakage_b_out": leakage_b_out,
        "leakage_b_in": leakage_b_in,
        "compression_error_a": compression_error_a,
        "compression_error_b": compression_error_b,
    }
    for name, value in values.items():
        _validate_nonnegative(name, value)
    if not isfinite(gain_a) or not isfinite(gain_b):
        raise ValueError("gains must be finite")

    signal = abs(gain_a * gain_b) * generator_commutator_norm
    directed_leakage = (
        leakage_b_in * leakage_a_out
        + leakage_a_in * leakage_b_out
    )
    approximation = (
        2.0 * abs(gain_b) * generator_norm_b * compression_error_a
        + 2.0 * abs(gain_a) * generator_norm_a * compression_error_b
        + 2.0 * compression_error_a * compression_error_b
    )
    supplied_budget = locality_defect + directed_leakage + approximation
    required_locality_or_leakage = max(0.0, signal - approximation)
    return {
        "nonabelian_signal": signal,
        "locality_defect": locality_defect,
        "directed_leakage_budget": directed_leakage,
        "compression_approximation_budget": approximation,
        "supplied_total_budget": supplied_budget,
        "required_locality_plus_leakage_budget": required_locality_or_leakage,
        "inequality_slack": supplied_budget - signal,
        "supplied_bounds_satisfy_theorem": supplied_budget + 1.0e-12 >= signal,
        "identity": (
            "[PAP,PBP]=P[A,B]P+PBQAP-PAQBP, with Q=I-P"
        ),
        "bound": (
            "|gain_a gain_b| ||[J_a,J_b]|| <= locality defect + "
            "lambda_B_in lambda_A_out + lambda_A_in lambda_B_out + "
            "compression approximation budget"
        ),
    }


def self_adjoint_locality_reference_leakage_bound(
    *,
    maximum_spin: float,
    gain_a: float,
    gain_b: float,
    locality_defect: float = 0.0,
    compression_error_a: float = 0.0,
    compression_error_b: float = 0.0,
) -> dict[str, float | str]:
    """Required leakage for two self-adjoint SO(3) actions.

    On an integer-spin code with largest spin ``J``, every Cartesian generator
    and every nonzero Cartesian commutator has norm ``J``.  If ``lambda_A`` and
    ``lambda_B`` are the two off-code amplitudes, then

    ``delta + 2 lambda_A lambda_B >= required_budget``.
    """
    _validate_nonnegative("maximum_spin", maximum_spin)
    _validate_nonnegative("locality_defect", locality_defect)
    _validate_nonnegative("compression_error_a", compression_error_a)
    _validate_nonnegative("compression_error_b", compression_error_b)
    if not isfinite(gain_a) or not isfinite(gain_b):
        raise ValueError("gains must be finite")

    signal = abs(gain_a * gain_b) * maximum_spin
    approximation = (
        2.0
        * maximum_spin
        * (
            abs(gain_b) * compression_error_a
            + abs(gain_a) * compression_error_b
        )
        + 2.0 * compression_error_a * compression_error_b
    )
    margin_before_locality = max(0.0, signal - approximation)
    leakage_product_budget = max(
        0.0,
        margin_before_locality - locality_defect,
    )
    return {
        "maximum_spin": maximum_spin,
        "nonabelian_signal": signal,
        "compression_approximation_budget": approximation,
        "locality_defect": locality_defect,
        "required_twice_leakage_product": leakage_product_budget,
        "minimum_leakage_product": leakage_product_budget / 2.0,
        "minimum_maximum_leakage_amplitude": sqrt(
            leakage_product_budget / 2.0
        ),
        "minimum_maximum_sqrt_locality_or_leakage_amplitude": sqrt(
            margin_before_locality / 3.0
        ),
        "positive_tradeoff": leakage_product_budget > 0.0,
        "claim_boundary": (
            "The amplitudes are operator norms. A fixed gain calibration is "
            "required; uniformly rescaling both observables rescales the "
            "absolute leakage."
        ),
    }


def required_mean_casimir_for_risk(risk_budget: float) -> float:
    """Invert ``R >= 1/(16 <J^2> + 8)`` as a necessary resource bound."""
    _validate_probability("risk_budget", risk_budget)
    return max(0.0, (1.0 / risk_budget - 8.0) / 16.0)


def minimum_continuous_spin_from_casimir(mean_casimir: float) -> float:
    """Smallest nonnegative ``j`` satisfying ``j(j+1)>=mean_casimir``."""
    _validate_nonnegative("mean_casimir", mean_casimir)
    return 0.5 * (sqrt(1.0 + 4.0 * mean_casimir) - 1.0)


def minimum_integer_spin_from_risk(risk_budget: float) -> dict[str, float | int]:
    """Return Casimir and sharp hard-cutoff spin requirements for a risk target."""
    _validate_probability("risk_budget", risk_budget)
    casimir = required_mean_casimir_for_risk(risk_budget)
    casimir_spin = minimum_continuous_spin_from_casimir(casimir)
    casimir_integer = int(ceil(casimir_spin - 1.0e-14))

    hard_cutoff_continuous = 0.0
    hard_cutoff_integer = 0
    if risk_budget < 0.75:
        hard_cutoff_continuous = max(
            0.0,
            0.5 * (pi / asin(sqrt(risk_budget)) - 3.0),
        )
        hard_cutoff_integer = int(ceil(hard_cutoff_continuous - 1.0e-14))
        hard_cutoff_integer = max(0, hard_cutoff_integer)
        while (
            hard_cutoff_integer > 0
            and hard_cutoff_orientation_risk_lower_bound(
                hard_cutoff_integer - 1
            )
            <= risk_budget
        ):
            hard_cutoff_integer -= 1
        while (
            hard_cutoff_orientation_risk_lower_bound(hard_cutoff_integer)
            > risk_budget
        ):
            hard_cutoff_integer += 1

    return {
        "risk_budget": risk_budget,
        "required_mean_casimir": casimir,
        "casimir_continuous_spin_requirement": casimir_spin,
        "casimir_integer_spin_requirement": casimir_integer,
        "hard_cutoff_continuous_spin_requirement": hard_cutoff_continuous,
        "hard_cutoff_integer_spin_requirement": hard_cutoff_integer,
        "binding_integer_spin_requirement": max(
            casimir_integer,
            hard_cutoff_integer,
        ),
    }


def operational_locality_leakage_bound(
    *,
    risk_budget: float,
    gain_a: float,
    gain_b: float,
    locality_defect: float = 0.0,
    compression_error_a: float = 0.0,
    compression_error_b: float = 0.0,
) -> dict[str, object]:
    """Compose global orientation risk with the self-adjoint leakage theorem."""
    resource = minimum_integer_spin_from_risk(risk_budget)
    required_spin = float(resource["binding_integer_spin_requirement"])
    tradeoff = self_adjoint_locality_reference_leakage_bound(
        maximum_spin=required_spin,
        gain_a=gain_a,
        gain_b=gain_b,
        locality_defect=locality_defect,
        compression_error_a=compression_error_a,
        compression_error_b=compression_error_b,
    )
    gain_margin = abs(gain_a * gain_b) - 2.0 * (
        abs(gain_b) * compression_error_a
        + abs(gain_a) * compression_error_b
    )
    return {
        "risk_resource_requirement": resource,
        "gain_margin": gain_margin,
        "gain_margin_is_positive": gain_margin > 0.0,
        "locality_reference_leakage_tradeoff": tradeoff,
        "operational_statement": (
            "Any Haar-prior SO(3) protocol attaining risk at most the declared "
            "budget on an integer-spin code must have at least the recorded "
            "spin support. At fixed gains and uniform compression errors, that "
            "support forces the recorded locality-or-leakage budget."
        ),
        "claim_boundary": (
            "This is a necessary implication. It does not prove that a state "
            "with the declared risk exists, and leakage amplitude is not yet a "
            "dynamical transition probability or lifetime."
        ),
    }


def pairwise_state_weighted_collective_mode_bound(
    *,
    generator_second_moment: float,
    maximum_spin: float,
    gain_a: float,
    gain_b: float,
    local_operator_norm_a: float,
    local_operator_norm_b: float,
    leakage_amplitude_cap_a: float | None = None,
    leakage_amplitude_cap_b: float | None = None,
    leakage_weight_a: float,
    leakage_weight_b: float,
    locality_defect: float = 0.0,
    compression_error_a: float = 0.0,
    compression_error_b: float = 0.0,
) -> dict[str, float | bool | str]:
    """State-weighted pairwise collective-mode inequality.

    For a code state ``rho``, ``leakage_weight_a`` denotes
    ``Tr(rho P A Q A P)``.  Hilbert-Schmidt Cauchy-Schwarz applied to the exact
    compression identity gives

    ``|alpha beta| sqrt(<J_c^2>)``
    `` <= Lambda_b sqrt(p_a) + Lambda_a sqrt(p_b) + delta + eta``.

    A supplied ``leakage_amplitude_cap_*`` is an assumed, independently
    certified upper bound on ``||Q A_* P||``.  The compression-error term
    ``eta`` is uniform on the entire code.
    """
    for name, value in {
        "generator_second_moment": generator_second_moment,
        "maximum_spin": maximum_spin,
        "local_operator_norm_a": local_operator_norm_a,
        "local_operator_norm_b": local_operator_norm_b,
        "leakage_weight_a": leakage_weight_a,
        "leakage_weight_b": leakage_weight_b,
        "locality_defect": locality_defect,
        "compression_error_a": compression_error_a,
        "compression_error_b": compression_error_b,
    }.items():
        _validate_nonnegative(name, value)
    if not isfinite(gain_a) or not isfinite(gain_b):
        raise ValueError("gains must be finite")
    if leakage_amplitude_cap_a is not None:
        _validate_nonnegative(
            "leakage_amplitude_cap_a", leakage_amplitude_cap_a
        )
    if leakage_amplitude_cap_b is not None:
        _validate_nonnegative(
            "leakage_amplitude_cap_b", leakage_amplitude_cap_b
        )

    cap_a = (
        local_operator_norm_a
        if leakage_amplitude_cap_a is None
        else leakage_amplitude_cap_a
    )
    cap_b = (
        local_operator_norm_b
        if leakage_amplitude_cap_b is None
        else leakage_amplitude_cap_b
    )
    if cap_a > local_operator_norm_a + 1.0e-12:
        raise ValueError(
            "leakage_amplitude_cap_a cannot exceed local_operator_norm_a"
        )
    if cap_b > local_operator_norm_b + 1.0e-12:
        raise ValueError(
            "leakage_amplitude_cap_b cannot exceed local_operator_norm_b"
        )

    approximation = (
        2.0 * abs(gain_b) * maximum_spin * compression_error_a
        + 2.0 * abs(gain_a) * maximum_spin * compression_error_b
        + 2.0 * compression_error_a * compression_error_b
    )
    target = abs(gain_a * gain_b) * sqrt(generator_second_moment)
    supplied = (
        cap_b * sqrt(leakage_weight_a)
        + cap_a * sqrt(leakage_weight_b)
        + locality_defect
        + approximation
    )
    return {
        "target_commutator_rms": target,
        "leakage_rms_budget": (
            cap_b * sqrt(leakage_weight_a)
            + cap_a * sqrt(leakage_weight_b)
        ),
        "leakage_amplitude_cap_a": cap_a,
        "leakage_amplitude_cap_b": cap_b,
        "locality_defect": locality_defect,
        "compression_approximation_budget": approximation,
        "supplied_total_budget": supplied,
        "inequality_slack": supplied - target,
        "supplied_bounds_satisfy_theorem": supplied + 1.0e-12 >= target,
        "supplied_weights_respect_certified_caps": (
            leakage_weight_a <= cap_a**2 + 1.0e-12
            and leakage_weight_b <= cap_b**2 + 1.0e-12
        ),
        "bound": (
            "|alpha beta| sqrt(Tr rho J_c^2) <= "
            "Lambda_b sqrt(p_a)+Lambda_a sqrt(p_b)+delta_ab+eta_ab"
        ),
    }


def collective_mode_leakage_from_casimir(
    *,
    mean_casimir: float,
    response_gain: float,
    local_operator_norm: float,
    leakage_amplitude_cap: float | None = None,
    maximum_spin: float | None = None,
    locality_defect: float = 0.0,
    compression_error: float = 0.0,
    young_parameter: float = 1.0,
) -> dict[str, float | bool | str | None]:
    """Three-cell state-weighted leakage forced by a Casimir resource.

    Three pairwise spacelike self-adjoint observables are assumed to compress
    to ``response_gain * J_a`` with uniform errors.  In the exact case,

    ``sum_a Tr(rho P A_a Q A_a P) >= alpha^4 <J^2>/(4 Lambda^2)``.

    Here ``Lambda`` is a caller-certified uniform upper bound on every
    ``||Q A_a P||``.  If it is omitted, ``||A_a||<=M`` supplies the coarser
    choice ``Lambda=M``.

    With locality or compression defects, a one-parameter Young inequality
    gives the robust bound recorded below.
    """
    _validate_nonnegative("mean_casimir", mean_casimir)
    _validate_positive("local_operator_norm", local_operator_norm)
    _validate_nonnegative("locality_defect", locality_defect)
    _validate_nonnegative("compression_error", compression_error)
    if not isfinite(response_gain):
        raise ValueError("response_gain must be finite")
    if maximum_spin is not None:
        _validate_nonnegative("maximum_spin", maximum_spin)
    if leakage_amplitude_cap is not None:
        _validate_positive(
            "leakage_amplitude_cap", leakage_amplitude_cap
        )
    if locality_defect > 0.0 or compression_error > 0.0:
        _validate_positive("young_parameter", young_parameter)
    if compression_error > 0.0 and maximum_spin is None:
        raise ValueError(
            "maximum_spin is required when compression_error is nonzero"
        )

    exact_case = locality_defect == 0.0 and compression_error == 0.0
    effective_cap = (
        local_operator_norm
        if leakage_amplitude_cap is None
        else leakage_amplitude_cap
    )
    if effective_cap > local_operator_norm + 1.0e-12:
        raise ValueError(
            "leakage_amplitude_cap cannot exceed local_operator_norm"
        )
    approximation = 0.0
    if compression_error > 0.0:
        approximation = (
            4.0 * abs(response_gain) * float(maximum_spin) * compression_error
            + 2.0 * compression_error * compression_error
        )
    combined_defect = locality_defect + approximation
    signal = abs(response_gain) ** 4 * mean_casimir
    if exact_case:
        denominator = 4.0 * effective_cap**2
        defect_penalty = 0.0
    else:
        denominator = (
            4.0 * (1.0 + young_parameter) * effective_cap**2
        )
        defect_penalty = (
            3.0
            * (1.0 + 1.0 / young_parameter)
            * combined_defect**2
        )
    required_weight = max(0.0, signal - defect_penalty) / denominator
    amplitude_floor_denominator = 12.0
    if not exact_case:
        amplitude_floor_denominator *= 1.0 + young_parameter
    minimum_uniform_leakage_amplitude = (
        max(0.0, signal - defect_penalty) / amplitude_floor_denominator
    ) ** 0.25
    normalized_weight = required_weight / local_operator_norm**2
    response_ratio = abs(response_gain) / local_operator_norm
    return {
        "mean_casimir": mean_casimir,
        "response_gain": response_gain,
        "local_operator_norm": local_operator_norm,
        "leakage_amplitude_cap": effective_cap,
        "leakage_cap_is_caller_certified_assumption": (
            leakage_amplitude_cap is not None
        ),
        "dimensionless_response_ratio": response_ratio,
        "compression_approximation_budget_per_pair": approximation,
        "locality_defect_per_pair": locality_defect,
        "young_parameter": young_parameter,
        "exact_case_uses_direct_factor_four": exact_case,
        "casimir_signal": signal,
        "robust_defect_penalty": defect_penalty,
        "minimum_total_off_code_weight": required_weight,
        "minimum_normalized_total_off_code_weight": normalized_weight,
        "minimum_uniform_leakage_amplitude_from_consistency": (
            minimum_uniform_leakage_amplitude
        ),
        "maximum_total_off_code_weight_under_certified_cap": (
            3.0 * effective_cap**2
        ),
        "certified_cap_is_consistent_with_required_weight": (
            required_weight <= 3.0 * effective_cap**2 + 1.0e-12
        ),
        "compression_norm_is_consistent_with_declared_maximum_spin": (
            None
            if maximum_spin is None
            else abs(response_gain) * maximum_spin
            <= local_operator_norm + compression_error + 1.0e-12
        ),
        "positive_state_weighted_tradeoff": required_weight > 0.0,
        "bound": (
            "sum_a Tr(rho P A_a Q A_a P) >= "
            "[alpha^4 Tr(rho J^2)-robust defect penalty]_+ / "
            "[4(1+t)Lambda^2], with the direct denominator 4Lambda^2 "
            "from the direct proof when defects vanish"
        ),
        "claim_boundary": (
            "A supplied Lambda must be independently proved to bound every "
            "||Q A_a P||; the scalar calculator cannot certify it. "
            "The three observables belong to three pairwise spacelike cells. "
            "The theorem does not require different current components in one "
            "cell to commute. The off-code weight becomes a transition "
            "probability only after normalizing a physical operation."
        ),
    }


def operational_collective_mode_leakage_bound(
    *,
    risk_budget: float,
    response_gain: float,
    local_operator_norm: float,
    leakage_amplitude_cap: float | None = None,
    maximum_spin: float | None = None,
    locality_defect: float = 0.0,
    compression_error: float = 0.0,
    young_parameter: float = 1.0,
) -> dict[str, object]:
    """Compose global SO(3) orientation risk with state-weighted leakage."""
    mean_casimir = required_mean_casimir_for_risk(risk_budget)
    support_requirement = minimum_integer_spin_from_risk(risk_budget)
    required_maximum_spin = float(
        support_requirement["binding_integer_spin_requirement"]
    )
    leakage = collective_mode_leakage_from_casimir(
        mean_casimir=mean_casimir,
        response_gain=response_gain,
        local_operator_norm=local_operator_norm,
        leakage_amplitude_cap=leakage_amplitude_cap,
        maximum_spin=maximum_spin,
        locality_defect=locality_defect,
        compression_error=compression_error,
        young_parameter=young_parameter,
    )
    support_is_sufficient = (
        None
        if maximum_spin is None
        else maximum_spin + 1.0e-12 >= required_maximum_spin
    )
    calibration_allows_required_support = (
        abs(response_gain) * required_maximum_spin
        <= local_operator_norm + compression_error + 1.0e-12
    )
    declared_parameters_not_ruled_out = (
        calibration_allows_required_support
        and (support_is_sufficient is not False)
        and leakage["certified_cap_is_consistent_with_required_weight"]
        and (
            leakage[
                "compression_norm_is_consistent_with_declared_maximum_spin"
            ]
            is not False
        )
    )
    return {
        "risk_budget": risk_budget,
        "required_mean_casimir": mean_casimir,
        "risk_support_requirement": support_requirement,
        "declared_maximum_spin_supports_risk_target": support_is_sufficient,
        "calibration_allows_minimum_required_spin": (
            calibration_allows_required_support
        ),
        "declared_parameters_are_not_ruled_out": (
            declared_parameters_not_ruled_out
        ),
        "risk_bound_used": "R_ref >= 1/(16 Tr(rho J^2)+8)",
        "state_weighted_leakage": leakage,
        "operational_statement": (
            "If a code state actually attains global Haar-prior orientation "
            "risk at most the declared budget, then three spacelike cells that "
            "uniformly reproduce its rigid SO(3) generators must carry at "
            "least the recorded total off-code weight."
        ),
        "claim_boundary": (
            "This is a necessary implication, not an achievability theorem. "
            "It concerns replicated rigid collective components in spacelike "
            "cells, not every localized non-Abelian current."
        ),
    }


def disjoint_block_ferromagnetic_code_record(
    site_count: int,
    *,
    buffer_sites: int = 0,
) -> dict[str, object]:
    """Exact record for the pairwise-sharp disjoint-block ferromagnetic code.

    ``site_count`` is even, so the symmetric code carries the integer spin
    ``j=N/2``.  Equal left and right blocks are separated by ``buffer_sites``
    unused sites.  The normalized block spins compress exactly to ``J_x`` and
    ``J_y`` while commuting microscopically.
    """
    if (
        isinstance(site_count, bool)
        or not isinstance(site_count, int)
        or site_count < 2
        or site_count % 2
    ):
        raise ValueError("site_count must be an even integer at least two")
    if (
        isinstance(buffer_sites, bool)
        or not isinstance(buffer_sites, int)
        or buffer_sites < 0
        or buffer_sites >= site_count
        or (site_count - buffer_sites) % 2
    ):
        raise ValueError(
            "buffer_sites must be a nonnegative integer below site_count "
            "with the same parity"
        )

    block_size = (site_count - buffer_sites) // 2
    spin = Fraction(site_count, 2)
    leakage_coefficient = Fraction(
        site_count - block_size,
        block_size * (site_count - 1),
    )
    leakage_squared = spin * spin * leakage_coefficient
    nonabelian_signal = spin
    twice_leakage_product = 2 * leakage_squared
    sharpness_ratio = twice_leakage_product / nonabelian_signal
    relative_leakage_squared = leakage_coefficient
    risk_floor = mean_casimir_orientation_risk_lower_bound(
        float(spin * (spin + 1))
    )
    hard_cutoff_floor = hard_cutoff_orientation_risk_lower_bound(int(spin))
    return {
        "model": "disjoint-block frustration-free ferromagnetic spin code",
        "site_count": site_count,
        "buffer_sites": buffer_sites,
        "block_size_each": block_size,
        "code_spin_exact": str(spin),
        "code_dimension": site_count + 1,
        "local_hamiltonian": (
            "H_F=sum_i [1/4-S_i dot S_(i+1)]; its exact ground space is "
            "Sym^N(C^2)"
        ),
        "microscopic_observables": (
            "A_x=(N/r) sum_(i in X) S_i^x and "
            "B_y=(N/r) sum_(k in Y) S_k^y"
        ),
        "microscopic_commutator_is_zero": True,
        "compressed_actions": "P A_x P=J_x and P B_y P=J_y",
        "nonabelian_signal_exact": str(nonabelian_signal),
        "leakage_coefficient_exact": str(leakage_coefficient),
        "leakage_squared_exact": str(leakage_squared),
        "leakage_amplitude": sqrt(float(leakage_squared)),
        "twice_leakage_product_exact": str(twice_leakage_product),
        "sharpness_ratio_exact": str(sharpness_ratio),
        "sharpness_ratio": float(sharpness_ratio),
        "relative_leakage_squared_exact": str(relative_leakage_squared),
        "relative_leakage": sqrt(float(relative_leakage_squared)),
        "mean_casimir_risk_floor": risk_floor,
        "hard_cutoff_risk_floor": hard_cutoff_floor,
        "exact_cross_leakage_identity": (
            "P B_y Q A_x P={J_x,J_y}/[2(N-1)]+iJ_z/2 and "
            "P A_x Q B_y P={J_x,J_y}/[2(N-1)]-iJ_z/2"
        ),
        "claim_boundary": (
            "This is a finite lattice-local code with a global projector, not "
            "an AQFT continuum, a prepared full-frame token, or a lifetime "
            "theorem."
        ),
    }


def three_cell_ferromagnetic_state_record(site_count: int) -> dict[str, object]:
    """Three disjoint blocks realizing the state-weighted theorem's scaling."""
    if (
        isinstance(site_count, bool)
        or not isinstance(site_count, int)
        or site_count < 6
        or site_count % 6
    ):
        raise ValueError("site_count must be a positive multiple of six")

    spin = Fraction(site_count, 2)
    block_size = site_count // 3
    leakage_coefficient = Fraction(2, site_count - 1)
    leakage_squared = spin * spin * leakage_coefficient
    mean_casimir = spin * (spin + 1)
    isotropic_leakage_weight_each = Fraction(site_count, 3)
    total_leakage_weight = Fraction(site_count, 1)
    state_bound_with_leakage_cap = mean_casimir / (4 * leakage_squared)
    state_bound_with_microscopic_norm = mean_casimir / (4 * spin * spin)
    scaling_ratio = total_leakage_weight / state_bound_with_leakage_cap
    return {
        "model": "three-cell disjoint-block ferromagnetic collective mode",
        "site_count": site_count,
        "block_size_each": block_size,
        "code_spin_exact": str(spin),
        "mean_casimir_exact": str(mean_casimir),
        "pairwise_microscopic_commutators_are_zero": True,
        "compressed_actions": "P A_a P=J_a for a=x,y,z",
        "leakage_amplitude_squared_exact": str(leakage_squared),
        "leakage_amplitude_cap": sqrt(float(leakage_squared)),
        "state_dependent_axis_weight": (
            "p_a(rho)=2[N^2/4-Tr(rho J_a^2)]/(N-1)"
        ),
        "isotropic_state_leakage_weight_each_exact": str(
            isotropic_leakage_weight_each
        ),
        "total_leakage_weight_exact": str(total_leakage_weight),
        "state_bound_with_leakage_cap_exact": str(
            state_bound_with_leakage_cap
        ),
        "state_bound_with_microscopic_norm_exact": str(
            state_bound_with_microscopic_norm
        ),
        "actual_to_leakage_cap_bound_ratio_exact": str(scaling_ratio),
        "actual_to_leakage_cap_bound_ratio": float(scaling_ratio),
        "asymptotic_ratio": 8.0,
        "claim_boundary": (
            "Only the sum of the three leakage weights is state-independent "
            "inside the single spin-N/2 irrep; N/3 per axis applies to the "
            "isotropic state. This checks the three-cell scaling but does not "
            "supply a high-accuracy full-frame state or dynamics."
        ),
    }


def locality_reference_leakage_certificate() -> dict[str, object]:
    """Return the deterministic theorem, composition, and sharpness audit."""
    model_records = tuple(
        disjoint_block_ferromagnetic_code_record(site_count)
        for site_count in (2, 4, 8, 16, 32, 64, 128)
    )
    buffered = disjoint_block_ferromagnetic_code_record(128, buffer_sites=2)
    three_cell = three_cell_ferromagnetic_state_record(120)
    operational = operational_locality_leakage_bound(
        risk_budget=0.01,
        gain_a=1.0,
        gain_b=1.0,
    )
    state_weighted = operational_collective_mode_leakage_bound(
        risk_budget=0.01,
        response_gain=1.0 / 15.0,
        local_operator_norm=1.0,
        maximum_spin=15.0,
    )
    claims = {
        "distributed_model_is_microscopically_local": all(
            record["microscopic_commutator_is_zero"]
            for record in model_records
        ),
        "distributed_model_satisfies_bound": all(
            record["sharpness_ratio"] >= 1.0
            for record in model_records
        ),
        "ferromagnetic_family_asymptotically_saturates_factor_two": (
            model_records[-1]["sharpness_ratio"] < 1.01
        ),
        "positive_buffer_preserves_near_saturation": (
            buffered["sharpness_ratio"] < 1.05
        ),
        "three_cell_model_realizes_state_weighted_scaling": (
            7.0
            < three_cell["actual_to_leakage_cap_bound_ratio"]
            < 9.0
        ),
        "small_global_risk_forces_positive_absolute_leakage_at_fixed_gain": (
            operational["locality_reference_leakage_tradeoff"][
                "minimum_maximum_leakage_amplitude"
            ]
            > 0.0
        ),
        "small_global_risk_forces_positive_state_weighted_leakage": (
            state_weighted["state_weighted_leakage"][
                "minimum_total_off_code_weight"
            ]
            > 0.0
        ),
        "operational_state_weighted_example_is_not_norm_vacuous": (
            state_weighted["declared_parameters_are_not_ruled_out"]
        ),
    }
    return {
        "goal": "Locality-Reference-Leakage Theorem",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": (
            "state_weighted_spacelike_replication_inequality_with_"
            "operational_so3_corollary_and_distributed_local_models"
        ),
        "theorem": (
            "For bounded self-adjoint A,B and code projector P, "
            "||[PAP,PBP]|| <= ||P[A,B]P||+2||QAP||||QBP||. "
            "Uniform approximation to noncommuting SO(3) generators adds the "
            "explicit compression-error budget. Three commuting cells obey "
            "sum p_a >= alpha^4 Tr(rho J^2)/(4 Lambda^2) for any certified "
            "uniform off-code amplitude cap Lambda."
        ),
        "certified_claims": claims,
        "operational_corollary": operational,
        "state_weighted_operational_corollary": state_weighted,
        "distributed_model_records": model_records,
        "buffered_model_record": buffered,
        "three_cell_state_weighted_model_record": three_cell,
        "claim_boundary": (
            "The compression lemma is standard and scale homogeneous. The "
            "candidate new result is the state-weighted three-cell collective-"
            "mode corollary. Both require fixed response calibration. Relative "
            "leakage can vanish in the large-spin limit, and no QFT continuum, "
            "dynamics, lifetime, gravity, or Paper U claim is made."
        ),
    }
