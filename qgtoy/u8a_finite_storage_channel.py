"""Conditional storage-channel box and locality stop for the U8a route.

The model is deliberately finite and explicit.  A Peter--Weyl register
``R_1=(V_0 tensor V_0*) direct_sum (V_1 tensor V_1*)`` is stored relative to
an inert spin-one target.  Its left angular charge couples to a conformal
pseudoscalar through the named smooth compact optical-worldtube profile from
``static_patch_smooth_worldtube_ule``.

The exact reduced map and the ULE comparison are both defined from the same
factorized pre-switch input.  No autonomous plateau map is inferred after the
system and bath have become correlated.  Uniformity under an inert ancilla
then permits a finite-dimensional operator-to-diamond conversion with its full
dimension cost exposed.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from math import exp, floor, isfinite, log, log1p, pi

from .finite_time_rotation_diffusion import finite_time_twirl_distance_record
from .global_so3_reference_risk import peter_weyl_token_risk_audit
from .static_patch_overlapping_ule import (
    smeared_gradient_zero_frequency_spectrum,
)
from .static_patch_smooth_worldtube_ule import (
    smooth_worldtube_analytic_sobolev_upper_bounds,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def normalized_diamond_bound_from_uniform_operator_residual(
    operator_residual: float,
    *,
    input_dimension: int,
    output_dimension: int,
) -> dict[str, object]:
    """Convert a uniform ancilla-stable operator residual to diamond norm.

    Let ``Delta`` be a Hermiticity-preserving, trace-annihilating difference of
    channels.  Diamond stabilization needs an ancilla of dimension
    ``input_dimension``.  For every density input, the output difference is a
    traceless Hermitian matrix of dimension
    ``input_dimension*output_dimension``.  Its positive and negative spectral
    sums agree, which proves

    ``0.5*||Delta||_diamond <= floor(Din*Dout/2)*epsilon_infinity``.

    The premise is stronger than a residual for one selected state.  Callers
    must separately prove that the same bound holds uniformly for all inputs
    entangled with an inert stabilizing ancilla.
    """
    _validate_nonnegative("operator_residual", operator_residual)
    _validate_positive_integer("input_dimension", input_dimension)
    _validate_positive_integer("output_dimension", output_dimension)
    stabilized_output_dimension = input_dimension * output_dimension
    conversion_factor = floor(stabilized_output_dimension / 2)
    raw_bound = conversion_factor * operator_residual
    return {
        "uniform_operator_residual": operator_residual,
        "input_dimension": input_dimension,
        "output_dimension": output_dimension,
        "stabilizing_ancilla_dimension": input_dimension,
        "stabilized_output_dimension": stabilized_output_dimension,
        "traceless_hermitian_conversion_factor": conversion_factor,
        "raw_normalized_diamond_bound": raw_bound,
        "normalized_diamond_bound": min(1.0, raw_bound),
        "formula": (
            "0.5||Delta||_diamond <= "
            "floor(D_in D_out/2) epsilon_infinity"
        ),
        "premise": (
            "uniform operator-norm residual for every system-plus-inert-ancilla "
            "density input from the common factorized pre-switch time"
        ),
    }


def u8a_finite_switch_channel_error_record(
    coupling: float,
    elapsed_time: float,
    burn_in: float,
    *,
    switch_effective_lead: float = 0.0,
    maximum_spin: int = 1,
    register_dimension: int = 10,
    lapse: float = 1.0,
    jump_l1_upper_bound: float,
    jump_first_moment_upper_bound: float,
) -> dict[str, object]:
    """Return the rigid-detector error ledger for the switched storage map."""
    _validate_positive("coupling", coupling)
    _validate_nonnegative("elapsed_time", elapsed_time)
    _validate_nonnegative("burn_in", burn_in)
    _validate_nonnegative("switch_effective_lead", switch_effective_lead)
    _validate_positive_integer("maximum_spin", maximum_spin)
    _validate_positive_integer("register_dimension", register_dimension)
    _validate_positive("lapse", lapse)
    _validate_positive("jump_l1_upper_bound", jump_l1_upper_bound)
    _validate_positive(
        "jump_first_moment_upper_bound", jump_first_moment_upper_bound
    )
    effective_age = burn_in + switch_effective_lead
    if effective_age <= 0.0:
        raise ValueError("burn_in + switch_effective_lead must be positive")

    c_value = 144.0 * coupling**2 * maximum_spin**2 / lapse**2
    gm = jump_l1_upper_bound * jump_first_moment_upper_bound
    stationary_initial = 2.0 * c_value * gm
    stationary_growth = (
        2.0
        * c_value**2
        * jump_l1_upper_bound**3
        * jump_first_moment_upper_bound
        * elapsed_time
    )
    finite_switch = c_value * gm * log1p(elapsed_time / effective_age)
    operator_total = stationary_initial + stationary_growth + finite_switch
    diamond = normalized_diamond_bound_from_uniform_operator_residual(
        operator_total,
        input_dimension=register_dimension,
        output_dimension=register_dimension,
    )
    factor = diamond["traceless_hermitian_conversion_factor"]
    normalized_components = {
        "stationary_initial": factor * stationary_initial,
        "stationary_growth": factor * stationary_growth,
        "finite_switch_history": factor * finite_switch,
        "multipole": 0.0,
        "band_leakage": 0.0,
        "free_evolution": 0.0,
        "lamb_shift": 0.0,
    }
    return {
        "coupling_lambda": coupling,
        "elapsed_time_T": elapsed_time,
        "burn_in_B": burn_in,
        "switch_effective_lead_T_chi": switch_effective_lead,
        "effective_preparation_age": effective_age,
        "maximum_left_spin": maximum_spin,
        "register_dimension": register_dimension,
        "lapse_N": lapse,
        "jump_l1_upper_bound": jump_l1_upper_bound,
        "jump_first_moment_upper_bound": jump_first_moment_upper_bound,
        "operator_residual_components": {
            "stationary_initial": stationary_initial,
            "stationary_growth": stationary_growth,
            "finite_switch_history": finite_switch,
        },
        "uniform_operator_residual_total": operator_total,
        "normalized_diamond_components": normalized_components,
        "normalized_diamond_total_before_clipping": sum(
            normalized_components.values()
        ),
        "normalized_diamond_bound": diamond["normalized_diamond_bound"],
        "diamond_conversion": diamond,
        "multipole_error_status": (
            "exactly zero: the action couples to the full smeared current and "
            "never replaces it by a center-value monopole"
        ),
        "band_leakage_status": (
            "exactly zero: the left generators preserve the hard j<=1 "
            "Peter-Weyl compression"
        ),
        "lamb_shift_status": (
            "exactly included with free Casimir evolution in the known "
            "covariant unitary; no Lamb-shift term is discarded"
        ),
    }


def u8a_operational_risk_record(
    *,
    heat_exposure: float,
    maximum_mean_casimir: float,
    physical_to_heat_diamond_bound: float,
    target_risk: float,
) -> dict[str, object]:
    """Compose the physical channel bound with heat-to-Haar and U7 risks."""
    _validate_nonnegative("heat_exposure", heat_exposure)
    _validate_nonnegative("maximum_mean_casimir", maximum_mean_casimir)
    _validate_nonnegative(
        "physical_to_heat_diamond_bound", physical_to_heat_diamond_bound
    )
    if physical_to_heat_diamond_bound > 1.0:
        raise ValueError("physical_to_heat_diamond_bound must not exceed one")
    if not isfinite(target_risk) or target_risk < 0.0 or target_risk > 1.0:
        raise ValueError("target_risk must lie in the closed unit interval")

    heat = finite_time_twirl_distance_record(
        heat_exposure,
        diffusion_rate=1.0,
    )
    heat_to_haar = heat["normalized_diamond_distance_to_haar_upper_bound"]
    attenuation = exp(-2.0 * heat_exposure)
    u7_effective_floor = (
        0.75 * (1.0 - attenuation)
        + attenuation / (16.0 * maximum_mean_casimir + 8.0)
    )
    haar_transfer_floor = max(0.0, 0.75 - heat_to_haar)
    effective_floor = max(u7_effective_floor, haar_transfer_floor)
    physical_floor = max(
        0.0,
        effective_floor - physical_to_heat_diamond_bound,
    )
    return {
        "heat_exposure_s": heat_exposure,
        "maximum_mean_casimir": maximum_mean_casimir,
        "heat_to_haar_normalized_diamond_bound": heat_to_haar,
        "u7_effective_heat_risk_floor": u7_effective_floor,
        "haar_transfer_effective_risk_floor": haar_transfer_floor,
        "best_effective_risk_floor": effective_floor,
        "physical_to_heat_normalized_diamond_bound": (
            physical_to_heat_diamond_bound
        ),
        "physical_operational_risk_floor": physical_floor,
        "target_risk": target_risk,
        "operational_margin_before_physical_error": (
            effective_floor - target_risk
        ),
        "target_is_excluded": physical_floor > target_risk,
    }


def u8a_named_action_record() -> dict[str, object]:
    """Return the binding WT-R1/D1 model and exact channel-domain contract."""
    token = peter_weyl_token_risk_audit(1)
    return {
        "model_name": "WT-R1/D1 smooth-worldtube storage model",
        "background": (
            "target realization: unit-radius de Sitter static patch, central "
            "static worldline, N=1, and the Bunch-Davies KMS state"
        ),
        "register": (
            "R_1=(V_0 tensor V_0*) direct_sum (V_1 tensor V_1*), "
            "dimension 10, with the unknown SO(3) action on the left factors"
        ),
        "target": (
            "an inert distinguishable spin-one relational anchor D=V_1; it is "
            "not counted in the storage-channel dimension because the compared "
            "maps act as identity_D"
        ),
        "prepared_token": (
            "|eta_1>=(|Phi_0>+3|Phi_1>)/sqrt(10), fixed before the "
            "unknown relative rotation is sampled"
        ),
        "canonical_token_exact_initial_risk": token[
            "canonical_token_exact_chordal_orientation_risk"
        ],
        "canonical_token_mean_casimir": token["mean_casimir"],
        "bath": (
            "conformally coupled pseudoscalar with improved axial gradient "
            "B_a=e_a^mu(nabla_mu phi+a_mu phi)"
        ),
        "spatial_profile": (
            "the C-infinity radial seed exp(1-1/(1-x^2)) on x<1, normalized "
            "by its zero-channel spherical transform and convolved with its "
            "reflection; optical support a=R/5"
        ),
        "switch": (
            "q(u)=0 for u<=0 and exp(-1/u) for u>0; "
            "S(u)=q(u)/(q(u)+q(1-u)); "
            "chi_(B,T)(tau)=S(tau)S(B+T+2-tau), giving unit-duration "
            "smooth ramps and a burn-in-plus-storage plateau"
        ),
        "interaction_action": (
            "H_int(tau)=lambda chi(tau) sum_a J_left^a tensor Phi_a(h_A), "
            "Phi_a(h_A)=integral_(H3_R) dmu_opt h_A(y) "
            "P_a^b(y->0) B_b(tau,y); "
            "the normalized optical profile and parallel transport are part "
            "of the binding extended-detector EFT"
        ),
        "free_action": (
            "H_R=C_left/(2I), H_D=h_D(J_D^2); hence "
            "[H_R,J_a^left]=0 and every coupled charge is zero Bohr"
        ),
        "conserved_resource": (
            "[C_left,J_a^left]=0, so the exact switched joint unitary, P_B, "
            "and the storage evolution preserve the register's mean left "
            "Casimir exactly"
        ),
        "physical_channel_target": (
            "F_{B,T}: pre-switch register input -> reduced register state after "
            "the smooth ramp, burn-in B, and storage time T, obtained by the "
            "switched joint dynamics and the KMS-state slice map"
        ),
        "comparison_channel": (
            "G_{B,T}=U_cov(T) o H_s(T) o P_B, where "
            "U_cov=U_free o U_LS includes both known Casimir unitaries and P_B "
            "is the exact reduced pre-switch-to-post-burn channel. Both F and "
            "G have the same input time; no autonomous map on arbitrary "
            "correlated plateau states is claimed"
        ),
        "channel_covariance": (
            "the radial optical profile, parallel transport, and contracted "
            "vector coupling are invariant under simultaneous register-bath "
            "SO(3) rotations, while the KMS bath state is rotation invariant. "
            "Therefore F_{B,T} and P_B are SO(3)-covariant; H_s is isotropic "
            "and U_free,U_LS are Casimir functions commuting with the encoding"
        ),
        "qft_channel_bridge": (
            "OPEN: construct the KMS GNS/Araki-Woods propagator for the "
            "unbounded smeared-field interaction, prove the Nathan-Rudner "
            "bounds uniformly for regulated dynamics, and pass the reduced-map "
            "inequality to the regulator-free limit"
        ),
        "locality_scope": (
            "a smooth compact spatially smeared rigid-detector EFT. Its bath "
            "coupling is worldtube supported, but the shared J_left operators "
            "are not a microcausal local matter current"
        ),
        "locality_obstruction": (
            "choose disjoint equal-time test functions f,g supported where "
            "h_A is nonzero, with alpha_f and alpha_g nonzero. For the exact "
            "density ell_a(x)=h_A(x)J_a^left, "
            "the commutator [ell_1(f),ell_2(g)]="
            "i alpha_f alpha_g J_3^left is nonzero on the V_1 block despite "
            "the spacelike-separated supports"
        ),
    }


def _decimal_fraction_bound(
    value: str,
    *,
    rounding: str,
    precision: int,
) -> Decimal:
    numerator, denominator = value.split("/", maxsplit=1)
    with localcontext() as context:
        context.prec = precision
        context.rounding = rounding
        return Decimal(numerator) / Decimal(denominator)


def _u8a_decimal_box_guard(
    box: dict[str, str],
    *,
    jump_l1_exact: str,
    jump_first_exact: str,
) -> dict[str, object]:
    """Audit the displayed decimal box with high-precision directed margins."""
    precision = 80
    lambda_lower = Decimal(box["lambda_lower"])
    lambda_upper = Decimal(box["lambda_upper"])
    burn_lower = Decimal(box["burn_lower"])
    burn_upper = Decimal(box["burn_upper"])
    time_lower = Decimal(box["time_lower"])
    time_upper = Decimal(box["time_upper"])
    jump_l1_lower = _decimal_fraction_bound(
        jump_l1_exact,
        rounding=ROUND_FLOOR,
        precision=precision,
    )
    jump_l1_upper = _decimal_fraction_bound(
        jump_l1_exact,
        rounding=ROUND_CEILING,
        precision=precision,
    )
    jump_first_upper = _decimal_fraction_bound(
        jump_first_exact,
        rounding=ROUND_CEILING,
        precision=precision,
    )

    # These rational pi bounds are far tighter than the declared exposure
    # slack and avoid treating a binary float for pi as exact.
    pi_lower = Decimal("3.14159")
    pi_upper = Decimal("3.14160")
    with localcontext() as lower_context:
        lower_context.prec = precision
        lower_context.rounding = ROUND_FLOOR
        minimum_exposure_lower = (
            lambda_lower**2 * time_lower / (Decimal(24) * pi_upper**2)
        )

    with localcontext() as upper_context:
        upper_context.prec = precision
        upper_context.rounding = ROUND_CEILING
        maximum_exposure_upper = (
            lambda_upper**2 * time_upper / (Decimal(24) * pi_lower**2)
        )
        c_value = Decimal(144) * lambda_upper**2
        log_upper = (Decimal(1) + time_upper / burn_lower).ln().next_plus(
            context=upper_context
        )
        operator_error = (
            Decimal(2) * c_value * jump_l1_upper * jump_first_upper
            + Decimal(2)
            * c_value**2
            * jump_l1_upper**3
            * jump_first_upper
            * time_upper
            + c_value
            * jump_l1_upper
            * jump_first_upper
            * log_upper
        )
        normalized_diamond = Decimal(50) * operator_error
        attenuation_upper = Decimal("-1.4").exp().next_plus(
            context=upper_context
        )
        initial_u7_floor = Decimal(5) / Decimal(184)
        risk_loss_upper = (
            Decimal(3) / Decimal(4) - initial_u7_floor
        ) * attenuation_upper

    with localcontext() as upper_context:
        upper_context.prec = precision
        upper_context.rounding = ROUND_CEILING
        required_burn_upper = (
            Decimal(10)
            / (Decimal(144) * lambda_lower**2 * jump_l1_lower**2)
        )

    declared_error = Decimal("0.039")
    declared_exposure_lower = Decimal("0.7")
    declared_exposure_upper = Decimal("1.0")
    with localcontext() as lower_context:
        lower_context.prec = precision
        lower_context.rounding = ROUND_FLOOR
        risk_at_declared_lower = (
            Decimal(3) / Decimal(4)
            - risk_loss_upper
            - declared_error
        )

    guards = {
        "coupling_interval_is_strict": (
            Decimal(0) < lambda_lower < lambda_upper
        ),
        "burn_interval_is_strict": Decimal(0) < burn_lower < burn_upper,
        "storage_interval_is_strict": Decimal(0) < time_lower < time_upper,
        "burn_exceeds_bound_level_requirement": (
            burn_lower > required_burn_upper
        ),
        "minimum_exposure_is_strictly_above_declared_lower": (
            minimum_exposure_lower > declared_exposure_lower
        ),
        "maximum_exposure_is_strictly_below_declared_upper": (
            maximum_exposure_upper < declared_exposure_upper
        ),
        "diamond_error_is_strictly_below_declared_bound": (
            normalized_diamond < declared_error
        ),
        "u7_risk_is_strictly_above_target_at_declared_lower": (
            risk_at_declared_lower > Decimal("0.5")
        ),
    }
    return {
        "precision_decimal_digits": precision,
        "rounding_policy": (
            "ROUND_FLOOR for lower bounds; ROUND_CEILING for upper bounds; "
            "correctly rounded ln/exp expanded by one Decimal ulp"
        ),
        "pi_rational_guard": "3.14159 < pi < 3.14160",
        "minimum_exposure_lower_bound": str(minimum_exposure_lower),
        "maximum_exposure_upper_bound": str(maximum_exposure_upper),
        "normalized_diamond_upper_bound": str(normalized_diamond),
        "required_burn_upper_bound": str(required_burn_upper),
        "u7_physical_risk_floor_at_s_0p7_eta_0p039": str(
            risk_at_declared_lower
        ),
        "guards": guards,
        "all_guards_pass": all(guards.values()),
    }


def u8a_finite_storage_channel_certificate() -> dict[str, object]:
    """Audit the conditional detector box and certify the locality route stop."""
    radius = Fraction(1, 1)
    support_radius = Fraction(1, 5)
    maximum_spin = 1
    register_dimension = 10
    lapse = 1.0
    beta = 10.0
    target_risk = 0.5
    declared_channel_error_bound = 0.039
    minimum_exposure = 0.7
    maximum_exposure = 1.0
    switch_duration = 1.0

    enclosure = smooth_worldtube_analytic_sobolev_upper_bounds(
        radius=radius,
        support_radius=support_radius,
    )
    jump_l1 = enclosure["jump_l1_sobolev_upper_bound"]
    jump_first = enclosure["jump_first_moment_sobolev_upper_bound"]
    zero_spectrum = smeared_gradient_zero_frequency_spectrum(radius=radius)

    conversion_factor = floor(register_dimension**2 / 2)
    decimal_box = {
        "lambda_lower": "1.278e-14",
        "lambda_upper": "1.460e-14",
        "burn_lower": "1.497e18",
        "burn_upper": "1.645e18",
        "time_lower": "1.031e30",
        "time_upper": "1.100e30",
    }
    lambda_lower = float(decimal_box["lambda_lower"])
    lambda_upper = float(decimal_box["lambda_upper"])
    burn_lower = float(decimal_box["burn_lower"])
    burn_upper = float(decimal_box["burn_upper"])
    time_lower = float(decimal_box["time_lower"])
    time_upper = float(decimal_box["time_upper"])
    decimal_guard = _u8a_decimal_box_guard(
        decimal_box,
        jump_l1_exact=enclosure["jump_l1_sobolev_upper_bound_exact"],
        jump_first_exact=enclosure[
            "jump_first_moment_sobolev_upper_bound_exact"
        ],
    )
    minimum_protocol_duration = (
        2.0 * switch_duration + burn_lower + time_lower
    )
    maximum_protocol_duration = (
        2.0 * switch_duration + burn_upper + time_upper
    )

    worst_error = u8a_finite_switch_channel_error_record(
        lambda_upper,
        time_upper,
        burn_lower,
        maximum_spin=maximum_spin,
        register_dimension=register_dimension,
        lapse=lapse,
        jump_l1_upper_bound=jump_l1,
        jump_first_moment_upper_bound=jump_first,
    )
    minimum_actual_exposure = (
        pi * lambda_lower**2 * zero_spectrum * time_lower / lapse**2
    )
    maximum_actual_exposure = (
        pi * lambda_upper**2 * zero_spectrum * time_upper / lapse**2
    )
    required_bound_level_burn = (
        beta
        * lapse**2
        / (144.0 * maximum_spin**2 * lambda_lower**2 * jump_l1**2)
    )
    risk = u8a_operational_risk_record(
        heat_exposure=minimum_actual_exposure,
        maximum_mean_casimir=1.8,
        physical_to_heat_diamond_bound=worst_error[
            "normalized_diamond_bound"
        ],
        target_risk=target_risk,
    )
    token = peter_weyl_token_risk_audit(1)
    u7_initial_floor = 1.0 / (16.0 * 1.8 + 8.0)
    declared_failure_exposure_threshold = 0.5 * log(
        (0.75 - u7_initial_floor)
        / (0.75 - target_risk - declared_channel_error_bound)
    )

    checks = {
        "register_is_fixed_finite_global_so3_token": (
            token["peter_weyl_dimension_D_J"] == register_dimension
            and token["canonical_token_exact_chordal_orientation_risk"]
            < target_risk
        ),
        "exact_profile_moments_are_analytically_enclosed": bool(
            enclosure["exact_integral_profile_enclosed"]
            and enclosure["finite_simpson_transform_extrapolated_to_infinity"]
            is False
        ),
        "displayed_decimal_box_has_directed_strict_guards": decimal_guard[
            "all_guards_pass"
        ],
        "channel_conversion_has_full_dimension_cost": conversion_factor == 50,
        "coupling_interval_has_positive_width_and_excludes_zero": (
            0.0 < lambda_lower < lambda_upper
        ),
        "preparation_and_storage_intervals_have_positive_width": (
            0.0 < burn_lower < burn_upper
            and 0.0 < time_lower < time_upper
        ),
        "burn_exceeds_bound_level_requirement_throughout_box": (
            burn_lower > required_bound_level_burn
        ),
        "finite_protocol_duration_interval_contains_every_box_point": (
            0.0 < minimum_protocol_duration < maximum_protocol_duration
        ),
        "heat_exposure_box_is_strictly_inside_declared_envelope": (
            minimum_actual_exposure > minimum_exposure
            and maximum_actual_exposure < maximum_exposure
        ),
        "all_channel_errors_fit_strictly_below_declared_bound": (
            worst_error["normalized_diamond_bound"]
            < declared_channel_error_bound
        ),
        "multipole_band_and_known_unitaries_are_accounted_for": (
            worst_error["normalized_diamond_components"]["multipole"] == 0.0
            and worst_error["normalized_diamond_components"]["band_leakage"]
            == 0.0
            and worst_error["normalized_diamond_components"]["lamb_shift"]
            == 0.0
        ),
        "operational_error_is_below_the_risk_margin": (
            worst_error["normalized_diamond_bound"]
            < risk["operational_margin_before_physical_error"]
        ),
        "target_record_quality_is_excluded_after_finite_storage": risk[
            "target_is_excluded"
        ],
        "box_begins_above_the_declared_failure_threshold": (
            minimum_actual_exposure > declared_failure_exposure_threshold
        ),
    }
    return {
        "goal": "Close Or Kill Paper U Gate U8a",
        "status": "conditional_pass" if all(checks.values()) else "fail",
        "result_type": (
            "conditional_detector_record_failure_box_with_locality_obstruction"
        ),
        "u8a_disposition": (
            "CONDITIONAL WT-R1/D1 DEGRADATION BOX; EXACT FACTORIZED-CURRENT "
            "LOCALITY ROUTE STOPPED"
        ),
        "detector_channel_status": (
            "CONDITIONAL on a regulator-uniform KMS GNS/Pauli-Fierz bridge"
        ),
        "paper_u_u8a_status": "OPEN",
        "route_terminal_status": (
            "INCONCLUSIVE STOP: the exact factorized rigid-current density "
            "cannot be promoted unchanged to a microcausal local-matter action "
            "while retaining its exact-zero error ledger"
        ),
        "central_result": (
            "Within the Nathan-Rudner regular Gaussian-bath framework, the "
            "fixed J<=1 detector has a finite-switch normalized-diamond bound "
            "below 0.039 on a positive-width nonzero-coupling box, and U7 gives "
            "orientation risk above 1/2. Applying that box to the named "
            "Bunch-Davies field remains conditional on the open QFT channel "
            "bridge. Independently, the exact factorized-current route fails "
            "microcausality under disjoint spacelike smearings."
        ),
        "named_action": u8a_named_action_record(),
        "analytic_profile_enclosure": enclosure,
        "decimal_box_guard": decimal_guard,
        "zero_frequency_spectrum": zero_spectrum,
        "parameter_box": {
            "coupling_lambda_open_interval": (lambda_lower, lambda_upper),
            "burn_in_B_open_interval": (burn_lower, burn_upper),
            "storage_time_T_open_interval": (time_lower, time_upper),
            "total_protocol_duration_open_bounds": (
                minimum_protocol_duration,
                maximum_protocol_duration,
            ),
            "smooth_switch_duration_each_end": switch_duration,
            "heat_exposure_range": (
                minimum_actual_exposure,
                maximum_actual_exposure,
            ),
            "declared_heat_exposure_open_envelope": (
                minimum_exposure,
                maximum_exposure,
            ),
            "all_times_in_units_of_de_sitter_radius": True,
            "declared_channel_error_bound": declared_channel_error_bound,
            "declared_failure_exposure_threshold": (
                declared_failure_exposure_threshold
            ),
            "required_bound_level_burn_at_lower_coupling": (
                required_bound_level_burn
            ),
        },
        "worst_corner_channel_error": worst_error,
        "minimum_exposure_risk_composition": risk,
        "verified_conditional_box_checks": checks,
        "open_bridge_checks": {
            "kms_gns_joint_propagator_constructed": False,
            "regulator_uniform_nathan_rudner_bounds_proved": False,
            "reduced_channel_norm_bound_passed_to_qft_limit": False,
        },
        "box_disposition": (
            "Assuming the open QFT channel bridge, WT-R1/D1 cannot retain risk "
            "<=1/2 on the displayed finite-time degradation box. The "
            "unconditional result is the exact factorized-current locality "
            "obstruction, not retention failure for the named QFT detector."
        ),
        "claim_boundary": (
            "The finite-switch estimate is proved for the regular "
            "Gaussian-bath hypotheses but its application to the named "
            "Bunch-Davies quasifree field is conditional on a regulator-uniform "
            "GNS/Pauli-Fierz bridge. The exact factorized density does not supply "
            "the microcausal local-matter action required by full U8a. Preparation "
            "of the token and a physical final readout are "
            "granted boundary operations, so U8b remains open. Persistence of "
            "the detector EFT through the finite protocol is an assumption, "
            "not an independently derived hardware-lifetime theorem. The very "
            "large conservative times reflect analytic Sobolev enclosures and "
            "make this a formal degradation theorem, not a practical detector "
            "proposal. "
            "No gravitational functional, S_Ob comparison, Paper R input, or "
            "full U8 claim is used."
        ),
    }
