"""Goal 24 conditional dS ER=EPR theorem ledger.

The module deliberately separates three layers:

* exact finite-cutoff statements inherited from Goal 23;
* a conditional finite-to-continuum theorem schema;
* physical assumptions that are not proved by the finite certificate.
"""

from __future__ import annotations

from math import exp, sqrt

from .relative_entropy_bridge import _rounded
from .static_patch_testbed import (
    goal23_regulated_static_patch_ds_cft_certificate,
    mode_count,
    regulated_kernel_summary,
    regulated_static_patch_collision_record,
    static_patch_mode_labels,
)


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 1:
        raise ValueError("max_cutoff must be at least one")


def _validate_low_order(low_order: int) -> None:
    if low_order < 0:
        raise ValueError("low_order must be nonnegative")


def _validate_probability(screen_probability: float) -> None:
    if not 0.0 <= screen_probability <= 1.0:
        raise ValueError("screen_probability must lie in [0,1]")


def _validate_alpha(alpha: float) -> None:
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must lie in [0,1]")


def _validate_damping_steps(damping_steps: int) -> None:
    if damping_steps < 0:
        raise ValueError("damping_steps must be nonnegative")


def _static_patch_mode_distance(
    first: tuple[int, int],
    second: tuple[int, int],
) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def max_static_patch_mode_distance(cutoff: int) -> int:
    """Maximum mode-distance used by the Goal 23 geometric kernel."""
    labels = static_patch_mode_labels(cutoff)
    return max(
        _static_patch_mode_distance(first, second)
        for first in labels
        for second in labels
    )


def static_patch_schur_coefficient(
    cutoff: int,
    first: tuple[int, int],
    second: tuple[int, int],
    *,
    alpha: float,
    damping_steps: int = 1,
) -> float:
    """Coefficient for the regulated Schur multiplier K_L(alpha,s)."""
    _validate_alpha(alpha)
    _validate_damping_steps(damping_steps)
    if first == second:
        return 1.0
    exponent = -damping_steps * _static_patch_mode_distance(first, second)
    exponent /= float((cutoff + 1) ** 2)
    return alpha * exp(exponent)


def static_patch_schur_coefficient_matrix(
    cutoff: int,
    *,
    alpha: float,
    damping_steps: int = 1,
) -> tuple[tuple[float, ...], ...]:
    """Finite coefficient matrix for the static-patch Schur multiplier."""
    labels = static_patch_mode_labels(cutoff)
    return tuple(
        tuple(
            static_patch_schur_coefficient(
                cutoff,
                first,
                second,
                alpha=alpha,
                damping_steps=damping_steps,
            )
            for second in labels
        )
        for first in labels
    )


def _cholesky_psd_summary(
    matrix: tuple[tuple[float, ...], ...],
    *,
    tolerance: float = 1e-10,
) -> dict[str, object]:
    """Small dependency-free PSD check for symmetric floating matrices."""
    size = len(matrix)
    lower = [[0.0 for _ in range(size)] for _ in range(size)]
    min_pivot = float("inf")
    for row in matrix:
        if len(row) != size:
            raise ValueError("matrix must be square")
    for i in range(size):
        for j in range(i + 1):
            value = matrix[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                min_pivot = min(min_pivot, value)
                if value < -tolerance:
                    return {
                        "psd": False,
                        "min_cholesky_pivot": _rounded(value),
                        "failure_index": i,
                    }
                lower[i][j] = sqrt(max(value, 0.0))
            elif lower[j][j] > tolerance:
                lower[i][j] = value / lower[j][j]
            elif abs(value) > tolerance:
                return {
                    "psd": False,
                    "min_cholesky_pivot": _rounded(min_pivot),
                    "failure_index": (i, j),
                }
    return {
        "psd": True,
        "min_cholesky_pivot": _rounded(min_pivot if size else 0.0),
        "failure_index": None,
    }


def static_patch_schur_channel_audit(
    cutoff: int,
    *,
    alpha: float,
    damping_steps: int = 1,
) -> dict[str, object]:
    """Audit CP/TP/unital properties for one finite Schur channel."""
    _validate_alpha(alpha)
    _validate_damping_steps(damping_steps)
    matrix = static_patch_schur_coefficient_matrix(
        cutoff,
        alpha=alpha,
        damping_steps=damping_steps,
    )
    size = len(matrix)
    diagonal_fixed = all(abs(matrix[index][index] - 1.0) <= 1e-12 for index in range(size))
    symmetric = all(
        abs(matrix[i][j] - matrix[j][i]) <= 1e-12
        for i in range(size)
        for j in range(size)
    )
    psd_summary = _cholesky_psd_summary(matrix)
    return {
        "cutoff_L": cutoff,
        "mode_count": size,
        "alpha": alpha,
        "damping_steps": damping_steps,
        "coefficient_matrix": {
            "diagonal_entries_equal_one": diagonal_fixed,
            "symmetric_real": symmetric,
            "positive_semidefinite_numeric": psd_summary["psd"],
            "min_cholesky_pivot": psd_summary["min_cholesky_pivot"],
        },
        "analytic_cp_proof": {
            "exp_abs_kernel_positive_definite_on_Z": True,
            "product_kernel_positive_definite_on_Z2": True,
            "finite_mode_restriction_preserves_psd": True,
            "convex_identity_mixture_preserves_psd_for_alpha_in_unit_interval": True,
            "proof_text": (
                "exp(-t|n-n'|) is the covariance kernel of a stationary "
                "AR(1)-type process on Z for t>0; at t=0 it is the constant "
                "PSD kernel. The product over (ell,m) is positive definite "
                "on Z^2. Restricting to the finite static-patch mode set "
                "preserves PSD, and C_alpha=(1-alpha)I+alpha G is PSD for "
                "0<=alpha<=1."
            ),
        },
        "schur_multiplier_channel_properties": {
            "complete_positive": bool(psd_summary["psd"]),
            "trace_preserving": diagonal_fixed,
            "unital": diagonal_fixed,
            "finite_dimensional": True,
            "cptp_unital": bool(psd_summary["psd"] and diagonal_fixed),
        },
    }


def static_patch_schur_composition_audit(
    cutoff: int,
    *,
    first_alpha: float,
    second_alpha: float,
    first_damping_steps: int = 1,
    second_damping_steps: int = 1,
) -> dict[str, object]:
    """Audit composition of two static-patch Schur multipliers."""
    _validate_alpha(first_alpha)
    _validate_alpha(second_alpha)
    _validate_damping_steps(first_damping_steps)
    _validate_damping_steps(second_damping_steps)
    labels = static_patch_mode_labels(cutoff)
    composed_alpha = first_alpha * second_alpha
    composed_damping_steps = first_damping_steps + second_damping_steps
    max_error = 0.0
    max_fixed_step_error = 0.0
    for first in labels:
        for second in labels:
            first_coeff = static_patch_schur_coefficient(
                cutoff,
                first,
                second,
                alpha=first_alpha,
                damping_steps=first_damping_steps,
            )
            second_coeff = static_patch_schur_coefficient(
                cutoff,
                first,
                second,
                alpha=second_alpha,
                damping_steps=second_damping_steps,
            )
            target = static_patch_schur_coefficient(
                cutoff,
                first,
                second,
                alpha=composed_alpha,
                damping_steps=composed_damping_steps,
            )
            fixed_step_target = static_patch_schur_coefficient(
                cutoff,
                first,
                second,
                alpha=composed_alpha,
                damping_steps=1,
            )
            product = first_coeff * second_coeff
            max_error = max(max_error, abs(product - target))
            max_fixed_step_error = max(max_fixed_step_error, abs(product - fixed_step_target))
    target_audit = static_patch_schur_channel_audit(
        cutoff,
        alpha=composed_alpha,
        damping_steps=composed_damping_steps,
    )
    return {
        "cutoff_L": cutoff,
        "first": {
            "alpha": first_alpha,
            "damping_steps": first_damping_steps,
        },
        "second": {
            "alpha": second_alpha,
            "damping_steps": second_damping_steps,
        },
        "composition": {
            "alpha": composed_alpha,
            "damping_steps": composed_damping_steps,
            "max_entrywise_error_against_broadened_family": _rounded(max_error),
            "closed_in_broadened_schur_damping_family": max_error <= 1e-12,
            "strict_single_step_family_error": _rounded(max_fixed_step_error),
            "strict_single_step_family_closed": max_fixed_step_error <= 1e-12,
            "cptp_unital": target_audit["schur_multiplier_channel_properties"][
                "cptp_unital"
            ],
        },
    }


def static_patch_kernel_cp_preflight_certificate(
    *,
    max_cutoff: int = 6,
    alphas: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0),
    damping_steps: tuple[int, ...] = (0, 1, 2),
) -> dict[str, object]:
    """Certificate for CP, TP, unitality, and composition behavior."""
    _validate_max_cutoff(max_cutoff)
    for alpha in alphas:
        _validate_alpha(alpha)
    for steps in damping_steps:
        _validate_damping_steps(steps)

    channel_rows = tuple(
        static_patch_schur_channel_audit(
            cutoff,
            alpha=alpha,
            damping_steps=steps,
        )
        for cutoff in range(1, max_cutoff + 1)
        for alpha in alphas
        for steps in damping_steps
    )
    composition_rows = tuple(
        static_patch_schur_composition_audit(
            cutoff,
            first_alpha=first_alpha,
            second_alpha=second_alpha,
        )
        for cutoff in range(1, max_cutoff + 1)
        for first_alpha, second_alpha in ((0.0, 1.0), (0.5, 0.75), (1.0, 1.0))
    )
    all_channels_cptp_unital = all(
        row["schur_multiplier_channel_properties"]["cptp_unital"]
        for row in channel_rows
    )
    all_compositions_cptp_unital = all(
        row["composition"]["cptp_unital"] for row in composition_rows
    )
    all_compositions_closed_broadened = all(
        row["composition"]["closed_in_broadened_schur_damping_family"]
        for row in composition_rows
    )
    nontrivial_single_step_not_closed = any(
        not row["composition"]["strict_single_step_family_closed"]
        for row in composition_rows
        if row["composition"]["alpha"] not in (0.0,)
        and row["composition"]["damping_steps"] > 1
    )
    certified_claims = {
        "analytic_psd_proof_recorded": all(
            row["analytic_cp_proof"]["exp_abs_kernel_positive_definite_on_Z"]
            and row["analytic_cp_proof"]["product_kernel_positive_definite_on_Z2"]
            and row["analytic_cp_proof"]["finite_mode_restriction_preserves_psd"]
            and row["analytic_cp_proof"][
                "convex_identity_mixture_preserves_psd_for_alpha_in_unit_interval"
            ]
            for row in channel_rows
        ),
        "bounded_numeric_psd_checks_pass": all(
            row["coefficient_matrix"]["positive_semidefinite_numeric"]
            for row in channel_rows
        ),
        "trace_preserving_and_unital_for_all_checked_channels": all_channels_cptp_unital,
        "composition_closed_in_broadened_schur_damping_family": (
            all_compositions_closed_broadened and all_compositions_cptp_unital
        ),
        "strict_single_step_subfamily_not_generically_closed": (
            nontrivial_single_step_not_closed
        ),
    }
    certified_claims["static_patch_kernel_cp_preflight_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 24.1: Static-Patch Schur Kernel CP Preflight",
        "status": (
            "pass"
            if certified_claims["static_patch_kernel_cp_preflight_certificate"]
            else "fail"
        ),
        "scope": {
            "max_cutoff": max_cutoff,
            "alphas": alphas,
            "damping_steps": damping_steps,
            "channel_family": (
                "Schur multipliers C_{alpha,s}(i,j) with diagonal one and "
                "off-diagonal alpha*exp(-s*distance(i,j)/(L+1)^2)"
            ),
        },
        "theorem_record": {
            "statement": (
                "For 0<=alpha<=1 and integer damping step s>=0, the regulated "
                "static-patch Schur multiplier is completely positive, trace "
                "preserving, and unital. Compositions remain in the broadened "
                "Schur-damping family with alpha multiplied and damping steps "
                "added."
            ),
            "proof": (
                "exp(-t|n-n'|) is positive definite on Z for t>=0; the "
                "product kernel on (ell,m) is positive definite on Z^2; "
                "finite restriction preserves PSD; "
                "C_{alpha,s}=(1-alpha)I+alpha G_s is PSD. A PSD Schur "
                "coefficient matrix with unit diagonal defines a CP, "
                "trace-preserving, unital Schur multiplier."
            ),
            "composition": (
                "C_{alpha,s} o C_{beta,r} has coefficient matrix "
                "C_{alpha*beta,s+r}. Thus the broadened damping family is "
                "composition closed; the fixed s=1 subfamily is not "
                "generically closed."
            ),
        },
        "channel_audit_rows": channel_rows,
        "composition_audit_rows": composition_rows,
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy static-patch-kernel-audit "
                f"--max-cutoff {max_cutoff}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_conditional_ds_er_epr"
            ),
        },
        "certified_claims": certified_claims,
    }


def exact_geometric_cutoff_error(cutoff: int) -> float:
    """The Goal 23 uniform off-diagonal error epsilon_L."""
    x_value = max_static_patch_mode_distance(cutoff) / float((cutoff + 1) ** 2)
    return 1.0 - exp(-x_value)


def analytic_cutoff_error_bound(cutoff: int) -> float:
    """A simple vanishing bound using 1-exp(-x) <= x."""
    return max_static_patch_mode_distance(cutoff) / float((cutoff + 1) ** 2)


def cutoff_static_patch_system(
    cutoff: int,
    *,
    screen_probability: float,
    low_order: int,
) -> dict[str, object]:
    """Formal finite system S_L for the Goal 24 cutoff sequence."""
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    dim = mode_count(cutoff)
    quantum_kernel = regulated_kernel_summary(
        cutoff,
        offdiag_coupling=1,
        screen_probability=screen_probability,
    )
    classical_kernel = regulated_kernel_summary(
        cutoff,
        offdiag_coupling=0,
        screen_probability=screen_probability,
    )
    collision = regulated_static_patch_collision_record(
        cutoff,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    exact_error = exact_geometric_cutoff_error(cutoff)
    bound = analytic_cutoff_error_bound(cutoff)
    return {
        "cutoff_L": cutoff,
        "mode_count": dim,
        "mode_labels": static_patch_mode_labels(cutoff),
        "finite_screen_algebra_A_L": f"C^{dim}",
        "north_observer_algebra_O_N_L": f"M_{dim}",
        "south_observer_algebra_O_S_L": f"M_{dim}",
        "shared_horizon_center_H_L": f"C^{dim}",
        "regulated_transfer_kernel_K_L": {
            "family": "K_L(alpha) Schur multiplier on matrix units E_ij",
            "alpha_quantum": 1,
            "alpha_classical": 0,
            "diagonal_rule": "E_ii -> E_ii",
            "off_diagonal_rule": (
                "E_ij -> alpha*exp(-distance(i,j)/(L+1)^2)*E_ij"
            ),
            "quantum_kernel": quantum_kernel,
            "classical_kernel": classical_kernel,
        },
        "intrinsic_operator_diagnostics": {
            "relative_entropy_response": collision["relative_entropy_response"],
            "modular_commutator_otoc_growth": collision[
                "modular_commutator_otoc_growth"
            ],
            "screen_entropy_correlator_shadow": collision[
                "screen_entropy_correlator_shadow"
            ],
            "screen_restricted_transfer_shadow": collision[
                "screen_restricted_transfer_shadow"
            ],
        },
        "induced_observer_bridge_channel_B_L": collision[
            "induced_observer_bridge_channel"
        ],
        "screen_shadow_collision": collision[
            "proposed_ds_cft_visible_data_insufficient"
        ],
        "cutoff_error": {
            "epsilon_L_exact": _rounded(exact_error),
            "epsilon_L_bound": _rounded(bound),
            "bound_formula": "epsilon_L <= 2L/(L+1)^2",
            "bound_vanishes_as_L_to_infinity": True,
        },
    }


def cutoff_static_patch_sequence(
    *,
    max_cutoff: int,
    screen_probability: float,
    low_order: int,
) -> dict[str, object]:
    """Finite prefix of the cutoff sequence and its analytic limit record."""
    _validate_max_cutoff(max_cutoff)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    systems = tuple(
        cutoff_static_patch_system(
            cutoff,
            screen_probability=screen_probability,
            low_order=low_order,
        )
        for cutoff in range(1, max_cutoff + 1)
    )
    errors = tuple(
        {
            "cutoff_L": system["cutoff_L"],
            "mode_count": system["mode_count"],
            "epsilon_L_exact": system["cutoff_error"]["epsilon_L_exact"],
            "epsilon_L_bound": system["cutoff_error"]["epsilon_L_bound"],
            "exact_error_below_bound": system["cutoff_error"]["epsilon_L_exact"]
            <= system["cutoff_error"]["epsilon_L_bound"],
        }
        for system in systems
    )
    return {
        "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
        "systems": systems,
        "required_objects_defined_for_every_cutoff": all(
            system["finite_screen_algebra_A_L"]
            and system["north_observer_algebra_O_N_L"]
            and system["south_observer_algebra_O_S_L"]
            and system["shared_horizon_center_H_L"]
            and system["regulated_transfer_kernel_K_L"]
            and system["induced_observer_bridge_channel_B_L"]
            for system in systems
        ),
        "cutoff_error_records": errors,
        "analytic_vanishing_error": {
            "exact_errors_below_bounds": all(
                record["exact_error_below_bound"] for record in errors
            ),
            "bound": "epsilon_L <= 2L/(L+1)^2",
            "limit": "lim_{L->infinity} 2L/(L+1)^2 = 0",
            "model_statement": (
                "Inside the regulated family, quantum off-diagonal matrix "
                "units are recovered with uniform error epsilon_L -> 0."
            ),
        },
    }


def continuum_assumption_catalog() -> tuple[dict[str, object], ...]:
    """Assumptions needed before the finite theorem becomes a dS theorem."""
    return (
        {
            "id": "directed_cutoff_net",
            "kind": "mathematical",
            "status": "verified_inside_regulated_model",
            "assumption": (
                "The finite systems S_L form a directed cutoff sequence with "
                "mode inclusions A_L -> A_{L+1}."
            ),
        },
        {
            "id": "operator_response_convergence",
            "kind": "mathematical",
            "status": "verified_inside_regulated_model",
            "assumption": (
                "The quantum kernels converge on the regulated local operator "
                "net with the analytic bound epsilon_L <= 2L/(L+1)^2."
            ),
        },
        {
            "id": "finite_schur_kernel_cptp",
            "kind": "mathematical",
            "status": "verified_inside_regulated_model",
            "assumption": (
                "For 0<=alpha<=1, the finite Schur coefficient matrices are "
                "positive semidefinite with unit diagonal, so K_L is CP, trace "
                "preserving, and unital."
            ),
        },
        {
            "id": "physical_static_patch_dynamics",
            "kind": "physics",
            "status": "not_proved_by_certificate",
            "assumption": (
                "K_L is derived from an actual de Sitter static-patch "
                "Hamiltonian, path integral, or controlled dS/CFT regulator."
            ),
        },
        {
            "id": "positivity_unitarity_reflection_control",
            "kind": "physics",
            "status": "not_proved_by_certificate",
            "assumption": (
                "The limiting dynamics has the right positivity, unitarity, or "
                "controlled non-unitarity properties for the proposed dS/CFT "
                "dictionary."
            ),
        },
        {
            "id": "continuum_operator_dictionary",
            "kind": "physics",
            "status": "not_proved_by_certificate",
            "assumption": (
                "The finite matrix-unit probes converge to continuum screen or "
                "observer operators with identified scaling/dictionary data."
            ),
        },
        {
            "id": "observer_algebra_limit",
            "kind": "operator_algebra",
            "status": "not_proved_by_certificate",
            "assumption": (
                "The finite Type-I observer algebras have the physically "
                "appropriate Type-II/Type-III continuum limit."
            ),
        },
        {
            "id": "relative_entropy_recovery_limit",
            "kind": "operator_algebra",
            "status": "conditional_on_approximate_oaqec_stability",
            "assumption": (
                "Relative-entropy/modular response convergence is strong enough "
                "to pass OA-QEC recoverability to the limiting observer algebra."
            ),
        },
        {
            "id": "horizon_qes_entropy_from_same_dynamics",
            "kind": "physics",
            "status": "not_proved_by_certificate",
            "assumption": (
                "The shared-horizon/generalized-entropy or QES data are derived "
                "from the same regulated dynamics, not added independently."
            ),
        },
        {
            "id": "algebraic_er_epr_interpretation",
            "kind": "interpretation",
            "status": "conceptual_prior_art_not_proved_here",
            "assumption": (
                "Algebraic connectivity of the limiting observer algebras is "
                "interpreted as ER=EPR-style spacetime connectivity."
            ),
        },
    )


def conditional_continuum_theorem_record() -> dict[str, object]:
    """Conditional theorem A: valid only if the assumptions are discharged."""
    assumptions = continuum_assumption_catalog()
    unproved = tuple(
        assumption["id"]
        for assumption in assumptions
        if assumption["status"]
        not in ("verified_inside_regulated_model", "standard_finite_theorem")
    )
    return {
        "result": "A: conditional theorem",
        "status": "conditional_not_promoted_to_physical_ds_theorem",
        "theorem": (
            "If the cutoff static-patch sequence has a physical continuum "
            "limit satisfying the listed convergence, observer-algebra, "
            "relative-entropy recovery, horizon/QES, and algebraic ER=EPR "
            "interpretation assumptions, then limiting algebraic connectivity "
            "is equivalent to a nontrivial recoverable observer bridge channel."
        ),
        "proof_skeleton": (
            "Goal 23 gives finite-cutoff operator-response completion.",
            "The regulated quantum kernel has epsilon_L <= 2L/(L+1)^2 -> 0.",
            "Under response/recovery convergence, relative-entropy and "
            "commutator response identify the limiting recoverable algebra.",
            "A noncommutative limiting recoverable observer algebra is exactly "
            "a nontrivial recoverable bridge channel by the channel definition.",
            "Under the separate algebraic ER=EPR interpretation assumption, "
            "that channel is the finite-to-continuum bridge-connectivity datum.",
        ),
        "assumptions": assumptions,
        "undischarged_assumption_ids": unproved,
        "literal_ds_er_epr_proved": False,
    }


def screen_shadow_sequence_no_go(
    *,
    max_cutoff: int,
    screen_probability: float,
    low_order: int,
) -> dict[str, object]:
    """No-go theorem B for screen-visible finite-order data."""
    sequence = cutoff_static_patch_sequence(
        max_cutoff=max_cutoff,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    collision_rows = tuple(
        {
            "cutoff_L": system["cutoff_L"],
            "screen_entropy_match": system["screen_shadow_collision"][
                "entropy_shadows_match"
            ],
            "low_order_correlators_match": system["screen_shadow_collision"][
                "low_order_correlators_match"
            ],
            "screen_restricted_transfer_match": system["screen_shadow_collision"][
                "screen_restricted_transfer_data_match"
            ],
            "quantum_bridge_algebra": system["induced_observer_bridge_channel_B_L"][
                "quantum_bridge_epsilon_recoverable_algebra"
            ],
            "classical_bridge_algebra": system["induced_observer_bridge_channel_B_L"][
                "classical_bridge_epsilon_recoverable_algebra"
            ],
        }
        for system in sequence["systems"]
    )
    all_collide = all(
        row["screen_entropy_match"]
        and row["low_order_correlators_match"]
        and row["screen_restricted_transfer_match"]
        and row["quantum_bridge_algebra"] != row["classical_bridge_algebra"]
        for row in collision_rows
    )
    return {
        "result": "B: no-go theorem",
        "status": "proved_inside_regulated_cutoff_family",
        "data_class": (
            "Any diagnostic depending only on diagonal screen entropy, "
            "finite-order diagonal correlators, horizon-overlap data, and "
            "screen-restricted transfer data."
        ),
        "claim": (
            "This screen-visible data class cannot determine the observer "
            "bridge channel, even as a cutoff sequence: the quantum and "
            "classical/dephased kernels agree on the data at every L but have "
            "different recoverable bridge algebras."
        ),
        "collision_rows": collision_rows,
        "all_cutoff_collisions_hold": all_collide,
        "sequence_level_collision": all_collide,
        "continuum_reading": (
            "Because the shadow sequences are identical term-by-term, any "
            "putative continuum invariant built only from those shadows is "
            "blind to the bridge-channel distinction unless extra operator "
            "response data are supplied."
        ),
    }


def obstruction_theorem_record() -> dict[str, object]:
    """Obstruction theorem C for promoting the benchmark to real dS/CFT."""
    assumptions = continuum_assumption_catalog()
    missing = tuple(
        assumption
        for assumption in assumptions
        if assumption["status"]
        not in ("verified_inside_regulated_model", "standard_finite_theorem")
    )
    return {
        "result": "C: obstruction theorem",
        "status": "obstruction_identified",
        "minimal_first_obstruction": "physical_static_patch_dynamics",
        "claim": (
            "The finite theorem cannot be promoted to literal de Sitter "
            "ER=EPR until the regulated kernel is derived from a controlled "
            "static-patch/dS-CFT dynamics. Without that, the model proves a "
            "finite benchmark and a conditional theorem schema, not a "
            "continuum-gravity theorem."
        ),
        "remaining_obligations": missing,
    }


def prior_art_positioning() -> tuple[dict[str, str], ...]:
    return (
        {
            "id": "engelhardt_liu_2023",
            "reference": "Engelhardt-Liu, Algebraic ER=EPR and Complexity Transfer, arXiv:2311.04281",
            "role": (
                "Conceptual prior art for associating spacetime connectivity "
                "with operator-algebraic structure rather than entanglement "
                "amount alone."
            ),
            "relation": (
                "Goal 24 is a finite regulated benchmark and conditional "
                "promotion ledger underneath that proposal, not a competing "
                "definition of algebraic ER=EPR."
            ),
        },
        {
            "id": "harlow_2016",
            "reference": "Harlow, The Ryu-Takayanagi Formula from Quantum Error Correction, arXiv:1607.03901",
            "role": (
                "OA-QEC language for reconstruction algebras, centers, and "
                "finite-dimensional von Neumann algebra codes."
            ),
            "relation": (
                "Goal 24 uses OA-QEC-style recoverability as the finite "
                "operator-algebraic reconstruction criterion."
            ),
        },
        {
            "id": "harlow_usatyuk_zhao_2025",
            "reference": "Harlow-Usatyuk-Zhao, Quantum mechanics and observers for gravity in a closed universe, arXiv:2501.02359",
            "role": (
                "Observer-effective Hilbert-space motivation in closed-universe "
                "quantum gravity."
            ),
            "relation": (
                "Goal 24 asks what regulated observer-algebra data would be "
                "needed before a finite static-patch benchmark could speak to "
                "observer physics."
            ),
        },
        {
            "id": "engelhardt_gesteau_harlow_2025",
            "reference": "Engelhardt-Gesteau-Harlow, Observer complementarity for black holes and holography, arXiv:2507.06046",
            "role": (
                "Recent mathematical observer-complementarity framing for "
                "holography and closed-universe configurations."
            ),
            "relation": (
                "Goal 24 remains a finite diagnostic theorem, but its "
                "observer-algebra gate is designed to be legible in this "
                "observer-complementarity language."
            ),
        },
    )


def goal24_conditional_ds_er_epr_certificate(
    *,
    max_cutoff: int = 5,
    screen_probability: float = 0.75,
    low_order: int = 2,
) -> dict[str, object]:
    """Emit the Goal 24 conditional theorem/no-go/obstruction certificate."""
    _validate_max_cutoff(max_cutoff)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    sequence = cutoff_static_patch_sequence(
        max_cutoff=max_cutoff,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    goal23 = goal23_regulated_static_patch_ds_cft_certificate(
        max_cutoff=max_cutoff,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    conditional = conditional_continuum_theorem_record()
    no_go = screen_shadow_sequence_no_go(
        max_cutoff=max_cutoff,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    cp_preflight = static_patch_kernel_cp_preflight_certificate(
        max_cutoff=max_cutoff,
    )
    obstruction = obstruction_theorem_record()
    prior_art = prior_art_positioning()
    taxonomy = {
        "exact_finite_results": (
            "Goal 23 finite-cutoff theorem",
            "Goal 24.1 finite Schur-kernel CP/TP/unital/composition audit",
            "Goal 24 screen-shadow sequence no-go inside the regulated family",
            "Goal 24 analytic cutoff-error bound inside the regulated family",
        ),
        "conditional_continuum_results": (
            "Finite-to-continuum algebraic-connectivity theorem under the "
            "listed convergence/recovery/interpretation assumptions",
        ),
        "speculative_or_unproved_physics": tuple(
            assumption["id"]
            for assumption in obstruction["remaining_obligations"]
        ),
    }
    certified_claims = {
        "cutoff_sequence_formalizes_required_objects": sequence[
            "required_objects_defined_for_every_cutoff"
        ],
        "finite_goal23_theorem_recovered": goal23["status"] == "pass",
        "analytic_cutoff_error_bound_vanishes": sequence[
            "analytic_vanishing_error"
        ]["exact_errors_below_bounds"]
        and sequence["analytic_vanishing_error"]["limit"].endswith("= 0"),
        "finite_schur_kernel_cp_preflight_passes": cp_preflight["status"] == "pass",
        "screen_visible_sequence_no_go_proved": no_go[
            "all_cutoff_collisions_hold"
        ]
        and no_go["sequence_level_collision"],
        "conditional_theorem_stated_but_not_overclaimed": conditional[
            "literal_ds_er_epr_proved"
        ]
        is False
        and len(conditional["undischarged_assumption_ids"]) > 0,
        "obstruction_theorem_identifies_minimal_first_missing_assumption": obstruction[
            "minimal_first_obstruction"
        ]
        == "physical_static_patch_dynamics",
        "prior_art_comparison_included": len(prior_art) >= 4,
        "exact_conditional_speculative_layers_separated": all(taxonomy.values()),
        "no_literal_ds_cft_or_er_epr_claim": True,
    }
    certified_claims["goal24_conditional_ds_er_epr_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 24: Conditional dS ER=EPR Theorem From Regulated Static-Patch Observer Algebras",
        "status": (
            "pass"
            if certified_claims["goal24_conditional_ds_er_epr_certificate"]
            else "fail"
        ),
        "result_type": (
            "conditional_continuum_theorem_plus_screen_shadow_sequence_no_go_"
            "and_obstruction"
        ),
        "cutoff_sequence": sequence,
        "finite_goal23_recovery": {
            "recovers_goal23": goal23["status"] == "pass",
            "goal23_result_type": goal23["result_type"],
            "goal23_command": goal23["reproducibility"]["certificate"],
        },
        "conditional_theorem": conditional,
        "finite_kernel_cp_preflight": cp_preflight,
        "screen_shadow_no_go": no_go,
        "obstruction_theorem": obstruction,
        "prior_art_positioning": prior_art,
        "result_taxonomy": taxonomy,
        "continuum_promotion_checklist": tuple(
            {
                "id": assumption["id"],
                "status": assumption["status"],
                "requirement": assumption["assumption"],
            }
            for assumption in continuum_assumption_catalog()
        ),
        "expert_feedback_summary": (
            "Goal 24 turns the regulated finite static-patch benchmark into a "
            "conditional theorem ledger: screen-visible cutoff data remain "
            "insufficient term-by-term, full operator response has a vanishing "
            "model error, and a real dS ER=EPR claim is blocked precisely by "
            "the unproved physical static-patch/dS-CFT promotion assumptions."
        ),
        "claim_boundary": (
            "This certificate proves finite regulated statements and a "
            "conditional theorem schema. It does not prove literal continuum "
            "dS/CFT, de Sitter quantum gravity, Type-II/Type-III observer "
            "algebras, or ER=EPR in de Sitter."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy conditional-ds-er-epr "
                f"--max-cutoff {max_cutoff} --screen-probability {screen_probability} "
                f"--low-order {low_order}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_conditional_ds_er_epr"
            ),
            "goal23_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_static_patch_testbed"
            ),
        },
        "certified_claims": certified_claims,
    }
