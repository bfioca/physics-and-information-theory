"""Global SO(3) orientation-risk bounds from asymmetry and mean spin.

The theorem in this module is deliberately global.  It applies to an
arbitrary state, arbitrary multiplicity spaces on which rotations act
trivially, and an arbitrary orientation measurement.  Its two inputs are

* relative entropy of rotational asymmetry; and
* the mean integer-spin label of the reference representation.

The first controls accessible orientation information by the Holevo bound.
The second controls the first through a Gibbs variational estimate with
effective degeneracy ``(2j+1)^2``.  This avoids local-unbiasedness assumptions
and remains valid in the presence of rare high-spin tails.
"""

from __future__ import annotations

from math import cos, exp, expm1, isfinite, log, pi, sin, sqrt
from sys import float_info


SO3_GAUSSIAN_PARTITION_CONSTANT = pi ** 2.5 / 8.0
SO3_ASYMMETRY_RISK_CONSTANT = 6.0 / (exp(1.0) * pi ** (5.0 / 3.0))


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def so3_chordal_frame_cost(rotation_angle: float) -> float:
    """Return ``sin^2(theta/2)=(3-Tr R)/4`` for ``0<=theta<=pi``."""
    _validate_nonnegative("rotation_angle", rotation_angle)
    if rotation_angle > pi:
        raise ValueError("rotation_angle must be at most pi")
    return sin(0.5 * rotation_angle) ** 2


def so3_haar_ball_volume(rotation_angle: float) -> float:
    """Normalized Haar volume of the geodesic ball of radius ``theta``."""
    _validate_nonnegative("rotation_angle", rotation_angle)
    if rotation_angle > pi:
        raise ValueError("rotation_angle must be at most pi")
    return (rotation_angle - sin(rotation_angle)) / pi


def so3_cost_partition_upper_bound(dual_parameter: float) -> float:
    """Upper-bound ``integral exp(-lambda c(g)) dg`` by ``C lambda^-3/2``.

    For the rotation angle ``theta``, normalized Haar measure has radial
    density ``(2/pi) sin^2(theta/2)``.  The chord inequalities
    ``sin(theta/2)>=theta/pi`` and ``sin(theta/2)<=theta/2`` reduce the
    partition function to a three-dimensional Gaussian integral.
    """
    _validate_positive("dual_parameter", dual_parameter)
    return SO3_GAUSSIAN_PARTITION_CONSTANT / dual_parameter**1.5


def asymmetry_orientation_risk_lower_bound(
    relative_entropy_of_asymmetry: float,
) -> float:
    """All-measurement Bayes-risk floor from rotational asymmetry.

    If ``A=D(rho || G(rho))`` for the SO(3) twirl and the true orientation is
    Haar distributed, every estimate obeys

    ``E[sin^2(theta_error/2)] >= C_* exp(-2 A/3)``.
    """
    _validate_nonnegative(
        "relative_entropy_of_asymmetry",
        relative_entropy_of_asymmetry,
    )
    return SO3_ASYMMETRY_RISK_CONSTANT * exp(
        -2.0 * relative_entropy_of_asymmetry / 3.0
    )


def spin_gibbs_partition(dual_parameter: float) -> float:
    """Return ``sum_j (2j+1)^2 exp(-beta j)`` in closed form."""
    log_partition = log_spin_gibbs_partition(dual_parameter)
    if log_partition > log(float_info.max):
        return float("inf")
    return exp(log_partition)


def log_spin_gibbs_partition(dual_parameter: float) -> float:
    """Log partition function, stable when the partition itself overflows."""
    _validate_positive("dual_parameter", dual_parameter)
    x = exp(-dual_parameter)
    one_minus_x = -expm1(-dual_parameter)
    return log(1.0 + 6.0 * x + x * x) - 3.0 * log(one_minus_x)


def spin_gibbs_mean(dual_parameter: float) -> float:
    """Mean spin label of the Gibbs distribution with degeneracy ``d_j^2``."""
    _validate_positive("dual_parameter", dual_parameter)
    x = exp(-dual_parameter)
    one_minus_x = -expm1(-dual_parameter)
    return (
        x * (6.0 + 2.0 * x) / (1.0 + 6.0 * x + x * x)
        + 3.0 * x / one_minus_x
    )


def mean_spin_asymmetry_upper_bound(
    mean_spin: float,
    *,
    dual_parameter: float,
) -> float:
    """Gibbs variational upper bound ``A<=beta K+log Z(beta)``."""
    _validate_nonnegative("mean_spin", mean_spin)
    _validate_positive("dual_parameter", dual_parameter)
    return dual_parameter * mean_spin + log_spin_gibbs_partition(dual_parameter)


def optimal_spin_gibbs_dual_parameter(mean_spin: float) -> float:
    """Solve ``-d log Z/dbeta=K`` by monotone bisection."""
    _validate_nonnegative("mean_spin", mean_spin)
    if mean_spin == 0.0:
        return float("inf")

    lower = 1.0 / (mean_spin + 1.0)
    upper = max(1.0, 10.0 / (mean_spin + 1.0))
    while spin_gibbs_mean(lower) < mean_spin:
        lower *= 0.5
    while spin_gibbs_mean(upper) > mean_spin:
        upper *= 2.0

    for _ in range(200):
        midpoint = exp(0.5 * (log(lower) + log(upper)))
        if spin_gibbs_mean(midpoint) > mean_spin:
            lower = midpoint
        else:
            upper = midpoint
    return 0.5 * (lower + upper)


def optimized_mean_spin_asymmetry_upper_bound(mean_spin: float) -> float:
    """Sharp Gibbs upper envelope for asymmetry at fixed mean spin label."""
    beta = optimal_spin_gibbs_dual_parameter(mean_spin)
    if beta == float("inf"):
        return 0.0
    return mean_spin_asymmetry_upper_bound(
        mean_spin,
        dual_parameter=beta,
    )


def mean_spin_orientation_risk_lower_bound(mean_spin: float) -> float:
    """Tail-robust global risk floor for all states with mean spin ``<=K``."""
    asymmetry_bound = optimized_mean_spin_asymmetry_upper_bound(mean_spin)
    return asymmetry_orientation_risk_lower_bound(asymmetry_bound)


def mean_casimir_orientation_risk_lower_bound(mean_casimir: float) -> float:
    """Direct fusion/Hardy risk floor ``1/(16 <J^2>+8)``.

    The cost convention is the unit-range
    ``sin^2(theta_error/2)`` used throughout this module.
    """
    _validate_nonnegative("mean_casimir", mean_casimir)
    return 1.0 / (16.0 * mean_casimir + 8.0)


def projective_mean_casimir_orientation_risk_lower_bound(
    mean_casimir: float,
) -> float:
    """Fusion/Hardy floor ``1/(16<J^2>)`` in one half-integer sector."""
    _validate_nonnegative("mean_casimir", mean_casimir)
    if mean_casimir < 0.75:
        raise ValueError(
            "a half-integer projective sector has mean Casimir at least 3/4"
        )
    return 1.0 / (16.0 * mean_casimir)


def projective_hard_cutoff_orientation_risk_lower_bound(
    reference_cutoff: int,
) -> float:
    """Sharp floor for spins ``1/2,3/2,...,J+1/2``."""
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    return sin(pi / (2.0 * (reference_cutoff + 2.0))) ** 2


def projective_fusion_score_matrix(
    reference_cutoff: int,
) -> tuple[tuple[int, ...], ...]:
    """Spin-1 fusion matrix on one odd half-integer Peter-Weyl sector."""
    projective_hard_cutoff_orientation_risk_lower_bound(reference_cutoff)
    size = reference_cutoff + 1
    return tuple(
        tuple(int(left == right or abs(left - right) == 1) for right in range(size))
        for left in range(size)
    )


def heat_diffused_orientation_risk_lower_bound(
    mean_casimir: float,
    dimensionless_time: float,
) -> float:
    """Global risk floor after isotropic reference-only rotational diffusion.

    The spin-1 character score is multiplied exactly by ``exp(-2s)`` under the
    SO(3) heat semigroup.  Combining that identity with the fusion/Hardy score
    ceiling gives an interpolation from the resource floor at ``s=0`` to the
    no-information Haar risk ``3/4``.
    """
    _validate_nonnegative("mean_casimir", mean_casimir)
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    initial_floor = mean_casimir_orientation_risk_lower_bound(mean_casimir)
    return heat_attenuated_orientation_risk_lower_bound(
        initial_floor,
        dimensionless_time,
    )


def heat_attenuated_orientation_risk_lower_bound(
    initial_risk_lower_bound: float,
    dimensionless_time: float,
) -> float:
    """Attenuate any valid initial chordal-risk floor by SO(3) heat flow."""
    _validate_nonnegative("initial_risk_lower_bound", initial_risk_lower_bound)
    if initial_risk_lower_bound > 0.75:
        raise ValueError("initial_risk_lower_bound must be at most three quarters")
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    attenuation = exp(-2.0 * dimensionless_time)
    return 0.75 * (1.0 - attenuation) + attenuation * initial_risk_lower_bound


def maximum_dimensionless_coherence_time(
    mean_casimir_upper_bound: float,
    risk_budget: float,
) -> float:
    """Necessary upper time for maintaining risk at most ``risk_budget``.

    The result uses the weakest fusion floor allowed by the supplied Casimir
    capacity.  Zero means the requested risk is excluded already at time zero;
    infinity means the budget is at least the no-information Haar risk.
    """
    _validate_nonnegative("mean_casimir_upper_bound", mean_casimir_upper_bound)
    _validate_nonnegative("risk_budget", risk_budget)
    if risk_budget > 1.0:
        raise ValueError("risk_budget must be at most one")
    initial_floor = mean_casimir_orientation_risk_lower_bound(
        mean_casimir_upper_bound
    )
    return maximum_coherence_time_from_initial_floor(initial_floor, risk_budget)


def maximum_coherence_time_from_initial_floor(
    initial_risk_lower_bound: float,
    risk_budget: float,
) -> float:
    """Necessary SO(3)-heat coherence time from any initial risk floor."""
    _validate_nonnegative("initial_risk_lower_bound", initial_risk_lower_bound)
    if initial_risk_lower_bound > 0.75:
        raise ValueError("initial_risk_lower_bound must be at most three quarters")
    _validate_nonnegative("risk_budget", risk_budget)
    if risk_budget > 1.0:
        raise ValueError("risk_budget must be at most one")
    if risk_budget < initial_risk_lower_bound:
        return 0.0
    if risk_budget >= 0.75:
        return float("inf")
    return 0.5 * log(
        (0.75 - initial_risk_lower_bound) / (0.75 - risk_budget)
    )


def hard_cutoff_orientation_risk_lower_bound(reference_cutoff: int) -> float:
    """Sharp fusion-matrix floor for states supported on ``0<=j<=J``."""
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    return sin(pi / (2.0 * reference_cutoff + 3.0)) ** 2


def tail_quantile_orientation_risk_lower_bound(
    reference_cutoff: int,
    tail_probability: float,
) -> float:
    """Transfer the sharp cutoff floor through a high-spin tail.

    Normalized projection onto ``j<=J`` changes the state by trace distance at
    most ``sqrt(q_J)``.  The cost lies in ``[0,1]``.
    """
    cutoff_bound = hard_cutoff_orientation_risk_lower_bound(reference_cutoff)
    _validate_nonnegative("tail_probability", tail_probability)
    if tail_probability > 1.0:
        raise ValueError("tail_probability must be at most one")
    return max(0.0, cutoff_bound - sqrt(tail_probability))


def fusion_score_matrix(reference_cutoff: int) -> tuple[tuple[int, ...], ...]:
    """Spin-1 fusion upper-bound matrix through integer spin ``J``."""
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    size = reference_cutoff + 1
    return tuple(
        tuple(
            int(
                (left == right and left >= 1)
                or abs(left - right) == 1
            )
            for right in range(size)
        )
        for left in range(size)
    )


def fusion_score_maximum_eigenvalue(reference_cutoff: int) -> float:
    """Largest eigenvalue ``1+2 cos(2 pi/(2J+3))``."""
    hard_cutoff_orientation_risk_lower_bound(reference_cutoff)
    return 1.0 + 2.0 * cos(2.0 * pi / (2.0 * reference_cutoff + 3.0))


def mean_spin_upper_bound_from_mean_casimir(mean_casimir: float) -> float:
    """Use Jensen: ``K(K+1)<=E[j(j+1)]``."""
    _validate_nonnegative("mean_casimir", mean_casimir)
    root = sqrt(1.0 + 4.0 * mean_casimir)
    return 2.0 * mean_casimir / (root + 1.0)


def compact_rotor_orientation_risk_record(
    *,
    observer_radius: float,
    newton_constant: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> dict[str, object]:
    """Insert the spherical-top compactness Casimir budget into the theorem."""
    from .finite_size_static_patch_observer import (
        maximum_mean_casimir_from_compactness,
    )

    maximum_mean_casimir = maximum_mean_casimir_from_compactness(
        observer_radius=observer_radius,
        newton_constant=newton_constant,
        inertia_coefficient=inertia_coefficient,
        compactness_margin=compactness_margin,
        maximum_excitation_fraction=maximum_excitation_fraction,
    )
    maximum_mean_spin = mean_spin_upper_bound_from_mean_casimir(
        maximum_mean_casimir
    )
    asymmetry_bound = optimized_mean_spin_asymmetry_upper_bound(
        maximum_mean_spin
    )
    asymmetry_risk_bound = asymmetry_orientation_risk_lower_bound(asymmetry_bound)
    casimir_risk_bound = mean_casimir_orientation_risk_lower_bound(
        maximum_mean_casimir
    )
    risk_bound = max(asymmetry_risk_bound, casimir_risk_bound)
    return {
        "observer_radius_a": observer_radius,
        "newton_constant_G": newton_constant,
        "inertia_coefficient_kappa": inertia_coefficient,
        "compactness_margin_chi": compactness_margin,
        "maximum_excitation_fraction_zeta": maximum_excitation_fraction,
        "maximum_mean_casimir_Cbar": maximum_mean_casimir,
        "maximum_mean_spin_K": maximum_mean_spin,
        "maximum_relative_entropy_of_asymmetry": asymmetry_bound,
        "asymmetry_mean_spin_risk_lower_bound": asymmetry_risk_bound,
        "direct_mean_casimir_risk_lower_bound": casimir_risk_bound,
        "global_chordal_orientation_risk_lower_bound": risk_bound,
        "risk_cost": "E[sin^2(theta_error/2)]=(3-E[Tr R_error])/4",
        "scope": (
            "all normal states of the integer-spin SO(3) rotor, arbitrary "
            "rotation-trivial multiplicities, Haar prior, and arbitrary POVMs, "
            "under the declared spherical-top inertia, excitation, and local "
            "compactness hypotheses"
        ),
    }


def peter_weyl_token_risk_audit(reference_cutoff: int) -> dict[str, object]:
    """Compare the canonical token's exact risk with the universal floors."""
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    dimension = (
        (reference_cutoff + 1)
        * (2 * reference_cutoff + 1)
        * (2 * reference_cutoff + 3)
        // 3
    )
    mean_spin = sum(
        spin * (2 * spin + 1) ** 2
        for spin in range(reference_cutoff + 1)
    ) / float(dimension)
    exact_asymmetry = log(float(dimension))
    mean_casimir = 3.0 * reference_cutoff * (reference_cutoff + 2.0) / 5.0
    exact_risk = (
        4.0 * reference_cutoff * (reference_cutoff + 2.0) + 3.0
    ) / (4.0 * dimension)
    asymmetry_floor = asymmetry_orientation_risk_lower_bound(exact_asymmetry)
    mean_spin_floor = mean_spin_orientation_risk_lower_bound(mean_spin)
    mean_casimir_floor = mean_casimir_orientation_risk_lower_bound(mean_casimir)
    hard_cutoff_floor = hard_cutoff_orientation_risk_lower_bound(reference_cutoff)
    return {
        "reference_cutoff_J": reference_cutoff,
        "peter_weyl_dimension_D_J": dimension,
        "mean_spin_K": mean_spin,
        "mean_casimir": mean_casimir,
        "exact_relative_entropy_of_asymmetry": exact_asymmetry,
        "canonical_token_exact_chordal_orientation_risk": exact_risk,
        "asymmetry_risk_lower_bound": asymmetry_floor,
        "mean_spin_risk_lower_bound": mean_spin_floor,
        "mean_casimir_risk_lower_bound": mean_casimir_floor,
        "hard_cutoff_risk_lower_bound": hard_cutoff_floor,
        "bounds_respected": (
            exact_risk + 1.0e-14 >= asymmetry_floor
            and asymmetry_floor + 1.0e-14 >= mean_spin_floor
            and exact_risk + 1.0e-14 >= mean_casimir_floor
            and exact_risk + 1.0e-14 >= hard_cutoff_floor
        ),
    }


def global_so3_reference_risk_certificate() -> dict[str, object]:
    """Return a deterministic audit of the global risk theorem package."""
    token_records = tuple(
        peter_weyl_token_risk_audit(cutoff)
        for cutoff in (0, 1, 2, 4, 8, 16, 32)
    )
    rare_tail_fixed_mean_spin = 1.0
    rare_tail_floor = mean_spin_orientation_risk_lower_bound(
        rare_tail_fixed_mean_spin
    )
    compact_record = compact_rotor_orientation_risk_record(
        observer_radius=1.0e-3,
        newton_constant=1.0e-12,
        inertia_coefficient=2.0 / 3.0,
        compactness_margin=0.5,
        maximum_excitation_fraction=0.25,
    )
    coherence_budget = 0.1
    coherence_time = maximum_dimensionless_coherence_time(
        compact_record["maximum_mean_casimir_Cbar"],
        coherence_budget,
    )
    certified_claims = {
        "peter_weyl_exact_risks_respect_both_universal_bounds": all(
            bool(record["bounds_respected"]) for record in token_records
        ),
        "mean_spin_bound_is_tail_robust": rare_tail_floor > 0.0,
        "compact_rotor_has_positive_global_risk_floor": (
            compact_record["global_chordal_orientation_risk_lower_bound"] > 0.0
        ),
        "fusion_hardy_casimir_floor_is_positive": all(
            record["mean_casimir_risk_lower_bound"] > 0.0
            for record in token_records
        ),
        "heat_diffusion_coherence_ceiling_is_positive_and_finite": (
            isfinite(coherence_time) and coherence_time > 0.0
        ),
        "risk_floor_decreases_with_reference_cutoff": all(
            right["mean_spin_risk_lower_bound"]
            < left["mean_spin_risk_lower_bound"]
            for left, right in zip(token_records[1:], token_records[2:])
        ),
    }
    return {
        "goal": "Tail-Robust Global SO(3) Orientation-Risk Theorem",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "central_result": (
            "For chordal full-frame cost and a Haar prior, every orientation "
            "measurement obeys both R>=1/(16<J^2>+8) and "
            "R>=6/(e*pi^(5/3))*exp(-2 A_SO3/3). For a reference with mean "
            "integer-spin label K, A_SO3 is at most inf_beta[beta K+log("
            "(1+6e^-beta+e^-2beta)/(1-e^-beta)^3)]."
        ),
        "rare_tail_consequence": (
            "A fixed mean-spin budget gives a strictly positive global Bayes-"
            "risk floor even when an arbitrarily remote spin sector carries a "
            "vanishing probability and divergent local QFI."
        ),
        "certified_claims": certified_claims,
        "rare_tail_mean_spin_K": rare_tail_fixed_mean_spin,
        "rare_tail_global_risk_lower_bound": rare_tail_floor,
        "peter_weyl_audits": token_records,
        "compact_rotor_audit": compact_record,
        "coherence_risk_budget": coherence_budget,
        "maximum_dimensionless_coherence_time": coherence_time,
        "risk_floor_at_coherence_ceiling": heat_diffused_orientation_risk_lower_bound(
            compact_record["maximum_mean_casimir_Cbar"],
            coherence_time,
        ),
        "claim_boundary": (
            "This is an information-theoretic SO(3) estimation theorem. It does "
            "not by itself provide a local interaction, coherent quantum "
            "recovery, a coherence time, or a model-independent gravitational "
            "compactness theorem."
        ),
    }
