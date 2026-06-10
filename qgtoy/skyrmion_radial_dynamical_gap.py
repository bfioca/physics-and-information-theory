"""Conditional radial normal-mode gap for a hard-supported Skyrmion.

Linear radial fluctuations around a static hedgehog satisfy the generalized
Sturm-Liouville problem

    L_Jacobi eta = omega_hat^2 W eta,
    W=(x^2+8 sin^2(F))/N.

Hard support gives ``W <= (x_w^2+8)/N_w``.  Consequently a lower form bound
``L_Jacobi>=alpha`` on the complete physical radial fluctuation domain implies
``omega_hat_0^2>=alpha N_w/(x_w^2+8)``.  Here ``omega_hat`` is conjugate to
``tau=e f_pi t``, so the static-patch Killing frequency is
``omega_K=e f_pi omega_hat``.  The current AU.1 Barta certificate does not yet
supply the full-domain hypothesis; it controls an approximate-profile,
positive-radius Dirichlet operator used in the nonlinear existence proof.
"""

from __future__ import annotations

from math import isfinite, sin

from .massive_skyrmion_profile import static_patch_lapse


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def radial_fluctuation_kinetic_weight(
    dimensionless_radius: float,
    profile: float,
    *,
    curvature: float,
) -> float:
    """Return ``W=(x^2+8sin^2(F))/N`` for radial hedgehog fluctuations."""
    _validate_nonnegative("dimensionless_radius", dimensionless_radius)
    if not isfinite(profile):
        raise ValueError("profile must be finite")
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(dimensionless_radius, curvature)
    if lapse <= 0.0:
        raise ValueError("radius must lie strictly inside the static-patch horizon")
    return (dimensionless_radius**2 + 8.0 * sin(profile) ** 2) / lapse


def uniform_radial_kinetic_weight_upper_bound(
    *,
    wall_radius: float,
    curvature: float,
) -> float:
    """Return the profile-independent hard-support bound ``(x_w^2+8)/N_w``."""
    _validate_positive("wall_radius", wall_radius)
    _validate_nonnegative("curvature", curvature)
    wall_lapse = static_patch_lapse(wall_radius, curvature)
    if wall_lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    return (wall_radius**2 + 8.0) / wall_lapse


def generalized_radial_frequency_squared_lower_bound(
    *,
    static_jacobi_form_gap: float,
    kinetic_weight_upper_bound: float,
) -> float:
    """Convert ``L>=alpha`` and ``W<=Wmax`` into ``omega_hat^2>=alpha/Wmax``."""
    _validate_nonnegative("static_jacobi_form_gap", static_jacobi_form_gap)
    _validate_positive("kinetic_weight_upper_bound", kinetic_weight_upper_bound)
    return static_jacobi_form_gap / kinetic_weight_upper_bound


def supported_radial_frequency_squared_lower_bound(
    *,
    static_jacobi_form_gap: float,
    wall_radius: float,
    curvature: float,
) -> float:
    """Apply the hard-support kinetic-weight bound to a full-domain form gap."""
    weight_upper = uniform_radial_kinetic_weight_upper_bound(
        wall_radius=wall_radius,
        curvature=curvature,
    )
    return generalized_radial_frequency_squared_lower_bound(
        static_jacobi_form_gap=static_jacobi_form_gap,
        kinetic_weight_upper_bound=weight_upper,
    )


def unbounded_kinetic_weight_counterexample(
    *,
    static_jacobi_form_gap: float,
    kinetic_weight_scale: float,
) -> dict[str, float | str]:
    """Show that a static form gap alone does not determine a frequency gap."""
    _validate_positive("static_jacobi_form_gap", static_jacobi_form_gap)
    _validate_positive("kinetic_weight_scale", kinetic_weight_scale)
    frequency_squared = static_jacobi_form_gap / kinetic_weight_scale
    return {
        "static_jacobi_form_gap": static_jacobi_form_gap,
        "kinetic_weight_scale": kinetic_weight_scale,
        "generalized_frequency_squared": frequency_squared,
        "statement": (
            "The pair L=alpha*identity and W=C*identity has the same static "
            "gap alpha for every C, while omega^2=alpha/C tends to zero. A "
            "kinetic-weight upper bound is an independent dynamical input."
        ),
    }


def skyrmion_radial_dynamical_gap_certificate(
    *,
    wall_radius: float = 4.0,
    curvature: float = 0.0025,
    au1_positive_radius_barta_lower_bound: float = 1.0235900944571767,
) -> dict[str, object]:
    """Audit the conditional radial dynamic-gap conversion and AU.1 mismatch."""
    weight_upper = uniform_radial_kinetic_weight_upper_bound(
        wall_radius=wall_radius,
        curvature=curvature,
    )
    conditional_frequency_squared = supported_radial_frequency_squared_lower_bound(
        static_jacobi_form_gap=au1_positive_radius_barta_lower_bound,
        wall_radius=wall_radius,
        curvature=curvature,
    )
    clean_truncated_frequency_squared = supported_radial_frequency_squared_lower_bound(
        static_jacobi_form_gap=1.0,
        wall_radius=wall_radius,
        curvature=curvature,
    )
    counterexamples = tuple(
        unbounded_kinetic_weight_counterexample(
            static_jacobi_form_gap=1.0,
            kinetic_weight_scale=scale,
        )
        for scale in (1.0, 10.0, 1000.0, 1e6)
    )
    claims = {
        "hard_support_gives_a_finite_profile_independent_weight_bound": (
            isfinite(weight_upper) and weight_upper > 0.0
        ),
        "full_domain_static_gap_would_give_a_positive_radial_frequency_gap": (
            conditional_frequency_squared > 0.0
        ),
        "static_gap_without_weight_control_is_not_a_dynamic_gap": all(
            right["generalized_frequency_squared"]
            < left["generalized_frequency_squared"]
            for left, right in zip(counterexamples, counterexamples[1:])
        ),
        "au1_number_is_not_promoted_beyond_its_certified_domain": True,
    }
    return {
        "goal": "Supported Skyrmion Radial Dynamical Gap Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "conditional_weighted_sturm_liouville_gap_conversion",
        "central_result": (
            "For radial hedgehog fluctuations, L_Jacobi eta=omega_hat^2 W eta "
            "with W=(x^2+8sin^2F)/N. Hard support gives "
            "W<=(x_w^2+8)/N_w, so a full physical-domain static form gap "
            "alpha would imply omega_hat_0^2>=alpha N_w/(x_w^2+8), with "
            "omega_K=e f_pi omega_hat."
        ),
        "parameters": {
            "wall_radius_x_w": wall_radius,
            "curvature_lambda": curvature,
            "wall_lapse_N_w": static_patch_lapse(wall_radius, curvature),
            "au1_positive_radius_barta_lower_bound": (
                au1_positive_radius_barta_lower_bound
            ),
        },
        "kinetic_weight_upper_bound": weight_upper,
        "certified_truncated_approximate_profile_frequency_squared": (
            conditional_frequency_squared
        ),
        "certified_truncated_approximate_profile_frequency": (
            conditional_frequency_squared**0.5
        ),
        "clean_truncated_frequency_squared_from_au1_target_one": (
            clean_truncated_frequency_squared
        ),
        "clean_truncated_frequency_from_au1_target_one": (
            clean_truncated_frequency_squared**0.5
        ),
        "conditional_frequency_squared_if_au1_bound_were_full_domain": (
            conditional_frequency_squared
        ),
        "conditional_frequency_if_au1_bound_were_full_domain": (
            conditional_frequency_squared**0.5
        ),
        "current_evidence": {
            "time_dependent_radial_kinetic_weight": "derived",
            "hard_support_weight_upper_bound": "proved",
            "positive_radius_approximate_profile_dirichlet_gap": "proved by AU.1",
            "exact_solution_tube_barta_robustness": "missing",
            "full_origin_to_wall_physical_form_gap": "missing",
            "coupled_profile_wall_radial_mode_gap": "missing",
            "physical_radial_dynamic_gap": "open",
        },
        "weight_counterexamples": counterexamples,
        "certified_claims": claims,
        "claim_boundary": (
            "The displayed number is certified for AU.1's artificially "
            "truncated approximate-profile Dirichlet operator, and only "
            "conditional as a physical normal-mode gap. AU.1 does not propagate "
            "the Barta quotient through the exact-solution Newton tube, remove "
            "the artificial boundary at x=1/16, or include membrane dynamics."
        ),
    }
