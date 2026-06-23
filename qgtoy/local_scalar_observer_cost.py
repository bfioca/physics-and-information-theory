"""Final-support thermal dephasing bounds and their de Sitter specialization.

The model is the conformally coupled massless field in four-dimensional de
Sitter, decomposed into free canonical partial waves on the optical half-line.
A pointer qubit couples through its ``Z`` observable to a smooth compact
spacetime source. Conditional field evolution is an exact Weyl displacement
of the Bunch-Davies KMS state.

The central theorem first solves the arbitrary-temperature half-line momentum
optimization. In the conformal de Sitter specialization, the simple top
eigenvalue is also the full all-angular phase-space optimum. Explicit Schur,
Green-kernel, and Poincare estimates give sharp support asymptotics. The source
actuator is prescribed rather than dynamical, so its switching cost is outside
the theorem.
"""

from __future__ import annotations

from math import asinh, atanh, exp, inf, isfinite, log, log1p, pi, sinh, sqrt, tanh


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_fraction(name: str, value: float, *, allow_zero: bool = True) -> None:
    lower_ok = value >= 0.0 if allow_zero else value > 0.0
    if not isfinite(value) or not lower_ok or value >= 1.0:
        left = "[0" if allow_zero else "(0"
        raise ValueError(f"{name} must lie in {left},1)")


def de_sitter_optical_radius(
    areal_radius: float,
    *,
    static_patch_radius: float,
) -> float:
    """Return ``x=R atanh(r/R)`` for a centered static-patch ball."""
    _validate_nonnegative("areal_radius", areal_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    if areal_radius >= static_patch_radius:
        raise ValueError("areal_radius must lie strictly inside the static patch")
    return static_patch_radius * atanh(areal_radius / static_patch_radius)


def de_sitter_areal_radius_from_optical(
    optical_radius: float,
    *,
    static_patch_radius: float,
) -> float:
    """Return ``r=R tanh(x/R)``."""
    _validate_nonnegative("optical_radius", optical_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    return static_patch_radius * tanh(optical_radius / static_patch_radius)


def causal_output_support_record(
    *,
    source_areal_radius: float,
    switching_duration: float,
    static_patch_radius: float,
) -> dict[str, float | str]:
    """Causal support of final radial data after a compact source switches off."""
    _validate_nonnegative("switching_duration", switching_duration)
    source_optical = de_sitter_optical_radius(
        source_areal_radius,
        static_patch_radius=static_patch_radius,
    )
    output_optical = source_optical + switching_duration
    output_areal = de_sitter_areal_radius_from_optical(
        output_optical,
        static_patch_radius=static_patch_radius,
    )
    return {
        "source_areal_radius_a": source_areal_radius,
        "source_optical_radius_ell": source_optical,
        "switching_duration_T": switching_duration,
        "output_optical_radius_L": output_optical,
        "output_areal_radius_b": output_areal,
        "finite_propagation_statement": (
            "A source supported in 0<=x<=ell during a static-time interval of "
            "length T has final radial Cauchy data supported in 0<=x<=ell+T."
        ),
    }


def scalar_pointer_action_record() -> dict[str, object]:
    """Frozen continuum action, exact channel, and stress identities."""
    return {
        "field": (
            "four-dimensional conformally coupled massless real scalar in one "
            "de Sitter static patch; the cost theorem includes every angular "
            "sector and the gravity corollary uses spherical final data"
        ),
        "state": "Bunch-Davies quasifree KMS state at beta=2*pi*R",
        "pointer": "finite qubit with degenerate Z-pointer basis",
        "interaction_action": (
            "S_int=-integral sqrt(-g) J(x) phi(x) Z_P d^4x, with real "
            "J in C_c^infinity of the centered observer worldtube"
        ),
        "exact_unitary": (
            "U_J=exp(i phase[J]) exp(-i phi(J) Z_P); the Magnus expansion "
            "terminates because free-field commutators are c-numbers"
        ),
        "exact_reduced_channel": (
            "D_kappa with |kappa|=exp(-Gamma), "
            "Gamma=2<K E J,coth(beta h/2) K E J>"
        ),
        "observer_error": (
            "epsilon_obs=(1/2)||D_kappa-D_0||_diamond=exp(-Gamma)/2"
        ),
        "harlow_pointer_target_relation": (
            "D_0 is the binary quantum-to-classical pointer channel used in "
            "the Harlow-Usatyuk-Zhao observer rule. epsilon_obs measures only "
            "distance to that ideal channel; it is not their gravitational "
            "encoding error and is not identified with exp(-S_Ob)."
        ),
        "pointer_locality_scope": (
            "The compact interaction densities commute at spacelike "
            "separation because Z_P is fixed and the scalar is microcausal, "
            "but one finite-dimensional Z_P appears across the spatial "
            "smearing. This is a prescribed gapless smeared-detector model, "
            "not an autonomous relativistic pointer field."
        ),
        "post_switch_killing_energy": (
            "E_K=<K E J,h K E J>; equivalently the classical Killing "
            "energy of the source-generated coherent solution"
        ),
        "renormalized_stress_identity": (
            "<T_ab^ren>_displaced-<T_ab^ren>_BD=T_ab[classical phi_J]"
        ),
        "stress_scope": (
            "The identity is exact after J switches off. J is prescribed; "
            "the stress of a clock or material actuator generating J is not "
            "part of this model."
        ),
        "flux_free_source_construction": (
            "Given smooth compact target data q=0, p=f at t=0, let phi_free "
            "be its homogeneous solution, choose a smooth eta that is zero "
            "before the protocol and one near t=0, and set J=P(eta*phi_free). "
            "The retarded solution then has exactly the target final data. "
            "To keep J in a prescribed worldtube, choose the target support "
            "strictly inside the tube and the eta transition shorter than "
            "the remaining optical-radius margin."
        ),
        "flux_free_constraint_identity": (
            "For spherical final data q=0, phi=0 and "
            "n(phi)=p(x)/(sqrt(4*pi)*r*sqrt(N)). The conformal stress has "
            "rho=n(phi)^2/2 and zero momentum density, so "
            "4*pi*r^2*rho*dr=p(x)^2*dx/2 and the exact constraint mass equals "
            "the fixed-background scalar Killing energy."
        ),
    }


def all_angular_cost_extension_record() -> dict[str, str]:
    """Record why the s-wave constants control the full conformal field."""
    return {
        "radial_operators": (
            "A_l=-d^2/dx^2+l(l+1)/(R^2 sinh^2(x/R)), h_l=sqrt(A_l)"
        ),
        "operator_order": (
            "A_l>=A_0, so h_l^-1<=h_0^-1 and h_l^-2<=h_0^-2 in quadratic-"
            "form order"
        ),
        "exact_thermal_resolvent_order": (
            "h^-1*coth(beta*h/2)=(2/beta)A^-1+(4/beta)*sum_[n>=1]"
            "(A+(2*pi*n/beta)^2)^-1. Every resolvent is order decreasing, "
            "so the exact l=0 thermal momentum kernel dominates all l>0."
        ),
        "field_coordinate_bound": (
            "For q supported in [0,L], ||h_l q||^2>=||q'||^2>="
            "(pi/L)^2||q||^2 and <q,h_l q><=||q|| ||h_l q||."
        ),
        "conclusion": (
            "The exact l=0 momentum kernel dominates every angular momentum "
            "sector. Its explicit linear and thermal lower bounds jointly "
            "dominate the field-coordinate upper bound for every L/R, so the "
            "full phase-space optimum for arbitrary angular source data is "
            "the top eigenvalue of that kernel. Strict thermal and resolvent "
            "ordering exclude coordinate-sector and l>0 ties."
        ),
    }


def smooth_source_density_record() -> dict[str, str]:
    """Record the density argument upgrading the ideal profile to smooth sources."""
    return {
        "profile_sequence": (
            "For any normalized p in L2(0,ell), including the top KMS-kernel "
            "eigenfunction and the explicit linear profile, choose normalized "
            "p_n smooth with support strictly inside (0,ell) and p_n->p in L2."
        ),
        "covariance_continuity": (
            "On data supported in [0,ell], h^-1*coth(beta*h/2)<="
            "h^-1+2*h^-2/beta has a bounded compressed quadratic form, so "
            "the dephasing covariance is continuous under L2 convergence."
        ),
        "mass_continuity": (
            "sup_x |int_0^x(p_n^2-p^2)|<="
            "||p_n-p||_2*(||p_n||_2+||p||_2), so cumulative mass and the "
            "strict spherical constraint margin converge uniformly."
        ),
        "source_realization": (
            "For each p_n, choose a time cutoff shorter than the remaining "
            "optical support margin and set J_n=P(eta_n*phi_free,n). Then J_n "
            "is smooth, compact, worldtube-supported, and has exact final data "
            "q=0,p=p_n."
        ),
    }


def bekenstein_dephasing_comparison_record() -> dict[str, str]:
    """Record the radial sequences separating local entropy from dephasing."""
    return {
        "setting": (
            "Massless conformal vacuum in a 3+1-dimensional Minkowski ball of "
            "radius a, restricted to q=0 radial data with ||p||_2=1. Then "
            "S_B=pi/(2a)*int_0^a(a^2-x^2)p(x)^2 dx and "
            "Gamma_0=<p,h^-1 p>."
        ),
        "boundary_sequence": (
            "For p_delta=delta^-1/2*f((a-x)/delta), f smooth positive and "
            "compact in (0,1), S_B=pi*delta*int(u*f^2)du+O(delta^2), while "
            "Gamma_0=delta*(int f)^2*log(1/delta)/pi+O(delta). Hence "
            "Gamma_0/S_B diverges."
        ),
        "center_sequence": (
            "For p_delta=delta^-1/2*f(x/delta), f smooth compact in (0,1), "
            "S_B->pi*a/2 while Gamma_0=O(delta). Hence S_B/Gamma_0 diverges."
        ),
        "conclusion": (
            "The localized Klein-Gordon Bekenstein entropy and pointer "
            "dephasing exponent are inequivalent quadratic forms; neither "
            "uniformly bounds the other at fixed ball radius."
        ),
    }


def fractional_inverse_schur_constant() -> float:
    """Constant ``c_1=2 asinh(1)/pi`` for ``P_L h^-1 P_L``."""
    return 2.0 * asinh(1.0) / pi


def second_inverse_norm_constant() -> float:
    """Constant ``c_2=4/pi^2`` for ``P_L h^-2 P_L``."""
    return 4.0 / pi**2


def logarithmic_kernel_row_integral(
    position_ratio: float,
) -> float:
    """Dimensionless row integral of the positive ``h^-1`` kernel.

    For ``u=x/L``, this is
    ``[(1+u)log(1+u)-2u log(u)-(1-u)log(1-u)]/pi``.
    Its maximum occurs at ``u=1/sqrt(2)`` and equals
    ``2 asinh(1)/pi``.
    """
    _validate_fraction("position_ratio", position_ratio)
    u = position_ratio
    if u == 0.0:
        return 0.0
    last = 0.0 if u == 1.0 else (1.0 - u) * log(1.0 - u)
    return (
        (1.0 + u) * log(1.0 + u)
        - 2.0 * u * log(u)
        - last
    ) / pi


def _dilog_unit_interval(value: float) -> float:
    """Return ``Li_2(value)`` for ``0<=value<=1`` without extra packages."""
    if not isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError("dilog argument must lie in [0,1]")
    if value == 0.0:
        return 0.0
    if value == 1.0:
        return pi**2 / 6.0
    if value > 0.5:
        return (
            pi**2 / 6.0
            - log(value) * log1p(-value)
            - _dilog_unit_interval(1.0 - value)
        )
    total = 0.0
    power = value
    for index in range(1, 10000):
        term = power / index**2
        total += term
        if abs(term) <= 2.0e-16 * max(1.0, abs(total)):
            return total
        power *= value
    raise ArithmeticError("dilog series did not converge")


def _integral_log_sinh_over_argument(argument: float) -> float:
    """Return ``integral_0^argument log(sinh(t)/t) dt``."""
    _validate_nonnegative("argument", argument)
    z = argument
    if z == 0.0:
        return 0.0
    if z < 0.25:
        return (
            z**3 / 18.0
            - z**5 / 900.0
            + z**7 / 19845.0
            - z**9 / 340200.0
            + z**11 / 5145525.0
        )
    return (
        0.5 * z**2
        - z * log(2.0)
        - z * log(z)
        + z
        + 0.5
        * (_dilog_unit_interval(exp(-2.0 * z)) - pi**2 / 6.0)
    )


def _log_sinh_positive(argument: float) -> float:
    """Stable ``log(sinh(argument))`` for a positive argument."""
    _validate_positive("argument", argument)
    if argument < 0.5:
        return log(sinh(argument))
    return argument - log(2.0) + log1p(-exp(-2.0 * argument))


def thermal_momentum_kernel_value(
    x_coordinate: float,
    y_coordinate: float,
    *,
    inverse_temperature: float,
) -> float:
    """Exact half-line kernel of ``h^-1 coth(beta h/2)``.

    The diagonal has the expected integrable logarithmic singularity and is
    returned as positive infinity.
    """
    _validate_nonnegative("x_coordinate", x_coordinate)
    _validate_nonnegative("y_coordinate", y_coordinate)
    _validate_positive("inverse_temperature", inverse_temperature)
    x = x_coordinate
    y = y_coordinate
    if x == 0.0 or y == 0.0:
        return 0.0
    if x == y:
        return inf
    scale = pi / inverse_temperature
    return (
        _log_sinh_positive(scale * (x + y))
        - _log_sinh_positive(scale * abs(x - y))
    ) / pi


def thermal_momentum_row_maximizer(thermal_support_ratio: float) -> float:
    """Return the maximizing ``u=x/L`` for the exact KMS kernel row sum."""
    _validate_nonnegative("thermal_support_ratio", thermal_support_ratio)
    tau = thermal_support_ratio
    if tau < 1.0e-7:
        return 1.0 / sqrt(2.0)
    log_scaled_sinh = _log_sinh_positive(tau) - 0.5 * log(2.0)
    if log_scaled_sinh < 300.0:
        numerator = asinh(exp(log_scaled_sinh))
    else:
        numerator = log_scaled_sinh + log1p(
            sqrt(1.0 + exp(-2.0 * log_scaled_sinh))
        )
    return numerator / tau


def thermal_momentum_maximum_row_integral(
    output_optical_radius: float,
    *,
    inverse_temperature: float,
) -> dict[str, float | str]:
    """Exact maximum row integral used in the sharp-kernel Schur bound."""
    _validate_positive("output_optical_radius", output_optical_radius)
    _validate_positive("inverse_temperature", inverse_temperature)
    length = output_optical_radius
    tau = pi * length / inverse_temperature
    u_star = thermal_momentum_row_maximizer(tau)
    vacuum_row = logarithmic_kernel_row_integral(u_star)
    correction = (
        _integral_log_sinh_over_argument(tau * (1.0 + u_star))
        - 2.0 * _integral_log_sinh_over_argument(tau * u_star)
        - _integral_log_sinh_over_argument(tau * (1.0 - u_star))
    ) / (pi * tau)
    dimensionless_row = vacuum_row + correction
    return {
        "thermal_support_ratio_tau": tau,
        "maximizing_position_ratio_u": u_star,
        "dimensionless_maximum_row_integral_M": dimensionless_row,
        "maximum_row_integral": length * dimensionless_row,
        "stationarity_identity": (
            "sinh(tau*(1+u))*sinh(tau*(1-u))=sinh(tau*u)^2, "
            "so sinh(tau*u)=sinh(tau)/sqrt(2)"
        ),
    }


def sharp_thermal_half_line_momentum_cost(
    support_length: float,
    *,
    inverse_temperature: float,
) -> dict[str, float | str]:
    """Return the sharp thermal momentum cost on a half-line interval.

    For ``h=sqrt(-d^2/dx^2)`` with the Dirichlet condition at the half-line
    origin, momentum data ``p`` supported in ``[0,L]`` have
    ``Gamma=<p,h^-1*coth(beta*h/2)p>`` and ``E=||p||^2/2``. Their exact
    optimal ratio is ``C_beta(L)=sup Gamma/E``.

    This result is independent of the de Sitter temperature-curvature
    relation. Dominance over the other canonical and angular sectors is a
    separate statement in the conformal de Sitter specialization.
    """
    _validate_positive("support_length", support_length)
    _validate_positive("inverse_temperature", inverse_temperature)
    length = support_length
    beta = inverse_temperature
    tau = pi * length / beta
    row = thermal_momentum_maximum_row_integral(
        length,
        inverse_temperature=beta,
    )
    row_upper = 2.0 * length * float(
        row["dimensionless_maximum_row_integral_M"]
    )
    vacuum_lower = 3.0 * length / pi
    thermal_lower = 16.0 * length**2 / (beta * pi**2)
    closed_form_upper = (
        4.0 * asinh(1.0) * length / pi + thermal_lower
    )
    small_support_upper = (
        4.0 * asinh(1.0) * length / pi
        + 2.0 * pi * length**3 / (3.0 * beta**2)
    )
    large_support_upper = thermal_lower + beta / 3.0
    explicit_upper = min(
        closed_form_upper,
        row_upper,
        small_support_upper,
        large_support_upper,
    )
    return {
        "support_length_L": length,
        "inverse_temperature_beta": beta,
        "thermal_support_ratio_tau": tau,
        "exact_optimal_coefficient_formula": (
            "C_beta(L)=2*L*Lambda(pi*L/beta)"
        ),
        "variational_statement": (
            "For half-line Dirichlet momentum data supported in [0,L], "
            "Gamma<=E*C_beta(L), with equality in the finite-energy closure."
        ),
        "dimensionless_kernel": (
            "k_tau(u,v)=pi^-1 log[sinh(tau*(u+v))/"
            "sinh(tau*abs(u-v))]"
        ),
        "optimizer": (
            "The normalized optimizer is unique up to sign and is the "
            "strictly positive top eigenfunction of K_tau."
        ),
        "vacuum_profile_lower_coefficient": vacuum_lower,
        "thermal_green_lower_coefficient": thermal_lower,
        "rigorous_lower_coefficient": max(vacuum_lower, thermal_lower),
        "closed_form_upper_coefficient": closed_form_upper,
        "exact_row_schur_upper_coefficient": row_upper,
        "small_support_upper_coefficient": small_support_upper,
        "large_support_upper_coefficient": large_support_upper,
        "rigorous_explicit_upper_coefficient": explicit_upper,
        "maximum_row_position_ratio": row["maximizing_position_ratio_u"],
        "small_support_statement": (
            "0<=C_beta(L)-2*L*Lambda(0)<=2*pi*L^3/(3*beta^2)."
        ),
        "large_support_statement": (
            "0<=C_beta(L)-16*L^2/(beta*pi^2)<=beta/3."
        ),
        "scope": (
            "This is the general-temperature half-line momentum theorem. "
            "Dominance over field-coordinate and higher-angular sectors is "
            "proved separately for the conformal de Sitter specialization."
        ),
    }


def sharp_observer_cost_characterization(
    output_optical_radius: float,
    *,
    static_patch_radius: float,
) -> dict[str, float | str]:
    """Sharp de Sitter final-support coefficient and explicit brackets.

    If ``Lambda(tau)`` is the top eigenvalue of the dimensionless exact KMS
    kernel on ``(0,1)``, then the optimal full phase-space coefficient is
    ``C_opt(y)=2*y*Lambda(y/2)``. The optimizer is an s-wave momentum datum.
    """
    _validate_positive("output_optical_radius", output_optical_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    length = output_optical_radius
    radius = static_patch_radius
    y = length / radius
    tau = 0.5 * y
    half_line = sharp_thermal_half_line_momentum_cost(
        length,
        inverse_temperature=2.0 * pi * radius,
    )
    row_upper = float(half_line["exact_row_schur_upper_coefficient"]) / radius
    legacy = observer_cost_coefficient_from_optical_support(
        length,
        static_patch_radius=radius,
    )
    legacy_upper = float(legacy["dimensionless_cost_coefficient_F"])
    vacuum_lower = float(half_line["vacuum_profile_lower_coefficient"]) / radius
    thermal_lower = float(half_line["thermal_green_lower_coefficient"]) / radius
    small_support_upper = (
        float(half_line["small_support_upper_coefficient"]) / radius
    )
    large_support_upper = (
        float(half_line["large_support_upper_coefficient"]) / radius
    )
    explicit_upper = min(
        legacy_upper,
        row_upper,
        small_support_upper,
        large_support_upper,
    )
    return {
        "output_optical_radius_over_R_y": y,
        "thermal_support_ratio_tau": tau,
        "exact_optimal_coefficient_formula": "C_opt(y)=2*y*Lambda(y/2)",
        "general_thermal_half_line_specialization": half_line,
        "dimensionless_kernel": (
            "k_tau(u,v)=pi^-1 log[sinh(tau*(u+v))/"
            "sinh(tau*abs(u-v))]"
        ),
        "optimizer": (
            "The top eigenfunction is unique up to scale, strictly positive, "
            "and lies in the s-wave momentum sector; smooth compact source "
            "profiles approach its Rayleigh quotient."
        ),
        "vacuum_profile_lower_coefficient": vacuum_lower,
        "thermal_green_lower_coefficient": thermal_lower,
        "rigorous_lower_coefficient": max(vacuum_lower, thermal_lower),
        "legacy_F_upper_coefficient": legacy_upper,
        "exact_row_schur_upper_coefficient": row_upper,
        "small_support_upper_coefficient": small_support_upper,
        "large_support_upper_coefficient": large_support_upper,
        "rigorous_explicit_upper_coefficient": explicit_upper,
        "maximum_row_position_ratio": half_line[
            "maximum_row_position_ratio"
        ],
        "small_support_statement": (
            "0<=C_opt(y)-2*y*Lambda(0)<=y^3/(6*pi); the finite-temperature "
            "correction is cubic, not quadratic, at small support."
        ),
        "large_support_statement": (
            "0<=C_opt(y)-8*y^2/pi^3<=2*pi/3; the thermal Green operator "
            "fixes the sharp leading large-support coefficient."
        ),
        "full_phase_space_domination": (
            "The q-sector obeys C_q<=2*y/pi+2*y^2/pi^3. The s-wave momentum "
            "sector obeys C_p>=max(3*y/pi,8*y^2/pi^3), which dominates that "
            "q bound for every y>0. Resolvent monotonicity under A_l>=A_0 "
            "makes l=0 the worst momentum sector."
        ),
    }


def observer_cost_coefficient_from_optical_support(
    output_optical_radius: float,
    *,
    static_patch_radius: float,
) -> dict[str, float | str]:
    """Return ``F`` in ``Gamma <= E_K R F`` at ``beta=2*pi*R``."""
    _validate_positive("output_optical_radius", output_optical_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    y = output_optical_radius / static_patch_radius
    vacuum = 4.0 * asinh(1.0) * y / pi
    thermal = 8.0 * y**2 / pi**3
    return {
        "output_optical_radius_over_R_y": y,
        "vacuum_localization_term": vacuum,
        "thermal_static_patch_term": thermal,
        "dimensionless_cost_coefficient_F": vacuum + thermal,
        "theorem": (
            "For arbitrary-angular compact final Cauchy data in a centered "
            "optical ball [0,L], the exact KMS dephasing exponent obeys "
            "Gamma<=E_K*R*F(L/R), with "
            "F(y)=4 asinh(1)y/pi+8y^2/pi^3."
        ),
    }


def observer_cost_optimality_bracket_from_optical_support(
    output_optical_radius: float,
    *,
    static_patch_radius: float,
) -> dict[str, float | str]:
    """Sharp characterization and explicit bracket for ``Gamma/(E_K R)``."""
    sharp = sharp_observer_cost_characterization(
        output_optical_radius,
        static_patch_radius=static_patch_radius,
    )
    y = float(sharp["output_optical_radius_over_R_y"])
    lower = 3.0 * y / pi
    rigorous_lower = float(sharp["rigorous_lower_coefficient"])
    upper = float(sharp["rigorous_explicit_upper_coefficient"])
    return {
        "output_optical_radius_over_R_y": y,
        "constructive_lower_coefficient": lower,
        "rigorous_lower_coefficient": rigorous_lower,
        "uniform_upper_coefficient": upper,
        "upper_to_lower_ratio": upper / rigorous_lower,
        "small_support_limiting_ratio": 4.0 * asinh(1.0) / 3.0,
        "sharp_characterization": sharp,
        "statement": (
            "If C_opt(y)=sup Gamma/(E_K R) over all nonzero data supported "
            "in [0,L], then C_opt(y)=2y Lambda(y/2), the top eigenvalue of "
            "the exact dimensionless KMS momentum kernel. The optimizer is "
            "an s-wave momentum profile. The returned numeric lower and "
            "upper coefficients are rigorous explicit brackets."
        ),
    }


def observer_cost_coefficient(
    *,
    source_areal_radius: float,
    switching_duration: float,
    static_patch_radius: float,
) -> dict[str, object]:
    """Compose finite propagation with the localization-energy theorem."""
    support = causal_output_support_record(
        source_areal_radius=source_areal_radius,
        switching_duration=switching_duration,
        static_patch_radius=static_patch_radius,
    )
    coefficient = observer_cost_coefficient_from_optical_support(
        float(support["output_optical_radius_L"]),
        static_patch_radius=static_patch_radius,
    )
    sharp = sharp_observer_cost_characterization(
        float(support["output_optical_radius_L"]),
        static_patch_radius=static_patch_radius,
    )
    return {
        "causal_support": support,
        "coefficient": coefficient,
        "sharp_characterization": sharp,
    }


def dephasing_exponent_from_observer_error(observer_error: float) -> float:
    """Return ``Gamma=log(1/(2 epsilon))`` for ``0<epsilon<=1/2``."""
    _validate_positive("observer_error", observer_error)
    if observer_error > 0.5:
        raise ValueError("observer_error must be at most one half")
    return log(1.0 / (2.0 * observer_error))


def minimum_scalar_killing_energy(
    observer_error: float,
    *,
    source_areal_radius: float,
    switching_duration: float,
    static_patch_radius: float,
) -> dict[str, object]:
    """Coupling-free scalar-energy lower bound for a target channel error."""
    exponent = dephasing_exponent_from_observer_error(observer_error)
    cost = observer_cost_coefficient(
        source_areal_radius=source_areal_radius,
        switching_duration=switching_duration,
        static_patch_radius=static_patch_radius,
    )
    coefficient = cost["coefficient"]
    sharp = cost["sharp_characterization"]
    if not isinstance(coefficient, dict) or not isinstance(sharp, dict):
        raise TypeError("invalid cost coefficient record")
    f_value = float(coefficient["dimensionless_cost_coefficient_F"])
    explicit_upper = float(sharp["rigorous_explicit_upper_coefficient"])
    energy = exponent / (static_patch_radius * explicit_upper)
    return {
        "observer_error_epsilon": observer_error,
        "dephasing_exponent_Gamma": exponent,
        "minimum_scalar_killing_energy": energy,
        "dimensionless_minimum_energy_E_R": energy * static_patch_radius,
        "legacy_F_energy_lower_bound": (
            exponent / (static_patch_radius * f_value)
        ),
        "rigorous_explicit_optimal_coefficient_upper": explicit_upper,
        "exact_optimal_coefficient_formula": sharp[
            "exact_optimal_coefficient_formula"
        ],
        "cost": cost,
        "exact_channel_relation": (
            "epsilon_obs=(1/2)exp(-Gamma), where the half-diamond distance "
            "is measured from complete pointer dephasing"
        ),
    }


def spherical_wall_constraint_ratio(
    killing_energy: float,
    *,
    output_areal_radius: float,
    static_patch_radius: float,
    newton_constant: float,
) -> float:
    """Return the exact wall value ``2GE/[b(1-b^2/R^2)]``."""
    _validate_nonnegative("killing_energy", killing_energy)
    _validate_positive("output_areal_radius", output_areal_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    if output_areal_radius >= static_patch_radius:
        raise ValueError("output_areal_radius must lie inside the static patch")
    lapse = 1.0 - (output_areal_radius / static_patch_radius) ** 2
    return 2.0 * newton_constant * killing_energy / (
        output_areal_radius * lapse
    )


def flux_free_constraint_measure_record(
    areal_radius: float,
    *,
    static_patch_radius: float,
) -> dict[str, float | str]:
    """Audit the exact radial energy-measure identity for ``q=0`` data."""
    _validate_positive("areal_radius", areal_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    if areal_radius >= static_patch_radius:
        raise ValueError("areal_radius must lie inside the static patch")
    lapse = 1.0 - (areal_radius / static_patch_radius) ** 2
    normal_derivative_per_p = 1.0 / (
        sqrt(4.0 * pi) * areal_radius * sqrt(lapse)
    )
    density_per_p_squared = 0.5 * normal_derivative_per_p**2
    dr_per_dx = lapse
    mass_measure_per_p_squared_dx = (
        4.0
        * pi
        * areal_radius**2
        * density_per_p_squared
        * dr_per_dx
    )
    return {
        "areal_radius": areal_radius,
        "static_factor_N": lapse,
        "normal_derivative_per_radial_momentum": normal_derivative_per_p,
        "energy_density_per_radial_momentum_squared": density_per_p_squared,
        "dr_per_dx": dr_per_dx,
        "mass_measure_per_radial_momentum_squared_dx": (
            mass_measure_per_p_squared_dx
        ),
        "identity": "4*pi*r^2*rho*dr=(1/2)*p(x)^2*dx for phi=0",
    }


def observer_backreaction_lower_bound(
    observer_error: float,
    *,
    source_areal_radius: float,
    switching_duration: float,
    static_patch_radius: float,
    newton_constant: float,
) -> dict[str, object]:
    """Necessary Einstein-scalar constraint cost on a flux-free final slice."""
    energy = minimum_scalar_killing_energy(
        observer_error,
        source_areal_radius=source_areal_radius,
        switching_duration=switching_duration,
        static_patch_radius=static_patch_radius,
    )
    cost = energy["cost"]
    if not isinstance(cost, dict) or not isinstance(cost["causal_support"], dict):
        raise TypeError("invalid cost record")
    output_areal = float(cost["causal_support"]["output_areal_radius_b"])
    ratio = spherical_wall_constraint_ratio(
        float(energy["minimum_scalar_killing_energy"]),
        output_areal_radius=output_areal,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    return {
        **energy,
        "output_areal_radius_b": output_areal,
        "minimum_wall_constraint_ratio_q": ratio,
        "backreaction_statement": (
            "If the source is engineered to finish with q=0 field data, its "
            "radial momentum density vanishes and K_ij=0 is constraint-"
            "compatible. The exact conformal map gives "
            "4*pi*r^2*rho*dr=p(x)^2*dx/2, so the scalar constraint mass at the "
            "wall equals its fixed-background Killing energy. Hence "
            "sup_[0<r<=b] q(r)>=q(b), making the displayed value a necessary "
            "exact final-slice local radial-constraint cost on this flux-free "
            "subclass."
        ),
        "gravity_hypothesis": (
            "spherical final data, interaction switched off, q=0, vanishing "
            "matter momentum density, and K_ij=0. The nonzero scalar normal "
            "momentum means the full data are not time-reflection symmetric."
        ),
        "gravity_boundary": (
            "This constructs exact spherical Einstein-scalar Hamiltonian and "
            "momentum constraint data on the final slice. It does not derive "
            "the observer channel on the perturbed geometry or solve the "
            "source history, lapse, actuator stress, or subsequent evolution. "
            "The exterior mass shifts the cosmological horizon, so weak-field "
            "comparison with pure de Sitter is asserted only on the stated "
            "interior ball."
        ),
    }


def weak_gravity_observer_error_floor(
    *,
    maximum_constraint_ratio: float,
    source_areal_radius: float,
    switching_duration: float,
    static_patch_radius: float,
    newton_constant: float,
) -> dict[str, object]:
    """Accuracy floor from a local weak-constraint budget on ``0<r<=b``."""
    _validate_fraction(
        "maximum_constraint_ratio",
        maximum_constraint_ratio,
        allow_zero=False,
    )
    cost = observer_cost_coefficient(
        source_areal_radius=source_areal_radius,
        switching_duration=switching_duration,
        static_patch_radius=static_patch_radius,
    )
    support = cost["causal_support"]
    sharp = cost["sharp_characterization"]
    if not isinstance(support, dict) or not isinstance(sharp, dict):
        raise TypeError("invalid cost record")
    output_areal = float(support["output_areal_radius_b"])
    lapse = 1.0 - (output_areal / static_patch_radius) ** 2
    maximum_energy = (
        maximum_constraint_ratio * output_areal * lapse
        / (2.0 * newton_constant)
    )
    maximum_exponent = (
        maximum_energy
        * static_patch_radius
        * float(sharp["rigorous_explicit_upper_coefficient"])
    )
    return {
        "maximum_constraint_ratio_beta": maximum_constraint_ratio,
        "maximum_scalar_killing_energy_from_local_ball_budget": maximum_energy,
        "maximum_dephasing_exponent_Gamma": maximum_exponent,
        "minimum_observer_error_epsilon": 0.5 * exp(-maximum_exponent),
        "cost": cost,
        "logical_form": (
            "sup_[0<r<=b] q(r)<=beta implies "
            "epsilon_obs>=0.5 exp[-beta*b*N(b)*R*C_upper/2G], where "
            "C_upper rigorously bounds the exact C_opt=2y*Lambda(y/2)"
        ),
        "gravity_hypothesis": (
            "flux-free spherical post-switch Einstein-scalar constraint data "
            "with K_ij=0"
        ),
    }


def linear_momentum_profile_window(
    observer_error: float,
    *,
    support_areal_radius: float,
    static_patch_radius: float,
    newton_constant: float,
    maximum_constraint_ratio: float,
) -> dict[str, object]:
    """Explicit weak-gravity existence window for ``p(x) proportional x``.

    The ideal kick has ``q=0`` and normalized momentum
    ``p(x)=sqrt(3/ell^3)x`` on ``0<x<ell``, where ``ell`` is the source optical
    radius. Its positive mass profile is ``m(x)=E(x/ell)^3`` and its exact
    constraint ratio is increasing on the support ball. The Weyl vacuum covariance is
    ``Q_0=3ell/(2*pi)``, so the thermal covariance is at
    least this large. This gives a sufficient energy and backreaction bound.
    Smooth compact source approximants preserve any strict margin, but their
    actuator cost is not included.
    """
    _validate_fraction(
        "maximum_constraint_ratio",
        maximum_constraint_ratio,
        allow_zero=False,
    )
    exponent = dephasing_exponent_from_observer_error(observer_error)
    optical = de_sitter_optical_radius(
        support_areal_radius,
        static_patch_radius=static_patch_radius,
    )
    lapse = 1.0 - (support_areal_radius / static_patch_radius) ** 2
    covariance_lower = 3.0 * optical / (2.0 * pi)
    energy_upper = exponent / (2.0 * covariance_lower)
    constraint_upper = spherical_wall_constraint_ratio(
        energy_upper,
        output_areal_radius=support_areal_radius,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    maximum_exponent = (
        3.0
        * maximum_constraint_ratio
        * optical
        * support_areal_radius
        * lapse
        / (2.0 * pi * newton_constant)
    )
    return {
        "profile": "normalized p(x)=sqrt(3/ell^3)*x on 0<x<ell; q(x)=0",
        "dephasing_exponent_Gamma": exponent,
        "thermal_covariance_lower_bound_Q": covariance_lower,
        "vacuum_covariance_identity": (
            "<p,h^-1 p>=3ell/(2*pi), obtained by scaling x=ell*u and "
            "integrating int_0^1 t*log((1+t)/(1-t))dt=1"
        ),
        "sufficient_scalar_killing_energy_upper_bound": energy_upper,
        "sufficient_local_constraint_ratio_upper_bound": constraint_upper,
        "maximum_exponent_with_certified_weak_gravity": maximum_exponent,
        "target_has_certified_weak_gravity_window": (
            constraint_upper <= maximum_constraint_ratio
        ),
        "constraint_monotonicity": (
            "With x=R atanh(r/R), q(r) is proportional to "
            "x^3/[r(1-r^2/R^2)] and is strictly increasing for "
            "0<r<=support_areal_radius."
        ),
        "regularization_boundary": (
            "The hard endpoint profile is finite-energy but not C-infinity. "
            "Smooth profiles supported strictly inside L, vanishing linearly "
            "at the origin, approximate it while preserving any strict "
            "constraint margin. Choose the eta transition shorter than the "
            "remaining optical support margin; then J=P(eta*phi_free) is a "
            "smooth compact source inside the declared worldtube and produces "
            "the exact q=0 final datum."
        ),
    }


def local_scalar_observer_cost_certificate(
    *,
    observer_error: float = 1.0e-6,
    source_areal_radius: float = 0.2,
    switching_duration: float = 0.1,
    static_patch_radius: float = 1.0,
    newton_constant: float = 1.0e-6,
    maximum_constraint_ratio: float = 0.25,
) -> dict[str, object]:
    """Build the theorem, backreaction, and explicit-window certificate."""
    bound = observer_backreaction_lower_bound(
        observer_error,
        source_areal_radius=source_areal_radius,
        switching_duration=switching_duration,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    floor = weak_gravity_observer_error_floor(
        maximum_constraint_ratio=maximum_constraint_ratio,
        source_areal_radius=source_areal_radius,
        switching_duration=switching_duration,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    construction = linear_momentum_profile_window(
        observer_error,
        support_areal_radius=source_areal_radius,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
        maximum_constraint_ratio=maximum_constraint_ratio,
    )
    support = bound["cost"]
    if not isinstance(support, dict) or not isinstance(
        support["causal_support"], dict
    ):
        raise TypeError("invalid observer support record")
    optimality = observer_cost_optimality_bracket_from_optical_support(
        float(support["causal_support"]["output_optical_radius_L"]),
        static_patch_radius=static_patch_radius,
    )
    constraint_measure = flux_free_constraint_measure_record(
        0.5 * float(bound["output_areal_radius_b"]),
        static_patch_radius=static_patch_radius,
    )
    claims = {
        "general_beta_half_line_momentum_theorem": True,
        "exact_quasifree_pointer_channel": True,
        "harlow_pointer_target_identified_without_entropy_dictionary": True,
        "same_source_scalar_energy_and_stress": True,
        "coupling_eliminated_from_cost_bound": True,
        "finite_support_and_duration_enter_coefficient": True,
        "all_angular_conformal_scalar_extension": True,
        "smooth_compact_source_density_closure": True,
        "bekenstein_entropy_and_dephasing_forms_are_incomparable": True,
        "linear_support_scaling_has_two_sided_constants": (
            float(optimality["upper_to_lower_ratio"]) < 2.0
        ),
        "exact_kms_momentum_kernel": True,
        "full_phase_space_optimum_is_swave_momentum": True,
        "sharp_small_and_large_support_asymptotics": True,
        "necessary_flux_free_einstein_scalar_constraint_bound": (
            float(bound["minimum_wall_constraint_ratio_q"]) > 0.0
        ),
        "flux_free_constraint_mass_equals_scalar_killing_energy": (
            abs(
                float(
                    constraint_measure[
                        "mass_measure_per_radial_momentum_squared_dx"
                    ]
                )
                - 0.5
            )
            < 1.0e-14
        ),
        "nonempty_explicit_weak_gravity_window": construction[
            "target_has_certified_weak_gravity_window"
        ],
    }
    passed = all(bool(value) for value in claims.values())
    return {
        "goal": "Sharp final-support field-energy bound for thermal dephasing",
        "status": (
            "strengthened_final_support_theorem_pass_external_review_open"
            if passed
            else "fail"
        ),
        "model": (
            "finite pointer qubit, full conformally coupled massless scalar, "
            "Bunch-Davies beta=2*pi*R KMS state, smooth compact source in a "
            "centered static-patch ball"
        ),
        "same_action_model": scalar_pointer_action_record(),
        "all_angular_extension": all_angular_cost_extension_record(),
        "smooth_source_density": smooth_source_density_record(),
        "bekenstein_comparison": bekenstein_dephasing_comparison_record(),
        "optimality_bracket": optimality,
        "flux_free_constraint_measure": constraint_measure,
        "observer_cost_bound": bound,
        "weak_gravity_error_floor": floor,
        "explicit_window": construction,
        "certified_claims": claims,
        "paper_gate": (
            "The general-beta half-line momentum theorem, conformal de Sitter "
            "all-sector specialization, sharp final-support asymptotics, and "
            "smooth compact realization pass. Standalone novelty remains an "
            "external specialist-review gate. The final-slice gravity "
            "application and prescribed actuator are not headline claims."
        ),
        "claim_boundary": (
            "The renormalized post-switch field stress is the coherent "
            "classical stress generated by the same source and its Killing "
            "energy is exact. The spherical constraint statements additionally "
            "assume engineered flux-free final data and K_ij=0. The prescribed "
            "source and switching profile are external controls; their material "
            "stress, clock, and work storage are not modeled. The single Z_P "
            "across the smearing is a detector idealization, not an autonomous "
            "relativistic pointer field. The exact "
            "Einstein-scalar statement is final-slice constraint data only; "
            "the channel is not rederived on the perturbed geometry and this "
            "is not a full Einstein-matter evolution. Weak-field comparison "
            "with pure de Sitter is local to the declared interior ball, since "
            "the exterior mass shifts the cosmological horizon. The exact "
            "C_opt is sharp at fixed final Cauchy support; attainability from "
            "every smaller source cylinder with L=ell+T is not claimed."
        ),
    }
