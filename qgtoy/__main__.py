"""Command-line interface for qgtoy."""

from __future__ import annotations

import argparse
import json
from typing import Any

from .algebraic_connectivity import goal19_algebraic_connectivity_order_parameter_certificate
from .axiomatic_static_patch_selection import goal28_axiomatic_static_patch_selection_certificate
from .bridge_proof import bridge_symbolic_proof_check
from .bridge_screen import goal17_inseparable_bridge_screen_dynamics_certificate
from .bilayer import bilayer_reconstruction_program_certificate
from .charged_reference_recovery import charged_reference_recovery_certificate
from .cosmology import (
    bridge_cosmology_phase1_certificate,
    bridge_cosmology_phase2_certificate,
    bridge_cosmology_phase3_certificate,
    bridge_cosmology_phase4_certificate,
    bridge_cosmology_phase5_certificate,
    bridge_cosmology_phase6_certificate,
    bridge_cosmology_phase7_certificate,
    bridge_cosmology_phase8_certificate,
    bridge_cosmology_phase9_certificate,
    bridge_cosmology_phase10_certificate,
    bridge_cosmology_phase11_certificate,
    bridge_cosmology_phase12_certificate,
    bridge_cosmology_phase13_certificate,
    bridge_cosmology_phase14_certificate,
    bridge_cosmology_phase15_certificate,
    bridge_cosmology_phase16_certificate,
    bridge_cosmology_phase17_certificate,
    bridge_cosmology_phase18_certificate,
    bridge_cosmology_phase19_certificate,
    bridge_cosmology_phase20_certificate,
    bridge_cosmology_phase21_certificate,
    bridge_cosmology_phase22_certificate,
    bridge_cosmology_phase23_certificate,
    bridge_cosmology_phase24_certificate,
    bridge_cosmology_phase25_certificate,
    bridge_cosmology_phase26_certificate,
    bridge_cosmology_phase27_certificate,
    bridge_cosmology_phase28_certificate,
    bridge_cosmology_phase29_certificate,
    bridge_cosmology_phase30_certificate,
    bridge_cosmology_phase31_certificate,
    de_sitter_qec_toy_model_certificate,
)
from .conditional_ds_er_epr import (
    goal24_conditional_ds_er_epr_certificate,
    static_patch_kernel_cp_preflight_certificate,
)
from .family import bridge_family_certificate, bridge_theorem_certificate, lift_frontier, witness_mechanism_summary
from .gf2 import mask_to_tuple
from .graphs import enumerate_graph_state_reps
from .er_epr_channel import goal10_finite_bridge_channel_benchmark_certificate
from .er_epr_controls import goal13_non_clifford_scrambling_bridge_controls_certificate
from .er_epr_encoded import goal11_encoded_mouth_bridge_channel_certificate
from .er_epr_traversable import goal12_finite_bridge_channel_dynamics_certificate
from .ds_cft_dynamics import goal22_ds_cft_er_epr_single_dynamics_certificate
from .ds_cft_er_epr import goal21_ds_cft_er_epr_compatibility_certificate
from .derived_static_patch_dynamics import goal26_derived_static_patch_dynamics_certificate
from .embedding_channels import approximate_static_patch_embedding_certificate
from .edge_symmetry_robustness import edge_symmetry_robustness_certificate
from .finite_clock_crossed_product import finite_clock_crossed_product_no_go_certificate
from .fuzzy_algebra_inference import fuzzy_algebra_inference_certificate
from .fuzzy_berezin import fuzzy_berezin_refinement_certificate
from .fuzzy_sphere import fuzzy_sphere_regulator_certificate
from .fuzzy_screen import coherent_screen_experiment_certificate
from .general_algebraic_connectivity import goal20_general_algebraic_connectivity_stability_certificate
from .geometric_thermal_type_no_go import geometric_thermal_type_no_go_certificate
from .interacting_bridge import (
    goal15_interacting_state_derived_bridge_theorem_certificate,
    goal16_paper_style_interacting_bridge_code_theorem_certificate,
)
from .inclusion_covariant_dynamics import inclusion_covariant_static_patch_dynamics_certificate
from .interacting_kms_edge import interacting_kms_edge_certificate
from .continuum_lift import continuum_lift_obstruction_certificate
from .core_edge_obstruction import core_edge_obstruction_certificate
from .local_bridge_screen import goal18_intrinsic_local_bridge_screen_dynamics_certificate
from .modular_kms_continuity import goal29_modular_kms_continuity_certificate
from .modular_manybody_regulator import modular_manybody_regulator_certificate
from .physical_static_patch_kernel import goal25_physical_static_patch_kernel_certificate
from .static_patch_physical_continuity import goal30_static_patch_physical_continuity_certificate
from .static_patch_all_angular import static_patch_all_angular_certificate
from .static_patch_lorentzian_hadamard import static_patch_lorentzian_hadamard_certificate
from .static_patch_phase_space import static_patch_phase_space_certificate
from .static_patch_uv_removal import static_patch_uv_removal_certificate
from .static_patch_strong_continuity import goal31_static_patch_strong_continuity_certificate
from .relative_entropy_bridge import major_unlock_relative_entropy_observer_bridge_certificate
from .redshifted_frame_capacity import redshifted_frame_capacity_certificate
from .redshifted_rotation_reference_tradeoff import (
    redshifted_rotation_reference_tradeoff_certificate,
)
from .covariant_observer_energy_no_go import (
    covariant_observer_energy_no_go_certificate,
)
from .finite_size_static_patch_observer import (
    finite_size_static_patch_observer_certificate,
)
from .finite_time_rotation_diffusion import (
    finite_time_rotation_diffusion_certificate,
)
from .static_patch_matter_observer_channel import (
    static_patch_matter_observer_channel_certificate,
)
from .u8a_finite_storage_channel import (
    u8a_finite_storage_channel_certificate,
)
from .common_mode_locality_mismatch import (
    common_mode_locality_mismatch_certificate,
)
from .static_patch_scalar_common_mode import (
    static_patch_scalar_common_mode_certificate,
)
from .static_patch_radial_smearing import (
    static_patch_radial_smearing_certificate,
)
from .static_patch_gradient_torque import (
    static_patch_gradient_torque_certificate,
)
from .static_patch_higher_spin_gradient import (
    static_patch_higher_spin_gradient_certificate,
)
from .static_patch_pseudoscalar_gyroscope import (
    static_patch_pseudoscalar_gyroscope_certificate,
)
from .static_patch_hard_current_multipole import (
    static_patch_hard_current_multipole_certificate,
)
from .static_patch_localization_backreaction import (
    static_patch_localization_backreaction_certificate,
)
from .static_patch_overlapping_ule import (
    static_patch_overlapping_ule_certificate,
)
from .static_patch_worldtube_ule import (
    static_patch_worldtube_ule_certificate,
)
from .static_patch_smooth_worldtube_ule import (
    static_patch_smooth_worldtube_ule_certificate,
)
from .static_patch_skyrmion_bath import (
    static_patch_skyrmion_bath_certificate,
)
from .static_patch_skyrmion_signed_ule import (
    static_patch_skyrmion_signed_ule_certificate,
)
from .static_patch_skyrmion_tail import (
    static_patch_skyrmion_tail_certificate,
)
from .static_patch_finite_switching_ule import (
    static_patch_finite_switching_ule_certificate,
)
from .static_patch_skyrmion_offcenter import (
    static_patch_skyrmion_offcenter_certificate,
)
from .validated_interval import validated_interval_foundation_certificate
from .validated_skyrmion_profile import (
    validated_skyrmion_profile_foundation_certificate,
)
from .validated_skyrmion_origin import validated_skyrmion_origin_certificate
from .validated_skyrmion_bvp import (
    conditional_skyrmion_barta_foundation_certificate,
)
from .massive_skyrmion_profile import massive_skyrmion_profile_certificate
from .massive_skyrmion_worldtube import massive_skyrmion_worldtube_certificate
from .collective_band_feshbach import collective_band_feshbach_certificate
from .skyrmion_radial_dynamical_gap import (
    skyrmion_radial_dynamical_gap_certificate,
)
from .supported_skyrmion_collective_spectral_floor import (
    supported_skyrmion_collective_spectral_floor_certificate,
)
from .skyrmion_projective_reference import (
    skyrmion_projective_reference_certificate,
)
from .skyrmion_joint_scaling_no_go import (
    skyrmion_joint_scaling_no_go_certificate,
)
from .skyrmion_current_moments import skyrmion_current_moments_certificate
from .skyrmion_worldtube_stability import (
    skyrmion_worldtube_stability_certificate,
)
from .scalar_clock_rotation_no_go import scalar_clock_rotation_no_go_certificate
from .relational_observer import relational_observer_constraint_certificate
from .static_patch_testbed import goal23_regulated_static_patch_ds_cft_certificate
from .static_patch_regulator_universality import goal27_static_patch_regulator_universality_certificate
from .static_patch_weyl_regulator import static_patch_weyl_regulator_certificate
from .state_bridge import goal14_state_derived_bridge_dynamics_certificate
from .su2_directional_reference_no_go import su2_directional_reference_no_go_certificate
from .observer_tomography import observer_algebra_tomography_certificate
from .observer_tomography_atlas import goal7_observer_tomography_atlas_certificate
from .observer_tomography_intrinsic import goal8_intrinsic_observer_tomography_certificate
from .observer_tomography_kgt1 import goal5_kgt1_observer_tomography_certificate
from .observer_tomography_operational import goal6_operational_observer_tomography_certificate
from .oaqec_tomography import goal9_finite_oaqec_intrinsic_tomography_certificate
from .operational_phase_reference import operational_phase_reference_certificate
from .operational_su2_reference import operational_su2_reference_certificate
from .robust import (
    ENTROPY_KEY_MODES,
    ROBUST_SOURCES,
    RobustConstraints,
    quality_summary,
    robust_frontier,
)
from .search import (
    CODE_EQUIVALENCES,
    certify_minimal_entropy_reconstruction_discordance,
    enumerate_stabilizer_codes,
    find_entropy_reconstruction_discordant_pairs,
)
from .stabilizer import StabilizerCode, pauli_to_string
from .tensor_network import (
    bridge_holography_phase1_certificate,
    bridge_holography_phase2_certificate,
    bridge_holography_phase3_certificate,
    bridge_holography_phase4_certificate,
    bridge_holography_phase5_certificate,
    bridge_holography_phase6_certificate,
    bridge_holography_phase7_certificate,
    bridge_holography_phase8_certificate,
    bridge_holography_phase9_certificate,
    bridge_holography_phase10_certificate,
    bridge_holography_phase11_certificate,
    bridge_holography_phase12_certificate,
    bridge_holography_phase13_certificate,
    bridge_holography_phase14_certificate,
    bridge_holography_phase15_certificate,
    bridge_holography_phase16_certificate,
    bridge_holography_phase17_certificate,
    bridge_holography_phase18_certificate,
    bridge_holography_phase19_certificate,
    bridge_holography_phase20_certificate,
    bridge_holography_phase21_certificate,
    bridge_holography_phase22_certificate,
    bridge_holography_phase23_certificate,
    bridge_holography_phase24_certificate,
    bridge_holography_phase25_certificate,
    bridge_holography_phase26_certificate,
    bridge_holography_phase27_certificate,
    bridge_holography_phase28_certificate,
    bridge_holography_phase29_certificate,
    bridge_holography_phase30_certificate,
    bridge_holography_phase31_certificate,
    bridge_holography_phase32_certificate,
    bridge_holography_phase33_certificate,
    bridge_holography_phase34_certificate,
    bridge_holography_phase35_certificate,
    bridge_holography_phase36_certificate,
    bridge_holography_phase37_certificate,
    bridge_holography_phase38_certificate,
    bridge_holography_phase39_certificate,
    bridge_holography_phase40_certificate,
)
from .typeii_static_patch_limit import major_goal_finite_to_typeii_static_patch_certificate


def pauli_rows(rows: tuple[int, ...], n: int) -> tuple[str, ...]:
    return tuple(pauli_to_string(row, n) for row in rows)


def region_algebra_summary(code: StabilizerCode, mask: int, *, include_bases: bool) -> Any:
    algebra = code.region_algebra(mask)
    if not include_bases:
        return algebra.signature()
    return {
        "signature": algebra.signature(),
        "logical_basis": pauli_rows(algebra.logical_basis, code.n),
        "center_basis": pauli_rows(algebra.center_basis, code.n),
        "commutant_basis": pauli_rows(algebra.commutant_basis, code.n),
    }


def code_summary(code: StabilizerCode, *, include_bases: bool = False) -> dict[str, Any]:
    summary = {
        "n": code.n,
        "k": code.k,
        "generators": code.pauli_generators(),
        "logical_basis": pauli_rows(code.logical_basis, code.n),
        "distance": code.distance(),
        "erasure_threshold": code.erasure_threshold(),
        "entropy_vector": {"".join(map(str, key)): value for key, value in code.entropy_vector().items()},
        "minimal_reconstruction_regions": [
            mask_to_tuple(mask, code.n) for mask in code.reconstruction_regions(minimal=True)
        ],
        "region_algebras": {
            "".join(map(str, mask_to_tuple(mask, code.n))): region_algebra_summary(
                code,
                mask,
                include_bases=include_bases,
            )
            for mask in range(1 << code.n)
        },
    }
    return summary


def run_code_info(args: argparse.Namespace) -> None:
    code = StabilizerCode.from_pauli_strings(args.generators)
    print(json.dumps(code_summary(code, include_bases=args.include_bases), indent=2, sort_keys=True))


def run_code_reps(args: argparse.Namespace) -> None:
    reps = []
    for index, code in enumerate(
        enumerate_stabilizer_codes(args.n, k=args.k, equivalence=args.dedupe, max_codes=args.limit)
    ):
        reps.append(
            {
                "index": index,
                "canonical_key": pauli_rows(code.canonical_key(args.dedupe), code.n),
                "code": code_summary(code, include_bases=args.include_bases),
            }
        )
    print(json.dumps(reps, indent=2, sort_keys=True))


def run_graph_reps(args: argparse.Namespace) -> None:
    reps = list(enumerate_graph_state_reps(args.n, local_clifford=not args.isomorphism_only))
    payload = [
        {
            "edge_mask": edge_mask,
            "generators": state.pauli_generators(),
            "entropy_profile": state.entropy_profile(),
        }
        for edge_mask, state in reps
    ]
    print(json.dumps(payload, indent=2))


def run_search(args: argparse.Namespace) -> None:
    if args.minimal:
        certificate = certify_minimal_entropy_reconstruction_discordance(
            max_n=args.max_n,
            k=args.k,
            equivalence=args.dedupe,
            max_subset_size=args.max_subset_size,
            max_codes_per_n=args.max_codes_per_n,
            min_distance=args.min_distance,
        )
        payload: dict[str, Any] = {
            "max_n": certificate.max_n,
            "k": certificate.k,
            "dedupe": certificate.equivalence,
            "max_subset_size": certificate.max_subset_size,
            "min_distance": certificate.min_distance,
            "scans": [
                {
                    "n": scan.n,
                    "codes_checked": scan.codes_checked,
                    "entropy_classes": scan.entropy_classes,
                    "pair_found": scan.pair is not None,
                }
                for scan in certificate.scans
            ],
            "pair": None,
        }
        if certificate.pair is not None:
            payload["pair"] = {
                "n": certificate.pair.n,
                "k": certificate.pair.k,
                "entropy_profile": certificate.pair.entropy_profile,
                "first": code_summary(certificate.pair.first, include_bases=args.include_bases),
                "second": code_summary(certificate.pair.second, include_bases=args.include_bases),
            }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    payload = []
    for pair in find_entropy_reconstruction_discordant_pairs(
        max_n=args.max_n,
        k=args.k,
        equivalence=args.dedupe,
        max_subset_size=args.max_subset_size,
        max_codes_per_n=args.max_codes_per_n,
        min_distance=args.min_distance,
    ):
        payload.append(
            {
                "n": pair.n,
                "k": pair.k,
                "entropy_profile": pair.entropy_profile,
                "first": code_summary(pair.first, include_bases=args.include_bases),
                "second": code_summary(pair.second, include_bases=args.include_bases),
            }
        )
        if len(payload) >= args.limit:
            break
    print(json.dumps(payload, indent=2, sort_keys=True))


def frontier_payload(args: argparse.Namespace) -> dict[str, Any]:
    constraints = RobustConstraints(
        max_subset_size=args.max_subset_size,
        min_distance=args.min_distance,
        min_reconstruction_size=args.min_reconstruction_size,
        forbid_single_qubit_noncentral=not args.allow_single_qubit_noncentral,
    )
    frontier = robust_frontier(
        max_n=args.max_n,
        k=args.k,
        sources=tuple(args.source),
        equivalence=args.dedupe,
        entropy_key_mode=args.entropy_key,
        constraints=constraints,
        max_codes=args.max_codes_per_source,
        encoder_depth=args.encoder_depth,
        exhaustive_max_n=args.exhaustive_max_n,
        stop_on_pair=args.stop_on_pair,
    )
    payload: dict[str, Any] = {
        "max_n": frontier.max_n,
        "k": frontier.k,
        "sources": frontier.sources,
        "dedupe": frontier.equivalence,
        "entropy_key": frontier.entropy_key_mode,
        "constraints": {
            "max_subset_size": constraints.max_subset_size,
            "min_distance": constraints.min_distance,
            "min_reconstruction_size": constraints.min_reconstruction_size,
            "forbid_single_qubit_noncentral": constraints.forbid_single_qubit_noncentral,
        },
        "frontier": [
            {
                "n": scan.n,
                "source": scan.source,
                "quotient_type": scan.equivalence,
                "entropy_key": scan.entropy_key_mode,
                "raw_codes": scan.raw_codes,
                "codes_checked": scan.codes_checked,
                "entropy_classes": scan.entropy_classes,
                "pair_found": scan.pair is not None,
                "status": scan.status,
            }
            for scan in frontier.scans
        ],
        "pair": None,
    }
    if frontier.pair is not None:
        pair = frontier.pair
        payload["pair"] = {
            "n": pair.n,
            "k": pair.k,
            "entropy_key": pair.entropy_profile,
            "first": {
                "quality": quality_summary(pair.first, constraints),
                "certificate": code_summary(pair.first, include_bases=args.include_bases),
                "canonical_key": pauli_rows(pair.first.canonical_key(args.dedupe), pair.first.n),
            },
            "second": {
                "quality": quality_summary(pair.second, constraints),
                "certificate": code_summary(pair.second, include_bases=args.include_bases),
                "canonical_key": pauli_rows(pair.second.canonical_key(args.dedupe), pair.second.n),
            },
            "explanation": (
                "Both codes pass the nontriviality filters: distance and minimal reconstruction "
                "bounds hold, and no forbidden single-qubit non-central logical algebra is present. "
                "Their low-order entropy key matches, but reconstruction/algebra profiles differ."
            ),
        }
    return payload


def run_robust_search(args: argparse.Namespace) -> None:
    print(json.dumps(frontier_payload(args), indent=2, sort_keys=True))


def run_witness_mechanism(args: argparse.Namespace) -> None:
    print(json.dumps(witness_mechanism_summary(), indent=2, sort_keys=True))


def run_lift_frontier(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            lift_frontier(
                max_balanced_supports=args.max_balanced_supports,
                max_repeat_steps=args.max_repeat_steps,
                max_repeated_supports=args.max_repeated_supports,
                include_codes=args.include_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_bridge_family(args: argparse.Namespace) -> None:
    z_support = sum(1 << qubit for qubit in args.z_support)
    x_support = sum(1 << qubit for qubit in args.x_support)
    print(
        json.dumps(
            bridge_family_certificate(
                z_support=z_support,
                x_support=x_support,
                max_steps=args.max_steps,
                include_codes=args.include_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_bridge_theorem(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_theorem_certificate(
                max_exact_steps=args.max_exact_steps,
                include_exact_codes=args.include_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_bridge_proof_check(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_symbolic_proof_check(
                sample_max_m=args.sample_max_m,
                include_proof_text=not args.no_proof_text,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_desitter_toy(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            de_sitter_qec_toy_model_certificate(
                max_m=args.max_m,
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_observer_tomography(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            observer_algebra_tomography_certificate(
                max_m=args.max_m,
                max_bonus=args.max_bonus,
                scan_max_n=args.scan_max_n,
                skip_boundary_scan=args.skip_boundary_scan,
                include_holography=args.include_holography,
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_observer_tomography_kgt1(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal5_kgt1_observer_tomography_certificate(
                max_n=args.max_n,
                k=args.k,
                equivalence=args.dedupe,
                max_codes_per_n=args.max_codes_per_n,
                max_extra_logicals=args.max_extra_logicals,
                include_amplified_full_scan=args.include_amplified_full_scan,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_observer_tomography_operational(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal6_operational_observer_tomography_certificate(
                max_n=args.max_n,
                k=args.k,
                equivalence=args.dedupe,
                max_codes_per_n=args.max_codes_per_n,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_observer_tomography_atlas(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal7_observer_tomography_atlas_certificate(
                max_n=args.max_n,
                k=args.k,
                equivalence=args.dedupe,
                max_codes_per_n=args.max_codes_per_n,
                max_region_catalog=args.max_region_catalog,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_observer_tomography_intrinsic(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal8_intrinsic_observer_tomography_certificate(
                max_n=args.max_n,
                k=args.k,
                equivalence=args.dedupe,
                max_codes_per_n=args.max_codes_per_n,
                max_region_catalog=args.max_region_catalog,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_observer_tomography_oaqec(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal9_finite_oaqec_intrinsic_tomography_certificate(
                max_block_dim=args.max_block_dim,
                max_blocks=args.max_blocks,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_er_epr_channel(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal10_finite_bridge_channel_benchmark_certificate(max_pairs=args.max_pairs),
            indent=2,
            sort_keys=True,
        )
    )


def run_er_epr_encoded(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal11_encoded_mouth_bridge_channel_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_er_epr_traversable(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal12_finite_bridge_channel_dynamics_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_bridge_channel_controls(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal13_non_clifford_scrambling_bridge_controls_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_bilayer_program(args: argparse.Namespace) -> None:
    print(json.dumps(bilayer_reconstruction_program_certificate(), indent=2, sort_keys=True))


def run_state_bridge_dynamics(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal14_state_derived_bridge_dynamics_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_interacting_bridge_theorem(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal15_interacting_state_derived_bridge_theorem_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_interacting_bridge_code_theorem(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal16_paper_style_interacting_bridge_code_theorem_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_bridge_screen_dynamics(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal17_inseparable_bridge_screen_dynamics_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_local_bridge_screen_dynamics(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal18_intrinsic_local_bridge_screen_dynamics_certificate(
                mouths=args.mouths,
                low_order=args.low_order,
                atlas_max_mouths=args.atlas_max_mouths,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_relative_entropy_bridge_theorem(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            major_unlock_relative_entropy_observer_bridge_certificate(
                bloch_radius=args.bloch_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_algebraic_connectivity_order(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal19_algebraic_connectivity_order_parameter_certificate(
                bloch_radius=args.bloch_radius,
                epsilon_bits=args.epsilon_bits,
                response_only_epsilon_bits=args.response_only_epsilon_bits,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_general_algebraic_connectivity(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal20_general_algebraic_connectivity_stability_certificate(
                max_dim=args.max_dim,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_ds_cft_er_epr(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal21_ds_cft_er_epr_compatibility_certificate(
                max_dim=args.max_dim,
                screen_probability=args.screen_probability,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_ds_cft_er_epr_dynamics(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal22_ds_cft_er_epr_single_dynamics_certificate(
                max_dim=args.max_dim,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_regulated_static_patch(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal23_regulated_static_patch_ds_cft_certificate(
                max_cutoff=args.max_cutoff,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_conditional_ds_er_epr(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal24_conditional_ds_er_epr_certificate(
                max_cutoff=args.max_cutoff,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_kernel_audit(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_kernel_cp_preflight_certificate(
                max_cutoff=args.max_cutoff,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_physical_static_patch_kernel(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal25_physical_static_patch_kernel_certificate(
                max_cutoff=args.max_cutoff,
                noise_strength=args.noise_strength,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_derived_static_patch_dynamics(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal26_derived_static_patch_dynamics_certificate(
                max_cutoff=args.max_cutoff,
                noise_strength=args.noise_strength,
                environment_qubits=args.environment_qubits,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_regulator_universality(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal27_static_patch_regulator_universality_certificate(
                max_cutoff=args.max_cutoff,
                noise_strength=args.noise_strength,
                environment_qubits=args.environment_qubits,
                temperature_scale=args.temperature_scale,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
                perturbation_radius=args.perturbation_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_axiomatic_static_patch_selection(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal28_axiomatic_static_patch_selection_certificate(
                max_cutoff=args.max_cutoff,
                noise_strength=args.noise_strength,
                environment_qubits=args.environment_qubits,
                temperature_scale=args.temperature_scale,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
                perturbation_radius=args.perturbation_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_modular_kms_continuity(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal29_modular_kms_continuity_certificate(
                max_cutoff=args.max_cutoff,
                noise_strength=args.noise_strength,
                environment_qubits=args.environment_qubits,
                temperature_scale=args.temperature_scale,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
                perturbation_radius=args.perturbation_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_physical_continuity(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal30_static_patch_physical_continuity_certificate(
                max_cutoff=args.max_cutoff,
                noise_strength=args.noise_strength,
                environment_qubits=args.environment_qubits,
                temperature_scale=args.temperature_scale,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
                perturbation_radius=args.perturbation_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_strong_continuity(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            goal31_static_patch_strong_continuity_certificate(
                max_cutoff=args.max_cutoff,
                noise_strength=args.noise_strength,
                fixed_lapse=args.fixed_lapse,
                environment_qubits=args.environment_qubits,
                temperature_scale=args.temperature_scale,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
                perturbation_radius=args.perturbation_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_finite_typeii_static_patch(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            major_goal_finite_to_typeii_static_patch_certificate(
                max_level=args.max_level,
                max_consecutive_cutoff=args.max_consecutive_cutoff,
                bridge_cert_max_cutoff=args.bridge_cert_max_cutoff,
                noise_strength=args.noise_strength,
                fixed_lapse=args.fixed_lapse,
                environment_qubits=args.environment_qubits,
                temperature_scale=args.temperature_scale,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
                perturbation_radius=args.perturbation_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_inclusion_covariant_dynamics(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            inclusion_covariant_static_patch_dynamics_certificate(
                max_level=args.max_level,
                max_consecutive_cutoff=args.max_consecutive_cutoff,
                bridge_cert_max_cutoff=args.bridge_cert_max_cutoff,
                noise_strength=args.noise_strength,
                fixed_lapse=args.fixed_lapse,
                environment_qubits=args.environment_qubits,
                temperature_scale=args.temperature_scale,
                screen_probability=args.screen_probability,
                low_order=args.low_order,
                perturbation_radius=args.perturbation_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_embedding_channels(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            approximate_static_patch_embedding_certificate(
                max_cutoff=args.max_cutoff,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_fuzzy_sphere_regulator(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            fuzzy_sphere_regulator_certificate(
                max_level=args.max_level,
                tolerance=args.tolerance,
                heat_time=args.heat_time,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_fuzzy_screen_experiment(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            coherent_screen_experiment_certificate(
                max_level=args.max_level,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_fuzzy_algebra_inference(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            fuzzy_algebra_inference_certificate(
                max_level=args.max_level,
                tolerance=args.tolerance,
                failure_probability=args.failure_probability,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_fuzzy_berezin_refinement(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            fuzzy_berezin_refinement_certificate(
                max_source_level=args.max_source_level,
                max_mode=args.max_mode,
                heat_time=args.heat_time,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_relational_observer_constraint(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            relational_observer_constraint_certificate(
                max_level=args.max_level,
                sigma=args.sigma,
                minimum_visibility=args.minimum_visibility,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_edge_symmetry_robustness(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            edge_symmetry_robustness_certificate(
                max_level=args.max_level,
                numerator=args.splitting_numerator,
                denominator=args.splitting_denominator,
                duration=args.duration,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_core_edge_obstruction(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            core_edge_obstruction_certificate(
                max_level=args.max_level,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_interacting_kms_edge(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            interacting_kms_edge_certificate(
                max_level=args.max_level,
                beta=args.beta,
                angular_scale=args.angular_scale,
                first_site_gap=args.first_site_gap,
                coupling=args.coupling,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_charged_reference_recovery(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            charged_reference_recovery_certificate(
                max_level=args.max_level,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_operational_phase_reference(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            operational_phase_reference_certificate(
                max_level=args.max_level,
                target_error=args.target_error,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_su2_directional_reference_no_go(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            su2_directional_reference_no_go_certificate(
                max_system_spin=args.max_system_spin,
                max_reference_spin=args.max_reference_spin,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_operational_su2_reference(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            operational_su2_reference_certificate(
                max_system_spin=args.max_system_spin,
                reference_scale=args.reference_scale,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_geometric_thermal_type_no_go(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            geometric_thermal_type_no_go_certificate(
                max_cutoff=args.max_cutoff,
                beta=args.beta,
                mass=args.mass,
                radius=args.radius,
                tolerance=args.tolerance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_weyl_regulator(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_weyl_regulator_certificate(
                radius=args.radius,
                minimum_power=args.minimum_power,
                steps=args.steps,
                momentum_cutoff=args.momentum_cutoff,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_redshifted_frame_capacity(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            redshifted_frame_capacity_certificate(
                radius=args.radius,
                energy_budget=args.energy_budget,
                inner_offset=args.inner_offset,
                outer_offset=args.outer_offset,
                minimum_power=args.minimum_power,
                steps=args.steps,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_redshifted_rotation_reference_tradeoff(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            redshifted_rotation_reference_tradeoff_certificate(
                radius=args.radius,
                field_energy_budget=args.field_energy_budget,
                inner_offset=args.inner_offset,
                outer_offset=args.outer_offset,
                target_recovery_error=args.target_recovery_error,
                rotor_moment_of_inertia=args.rotor_moment_of_inertia,
                minimum_power=args.minimum_power,
                steps=args.steps,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_covariant_observer_energy_no_go(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            covariant_observer_energy_no_go_certificate(
                radius=args.radius,
                field_energy_budget=args.field_energy_budget,
                inner_offset=args.inner_offset,
                outer_offset=args.outer_offset,
                target_recovery_error=args.target_recovery_error,
                energy_scale=args.energy_scale,
                fixed_moment_of_inertia=args.fixed_moment_of_inertia,
                minimum_power=args.minimum_power,
                steps=args.steps,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_finite_size_static_patch_observer(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            finite_size_static_patch_observer_certificate(
                radius=args.radius,
                newton_constant=args.newton_constant,
                field_energy_budget=args.field_energy_budget,
                inner_offset=args.inner_offset,
                outer_offset=args.outer_offset,
                target_recovery_error=args.target_recovery_error,
                fixed_observer_radius=args.fixed_observer_radius,
                collar_size_fraction=args.collar_size_fraction,
                inertia_coefficient=args.inertia_coefficient,
                compactness_margin=args.compactness_margin,
                maximum_excitation_fraction=args.maximum_excitation_fraction,
                minimum_power=args.minimum_power,
                steps=args.steps,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_finite_time_rotation_diffusion(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            finite_time_rotation_diffusion_certificate(
                maximum_system_spin=args.maximum_system_spin,
                maximum_mean_casimir=args.maximum_mean_casimir,
                diffusion_rate=args.diffusion_rate,
                target_twirl_distance=args.target_twirl_distance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_matter_observer_channel(args: argparse.Namespace) -> None:
    del args
    print(
        json.dumps(
            static_patch_matter_observer_channel_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_u8a_finite_storage_channel(args: argparse.Namespace) -> None:
    del args
    print(
        json.dumps(
            u8a_finite_storage_channel_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_common_mode_locality_mismatch(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            common_mode_locality_mismatch_certificate(
                correlation=args.correlation,
                maximum_dimension=args.maximum_dimension,
                mismatch_coefficient=args.mismatch_coefficient,
                separation=args.separation,
                charge_gap=args.charge_gap,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_scalar_common_mode(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_scalar_common_mode_certificate(
                radius=args.radius,
                stretched_distance=args.stretched_distance,
                angular_separation=args.angular_separation,
                maximum_dimension=args.maximum_dimension,
                mismatch_coefficient=args.mismatch_coefficient,
                charge_gap=args.charge_gap,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_radial_smearing(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_radial_smearing_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_gradient_torque(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_gradient_torque_certificate(
                center_distance_over_radius=args.center_distance_over_radius,
                maximum_dimension=args.maximum_dimension,
                charge_gap=args.charge_gap,
                mismatch_coefficient=args.mismatch_coefficient,
                stretched_distance=args.stretched_distance,
                radius=args.radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_higher_spin_gradient(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_higher_spin_gradient_certificate(
                maximum_spin=args.maximum_spin,
                center_distance_over_radius=args.center_distance_over_radius,
                mismatch_coefficient=args.mismatch_coefficient,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_pseudoscalar_gyroscope(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_pseudoscalar_gyroscope_certificate(
                maximum_spin=args.maximum_spin,
                fixed_coupling=args.fixed_coupling,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_hard_current_multipole(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_hard_current_multipole_certificate(
                maximum_spin=args.maximum_spin,
                mismatch_coefficient=args.mismatch_coefficient,
                multipole_error_coefficient=args.multipole_error_coefficient,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_localization_backreaction(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_localization_backreaction_certificate(
                maximum_spin=args.maximum_spin,
                radius=args.radius,
                newton_constant=args.newton_constant,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_overlapping_ule(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_overlapping_ule_certificate(
                maximum_spin=args.maximum_spin,
                radius=args.radius,
                smearing_width=args.smearing_width,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_worldtube_ule(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_worldtube_ule_certificate(
                maximum_spin=args.maximum_spin,
                radius=args.radius,
                support_radius=args.support_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_smooth_worldtube_ule(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_smooth_worldtube_ule_certificate(
                maximum_spin=args.maximum_spin,
                radius=args.radius,
                support_radius=args.support_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_skyrmion_bath(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_skyrmion_bath_certificate(
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
                step=args.step,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_skyrmion_signed_ule(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_skyrmion_signed_ule_certificate(
                maximum_spin=args.maximum_spin,
                radius=args.radius,
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
                step=args.step,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_skyrmion_tail(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_skyrmion_tail_certificate(
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
                step=args.step,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_finite_switching_ule(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_finite_switching_ule_certificate(
                maximum_spin=args.maximum_spin,
                radius=args.radius,
                burnin_rate_multiples=args.burnin_rate_multiples,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_skyrmion_offcenter(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_skyrmion_offcenter_certificate(
                radius=args.radius,
                frequency=args.frequency,
                center_distance_over_radius=args.center_distance,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_validated_interval_foundation(args: argparse.Namespace) -> None:
    del args
    print(
        json.dumps(
            validated_interval_foundation_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_validated_skyrmion_profile_foundation(
    args: argparse.Namespace,
) -> None:
    del args
    print(
        json.dumps(
            validated_skyrmion_profile_foundation_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_validated_skyrmion_origin(args: argparse.Namespace) -> None:
    del args
    print(
        json.dumps(
            validated_skyrmion_origin_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_validated_skyrmion_barta_foundation(
    args: argparse.Namespace,
) -> None:
    del args
    print(
        json.dumps(
            conditional_skyrmion_barta_foundation_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_massive_skyrmion_profile(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            massive_skyrmion_profile_certificate(
                pion_mass=args.pion_mass,
                maximum_radius=args.maximum_radius,
                step=args.step,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_massive_skyrmion_worldtube(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            massive_skyrmion_worldtube_certificate(
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
                step=args.step,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_supported_skyrmion_collective_spectral_floor(
    args: argparse.Namespace,
) -> None:
    print(
        json.dumps(
            supported_skyrmion_collective_spectral_floor_certificate(
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
                step=args.step,
                skyrme_coupling=args.skyrme_coupling,
                pion_decay_constant=args.pion_decay_constant,
                energy_multiplier=args.energy_multiplier,
                dual_parameter=args.dual_parameter,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_collective_band_feshbach(_: argparse.Namespace) -> None:
    print(
        json.dumps(
            collective_band_feshbach_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_skyrmion_radial_dynamical_gap(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            skyrmion_radial_dynamical_gap_certificate(
                wall_radius=args.wall_radius,
                curvature=args.curvature,
                au1_positive_radius_barta_lower_bound=args.barta_lower_bound,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_skyrmion_projective_reference(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            skyrmion_projective_reference_certificate(
                maximum_system_spin=args.maximum_system_spin,
                maximum_reference_cutoff=args.maximum_reference_cutoff,
                skyrme_coupling=args.skyrme_coupling,
                pion_decay_constant=args.pion_decay_constant,
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_skyrmion_joint_scaling_no_go(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            skyrmion_joint_scaling_no_go_certificate(
                static_patch_radius=args.static_patch_radius,
                newton_constant=args.newton_constant,
                maximum_compactness=args.maximum_compactness,
                maximum_slow_rotation=args.maximum_slow_rotation,
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_skyrmion_current_moments(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            skyrmion_current_moments_certificate(
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
                step=args.step,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_skyrmion_worldtube_stability(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            skyrmion_worldtube_stability_certificate(
                pion_mass=args.pion_mass,
                curvature=args.curvature,
                wall_radius=args.wall_radius,
                step=args.step,
                radius_difference=args.radius_difference,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_phase_space(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_phase_space_certificate(
                radius=args.radius,
                minimum_power=args.minimum_power,
                steps=args.steps,
                momentum_cutoff=args.momentum_cutoff,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_uv_removal(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_uv_removal_certificate(
                radius=args.radius,
                minimum_cutoff=args.minimum_cutoff,
                steps=args.steps,
                derivative_order=args.derivative_order,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_all_angular(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_all_angular_certificate(
                radius=args.radius,
                dimensionless_momentum_cutoff=args.dimensionless_momentum_cutoff,
                integration_steps=args.integration_steps,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_static_patch_lorentzian_hadamard(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            static_patch_lorentzian_hadamard_certificate(
                radius=args.radius,
                integration_steps=args.integration_steps,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_scalar_clock_rotation_no_go(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            scalar_clock_rotation_no_go_certificate(
                radius=args.radius,
                energy_budget=args.energy_budget,
                inner_offset=args.inner_offset,
                outer_offset=args.outer_offset,
                minimum_power=args.minimum_power,
                steps=args.steps,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_finite_clock_crossed_product(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            finite_clock_crossed_product_no_go_certificate(
                max_level=args.max_level,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_modular_manybody_regulator(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            modular_manybody_regulator_certificate(
                max_sites=args.max_sites,
                beta=args.beta,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_continuum_lift(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            continuum_lift_obstruction_certificate(
                max_cutoff=args.max_cutoff,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase1(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase1_certificate(
                max_m=args.max_m,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase2(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase2_certificate(
                max_m=args.max_m,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase3(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase3_certificate(
                m=args.m,
                horizon_size=args.horizon_size,
                max_candidates=args.max_candidates,
                max_hits=args.max_hits,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase4(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase4_certificate(
                horizon_size=args.horizon_size,
                private_size=args.private_size,
                max_cover_candidates=args.max_cover_candidates,
                max_hits_per_pair=args.max_hits_per_pair,
                include_calibration=not args.no_calibration,
                include_source_scans=not args.no_source_scans,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase5(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase5_certificate(
                max_bridge_m=args.max_bridge_m,
                horizon_size=args.horizon_size,
                private_size=args.private_size,
                max_cover_candidates=args.max_cover_candidates,
                max_hits_per_source=args.max_hits_per_source,
                include_calibration=not args.no_calibration,
                include_source_scans=not args.no_source_scans,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase6(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase6_certificate(
                max_bridge_m=args.max_bridge_m,
                horizon_size=args.horizon_size,
                private_size=args.private_size,
                max_generic_candidates=args.max_generic_candidates,
                max_hits_per_source=args.max_hits_per_source,
                include_calibration=not args.no_calibration,
                include_source_scans=not args.no_source_scans,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase7(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase7_certificate(
                cache_path=args.cache_path,
                horizon_size=args.horizon_size,
                private_size=args.private_size,
                max_generic_candidates=args.max_generic_candidates,
                max_hits_per_source=args.max_hits_per_source,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase8(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase8_certificate(
                cache_path=args.cache_path,
                horizon_size=args.horizon_size,
                private_size=args.private_size,
                max_generic_candidates=args.max_generic_candidates,
                max_hits_per_source=args.max_hits_per_source,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase9(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase9_certificate(
                cache_path=args.cache_path,
                max_hits_per_source=args.max_hits_per_source,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase10(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase10_certificate(
                cache_path=args.cache_path,
                graph_n=args.graph_n,
                graph_max_codes=args.graph_max_codes,
                max_hits_per_source=args.max_hits_per_source,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase11(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase11_certificate(
                max_hits_per_source=args.max_hits_per_source,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase12(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase12_certificate(
                max_hits_per_source=args.max_hits_per_source,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase13(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase13_certificate(
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase14(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase14_certificate(
                max_observer_q_edit=args.max_observer_q_edit,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase15(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase15_certificate(
                max_observer_q_edit=args.max_observer_q_edit,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase16(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase16_certificate(
                max_m=args.max_m,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase17(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase17_certificate(
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase18(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase18_certificate(
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase19(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase19_certificate(
                max_radius=args.max_radius,
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase20(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase20_certificate(
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase21(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase21_certificate(
                include_bases=args.include_bases,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase22(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase22_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase23(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase23_certificate(),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase24(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase24_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase25(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase25_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase26(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase26_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase27(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase27_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase28(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase28_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase29(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase29_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase30(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase30_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_cosmology_phase31(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_cosmology_phase31_certificate(
                max_bonus=args.max_bonus,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase1(args: argparse.Namespace) -> None:
    print(json.dumps(bridge_holography_phase1_certificate(), indent=2, sort_keys=True))


def run_holography_phase2(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase2_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase3(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase3_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase4(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase4_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase5(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase5_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase6(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase6_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase7(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase7_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase8(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase8_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase9(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase9_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase10(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase10_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase11(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase11_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase12(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase12_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase13(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase13_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase14(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase14_certificate(
                graph_max_codes=args.graph_max_codes,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase15(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase15_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase16(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase16_certificate(
                graph_max_codes=args.graph_max_codes,
                min_interval_length=args.min_interval_length,
                max_interval_length=args.max_interval_length,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase17(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase17_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase18(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase18_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase19(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase19_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase20(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase20_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase21(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase21_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase22(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase22_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase23(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase23_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase24(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase24_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase25(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase25_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase26(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase26_certificate(
                graph_max_codes=args.graph_max_codes,
                audit_entropy_mismatch_near_hits=args.audit_entropy_mismatch_near_hits,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase27(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase27_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase28(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase28_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase29(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase29_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase30(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase30_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase31(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase31_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase32(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase32_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase33(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase33_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase34(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase34_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase35(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase35_certificate(
                graph_max_codes=args.graph_max_codes,
                source_ordinals=tuple(args.source_ordinals),
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase36(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase36_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase37(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase37_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase38(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase38_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase39(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase39_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def run_holography_phase40(args: argparse.Namespace) -> None:
    print(
        json.dumps(
            bridge_holography_phase40_certificate(
                graph_max_codes=args.graph_max_codes,
            ),
            indent=2,
            sort_keys=True,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="qgtoy")
    subparsers = parser.add_subparsers(required=True)

    code_info = subparsers.add_parser("code-info", help="compute exact diagnostics for a stabilizer code")
    code_info.add_argument("generators", nargs="+", help="Pauli stabilizer generators, e.g. XZZXI")
    code_info.add_argument("--include-bases", action="store_true", help="include region algebra Pauli bases")
    code_info.set_defaults(func=run_code_info)

    code_reps = subparsers.add_parser("code-reps", help="enumerate stabilizer-code representatives")
    code_reps.add_argument("--n", type=int, required=True)
    code_reps.add_argument("--k", type=int, required=True)
    code_reps.add_argument("--dedupe", choices=CODE_EQUIVALENCES, default="local-clifford")
    code_reps.add_argument("--limit", type=int)
    code_reps.add_argument("--include-bases", action="store_true", help="include region algebra Pauli bases")
    code_reps.set_defaults(func=run_code_reps)

    graph_reps = subparsers.add_parser("graph-reps", help="enumerate graph-state representatives")
    graph_reps.add_argument("--n", type=int, required=True)
    graph_reps.add_argument("--isomorphism-only", action="store_true")
    graph_reps.set_defaults(func=run_graph_reps)

    search = subparsers.add_parser("search", help="search for entropy-matched reconstruction-discordant code pairs")
    search.add_argument("--max-n", type=int, default=4)
    search.add_argument("--k", type=int, default=1)
    search.add_argument("--dedupe", choices=CODE_EQUIVALENCES, default="permutation")
    search.add_argument("--max-subset-size", type=int)
    search.add_argument("--max-codes-per-n", type=int)
    search.add_argument("--min-distance", type=int)
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--minimal", action="store_true", help="stop at first n with a pair and report scan counts")
    search.add_argument("--include-bases", action="store_true", help="include region algebra Pauli bases")
    search.set_defaults(func=run_search)

    robust = subparsers.add_parser("robust-search", help="search nontrivial stabilizer-code separations")
    robust.add_argument("--max-n", type=int, default=6)
    robust.add_argument("--k", type=int, default=1)
    robust.add_argument(
        "--source",
        choices=ROBUST_SOURCES,
        action="append",
        default=None,
        help="structured source to scan; may be repeated",
    )
    robust.add_argument("--dedupe", choices=CODE_EQUIVALENCES, default="permutation")
    robust.add_argument("--entropy-key", choices=ENTROPY_KEY_MODES, default="profile")
    robust.add_argument("--max-subset-size", type=int, default=2)
    robust.add_argument("--min-distance", type=int, default=2)
    robust.add_argument("--min-reconstruction-size", type=int, default=2)
    robust.add_argument("--allow-single-qubit-noncentral", action="store_true")
    robust.add_argument("--max-codes-per-source", type=int)
    robust.add_argument("--encoder-depth", type=int, default=2)
    robust.add_argument("--exhaustive-max-n", type=int, default=4)
    robust.add_argument("--stop-on-pair", action="store_true")
    robust.add_argument("--include-bases", action="store_true", help="include region algebra Pauli bases")
    robust.set_defaults(func=run_robust_search)

    mechanism = subparsers.add_parser("witness-mechanism", help="analyze the robust n=6 CSS witness mechanism")
    mechanism.set_defaults(func=run_witness_mechanism)

    lifts = subparsers.add_parser("lift-frontier", help="try nontrivial lift rules for the robust n=6 CSS witness")
    lifts.add_argument("--max-balanced-supports", type=int, default=32)
    lifts.add_argument("--max-repeat-steps", type=int, default=1)
    lifts.add_argument("--max-repeated-supports", type=int, default=16)
    lifts.add_argument("--include-codes", action="store_true")
    lifts.set_defaults(func=run_lift_frontier)

    bridge_family = subparsers.add_parser("bridge-family", help="verify a repeated balanced-bridge family")
    bridge_family.add_argument("--z-support", type=int, nargs="+", default=[1, 2])
    bridge_family.add_argument("--x-support", type=int, nargs="+", default=[0, 5])
    bridge_family.add_argument("--max-steps", type=int, default=3)
    bridge_family.add_argument("--include-codes", action="store_true")
    bridge_family.set_defaults(func=run_bridge_family)

    bridge_theorem = subparsers.add_parser(
        "bridge-theorem",
        help="emit theorem-style balanced-bridge family statement and certificates",
    )
    bridge_theorem.add_argument("--max-exact-steps", type=int, default=3)
    bridge_theorem.add_argument("--include-codes", action="store_true")
    bridge_theorem.set_defaults(func=run_bridge_theorem)

    bridge_proof = subparsers.add_parser(
        "bridge-proof-check",
        help="run the independent symbolic checker for the balanced-bridge proof",
    )
    bridge_proof.add_argument("--sample-max-m", type=int, default=4)
    bridge_proof.add_argument("--no-proof-text", action="store_true")
    bridge_proof.set_defaults(func=run_bridge_proof_check)

    desitter_toy = subparsers.add_parser(
        "desitter-toy",
        help="emit the finite de Sitter-like QEC toy model capstone certificate",
    )
    desitter_toy.add_argument("--max-m", type=int, default=3)
    desitter_toy.add_argument("--max-bonus", type=int, default=2)
    desitter_toy.set_defaults(func=run_desitter_toy)

    observer_tomography = subparsers.add_parser(
        "observer-tomography",
        help="emit the Goal 4 observer-algebra tomography certificate",
    )
    observer_tomography.add_argument("--max-m", type=int, default=3)
    observer_tomography.add_argument("--max-bonus", type=int, default=2)
    observer_tomography.add_argument("--scan-max-n", type=int, default=4)
    observer_tomography.add_argument(
        "--skip-boundary-scan",
        action="store_true",
        help="skip the bounded all-region positive-boundary scan",
    )
    observer_tomography.add_argument(
        "--include-holography",
        action="store_true",
        help="also run the heavier Goal 3 min-cut/reconstruction/channel certificate",
    )
    observer_tomography.add_argument("--graph-max-codes", type=int, default=220)
    observer_tomography.set_defaults(func=run_observer_tomography)

    observer_tomography_kgt1 = subparsers.add_parser(
        "observer-tomography-kgt1",
        help="emit the Goal 5 k>1 observer-algebra tomography certificate",
    )
    observer_tomography_kgt1.add_argument("--max-n", type=int, default=4)
    observer_tomography_kgt1.add_argument("--k", type=int, default=2)
    observer_tomography_kgt1.add_argument("--dedupe", choices=CODE_EQUIVALENCES, default="permutation")
    observer_tomography_kgt1.add_argument("--max-codes-per-n", type=int)
    observer_tomography_kgt1.add_argument("--max-extra-logicals", type=int, default=3)
    observer_tomography_kgt1.add_argument(
        "--include-amplified-full-scan",
        action="store_true",
        help="directly scan all regions of the distance-amplified [[15,2,3]] witness",
    )
    observer_tomography_kgt1.set_defaults(func=run_observer_tomography_kgt1)

    observer_tomography_operational = subparsers.add_parser(
        "observer-tomography-operational",
        help="emit the Goal 6 operational observer-algebra tomography certificate",
    )
    observer_tomography_operational.add_argument("--max-n", type=int, default=4)
    observer_tomography_operational.add_argument("--k", type=int, default=2)
    observer_tomography_operational.add_argument("--dedupe", choices=CODE_EQUIVALENCES, default="permutation")
    observer_tomography_operational.add_argument("--max-codes-per-n", type=int)
    observer_tomography_operational.set_defaults(func=run_observer_tomography_operational)

    observer_tomography_atlas = subparsers.add_parser(
        "observer-tomography-atlas",
        help="emit the Goal 7 equivalence-aware observer-algebra tomography atlas",
    )
    observer_tomography_atlas.add_argument("--max-n", type=int, default=4)
    observer_tomography_atlas.add_argument("--k", type=int, default=2)
    observer_tomography_atlas.add_argument("--dedupe", choices=CODE_EQUIVALENCES, default="permutation")
    observer_tomography_atlas.add_argument("--max-codes-per-n", type=int)
    observer_tomography_atlas.add_argument("--max-region-catalog", type=int, default=8)
    observer_tomography_atlas.set_defaults(func=run_observer_tomography_atlas)

    observer_tomography_intrinsic = subparsers.add_parser(
        "observer-tomography-intrinsic",
        help="emit the Goal 8 intrinsic observer-algebra tomography atlas",
    )
    observer_tomography_intrinsic.add_argument("--max-n", type=int, default=4)
    observer_tomography_intrinsic.add_argument("--k", type=int, default=2)
    observer_tomography_intrinsic.add_argument("--dedupe", choices=CODE_EQUIVALENCES, default="permutation")
    observer_tomography_intrinsic.add_argument("--max-codes-per-n", type=int)
    observer_tomography_intrinsic.add_argument("--max-region-catalog", type=int, default=8)
    observer_tomography_intrinsic.set_defaults(func=run_observer_tomography_intrinsic)

    observer_tomography_oaqec = subparsers.add_parser(
        "observer-tomography-oaqec",
        help="emit the Goal 9 finite-dimensional OAQEC observer-algebra tomography certificate",
    )
    observer_tomography_oaqec.add_argument("--max-block-dim", type=int, default=4)
    observer_tomography_oaqec.add_argument("--max-blocks", type=int, default=5)
    observer_tomography_oaqec.set_defaults(func=run_observer_tomography_oaqec)

    er_epr_channel = subparsers.add_parser(
        "er-epr-channel",
        help="emit the Goal 10 finite bridge-channel benchmark certificate",
    )
    er_epr_channel.add_argument("--max-pairs", type=int, default=4)
    er_epr_channel.set_defaults(func=run_er_epr_channel)

    er_epr_encoded = subparsers.add_parser(
        "er-epr-encoded",
        help="emit the Goal 11 encoded-mouth bridge-channel benchmark certificate",
    )
    er_epr_encoded.add_argument("--mouths", type=int, default=2)
    er_epr_encoded.add_argument("--low-order", type=int, default=3)
    er_epr_encoded.add_argument("--atlas-max-mouths", type=int, default=3)
    er_epr_encoded.set_defaults(func=run_er_epr_encoded)

    er_epr_traversable = subparsers.add_parser(
        "er-epr-traversable",
        help="emit the Goal 12 finite bridge-channel dynamics certificate",
    )
    er_epr_traversable.add_argument("--mouths", type=int, default=2)
    er_epr_traversable.add_argument("--low-order", type=int, default=3)
    er_epr_traversable.add_argument("--atlas-max-mouths", type=int, default=3)
    er_epr_traversable.set_defaults(func=run_er_epr_traversable)

    bridge_channel_controls = subparsers.add_parser(
        "bridge-channel-controls",
        help="emit the Goal 13 non-Clifford/scrambling bridge-channel control certificate",
    )
    bridge_channel_controls.add_argument("--mouths", type=int, default=2)
    bridge_channel_controls.add_argument("--low-order", type=int, default=3)
    bridge_channel_controls.add_argument("--atlas-max-mouths", type=int, default=3)
    bridge_channel_controls.set_defaults(func=run_bridge_channel_controls)

    bilayer_program = subparsers.add_parser(
        "bilayer-program",
        help="emit the finite static-patch bilayer reconstruction research certificate",
    )
    bilayer_program.set_defaults(func=run_bilayer_program)

    state_bridge_dynamics = subparsers.add_parser(
        "state-bridge-dynamics",
        help="emit the Goal 14 state-derived bridge dynamics certificate",
    )
    state_bridge_dynamics.add_argument("--mouths", type=int, default=2)
    state_bridge_dynamics.add_argument("--low-order", type=int, default=3)
    state_bridge_dynamics.add_argument("--atlas-max-mouths", type=int, default=3)
    state_bridge_dynamics.set_defaults(func=run_state_bridge_dynamics)

    interacting_bridge_theorem = subparsers.add_parser(
        "interacting-bridge-theorem",
        help="emit the Goal 15 interacting state-derived bridge theorem certificate",
    )
    interacting_bridge_theorem.add_argument("--mouths", type=int, default=2)
    interacting_bridge_theorem.add_argument("--low-order", type=int, default=3)
    interacting_bridge_theorem.add_argument("--atlas-max-mouths", type=int, default=3)
    interacting_bridge_theorem.set_defaults(func=run_interacting_bridge_theorem)

    interacting_bridge_code_theorem = subparsers.add_parser(
        "interacting-bridge-code-theorem",
        help="emit the Goal 16 paper-style interacting bridge code theorem certificate",
    )
    interacting_bridge_code_theorem.add_argument("--mouths", type=int, default=3)
    interacting_bridge_code_theorem.add_argument("--low-order", type=int, default=3)
    interacting_bridge_code_theorem.add_argument("--atlas-max-mouths", type=int, default=3)
    interacting_bridge_code_theorem.set_defaults(func=run_interacting_bridge_code_theorem)

    bridge_screen_dynamics = subparsers.add_parser(
        "bridge-screen-dynamics",
        help="emit the Goal 17 inseparable bridge-screen dynamics certificate",
    )
    bridge_screen_dynamics.add_argument("--mouths", type=int, default=3)
    bridge_screen_dynamics.add_argument("--low-order", type=int, default=3)
    bridge_screen_dynamics.add_argument("--atlas-max-mouths", type=int, default=3)
    bridge_screen_dynamics.set_defaults(func=run_bridge_screen_dynamics)

    local_bridge_screen_dynamics = subparsers.add_parser(
        "local-bridge-screen-dynamics",
        help="emit the Goal 18 intrinsic local bridge-screen dynamics certificate",
    )
    local_bridge_screen_dynamics.add_argument("--mouths", type=int, default=3)
    local_bridge_screen_dynamics.add_argument("--low-order", type=int, default=3)
    local_bridge_screen_dynamics.add_argument("--atlas-max-mouths", type=int, default=3)
    local_bridge_screen_dynamics.set_defaults(func=run_local_bridge_screen_dynamics)

    relative_entropy_bridge_theorem = subparsers.add_parser(
        "relative-entropy-bridge-theorem",
        help="emit the major-unlock finite relative-entropy observer-bridge theorem certificate",
    )
    relative_entropy_bridge_theorem.add_argument("--bloch-radius", type=float, default=0.5)
    relative_entropy_bridge_theorem.set_defaults(func=run_relative_entropy_bridge_theorem)

    algebraic_connectivity_order = subparsers.add_parser(
        "algebraic-connectivity-order",
        help="emit the Goal 19 algebraic connectivity order-parameter certificate",
    )
    algebraic_connectivity_order.add_argument("--bloch-radius", type=float, default=0.5)
    algebraic_connectivity_order.add_argument("--epsilon-bits", type=float, default=0.25)
    algebraic_connectivity_order.add_argument(
        "--response-only-epsilon-bits",
        type=float,
        default=0.4,
    )
    algebraic_connectivity_order.set_defaults(func=run_algebraic_connectivity_order)

    general_algebraic_connectivity = subparsers.add_parser(
        "general-algebraic-connectivity",
        help="emit the Goal 20 general finite-dimensional algebraic connectivity no-go certificate",
    )
    general_algebraic_connectivity.add_argument("--max-dim", type=int, default=5)
    general_algebraic_connectivity.set_defaults(func=run_general_algebraic_connectivity)

    ds_cft_er_epr = subparsers.add_parser(
        "ds-cft-er-epr",
        help="emit the Goal 21 finite dS/CFT-ER=EPR compatibility benchmark certificate",
    )
    ds_cft_er_epr.add_argument("--max-dim", type=int, default=5)
    ds_cft_er_epr.add_argument("--screen-probability", type=float, default=0.75)
    ds_cft_er_epr.set_defaults(func=run_ds_cft_er_epr)

    ds_cft_er_epr_dynamics = subparsers.add_parser(
        "ds-cft-er-epr-dynamics",
        help="emit the Goal 22 finite dS/CFT-ER=EPR single-dynamics benchmark certificate",
    )
    ds_cft_er_epr_dynamics.add_argument("--max-dim", type=int, default=5)
    ds_cft_er_epr_dynamics.add_argument("--screen-probability", type=float, default=0.75)
    ds_cft_er_epr_dynamics.add_argument("--low-order", type=int, default=2)
    ds_cft_er_epr_dynamics.set_defaults(func=run_ds_cft_er_epr_dynamics)

    regulated_static_patch = subparsers.add_parser(
        "regulated-static-patch",
        help="emit the Goal 23 regulated static-patch dS/CFT algebraic ER=EPR testbed certificate",
    )
    regulated_static_patch.add_argument("--max-cutoff", type=int, default=4)
    regulated_static_patch.add_argument("--screen-probability", type=float, default=0.75)
    regulated_static_patch.add_argument("--low-order", type=int, default=2)
    regulated_static_patch.set_defaults(func=run_regulated_static_patch)

    conditional_ds_er_epr = subparsers.add_parser(
        "conditional-ds-er-epr",
        help="emit the Goal 24 conditional dS ER=EPR theorem ledger certificate",
    )
    conditional_ds_er_epr.add_argument("--max-cutoff", type=int, default=5)
    conditional_ds_er_epr.add_argument("--screen-probability", type=float, default=0.75)
    conditional_ds_er_epr.add_argument("--low-order", type=int, default=2)
    conditional_ds_er_epr.set_defaults(func=run_conditional_ds_er_epr)

    static_patch_kernel_audit = subparsers.add_parser(
        "static-patch-kernel-audit",
        help="emit the Goal 24.1 CP/TP/unital/composition audit for the static-patch Schur kernel",
    )
    static_patch_kernel_audit.add_argument("--max-cutoff", type=int, default=6)
    static_patch_kernel_audit.set_defaults(func=run_static_patch_kernel_audit)

    physical_static_patch_kernel = subparsers.add_parser(
        "physical-static-patch-kernel",
        help="emit the Goal 25 physical static-patch kernel search certificate",
    )
    physical_static_patch_kernel.add_argument("--max-cutoff", type=int, default=5)
    physical_static_patch_kernel.add_argument("--noise-strength", type=float, default=1.0)
    physical_static_patch_kernel.add_argument("--screen-probability", type=float, default=0.75)
    physical_static_patch_kernel.add_argument("--low-order", type=int, default=2)
    physical_static_patch_kernel.set_defaults(func=run_physical_static_patch_kernel)

    derived_static_patch_dynamics = subparsers.add_parser(
        "derived-static-patch-dynamics",
        help="emit the Goal 26 derived finite static-patch dynamics certificate",
    )
    derived_static_patch_dynamics.add_argument("--max-cutoff", type=int, default=5)
    derived_static_patch_dynamics.add_argument("--noise-strength", type=float, default=1.0)
    derived_static_patch_dynamics.add_argument("--environment-qubits", type=int, default=4)
    derived_static_patch_dynamics.add_argument("--screen-probability", type=float, default=0.75)
    derived_static_patch_dynamics.add_argument("--low-order", type=int, default=2)
    derived_static_patch_dynamics.set_defaults(func=run_derived_static_patch_dynamics)

    static_patch_regulator_universality = subparsers.add_parser(
        "static-patch-regulator-universality",
        help="emit the Goal 27 finite static-patch regulator universality certificate",
    )
    static_patch_regulator_universality.add_argument("--max-cutoff", type=int, default=5)
    static_patch_regulator_universality.add_argument("--noise-strength", type=float, default=1.0)
    static_patch_regulator_universality.add_argument("--environment-qubits", type=int, default=4)
    static_patch_regulator_universality.add_argument("--temperature-scale", type=float, default=1.0)
    static_patch_regulator_universality.add_argument("--screen-probability", type=float, default=0.75)
    static_patch_regulator_universality.add_argument("--low-order", type=int, default=2)
    static_patch_regulator_universality.add_argument("--perturbation-radius", type=float, default=0.05)
    static_patch_regulator_universality.set_defaults(func=run_static_patch_regulator_universality)

    axiomatic_static_patch_selection = subparsers.add_parser(
        "axiomatic-static-patch-selection",
        help="emit the Goal 28 finite axiomatic static-patch regulator selection certificate",
    )
    axiomatic_static_patch_selection.add_argument("--max-cutoff", type=int, default=5)
    axiomatic_static_patch_selection.add_argument("--noise-strength", type=float, default=1.0)
    axiomatic_static_patch_selection.add_argument("--environment-qubits", type=int, default=4)
    axiomatic_static_patch_selection.add_argument("--temperature-scale", type=float, default=1.0)
    axiomatic_static_patch_selection.add_argument("--screen-probability", type=float, default=0.75)
    axiomatic_static_patch_selection.add_argument("--low-order", type=int, default=2)
    axiomatic_static_patch_selection.add_argument("--perturbation-radius", type=float, default=0.05)
    axiomatic_static_patch_selection.set_defaults(func=run_axiomatic_static_patch_selection)

    modular_kms_continuity = subparsers.add_parser(
        "modular-kms-continuity",
        help="emit the Goal 29 finite modular/KMS continuity certificate",
    )
    modular_kms_continuity.add_argument("--max-cutoff", type=int, default=5)
    modular_kms_continuity.add_argument("--noise-strength", type=float, default=1.0)
    modular_kms_continuity.add_argument("--environment-qubits", type=int, default=4)
    modular_kms_continuity.add_argument("--temperature-scale", type=float, default=1.0)
    modular_kms_continuity.add_argument("--screen-probability", type=float, default=0.75)
    modular_kms_continuity.add_argument("--low-order", type=int, default=2)
    modular_kms_continuity.add_argument("--perturbation-radius", type=float, default=0.05)
    modular_kms_continuity.set_defaults(func=run_modular_kms_continuity)

    static_patch_physical_continuity = subparsers.add_parser(
        "static-patch-physical-continuity",
        help="emit the Goal 30 finite static-patch physical continuity gate certificate",
    )
    static_patch_physical_continuity.add_argument("--max-cutoff", type=int, default=5)
    static_patch_physical_continuity.add_argument("--noise-strength", type=float, default=1.0)
    static_patch_physical_continuity.add_argument("--environment-qubits", type=int, default=4)
    static_patch_physical_continuity.add_argument("--temperature-scale", type=float, default=1.0)
    static_patch_physical_continuity.add_argument("--screen-probability", type=float, default=0.75)
    static_patch_physical_continuity.add_argument("--low-order", type=int, default=2)
    static_patch_physical_continuity.add_argument("--perturbation-radius", type=float, default=0.05)
    static_patch_physical_continuity.set_defaults(func=run_static_patch_physical_continuity)

    static_patch_strong_continuity = subparsers.add_parser(
        "static-patch-strong-continuity",
        help="emit the Goal 31 finite static-patch strong-continuity theorem certificate",
    )
    static_patch_strong_continuity.add_argument("--max-cutoff", type=int, default=5)
    static_patch_strong_continuity.add_argument("--noise-strength", type=float, default=1.0)
    static_patch_strong_continuity.add_argument("--fixed-lapse", type=float, default=1.0)
    static_patch_strong_continuity.add_argument("--environment-qubits", type=int, default=4)
    static_patch_strong_continuity.add_argument("--temperature-scale", type=float, default=1.0)
    static_patch_strong_continuity.add_argument("--screen-probability", type=float, default=0.75)
    static_patch_strong_continuity.add_argument("--low-order", type=int, default=2)
    static_patch_strong_continuity.add_argument("--perturbation-radius", type=float, default=0.05)
    static_patch_strong_continuity.set_defaults(func=run_static_patch_strong_continuity)

    finite_typeii_static_patch = subparsers.add_parser(
        "finite-typeii-static-patch",
        help="emit the finite-to-Type-II static-patch observer algebra certificate",
    )
    finite_typeii_static_patch.add_argument("--max-level", type=int, default=4)
    finite_typeii_static_patch.add_argument("--max-consecutive-cutoff", type=int, default=5)
    finite_typeii_static_patch.add_argument("--bridge-cert-max-cutoff", type=int, default=5)
    finite_typeii_static_patch.add_argument("--noise-strength", type=float, default=1.0)
    finite_typeii_static_patch.add_argument("--fixed-lapse", type=float, default=1.0)
    finite_typeii_static_patch.add_argument("--environment-qubits", type=int, default=4)
    finite_typeii_static_patch.add_argument("--temperature-scale", type=float, default=1.0)
    finite_typeii_static_patch.add_argument("--screen-probability", type=float, default=0.75)
    finite_typeii_static_patch.add_argument("--low-order", type=int, default=2)
    finite_typeii_static_patch.add_argument("--perturbation-radius", type=float, default=0.05)
    finite_typeii_static_patch.set_defaults(func=run_finite_typeii_static_patch)

    inclusion_covariant_dynamics = subparsers.add_parser(
        "inclusion-covariant-dynamics",
        help="emit the inclusion-covariant static-patch dynamics certificate",
    )
    inclusion_covariant_dynamics.add_argument("--max-level", type=int, default=4)
    inclusion_covariant_dynamics.add_argument("--max-consecutive-cutoff", type=int, default=5)
    inclusion_covariant_dynamics.add_argument("--bridge-cert-max-cutoff", type=int, default=5)
    inclusion_covariant_dynamics.add_argument("--noise-strength", type=float, default=1.0)
    inclusion_covariant_dynamics.add_argument("--fixed-lapse", type=float, default=1.0)
    inclusion_covariant_dynamics.add_argument("--environment-qubits", type=int, default=4)
    inclusion_covariant_dynamics.add_argument("--temperature-scale", type=float, default=1.0)
    inclusion_covariant_dynamics.add_argument("--screen-probability", type=float, default=0.75)
    inclusion_covariant_dynamics.add_argument("--low-order", type=int, default=2)
    inclusion_covariant_dynamics.add_argument("--perturbation-radius", type=float, default=0.05)
    inclusion_covariant_dynamics.set_defaults(func=run_inclusion_covariant_dynamics)

    embedding_channels = subparsers.add_parser(
        "static-patch-embedding-channels",
        help="emit the approximate static-patch cutoff embedding audit",
    )
    embedding_channels.add_argument("--max-cutoff", type=int, default=5)
    embedding_channels.set_defaults(func=run_embedding_channels)

    fuzzy_sphere = subparsers.add_parser(
        "fuzzy-sphere-regulator",
        help="audit the canonical SU(2)-equivariant finite fuzzy-sphere regulator",
    )
    fuzzy_sphere.add_argument("--max-level", type=int, default=4)
    fuzzy_sphere.add_argument("--tolerance", type=float, default=1e-9)
    fuzzy_sphere.add_argument("--heat-time", type=float, default=0.2)
    fuzzy_sphere.set_defaults(func=run_fuzzy_sphere_regulator)

    fuzzy_screen = subparsers.add_parser(
        "fuzzy-screen-experiment",
        help="audit the canonical coherent-state fuzzy-sphere screen experiment",
    )
    fuzzy_screen.add_argument("--max-level", type=int, default=6)
    fuzzy_screen.add_argument("--tolerance", type=float, default=1e-9)
    fuzzy_screen.set_defaults(func=run_fuzzy_screen_experiment)

    fuzzy_algebra = subparsers.add_parser(
        "fuzzy-algebra-inference",
        help="audit noisy three-model observer-algebra inference on the coherent screen",
    )
    fuzzy_algebra.add_argument("--max-level", type=int, default=6)
    fuzzy_algebra.add_argument("--tolerance", type=float, default=1e-10)
    fuzzy_algebra.add_argument("--failure-probability", type=float, default=0.05)
    fuzzy_algebra.set_defaults(func=run_fuzzy_algebra_inference)

    fuzzy_berezin = subparsers.add_parser(
        "fuzzy-berezin-refinement",
        help="audit canonical coherent-state refinement between fuzzy-sphere cutoffs",
    )
    fuzzy_berezin.add_argument("--max-source-level", type=int, default=5)
    fuzzy_berezin.add_argument("--max-mode", type=int, default=2)
    fuzzy_berezin.add_argument("--heat-time", type=float, default=0.2)
    fuzzy_berezin.add_argument("--tolerance", type=float, default=1e-8)
    fuzzy_berezin.set_defaults(func=run_fuzzy_berezin_refinement)

    relational_observer = subparsers.add_parser(
        "relational-observer-constraint",
        help="audit the time-and-edge-reference fuzzy-horizon observer algebra",
    )
    relational_observer.add_argument("--max-level", type=int, default=8)
    relational_observer.add_argument("--sigma", type=float, default=0.2)
    relational_observer.add_argument("--minimum-visibility", type=float, default=0.5)
    relational_observer.add_argument("--tolerance", type=float, default=1e-12)
    relational_observer.set_defaults(func=run_relational_observer_constraint)

    edge_robustness = subparsers.add_parser(
        "edge-symmetry-robustness",
        help="audit full-rotation loss and Zeeman fragility of the edge theorem",
    )
    edge_robustness.add_argument("--max-level", type=int, default=8)
    edge_robustness.add_argument("--splitting-numerator", type=int, default=1)
    edge_robustness.add_argument(
        "--splitting-denominator", type=int, default=1_000_000
    )
    edge_robustness.add_argument("--duration", type=float, default=1.0)
    edge_robustness.add_argument("--tolerance", type=float, default=1e-12)
    edge_robustness.set_defaults(func=run_edge_symmetry_robustness)

    core_edge = subparsers.add_parser(
        "core-edge-obstruction",
        help="audit persistence of angular recovery and entropy loss in the core",
    )
    core_edge.add_argument("--max-level", type=int, default=8)
    core_edge.add_argument("--tolerance", type=float, default=1e-12)
    core_edge.set_defaults(func=run_core_edge_obstruction)

    interacting_kms = subparsers.add_parser(
        "interacting-kms-edge",
        help="audit the rotationally invariant boundary-KMS edge obstruction",
    )
    interacting_kms.add_argument("--max-level", type=int, default=8)
    interacting_kms.add_argument("--beta", type=float, default=1.0)
    interacting_kms.add_argument("--angular-scale", type=float, default=0.25)
    interacting_kms.add_argument("--first-site-gap", type=float, default=1.0)
    interacting_kms.add_argument("--coupling", type=float, default=0.2)
    interacting_kms.add_argument("--tolerance", type=float, default=1e-12)
    interacting_kms.set_defaults(func=run_interacting_kms_edge)

    charged_reference = subparsers.add_parser(
        "charged-reference-recovery",
        help="audit the SU(2) singlet multiplicity code and covariance boundary",
    )
    charged_reference.add_argument("--max-level", type=int, default=8)
    charged_reference.add_argument("--tolerance", type=float, default=1e-12)
    charged_reference.set_defaults(func=run_charged_reference_recovery)

    operational_phase_reference = subparsers.add_parser(
        "operational-phase-reference",
        help="audit the finite prepared U(1) reference recovery theorem",
    )
    operational_phase_reference.add_argument("--max-level", type=int, default=8)
    operational_phase_reference.add_argument("--target-error", type=float, default=0.1)
    operational_phase_reference.add_argument("--tolerance", type=float, default=1e-12)
    operational_phase_reference.set_defaults(func=run_operational_phase_reference)

    su2_directional_reference = subparsers.add_parser(
        "su2-directional-reference-no-go",
        help="audit the multiplicity-free single-spin reference obstruction",
    )
    su2_directional_reference.add_argument("--max-system-spin", type=int, default=8)
    su2_directional_reference.add_argument("--max-reference-spin", type=int, default=8)
    su2_directional_reference.set_defaults(func=run_su2_directional_reference_no_go)

    operational_su2_reference = subparsers.add_parser(
        "operational-su2-reference",
        help="audit center-blind SO(3) rotation-reference recovery and cost",
    )
    operational_su2_reference.add_argument("--max-system-spin", type=int, default=6)
    operational_su2_reference.add_argument("--reference-scale", type=int, default=8)
    operational_su2_reference.add_argument("--tolerance", type=float, default=1e-12)
    operational_su2_reference.set_defaults(func=run_operational_su2_reference)

    geometric_thermal = subparsers.add_parser(
        "geometric-thermal-type-no-go",
        help="audit the Type-I obstruction for a global fuzzy-sphere Gibbs field",
    )
    geometric_thermal.add_argument("--max-cutoff", type=int, default=24)
    geometric_thermal.add_argument("--beta", type=float, default=2.0)
    geometric_thermal.add_argument("--mass", type=float, default=1.0)
    geometric_thermal.add_argument("--radius", type=float, default=1.0)
    geometric_thermal.add_argument("--tolerance", type=float, default=1e-10)
    geometric_thermal.set_defaults(func=run_geometric_thermal_type_no_go)

    static_patch_weyl = subparsers.add_parser(
        "static-patch-weyl-regulator",
        help="audit the static-patch s-wave equal-time covariance refinement",
    )
    static_patch_weyl.add_argument("--radius", type=float, default=1.0)
    static_patch_weyl.add_argument("--minimum-power", type=int, default=16)
    static_patch_weyl.add_argument("--steps", type=int, default=6)
    static_patch_weyl.add_argument("--momentum-cutoff", type=float, default=80.0)
    static_patch_weyl.set_defaults(func=run_static_patch_weyl_regulator)

    redshifted_frame = subparsers.add_parser(
        "redshifted-frame-capacity",
        help="audit the bounded-energy near-horizon rotational-frame entropy bound",
    )
    redshifted_frame.add_argument("--radius", type=float, default=1.0)
    redshifted_frame.add_argument("--energy-budget", type=float, default=4.0)
    redshifted_frame.add_argument("--inner-offset", type=float, default=0.5)
    redshifted_frame.add_argument("--outer-offset", type=float, default=1.5)
    redshifted_frame.add_argument("--minimum-power", type=int, default=64)
    redshifted_frame.add_argument("--steps", type=int, default=6)
    redshifted_frame.set_defaults(func=run_redshifted_frame_capacity)

    redshifted_reference = subparsers.add_parser(
        "redshifted-rotation-reference-tradeoff",
        help="audit the same-target clock-only versus charged SO(3) achievability bound",
    )
    redshifted_reference.add_argument("--radius", type=float, default=1.0)
    redshifted_reference.add_argument("--field-energy-budget", type=float, default=4.0)
    redshifted_reference.add_argument("--inner-offset", type=float, default=0.5)
    redshifted_reference.add_argument("--outer-offset", type=float, default=1.5)
    redshifted_reference.add_argument("--target-recovery-error", type=float, default=0.1)
    redshifted_reference.add_argument("--rotor-moment-of-inertia", type=float, default=1.0)
    redshifted_reference.add_argument("--minimum-power", type=int, default=64)
    redshifted_reference.add_argument("--steps", type=int, default=6)
    redshifted_reference.set_defaults(func=run_redshifted_rotation_reference_tradeoff)

    observer_energy_no_go = subparsers.add_parser(
        "covariant-observer-energy-no-go",
        help="audit why covariant recovery data do not determine observer energy",
    )
    observer_energy_no_go.add_argument("--radius", type=float, default=1.0)
    observer_energy_no_go.add_argument(
        "--field-energy-budget", type=float, default=4.0
    )
    observer_energy_no_go.add_argument("--inner-offset", type=float, default=0.5)
    observer_energy_no_go.add_argument("--outer-offset", type=float, default=1.5)
    observer_energy_no_go.add_argument(
        "--target-recovery-error", type=float, default=0.1
    )
    observer_energy_no_go.add_argument("--energy-scale", type=float, default=1.0)
    observer_energy_no_go.add_argument(
        "--fixed-moment-of-inertia", type=float, default=1.0
    )
    observer_energy_no_go.add_argument("--minimum-power", type=int, default=64)
    observer_energy_no_go.add_argument("--steps", type=int, default=6)
    observer_energy_no_go.set_defaults(func=run_covariant_observer_energy_no_go)

    finite_size_observer = subparsers.add_parser(
        "finite-size-static-patch-observer",
        help="audit finite-size rotation-reference compactness and recovery bounds",
    )
    finite_size_observer.add_argument("--radius", type=float, default=1.0)
    finite_size_observer.add_argument("--newton-constant", type=float, default=1e-6)
    finite_size_observer.add_argument(
        "--field-energy-budget", type=float, default=4.0
    )
    finite_size_observer.add_argument("--inner-offset", type=float, default=0.5)
    finite_size_observer.add_argument("--outer-offset", type=float, default=1.5)
    finite_size_observer.add_argument(
        "--target-recovery-error", type=float, default=0.1
    )
    finite_size_observer.add_argument(
        "--fixed-observer-radius", type=float, default=0.05
    )
    finite_size_observer.add_argument(
        "--collar-size-fraction", type=float, default=0.25
    )
    finite_size_observer.add_argument(
        "--inertia-coefficient", type=float, default=2.0 / 3.0
    )
    finite_size_observer.add_argument(
        "--compactness-margin", type=float, default=0.5
    )
    finite_size_observer.add_argument(
        "--maximum-excitation-fraction", type=float, default=0.25
    )
    finite_size_observer.add_argument("--minimum-power", type=int, default=64)
    finite_size_observer.add_argument("--steps", type=int, default=9)
    finite_size_observer.set_defaults(func=run_finite_size_static_patch_observer)

    finite_time_diffusion = subparsers.add_parser(
        "finite-time-rotation-diffusion",
        help="audit finite-time SO(3) heat-kernel convergence to Haar twirling",
    )
    finite_time_diffusion.add_argument(
        "--maximum-system-spin", type=int, default=512
    )
    finite_time_diffusion.add_argument(
        "--maximum-mean-casimir", type=float, default=10.0
    )
    finite_time_diffusion.add_argument("--diffusion-rate", type=float, default=1.0)
    finite_time_diffusion.add_argument(
        "--target-twirl-distance", type=float, default=0.05
    )
    finite_time_diffusion.set_defaults(func=run_finite_time_rotation_diffusion)

    matter_observer_channel = subparsers.add_parser(
        "static-patch-matter-observer-channel",
        help=(
            "audit norm-separated finite-time matter-to-observer recovery "
            "transfers"
        ),
    )
    matter_observer_channel.set_defaults(
        func=run_static_patch_matter_observer_channel
    )

    u8a_storage_channel = subparsers.add_parser(
        "u8a-finite-storage-channel",
        help=(
            "audit the conditional fixed-register degradation box and "
            "certify the factorized-current locality route stop"
        ),
    )
    u8a_storage_channel.set_defaults(func=run_u8a_finite_storage_channel)

    common_mode_mismatch = subparsers.add_parser(
        "common-mode-locality-mismatch",
        help="audit local covariance mismatch from ideal common rotation noise",
    )
    common_mode_mismatch.add_argument("--correlation", type=float, default=0.95)
    common_mode_mismatch.add_argument(
        "--maximum-dimension", type=int, default=4096
    )
    common_mode_mismatch.add_argument(
        "--mismatch-coefficient", type=float, default=1.0
    )
    common_mode_mismatch.add_argument("--separation", type=float, default=1.0)
    common_mode_mismatch.add_argument("--charge-gap", type=float, default=1.0)
    common_mode_mismatch.set_defaults(func=run_common_mode_locality_mismatch)

    scalar_common_mode = subparsers.add_parser(
        "static-patch-scalar-common-mode",
        help="audit the Bunch-Davies scalar zero-frequency common-mode covariance",
    )
    scalar_common_mode.add_argument("--radius", type=float, default=1.0)
    scalar_common_mode.add_argument(
        "--stretched-distance", type=float, default=0.05
    )
    scalar_common_mode.add_argument(
        "--angular-separation", type=float, default=0.1
    )
    scalar_common_mode.add_argument(
        "--maximum-dimension", type=int, default=4096
    )
    scalar_common_mode.add_argument(
        "--mismatch-coefficient", type=float, default=1.0
    )
    scalar_common_mode.add_argument("--charge-gap", type=float, default=1.0)
    scalar_common_mode.set_defaults(func=run_static_patch_scalar_common_mode)

    radial_smearing = subparsers.add_parser(
        "static-patch-radial-smearing",
        help="audit exact H3 radial-smearing invariance of the scalar zero mode",
    )
    radial_smearing.set_defaults(func=run_static_patch_radial_smearing)

    gradient_torque = subparsers.add_parser(
        "static-patch-gradient-torque",
        help="audit the three-axis Bunch-Davies gradient covariance obstruction",
    )
    gradient_torque.add_argument(
        "--center-distance-over-radius", type=float, default=0.2
    )
    gradient_torque.add_argument("--maximum-dimension", type=int, default=4096)
    gradient_torque.add_argument("--charge-gap", type=float, default=1.0)
    gradient_torque.add_argument(
        "--mismatch-coefficient", type=float, default=1.0
    )
    gradient_torque.add_argument("--stretched-distance", type=float, default=0.05)
    gradient_torque.add_argument("--radius", type=float, default=1.0)
    gradient_torque.set_defaults(func=run_static_patch_gradient_torque)

    higher_spin_gradient = subparsers.add_parser(
        "static-patch-higher-spin-gradient",
        help="audit Casimir-enhanced higher-spin gradient-channel singlet leakage",
    )
    higher_spin_gradient.add_argument("--maximum-spin", type=int, default=4096)
    higher_spin_gradient.add_argument(
        "--center-distance-over-radius", type=float, default=1.0e-6
    )
    higher_spin_gradient.add_argument(
        "--mismatch-coefficient", type=float, default=1.0
    )
    higher_spin_gradient.set_defaults(func=run_static_patch_higher_spin_gradient)

    pseudoscalar_gyroscope = subparsers.add_parser(
        "static-patch-pseudoscalar-gyroscope",
        help="audit a local parity-even pseudoscalar gyroscope and lapse tradeoff",
    )
    pseudoscalar_gyroscope.add_argument(
        "--maximum-spin", type=int, default=4096
    )
    pseudoscalar_gyroscope.add_argument(
        "--fixed-coupling", type=float, default=0.01
    )
    pseudoscalar_gyroscope.set_defaults(
        func=run_static_patch_pseudoscalar_gyroscope
    )

    hard_current_multipole = subparsers.add_parser(
        "static-patch-hard-current-multipole",
        help="audit distributed angular-current multipoles and Bohr leakage",
    )
    hard_current_multipole.add_argument(
        "--maximum-spin", type=int, default=4096
    )
    hard_current_multipole.add_argument(
        "--mismatch-coefficient", type=float, default=1.0
    )
    hard_current_multipole.add_argument(
        "--multipole-error-coefficient", type=float, default=1.0
    )
    hard_current_multipole.set_defaults(
        func=run_static_patch_hard_current_multipole
    )

    localization_backreaction = subparsers.add_parser(
        "static-patch-localization-backreaction",
        help="audit compactness against shrinking hard-current support windows",
    )
    localization_backreaction.add_argument(
        "--maximum-spin", type=int, default=4096
    )
    localization_backreaction.add_argument("--radius", type=float, default=1.0)
    localization_backreaction.add_argument(
        "--newton-constant", type=float, default=1.0e-12
    )
    localization_backreaction.set_defaults(
        func=run_static_patch_localization_backreaction
    )

    overlapping_ule = subparsers.add_parser(
        "static-patch-overlapping-ule",
        help="audit overlapping-sector Bunch-Davies ULE spectral data",
    )
    overlapping_ule.add_argument("--maximum-spin", type=int, default=4096)
    overlapping_ule.add_argument("--radius", type=float, default=1.0)
    overlapping_ule.add_argument("--smearing-width", type=float, default=0.2)
    overlapping_ule.set_defaults(func=run_static_patch_overlapping_ule)

    worldtube_ule = subparsers.add_parser(
        "static-patch-worldtube-ule",
        help="audit compact optical-worldtube filtering and stabilized ULE error",
    )
    worldtube_ule.add_argument("--maximum-spin", type=int, default=4096)
    worldtube_ule.add_argument("--radius", type=float, default=1.0)
    worldtube_ule.add_argument("--support-radius", type=float, default=0.2)
    worldtube_ule.set_defaults(func=run_static_patch_worldtube_ule)

    smooth_worldtube_ule = subparsers.add_parser(
        "static-patch-smooth-worldtube-ule",
        help="audit a smooth compact optical profile and its ULE moment bounds",
    )
    smooth_worldtube_ule.add_argument("--maximum-spin", type=int, default=4096)
    smooth_worldtube_ule.add_argument("--radius", type=float, default=1.0)
    smooth_worldtube_ule.add_argument(
        "--support-radius", type=float, default=0.2
    )
    smooth_worldtube_ule.set_defaults(
        func=run_static_patch_smooth_worldtube_ule
    )

    skyrmion_bath = subparsers.add_parser(
        "static-patch-skyrmion-bath",
        help="derive the centered Skyrmion bath form factor and root no-go",
    )
    skyrmion_bath.add_argument("--pion-mass", type=float, default=1.0)
    skyrmion_bath.add_argument("--curvature", type=float, default=0.0025)
    skyrmion_bath.add_argument("--wall-radius", type=float, default=4.0)
    skyrmion_bath.add_argument("--step", type=float, default=0.002)
    skyrmion_bath.set_defaults(func=run_static_patch_skyrmion_bath)

    skyrmion_signed_ule = subparsers.add_parser(
        "static-patch-skyrmion-signed-ule",
        help="audit the signed Skyrmion jump-correlator ULE route",
    )
    skyrmion_signed_ule.add_argument("--maximum-spin", type=int, default=4096)
    skyrmion_signed_ule.add_argument("--radius", type=float, default=1.0)
    skyrmion_signed_ule.add_argument("--pion-mass", type=float, default=1.0)
    skyrmion_signed_ule.add_argument("--curvature", type=float, default=0.0025)
    skyrmion_signed_ule.add_argument("--wall-radius", type=float, default=4.0)
    skyrmion_signed_ule.add_argument("--step", type=float, default=0.002)
    skyrmion_signed_ule.set_defaults(func=run_static_patch_skyrmion_signed_ule)

    skyrmion_tail = subparsers.add_parser(
        "static-patch-skyrmion-tail",
        help="audit the exact continuum tail of the signed Skyrmion factor",
    )
    skyrmion_tail.add_argument("--pion-mass", type=float, default=1.0)
    skyrmion_tail.add_argument("--curvature", type=float, default=0.0025)
    skyrmion_tail.add_argument("--wall-radius", type=float, default=4.0)
    skyrmion_tail.add_argument("--step", type=float, default=0.002)
    skyrmion_tail.set_defaults(func=run_static_patch_skyrmion_tail)

    finite_switching_ule = subparsers.add_parser(
        "static-patch-finite-switching-ule",
        help="audit finite switch-on and burn-in for the stationary ULE route",
    )
    finite_switching_ule.add_argument(
        "--maximum-spin", type=int, default=4096
    )
    finite_switching_ule.add_argument("--radius", type=float, default=1.0)
    finite_switching_ule.add_argument(
        "--burnin-rate-multiples", type=float, default=10.0
    )
    finite_switching_ule.set_defaults(
        func=run_static_patch_finite_switching_ule
    )

    skyrmion_offcenter = subparsers.add_parser(
        "static-patch-skyrmion-offcenter",
        help="audit optical translation versus intrinsic off-center deformation",
    )
    skyrmion_offcenter.add_argument("--radius", type=float, default=1.0)
    skyrmion_offcenter.add_argument("--frequency", type=float, default=0.7)
    skyrmion_offcenter.add_argument(
        "--center-distance", type=float, default=0.2
    )
    skyrmion_offcenter.set_defaults(func=run_static_patch_skyrmion_offcenter)

    validated_interval = subparsers.add_parser(
        "validated-interval-foundation",
        help="audit exact rational intervals for the validated Skyrmion program",
    )
    validated_interval.set_defaults(func=run_validated_interval_foundation)

    validated_profile = subparsers.add_parser(
        "validated-skyrmion-profile-foundation",
        help="audit a conditional exact-rational Skyrmion Picard cell",
    )
    validated_profile.set_defaults(
        func=run_validated_skyrmion_profile_foundation
    )

    validated_origin = subparsers.add_parser(
        "validated-skyrmion-origin",
        help="audit the exact uniform regular-origin shooting-slope family",
    )
    validated_origin.set_defaults(func=run_validated_skyrmion_origin)

    validated_barta = subparsers.add_parser(
        "validated-skyrmion-barta-foundation",
        help="audit conditional exact-rational Skyrmion Jacobi Barta cells",
    )
    validated_barta.set_defaults(func=run_validated_skyrmion_barta_foundation)

    massive_skyrmion = subparsers.add_parser(
        "massive-skyrmion-profile",
        help="solve the flat massive profile and audit the de Sitter inertia gate",
    )
    massive_skyrmion.add_argument("--pion-mass", type=float, default=1.0)
    massive_skyrmion.add_argument("--maximum-radius", type=float, default=10.0)
    massive_skyrmion.add_argument("--step", type=float, default=0.002)
    massive_skyrmion.set_defaults(func=run_massive_skyrmion_profile)

    massive_skyrmion_worldtube = subparsers.add_parser(
        "massive-skyrmion-worldtube",
        help="solve the centered membrane-supported hard-wall Skyrmion",
    )
    massive_skyrmion_worldtube.add_argument(
        "--pion-mass", type=float, default=1.0
    )
    massive_skyrmion_worldtube.add_argument(
        "--curvature", type=float, default=0.0025
    )
    massive_skyrmion_worldtube.add_argument(
        "--wall-radius", type=float, default=4.0
    )
    massive_skyrmion_worldtube.add_argument("--step", type=float, default=0.002)
    massive_skyrmion_worldtube.set_defaults(
        func=run_massive_skyrmion_worldtube
    )

    supported_skyrmion_floor = subparsers.add_parser(
        "supported-skyrmion-collective-spectral-floor",
        help="audit the profile-uniform supported Skyrmion collective floor",
    )
    supported_skyrmion_floor.add_argument(
        "--pion-mass", type=float, default=1.0
    )
    supported_skyrmion_floor.add_argument(
        "--curvature", type=float, default=0.0025
    )
    supported_skyrmion_floor.add_argument(
        "--wall-radius", type=float, default=4.0
    )
    supported_skyrmion_floor.add_argument("--step", type=float, default=0.002)
    supported_skyrmion_floor.add_argument(
        "--skyrme-coupling", type=float, default=1.0
    )
    supported_skyrmion_floor.add_argument(
        "--pion-decay-constant", type=float, default=1.0
    )
    supported_skyrmion_floor.add_argument(
        "--energy-multiplier", type=float, default=1.1
    )
    supported_skyrmion_floor.add_argument(
        "--dual-parameter", type=float, default=0.1
    )
    supported_skyrmion_floor.set_defaults(
        func=run_supported_skyrmion_collective_spectral_floor
    )

    collective_band_feshbach = subparsers.add_parser(
        "collective-band-feshbach",
        help="audit collective-to-full spectral transfer and missing inputs",
    )
    collective_band_feshbach.set_defaults(func=run_collective_band_feshbach)

    radial_dynamical_gap = subparsers.add_parser(
        "skyrmion-radial-dynamical-gap",
        help="audit radial kinetic weight and conditional dynamic-gap transfer",
    )
    radial_dynamical_gap.add_argument(
        "--wall-radius", type=float, default=4.0
    )
    radial_dynamical_gap.add_argument(
        "--curvature", type=float, default=0.0025
    )
    radial_dynamical_gap.add_argument(
        "--barta-lower-bound", type=float, default=1.0235900944571767
    )
    radial_dynamical_gap.set_defaults(func=run_skyrmion_radial_dynamical_gap)

    skyrmion_projective_reference = subparsers.add_parser(
        "skyrmion-projective-reference",
        help="audit the odd Peter-Weyl B=1 Skyrmion orientation reference",
    )
    skyrmion_projective_reference.add_argument(
        "--maximum-system-spin", type=int, default=6
    )
    skyrmion_projective_reference.add_argument(
        "--maximum-reference-cutoff", type=int, default=8
    )
    skyrmion_projective_reference.add_argument(
        "--skyrme-coupling", type=float, default=0.1
    )
    skyrmion_projective_reference.add_argument(
        "--pion-decay-constant", type=float, default=1.0
    )
    skyrmion_projective_reference.add_argument(
        "--pion-mass", type=float, default=1.0
    )
    skyrmion_projective_reference.add_argument(
        "--curvature", type=float, default=0.0025
    )
    skyrmion_projective_reference.add_argument(
        "--wall-radius", type=float, default=4.0
    )
    skyrmion_projective_reference.set_defaults(
        func=run_skyrmion_projective_reference
    )

    skyrmion_joint_scaling = subparsers.add_parser(
        "skyrmion-joint-scaling-no-go",
        help="audit compactness against slow rotation for the fixed worldtube",
    )
    skyrmion_joint_scaling.add_argument(
        "--static-patch-radius", type=float, default=1.0
    )
    skyrmion_joint_scaling.add_argument(
        "--newton-constant", type=float, default=1.0e-6
    )
    skyrmion_joint_scaling.add_argument(
        "--maximum-compactness", type=float, default=0.5
    )
    skyrmion_joint_scaling.add_argument(
        "--maximum-slow-rotation", type=float, default=0.1
    )
    skyrmion_joint_scaling.add_argument("--pion-mass", type=float, default=1.0)
    skyrmion_joint_scaling.add_argument(
        "--curvature", type=float, default=0.0025
    )
    skyrmion_joint_scaling.add_argument(
        "--wall-radius", type=float, default=4.0
    )
    skyrmion_joint_scaling.set_defaults(
        func=run_skyrmion_joint_scaling_no_go
    )

    skyrmion_current_moments = subparsers.add_parser(
        "skyrmion-current-moments",
        help="audit centered hard-wall Skyrmion collective-current moments",
    )
    skyrmion_current_moments.add_argument(
        "--pion-mass", type=float, default=1.0
    )
    skyrmion_current_moments.add_argument(
        "--curvature", type=float, default=0.0025
    )
    skyrmion_current_moments.add_argument(
        "--wall-radius", type=float, default=4.0
    )
    skyrmion_current_moments.add_argument("--step", type=float, default=0.002)
    skyrmion_current_moments.set_defaults(func=run_skyrmion_current_moments)

    skyrmion_worldtube_stability = subparsers.add_parser(
        "skyrmion-worldtube-stability",
        help="audit centered radial stability and finite-pinning topology",
    )
    skyrmion_worldtube_stability.add_argument(
        "--pion-mass", type=float, default=1.0
    )
    skyrmion_worldtube_stability.add_argument(
        "--curvature", type=float, default=0.0025
    )
    skyrmion_worldtube_stability.add_argument(
        "--wall-radius", type=float, default=4.0
    )
    skyrmion_worldtube_stability.add_argument("--step", type=float, default=0.002)
    skyrmion_worldtube_stability.add_argument(
        "--radius-difference", type=float, default=0.005
    )
    skyrmion_worldtube_stability.set_defaults(
        func=run_skyrmion_worldtube_stability
    )

    static_patch_phase_space = subparsers.add_parser(
        "static-patch-phase-space",
        help="audit the fixed-UV s-wave canonical phase-space KMS limit",
    )
    static_patch_phase_space.add_argument("--radius", type=float, default=1.0)
    static_patch_phase_space.add_argument("--minimum-power", type=int, default=64)
    static_patch_phase_space.add_argument("--steps", type=int, default=5)
    static_patch_phase_space.add_argument("--momentum-cutoff", type=float, default=20.0)
    static_patch_phase_space.set_defaults(func=run_static_patch_phase_space)

    static_patch_uv = subparsers.add_parser(
        "static-patch-uv-removal",
        help="audit quantitative UV removal for the static-patch s-wave KMS state",
    )
    static_patch_uv.add_argument("--radius", type=float, default=1.0)
    static_patch_uv.add_argument("--minimum-cutoff", type=float, default=8.0)
    static_patch_uv.add_argument("--steps", type=int, default=4)
    static_patch_uv.add_argument("--derivative-order", type=int, default=4)
    static_patch_uv.set_defaults(func=run_static_patch_uv_removal)

    static_patch_all_angular = subparsers.add_parser(
        "static-patch-all-angular",
        help="audit the all-angular conformal static-patch wall limit and kernel",
    )
    static_patch_all_angular.add_argument("--radius", type=float, default=1.0)
    static_patch_all_angular.add_argument(
        "--dimensionless-momentum-cutoff",
        type=float,
        default=30.0,
    )
    static_patch_all_angular.add_argument(
        "--integration-steps",
        type=int,
        default=1600,
    )
    static_patch_all_angular.set_defaults(func=run_static_patch_all_angular)

    static_patch_hadamard = subparsers.add_parser(
        "static-patch-lorentzian-hadamard",
        help="audit the Lorentzian Bunch-Davies Hadamard local-net benchmark",
    )
    static_patch_hadamard.add_argument("--radius", type=float, default=1.0)
    static_patch_hadamard.add_argument(
        "--integration-steps",
        type=int,
        default=8000,
    )
    static_patch_hadamard.set_defaults(func=run_static_patch_lorentzian_hadamard)

    scalar_clock_rotation = subparsers.add_parser(
        "scalar-clock-rotation-no-go",
        help="audit the hard-energy SO(3) fixed-point obstruction for a clock-only truncation",
    )
    scalar_clock_rotation.add_argument("--radius", type=float, default=1.0)
    scalar_clock_rotation.add_argument("--energy-budget", type=float, default=4.0)
    scalar_clock_rotation.add_argument("--inner-offset", type=float, default=0.5)
    scalar_clock_rotation.add_argument("--outer-offset", type=float, default=1.5)
    scalar_clock_rotation.add_argument("--minimum-power", type=int, default=64)
    scalar_clock_rotation.add_argument("--steps", type=int, default=6)
    scalar_clock_rotation.set_defaults(func=run_scalar_clock_rotation_no_go)

    finite_clock = subparsers.add_parser(
        "finite-clock-crossed-product",
        help="audit the finite inner-action obstruction to a Type-II clock algebra",
    )
    finite_clock.add_argument("--max-level", type=int, default=8)
    finite_clock.set_defaults(func=run_finite_clock_crossed_product)

    modular_manybody = subparsers.add_parser(
        "modular-manybody-regulator",
        help="audit the state-derived ITPFI limit and Type-II continuous core",
    )
    modular_manybody.add_argument("--max-sites", type=int, default=10)
    modular_manybody.add_argument("--beta", type=float, default=1.0)
    modular_manybody.set_defaults(func=run_modular_manybody_regulator)

    continuum_lift = subparsers.add_parser(
        "continuum-lift-obstruction",
        help="emit the conditional continuum-lift screen-only dictionary obstruction schema",
    )
    continuum_lift.add_argument("--max-cutoff", type=int, default=5)
    continuum_lift.set_defaults(func=run_continuum_lift)

    cosmology_phase1 = subparsers.add_parser(
        "cosmology-phase1",
        help="emit the Goal 2 Phase 1 finite causal-patch/horizon-code certificate",
    )
    cosmology_phase1.add_argument("--max-m", type=int, default=3)
    cosmology_phase1.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase1.set_defaults(func=run_cosmology_phase1)

    cosmology_phase2 = subparsers.add_parser(
        "cosmology-phase2",
        help="emit the Goal 2 Phase 2 bridge-growth and erasure-channel certificate",
    )
    cosmology_phase2.add_argument("--max-m", type=int, default=3)
    cosmology_phase2.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase2.set_defaults(func=run_cosmology_phase2)

    cosmology_phase3 = subparsers.add_parser(
        "cosmology-phase3",
        help="emit the Goal 2 Phase 3 bounded causal-patch cover-search certificate",
    )
    cosmology_phase3.add_argument("--m", type=int, default=2)
    cosmology_phase3.add_argument("--horizon-size", type=int, default=3)
    cosmology_phase3.add_argument("--max-candidates", type=int)
    cosmology_phase3.add_argument("--max-hits", type=int, default=5)
    cosmology_phase3.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase3.set_defaults(func=run_cosmology_phase3)

    cosmology_phase4 = subparsers.add_parser(
        "cosmology-phase4",
        help="emit the Goal 2 Phase 4 code-source and generic cover-search certificate",
    )
    cosmology_phase4.add_argument("--horizon-size", type=int, default=2)
    cosmology_phase4.add_argument("--private-size", type=int, default=1)
    cosmology_phase4.add_argument("--max-cover-candidates", type=int)
    cosmology_phase4.add_argument("--max-hits-per-pair", type=int, default=3)
    cosmology_phase4.add_argument("--no-calibration", action="store_true")
    cosmology_phase4.add_argument("--no-source-scans", action="store_true")
    cosmology_phase4.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase4.set_defaults(func=run_cosmology_phase4)

    cosmology_phase5 = subparsers.add_parser(
        "cosmology-phase5",
        help="emit the Goal 2 Phase 5 cached source-frontier and targeted-lift certificate",
    )
    cosmology_phase5.add_argument("--max-bridge-m", type=int, default=2)
    cosmology_phase5.add_argument("--horizon-size", type=int, default=2)
    cosmology_phase5.add_argument("--private-size", type=int, default=1)
    cosmology_phase5.add_argument("--max-cover-candidates", type=int, default=120)
    cosmology_phase5.add_argument("--max-hits-per-source", type=int, default=1)
    cosmology_phase5.add_argument("--no-calibration", action="store_true")
    cosmology_phase5.add_argument("--no-source-scans", action="store_true")
    cosmology_phase5.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase5.set_defaults(func=run_cosmology_phase5)

    cosmology_phase6 = subparsers.add_parser(
        "cosmology-phase6",
        help="emit the Goal 2 Phase 6 source-aware cover-template certificate",
    )
    cosmology_phase6.add_argument("--max-bridge-m", type=int, default=2)
    cosmology_phase6.add_argument("--horizon-size", type=int, default=2)
    cosmology_phase6.add_argument("--private-size", type=int, default=1)
    cosmology_phase6.add_argument("--max-generic-candidates", type=int, default=120)
    cosmology_phase6.add_argument("--max-hits-per-source", type=int, default=1)
    cosmology_phase6.add_argument("--no-calibration", action="store_true")
    cosmology_phase6.add_argument("--no-source-scans", action="store_true")
    cosmology_phase6.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase6.set_defaults(func=run_cosmology_phase6)

    cosmology_phase7 = subparsers.add_parser(
        "cosmology-phase7",
        help="emit the Goal 2 Phase 7 persistent frontier-cache replay certificate",
    )
    cosmology_phase7.add_argument("--cache-path", default=None)
    cosmology_phase7.add_argument("--horizon-size", type=int, default=2)
    cosmology_phase7.add_argument("--private-size", type=int, default=1)
    cosmology_phase7.add_argument("--max-generic-candidates", type=int, default=120)
    cosmology_phase7.add_argument("--max-hits-per-source", type=int, default=1)
    cosmology_phase7.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase7.set_defaults(func=run_cosmology_phase7)

    cosmology_phase8 = subparsers.add_parser(
        "cosmology-phase8",
        help="emit the Goal 2 Phase 8 graph/encoder extended frontier-cache certificate",
    )
    cosmology_phase8.add_argument("--cache-path", default=None)
    cosmology_phase8.add_argument("--horizon-size", type=int, default=2)
    cosmology_phase8.add_argument("--private-size", type=int, default=1)
    cosmology_phase8.add_argument("--max-generic-candidates", type=int, default=120)
    cosmology_phase8.add_argument("--max-hits-per-source", type=int, default=1)
    cosmology_phase8.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase8.set_defaults(func=run_cosmology_phase8)

    cosmology_phase9 = subparsers.add_parser(
        "cosmology-phase9",
        help="emit the Goal 2 Phase 9 graph-specific cover-template no-go certificate",
    )
    cosmology_phase9.add_argument("--cache-path", default=None)
    cosmology_phase9.add_argument("--max-hits-per-source", type=int, default=1)
    cosmology_phase9.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase9.set_defaults(func=run_cosmology_phase9)

    cosmology_phase10 = subparsers.add_parser(
        "cosmology-phase10",
        help="emit the Goal 2 Phase 10 labeled graph/CWS strict-atlas certificate",
    )
    cosmology_phase10.add_argument("--cache-path", default=None)
    cosmology_phase10.add_argument("--graph-n", type=int, default=5)
    cosmology_phase10.add_argument("--graph-max-codes", type=int, default=64)
    cosmology_phase10.add_argument("--max-hits-per-source", type=int, default=3)
    cosmology_phase10.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase10.set_defaults(func=run_cosmology_phase10)

    cosmology_phase11 = subparsers.add_parser(
        "cosmology-phase11",
        help="emit the Goal 2 Phase 11 distance-repaired graph-atlas tension certificate",
    )
    cosmology_phase11.add_argument("--max-hits-per-source", type=int, default=1)
    cosmology_phase11.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase11.set_defaults(func=run_cosmology_phase11)

    cosmology_phase12 = subparsers.add_parser(
        "cosmology-phase12",
        help="emit the Goal 2 Phase 12 atlas-aware repaired-cover certificate",
    )
    cosmology_phase12.add_argument("--max-hits-per-source", type=int, default=1)
    cosmology_phase12.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase12.set_defaults(func=run_cosmology_phase12)

    cosmology_phase13 = subparsers.add_parser(
        "cosmology-phase13",
        help="emit the Goal 2 Phase 13 repaired cover-dynamics certificate",
    )
    cosmology_phase13.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase13.set_defaults(func=run_cosmology_phase13)

    cosmology_phase14 = subparsers.add_parser(
        "cosmology-phase14",
        help="emit the Goal 2 Phase 14 bounded repaired-cover transition-graph certificate",
    )
    cosmology_phase14.add_argument("--max-observer-q-edit", type=int, default=5)
    cosmology_phase14.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase14.set_defaults(func=run_cosmology_phase14)

    cosmology_phase15 = subparsers.add_parser(
        "cosmology-phase15",
        help="emit the Goal 2 Phase 15 multi-source cover-flow invariant atlas certificate",
    )
    cosmology_phase15.add_argument("--max-observer-q-edit", type=int, default=5)
    cosmology_phase15.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase15.set_defaults(func=run_cosmology_phase15)

    cosmology_phase16 = subparsers.add_parser(
        "cosmology-phase16",
        help="emit the Goal 2 Phase 16 mixed CSS code-cover transition graph certificate",
    )
    cosmology_phase16.add_argument("--max-m", type=int, default=3)
    cosmology_phase16.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase16.set_defaults(func=run_cosmology_phase16)

    cosmology_phase17 = subparsers.add_parser(
        "cosmology-phase17",
        help="emit the Goal 2 Phase 17 repaired non-CSS local-Clifford flow certificate",
    )
    cosmology_phase17.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase17.set_defaults(func=run_cosmology_phase17)

    cosmology_phase18 = subparsers.add_parser(
        "cosmology-phase18",
        help="emit the Goal 2 Phase 18 non-CSS outer-code swap taxonomy certificate",
    )
    cosmology_phase18.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase18.set_defaults(func=run_cosmology_phase18)

    cosmology_phase19 = subparsers.add_parser(
        "cosmology-phase19",
        help="emit the Goal 2 Phase 19 bounded outer-code mutation search certificate",
    )
    cosmology_phase19.add_argument("--max-radius", type=int, choices=(1, 2), default=2)
    cosmology_phase19.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase19.set_defaults(func=run_cosmology_phase19)

    cosmology_phase20 = subparsers.add_parser(
        "cosmology-phase20",
        help="emit the Goal 2 Phase 20 bounded inner graph/CWS mutation search certificate",
    )
    cosmology_phase20.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase20.set_defaults(func=run_cosmology_phase20)

    cosmology_phase21 = subparsers.add_parser(
        "cosmology-phase21",
        help="emit the Goal 2 Phase 21 mixed inner-outer transition graph certificate",
    )
    cosmology_phase21.add_argument("--include-bases", action="store_true", help="include Pauli bases for patch algebras")
    cosmology_phase21.set_defaults(func=run_cosmology_phase21)

    cosmology_phase22 = subparsers.add_parser(
        "cosmology-phase22",
        help="emit the Goal 2 Phase 22 exact time/channel dynamics certificate",
    )
    cosmology_phase22.set_defaults(func=run_cosmology_phase22)

    cosmology_phase23 = subparsers.add_parser(
        "cosmology-phase23",
        help="emit the Goal 2 Phase 23 biased channel comparison certificate",
    )
    cosmology_phase23.set_defaults(func=run_cosmology_phase23)

    cosmology_phase24 = subparsers.add_parser(
        "cosmology-phase24",
        help="emit the Goal 2 Phase 24 bounded exact channel-rule search certificate",
    )
    cosmology_phase24.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase24.set_defaults(func=run_cosmology_phase24)

    cosmology_phase25 = subparsers.add_parser(
        "cosmology-phase25",
        help="emit the Goal 2 Phase 25 target-constrained channel synthesis certificate",
    )
    cosmology_phase25.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase25.set_defaults(func=run_cosmology_phase25)

    cosmology_phase26 = subparsers.add_parser(
        "cosmology-phase26",
        help="emit the Goal 2 Phase 26 cross-substrate channel-rule transfer certificate",
    )
    cosmology_phase26.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase26.set_defaults(func=run_cosmology_phase26)

    cosmology_phase27 = subparsers.add_parser(
        "cosmology-phase27",
        help="emit the Goal 2 Phase 27 multi-substrate robust channel synthesis certificate",
    )
    cosmology_phase27.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase27.set_defaults(func=run_cosmology_phase27)

    cosmology_phase28 = subparsers.add_parser(
        "cosmology-phase28",
        help="emit the Goal 2 Phase 28 audited rule-language proof certificate",
    )
    cosmology_phase28.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase28.set_defaults(func=run_cosmology_phase28)

    cosmology_phase29 = subparsers.add_parser(
        "cosmology-phase29",
        help="emit the Goal 2 Phase 29 bounded substrate-family co-design certificate",
    )
    cosmology_phase29.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase29.set_defaults(func=run_cosmology_phase29)

    cosmology_phase30 = subparsers.add_parser(
        "cosmology-phase30",
        help="emit the Goal 2 Phase 30 bounded observer-cover co-design certificate",
    )
    cosmology_phase30.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase30.set_defaults(func=run_cosmology_phase30)

    cosmology_phase31 = subparsers.add_parser(
        "cosmology-phase31",
        help="emit the Goal 2 Phase 31 strict-cover exhaustive audit certificate",
    )
    cosmology_phase31.add_argument("--max-bonus", type=int, default=2)
    cosmology_phase31.set_defaults(func=run_cosmology_phase31)

    holography_phase1 = subparsers.add_parser(
        "holography-phase1",
        help="emit the Goal 3 Phase 1 stabilizer tensor-network seed certificate",
    )
    holography_phase1.set_defaults(func=run_holography_phase1)

    holography_phase2 = subparsers.add_parser(
        "holography-phase2",
        help="emit the Goal 3 Phase 2 bounded graph/CWS ring-spoke atlas certificate",
    )
    holography_phase2.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase2.add_argument("--max-interval-length", type=int, default=2)
    holography_phase2.set_defaults(func=run_holography_phase2)

    holography_phase3 = subparsers.add_parser(
        "holography-phase3",
        help="emit the Goal 3 Phase 3 distance-repaired lifted graph/CWS ring-spoke atlas certificate",
    )
    holography_phase3.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase3.add_argument("--max-interval-length", type=int, default=2)
    holography_phase3.set_defaults(func=run_holography_phase3)

    holography_phase4 = subparsers.add_parser(
        "holography-phase4",
        help="emit the Goal 3 Phase 4 multi-bulk-node layout audit certificate",
    )
    holography_phase4.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase4.add_argument("--max-interval-length", type=int, default=2)
    holography_phase4.set_defaults(func=run_holography_phase4)

    holography_phase5 = subparsers.add_parser(
        "holography-phase5",
        help="emit the Goal 3 Phase 5 generated Clifford/MERA-style layout search certificate",
    )
    holography_phase5.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase5.set_defaults(func=run_holography_phase5)

    holography_phase6 = subparsers.add_parser(
        "holography-phase6",
        help="emit the Goal 3 Phase 6 generated Clifford tensor-network audit certificate",
    )
    holography_phase6.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase6.set_defaults(func=run_holography_phase6)

    holography_phase7 = subparsers.add_parser(
        "holography-phase7",
        help="emit the Goal 3 Phase 7 joint Clifford circuit and compact-patch search certificate",
    )
    holography_phase7.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase7.add_argument("--max-interval-length", type=int, default=6)
    holography_phase7.set_defaults(func=run_holography_phase7)

    holography_phase8 = subparsers.add_parser(
        "holography-phase8",
        help="emit the Goal 3 Phase 8 distance-gated Clifford synthesis search certificate",
    )
    holography_phase8.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase8.add_argument("--max-interval-length", type=int, default=6)
    holography_phase8.set_defaults(func=run_holography_phase8)

    holography_phase9 = subparsers.add_parser(
        "holography-phase9",
        help="emit the Goal 3 Phase 9 compressed pentagon two-layer block certificate",
    )
    holography_phase9.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase9.add_argument("--max-interval-length", type=int, default=6)
    holography_phase9.set_defaults(func=run_holography_phase9)

    holography_phase10 = subparsers.add_parser(
        "holography-phase10",
        help="emit the Goal 3 Phase 10 five-qubit perfect outer-block certificate",
    )
    holography_phase10.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase10.add_argument("--max-interval-length", type=int, default=8)
    holography_phase10.set_defaults(func=run_holography_phase10)

    holography_phase11 = subparsers.add_parser(
        "holography-phase11",
        help="emit the Goal 3 Phase 11 same-distance perfect-outer variant certificate",
    )
    holography_phase11.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase11.add_argument("--max-interval-length", type=int, default=8)
    holography_phase11.set_defaults(func=run_holography_phase11)

    holography_phase12 = subparsers.add_parser(
        "holography-phase12",
        help="emit the Goal 3 Phase 12 perfect-outer embedding robustness certificate",
    )
    holography_phase12.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase12.add_argument("--max-interval-length", type=int, default=8)
    holography_phase12.set_defaults(func=run_holography_phase12)

    holography_phase13 = subparsers.add_parser(
        "holography-phase13",
        help="emit the Goal 3 Phase 13 two-perfect-tensor tiling certificate",
    )
    holography_phase13.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase13.add_argument("--max-interval-length", type=int, default=8)
    holography_phase13.set_defaults(func=run_holography_phase13)

    holography_phase14 = subparsers.add_parser(
        "holography-phase14",
        help="emit the Goal 3 Phase 14 three-perfect-cell chain/ring atlas certificate",
    )
    holography_phase14.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase14.add_argument("--max-interval-length", type=int, default=8)
    holography_phase14.set_defaults(func=run_holography_phase14)

    holography_phase15 = subparsers.add_parser(
        "holography-phase15",
        help="emit the Goal 3 Phase 15 capacity/branching fixed-witness grammar certificate",
    )
    holography_phase15.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase15.set_defaults(func=run_holography_phase15)

    holography_phase16 = subparsers.add_parser(
        "holography-phase16",
        help="emit the Goal 3 Phase 16 capacity-sensitive interval no-go certificate",
    )
    holography_phase16.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase16.add_argument("--min-interval-length", type=int, default=9)
    holography_phase16.add_argument("--max-interval-length", type=int, default=45)
    holography_phase16.set_defaults(func=run_holography_phase16)

    holography_phase17 = subparsers.add_parser(
        "holography-phase17",
        help="emit the Goal 3 Phase 17 four-perfect-cell tree fixed-witness certificate",
    )
    holography_phase17.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase17.set_defaults(func=run_holography_phase17)

    holography_phase18 = subparsers.add_parser(
        "holography-phase18",
        help="emit the Goal 3 Phase 18 four-cell tree shell-bottleneck certificate",
    )
    holography_phase18.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase18.set_defaults(func=run_holography_phase18)

    holography_phase19 = subparsers.add_parser(
        "holography-phase19",
        help="emit the Goal 3 Phase 19 compact-core plus shell hybrid no-go certificate",
    )
    holography_phase19.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase19.set_defaults(func=run_holography_phase19)

    holography_phase20 = subparsers.add_parser(
        "holography-phase20",
        help="emit the Goal 3 Phase 20 four-cell outer-tree local-variant no-go certificate",
    )
    holography_phase20.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase20.set_defaults(func=run_holography_phase20)

    holography_phase21 = subparsers.add_parser(
        "holography-phase21",
        help="emit the Goal 3 Phase 21 four-cell outer-tree topology no-go certificate",
    )
    holography_phase21.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase21.set_defaults(func=run_holography_phase21)

    holography_phase22 = subparsers.add_parser(
        "holography-phase22",
        help="emit the Goal 3 Phase 22 five-cell branching internal-witness audit certificate",
    )
    holography_phase22.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase22.set_defaults(func=run_holography_phase22)

    holography_phase23 = subparsers.add_parser(
        "holography-phase23",
        help="emit the Goal 3 Phase 23 interface-cell star audit certificate",
    )
    holography_phase23.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase23.set_defaults(func=run_holography_phase23)

    holography_phase24 = subparsers.add_parser(
        "holography-phase24",
        help="emit the Goal 3 Phase 24 punctured interface-shell frontier certificate",
    )
    holography_phase24.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase24.set_defaults(func=run_holography_phase24)

    holography_phase25 = subparsers.add_parser(
        "holography-phase25",
        help="emit the Goal 3 Phase 25 two-layer Clifford/MERA-like frontier certificate",
    )
    holography_phase25.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase25.set_defaults(func=run_holography_phase25)

    holography_phase26 = subparsers.add_parser(
        "holography-phase26",
        help="emit the Goal 3 Phase 26 offset-flip entropy-gated neighborhood certificate",
    )
    holography_phase26.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase26.add_argument(
        "--audit-entropy-mismatch-near-hits",
        action="store_true",
        help="also run operator/channel checks on entropy-rejected records",
    )
    holography_phase26.set_defaults(func=run_holography_phase26)

    holography_phase27 = subparsers.add_parser(
        "holography-phase27",
        help="emit the Goal 3 Phase 27 second-root-hole region-grammar certificate",
    )
    holography_phase27.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase27.set_defaults(func=run_holography_phase27)

    holography_phase28 = subparsers.add_parser(
        "holography-phase28",
        help="emit the Goal 3 Phase 28 leaf-private sentinel region-grammar certificate",
    )
    holography_phase28.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase28.set_defaults(func=run_holography_phase28)

    holography_phase29 = subparsers.add_parser(
        "holography-phase29",
        help="emit the Goal 3 Phase 29 full leaf-private region-grammar certificate",
    )
    holography_phase29.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase29.set_defaults(func=run_holography_phase29)

    holography_phase30 = subparsers.add_parser(
        "holography-phase30",
        help="emit the Goal 3 Phase 30 bridge-axis source-pairing certificate",
    )
    holography_phase30.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase30.set_defaults(func=run_holography_phase30)

    holography_phase31 = subparsers.add_parser(
        "holography-phase31",
        help="emit the Goal 3 Phase 31 shared logical-basis twist certificate",
    )
    holography_phase31.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase31.set_defaults(func=run_holography_phase31)

    holography_phase32 = subparsers.add_parser(
        "holography-phase32",
        help="emit the Goal 3 Phase 32 independent logical-basis twist priority certificate",
    )
    holography_phase32.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase32.set_defaults(func=run_holography_phase32)

    holography_phase33 = subparsers.add_parser(
        "holography-phase33",
        help="emit the Goal 3 Phase 33 full independent logical-basis twist certificate",
    )
    holography_phase33.add_argument("--graph-max-codes", type=int, default=24)
    holography_phase33.set_defaults(func=run_holography_phase33)

    holography_phase34 = subparsers.add_parser(
        "holography-phase34",
        help="emit the Goal 3 Phase 34 alternative graph/CWS source-pair scout certificate",
    )
    holography_phase34.add_argument("--graph-max-codes", type=int, default=64)
    holography_phase34.set_defaults(func=run_holography_phase34)

    holography_phase35 = subparsers.add_parser(
        "holography-phase35",
        help="emit the Goal 3 Phase 35 full alternative source-pair semantic audit certificate",
    )
    holography_phase35.add_argument("--graph-max-codes", type=int, default=64)
    holography_phase35.add_argument(
        "--source-ordinals",
        type=int,
        nargs=2,
        default=(21, 26),
        metavar=("FIRST", "SECOND"),
        help="graph/CWS source-pair ordinals to audit",
    )
    holography_phase35.set_defaults(func=run_holography_phase35)

    holography_phase36 = subparsers.add_parser(
        "holography-phase36",
        help="emit the Goal 3 Phase 36 full entropy-mismatch near-hit audit certificate",
    )
    holography_phase36.add_argument("--graph-max-codes", type=int, default=64)
    holography_phase36.set_defaults(func=run_holography_phase36)

    holography_phase37 = subparsers.add_parser(
        "holography-phase37",
        help="emit the Goal 3 Phase 37 split-support region-grammar certificate",
    )
    holography_phase37.add_argument("--graph-max-codes", type=int, default=64)
    holography_phase37.set_defaults(func=run_holography_phase37)

    holography_phase38 = subparsers.add_parser(
        "holography-phase38",
        help="emit the Goal 3 Phase 38 q139 support-scale strict-hit certificate",
    )
    holography_phase38.add_argument("--graph-max-codes", type=int, default=64)
    holography_phase38.set_defaults(func=run_holography_phase38)

    holography_phase39 = subparsers.add_parser(
        "holography-phase39",
        help="emit the Goal 3 Phase 39 representative witness robustness certificate",
    )
    holography_phase39.add_argument("--graph-max-codes", type=int, default=64)
    holography_phase39.set_defaults(func=run_holography_phase39)

    holography_phase40 = subparsers.add_parser(
        "holography-phase40",
        help="emit the Goal 3 Phase 40 theorem-style holographic-cousin package",
    )
    holography_phase40.add_argument("--graph-max-codes", type=int, default=64)
    holography_phase40.set_defaults(func=run_holography_phase40)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "source") and args.source is None:
        args.source = ["exhaustive", "css", "cyclic-css", "graph", "encoder"]
    args.func(args)


if __name__ == "__main__":
    main()
