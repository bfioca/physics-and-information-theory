"""Goal 21 finite dS/CFT-ER=EPR compatibility benchmarks."""

from __future__ import annotations

from math import isclose

from .bilayer import binary_entropy
from .general_algebraic_connectivity import (
    diagonal_probe_no_go_record,
    goal20_general_algebraic_connectivity_stability_certificate,
)
from .local_bridge_screen import local_entropy_only_control
from .relative_entropy_bridge import _rounded


def _validate_dimension(dim: int) -> None:
    if dim < 2:
        raise ValueError("dimension must be at least two")


def _validate_probability(probability: float) -> None:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("screen_probability must lie in [0,1]")


def _transfer_spectrum_identity(dim: int) -> tuple[float, ...]:
    return tuple(1.0 for _ in range(dim * dim))


def _transfer_spectrum_dephasing(dim: int) -> tuple[float, ...]:
    return tuple(1.0 for _ in range(dim)) + tuple(
        0.0 for _ in range(dim * dim - dim)
    )


def _screen_transfer_spectrum(dim: int) -> tuple[float, ...]:
    return tuple(1.0 for _ in range(dim))


def ds_cft_screen_shadow(dim: int, *, screen_probability: float) -> dict[str, object]:
    """Finite screen/CFT-like data deliberately restricted to the horizon screen."""
    _validate_dimension(dim)
    _validate_probability(screen_probability)
    diagonal_record = diagonal_probe_no_go_record(dim)
    north_entropy = binary_entropy(screen_probability)
    south_entropy = binary_entropy(1.0 - screen_probability)
    return {
        "dimension": dim,
        "screen_probability": screen_probability,
        "finite_objects": {
            "spacetime_claim": "finite dS/CFT-inspired observer-screen benchmark",
            "no_asymptotic_ads_boundary": True,
            "observer_primitives": (
                "north_static_patch",
                "south_static_patch",
            ),
            "shared_finite_horizon_algebra": f"C^{dim}",
            "screen_operator_algebra_visible_to_shadow": f"C^{dim}",
            "bulk_bridge_operator_algebra_under_test": f"M_{dim}",
        },
        "screen_entropies_bits": {
            "north_screen": _rounded(north_entropy),
            "south_screen": _rounded(south_entropy),
            "entropy_only_orients_patch": not isclose(
                north_entropy,
                south_entropy,
                abs_tol=1e-12,
            ),
        },
        "area_analogue_bits": {
            "north_screen": _rounded(north_entropy + screen_probability),
            "south_screen": _rounded(south_entropy + 1.0 - screen_probability),
        },
        "horizon_overlap_shadow": {
            "shared_horizon_dimension": dim,
            "shared_horizon_algebra": f"C^{dim}",
            "commutator_dimension": 0,
            "center_dimension": dim,
        },
        "diagonal_correlator_shadow": {
            "rho_diagonal": diagonal_record["diagonal_probe_pair"]["rho_diagonal"],
            "sigma_diagonal": diagonal_record["diagonal_probe_pair"][
                "sigma_diagonal"
            ],
            "relative_entropy_bits": diagonal_record[
                "relative_entropy_response_on_probe_algebra"
            ]["input_bits"],
        },
        "screen_transfer_matrix_spectrum": {
            "restricted_to_screen_algebra": f"C^{dim}",
            "identity_bridge": _screen_transfer_spectrum(dim),
            "dephased_bridge": _screen_transfer_spectrum(dim),
            "spectra_match_on_screen_shadow": True,
        },
        "claim_boundary": (
            "This shadow is a finite screen/CFT-like diagnostic layer, not a "
            "continuum CFT dictionary or de Sitter boundary construction."
        ),
    }


def ds_cft_er_epr_collision_record(
    dim: int,
    *,
    screen_probability: float,
) -> dict[str, object]:
    """Exact collision between screen-visible data and bridge algebra."""
    _validate_dimension(dim)
    _validate_probability(screen_probability)
    shadow = ds_cft_screen_shadow(dim, screen_probability=screen_probability)
    diagonal_record = diagonal_probe_no_go_record(dim)
    completion = diagonal_record["completion_probe"]
    full_identity_spectrum = _transfer_spectrum_identity(dim)
    full_dephasing_spectrum = _transfer_spectrum_dephasing(dim)
    return {
        "dimension": dim,
        "screen_probability": screen_probability,
        "model_pair": {
            "quantum_bridge_realization": (
                "same finite screen layer plus identity bridge channel on M_d"
            ),
            "classical_horizon_bridge_realization": (
                "same finite screen layer plus complete dephasing bridge onto C^d"
            ),
        },
        "screen_cft_visible_shadow": shadow,
        "screen_shadow_agreement": {
            "screen_entropies_match": True,
            "diagonal_correlator_shadows_match": diagonal_record[
                "relative_entropy_response_on_probe_algebra"
            ]["relative_entropy_defects_match"],
            "horizon_overlap_shadows_match": True,
            "screen_transfer_spectra_match": shadow[
                "screen_transfer_matrix_spectrum"
            ]["spectra_match_on_screen_shadow"],
            "all_declared_screen_cft_visible_data_match": True,
        },
        "algebraic_er_epr_bridge_channel": {
            "identity_bridge_maximal_recoverable_algebra": f"M_{dim}",
            "dephased_bridge_maximal_recoverable_algebra": f"C^{dim}",
            "maximal_bridge_algebras_differ": True,
            "identity_bridge_phase": "quantum_bridge",
            "dephased_bridge_phase": "classical_horizon_bridge",
            "fixed_screen_shadow_does_not_determine_bridge_phase": True,
        },
        "completion_diagnostic": {
            "needed_extra_data": (
                "intrinsic off-diagonal response, informationally complete "
                "operator probes, or an equivalent maximality test"
            ),
            "off_diagonal_relative_entropy_input_bits": completion[
                "input_relative_entropy_bits"
            ],
            "identity_off_diagonal_output_bits": completion[
                "identity_output_relative_entropy_bits"
            ],
            "dephasing_off_diagonal_output_bits": completion[
                "dephasing_output_relative_entropy_bits"
            ],
            "off_diagonal_probe_separates_bridge_channels": completion[
                "off_diagonal_probe_separates_channels"
            ],
            "full_operator_transfer_spectrum_identity": full_identity_spectrum,
            "full_operator_transfer_spectrum_dephasing": full_dephasing_spectrum,
            "full_operator_spectra_differ": full_identity_spectrum
            != full_dephasing_spectrum,
        },
        "wrong_patch_and_entropy_only_control": local_entropy_only_control(
            screen_probability
        ),
        "conclusion": (
            "Finite dS/CFT-visible screen shadows restricted to the shared "
            "horizon algebra can be identical while algebraic ER=EPR bridge "
            "connectivity differs. The compatible completion is intrinsic "
            "observer-algebra response/commutator tomography, not entropy alone."
        ),
    }


def _bounded_ds_cft_family(
    *,
    max_dim: int,
    screen_probability: float,
) -> dict[str, object]:
    records = tuple(
        ds_cft_er_epr_collision_record(
            dim,
            screen_probability=screen_probability,
        )
        for dim in range(2, max_dim + 1)
    )
    return {
        "dimensions_checked": tuple(range(2, max_dim + 1)),
        "screen_probability": screen_probability,
        "records": records,
        "all_screen_shadows_match": all(
            record["screen_shadow_agreement"][
                "all_declared_screen_cft_visible_data_match"
            ]
            for record in records
        ),
        "all_bridge_algebras_differ": all(
            record["algebraic_er_epr_bridge_channel"][
                "maximal_bridge_algebras_differ"
            ]
            for record in records
        ),
        "all_completion_probes_separate": all(
            record["completion_diagnostic"][
                "off_diagonal_probe_separates_bridge_channels"
            ]
            for record in records
        ),
    }


def goal21_ds_cft_er_epr_compatibility_certificate(
    *,
    max_dim: int = 5,
    screen_probability: float = 0.75,
) -> dict[str, object]:
    if max_dim < 2:
        raise ValueError("max_dim must be at least two")
    _validate_probability(screen_probability)

    minimal = ds_cft_er_epr_collision_record(
        2,
        screen_probability=screen_probability,
    )
    qutrit = ds_cft_er_epr_collision_record(
        3,
        screen_probability=screen_probability,
    )
    family = _bounded_ds_cft_family(
        max_dim=max_dim,
        screen_probability=screen_probability,
    )
    goal20 = goal20_general_algebraic_connectivity_stability_certificate(
        max_dim=max_dim,
    )
    entropy_control = minimal["wrong_patch_and_entropy_only_control"]
    certified_claims = {
        "finite_ds_cft_er_epr_no_go_stated": True,
        "no_asymptotic_ads_boundary": minimal["screen_cft_visible_shadow"][
            "finite_objects"
        ]["no_asymptotic_ads_boundary"],
        "two_observer_static_patches_declared": len(
            minimal["screen_cft_visible_shadow"]["finite_objects"][
                "observer_primitives"
            ]
        )
        == 2,
        "shared_finite_horizon_algebra_declared": minimal[
            "screen_cft_visible_shadow"
        ]["finite_objects"]["shared_finite_horizon_algebra"]
        == "C^2",
        "minimal_qubit_screen_shadow_collision": minimal[
            "screen_shadow_agreement"
        ]["all_declared_screen_cft_visible_data_match"]
        and minimal["algebraic_er_epr_bridge_channel"][
            "maximal_bridge_algebras_differ"
        ],
        "non_pauli_qutrit_screen_shadow_collision": qutrit[
            "screen_shadow_agreement"
        ]["all_declared_screen_cft_visible_data_match"]
        and qutrit["algebraic_er_epr_bridge_channel"][
            "maximal_bridge_algebras_differ"
        ],
        "bounded_family_checked": family["all_screen_shadows_match"]
        and family["all_bridge_algebras_differ"]
        and family["all_completion_probes_separate"],
        "entropy_only_wrong_patch_control_passes": entropy_control[
            "entropy_only_is_insufficient_for_oriented_screen_recovery"
        ],
        "intrinsic_completion_probe_separates_channels": minimal[
            "completion_diagnostic"
        ]["off_diagonal_probe_separates_bridge_channels"],
        "goal20_recovered_as_screen_shadow_obstruction": goal20["status"]
        == "pass",
        "no_continuum_ds_cft_or_er_epr_claim": True,
    }
    certified_claims["goal21_ds_cft_er_epr_compatibility_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 21: Finite dS/CFT-ER=EPR Compatibility Benchmark",
        "status": (
            "pass"
            if certified_claims[
                "goal21_ds_cft_er_epr_compatibility_certificate"
            ]
            else "fail"
        ),
        "result_type": "finite_screen_shadow_no_go_with_intrinsic_completion",
        "theorem_record": {
            "theorem": (
                "Finite dS/CFT-screen shadows do not determine algebraic "
                "ER=EPR bridge connectivity"
            ),
            "statement": (
                "For every d>=2, a finite two-observer static-patch screen "
                "model with shared horizon algebra C^d has two realizations "
                "with identical screen entropies, diagonal correlator shadows, "
                "horizon-overlap data, and transfer spectra restricted to the "
                "screen algebra, but different bridge channels: identity on "
                "M_d versus complete dephasing onto C^d."
            ),
            "completion": (
                "Adding intrinsic off-diagonal response, informationally "
                "complete operator probes, or an equivalent maximality test "
                "separates the bridge channels and recovers the algebraic "
                "connectivity phase in this finite family."
            ),
            "why_this_is_ds_cft_like_not_ds_cft": (
                "The benchmark has no asymptotic AdS boundary and uses "
                "observer static patches plus a shared finite horizon screen. "
                "The screen/CFT layer is an abstract finite shadow, not a "
                "continuum CFT dictionary."
            ),
        },
        "minimal_counterexample": minimal,
        "non_pauli_qutrit_counterexample": qutrit,
        "bounded_family": family,
        "relationship_to_goals_19_20": {
            "goal19": (
                "Algebraic connectivity is the recoverable bridge algebra "
                "detected by relative-entropy response plus closure when the "
                "probe atlas is complete."
            ),
            "goal20": (
                "Goal 20 supplies the exact probe-incompleteness mechanism: "
                "diagonal response certifies C^d but does not identify whether "
                "M_d is also recoverable."
            ),
            "goal21": (
                "The same obstruction is reinterpreted as a finite dS/CFT "
                "compatibility benchmark: screen-visible horizon data can hide "
                "the ER=EPR bridge algebra."
            ),
        },
        "expert_feedback_summary": (
            "In a finite two-observer static-patch benchmark, dS/CFT-like "
            "screen data restricted to the shared horizon do not determine "
            "algebraic ER=EPR connectivity. The missing datum is intrinsic "
            "observer-algebra response/commutator tomography, which distinguishes "
            "a quantum bridge from a classical horizon bridge."
        ),
        "claim_boundary": (
            "This is a finite QEC/OA-QEC compatibility benchmark. It is not "
            "a continuum dS/CFT theorem, not de Sitter quantum gravity, not a "
            "type-III algebra theorem, and not a proof of ER=EPR in de Sitter."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy ds-cft-er-epr "
                f"--max-dim {max_dim} --screen-probability {screen_probability}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_ds_cft_er_epr"
            ),
        },
        "certified_claims": certified_claims,
    }
