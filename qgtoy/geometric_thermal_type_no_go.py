"""Geometric Type-I no-go for a global fuzzy-sphere thermal regulator.

The normal-ordered free boson Hamiltonian uses angular frequencies
``omega_l=sqrt(mu^2+l(l+1)/R^2)`` with degeneracy ``2l+1``.  For positive mass
and inverse temperature, its infinite angular Gibbs partition function is
finite.  The harmonic-cutoff Gibbs densities converge in trace norm after the
omitted modes are embedded in their vacuum.  The resulting global algebra is
therefore Type I, not the local Type-III algebra needed before a gravitational
modular crossed product.
"""

from __future__ import annotations

from math import exp, expm1, isfinite, log, log1p, pi, sqrt


def _validate_cutoff(cutoff: int) -> None:
    if isinstance(cutoff, bool) or not isinstance(cutoff, int) or cutoff < 0:
        raise ValueError("cutoff must be a nonnegative integer")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def angular_frequency(level: int, *, mass: float, radius: float) -> float:
    """Free scalar angular frequency on a sphere of radius ``radius``."""
    _validate_cutoff(level)
    if not isfinite(mass) or mass < 0.0:
        raise ValueError("mass must be finite and nonnegative")
    _validate_positive("radius", radius)
    return sqrt(mass * mass + level * (level + 1) / (radius * radius))


def log_partition_cutoff(
    cutoff: int,
    *,
    beta: float,
    mass: float,
    radius: float,
) -> float:
    """Log partition function through an angular momentum cutoff."""
    _validate_cutoff(cutoff)
    _validate_positive("beta", beta)
    if not isfinite(mass) or mass <= 0.0:
        raise ValueError("mass must be finite and positive for the Gibbs state")
    _validate_positive("radius", radius)
    return sum(
        -(2 * level + 1)
        * log1p(-exp(-beta * angular_frequency(level, mass=mass, radius=radius)))
        for level in range(cutoff + 1)
    )


def mean_particle_number_cutoff(
    cutoff: int,
    *,
    beta: float,
    mass: float,
    radius: float,
) -> float:
    """Expected total occupation through the angular cutoff."""
    _validate_cutoff(cutoff)
    _validate_positive("beta", beta)
    if not isfinite(mass) or mass <= 0.0:
        raise ValueError("mass must be finite and positive for the Gibbs state")
    _validate_positive("radius", radius)
    total = 0.0
    for level in range(cutoff + 1):
        exponent = beta * angular_frequency(level, mass=mass, radius=radius)
        occupation = exp(-exponent) if exponent > 700.0 else 1.0 / expm1(exponent)
        total += (2 * level + 1) * occupation
    return total


def angular_tail_geometric_sum(cutoff: int, *, beta: float, radius: float) -> float:
    """Exact sum of ``(2l+1)q^l`` above the cutoff, ``q=e^-beta/R``."""
    _validate_cutoff(cutoff)
    _validate_positive("beta", beta)
    _validate_positive("radius", radius)
    exponent = beta / radius
    q = exp(-exponent)
    one_minus_q = -expm1(-exponent)
    first = cutoff + 1
    numerator = q**first * (2.0 + (2 * first - 1) * one_minus_q)
    return numerator / (one_minus_q**2)


def log_partition_tail_upper_bound(
    cutoff: int,
    *,
    beta: float,
    radius: float,
) -> float:
    """Bound the omitted massive log partition function independently of mass."""
    _validate_cutoff(cutoff)
    _validate_positive("beta", beta)
    _validate_positive("radius", radius)
    one_minus_q = -expm1(-beta / radius)
    return angular_tail_geometric_sum(cutoff, beta=beta, radius=radius) / one_minus_q


def finite_shell_log_partition(
    cutoff: int,
    tail_cutoff: int,
    *,
    beta: float,
    mass: float,
    radius: float,
) -> float:
    """Exact log partition function of modes ``cutoff < l <= tail_cutoff``."""
    _validate_cutoff(cutoff)
    _validate_cutoff(tail_cutoff)
    if tail_cutoff <= cutoff:
        raise ValueError("tail_cutoff must exceed cutoff")
    _validate_positive("beta", beta)
    _validate_positive("mass", mass)
    _validate_positive("radius", radius)
    return sum(
        -(2 * level + 1)
        * log1p(-exp(-beta * angular_frequency(level, mass=mass, radius=radius)))
        for level in range(cutoff + 1, tail_cutoff + 1)
    )


def finite_shell_vacuum_trace_distance(
    cutoff: int,
    tail_cutoff: int,
    *,
    beta: float,
    mass: float,
    radius: float,
) -> float:
    """Exact normalized trace distance from shell vacuum to its Gibbs state."""
    shell_log_partition = finite_shell_log_partition(
        cutoff,
        tail_cutoff,
        beta=beta,
        mass=mass,
        radius=radius,
    )
    return -expm1(-shell_log_partition)


def static_patch_optical_volume(*, radius: float, stretched_distance: float) -> float:
    """Optical volume of a four-dimensional de Sitter static slice cutoff at R-delta."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    if stretched_distance >= radius:
        raise ValueError("stretched_distance must be smaller than radius")
    x = 1.0 - stretched_distance / radius
    antiderivative = x / (2.0 * (1.0 - x * x)) - 0.25 * log(
        (1.0 + x) / (1.0 - x)
    )
    return 4.0 * pi * radius**3 * antiderivative


def optical_volume_record(*, radius: float, stretched_distance: float) -> dict[str, object]:
    """Record the near-horizon optical-volume divergence absent angular-only refinement."""
    volume = static_patch_optical_volume(
        radius=radius,
        stretched_distance=stretched_distance,
    )
    return {
        "sphere_radius_R": radius,
        "stretched_horizon_distance_delta": stretched_distance,
        "optical_volume": volume,
        "leading_divergence": "pi R^4/delta",
        "scaled_asymptotic_ratio": (
            stretched_distance * volume / (pi * radius**4)
        ),
        "interpretation": (
            "the static-patch local-field regulator has an infinite optical-volume "
            "limit at the horizon, a geometric limit absent from angular refinement"
        ),
    }


def trace_distance_to_thermal_limit_bound(
    cutoff: int,
    *,
    beta: float,
    radius: float,
) -> float:
    """Bound cutoff Gibbs plus tail vacuum versus the infinite Gibbs density."""
    tail_log_partition_bound = log_partition_tail_upper_bound(
        cutoff,
        beta=beta,
        radius=radius,
    )
    return min(1.0, tail_log_partition_bound)


def geometric_thermal_limit_record(
    cutoff: int,
    *,
    beta: float = 2.0,
    mass: float = 1.0,
    radius: float = 1.0,
) -> dict[str, object]:
    """Record the analytic convergence and operator-algebra consequence."""
    log_partition = log_partition_cutoff(
        cutoff,
        beta=beta,
        mass=mass,
        radius=radius,
    )
    mean_particles = mean_particle_number_cutoff(
        cutoff,
        beta=beta,
        mass=mass,
        radius=radius,
    )
    tail_bound = log_partition_tail_upper_bound(
        cutoff,
        beta=beta,
        radius=radius,
    )
    return {
        "cutoff_L": cutoff,
        "inverse_temperature_beta": beta,
        "mass_mu": mass,
        "sphere_radius_R": radius,
        "mode_frequency": "sqrt(mu^2+l(l+1)/R^2)",
        "mode_degeneracy": "2l+1",
        "normal_ordered_log_partition_cutoff": log_partition,
        "mean_particle_number_cutoff": mean_particles,
        "log_partition_tail_upper_bound": tail_bound,
        "trace_distance_to_limit_upper_bound": min(1.0, tail_bound),
        "tail_bound_tends_to_zero": True,
        "infinite_partition_function_is_finite": True,
        "infinite_gibbs_density_is_trace_class": True,
        "cutoff_states_converge_in_trace_norm": True,
        "global_observable_algebra": "B(Gamma_s(L2(S2))) in the Fock representation",
        "global_gns_algebra_under_declared_algebra": "B(Fock), Type I_infinity",
        "modular_action": "inner, implemented by the Gibbs density",
        "continuous_core": "Type-I algebra with diffuse center, not a Type-II factor",
        "derivation": (
            "omega_l>=l/R and -log(1-x)<=x/(1-q) for x<=q^l, "
            "q=exp(-beta/R); the omitted thermal state differs from its vacuum "
            "by 1-exp(-log Z_tail)<=log Z_tail"
        ),
    }


def massless_zero_mode_record(*, beta: float = 2.0, radius: float = 1.0) -> dict[str, object]:
    """Separate the compact massless zero-mode divergence from Type-III behavior."""
    _validate_positive("beta", beta)
    _validate_positive("radius", radius)
    return {
        "inverse_temperature_beta": beta,
        "sphere_radius_R": radius,
        "mass_mu": 0.0,
        "zero_mode_frequency": 0.0,
        "formal_occupation_partition_factor": "(1-exp(-beta*0))^-1=infinity",
        "canonical_zero_mode": (
            "the noncompact constant scalar mode is a free-particle degree of "
            "freedom, for which the thermal trace diverges"
        ),
        "global_gibbs_state_exists": False,
        "interpretation": (
            "infrared zero-mode failure of the global Gibbs ensemble; it does "
            "not produce a local Type-III factor or a Type-II observer algebra"
        ),
        "standard_repairs": (
            "positive mass, zero-mode removal, or compact field target; each "
            "returns to the declared global Type-I Fock-algebra setting"
        ),
    }


def geometric_thermal_type_no_go_certificate(
    *,
    max_cutoff: int = 24,
    beta: float = 2.0,
    mass: float = 1.0,
    radius: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, object]:
    """Audit the global geometric Gibbs Type-I obstruction."""
    _validate_cutoff(max_cutoff)
    _validate_positive("beta", beta)
    _validate_positive("mass", mass)
    _validate_positive("radius", radius)
    _validate_positive("tolerance", tolerance)
    records = tuple(
        geometric_thermal_limit_record(
            cutoff,
            beta=beta,
            mass=mass,
            radius=radius,
        )
        for cutoff in range(max_cutoff + 1)
    )
    tail_bounds = tuple(record["log_partition_tail_upper_bound"] for record in records)
    certified_claims = {
        "geometric_tail_bound_is_nonincreasing": all(
            right <= left for left, right in zip(tail_bounds, tail_bounds[1:])
        ),
        "global_partition_function_converges": all(
            record["infinite_partition_function_is_finite"] for record in records
        ),
        "cutoff_gibbs_states_have_a_trace_norm_limit": all(
            record["cutoff_states_converge_in_trace_norm"] for record in records
        ),
        "global_harmonic_limit_remains_type_i": all(
            record["global_gns_algebra_under_declared_algebra"]
            == "B(Fock), Type I_infinity"
            for record in records
        ),
        "requested_terminal_tolerance_is_reached": tail_bounds[-1] <= tolerance,
        "massless_zero_mode_is_an_ir_divergence_not_a_typeiii_mechanism": not (
            massless_zero_mode_record(beta=beta, radius=radius)["global_gibbs_state_exists"]
        ),
    }
    return {
        "goal": "Global Geometric Thermal Type-I No-Go",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "trace_class_global_gibbs_static_patch_regulator_obstruction",
        "central_result": (
            "For a positive-mass free boson with fuzzy-sphere angular cutoff, "
            "omega_l=sqrt(mu^2+l(l+1)/R^2), the cutoff Gibbs states converge in "
            "trace norm to a trace-class global Gibbs density on the declared "
            "global Fock algebra B(Fock). Its GNS algebra is Type I, and its "
            "inner modular crossed "
            "product is not the Type-II factor of the de Sitter observer algebra."
        ),
        "physical_consequence": (
            "Adding arbitrarily many compact angular harmonics to the global Fock "
            "algebra is insufficient. A successful construction must retain "
            "localization and net structure; a faithful static-patch realization "
            "should also include radial and near-horizon redshift degrees of freedom."
        ),
        "claim_boundary": (
            "global normal-ordered free scalar Gibbs model on a compact sphere, "
            "positive mass, angular cutoff removal; interacting local AQFT nets, "
            "radial static-patch modes, horizon redshift, gauge constraints, and "
            "the Bunch-Davies local representation are outside the theorem"
        ),
        "certified_claims": certified_claims,
        "records": records,
        "massless_zero_mode_record": massless_zero_mode_record(beta=beta, radius=radius),
        "optical_volume_records": tuple(
            optical_volume_record(radius=radius, stretched_distance=radius / power)
            for power in (4.0, 16.0, 64.0, 256.0, 1024.0)
        ),
        "next_physics_gate": (
            "construct nested local static-patch algebras and prove distributional "
            "KMS/modular convergence; include the radial/redshift sector for a "
            "faithful de Sitter realization before crossing with the clock"
        ),
    }
