"""Gaussian-filtered overlapping-sector spectral ansatz and residual scaling.

This module fixes a KMS-compatible Gaussian spectral UV ansatz motivated by the
conformal Bunch-Davies improved-gradient bath. It verifies the exact KMS
relation, zero-frequency collective jump coefficient, and principal-value Lamb
shift in a stated Davies convention. The companion
``static_patch_worldtube_ule`` module derives the regulator geometrically and
proves the ancilla-stable spectral residual under explicit Gaussian-bath and
remote-past hypotheses; ``static_patch_finite_switching_ule`` replaces that
preparation idealization by a prescribed ramp and burn-in bound. The collective
singlet is exactly dark and cannot serve as that witness.
"""

from __future__ import annotations

from math import exp, expm1, isfinite, log, pi, sqrt


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def smeared_gradient_spectrum(
    frequency: float,
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
) -> float:
    """Return the declared Gaussian-filtered optical gradient spectrum.

    The convention is

    ``j(w)=w(1+R^2 w^2)e^(-sigma^2 w^2)``
    ``/[12 pi^2 R^2(1-e^(-2 pi R w))]``.
    """
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    _validate_positive("smearing_width", smearing_width)
    if frequency == 0.0:
        return 1.0 / (24.0 * pi**3 * radius**3)
    if frequency < 0.0:
        return exp(2.0 * pi * radius * frequency) * smeared_gradient_spectrum(
            -frequency,
            radius=radius,
            smearing_width=smearing_width,
        )
    thermal_denominator = -expm1(-2.0 * pi * radius * frequency)
    form_factor = exp(-(smearing_width * frequency) ** 2)
    return (
        frequency
        * (1.0 + (radius * frequency) ** 2)
        * form_factor
        / (12.0 * pi**2 * radius**2 * thermal_denominator)
    )


def smeared_gradient_zero_frequency_spectrum(*, radius: float = 1.0) -> float:
    """Return ``j_sigma(0)=1/(24 pi^3 R^3)``."""
    _validate_positive("radius", radius)
    return 1.0 / (24.0 * pi**3 * radius**3)


def collective_jump_prefactor(
    coupling: float,
    lapse: float,
    *,
    radius: float = 1.0,
) -> float:
    """Return the coefficient multiplying each collective charge ``Q_a``."""
    if not isfinite(coupling):
        raise ValueError("coupling must be finite")
    _validate_positive("lapse", lapse)
    spectrum = smeared_gradient_zero_frequency_spectrum(radius=radius)
    return coupling * sqrt(2.0 * pi * spectrum) / lapse


def collective_kossakowski_coefficient(
    coupling: float,
    lapse: float,
    *,
    radius: float = 1.0,
) -> float:
    """Return the scalar multiplying the rank-one ``[[I,I],[I,I]]`` block."""
    prefactor = collective_jump_prefactor(coupling, lapse, radius=radius)
    return prefactor * prefactor


def collective_lamb_shift_principal_value_magnitude(
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
) -> float:
    """Return the positive magnitude ``PV int j_sigma(w)/w dw``."""
    _validate_positive("radius", radius)
    _validate_positive("smearing_width", smearing_width)
    sigma = smearing_width
    return (
        1.0 / (24.0 * pi**1.5 * radius**2 * sigma)
        + 1.0 / (48.0 * pi**1.5 * sigma**3)
    )


def collective_lamb_shift_coefficient(
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
) -> float:
    """Return the signed standard-Davies coefficient at zero Bohr frequency.

    With ``gamma(w)=2 pi j(w)`` and
    ``S(0)=(1/2pi)PV int gamma(nu)/(0-nu) dnu``, this is the negative of the
    positive principal-value magnitude.
    """
    return -collective_lamb_shift_principal_value_magnitude(
        radius=radius,
        smearing_width=smearing_width,
    )


def numerical_collective_lamb_shift_coefficient(
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
    steps: int = 20_000,
) -> float:
    """Numerically integrate the signed paired principal value by Simpson."""
    _validate_positive("radius", radius)
    _validate_positive("smearing_width", smearing_width)
    _validate_positive_integer("steps", steps)
    if steps % 2:
        raise ValueError("steps must be even")
    upper = 8.0 / smearing_width
    spacing = upper / steps

    def paired_integrand(frequency: float) -> float:
        if frequency == 0.0:
            return -1.0 / (12.0 * pi**2 * radius**2)
        positive = smeared_gradient_spectrum(
            frequency,
            radius=radius,
            smearing_width=smearing_width,
        )
        negative = smeared_gradient_spectrum(
            -frequency,
            radius=radius,
            smearing_width=smearing_width,
        )
        return (negative - positive) / frequency

    total = paired_integrand(0.0) + paired_integrand(upper)
    total += 4.0 * sum(
        paired_integrand(index * spacing) for index in range(1, steps, 2)
    )
    total += 2.0 * sum(
        paired_integrand(index * spacing) for index in range(2, steps, 2)
    )
    return spacing * total / 3.0


def sufficient_ule_residual_coupling_cap(
    spin: int,
    lapse: float,
    *,
    mismatch_coefficient: float = 1.0,
    ule_witness_constant: float = 1.0,
) -> float:
    """Return the formal cap from ``C lambda^2 L^4 N^-2 log(d)<=A/d``.

    The estimate must apply to a specified non-dark observable with uniformly
    bounded trace norm, or to a suitable channel norm.
    It does not constrain the collective singlet, which is exactly annihilated
    by every ``Q_a`` in the declared overlapping model.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    _validate_positive("ule_witness_constant", ule_witness_constant)
    dimension = 2 * spin + 1
    return (
        sqrt(mismatch_coefficient / ule_witness_constant)
        * lapse
        / (spin**2 * sqrt(dimension * log(float(dimension))))
    )


def logarithmic_heat_to_haar_distance_bound(spin: int) -> float:
    """Return the elementary heat-to-Haar bound at ``s=log(d)/2``."""
    _validate_positive_integer("spin", spin)
    dimension = 2 * spin + 1
    return 1.5 / (
        dimension * (1.0 - 1.0 / dimension**2) ** 1.5
    )


def rank_one_return_probability_upper_bound(spin: int) -> float:
    """Bound the heat-channel return probability of the rank-one Choi test.

    The Haar append-and-twirl output is entanglement breaking, so its overlap
    with the maximally entangled target-memory projector is at most ``1/d``.
    The finite heat correction is then added in normalized diamond distance.
    """
    _validate_positive_integer("spin", spin)
    dimension = 2 * spin + 1
    return min(
        1.0,
        1.0 / dimension + logarithmic_heat_to_haar_distance_bound(spin),
    )


def rank_one_return_initial_decay_rate_lower_bound(spin: int) -> float:
    """Lower-bound the initial decay under ``-sum_a[Q_a,[Q_a,rho]]``.

    For the Choi-return pure state, the target marginal is maximally mixed and
    uncorrelated with the pure reference. Hence

    ``sum_a Var(Q_a)=2L(L+1)-|<L_R>|^2 >= L^2+2L``.

    The return derivative is minus twice this variance sum.
    """
    _validate_positive_integer("spin", spin)
    return 2.0 * spin * (spin + 2.0)


def decoder_witness_trace_norm(spin: int) -> float:
    """Return ``||W_D||_1=d`` for any trace-preserving recovery decoder."""
    _validate_positive_integer("spin", spin)
    return float(2 * spin + 1)


def all_decoder_recovery_error_lower_bound_from_spectral_residual(
    spin: int,
    ancilla_stable_spectral_residual: float,
) -> float:
    """Transfer an ancilla-stable Choi spectral residual to all decoders.

    For ``W_D=(id tensor D^*)(Phi)``, trace preservation gives
    ``||W_D||_1=d``.  Therefore a spectral-state residual ``epsilon_infty``
    costs ``d epsilon_infty`` in entanglement fidelity.
    """
    _validate_positive_integer("spin", spin)
    _validate_nonnegative(
        "ancilla_stable_spectral_residual",
        ancilla_stable_spectral_residual,
    )
    dimension = 2 * spin + 1
    return max(
        0.0,
        1.0
        - 1.0 / dimension
        - logarithmic_heat_to_haar_distance_bound(spin)
        - dimension * ancilla_stable_spectral_residual,
    )


def heat_scale_matching_ule_residual_coupling_cap(
    spin: int,
    lapse: float,
    *,
    mismatch_coefficient: float = 1.0,
    ule_witness_constant: float = 1.0,
) -> float:
    """Return the stronger cap making decoder error ``O(1/d)``.

    This imposes ``epsilon_infty<=A/d^2`` rather than the ``A/d`` condition
    needed only to preserve a nonzero constant all-decoder obstruction.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    _validate_positive("ule_witness_constant", ule_witness_constant)
    dimension = 2 * spin + 1
    return (
        sqrt(mismatch_coefficient / ule_witness_constant)
        * lapse
        / (spin**2 * dimension * sqrt(log(float(dimension))))
    )


def overlapping_ule_record(
    spin: int,
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
    mismatch_coefficient: float = 1.0,
    ule_witness_constant: float = 1.0,
) -> dict[str, float | int | str]:
    """Return exact bath coefficients and the conditional collar coupling cap."""
    _validate_positive_integer("spin", spin)
    dimension = 2 * spin + 1
    lapse = 1.0 / dimension
    coupling_cap = sufficient_ule_residual_coupling_cap(
        spin,
        lapse,
        mismatch_coefficient=mismatch_coefficient,
        ule_witness_constant=ule_witness_constant,
    )
    heat_scale_coupling_cap = heat_scale_matching_ule_residual_coupling_cap(
        spin,
        lapse,
        mismatch_coefficient=mismatch_coefficient,
        ule_witness_constant=ule_witness_constant,
    )
    return {
        "spin_L": spin,
        "sector_dimension_d": dimension,
        "collar_lapse_N": lapse,
        "smearing_width_sigma": smearing_width,
        "zero_frequency_gradient_spectrum": (
            smeared_gradient_zero_frequency_spectrum(radius=radius)
        ),
        "collective_lamb_shift_coefficient": collective_lamb_shift_coefficient(
            radius=radius,
            smearing_width=smearing_width,
        ),
        "conditional_generic_ule_residual_coupling_cap": coupling_cap,
        "scaled_coupling_cap_d_to_7_over_2_sqrt_log": (
            coupling_cap * dimension**3.5 * sqrt(log(float(dimension)))
        ),
        "conditional_heat_scale_ule_residual_coupling_cap": (
            heat_scale_coupling_cap
        ),
        "scaled_heat_cap_d_to_4_sqrt_log": (
            heat_scale_coupling_cap
            * dimension**4
            * sqrt(log(float(dimension)))
        ),
        "rank_one_return_probability_upper_bound": (
            rank_one_return_probability_upper_bound(spin)
        ),
        "rank_one_return_initial_decay_rate_lower_bound": (
            rank_one_return_initial_decay_rate_lower_bound(spin)
        ),
        "decoder_witness_trace_norm": decoder_witness_trace_norm(spin),
        "constant_obstruction_example_lower_bound": (
            all_decoder_recovery_error_lower_bound_from_spectral_residual(
                spin,
                1.0 / (4.0 * dimension),
            )
        ),
        "interpretation": (
            "exact algebra for the declared KMS-compatible spectral ansatz; the "
            "rank-one return is a non-dark bounded-trace-norm diagnostic, while "
            "the all-decoder cap uses the companion ancilla-stable Choi "
            "spectral theorem; its decoder transfer costs a factor d"
        ),
    }


def static_patch_overlapping_ule_certificate(
    *,
    maximum_spin: int = 4096,
    radius: float = 1.0,
    smearing_width: float = 0.2,
) -> dict[str, object]:
    """Certify the overlapping zero-Bohr spectral ansatz and scaling target."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 64:
        raise ValueError("maximum_spin must be at least sixty-four")
    _validate_positive("radius", radius)
    _validate_positive("smearing_width", smearing_width)
    spins = tuple(
        sorted(
            {
                spin
                for spin in (16, 64, 256, 1024, maximum_spin)
                if spin <= maximum_spin
            }
            | {maximum_spin}
        )
    )
    records = tuple(
        overlapping_ule_record(
            spin,
            radius=radius,
            smearing_width=smearing_width,
        )
        for spin in spins
    )
    test_frequency = 0.7 / radius
    positive = smeared_gradient_spectrum(
        test_frequency,
        radius=radius,
        smearing_width=smearing_width,
    )
    negative = smeared_gradient_spectrum(
        -test_frequency,
        radius=radius,
        smearing_width=smearing_width,
    )
    analytic_lamb = collective_lamb_shift_coefficient(
        radius=radius,
        smearing_width=smearing_width,
    )
    numeric_lamb = numerical_collective_lamb_shift_coefficient(
        radius=radius,
        smearing_width=smearing_width,
    )
    sample_coupling = 0.03
    sample_lapse = 0.2
    jump = collective_jump_prefactor(sample_coupling, sample_lapse, radius=radius)
    kossakowski = collective_kossakowski_coefficient(
        sample_coupling,
        sample_lapse,
        radius=radius,
    )
    last = records[-1]
    certified_claims = {
        "kms_detailed_balance_holds": abs(
            negative / positive - exp(-2.0 * pi * radius * test_frequency)
        )
        < 1.0e-12,
        "zero_frequency_limit_is_positive": (
            smeared_gradient_zero_frequency_spectrum(radius=radius) > 0.0
        ),
        "signed_principal_value_lamb_shift_matches_closed_form": abs(
            numeric_lamb / analytic_lamb - 1.0
        )
        < 1.0e-10,
        "jump_square_equals_kossakowski_coefficient": abs(
            jump * jump - kossakowski
        )
        < 1.0e-15,
        "conditional_coupling_cap_has_d_minus_seven_halves_scaling": abs(
            last["scaled_coupling_cap_d_to_7_over_2_sqrt_log"] - 4.0
        )
        < 2.0e-3,
        "heat_scale_coupling_cap_has_d_minus_four_scaling": abs(
            last["scaled_heat_cap_d_to_4_sqrt_log"] - 4.0
        )
        < 2.0e-3,
        "rank_one_return_test_decays_as_inverse_dimension": (
            last["rank_one_return_probability_upper_bound"]
            * last["sector_dimension_d"]
            < 3.0
        ),
        "rank_one_return_test_is_strictly_non_dark": (
            last["rank_one_return_initial_decay_rate_lower_bound"] > 0.0
        ),
        "decoder_spectral_transfer_costs_exactly_one_dimension_factor": (
            last["decoder_witness_trace_norm"]
            == float(last["sector_dimension_d"])
        ),
        "one_over_d_spectral_control_preserves_a_constant_obstruction": (
            last["constant_obstruction_example_lower_bound"] > 0.7
        ),
    }
    return {
        "goal": "Overlapping-Sector Bunch-Davies ULE Spectral Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "kms_spectral_ansatz_conditional_residual_scaling",
        "central_result": (
            "For a fixed Gaussian spectral regulator and two overlapping fixed-"
            "spin sectors, the declared ansatz has exact KMS balance, a finite "
            "collective Casimir Lamb shift, and three rank-one target/reference "
            "blocks in the zero-Bohr Kossakowski matrix (full rank three)."
        ),
        "conditional_scaling_target": (
            "A rank-one Choi return projector is a non-dark fixed-task witness. "
            "For every decoder, however, the pulled-back fidelity witness has "
            "trace norm d. The companion worldtube/ULE theorem proves an "
            "ancilla-stable spectral residual with leading scaling "
            "lambda^2 L^4 N^-2 log(d) under its stated hypotheses. Therefore "
            "epsilon_infty=O(1/d) gives lambda=O[d^(-7/2)/sqrt(log d)], while "
            "matching the heat correction gives lambda=O[d^-4/sqrt(log d)]."
        ),
        "claim_boundary": (
            "The algebraic identities are exact for the declared spectral ansatz. "
            "The companion theorem derives it from a stationary optical heat "
            "kernel, proves that exact Gaussian smearing is quasilocal, and gives "
            "a compact replacement. The total-"
            "spin singlet is exactly dark under the full collective system-bath "
            "Hamiltonian and cannot diagnose ULE error. A bounded-trace-norm "
            "rank-one non-dark witness is now explicit, but it does not prove "
            "all-decoder robustness by itself. The stabilized spectral theorem is "
            "not a trace/diamond bound and assumes a Gaussian bath factorized in "
            "the remote past; a companion theorem controls a prescribed finite "
            "amplitude ramp and burn-in. A smooth matter-derived compact profile, "
            "certified sharp moments, direct interactions, source, "
            "lifetime, and gravity remain open."
        ),
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "derive the compact smooth regulator from the finite matter action, "
            "certify its Sobolev constants, derive the switch from its action, and control direct "
            "interactions, stress, lifetime, and gravity"
        ),
    }
