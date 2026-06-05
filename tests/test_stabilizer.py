import unittest

from qgtoy.bridge_proof import bridge_symbolic_proof_check
from qgtoy.cosmology import (
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
    bridge_observer_cover,
    de_sitter_qec_toy_model_certificate,
    rank_kernel_algebra_summary,
    rank_kernel_entropy,
)
from qgtoy.family import (
    bridge_family_certificate,
    bridge_theorem_certificate,
    lift_frontier,
    seed_pair,
    witness_mechanism_summary,
)
from qgtoy.graphs import enumerate_graph_state_reps
from qgtoy.observer_tomography import observer_algebra_tomography_certificate
from qgtoy.observer_tomography_atlas import goal7_observer_tomography_atlas_certificate
from qgtoy.observer_tomography_intrinsic import goal8_intrinsic_observer_tomography_certificate
from qgtoy.observer_tomography_kgt1 import goal5_kgt1_observer_tomography_certificate
from qgtoy.observer_tomography_operational import goal6_operational_observer_tomography_certificate
from qgtoy.oaqec_tomography import goal9_finite_oaqec_intrinsic_tomography_certificate
from qgtoy.robust import RobustConstraints, code_quality, robust_frontier
from qgtoy.search import (
    certify_minimal_entropy_reconstruction_discordance,
    enumerate_stabilizer_codes,
    find_entropy_reconstruction_discordant_pairs,
)
from qgtoy.stabilizer import StabilizerCode, StabilizerState, pauli_from_string
from qgtoy.tensor_network import (
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


class StabilizerDiagnosticsTest(unittest.TestCase):
    def test_bell_state_entropies(self):
        state = StabilizerState(2, [pauli_from_string("XX"), pauli_from_string("ZZ")])
        self.assertEqual(state.k, 0)
        self.assertEqual(state.entropy([0]), 1)
        self.assertEqual(state.entropy([1]), 1)
        self.assertEqual(state.entropy([0, 1]), 0)
        self.assertEqual(state.mutual_information([0], [1]), 2)

    def test_ghz_information_quantities(self):
        state = StabilizerState(
            3,
            [
                pauli_from_string("XXX"),
                pauli_from_string("ZZI"),
                pauli_from_string("IZZ"),
            ],
        )
        self.assertEqual(state.tripartite_information([0], [1], [2]), 0)
        self.assertEqual(state.conditional_mutual_information([0], [1], [2]), 1)

    def test_five_qubit_code_distance_and_erasure(self):
        code = StabilizerCode.from_pauli_strings(["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"])
        self.assertEqual(code.k, 1)
        self.assertEqual(code.distance(), 3)
        self.assertEqual(code.erasure_threshold(), 2)
        self.assertTrue(code.erasure_correctable([0, 1]))
        self.assertFalse(code.erasure_correctable([0, 1, 2]))
        self.assertTrue(code.reconstructs_all_logicals([2, 3, 4]))

    def test_region_algebra_center_for_full_logical_region(self):
        code = StabilizerCode.from_pauli_strings(["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"])
        algebra = code.region_algebra([2, 3, 4])
        self.assertEqual(algebra.logical_dim, 2)
        self.assertEqual(algebra.center_dim, 0)
        self.assertEqual(algebra.commutant_dim, 0)
        self.assertEqual(len(algebra.logical_basis), 2)
        self.assertEqual(algebra.center_basis, ())
        self.assertEqual(algebra.commutant_basis, ())
        self.assertTrue(algebra.reconstructs_all)

    def test_graph_state_lc_representatives_n3(self):
        reps = list(enumerate_graph_state_reps(3))
        self.assertEqual(len(reps), 3)

    def test_code_local_clifford_representatives_n1_state(self):
        raw = list(enumerate_stabilizer_codes(1, k=0, equivalence="none"))
        local_clifford = list(enumerate_stabilizer_codes(1, k=0, equivalence="local-clifford"))
        self.assertEqual(len(raw), 3)
        self.assertEqual(len(local_clifford), 1)

    def test_local_clifford_canonicalizes_x_and_z_state(self):
        x_state = StabilizerCode.from_pauli_strings(["X"])
        z_state = StabilizerCode.from_pauli_strings(["Z"])
        self.assertEqual(x_state.canonical_key("local-clifford"), z_state.canonical_key("local-clifford"))

    def test_search_finds_or_certifies_small_space(self):
        pairs = list(find_entropy_reconstruction_discordant_pairs(max_n=3, k=1))
        self.assertIsInstance(pairs, list)

    def test_low_order_entropy_search_finds_n4_discordance(self):
        pairs = list(find_entropy_reconstruction_discordant_pairs(max_n=4, k=1, max_subset_size=2))
        self.assertGreaterEqual(len(pairs), 1)
        pair = pairs[0]
        self.assertEqual(pair.n, 4)
        self.assertEqual(pair.k, 1)
        self.assertEqual(
            pair.first.entropy_profile(max_subset_size=2),
            pair.second.entropy_profile(max_subset_size=2),
        )
        self.assertNotEqual(pair.first.reconstruction_profile(), pair.second.reconstruction_profile())

    def test_minimal_low_order_entropy_certificate(self):
        certificate = certify_minimal_entropy_reconstruction_discordance(max_n=4, k=1, max_subset_size=2)
        self.assertIsNotNone(certificate.pair)
        self.assertEqual(certificate.pair.n, 4)
        self.assertTrue(all(scan.pair is None for scan in certificate.scans[:-1]))
        self.assertTrue(certificate.scans[-1].pair is not None)

    def test_robust_filters_reject_distance_one_calibration_witness(self):
        code = StabilizerCode.from_pauli_strings(["XIZI", "XZII", "ZXXI"])
        quality = code_quality(code, RobustConstraints())
        self.assertFalse(quality.passes)
        self.assertEqual(quality.reason, "distance")

    def test_robust_filters_accept_five_qubit_code(self):
        code = StabilizerCode.from_pauli_strings(["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"])
        quality = code_quality(code, RobustConstraints())
        self.assertTrue(quality.passes)
        self.assertEqual(quality.distance, 3)
        self.assertEqual(quality.minimal_reconstruction_size, 3)
        self.assertFalse(quality.has_single_qubit_noncentral_logical)

    def test_robust_frontier_smoke_css_n4(self):
        frontier = robust_frontier(max_n=4, k=1, sources=("css",), stop_on_pair=True)
        self.assertGreaterEqual(len(frontier.scans), 1)
        self.assertTrue(all(scan.source == "css" for scan in frontier.scans))

    def test_seed_pair_is_labeled_t2_robust_witness(self):
        first, second = seed_pair()
        self.assertTrue(code_quality(first, RobustConstraints()).passes)
        self.assertTrue(code_quality(second, RobustConstraints()).passes)
        self.assertEqual(first.entropy_vector(max_subset_size=2), second.entropy_vector(max_subset_size=2))
        self.assertNotEqual(first.reconstruction_profile(), second.reconstruction_profile())

    def test_witness_mechanism_summary(self):
        summary = witness_mechanism_summary()
        self.assertTrue(summary["same_labeled_t2_entropy"])
        self.assertTrue(summary["same_labeled_t2_local_stabilizer_ranks"])
        self.assertIn("changed_checks", summary)

    def test_lift_frontier_smoke(self):
        frontier = lift_frontier(max_balanced_supports=2, max_repeat_steps=0)
        self.assertGreater(frontier["total_candidates"], 0)
        self.assertIn("failure_counts", frontier)

    def test_bridge_family_certificate_one_step(self):
        certificate = bridge_family_certificate(max_steps=1)
        self.assertEqual(len(certificate["steps"]), 1)
        self.assertTrue(certificate["steps"][0]["is_family_step"])

    def test_bridge_theorem_certificate_one_step(self):
        certificate = bridge_theorem_certificate(max_exact_steps=1)
        self.assertEqual(certificate["family"]["n"], "6 + 2m")
        self.assertEqual(certificate["symbolic_witness_region"]["A_m_signature_on_R_m"], (1, 1, 1, False))
        self.assertTrue(certificate["symbolic_checker"]["all_checks_pass"])
        self.assertTrue(certificate["exact_prefix"]["steps"][0]["is_family_step"])

    def test_bridge_symbolic_proof_checker(self):
        certificate = bridge_symbolic_proof_check(sample_max_m=2)
        self.assertTrue(certificate["all_checks_pass"])
        self.assertTrue(certificate["checks"]["restricted_rank_cases"])
        self.assertTrue(certificate["checks"]["restricted_rank_schema"])
        self.assertTrue(certificate["checks"]["restricted_rank_formula_schema"])
        self.assertTrue(certificate["restricted_rank_schema"]["obligations"]["obligations_pass"])
        self.assertTrue(certificate["restricted_rank_formula_schema"]["passes"])
        self.assertTrue(
            all(
                sample["counts_match_formula"] and sample["all_regions_match_formula"]
                for sample in certificate["restricted_rank_formula_schema"]["prefix_formula_samples"]
            )
        )
        self.assertTrue(certificate["restricted_rank_schema"]["prefix_exhaustive_samples"][-1]["all_match"])
        self.assertIn("Restricted ranks for all one- and two-qubit subsets", certificate["proof_text"])

    def test_bridge_observer_cover_shape(self):
        cover = bridge_observer_cover(2)
        observer_p = cover.patch("observer_p")
        observer_q = cover.patch("observer_q")
        shared_horizon = cover.patch("shared_horizon")
        self.assertEqual(observer_p.region & observer_q.region, shared_horizon.region)
        self.assertEqual(shared_horizon.region.bit_count(), 3)

    def test_rank_kernel_diagnostics_match_small_exact_path(self):
        code = StabilizerCode.from_pauli_strings(["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"])
        for region in (0, 1, 0b101, 0b11101):
            self.assertEqual(rank_kernel_entropy(code, region), code.entropy(region))
            self.assertEqual(
                rank_kernel_algebra_summary(code, region)["signature"],
                code.region_algebra(region).signature(),
            )

    def test_cosmology_phase1_certificate(self):
        certificate = bridge_cosmology_phase1_certificate(max_m=2)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["recommendation"]["next_phase"], "adapt_then_proceed")
        for instance in certificate["instances"]:
            claims = instance["certified_claims"]
            self.assertTrue(claims["phase_1_static_patch_separation"])
            self.assertTrue(claims["same_patch_entropy_overlap_data"])
            self.assertTrue(claims["same_shared_horizon_algebra"])
            self.assertTrue(claims["different_observer_patch_reconstruction"])
            self.assertEqual(instance["witness"]["observer_p"]["first_signature"], (1, 1, 1, False))
            self.assertEqual(instance["witness"]["observer_p"]["second_signature"], (2, 0, 0, True))

    def test_cosmology_phase2_certificate(self):
        certificate = bridge_cosmology_phase2_certificate(max_m=2)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["recommendation"]["next_phase"], "proceed_as_written")
        slice_claims = certificate["slices"][0]["certified_claims"]
        self.assertTrue(slice_claims["phase_2_erasure_channel_probe"])
        self.assertTrue(slice_claims["same_erasure_correctability_profile"])
        self.assertTrue(slice_claims["private_shell_erasures_correctable"])
        self.assertTrue(slice_claims["shared_horizon_erasure_not_correctable"])
        self.assertTrue(slice_claims["observer_erasure_algebra_differs"])
        transition_claims = certificate["transitions"][0]["certified_claims"]
        self.assertTrue(transition_claims["phase_2_growth_transition"])
        self.assertTrue(transition_claims["shared_horizon_fixed"])
        self.assertTrue(transition_claims["observer_entropy_increments_by_one"])
        self.assertTrue(transition_claims["observer_pair_mi_increments_by_two"])

    def test_cosmology_phase3_certificate(self):
        certificate = bridge_cosmology_phase3_certificate(m=2, max_hits=1)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["recommendation"]["next_phase"], "adapt_then_proceed")
        self.assertGreaterEqual(certificate["counts"]["scanned"], 1)
        self.assertEqual(certificate["counts"]["hits_returned"], 1)
        hit = certificate["hits"][0]
        self.assertTrue(hit["certified_claims"]["causal_patch_search_hit"])
        self.assertTrue(hit["certified_claims"]["same_entropy_overlap_data"])
        self.assertTrue(hit["certified_claims"]["different_observer_reconstruction"])
        self.assertTrue(hit["certified_claims"]["same_erasure_correctability_profile"])

    def test_cosmology_phase4_certificate(self):
        certificate = bridge_cosmology_phase4_certificate(max_hits_per_pair=1)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["recommendation"]["next_phase"], "adapt_then_proceed")
        self.assertEqual(certificate["counts"]["pair_sources"], 2)
        self.assertEqual(certificate["counts"]["source_scans"], 4)
        self.assertGreaterEqual(certificate["counts"]["total_hits"], 1)
        seed_result = certificate["pair_results"][0]
        self.assertEqual(seed_result["source"]["name"], "seed_css_witness")
        self.assertEqual(seed_result["status"], "hit")
        hit = seed_result["hits"][0]
        self.assertTrue(hit["certified_claims"]["causal_patch_search_hit"])
        self.assertTrue(hit["certified_claims"]["same_entropy_overlap_data"])
        self.assertTrue(hit["certified_claims"]["different_observer_reconstruction"])
        self.assertTrue(hit["certified_claims"]["same_erasure_correctability_profile"])

    def test_cosmology_phase5_certificate(self):
        certificate = bridge_cosmology_phase5_certificate(
            max_bridge_m=1,
            max_cover_candidates=80,
            include_source_scans=False,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["recommendation"]["next_phase"], "adapt_then_proceed")
        self.assertTrue(certificate["certified_claims"]["phase_5_frontier_certificate"])
        self.assertTrue(certificate["certified_claims"]["cached_frontier_scored"])
        self.assertTrue(certificate["certified_claims"]["targeted_lifts_scored"])
        self.assertEqual(certificate["counts"]["targeted_lift_sources"], 1)
        self.assertGreaterEqual(certificate["counts"]["total_hits"], 1)
        self.assertEqual(certificate["frontier_results"][0]["source"]["name"], "seed_css_witness")
        self.assertEqual(certificate["frontier_results"][0]["status"], "hit")

    def test_cosmology_phase6_source_aware_certificate(self):
        certificate = bridge_cosmology_phase6_certificate(
            max_bridge_m=1,
            max_generic_candidates=0,
            include_calibration=False,
            include_source_scans=False,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["recommendation"]["next_phase"], "adapt_then_proceed")
        self.assertTrue(certificate["certified_claims"]["phase_6_source_aware_certificate"])
        self.assertTrue(certificate["certified_claims"]["source_aware_templates_used"])
        self.assertTrue(certificate["certified_claims"]["targeted_lift_hits_recovered"])
        self.assertEqual(certificate["counts"]["targeted_lift_sources"], 1)
        self.assertEqual(certificate["counts"]["source_aware_template_hits"], 1)
        self.assertEqual(certificate["counts"]["generic_template_hits"], 0)
        lift_result = certificate["frontier_results"][1]
        self.assertEqual(lift_result["source"]["name"], "balanced_bridge_lift_m1")
        self.assertEqual(lift_result["status"], "hit")
        self.assertEqual(lift_result["hits"][0]["template"]["kind"], "source_aware_bridge_observer")

    def test_cosmology_phase7_persistent_cache_certificate(self):
        certificate = bridge_cosmology_phase7_certificate(max_generic_candidates=0)
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(certificate["certified_claims"]["phase_7_persistent_cache_certificate"])
        self.assertTrue(certificate["certified_claims"]["all_cache_records_verified"])
        self.assertTrue(certificate["certified_claims"]["cache_matches_generator"])
        self.assertTrue(certificate["certified_claims"]["targeted_lift_hits_replayed_from_cache"])
        self.assertEqual(certificate["counts"]["cache_records"], 4)
        self.assertEqual(certificate["counts"]["targeted_lift_sources"], 2)
        self.assertEqual(certificate["counts"]["targeted_lift_source_aware_hits"], 2)
        self.assertEqual(certificate["counts"]["generic_template_hits"], 0)
        self.assertTrue(all(report["verified"] for report in certificate["cache_verification"]["record_reports"]))

    def test_cosmology_phase8_extended_frontier_certificate(self):
        certificate = bridge_cosmology_phase8_certificate(max_generic_candidates=0)
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(certificate["certified_claims"]["phase_8_extended_frontier_certificate"])
        self.assertTrue(certificate["certified_claims"]["all_cache_records_verified"])
        self.assertTrue(certificate["certified_claims"]["all_scan_records_verified"])
        self.assertTrue(certificate["certified_claims"]["graph_profile_calibration_pair_loaded"])
        self.assertTrue(certificate["certified_claims"]["graph_profile_pair_no_generic_causal_hit"])
        self.assertTrue(certificate["certified_claims"]["robust_non_css_scans_no_pair"])
        self.assertEqual(certificate["counts"]["cache_records"], 5)
        self.assertEqual(certificate["counts"]["scan_records"], 2)
        self.assertEqual(certificate["counts"]["graph_profile_calibration_records"], 1)
        self.assertEqual(certificate["counts"]["targeted_lift_source_aware_hits"], 2)
        self.assertTrue(all(report["verified"] for report in certificate["cache_verification"]["scan_record_reports"]))

    def test_cosmology_phase9_graph_template_no_go_certificate(self):
        certificate = bridge_cosmology_phase9_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(certificate["certified_claims"]["phase_9_graph_template_no_go_certificate"])
        self.assertTrue(certificate["certified_claims"]["graph_pair_is_profile_only_not_labeled_t2"])
        self.assertTrue(certificate["certified_claims"]["graph_specific_templates_no_hit"])
        self.assertTrue(certificate["certified_claims"]["exhaustive_two_observer_no_hit"])
        self.assertTrue(certificate["certified_claims"]["observer_reconstruction_differences_exist_in_exhaustive_space"])
        self.assertEqual(certificate["counts"]["graph_sources"], 1)
        self.assertEqual(certificate["counts"]["graph_template_hits"], 0)
        self.assertEqual(certificate["counts"]["exhaustive_two_observer_hits"], 0)
        self.assertGreater(certificate["counts"]["exhaustive_observer_reconstruction_differences"], 0)

    def test_cosmology_phase10_labeled_graph_atlas_certificate(self):
        certificate = bridge_cosmology_phase10_certificate(max_hits_per_source=2)
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(certificate["certified_claims"]["phase_10_labeled_graph_atlas_certificate"])
        self.assertTrue(certificate["certified_claims"]["strict_non_css_guardrail_no_pair"])
        self.assertTrue(certificate["certified_claims"]["labeled_graph_pair_found"])
        self.assertTrue(certificate["certified_claims"]["graph_metadata_preserved"])
        self.assertTrue(certificate["certified_claims"]["graph_pair_same_labeled_t2_entropy"])
        self.assertTrue(certificate["certified_claims"]["graph_pair_distance_one_caveat"])
        self.assertTrue(certificate["certified_claims"]["graph_native_templates_no_hit"])
        self.assertTrue(certificate["certified_claims"]["strict_horizon_private_atlas_hit"])
        self.assertTrue(certificate["certified_claims"]["strict_exhaustive_atlas_hit"])
        self.assertEqual(certificate["labeled_graph_search"]["status"], "pair-found")
        self.assertEqual(certificate["counts"]["graph_search_raw_codes"], 33)
        self.assertEqual(certificate["counts"]["graph_template_hits"], 0)
        self.assertGreater(certificate["counts"]["strict_horizon_private_hits"], 0)
        self.assertGreater(certificate["counts"]["strict_exhaustive_raw_hits"], 0)
        graph_metadata = certificate["labeled_graph_search"]["graph_metadata"]
        self.assertIn("edges", graph_metadata["first"])
        self.assertIn("deleted_graph_generator_indices", graph_metadata["second"])

    def test_cosmology_phase11_distance_repair_tension_certificate(self):
        certificate = bridge_cosmology_phase11_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(certificate["certified_claims"]["phase_11_distance_repair_tension_certificate"])
        self.assertTrue(certificate["certified_claims"]["distance_at_least_2_repaired"])
        self.assertTrue(certificate["certified_claims"]["same_labeled_t2_entropy_after_repair"])
        self.assertTrue(certificate["certified_claims"]["reconstruction_difference_after_repair"])
        self.assertTrue(certificate["certified_claims"]["lifted_phase10_atlas_near_misses_exist"])
        self.assertTrue(certificate["certified_claims"]["lifted_phase10_atlas_no_hit"])
        self.assertEqual(certificate["repaired_codes"]["n"], 20)
        self.assertEqual(certificate["repaired_codes"]["k"], 1)
        self.assertEqual(certificate["counts"]["low_order_subsets_checked"], 211)
        self.assertEqual(certificate["counts"]["low_order_entropy_mismatches"], 0)
        self.assertEqual(certificate["counts"]["lifted_atlas_candidates"], 525)
        self.assertGreater(certificate["counts"]["lifted_atlas_raw_hits"], 0)
        self.assertEqual(certificate["counts"]["lifted_atlas_hits_returned"], 0)
        self.assertIsNotNone(certificate["distance_repair"]["first"]["logical_witness"])
        self.assertIsNone(certificate["distance_repair"]["second"]["logical_witness"])

    def test_cosmology_phase12_atlas_aware_repaired_cover_certificate(self):
        certificate = bridge_cosmology_phase12_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(certificate["certified_claims"]["phase_12_atlas_aware_repaired_cover_certificate"])
        self.assertTrue(certificate["certified_claims"]["private_full_shared_inner_atlas_hit"])
        self.assertTrue(certificate["certified_claims"]["plain_inner_lift_representative_erasure_mismatch"])
        self.assertTrue(certificate["certified_claims"]["full_outer_block_control_no_observer_difference"])
        self.assertEqual(certificate["counts"]["low_order_subsets_checked"], 211)
        self.assertEqual(certificate["counts"]["low_order_entropy_mismatches"], 0)
        self.assertEqual(certificate["counts"]["atlas_aware_candidates"], 525)
        self.assertEqual(certificate["counts"]["full_outer_control_candidates"], 175)
        self.assertEqual(certificate["counts"]["full_outer_control_raw_hits"], 0)
        self.assertEqual(certificate["counts"]["inner_lift_raw_hits"], 72)
        self.assertEqual(certificate["counts"]["private_full_shared_inner_raw_hits"], 66)
        self.assertEqual(certificate["counts"]["private_full_shared_inner_hits"], 1)
        hit = certificate["atlas_aware_repaired_search"]["hits"][0]
        self.assertTrue(hit["certified_claims"]["causal_patch_search_hit"])
        self.assertEqual(hit["template"]["kind"], "phase12_private_full_shared_inner")
        self.assertEqual(hit["template"]["observer_p_block_mask"], 1)
        self.assertEqual(hit["template"]["observer_q_block_mask"], 13)
        near_miss = certificate["atlas_aware_repaired_search"]["representative_near_misses"][0]
        self.assertFalse(near_miss["certified_claims"]["same_erasure_correctability_profile"])

    def test_cosmology_phase13_repaired_cover_dynamics_certificate(self):
        certificate = bridge_cosmology_phase13_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(certificate["certified_claims"]["phase_13_repaired_cover_dynamics_certificate"])
        transition_claims = certificate["timeline"]["transition"]["certified_claims"]
        self.assertTrue(transition_claims["phase_13_repaired_cover_transition"])
        self.assertTrue(transition_claims["observer_p_region_stable"])
        self.assertTrue(transition_claims["shared_horizon_region_stable"])
        self.assertTrue(transition_claims["observer_q_promotes_private_outer_blocks_2_3"])
        self.assertTrue(transition_claims["observer_q_drops_plain_inner_block_1_qubits"])
        near_slice, hit_slice = certificate["timeline"]["slices"]
        self.assertFalse(near_slice["certified_claims"]["causal_patch_search_hit"])
        self.assertFalse(near_slice["certified_claims"]["same_erasure_correctability_profile"])
        self.assertTrue(hit_slice["certified_claims"]["causal_patch_search_hit"])
        self.assertTrue(hit_slice["certified_claims"]["same_erasure_correctability_profile"])
        self.assertEqual(certificate["counts"]["near_slice_algebra_difference_scenarios"], 4)
        self.assertEqual(certificate["counts"]["hit_slice_algebra_difference_scenarios"], 2)
        self.assertEqual(certificate["counts"]["observer_q_added_qubits"], 10)
        self.assertEqual(certificate["counts"]["observer_q_removed_qubits"], 2)
        baseline = certificate["css_baseline_comparison"]
        self.assertTrue(baseline["certified_claims"]["phase_13_css_baseline_comparison"])
        self.assertFalse(baseline["css_shared_horizon_erasure_correctable"])
        self.assertTrue(baseline["repaired_hit_shared_horizon_erasure_correctable"])

    def test_cosmology_phase14_transition_graph_certificate(self):
        certificate = bridge_cosmology_phase14_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_14_transition_graph_certificate"])
        self.assertTrue(claims["near_to_hit_path_found"])
        self.assertTrue(claims["path_edges_are_small_patch_edits"])
        self.assertTrue(claims["path_repairs_erasure_correctability_profile"])
        self.assertTrue(claims["path_changes_erasure_algebra_difference_set"])
        self.assertTrue(claims["shared_horizon_semantics_stable_within_repaired_flow"])
        self.assertTrue(claims["shared_horizon_semantics_differs_from_css_baseline"])
        self.assertEqual(certificate["counts"]["nodes"], 24)
        self.assertGreater(certificate["counts"]["edges"], 0)
        self.assertEqual(certificate["path_search"]["path_node_ids"][0], "inner:p1:q3")
        self.assertEqual(certificate["path_search"]["path_node_ids"][-1], "private:p1:q13")
        self.assertGreaterEqual(certificate["counts"]["path_length_edges"], 3)
        shared = certificate["role_semantics"]["shared_horizon"]
        self.assertTrue(shared["stable_within_repaired_flow"])
        self.assertFalse(shared["hit_agrees_with_css_baseline"])

    def test_cosmology_phase15_multi_source_flow_invariant_certificate(self):
        certificate = bridge_cosmology_phase15_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_15_multi_source_flow_invariant_certificate"])
        self.assertTrue(claims["multiple_source_graphs_classified"])
        self.assertTrue(claims["all_classified_nodes_have_exact_qec_identity"])
        self.assertTrue(claims["shared_horizon_semantics_differs_between_css_and_repaired_paths"])
        self.assertTrue(claims["repaired_full_graph_detects_role_semantics_not_global_invariant"])
        self.assertTrue(claims["algebra_difference_counts_nonincreasing_on_all_canonical_paths"])
        self.assertEqual(certificate["counts"]["source_graphs"], 3)
        self.assertEqual(certificate["counts"]["total_nodes"], 36)
        self.assertEqual(certificate["counts"]["css_m2_nodes"], 4)
        self.assertEqual(certificate["counts"]["css_m3_nodes"], 8)
        self.assertEqual(certificate["counts"]["repaired_nodes"], 24)
        shared_profiles = dict(certificate["cross_model_classification"]["shared_horizon_path_correctability_profiles"])
        self.assertEqual(shared_profiles["css_bridge_orientation_m2"], ((False, False),))
        self.assertEqual(shared_profiles["css_bridge_orientation_m3"], ((False, False),))
        self.assertEqual(shared_profiles["repaired_noncss_phase14_neighborhood"], ((True, True),))

    def test_cosmology_phase16_mixed_code_cover_graph_certificate(self):
        certificate = bridge_cosmology_phase16_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_16_mixed_code_cover_graph_certificate"])
        self.assertTrue(claims["growth_edges_certified"])
        self.assertTrue(claims["canonical_path_uses_growth_edges"])
        self.assertTrue(claims["shared_horizon_correctability_stable_across_mixed_graph"])
        self.assertTrue(claims["algebra_difference_count_flat_across_mixed_graph"])
        self.assertEqual(certificate["counts"]["nodes"], 14)
        self.assertEqual(certificate["counts"]["edges"], 29)
        self.assertEqual(certificate["counts"]["orientation_edges"], 17)
        self.assertEqual(certificate["counts"]["growth_edges"], 12)
        self.assertEqual(certificate["counts"]["path_growth_edges"], 2)
        self.assertEqual(certificate["counts"]["path_cover_orientation_edges"], 1)
        self.assertEqual(certificate["path_search"]["path_node_ids"][0], "mixed_css:m1:o0")
        self.assertEqual(certificate["path_search"]["path_node_ids"][-1], "mixed_css:m3:o111")
        shared = certificate["path_invariants"]["shared_horizon"]
        self.assertEqual(shared["correctability_unique_profiles"], ((False, False),))

    def test_cosmology_phase17_noncss_local_clifford_flow_certificate(self):
        certificate = bridge_cosmology_phase17_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_17_noncss_local_clifford_flow_certificate"])
        self.assertTrue(claims["local_clifford_edges_certified"])
        self.assertTrue(claims["lc_generators_actually_change"])
        self.assertTrue(claims["shared_horizon_correctability_stable_across_lc_graph"])
        self.assertTrue(claims["repaired_lc_horizon_semantics_differs_from_css_mixed_baseline"])
        self.assertEqual(certificate["counts"]["nodes"], 4)
        self.assertEqual(certificate["counts"]["edges"], 4)
        self.assertEqual(certificate["counts"]["path_length_edges"], 2)
        self.assertEqual(certificate["path_search"]["path_node_ids"][0], "repaired_lc:h0:s0")
        self.assertEqual(certificate["path_search"]["path_node_ids"][-1], "repaired_lc:h1:s1")
        self.assertEqual(
            certificate["css_mixed_baseline_comparison"]["css_shared_horizon_path_correctability"],
            ((False, False),),
        )
        self.assertEqual(
            certificate["css_mixed_baseline_comparison"]["repaired_lc_shared_horizon_path_correctability"],
            ((True, True),),
        )

    def test_cosmology_phase18_outer_code_swap_taxonomy_certificate(self):
        certificate = bridge_cosmology_phase18_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_18_outer_code_swap_taxonomy_certificate"])
        self.assertTrue(claims["outer_swap_edges_certified"])
        self.assertTrue(claims["same_class_preserving_swap_exists"])
        self.assertTrue(claims["same_class_collapsing_swap_exists"])
        self.assertTrue(claims["distinct_class_entropy_break_exists"])
        self.assertTrue(claims["shared_horizon_correctability_stable_across_outer_swaps"])
        self.assertEqual(certificate["counts"]["nodes"], 4)
        self.assertEqual(certificate["counts"]["edges"], 3)
        self.assertEqual(certificate["counts"]["outer_local_clifford_classes"], 2)
        self.assertEqual(certificate["counts"]["full_semantics_preserving_targets"], 1)
        self.assertEqual(certificate["counts"]["operator_geometry_collapsing_targets"], 1)
        self.assertEqual(certificate["counts"]["low_order_entropy_breaking_targets"], 1)
        taxonomy = {item["target"]: item["outcome"] for item in certificate["swap_taxonomy"]}
        self.assertEqual(taxonomy["same_class_preserve"], "full_semantics_preserved")
        self.assertEqual(taxonomy["same_class_collapse"], "operator_geometry_collapsed")
        self.assertEqual(taxonomy["distinct_class_entropy_break"], "low_order_entropy_break")

    def test_cosmology_phase19_bounded_outer_mutation_search_certificate(self):
        certificate = bridge_cosmology_phase19_certificate(max_radius=2)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_19_bounded_outer_mutation_search_certificate"])
        self.assertTrue(claims["mutation_edges_certified"])
        self.assertTrue(claims["phase18_major_buckets_recovered_by_search"])
        self.assertTrue(claims["radius_one_search_has_no_entropy_break"])
        self.assertTrue(claims["radius_two_search_finds_entropy_break"])
        self.assertTrue(claims["entropy_break_with_reconstruction_survival_exists"])
        self.assertTrue(claims["shared_horizon_correctability_stable_across_mutations"])
        self.assertEqual(certificate["counts"]["accepted_mutation_nodes"], 37)
        self.assertEqual(certificate["counts"]["full_semantics_preserving_targets"], 25)
        self.assertEqual(certificate["counts"]["operator_geometry_collapsing_targets"], 8)
        self.assertEqual(certificate["counts"]["low_order_entropy_breaking_targets"], 4)
        self.assertEqual(certificate["counts"]["low_order_entropy_break_with_reconstruction_survives_targets"], 2)
        radius_counts = {
            item["radius"]: dict(item["outcome_counts"]) for item in certificate["radius_outcome_counts"]
        }
        self.assertEqual(radius_counts[1].get("full_semantics_preserved"), 5)
        self.assertEqual(radius_counts[1].get("operator_geometry_collapsed"), 1)
        self.assertEqual(radius_counts[1].get("low_order_entropy_break_with_operator_collapse"), 0)
        self.assertEqual(radius_counts[1].get("low_order_entropy_break_with_reconstruction_survives"), 0)
        self.assertEqual(radius_counts[2].get("low_order_entropy_break_with_operator_collapse"), 2)
        self.assertEqual(radius_counts[2].get("low_order_entropy_break_with_reconstruction_survives"), 2)

    def test_cosmology_phase20_inner_graph_mutation_search_certificate(self):
        certificate = bridge_cosmology_phase20_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_20_inner_graph_mutation_search_certificate"])
        self.assertTrue(claims["radius_one_graph_edge_ball_enumerated"])
        self.assertTrue(claims["inner_graph_mutation_edges_certified"])
        self.assertTrue(claims["shared_horizon_correctability_stable_across_inner_graph_mutations"])
        self.assertTrue(claims["inner_radius_one_finds_entropy_breaks"])
        self.assertTrue(claims["inner_radius_one_differs_from_outer_radius_one_entropy_break_behavior"])
        self.assertTrue(claims["inner_radius_one_has_extra_algebra_buckets"])
        self.assertEqual(certificate["counts"]["accepted_mutation_nodes"], 20)
        self.assertEqual(certificate["counts"]["full_semantics_preserving_targets"], 4)
        self.assertEqual(certificate["counts"]["operator_geometry_collapsing_targets"], 2)
        self.assertEqual(certificate["counts"]["low_order_entropy_breaking_targets"], 13)
        self.assertEqual(certificate["counts"]["observer_reconstruction_signal_targets"], 9)
        self.assertEqual(certificate["counts"]["entropy_break_operator_collapsed_algebra_residue_targets"], 9)
        self.assertEqual(certificate["counts"]["entropy_preserved_reconstruction_extra_algebra_targets"], 1)
        self.assertEqual(certificate["counts"]["entropy_break_reconstruction_extra_algebra_targets"], 1)
        buckets = {item["outcome"]: item["count"] for item in certificate["bucket_summary"]}
        self.assertEqual(buckets["full_semantics_preserved"], 4)
        self.assertEqual(buckets["operator_geometry_collapsed"], 2)
        self.assertEqual(buckets["low_order_entropy_break_with_reconstruction_survives"], 3)
        self.assertEqual(buckets["entropy_break_operator_collapsed_algebra_residue"], 9)
        outer_radius_one = dict(
            certificate["phase19_outer_mutation_comparison"]["radius_outcome_counts"][0]["outcome_counts"]
        )
        self.assertEqual(outer_radius_one["full_semantics_preserved"], 5)
        self.assertEqual(outer_radius_one["operator_geometry_collapsed"], 1)
        self.assertEqual(outer_radius_one["low_order_entropy_break_with_operator_collapse"], 0)
        self.assertEqual(outer_radius_one["low_order_entropy_break_with_reconstruction_survives"], 0)

    def test_cosmology_phase21_mixed_inner_outer_transition_graph_certificate(self):
        certificate = bridge_cosmology_phase21_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_21_mixed_inner_outer_transition_graph_certificate"])
        self.assertTrue(claims["mixed_product_nodes_scored"])
        self.assertTrue(claims["mixed_axis_edges_certified"])
        self.assertTrue(claims["commuting_squares_certified"])
        self.assertTrue(claims["all_nodes_reachable_within_two_steps"])
        self.assertTrue(claims["shared_horizon_correctability_stable_across_mixed_graph"])
        self.assertTrue(claims["algebra_difference_monotonicity_failures_exist"])
        self.assertEqual(certificate["counts"]["nodes"], 49)
        self.assertEqual(certificate["counts"]["edges"], 84)
        self.assertEqual(certificate["counts"]["commuting_squares"], 36)
        self.assertEqual(certificate["counts"]["algebra_increase_edges"], 14)
        self.assertEqual(certificate["counts"]["algebra_decrease_edges"], 11)
        self.assertEqual(certificate["counts"]["algebra_flat_edges"], 59)
        self.assertEqual(certificate["counts"]["entropy_match_flip_edges"], 21)
        self.assertEqual(certificate["counts"]["observer_signal_flip_edges"], 17)
        outcomes = dict(certificate["classification"]["node_outcome_counts"])
        self.assertEqual(outcomes["full_semantics_preserved"], 12)
        self.assertEqual(outcomes["operator_geometry_collapsed"], 10)
        self.assertEqual(outcomes["entropy_break_operator_collapsed_algebra_residue"], 7)
        self.assertEqual(outcomes["low_order_entropy_break_with_operator_collapse"], 2)
        edge_types = dict(certificate["classification"]["edge_type_counts"])
        self.assertEqual(edge_types["inner_graph_toggle"], 42)
        self.assertEqual(edge_types["outer_repair_mutation"], 42)
        self.assertEqual(certificate["reachability"]["max_distance"], 2)

    def test_cosmology_phase22_exact_time_channel_certificate(self):
        certificate = bridge_cosmology_phase22_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_22_exact_time_channel_certificate"])
        self.assertTrue(claims["random_walk_stationary_distribution_verified_exactly"])
        self.assertTrue(claims["algebra_descent_absorption_probabilities_verified_exactly"])
        self.assertTrue(claims["algebra_descent_is_nonincreasing"])
        self.assertTrue(claims["algebra_descent_detects_nonzero_local_minima"])
        self.assertTrue(claims["horizon_fixed_point_invariant_under_both_channels"])
        self.assertEqual(certificate["counts"]["nodes"], 49)
        self.assertEqual(certificate["counts"]["phase21_edges"], 84)
        self.assertEqual(certificate["counts"]["random_walk_positive_transitions"], 168)
        self.assertEqual(certificate["counts"]["descent_positive_transitions"], 53)
        self.assertEqual(certificate["counts"]["absorbing_nodes"], 28)
        self.assertEqual(certificate["counts"]["absorbing_algebra_counts"], (0, 2))
        random_walk_weights = {
            item["key"]: item["weight"]["string"]
            for item in certificate["channels"]["uniform_edge_random_walk"]["stationary_bucket_weights"]
        }
        self.assertEqual(random_walk_weights["full_semantics_preserved"], "8/21")
        self.assertEqual(random_walk_weights["operator_geometry_collapsed"], "5/28")
        descent_weights = {
            item["key"]: item["weight"]["string"]
            for item in certificate["channels"]["algebra_descent_channel"][
                "uniform_initial_absorbing_bucket_weights"
            ]
        }
        self.assertEqual(descent_weights["operator_geometry_collapsed"], "29/49")
        self.assertEqual(descent_weights["entropy_break_operator_collapsed_algebra_residue"], "13/98")

    def test_cosmology_phase23_biased_channel_comparison_certificate(self):
        certificate = bridge_cosmology_phase23_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_23_biased_channel_comparison_certificate"])
        self.assertTrue(claims["all_biased_walk_transition_matrices_are_exact_stochastic"])
        self.assertTrue(claims["all_biased_walk_stationary_distributions_verified_exactly"])
        self.assertTrue(claims["all_biased_walk_stationary_formulas_use_symmetric_edge_weights"])
        self.assertTrue(claims["stationary_bucket_weights_rule_dependent"])
        self.assertTrue(claims["absorbing_classes_rule_dependent"])
        self.assertTrue(claims["horizon_fixed_point_invariant_across_channel_family"])
        self.assertEqual(certificate["counts"]["nodes"], 49)
        self.assertEqual(certificate["counts"]["phase21_edges"], 84)
        self.assertEqual(certificate["counts"]["biased_walk_channels"], 4)
        self.assertEqual(certificate["counts"]["rule_dependent_stationary_buckets"], 7)
        self.assertEqual(certificate["counts"]["rule_invariant_stationary_buckets"], 0)
        self.assertEqual(certificate["counts"]["biased_walk_closed_class_counts"], (1, 1, 1, 1))
        self.assertEqual(certificate["counts"]["biased_walk_absorbing_node_counts"], (0, 0, 0, 0))
        self.assertEqual(certificate["counts"]["algebra_descent_closed_classes"], 28)
        self.assertEqual(certificate["counts"]["algebra_descent_absorbing_nodes"], 28)
        full_semantics = {
            item["channel"]: item["weight"]["string"]
            for row in certificate["comparison"]["stationary_bucket_weight_table"]
            if row["bucket"] == "full_semantics_preserved"
            for item in row["weights_by_channel"]
        }
        self.assertEqual(full_semantics["uniform_edge_random_walk"], "8/21")
        self.assertEqual(full_semantics["entropy_match_preserving_bias"], "55/147")
        self.assertEqual(full_semantics["observer_signal_preserving_bias"], "57/151")
        self.assertEqual(full_semantics["algebra_flat_bias"], "54/143")
        operator_collapse = {
            item["channel"]: item["weight"]["string"]
            for row in certificate["comparison"]["stationary_bucket_weight_table"]
            if row["bucket"] == "operator_geometry_collapsed"
            for item in row["weights_by_channel"]
        }
        self.assertEqual(operator_collapse["uniform_edge_random_walk"], "5/28")
        self.assertEqual(operator_collapse["entropy_match_preserving_bias"], "19/98")
        self.assertEqual(operator_collapse["observer_signal_preserving_bias"], "51/302")
        self.assertEqual(operator_collapse["algebra_flat_bias"], "25/143")

    def test_cosmology_phase24_bounded_channel_rule_search_certificate(self):
        certificate = bridge_cosmology_phase24_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_24_bounded_channel_rule_search_certificate"])
        self.assertTrue(claims["weighted_edge_rule_search_space_exactly_bounded"])
        self.assertTrue(claims["all_weighted_walk_stationary_distributions_verified_exactly"])
        self.assertTrue(claims["positive_symmetric_walk_absorbing_no_go"])
        self.assertTrue(claims["descent_absorbing_yes_go"])
        self.assertTrue(claims["descent_absorbing_structure_rule_dependent"])
        self.assertTrue(claims["horizon_fixed_point_invariant_across_searched_rules"])
        self.assertEqual(certificate["counts"]["nodes"], 49)
        self.assertEqual(certificate["counts"]["phase21_edges"], 84)
        self.assertEqual(certificate["counts"]["weighted_walk_rules"], 27)
        self.assertEqual(certificate["counts"]["score_descent_rules"], 7)
        self.assertEqual(certificate["counts"]["weighted_walk_closed_class_counts"], (1,))
        self.assertEqual(certificate["counts"]["weighted_walk_absorbing_node_counts"], (0,))
        self.assertEqual(certificate["counts"]["score_descent_absorbing_node_count_range"], (28, 42))
        self.assertEqual(certificate["counts"]["stationary_extrema_buckets"], 7)
        weighted_extrema = {
            item["bucket"]: item for item in certificate["comparison"]["weighted_walk_stationary_bucket_extrema"]
        }
        self.assertEqual(weighted_extrema["full_semantics_preserved"]["minimum"]["weight"]["string"], "13/35")
        self.assertEqual(weighted_extrema["full_semantics_preserved"]["minimum"]["rules"], ("edge_bonus_e2_o0_a0",))
        self.assertEqual(weighted_extrema["full_semantics_preserved"]["maximum"]["weight"]["string"], "8/21")
        self.assertEqual(weighted_extrema["full_semantics_preserved"]["maximum"]["rules"], ("edge_bonus_e0_o0_a0",))
        self.assertEqual(weighted_extrema["operator_geometry_collapsed"]["minimum"]["weight"]["string"], "18/109")
        self.assertEqual(weighted_extrema["operator_geometry_collapsed"]["minimum"]["rules"], ("edge_bonus_e0_o2_a0",))
        self.assertEqual(weighted_extrema["operator_geometry_collapsed"]["maximum"]["weight"]["string"], "1/5")
        self.assertEqual(weighted_extrema["operator_geometry_collapsed"]["maximum"]["rules"], ("edge_bonus_e2_o0_a0",))
        descent_extrema = certificate["comparison"]["score_descent_absorbing_node_extrema"]
        self.assertEqual(descent_extrema["minimum_absorbing_nodes"]["count"], 28)
        self.assertEqual(
            descent_extrema["minimum_absorbing_nodes"]["rules"],
            ("score_descent_a1_e0_o0", "score_descent_a1_e0_o1"),
        )
        self.assertEqual(descent_extrema["maximum_absorbing_nodes"]["count"], 42)
        self.assertEqual(descent_extrema["maximum_absorbing_nodes"]["rules"], ("score_descent_a0_e1_o0",))
        descent_bucket_extrema = {
            item["bucket"]: item
            for item in certificate["comparison"]["score_descent_absorbing_bucket_weight_extrema"]
        }
        self.assertEqual(descent_bucket_extrema["operator_geometry_collapsed"]["minimum"]["weight"]["string"], "9/49")
        self.assertEqual(descent_bucket_extrema["operator_geometry_collapsed"]["maximum"]["weight"]["string"], "29/49")

    def test_cosmology_phase25_target_constrained_channel_synthesis_certificate(self):
        certificate = bridge_cosmology_phase25_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_25_target_constrained_channel_synthesis_certificate"])
        self.assertTrue(claims["target_synthesis_rule_space_exactly_bounded"])
        self.assertTrue(claims["all_synthesis_candidates_satisfy_horizon_and_observer_constraints"])
        self.assertTrue(claims["target_gap_objectives_exactly_certified"])
        self.assertTrue(claims["pareto_frontier_certified_exactly"])
        self.assertTrue(claims["pareto_frontier_contains_tradeoffs"])
        self.assertTrue(claims["target_synthesis_detects_signed_gap_no_go"])
        self.assertEqual(certificate["counts"]["nodes"], 49)
        self.assertEqual(certificate["counts"]["phase21_edges"], 84)
        self.assertEqual(certificate["counts"]["candidate_rules"], 27)
        self.assertEqual(certificate["counts"]["target_gap_objectives"], 6)
        self.assertEqual(certificate["counts"]["unique_minimal_target_witness_rules"], 3)
        self.assertEqual(certificate["counts"]["nonuniform_minimal_target_witness_rules"], 3)
        self.assertFalse(certificate["counts"]["uniform_is_minimal_for_at_least_one_target"])
        self.assertEqual(certificate["counts"]["negative_gap_objectives"], 2)
        self.assertEqual(certificate["counts"]["pareto_frontier_rules"], 7)
        self.assertEqual(certificate["counts"]["pareto_frontier_metric_vectors"], 7)
        self.assertEqual(certificate["counts"]["pareto_dominated_rules"], 20)
        witnesses = {item["objective"]["name"]: item for item in certificate["target_gap_witnesses"]}
        self.assertEqual(witnesses["prefer_full_semantics_over_entropy_break"]["max_gap"]["string"], "9/140")
        self.assertEqual(
            witnesses["prefer_full_semantics_over_entropy_break"]["all_maximizing_rules"],
            ("edge_bonus_e2_o0_a0",),
        )
        self.assertEqual(witnesses["prefer_full_semantics_over_operator_collapse"]["max_gap"]["string"], "39/436")
        self.assertEqual(
            witnesses["prefer_full_semantics_over_operator_collapse"]["all_maximizing_rules"],
            ("edge_bonus_e0_o2_a0",),
        )
        self.assertEqual(witnesses["prefer_entropy_break_over_full_semantics"]["max_gap"]["string"], "-7/404")
        self.assertEqual(
            witnesses["prefer_entropy_break_over_full_semantics"]["all_maximizing_rules"],
            ("edge_bonus_e0_o0_a2",),
        )
        self.assertEqual(witnesses["prefer_operator_collapse_over_entropy_break"]["max_gap"]["string"], "1/70")
        self.assertEqual(
            witnesses["prefer_operator_collapse_over_entropy_break"]["all_maximizing_rules"],
            ("edge_bonus_e2_o0_a0",),
        )
        frontier = certificate["pareto_frontier"]
        frontier_rules = set(frontier["frontier_rules"])
        self.assertEqual(len(frontier_rules), 7)
        self.assertIn("edge_bonus_e0_o0_a0", frontier_rules)
        self.assertIn("edge_bonus_e2_o0_a2", frontier_rules)
        first_vector = frontier["frontier_metric_vectors"][0]
        self.assertEqual(first_vector["metrics"]["full_semantics"]["string"], "61/164")
        self.assertEqual(first_vector["metrics"]["entropy_break"]["string"], "217/656")
        self.assertEqual(first_vector["metrics"]["operator_collapse"]["string"], "211/656")
        self.assertEqual(
            first_vector["minimal_rule_witnesses"][0]["rule"]["name"],
            "edge_bonus_e2_o0_a2",
        )

    def test_cosmology_phase26_cross_substrate_channel_rule_transfer_certificate(self):
        certificate = bridge_cosmology_phase26_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_26_cross_substrate_channel_rule_transfer_certificate"])
        self.assertTrue(claims["all_transfer_substrates_certified"])
        self.assertTrue(claims["baseline_reproduces_phase25_target_synthesis"])
        self.assertTrue(claims["target_transfer_successes_detected"])
        self.assertTrue(claims["target_no_transfer_counterexamples_detected"])
        self.assertTrue(claims["pareto_transfer_changes_detected"])
        self.assertTrue(claims["horizon_invariant_across_transfer_substrates"])
        self.assertEqual(certificate["counts"]["substrates"], 4)
        self.assertEqual(certificate["counts"]["nonbaseline_substrates"], 3)
        self.assertEqual(certificate["counts"]["candidate_rules"], 27)
        self.assertEqual(certificate["counts"]["target_transfer_records"], 18)
        self.assertEqual(certificate["counts"]["target_transfer_successes"], 16)
        self.assertEqual(certificate["counts"]["target_no_transfer_counterexamples"], 2)
        self.assertEqual(certificate["counts"]["pareto_changed_substrates"], 3)
        substrate_by_name = {
            item["name"]: item for item in certificate["substrate_transfer_analyses"]
        }
        self.assertEqual(substrate_by_name["full_mixed_graph"]["counts"]["edges"], 84)
        self.assertEqual(substrate_by_name["entropy_stable_edges"]["counts"]["edges"], 63)
        self.assertEqual(substrate_by_name["observer_signal_stable_edges"]["counts"]["edges"], 67)
        self.assertEqual(substrate_by_name["algebra_flat_edges"]["counts"]["edges"], 59)
        self.assertEqual(substrate_by_name["algebra_flat_edges"]["counts"]["isolated_nodes"], 1)
        entropy_records = {
            item["objective"]["name"]: item
            for item in substrate_by_name["entropy_stable_edges"]["target_transfer"]
        }
        self.assertTrue(
            entropy_records["prefer_full_semantics_over_entropy_break"][
                "baseline_witness_transfers_as_maximizer"
            ]
        )
        self.assertFalse(
            entropy_records["prefer_entropy_break_over_operator_collapse"][
                "baseline_witness_transfers_as_maximizer"
            ]
        )
        self.assertEqual(
            entropy_records["prefer_entropy_break_over_operator_collapse"]["substrate_max_gap"]["string"],
            "3/514",
        )
        self.assertEqual(
            entropy_records["prefer_entropy_break_over_operator_collapse"]["substrate_all_maximizing_rules"],
            ("edge_bonus_e0_o2_a2",),
        )
        signal_records = {
            item["objective"]["name"]: item
            for item in substrate_by_name["observer_signal_stable_edges"]["target_transfer"]
        }
        self.assertFalse(
            signal_records["prefer_operator_collapse_over_full_semantics"][
                "baseline_witness_transfers_as_maximizer"
            ]
        )
        self.assertEqual(
            signal_records["prefer_operator_collapse_over_full_semantics"]["substrate_max_gap"]["string"],
            "-13/173",
        )
        self.assertEqual(
            signal_records["prefer_operator_collapse_over_full_semantics"]["substrate_all_maximizing_rules"],
            ("edge_bonus_e0_o0_a2",),
        )
        algebra_pareto = substrate_by_name["algebra_flat_edges"]["pareto_transfer"]
        self.assertEqual(
            algebra_pareto["lost_baseline_frontier_rules"],
            ("edge_bonus_e1_o0_a0", "edge_bonus_e1_o0_a1", "edge_bonus_e1_o0_a2", "edge_bonus_e2_o0_a2"),
        )
        self.assertEqual(algebra_pareto["new_substrate_frontier_rules"], ())

    def test_cosmology_phase27_multi_substrate_robust_channel_synthesis_certificate(self):
        certificate = bridge_cosmology_phase27_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_27_multi_substrate_robust_channel_synthesis_certificate"])
        self.assertTrue(claims["robust_substrate_family_certified"])
        self.assertTrue(claims["robust_rule_space_exactly_bounded"])
        self.assertTrue(claims["robust_target_objectives_exactly_certified"])
        self.assertTrue(claims["robust_pareto_frontier_certified"])
        self.assertTrue(claims["robust_synthesis_finds_positive_worst_case_gap"])
        self.assertTrue(claims["robust_synthesis_detects_worst_case_no_go"])
        self.assertTrue(claims["horizon_invariant_across_robust_substrates"])
        self.assertEqual(certificate["counts"]["substrates"], 4)
        self.assertEqual(certificate["counts"]["candidate_rules"], 27)
        self.assertEqual(certificate["counts"]["robust_target_objectives"], 6)
        self.assertEqual(certificate["counts"]["unique_minimal_robust_witness_rules"], 4)
        self.assertEqual(certificate["counts"]["positive_worst_case_objectives"], 3)
        self.assertEqual(certificate["counts"]["negative_worst_case_objectives"], 3)
        self.assertEqual(certificate["counts"]["robust_pareto_frontier_rules"], 17)
        self.assertEqual(certificate["counts"]["robust_pareto_frontier_metric_vectors"], 17)
        self.assertEqual(certificate["counts"]["robust_pareto_dominated_rules"], 10)
        witnesses = {item["objective"]["name"]: item for item in certificate["robust_target_gap_witnesses"]}
        self.assertEqual(witnesses["prefer_full_semantics_over_entropy_break"]["max_worst_case_gap"]["string"], "2/149")
        self.assertEqual(
            witnesses["prefer_full_semantics_over_entropy_break"]["all_robust_maximizing_rules"],
            ("edge_bonus_e2_o0_a0",),
        )
        self.assertEqual(
            witnesses["prefer_full_semantics_over_operator_collapse"]["max_worst_case_gap"]["string"],
            "3/55",
        )
        self.assertEqual(
            witnesses["prefer_full_semantics_over_operator_collapse"]["all_robust_maximizing_rules"],
            ("edge_bonus_e0_o2_a0",),
        )
        self.assertEqual(witnesses["prefer_entropy_break_over_full_semantics"]["max_worst_case_gap"]["string"], "-7/153")
        self.assertEqual(
            witnesses["prefer_entropy_break_over_full_semantics"]["all_robust_maximizing_rules"],
            ("edge_bonus_e0_o0_a2",),
        )
        self.assertEqual(
            witnesses["prefer_entropy_break_over_operator_collapse"]["max_worst_case_gap"]["string"],
            "3/514",
        )
        self.assertEqual(
            witnesses["prefer_entropy_break_over_operator_collapse"]["all_robust_maximizing_rules"],
            ("edge_bonus_e0_o2_a2",),
        )
        operator_entropy = witnesses["prefer_operator_collapse_over_entropy_break"]
        self.assertEqual(operator_entropy["max_worst_case_gap"]["string"], "-5/114")
        self.assertEqual(operator_entropy["all_robust_maximizing_rules"], ("edge_bonus_e2_o0_a0",))
        robust_gaps = {
            item["substrate"]: item["gap"]["string"]
            for item in operator_entropy["minimal_robust_rule_witnesses"][0]["gaps_by_substrate"]
        }
        self.assertEqual(robust_gaps["observer_signal_stable_edges"], "-5/114")
        frontier = certificate["robust_pareto_frontier"]
        self.assertEqual(frontier["frontier_rule_count"], 17)
        frontier_rules = set(frontier["frontier_rules"])
        self.assertIn("edge_bonus_e0_o0_a2", frontier_rules)
        self.assertIn("edge_bonus_e2_o2_a2", frontier_rules)
        first_vector = frontier["frontier_metric_vectors"][0]
        self.assertEqual(first_vector["metrics"]["full_semantics"]["string"], "55/153")
        self.assertEqual(first_vector["metrics"]["entropy_break"]["string"], "16/51")
        self.assertEqual(first_vector["metrics"]["operator_collapse"]["string"], "50/173")
        self.assertEqual(first_vector["minimal_rule_witnesses"][0]["rule"]["name"], "edge_bonus_e0_o0_a2")

    def test_cosmology_phase28_audited_rule_language_proof_certificate(self):
        certificate = bridge_cosmology_phase28_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_28_audited_rule_language_proof_certificate"])
        self.assertTrue(claims["phase27_robust_synthesis_certified"])
        self.assertTrue(claims["rule_language_schema_covers_exact_enumeration"])
        self.assertTrue(claims["feature_conditions_select_exact_robust_maximizers"])
        self.assertTrue(claims["sign_classification_matches_exact_worst_case_gaps"])
        self.assertTrue(claims["positive_and_no_go_feature_conditions_both_exist"])
        self.assertEqual(certificate["counts"]["candidate_rules"], 27)
        self.assertEqual(certificate["counts"]["target_objectives"], 6)
        self.assertEqual(certificate["counts"]["positive_feature_conditions"], 3)
        self.assertEqual(certificate["counts"]["negative_no_go_feature_conditions"], 3)
        self.assertEqual(certificate["counts"]["distinct_feature_condition_rules"], 4)
        self.assertEqual(
            certificate["rule_language_schema"]["domains"]["entropy_bonus"],
            (0, 1, 2),
        )
        audits = {item["objective"]["name"]: item for item in certificate["target_feature_audits"]}
        self.assertEqual(
            audits["prefer_full_semantics_over_entropy_break"]["feature_condition"],
            {"entropy_bonus": 2, "observer_bonus": 0, "algebra_bonus": 0},
        )
        self.assertEqual(
            audits["prefer_full_semantics_over_entropy_break"]["predicate_rules"],
            ("edge_bonus_e2_o0_a0",),
        )
        self.assertEqual(audits["prefer_full_semantics_over_entropy_break"]["max_worst_case_gap"]["string"], "2/149")
        self.assertEqual(
            audits["prefer_full_semantics_over_entropy_break"]["worst_case_substrates_for_minimal_witnesses"],
            ("algebra_flat_edges",),
        )
        self.assertEqual(
            audits["prefer_entropy_break_over_operator_collapse"]["feature_condition"],
            {"entropy_bonus": 0, "observer_bonus": 2, "algebra_bonus": 2},
        )
        self.assertEqual(
            audits["prefer_entropy_break_over_operator_collapse"]["predicate_rules"],
            ("edge_bonus_e0_o2_a2",),
        )
        self.assertEqual(audits["prefer_entropy_break_over_operator_collapse"]["max_worst_case_gap"]["string"], "3/514")
        self.assertEqual(
            audits["prefer_operator_collapse_over_full_semantics"]["feature_condition"],
            {"entropy_bonus": 0, "observer_bonus": 0, "algebra_bonus": 2},
        )
        self.assertEqual(
            audits["prefer_operator_collapse_over_full_semantics"]["actual_sign"],
            "negative",
        )
        self.assertEqual(
            audits["prefer_operator_collapse_over_full_semantics"]["max_worst_case_gap"]["string"],
            "-13/173",
        )
        self.assertEqual(
            audits["prefer_operator_collapse_over_full_semantics"]["worst_case_substrates_for_minimal_witnesses"],
            ("observer_signal_stable_edges",),
        )
        self.assertIn("finite exact checks", certificate["interpretation"]["audit_lesson"])

    def test_cosmology_phase29_bounded_substrate_family_co_design_certificate(self):
        certificate = bridge_cosmology_phase29_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_29_bounded_substrate_family_co_design_certificate"])
        self.assertTrue(claims["family_search_space_exactly_bounded"])
        self.assertTrue(claims["all_family_robust_syntheses_certified"])
        self.assertTrue(claims["all_family_local_feature_audits_certified"])
        self.assertTrue(claims["co_design_finds_negative_to_positive_no_go_flip"])
        self.assertTrue(claims["co_design_preserves_some_no_go_signs_across_every_family"])
        self.assertEqual(certificate["counts"]["candidate_families"], 8)
        self.assertEqual(certificate["counts"]["candidate_rules"], 27)
        self.assertEqual(certificate["counts"]["negative_to_positive_no_go_flips"], 2)
        self.assertEqual(certificate["counts"]["preserved_negative_no_go_objectives"], 2)
        self.assertEqual(
            certificate["preserved_negative_no_go_objectives"],
            (
                "prefer_entropy_break_over_full_semantics",
                "prefer_operator_collapse_over_full_semantics",
            ),
        )
        flips = {
            (item["family"], item["objective"])
            for item in certificate["negative_to_positive_no_go_flips"]
        }
        self.assertEqual(
            flips,
            {
                ("full_only", "prefer_operator_collapse_over_entropy_break"),
                ("full_plus_entropy", "prefer_operator_collapse_over_entropy_break"),
            },
        )
        family_by_name = {
            item["family"]["name"]: item
            for item in certificate["family_results"]
        }
        self.assertEqual(family_by_name["full_only"]["counts"]["positive_worst_case_objectives"], 4)
        self.assertEqual(family_by_name["full_plus_all_filters"]["counts"]["positive_worst_case_objectives"], 3)
        self.assertEqual(family_by_name["full_plus_all_filters"]["counts"]["robust_pareto_frontier_rules"], 17)
        full_only_witnesses = {
            item["objective"]["name"]: item
            for item in family_by_name["full_only"]["robust_target_gap_witnesses"]
        }
        self.assertEqual(
            full_only_witnesses["prefer_operator_collapse_over_entropy_break"]["max_worst_case_gap"]["string"],
            "1/70",
        )
        baseline_witnesses = {
            item["objective"]["name"]: item
            for item in family_by_name["full_plus_all_filters"]["robust_target_gap_witnesses"]
        }
        self.assertEqual(
            baseline_witnesses["prefer_operator_collapse_over_entropy_break"]["max_worst_case_gap"]["string"],
            "-5/114",
        )
        local_audits = {
            item["objective"]["name"]: item
            for item in family_by_name["full_only"]["local_feature_audits"]
        }
        self.assertEqual(
            local_audits["prefer_operator_collapse_over_entropy_break"]["feature_condition_signatures"],
            ({"entropy_bonus": 2, "observer_bonus": 0, "algebra_bonus": 0},),
        )
        self.assertEqual(
            local_audits["prefer_operator_collapse_over_entropy_break"]["worst_case_substrates_for_minimal_witnesses"],
            ("full_mixed_graph",),
        )
        self.assertGreater(
            certificate["counts"]["phase28_schema_transfer_failed_nonbaseline_objectives"],
            0,
        )

    def test_cosmology_phase30_bounded_observer_cover_co_design_certificate(self):
        certificate = bridge_cosmology_phase30_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_30_bounded_observer_cover_co_design_certificate"])
        self.assertTrue(claims["strict_seed_cover_certificates_verified"])
        self.assertTrue(claims["near_miss_rejected_by_erasure_gate"])
        self.assertTrue(claims["all_cover_mixed_graphs_certified"])
        self.assertTrue(claims["all_cover_robust_audits_certified"])
        self.assertTrue(claims["strict_cover_flips_operator_full_no_go"])
        self.assertTrue(claims["strict_covers_preserve_entropy_full_no_go"])
        self.assertTrue(claims["near_miss_flips_entropy_full_no_go_but_fails_erasure_gate"])
        self.assertEqual(certificate["counts"]["selected_covers"], 4)
        self.assertEqual(certificate["counts"]["strict_cover_hits"], 3)
        self.assertEqual(certificate["counts"]["near_miss_covers"], 1)
        self.assertEqual(certificate["counts"]["strict_operator_full_no_go_flips"], 1)
        self.assertEqual(certificate["counts"]["near_miss_entropy_full_no_go_flips"], 1)
        self.assertEqual(certificate["key_gap_comparison"]["baseline_entropy_break_over_full"]["string"], "-7/153")
        self.assertEqual(certificate["key_gap_comparison"]["near_miss_entropy_break_over_full"]["string"], "7/365")
        self.assertEqual(certificate["key_gap_comparison"]["baseline_operator_collapse_over_full"]["string"], "-13/173")
        self.assertEqual(certificate["key_gap_comparison"]["strict_operator_flip_over_full"]["string"], "3/70")
        strict_flips = {
            (item["cover"], item["objective"], item["baseline_sign"], item["cover_sign"])
            for item in certificate["strict_operator_full_no_go_flips"]
        }
        self.assertEqual(
            strict_flips,
            {
                (
                    "strict_operator_flip_p3_q13",
                    "prefer_operator_collapse_over_full_semantics",
                    "negative",
                    "positive",
                ),
            },
        )
        near_miss_flips = {
            (item["cover"], item["objective"], item["baseline_sign"], item["cover_sign"])
            for item in certificate["near_miss_entropy_full_no_go_flips"]
        }
        self.assertEqual(
            near_miss_flips,
            {
                (
                    "near_miss_entropy_flip_p3_q5",
                    "prefer_entropy_break_over_full_semantics",
                    "negative",
                    "positive",
                ),
            },
        )
        cover_by_name = {
            item["cover_candidate"]["name"]: item
            for item in certificate["cover_results"]
        }
        self.assertEqual(cover_by_name["strict_control_p2_q7"]["counts"]["positive_worst_case_objectives"], 3)
        self.assertEqual(cover_by_name["strict_control_p2_q7"]["counts"]["negative_worst_case_objectives"], 3)
        operator_flip_signs = {
            item["objective"]: item["sign"]
            for item in cover_by_name["strict_operator_flip_p3_q13"]["objective_signs"]
        }
        self.assertEqual(operator_flip_signs["prefer_entropy_break_over_full_semantics"], "negative")
        self.assertEqual(operator_flip_signs["prefer_operator_collapse_over_full_semantics"], "positive")
        self.assertEqual(operator_flip_signs["prefer_full_semantics_over_entropy_break"], "negative")
        near_miss_claims = cover_by_name["near_miss_entropy_flip_p3_q5"]["cover_candidate"][
            "seed_cover_certificate"
        ]["certified_claims"]
        self.assertFalse(near_miss_claims["same_erasure_correctability_profile"])
        self.assertFalse(near_miss_claims["causal_patch_search_hit"])

    def test_cosmology_phase31_strict_cover_exhaustive_audit_certificate(self):
        certificate = bridge_cosmology_phase31_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["phase_31_strict_cover_exhaustive_audit_certificate"])
        self.assertTrue(claims["phase31_exhaustive_strict_cover_scan_certified"])
        self.assertTrue(claims["all_strict_seed_cover_certificates_verified"])
        self.assertTrue(claims["all_strict_cover_mixed_graphs_certified"])
        self.assertTrue(claims["all_strict_cover_robust_audits_certified"])
        self.assertTrue(claims["entropy_break_over_full_is_strict_cover_no_go"])
        self.assertTrue(claims["operator_related_sign_flips_classified_by_p_private"])
        self.assertEqual(certificate["counts"]["phase12_private_full_shared_inner_candidates"], 175)
        self.assertEqual(certificate["counts"]["raw_entropy_reconstruction_hits"], 66)
        self.assertEqual(certificate["counts"]["strict_cover_hits"], 8)
        self.assertEqual(certificate["counts"]["raw_hits_rejected_by_erasure_profile"], 58)
        self.assertEqual(certificate["counts"]["operator_related_sign_flip_records"], 16)
        self.assertEqual(certificate["counts"]["operator_related_sign_flip_covers"], 4)
        self.assertEqual(certificate["counts"]["operator_related_sign_preserving_covers"], 4)
        self.assertEqual(certificate["counts"]["operator_full_no_go_flips"], 4)
        self.assertEqual(certificate["counts"]["operator_entropy_no_go_flips"], 4)
        self.assertEqual(
            certificate["gap_extrema"]["entropy_break_over_full_semantics"]["maximum"]["string"],
            "-1/53",
        )
        self.assertEqual(
            certificate["gap_extrema"]["entropy_break_over_full_semantics"]["maximum_covers"],
            (
                "strict_hit_p10_q7",
                "strict_hit_p12_q11",
                "strict_hit_p3_q13",
                "strict_hit_p6_q13",
            ),
        )
        self.assertEqual(
            certificate["gap_extrema"]["operator_collapse_over_full_semantics"]["maximum"]["string"],
            "3/70",
        )
        self.assertEqual(
            certificate["gap_extrema"]["operator_collapse_over_entropy_break"]["maximum"]["string"],
            "19/284",
        )
        partition = certificate["operator_flip_cover_partition"]
        self.assertEqual(
            partition["operator_related_sign_flip_covers"],
            (
                "strict_hit_p10_q7",
                "strict_hit_p12_q11",
                "strict_hit_p3_q13",
                "strict_hit_p6_q13",
            ),
        )
        self.assertEqual(
            partition["operator_related_sign_preserving_covers"],
            (
                "strict_hit_p1_q13",
                "strict_hit_p2_q7",
                "strict_hit_p4_q13",
                "strict_hit_p8_q11",
            ),
        )
        self.assertTrue(
            all(
                item["cover_pattern"]["observer_p_private_nonempty"]
                for item in partition["flip_cover_patterns"]
            )
        )
        self.assertTrue(
            all(
                not item["cover_pattern"]["observer_p_private_nonempty"]
                for item in partition["preserving_cover_patterns"]
            )
        )
        scan_masks = {
            (item["observer_p_block_mask"], item["observer_q_block_mask"])
            for item in certificate["strict_cover_scan"]["strict_cover_block_masks"]
        }
        self.assertEqual(
            scan_masks,
            {
                (1, 13),
                (2, 7),
                (3, 13),
                (4, 13),
                (6, 13),
                (8, 11),
                (10, 7),
                (12, 11),
            },
        )

    def test_de_sitter_qec_toy_model_capstone_certificate(self):
        certificate = de_sitter_qec_toy_model_certificate(max_m=2)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["finite_de_sitter_like_qec_toy_model_certified"])
        self.assertTrue(claims["finite_observer_causal_patch_primitive_certified"])
        self.assertTrue(claims["horizon_entropy_overlap_certificate"])
        self.assertTrue(claims["observer_reconstruction_algebra_split"])
        self.assertTrue(claims["complementarity_no_cloning_guard"])
        self.assertTrue(claims["erasure_semantics_certified"])
        self.assertTrue(claims["controlled_patch_growth_certified"])
        self.assertTrue(claims["patch_channel_fixed_point_behavior_certified"])
        self.assertTrue(claims["bounded_strict_cover_audit_certified"])

        obligations = certificate["proof_obligations"]
        self.assertTrue(all(record["satisfied"] for record in obligations.values()))
        primitive = obligations["observer_causal_patch_primitive"]["evidence"]
        self.assertEqual(primitive["observer_overlap"], primitive["shared_horizon_qubits"])
        self.assertTrue(primitive["no_boundary_interval_role"])
        horizon = obligations["horizon_entropy_and_patch_overlap"]["evidence"]
        self.assertEqual(horizon["shared_horizon_entropy"], 2)
        self.assertEqual(horizon["shared_horizon_signature"], (1, 1, 1, False))
        channel = obligations["patch_channel_fixed_point_behavior"]["evidence"]
        self.assertEqual(channel["phase22_counts"]["nodes"], 49)
        self.assertEqual(channel["phase31_counts"]["strict_cover_hits"], 8)
        self.assertEqual(certificate["recommendation"]["next_phase"], "stop")

    def test_goal4_observer_algebra_tomography_certificate(self):
        certificate = observer_algebra_tomography_certificate(max_m=2)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["observer_entropy_non_identifiability_prefix_certified"])
        self.assertTrue(claims["center_profile_boundary_separates_prefix"])
        self.assertTrue(claims["k1_all_region_completion_lemma_declared"])
        self.assertTrue(claims["k1_all_region_completion_lemma_audited"])

        records = certificate["family_prefix"]["records"]
        self.assertEqual(len(records), 2)
        for record in records:
            self.assertTrue(record["certified_claims"]["entropy_horizon_shadow_agrees"])
            self.assertTrue(record["certified_claims"]["erasure_survivor_shadow_agrees"])
            self.assertTrue(record["certified_claims"]["observer_algebra_differs"])
            self.assertTrue(record["certified_claims"]["channel_semantics_differ"])
            self.assertEqual(record["first_separating_tier"], "plus_observer_center_profile")

        boundary = certificate["positive_boundary"]
        self.assertEqual(boundary["weakest_tier_separating_balanced_bridge_prefix"], "plus_observer_center_profile")
        scan = boundary["bounded_all_region_shadow_scan"]
        self.assertEqual(scan["first_no_collision_tier_observed"], "plus_erasure_fixed_points")
        self.assertEqual(scan["k1_erasure_fixed_point_completion_lemma"]["status"], "pass")
        self.assertIn("S_Ob", certificate["harlow_facing_interpretation"])

    def test_goal5_kgt1_observer_algebra_tomography_certificate(self):
        certificate = goal5_kgt1_observer_tomography_certificate(max_n=4)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["k_gt_1_channel_shadow_counterexample_certified"])
        self.assertTrue(claims["permutation_quotient_first_channel_collision_at_n3"])
        self.assertTrue(claims["channel_plus_center_counterexample_certified"])
        self.assertTrue(claims["center_commutant_completion_proposition_declared"])
        self.assertTrue(claims["bounded_scan_center_commutant_no_collision"])
        self.assertTrue(claims["full_bounded_scan_first_no_collision_at_center_commutant"])
        self.assertTrue(claims["spectator_lift_certified"])
        self.assertTrue(claims["distance_amplified_witness_certified"])

        minimal = certificate["minimal_channel_counterexample"]
        self.assertEqual(minimal["first_generators"], ("XXI",))
        self.assertEqual(minimal["second_generators"], ("XXX",))
        self.assertTrue(minimal["channel_shadow_matches"])
        self.assertFalse(minimal["algebra_profile_matches"])
        self.assertEqual(
            minimal["algebra_difference_witness"],
            {"region": (0, 1), "first_signature": (2, 0, 2, False), "second_signature": (3, 1, 1, False)},
        )

        center = certificate["center_shadow_counterexample"]
        self.assertTrue(center["channel_shadow_matches"])
        self.assertTrue(center["center_shadow_matches"])
        self.assertFalse(center["commutant_shadow_matches"])

        amplified = certificate["distance_amplified_witness"]
        self.assertEqual(amplified["parameters"]["first"], {"n": 15, "k": 2})
        self.assertEqual(amplified["distance_audit"]["first"]["distance_exact_if_pass"], 3)
        self.assertEqual(amplified["distance_audit"]["second"]["distance_exact_if_pass"], 3)
        self.assertEqual(amplified["representative_signatures"]["first"], (2, 0, 2, False))
        self.assertEqual(amplified["representative_signatures"]["second"], (3, 1, 1, False))

    def test_goal6_operational_observer_algebra_tomography_certificate(self):
        certificate = goal6_operational_observer_tomography_certificate(max_n=4)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["channel_shadow_insufficient_for_k_gt_1"])
        self.assertTrue(claims["center_shadow_insufficient"])
        self.assertTrue(claims["channel_plus_center_shadow_insufficient"])
        self.assertTrue(claims["center_plus_entropy_response_sufficient_in_bounded_scan"])
        self.assertTrue(claims["entropy_response_commutator_sufficient_in_bounded_scan"])
        self.assertTrue(claims["relative_entropy_profile_equivalent_to_entropy_response"])
        self.assertTrue(claims["recovery_success_spectrum_equivalent_to_entropy_response"])
        self.assertTrue(claims["commutator_test_shadow_sufficient_in_bounded_scan"])
        self.assertTrue(claims["operational_completion_theorem_bounded_audit"])
        self.assertTrue(claims["distance_amplified_channel_witness"])
        self.assertTrue(claims["distance_amplified_channel_plus_center_witness"])

        theorem = certificate["operational_completion_theorem"]
        self.assertIn("without directly supplying dim L_R^perp", theorem["claim"])
        audit = certificate["bounded_operational_theorem_audit"]
        self.assertEqual(audit["status"], "pass")
        self.assertEqual(audit["records"][-1]["n"], 4)

        amplified = certificate["distance_amplified_witnesses"]
        self.assertEqual(amplified["channel"]["parameters"]["first"], {"n": 15, "k": 2})
        self.assertEqual(amplified["channel_plus_center"]["parameters"]["first"], {"n": 20, "k": 2})
        self.assertEqual(amplified["channel_plus_center"]["distance_audit"]["first"]["distance_exact_if_pass"], 3)
        self.assertEqual(amplified["channel"]["representative_signatures"]["second"], (3, 1, 1, False))

    def test_goal7_observer_algebra_tomography_atlas_certificate(self):
        certificate = goal7_observer_tomography_atlas_certificate(max_n=4)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["minimal_channel_collision_at_n3"])
        self.assertTrue(claims["channel_plus_center_collision_at_n4"])
        self.assertTrue(claims["entropy_response_dimension_collision_at_n4"])
        self.assertTrue(claims["completion_tiers_have_no_bounded_collisions"])
        self.assertTrue(claims["distance_amplification_records_present"])
        self.assertTrue(claims["theorem_candidates_generated"])

        rows = {row["shadow"]: row for row in certificate["atlas_table"]}
        self.assertEqual(rows["channel"]["determines_tau"], "no")
        self.assertEqual(rows["channel"]["minimal_counterexample"]["n"], 3)
        self.assertEqual(rows["channel_plus_center"]["minimal_counterexample"]["n"], 4)
        self.assertEqual(rows["entropy_response_dimension"]["minimal_counterexample"]["n"], 4)
        self.assertEqual(rows["center_plus_entropy_response"]["determines_tau"], "yes")
        self.assertEqual(rows["commutator_test"]["proof_status"], "theorem")
        self.assertEqual(rows["channel"]["amplification"]["status"], "pass")
        self.assertEqual(certificate["intrinsic_probe_frontier"]["status"], "open")

    def test_goal8_intrinsic_observer_algebra_tomography_certificate(self):
        certificate = goal8_intrinsic_observer_tomography_certificate(max_n=4)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["labeled_logical_pauli_probes_removed"])
        self.assertTrue(claims["channel_collision_at_n3"])
        self.assertTrue(claims["dimension_only_intrinsic_probe_collision_at_n4"])
        self.assertTrue(claims["local_commutator_center_collision_at_n4"])
        self.assertTrue(claims["intrinsic_completion_tiers_have_no_bounded_collisions"])
        self.assertTrue(claims["intrinsic_theorem_audit_pass"])
        self.assertTrue(claims["distance_amplification_records_present"])

        rows = {row["shadow"]: row for row in certificate["intrinsic_atlas_table"]}
        self.assertEqual(rows["erasure_survivor_channel"]["determines_tau"], "no")
        self.assertEqual(rows["erasure_survivor_channel"]["minimal_counterexample"]["n"], 3)
        self.assertEqual(rows["physical_pauli_response_spectrum"]["minimal_counterexample"]["n"], 4)
        self.assertEqual(rows["local_commutator_center"]["minimal_counterexample"]["n"], 4)
        self.assertEqual(rows["physical_response_plus_center"]["determines_tau"], "yes")
        self.assertEqual(rows["physical_response_plus_center"]["completion_type"], "intrinsic_operational")
        self.assertEqual(rows["physical_response_commutator_tomography"]["proof_status"], "theorem")
        self.assertEqual(rows["erasure_survivor_channel"]["amplification"]["status"], "pass")
        self.assertIn("without labeled logical Pauli probes", certificate["intrinsic_completion_theorem"]["claim"])

    def test_goal9_finite_oaqec_intrinsic_observer_tomography_certificate(self):
        certificate = goal9_finite_oaqec_intrinsic_tomography_certificate(max_block_dim=4, max_blocks=5)
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["formal_wedderburn_signature_declared"])
        self.assertTrue(claims["weak_dimension_center_commutator_shadow_collision_found"])
        self.assertTrue(claims["bounded_collision_is_minimal_in_declared_order"])
        self.assertTrue(claims["full_product_star_tomography_recovers_examples"])
        self.assertTrue(claims["finite_oaqec_tomography_theorem_declared"])
        self.assertTrue(claims["goal8_stabilizer_special_case_bridge_declared"])

        collision = certificate["negative_hierarchy"]["bounded_first_collision"]
        self.assertEqual(collision["shadow"], (20, 5, 15))
        self.assertEqual(collision["first_block_sizes"], (1, 1, 1, 1, 4))
        self.assertEqual(collision["second_block_sizes"], (2, 2, 2, 2, 2))
        self.assertNotEqual(
            collision["first_signature"]["abstract_block_sizes"],
            collision["second_signature"]["abstract_block_sizes"],
        )

        theorem = certificate["positive_theorem"]
        self.assertIn("product/* table", theorem["claim"])
        self.assertTrue(all(record["status"] == "pass" for record in theorem["theorem_audit_examples"]))
        self.assertIn("stabilizer special case", certificate["harlow_facing_interpretation"])

    def test_holography_phase1_stabilizer_tensor_network_seed_certificate(self):
        certificate = bridge_holography_phase1_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_1_tensor_network_seed_certificate"])
        self.assertTrue(claims["shared_min_cut_profile_certified"])
        self.assertTrue(claims["named_boundary_entropy_profile_matches"])
        self.assertTrue(claims["ring_interval_entropy_profile_matches"])
        self.assertTrue(claims["observer_reconstruction_differs"])
        self.assertTrue(claims["low_order_erasure_visible_difference_exists"])
        self.assertEqual(certificate["counts"]["boundary_qubits"], 8)
        self.assertEqual(certificate["counts"]["internal_nodes"], 1)
        self.assertEqual(certificate["counts"]["named_regions"], 5)
        self.assertEqual(certificate["counts"]["ring_low_order_intervals"], 16)
        self.assertEqual(certificate["counts"]["named_entropy_mismatches"], 0)
        self.assertEqual(certificate["counts"]["ring_entropy_mismatches"], 0)
        self.assertEqual(certificate["counts"]["low_order_erasure_difference_witnesses"], 1)

        named = {
            item["region"]["name"]: item
            for item in certificate["named_region_diagnostics"]
        }
        observer_p = named["observer_p"]
        self.assertEqual(observer_p["region"]["qubits"], (1, 2, 3, 6))
        self.assertEqual(observer_p["first"]["entropy"], 3)
        self.assertEqual(observer_p["second"]["entropy"], 3)
        self.assertEqual(observer_p["min_cut"]["value"], 6)
        self.assertEqual(observer_p["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(observer_p["second"]["algebra_signature"], (2, 0, 0, True))
        shared_horizon = named["shared_horizon"]
        self.assertEqual(shared_horizon["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(shared_horizon["second"]["algebra_signature"], (1, 1, 1, False))

        witness = certificate["low_order_erasure_difference_witnesses"][0]
        self.assertEqual(witness["region"]["qubits"], (5, 0))
        self.assertEqual(witness["first"]["entropy"], 1)
        self.assertEqual(witness["second"]["entropy"], 1)
        self.assertEqual(witness["min_cut"]["value"], 4)
        self.assertEqual(witness["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(witness["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(witness["first"]["erasure_correctable"])
        self.assertTrue(witness["second"]["erasure_correctable"])
        self.assertFalse(witness["first"]["survivor_fixed_point_reconstructs_all"])
        self.assertTrue(witness["second"]["survivor_fixed_point_reconstructs_all"])

    def test_holography_phase2_bounded_graph_cws_ring_atlas_certificate(self):
        certificate = bridge_holography_phase2_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_2_bounded_graph_cws_ring_atlas_certificate"])
        self.assertTrue(claims["strict_source_menu_no_pair"])
        self.assertTrue(claims["strict_source_scans_exhausted_under_bounds"])
        self.assertTrue(claims["relaxed_graph_pair_found"])
        self.assertTrue(claims["relaxed_graph_pair_same_labeled_t2_entropy"])
        self.assertTrue(claims["relaxed_graph_pair_reconstruction_profiles_differ"])
        self.assertTrue(claims["distance_one_caveat_certified"])
        self.assertTrue(claims["ring_orders_exhaustively_checked_mod_dihedral"])
        self.assertTrue(claims["reconstruction_visible_ring_interval_witness_exists"])
        self.assertEqual(certificate["counts"]["strict_source_scans"], 4)
        self.assertEqual(certificate["counts"]["strict_source_no_pair_scans"], 4)
        self.assertEqual(certificate["counts"]["strict_source_exhausted_scans"], 4)
        self.assertEqual(certificate["counts"]["relaxed_graph_raw_codes"], 24)
        self.assertEqual(certificate["counts"]["relaxed_graph_codes_checked"], 24)
        self.assertEqual(certificate["counts"]["ring_orders_checked"], 12)
        self.assertEqual(certificate["counts"]["expected_ring_orders_mod_dihedral"], 12)
        self.assertEqual(certificate["counts"]["ring_orders_with_hits"], 10)
        self.assertEqual(certificate["counts"]["selected_hit_interval_witnesses"], 1)

        scans = {scan["source"]: scan for scan in certificate["strict_source_menu"]["scan_reports"]}
        self.assertEqual(scans["css"]["raw_codes"], 93)
        self.assertEqual(scans["css"]["codes_checked"], 9)
        self.assertEqual(scans["cyclic-css"]["raw_codes"], 2)
        self.assertEqual(scans["graph"]["raw_codes"], 33)
        self.assertEqual(scans["encoder"]["raw_codes"], 10)
        self.assertTrue(all(scan["status"] == "no-pair" for scan in scans.values()))

        pair = certificate["relaxed_graph_code_pair"]
        self.assertEqual(pair["n"], 5)
        self.assertEqual(pair["k"], 1)
        self.assertEqual(pair["first_distance"], 1)
        self.assertEqual(pair["second_distance"], 1)
        self.assertEqual(pair["first_generators"], ("XIXZI", "IXZXI", "IZXII", "ZIIXI"))
        self.assertEqual(pair["second_generators"], ("XIXZZ", "IXZXI", "IZXII", "ZIIXI"))

        selected = certificate["ring_atlas_search"]["selected_hit"]
        self.assertEqual(selected["boundary_order"], (0, 1, 2, 4, 3))
        self.assertEqual(selected["summary"]["entropy_mismatches"], 0)
        self.assertEqual(selected["summary"]["min_cut_mismatches"], 0)
        self.assertEqual(selected["summary"]["length_at_least_2_reconstruction_witnesses"], 1)
        self.assertEqual(selected["summary"]["length_at_least_2_erasure_witnesses"], 0)
        witness = selected["interval_reconstruction_witnesses"][0]
        self.assertEqual(witness["region"]["qubits"], (2, 4))
        self.assertEqual(witness["region"]["length"], 2)
        self.assertEqual(witness["min_cut"]["value"], 4)
        self.assertEqual(witness["first"]["entropy"], 2)
        self.assertEqual(witness["second"]["entropy"], 2)
        self.assertEqual(witness["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(witness["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertFalse(witness["first"]["erasure_correctable"])
        self.assertFalse(witness["second"]["erasure_correctable"])

    def test_holography_phase3_distance_repaired_lifted_ring_atlas_certificate(self):
        certificate = bridge_holography_phase3_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_3_distance_repaired_lifted_ring_atlas_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["outer_code_distance_2"])
        self.assertTrue(claims["logical_concatenation_k1"])
        self.assertTrue(claims["distance_at_least_2_after_repair_certified"])
        self.assertTrue(claims["all_labeled_t2_entropy_matches_after_repair"])
        self.assertTrue(claims["all_template_low_order_entropy_and_min_cut_profiles_match"])
        self.assertTrue(claims["single_block_lift_collapses_original_witness"])
        self.assertTrue(claims["two_block_lifted_reconstruction_and_erasure_witnesses_exist"])
        self.assertTrue(claims["large_lifts_rejected_by_entropy_gate"])
        self.assertTrue(claims["selected_witness_is_boundary_ring_interval"])
        self.assertTrue(claims["selected_witness_survivor_fixed_point_differs"])

        self.assertEqual(certificate["counts"]["low_order_subsets_checked"], 211)
        self.assertEqual(certificate["counts"]["low_order_entropy_mismatches"], 0)
        self.assertEqual(certificate["counts"]["ring_templates"], 3)
        self.assertEqual(certificate["counts"]["ring_template_intervals_checked"], 120)
        self.assertEqual(certificate["counts"]["lifted_block_masks_checked"], 15)
        self.assertEqual(certificate["counts"]["single_block_collapses"], 4)
        self.assertEqual(certificate["counts"]["accepted_two_block_hits"], 6)
        self.assertEqual(certificate["counts"]["entropy_gate_rejections"], 5)

        distance = certificate["distance_repair"]
        self.assertTrue(distance["distance_at_least_2_for_both"])
        self.assertEqual(distance["first"]["max_weight_checked"], 1)
        self.assertIsNone(distance["first"]["logical_witness"])
        self.assertEqual(distance["second"]["max_weight_checked"], 1)
        self.assertIsNone(distance["second"]["logical_witness"])

        templates = {
            template["name"]: template
            for template in certificate["ring_template_search"]["templates"]
        }
        self.assertEqual(
            templates["source_aware_witness_strip_ring"]["boundary_order"][:8],
            (2, 4, 7, 9, 12, 14, 17, 19),
        )
        self.assertTrue(
            all(
                template["summary"]["entropy_mismatches"] == 0
                and template["summary"]["min_cut_mismatches"] == 0
                for template in templates.values()
            )
        )

        audit = certificate["lifted_phase2_witness_audit"]
        self.assertEqual(
            tuple(record["region"]["block_mask"] for record in audit["accepted_two_block_hits"]),
            (3, 5, 6, 9, 10, 12),
        )
        self.assertEqual(
            tuple(record["region"]["block_mask"] for record in audit["entropy_gate_rejections"]),
            (7, 11, 13, 14, 15),
        )
        selected = audit["selected_witness"]
        self.assertEqual(selected["region"]["block_mask"], 3)
        self.assertEqual(selected["region"]["qubits"], (2, 4, 7, 9))
        self.assertEqual(selected["interval_location"]["is_boundary_ring_interval"], True)
        self.assertEqual(selected["interval_location"]["start"], 0)
        self.assertEqual(selected["interval_location"]["length"], 4)
        self.assertEqual(selected["min_cut"]["value"], 6)
        self.assertEqual(selected["first"]["entropy"], 4)
        self.assertEqual(selected["second"]["entropy"], 4)
        self.assertEqual(selected["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected["first"]["erasure_correctable"])
        self.assertTrue(selected["second"]["erasure_correctable"])
        self.assertFalse(selected["first"]["survivor_fixed_point_reconstructs_all"])
        self.assertTrue(selected["second"]["survivor_fixed_point_reconstructs_all"])

    def test_holography_phase4_multi_bulk_layout_audit_certificate(self):
        certificate = bridge_holography_phase4_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_4_multi_bulk_layout_audit_certificate"])
        self.assertTrue(claims["phase3_repaired_source_loaded"])
        self.assertTrue(claims["selected_phase3_witness_operator_channel_split_certified"])
        self.assertTrue(claims["multi_bulk_layout_space_scored"])
        self.assertTrue(claims["all_layout_interval_entropy_profiles_match"])
        self.assertTrue(claims["all_layout_min_cuts_exactly_enumerated"])
        self.assertTrue(claims["source_aware_layouts_recover_strict_witness"])
        self.assertTrue(claims["less_source_aware_layouts_do_not_recover_strict_witness"])
        self.assertTrue(claims["less_source_aware_layouts_are_operator_channel_near_misses"])
        self.assertTrue(claims["less_source_aware_interval_cover_overhead_certified"])

        self.assertEqual(certificate["counts"]["boundary_templates"], 4)
        self.assertEqual(certificate["counts"]["network_skeletons_per_boundary_order"], 4)
        self.assertEqual(certificate["counts"]["layout_candidates"], 16)
        self.assertEqual(certificate["counts"]["source_aware_strict_hits"], 4)
        self.assertEqual(certificate["counts"]["less_source_aware_strict_hits"], 0)
        self.assertEqual(certificate["counts"]["less_source_aware_near_misses"], 12)
        self.assertEqual(certificate["counts"]["min_less_source_aware_interval_cover_length"], 6)
        self.assertEqual(certificate["counts"]["max_less_source_aware_interval_cover_length"], 8)
        self.assertEqual(certificate["counts"]["max_min_cut_internal_assignments"], 32)

        witness = certificate["selected_witness"]
        self.assertEqual(witness["region"]["qubits"], (2, 4, 7, 9))
        self.assertEqual(witness["first"]["entropy"], 4)
        self.assertEqual(witness["second"]["entropy"], 4)
        self.assertEqual(witness["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(witness["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(witness["first"]["erasure_correctable"])
        self.assertTrue(witness["second"]["erasure_correctable"])
        self.assertFalse(witness["first"]["survivor_fixed_point_reconstructs_all"])
        self.assertTrue(witness["second"]["survivor_fixed_point_reconstructs_all"])

        layout_by_key = {
            (item["boundary_template"]["name"], item["network"]["name"]): item
            for item in certificate["layout_records"]
        }
        expected_cover_lengths = {
            "natural_block_order": 8,
            "block_contiguous_phase2_ring": 7,
            "inner_position_interleaved_ring": 6,
            "source_aware_witness_strip_ring": 4,
        }
        expected_assignments = {
            "single_bulk_ring_spoke": 2,
            "outer_block_bulk_path": 16,
            "inner_position_bulk_cycle": 32,
            "binary_outer_tree": 8,
        }
        for boundary_name, cover_length in expected_cover_lengths.items():
            for network_name, assignments in expected_assignments.items():
                record = layout_by_key[(boundary_name, network_name)]
                selected_layout = record["selected_witness_layout"]
                self.assertEqual(
                    selected_layout["minimal_interval_cover"]["minimal_cover_length"],
                    cover_length,
                )
                self.assertEqual(selected_layout["min_cut"]["assignments_checked"], assignments)
                self.assertTrue(selected_layout["operator_channel_split"])
                self.assertEqual(
                    selected_layout["strict_layout_hit"],
                    boundary_name == "source_aware_witness_strip_ring",
                )
                self.assertEqual(
                    selected_layout["non_source_aware_near_miss"],
                    boundary_name != "source_aware_witness_strip_ring",
                )

        self.assertEqual(
            tuple((item["boundary_template"]["name"], item["network"]["name"]) for item in certificate["strict_layout_hits"]),
            (
                ("source_aware_witness_strip_ring", "single_bulk_ring_spoke"),
                ("source_aware_witness_strip_ring", "outer_block_bulk_path"),
                ("source_aware_witness_strip_ring", "inner_position_bulk_cycle"),
                ("source_aware_witness_strip_ring", "binary_outer_tree"),
            ),
        )

    def test_holography_phase5_generated_layout_search_certificate(self):
        certificate = bridge_holography_phase5_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_5_generated_layout_search_certificate"])
        self.assertTrue(claims["phase3_repaired_source_loaded"])
        self.assertTrue(claims["selected_phase3_witness_operator_channel_split_certified"])
        self.assertTrue(claims["all_labeled_t2_entropy_matches_after_repair"])
        self.assertTrue(claims["generated_layout_space_scored"])
        self.assertTrue(claims["all_generated_selected_mincuts_exact"])
        self.assertTrue(claims["generated_layouts_have_no_strict_compact_hit"])
        self.assertTrue(claims["source_agnostic_best_cover_length_is_8"])
        self.assertTrue(claims["phase2_seeded_best_cover_length_is_6"])
        self.assertTrue(claims["phase2_seeded_improves_but_does_not_recover_strict_locality"])

        self.assertEqual(certificate["counts"]["raw_generated_layouts"], 169)
        self.assertEqual(certificate["counts"]["unique_generated_layouts"], 168)
        self.assertEqual(certificate["counts"]["source_agnostic_layouts"], 166)
        self.assertEqual(certificate["counts"]["phase2_seeded_layouts"], 2)
        self.assertEqual(certificate["counts"]["strict_compact_hits"], 0)
        self.assertEqual(certificate["counts"]["source_agnostic_best_cover_length"], 8)
        self.assertEqual(certificate["counts"]["source_agnostic_best_layouts"], 80)
        self.assertEqual(certificate["counts"]["phase2_seeded_best_cover_length"], 6)
        self.assertEqual(certificate["counts"]["phase2_seeded_best_layouts"], 1)
        self.assertEqual(certificate["counts"]["selected_mincut_records"], 672)
        self.assertEqual(certificate["counts"]["max_selected_mincut_internal_assignments"], 32)

        self.assertEqual(
            tuple(
                (item["cover_length"], item["layout_count"])
                for item in certificate["layout_search"]["cover_distribution"]
            ),
            (
                (6, 1),
                (7, 1),
                (8, 80),
                (10, 2),
                (11, 1),
                (12, 80),
                (13, 1),
                (14, 1),
                (15, 1),
            ),
        )
        source_best = certificate["layout_search"]["best_source_agnostic_layouts"][0]
        self.assertEqual(source_best["minimal_interval_cover"]["minimal_cover_length"], 8)
        self.assertEqual(source_best["minimal_interval_cover"]["cover_qubits"], (2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(source_best["generator_kind"], "source_agnostic")
        phase2_best = certificate["layout_search"]["best_phase2_seeded_layouts"][0]
        self.assertEqual(phase2_best["name"], "inner_major_phase2_inner_ring")
        self.assertEqual(phase2_best["minimal_interval_cover"]["minimal_cover_length"], 6)
        self.assertEqual(phase2_best["minimal_interval_cover"]["cover_qubits"], (2, 7, 12, 17, 4, 9))
        self.assertFalse(certificate["layout_search"]["strict_compact_hits"])

        witness = certificate["selected_witness"]
        self.assertEqual(witness["region"]["qubits"], (2, 4, 7, 9))
        self.assertTrue(witness["comparisons"]["entropy_matches"])
        self.assertTrue(witness["comparisons"]["reconstruction_visible_differs"])
        self.assertTrue(witness["comparisons"]["channel_visible_differs"])

    def test_holography_phase6_generated_clifford_tensor_network_certificate(self):
        certificate = bridge_holography_phase6_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_6_generated_clifford_tensor_network_certificate"])
        self.assertTrue(claims["phase3_repaired_source_loaded"])
        self.assertTrue(claims["generated_clifford_tensor_networks_scored"])
        self.assertTrue(claims["all_circuit_selected_mincuts_exact"])
        self.assertTrue(claims["all_circuits_keep_selected_entropy_visible_match"])
        self.assertTrue(claims["local_clifford_layers_preserve_operator_channel_split"])
        self.assertTrue(claims["source_agnostic_entangling_layers_can_preserve_or_collapse"])
        self.assertTrue(claims["nearest_neighbor_cx_collapses_selected_witness"])
        self.assertTrue(claims["butterfly_cx_preserves_selected_witness"])

        self.assertEqual(certificate["counts"]["circuits_scored"], 6)
        self.assertEqual(certificate["counts"]["source_agnostic_local_clifford_circuits"], 2)
        self.assertEqual(certificate["counts"]["source_agnostic_entangling_circuits"], 2)
        self.assertEqual(certificate["counts"]["source_aware_control_circuits"], 1)
        self.assertEqual(certificate["counts"]["operator_channel_preserving_circuits"], 5)
        self.assertEqual(certificate["counts"]["operator_channel_collapsing_circuits"], 1)
        self.assertEqual(certificate["counts"]["max_circuit_internal_assignments"], 1024)

        records = {record["name"]: record for record in certificate["circuit_records"]}
        for name in ("identity_reference", "local_h_layer", "local_s_layer"):
            record = records[name]
            self.assertTrue(record["certified_behavior"]["operator_channel_split"])
            self.assertEqual(record["selected_witness_min_cut"]["assignments_checked"], 1)
            self.assertEqual(record["selected_witness_min_cut"]["value"], 8)
            self.assertEqual(record["selected_witness"]["first"]["algebra_signature"], (1, 1, 1, False))
            self.assertEqual(record["selected_witness"]["second"]["algebra_signature"], (0, 0, 2, False))

        nearest = records["nearest_neighbor_even_cx_layer"]
        self.assertEqual(nearest["gate_counts"]["two_qubit"], 10)
        self.assertTrue(nearest["certified_behavior"]["operator_channel_collapsed"])
        self.assertFalse(nearest["certified_behavior"]["operator_channel_split"])
        self.assertEqual(nearest["selected_witness"]["first"]["algebra_signature"], (0, 0, 2, False))
        self.assertEqual(nearest["selected_witness"]["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertTrue(nearest["selected_witness"]["first"]["erasure_correctable"])
        self.assertTrue(nearest["selected_witness"]["second"]["erasure_correctable"])
        self.assertEqual(nearest["selected_witness_min_cut"]["assignments_checked"], 1024)
        self.assertEqual(nearest["selected_witness_min_cut"]["value"], 12)

        butterfly = records["butterfly_halves_cx_layer"]
        self.assertEqual(butterfly["gate_counts"]["two_qubit"], 10)
        self.assertTrue(butterfly["certified_behavior"]["operator_channel_split"])
        self.assertEqual(butterfly["selected_witness"]["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(butterfly["selected_witness"]["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(butterfly["selected_witness"]["first"]["erasure_correctable"])
        self.assertTrue(butterfly["selected_witness"]["second"]["erasure_correctable"])
        self.assertEqual(butterfly["selected_witness_min_cut"]["assignments_checked"], 1024)
        self.assertEqual(butterfly["selected_witness_min_cut"]["value"], 12)

        control = records["phase2_witness_pair_cx_control"]
        self.assertEqual(control["generator_kind"], "source_aware_control")
        self.assertEqual(control["gate_counts"]["two_qubit"], 4)
        self.assertTrue(control["certified_behavior"]["operator_channel_split"])
        self.assertEqual(control["selected_witness_min_cut"]["assignments_checked"], 16)
        self.assertEqual(control["selected_witness_min_cut"]["value"], 8)

    def test_holography_phase7_joint_clifford_patch_search_certificate(self):
        certificate = bridge_holography_phase7_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_7_joint_clifford_patch_search_certificate"])
        self.assertTrue(claims["phase3_repaired_source_loaded"])
        self.assertTrue(claims["compact_interval_joint_search_scored"])
        self.assertTrue(claims["all_candidate_mincuts_exact"])
        self.assertTrue(claims["distance_audits_are_exact_weight_one_checks"])
        self.assertTrue(claims["entropy_visible_match_on_all_hits"])
        self.assertTrue(claims["operator_or_channel_split_on_all_hits"])
        self.assertTrue(claims["distance_preserving_compact_witnesses_exist"])
        self.assertTrue(claims["distance_preserving_hits_have_min_length_six"])
        self.assertTrue(claims["nearest_neighbor_fixed_patch_collapses_but_replacement_interval_exists"])
        self.assertTrue(claims["source_agnostic_entangling_distance_preserving_hit_exists"])
        self.assertTrue(claims["frontier_one_qubit_hits_separated_by_distance_gate"])
        self.assertTrue(claims["frontier_hits_have_min_length_one"])

        self.assertEqual(certificate["counts"]["circuits_scored"], 6)
        self.assertEqual(certificate["counts"]["candidate_intervals_scanned"], 720)
        self.assertEqual(certificate["counts"]["entropy_gate_passes"], 655)
        self.assertEqual(certificate["counts"]["entropy_gate_rejections"], 65)
        self.assertEqual(certificate["counts"]["operator_or_channel_hits"], 23)
        self.assertEqual(certificate["counts"]["distance_preserving_circuits"], 4)
        self.assertEqual(certificate["counts"]["low_distance_frontier_circuits"], 2)
        self.assertEqual(certificate["counts"]["distance_preserving_hits"], 11)
        self.assertEqual(certificate["counts"]["source_agnostic_entangling_distance_preserving_hits"], 2)
        self.assertEqual(certificate["counts"]["low_distance_frontier_hits"], 12)
        self.assertEqual(certificate["counts"]["one_qubit_frontier_hits"], 2)
        self.assertEqual(certificate["counts"]["min_distance_preserving_hit_length"], 6)
        self.assertEqual(certificate["counts"]["min_low_distance_frontier_hit_length"], 1)
        self.assertEqual(certificate["counts"]["max_candidate_min_cut_internal_assignments"], 1024)

        records = {record["name"]: record for record in certificate["circuit_records"]}
        nearest = records["nearest_neighbor_even_cx_layer"]
        self.assertTrue(nearest["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"])
        self.assertFalse(nearest["fixed_phase3_patch"]["operator_or_channel_split"])
        self.assertEqual(nearest["interval_search"]["hit_count"], 2)
        self.assertEqual(nearest["interval_search"]["shortest_hit_length"], 6)

        selected = certificate["selected_distance_preserving_replacement_hit"]
        self.assertEqual(selected["circuit"]["name"], "nearest_neighbor_even_cx_layer")
        self.assertEqual(selected["region"]["qubits"], (9, 10, 11, 12, 13, 14))
        self.assertEqual(selected["min_cut"]["value"], 4)
        self.assertEqual(selected["min_cut"]["assignments_checked"], 1024)
        self.assertEqual(selected["first"]["entropy"], 2)
        self.assertEqual(selected["second"]["entropy"], 2)
        self.assertEqual(selected["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected["first"]["erasure_correctable"])
        self.assertTrue(selected["second"]["erasure_correctable"])
        self.assertFalse(selected["first"]["survivor_fixed_point_reconstructs_all"])
        self.assertTrue(selected["second"]["survivor_fixed_point_reconstructs_all"])

        butterfly = records["butterfly_halves_cx_layer"]
        self.assertFalse(butterfly["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"])
        self.assertEqual(butterfly["distance_audit"]["first"]["logical_witness"]["qubits"], (4,))
        self.assertEqual(butterfly["interval_search"]["hit_count"], 6)
        self.assertEqual(butterfly["interval_search"]["shortest_hit_length"], 1)

        frontier = certificate["selected_frontier_tiny_hit"]
        self.assertEqual(frontier["circuit"]["name"], "butterfly_halves_cx_layer")
        self.assertEqual(frontier["region"]["qubits"], (4,))
        self.assertEqual(frontier["min_cut"]["value"], 3)
        self.assertEqual(frontier["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(frontier["second"]["algebra_signature"], (0, 0, 2, False))

    def test_holography_phase8_distance_gated_clifford_synthesis_certificate(self):
        certificate = bridge_holography_phase8_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_8_distance_gated_clifford_synthesis_certificate"])
        self.assertTrue(claims["phase3_repaired_source_loaded"])
        self.assertTrue(claims["synthesis_menu_scored"])
        self.assertTrue(claims["all_candidate_mincuts_exact"])
        self.assertTrue(claims["distance_gate_exact_weight_one_for_all_layers"])
        self.assertTrue(claims["distance_gate_accepts_and_rejects_layers"])
        self.assertTrue(claims["all_reported_hits_are_entropy_matched_operator_or_channel_splits"])
        self.assertTrue(claims["distance_preserving_hits_exist"])
        self.assertTrue(claims["distance_preserving_min_length_four"])
        self.assertTrue(claims["no_distance_preserving_hits_below_length_four"])
        self.assertTrue(claims["hierarchical_gray_layers_improve_over_affine_length_six"])
        self.assertTrue(claims["frontier_one_qubit_hits_rejected_by_distance_gate"])
        self.assertTrue(claims["fixed_patch_split_does_not_imply_compact_hit"])

        self.assertEqual(certificate["counts"]["synthesized_circuits"], 38)
        self.assertEqual(certificate["counts"]["unique_cx_layers"], 38)
        self.assertEqual(certificate["counts"]["candidate_intervals_scanned"], 4560)
        self.assertEqual(certificate["counts"]["entropy_gate_passes"], 4274)
        self.assertEqual(certificate["counts"]["entropy_gate_rejections"], 286)
        self.assertEqual(certificate["counts"]["operator_or_channel_hits"], 130)
        self.assertEqual(certificate["counts"]["distance_preserving_circuits"], 35)
        self.assertEqual(certificate["counts"]["distance_gate_rejections"], 3)
        self.assertEqual(certificate["counts"]["distance_preserving_hits"], 95)
        self.assertEqual(certificate["counts"]["low_distance_frontier_hits"], 35)
        self.assertEqual(certificate["counts"]["min_distance_preserving_hit_length"], 4)
        self.assertEqual(certificate["counts"]["min_low_distance_frontier_hit_length"], 1)
        self.assertEqual(certificate["counts"]["hierarchical_distance_preserving_hits"], 25)
        self.assertEqual(certificate["counts"]["affine_distance_preserving_hits"], 70)
        self.assertEqual(certificate["counts"]["max_candidate_min_cut_internal_assignments"], 1024)

        self.assertEqual(
            tuple(
                (item["length"], item["hit_count"])
                for item in certificate["hit_length_distributions"]["distance_preserving"]
            ),
            ((1, 0), (2, 0), (3, 0), (4, 4), (5, 8), (6, 83)),
        )
        self.assertEqual(
            tuple(
                (item["length"], item["hit_count"])
                for item in certificate["hit_length_distributions"]["low_distance_frontier"]
            ),
            ((1, 3), (2, 9), (3, 7), (4, 7), (5, 5), (6, 4)),
        )

        selected = certificate["selected_distance_preserving_hit"]
        self.assertEqual(selected["circuit"]["name"], "synth_bitrev_gray_5bit")
        self.assertEqual(selected["region"]["qubits"], (12, 19, 4, 11))
        self.assertEqual(selected["region"]["length"], 4)
        self.assertEqual(selected["first"]["entropy"], 3)
        self.assertEqual(selected["second"]["entropy"], 3)
        self.assertEqual(selected["min_cut"]["value"], 2)
        self.assertEqual(selected["min_cut"]["assignments_checked"], 1024)
        self.assertEqual(selected["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected["first"]["erasure_correctable"])
        self.assertTrue(selected["second"]["erasure_correctable"])

        frontier = certificate["selected_frontier_rejected_hit"]
        self.assertEqual(frontier["circuit"]["name"], "synth_inner_major_natural")
        self.assertEqual(frontier["region"]["qubits"], (9,))
        self.assertEqual(frontier["region"]["length"], 1)
        self.assertEqual(frontier["min_cut"]["value"], 3)

        no_compact = certificate["selected_fixed_patch_no_compact_hit_record"]
        self.assertEqual(no_compact["name"], "synth_block_major_phase2_inner_ring")
        self.assertTrue(no_compact["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"])
        self.assertTrue(no_compact["fixed_phase3_patch"]["operator_or_channel_split"])
        self.assertEqual(no_compact["interval_search"]["hit_count"], 0)

        family_summary = {
            item["generator_family"]: item
            for item in certificate["family_summary"]
        }
        self.assertEqual(family_summary["affine_modular_adjacency"]["circuits"], 30)
        self.assertEqual(family_summary["affine_modular_adjacency"]["distance_preserving_circuits"], 30)
        self.assertEqual(family_summary["affine_modular_adjacency"]["operator_or_channel_hits"], 70)
        self.assertEqual(family_summary["hierarchical_bit_adjacency"]["circuits"], 4)
        self.assertEqual(family_summary["hierarchical_bit_adjacency"]["distance_preserving_circuits"], 4)
        self.assertEqual(family_summary["hierarchical_bit_adjacency"]["operator_or_channel_hits"], 25)

    def test_holography_phase9_compressed_pentagon_two_layer_certificate(self):
        certificate = bridge_holography_phase9_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_9_compressed_pentagon_two_layer_certificate"])
        self.assertTrue(claims["phase3_repaired_source_loaded"])
        self.assertTrue(claims["two_layer_distance_screen_scored"])
        self.assertTrue(claims["pentagon_block_menu_scored"])
        self.assertTrue(claims["all_block_menu_circuits_distance_preserving"])
        self.assertTrue(claims["all_candidate_mincuts_exact_on_compressed_skeleton"])
        self.assertTrue(claims["compressed_skeleton_has_five_internal_blocks"])
        self.assertTrue(claims["all_reported_hits_are_entropy_matched_operator_or_channel_splits"])
        self.assertTrue(claims["distance_preserving_length_two_hits_exist"])
        self.assertTrue(claims["no_distance_preserving_length_one_hits"])
        self.assertTrue(claims["two_layer_compressed_blocks_improve_over_phase8_length_four"])

        self.assertEqual(certificate["counts"]["distance_screen_seed_layers"], 13)
        self.assertEqual(certificate["counts"]["distance_screen_ordered_pairs"], 169)
        self.assertEqual(certificate["counts"]["distance_screen_accepted_pairs"], 153)
        self.assertEqual(certificate["counts"]["distance_screen_rejected_pairs"], 16)
        self.assertEqual(certificate["counts"]["block_menu_circuits"], 18)
        self.assertEqual(certificate["counts"]["distance_preserving_block_menu_circuits"], 18)
        self.assertEqual(certificate["counts"]["candidate_intervals_scanned"], 2160)
        self.assertEqual(certificate["counts"]["entropy_gate_passes"], 2058)
        self.assertEqual(certificate["counts"]["entropy_gate_rejections"], 102)
        self.assertEqual(certificate["counts"]["operator_or_channel_hits"], 112)
        self.assertEqual(certificate["counts"]["distance_preserving_hits"], 112)
        self.assertEqual(certificate["counts"]["min_distance_preserving_hit_length"], 2)
        self.assertEqual(certificate["counts"]["max_candidate_min_cut_internal_assignments"], 32)

        self.assertEqual(
            tuple((item["length"], item["hit_count"]) for item in certificate["hit_length_distribution"]),
            ((1, 0), (2, 2), (3, 7), (4, 22), (5, 34), (6, 47)),
        )

        selected = certificate["selected_distance_preserving_hit"]
        self.assertEqual(selected["circuit"]["name"], "pentagon_bitrev_gray_5bit__then__bitrev_gray_5bit")
        self.assertEqual(selected["region"]["qubits"], (19, 4))
        self.assertEqual(selected["region"]["length"], 2)
        self.assertEqual(selected["first"]["entropy"], 2)
        self.assertEqual(selected["second"]["entropy"], 2)
        self.assertEqual(selected["min_cut"]["value"], 4)
        self.assertEqual(selected["min_cut"]["assignments_checked"], 32)
        self.assertEqual(selected["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected["first"]["erasure_correctable"])
        self.assertTrue(selected["second"]["erasure_correctable"])

        rejected = certificate["distance_screen"]["rejected_pair_records"]
        self.assertEqual(len(rejected), 16)
        self.assertEqual(rejected[0]["first_layer"], "synth_affine_stride1_offset1")
        self.assertEqual(rejected[0]["second_layer"], "synth_bit_reversal_5bit")
        self.assertFalse(rejected[0]["distance_gate_accepted"])
        self.assertEqual(rejected[0]["second_distance"]["logical_witness"]["qubits"], (13,))

        for record in certificate["circuit_records"]:
            self.assertTrue(record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"])
            self.assertEqual(record["network"]["internal_assignments_per_min_cut"], 32)

    def test_holography_phase10_five_qubit_perfect_outer_certificate(self):
        certificate = bridge_holography_phase10_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_10_five_qubit_perfect_outer_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["outer_code_is_five_qubit_perfect_code"])
        self.assertTrue(claims["perfect_outer_concatenation_k1_n25"])
        self.assertTrue(claims["exact_distance_profile_certified"])
        self.assertTrue(claims["both_distances_at_least_three"])
        self.assertTrue(claims["all_labeled_t2_entropy_matches"])
        self.assertTrue(claims["three_boundary_atlases_scored"])
        self.assertTrue(claims["all_interval_mincuts_exact"])
        self.assertTrue(claims["block_contiguous_has_no_compact_hits"])
        self.assertTrue(claims["inner_major_has_length_three_compact_hits"])
        self.assertTrue(claims["lifted_three_block_witnesses_exist"])
        self.assertTrue(claims["source_aware_lifted_strict_hits_exist"])

        outer = certificate["perfect_outer_source"]["outer_code"]
        self.assertEqual(outer["parameters"], {"distance": 3, "k": 1, "n": 5})
        self.assertEqual(outer["erasure_threshold"], 2)
        self.assertTrue(outer["perfect_tensor_like_checks"]["all_size_two_or_less_erasures_correctable"])
        self.assertTrue(outer["perfect_tensor_like_checks"]["all_size_three_regions_reconstruct"])

        self.assertEqual(certificate["code_pair"]["n"], 25)
        self.assertEqual(certificate["code_pair"]["k"], 1)
        self.assertEqual(certificate["distance_audit"]["first_exact_distance"], 3)
        self.assertEqual(certificate["distance_audit"]["second_exact_distance"], 4)
        self.assertEqual(certificate["distance_audit"]["first"]["logical_witness"]["qubits"], (4, 9, 14))
        self.assertEqual(certificate["distance_audit"]["second"]["logical_witness"]["qubits"], (0, 4, 9, 24))

        self.assertEqual(certificate["counts"]["low_order_subsets_checked"], 326)
        self.assertEqual(certificate["counts"]["low_order_entropy_mismatches"], 0)
        self.assertEqual(certificate["counts"]["boundary_atlases"], 3)
        self.assertEqual(certificate["counts"]["candidate_intervals_scanned"], 600)
        self.assertEqual(certificate["counts"]["entropy_gate_passes"], 493)
        self.assertEqual(certificate["counts"]["entropy_gate_rejections"], 107)
        self.assertEqual(certificate["counts"]["compact_interval_hits"], 29)
        self.assertEqual(certificate["counts"]["block_contiguous_hits"], 0)
        self.assertEqual(certificate["counts"]["inner_major_hits"], 12)
        self.assertEqual(certificate["counts"]["witness_strip_hits"], 17)
        self.assertEqual(certificate["counts"]["min_inner_major_hit_length"], 3)
        self.assertEqual(certificate["counts"]["lifted_block_masks_checked"], 31)
        self.assertEqual(certificate["counts"]["lifted_three_block_hits"], 10)
        self.assertEqual(certificate["counts"]["strict_lifted_hits"], 3)
        self.assertEqual(certificate["counts"]["max_candidate_min_cut_internal_assignments"], 32)

        selected = certificate["boundary_atlas_search"]["selected_interval_hit"]
        self.assertEqual(selected["circuit"]["name"], "perfect_outer_inner_major")
        self.assertEqual(selected["region"]["qubits"], (4, 9, 14))
        self.assertEqual(selected["region"]["length"], 3)
        self.assertEqual(selected["first"]["entropy"], 3)
        self.assertEqual(selected["second"]["entropy"], 3)
        self.assertEqual(selected["min_cut"]["value"], 5)
        self.assertEqual(selected["min_cut"]["assignments_checked"], 32)
        self.assertEqual(selected["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(selected["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected["first"]["erasure_correctable"])
        self.assertTrue(selected["second"]["erasure_correctable"])

        templates = {
            record["name"]: record
            for record in certificate["boundary_atlas_search"]["templates"]
        }
        self.assertEqual(templates["perfect_outer_block_contiguous"]["interval_search"]["hit_count"], 0)
        self.assertEqual(templates["perfect_outer_inner_major"]["interval_search"]["shortest_hit_length"], 3)
        self.assertEqual(templates["perfect_outer_witness_strip"]["interval_search"]["shortest_hit_length"], 5)

        lifted = certificate["lifted_phase2_witness_audit"]["selected_lifted_hit"]
        self.assertEqual(lifted["region"]["block_mask"], 7)
        self.assertEqual(lifted["region"]["qubits"], (2, 4, 7, 9, 12, 14))
        self.assertTrue(lifted["interval_location"]["is_boundary_ring_interval"])
        self.assertEqual(lifted["interval_location"]["start"], 0)
        self.assertEqual(lifted["min_cut"]["value"], 8)
        self.assertEqual(lifted["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(lifted["second"]["algebra_signature"], (0, 0, 2, False))

    def test_holography_phase11_same_distance_perfect_outer_variant_certificate(self):
        certificate = bridge_holography_phase11_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_11_same_distance_perfect_outer_variant_certificate"])
        self.assertTrue(claims["outer_variant_menu_bounded_and_scored"])
        self.assertTrue(claims["all_outer_variants_remain_five_qubit_perfect"])
        self.assertTrue(claims["all_variants_preserve_labeled_t2_entropy"])
        self.assertTrue(claims["same_distance_variants_exist"])
        self.assertTrue(claims["asymmetric_variants_remain_in_menu"])
        self.assertTrue(claims["same_distance_variants_keep_inner_major_length_three_hits"])
        self.assertTrue(claims["selected_variant_is_single_hadamard_q0"])
        self.assertTrue(claims["selected_variant_has_exact_same_distance_three"])
        self.assertTrue(claims["selected_variant_replays_phase10_compact_atlas"])
        self.assertTrue(claims["source_aware_lifted_strict_hits_survive"])

        self.assertEqual(certificate["counts"]["outer_variants_scored"], 44)
        self.assertEqual(certificate["counts"]["outer_variants_all_perfect"], 44)
        self.assertEqual(certificate["counts"]["low_order_t2_matches"], 44)
        self.assertEqual(certificate["counts"]["same_exact_distance_three_variants"], 20)
        self.assertEqual(certificate["counts"]["asymmetric_or_second_distance_at_least_four_variants"], 24)
        self.assertEqual(certificate["counts"]["same_distance_compact_scans"], 20)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_hit_variants"], 20)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_total_hits"], 240)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_min_hit_length"], 3)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_intervals_scanned"], 4000)
        self.assertEqual(certificate["counts"]["selected_candidate_intervals_scanned"], 600)
        self.assertEqual(certificate["counts"]["selected_entropy_gate_passes"], 493)
        self.assertEqual(certificate["counts"]["selected_entropy_gate_rejections"], 107)
        self.assertEqual(certificate["counts"]["selected_compact_interval_hits"], 29)
        self.assertEqual(certificate["counts"]["selected_block_contiguous_hits"], 0)
        self.assertEqual(certificate["counts"]["selected_inner_major_hits"], 12)
        self.assertEqual(certificate["counts"]["selected_witness_strip_hits"], 17)
        self.assertEqual(certificate["counts"]["lifted_block_masks_checked"], 31)
        self.assertEqual(certificate["counts"]["lifted_three_block_hits"], 10)
        self.assertEqual(certificate["counts"]["strict_lifted_hits"], 3)

        family_counts = {
            record["family"]: record
            for record in certificate["outer_variant_search"]["family_counts"]
        }
        self.assertEqual(family_counts["global_local_clifford"]["variants"], 4)
        self.assertEqual(family_counts["global_local_clifford"]["same_exact_distance_three"], 0)
        self.assertEqual(family_counts["outer_permutation"]["variants"], 5)
        self.assertEqual(family_counts["outer_permutation"]["same_exact_distance_three"], 0)
        self.assertEqual(family_counts["single_site_local_clifford"]["variants"], 15)
        self.assertEqual(family_counts["single_site_local_clifford"]["same_exact_distance_three"], 10)
        self.assertEqual(family_counts["two_site_hadamard"]["variants"], 10)
        self.assertEqual(family_counts["two_site_hadamard"]["same_exact_distance_three"], 10)
        self.assertEqual(family_counts["two_site_phase"]["variants"], 10)
        self.assertEqual(family_counts["two_site_phase"]["same_exact_distance_three"], 0)

        names = certificate["outer_variant_search"]["same_distance_variant_names"]
        self.assertEqual(len(names), 20)
        self.assertEqual(names[:4], ("q0_H", "q0_HS", "q1_H", "q1_HS"))

        selected_variant = certificate["selected_same_distance_variant"]["variant_record"]
        self.assertEqual(selected_variant["spec"]["name"], "q0_H")
        self.assertEqual(selected_variant["distance_audit_weight3"]["first_exact_distance"], 3)
        self.assertEqual(selected_variant["distance_audit_weight3"]["second_exact_distance"], 3)
        self.assertEqual(selected_variant["distance_audit_weight3"]["first"]["logical_witness"]["qubits"], (4, 9, 14))
        self.assertEqual(selected_variant["distance_audit_weight3"]["second"]["logical_witness"]["qubits"], (4, 9, 24))

        selected_hit = certificate["selected_same_distance_variant"]["boundary_atlas_search"]["selected_interval_hit"]
        self.assertEqual(selected_hit["circuit"]["name"], "perfect_outer_inner_major")
        self.assertEqual(selected_hit["region"]["qubits"], (4, 9, 14))
        self.assertEqual(selected_hit["region"]["length"], 3)
        self.assertEqual(selected_hit["first"]["entropy"], 3)
        self.assertEqual(selected_hit["second"]["entropy"], 3)
        self.assertEqual(selected_hit["min_cut"]["value"], 5)
        self.assertEqual(selected_hit["min_cut"]["assignments_checked"], 32)
        self.assertEqual(selected_hit["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(selected_hit["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected_hit["first"]["erasure_correctable"])
        self.assertTrue(selected_hit["second"]["erasure_correctable"])

        templates = {
            record["name"]: record
            for record in certificate["selected_same_distance_variant"]["boundary_atlas_search"]["templates"]
        }
        self.assertEqual(templates["perfect_outer_block_contiguous"]["interval_search"]["hit_count"], 0)
        self.assertEqual(templates["perfect_outer_inner_major"]["interval_search"]["shortest_hit_length"], 3)
        self.assertEqual(templates["perfect_outer_witness_strip"]["interval_search"]["shortest_hit_length"], 5)

        lifted = certificate["selected_same_distance_variant"]["lifted_phase2_witness_audit"]["selected_lifted_hit"]
        self.assertEqual(lifted["region"]["block_mask"], 7)
        self.assertEqual(lifted["region"]["qubits"], (2, 4, 7, 9, 12, 14))
        self.assertTrue(lifted["interval_location"]["is_boundary_ring_interval"])
        self.assertEqual(lifted["interval_location"]["length"], 6)
        self.assertEqual(lifted["min_cut"]["value"], 8)
        self.assertEqual(lifted["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(lifted["second"]["algebra_signature"], (0, 0, 2, False))

    def test_holography_phase12_outer_embedding_robustness_certificate(self):
        certificate = bridge_holography_phase12_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_12_outer_embedding_robustness_certificate"])
        self.assertTrue(claims["phase12_superset_menu_scored"])
        self.assertTrue(claims["phase11_menu_embedded"])
        self.assertTrue(claims["full_s5_outer_permutations_covered"])
        self.assertTrue(claims["all_outer_variants_remain_five_qubit_perfect"])
        self.assertTrue(claims["all_variants_preserve_labeled_t2_entropy"])
        self.assertTrue(claims["same_distance_variants_exactly_30"])
        self.assertTrue(claims["new_single_site_lc_variants_add_10_same_distance_hits"])
        self.assertTrue(claims["pure_outer_permutations_do_not_repair_distance_asymmetry"])
        self.assertTrue(claims["global_full_lc_variants_do_not_repair_distance_asymmetry"])
        self.assertTrue(claims["all_same_distance_variants_keep_inner_major_length_three_hits"])
        self.assertTrue(claims["selected_variant_remains_phase11_q0_H"])
        self.assertTrue(claims["selected_variant_replays_phase10_compact_atlas"])
        self.assertTrue(claims["source_aware_lifted_strict_hits_survive"])

        self.assertEqual(certificate["counts"]["outer_embedding_variants_scored"], 170)
        self.assertEqual(certificate["counts"]["phase11_seed_variants"], 44)
        self.assertEqual(certificate["counts"]["added_variants"], 126)
        self.assertEqual(certificate["counts"]["outer_variants_all_perfect"], 170)
        self.assertEqual(certificate["counts"]["low_order_t2_matches"], 170)
        self.assertEqual(certificate["counts"]["same_exact_distance_three_variants"], 30)
        self.assertEqual(certificate["counts"]["same_distance_phase11_seed_variants"], 20)
        self.assertEqual(certificate["counts"]["same_distance_added_single_site_lc_variants"], 10)
        self.assertEqual(certificate["counts"]["pure_permutation_specs"], 119)
        self.assertEqual(certificate["counts"]["full_s5_permutations_covered_with_identity"], 120)
        self.assertEqual(certificate["counts"]["pure_permutation_same_distance_variants"], 0)
        self.assertEqual(certificate["counts"]["same_distance_compact_scans"], 30)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_hit_variants"], 30)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_total_hits"], 360)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_min_hit_length"], 3)
        self.assertEqual(certificate["counts"]["same_distance_inner_major_intervals_scanned"], 6000)
        self.assertEqual(certificate["counts"]["selected_candidate_intervals_scanned"], 600)
        self.assertEqual(certificate["counts"]["selected_compact_interval_hits"], 29)
        self.assertEqual(certificate["counts"]["selected_block_contiguous_hits"], 0)
        self.assertEqual(certificate["counts"]["selected_inner_major_hits"], 12)
        self.assertEqual(certificate["counts"]["selected_witness_strip_hits"], 17)
        self.assertEqual(certificate["counts"]["lifted_block_masks_checked"], 31)
        self.assertEqual(certificate["counts"]["lifted_three_block_hits"], 10)
        self.assertEqual(certificate["counts"]["strict_lifted_hits"], 3)

        family_counts = {
            record["family"]: record
            for record in certificate["outer_embedding_search"]["family_counts"]
        }
        self.assertEqual(family_counts["added_global_full_lc"]["variants"], 2)
        self.assertEqual(family_counts["added_global_full_lc"]["same_exact_distance_three"], 0)
        self.assertEqual(family_counts["added_outer_permutation_full_s5"]["variants"], 114)
        self.assertEqual(family_counts["added_outer_permutation_full_s5"]["same_exact_distance_three"], 0)
        self.assertEqual(family_counts["added_single_site_full_lc"]["variants"], 10)
        self.assertEqual(family_counts["added_single_site_full_lc"]["same_exact_distance_three"], 10)
        self.assertEqual(family_counts["single_site_local_clifford"]["same_exact_distance_three"], 10)
        self.assertEqual(family_counts["two_site_hadamard"]["same_exact_distance_three"], 10)
        self.assertEqual(family_counts["outer_permutation"]["same_exact_distance_three"], 0)

        names = certificate["outer_embedding_search"]["same_distance_variant_names"]
        self.assertEqual(len(names), 30)
        self.assertEqual(names[:4], ("q0_H", "q0_HS", "q1_H", "q1_HS"))
        self.assertEqual(names[-4:], ("q3_LC1", "q3_LC4", "q4_LC1", "q4_LC4"))

        selected_variant = certificate["selected_same_distance_variant"]["variant_record"]
        self.assertEqual(selected_variant["spec"]["name"], "q0_H")
        self.assertEqual(selected_variant["distance_audit_weight3"]["first_exact_distance"], 3)
        self.assertEqual(selected_variant["distance_audit_weight3"]["second_exact_distance"], 3)

        selected_hit = certificate["selected_same_distance_variant"]["boundary_atlas_search"]["selected_interval_hit"]
        self.assertEqual(selected_hit["region"]["qubits"], (4, 9, 14))
        self.assertEqual(selected_hit["region"]["length"], 3)
        self.assertEqual(selected_hit["first"]["entropy"], 3)
        self.assertEqual(selected_hit["second"]["entropy"], 3)
        self.assertEqual(selected_hit["min_cut"]["value"], 5)
        self.assertEqual(selected_hit["min_cut"]["assignments_checked"], 32)
        self.assertEqual(selected_hit["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(selected_hit["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected_hit["first"]["erasure_correctable"])
        self.assertTrue(selected_hit["second"]["erasure_correctable"])

        lifted = certificate["selected_same_distance_variant"]["lifted_phase2_witness_audit"]["selected_lifted_hit"]
        self.assertEqual(lifted["region"]["block_mask"], 7)
        self.assertEqual(lifted["region"]["qubits"], (2, 4, 7, 9, 12, 14))
        self.assertTrue(lifted["interval_location"]["is_boundary_ring_interval"])
        self.assertEqual(lifted["min_cut"]["value"], 8)
        self.assertEqual(lifted["first"]["algebra_signature"], (2, 0, 0, True))
        self.assertEqual(lifted["second"]["algebra_signature"], (0, 0, 2, False))

    def test_holography_phase13_two_perfect_tensor_tiling_certificate(self):
        certificate = bridge_holography_phase13_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_13_two_perfect_tensor_tiling_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["two_perfect_outer_codes_are_k1_distance3"])
        self.assertTrue(claims["all_variants_preserve_labeled_t2_entropy"])
        self.assertTrue(claims["unrepaired_bridge_identities_are_distance_asymmetric"])
        self.assertTrue(claims["same_distance_tiling_repairs_exist"])
        self.assertTrue(claims["x_and_y_bridge_repairs_classified"])
        self.assertTrue(claims["representative_repair_families_keep_inner_major_length_three_hits"])
        self.assertTrue(claims["selected_variant_is_y_q0_h"])
        self.assertTrue(claims["selected_variant_replays_two_tensor_atlas"])
        self.assertTrue(claims["selected_interval_mincuts_exact"])

        counts = certificate["counts"]
        self.assertEqual(counts["tiling_variants_scored"], 48)
        self.assertEqual(counts["bridge_identity_variants"], 3)
        self.assertEqual(counts["distance_asymmetric_identity_variants"], 3)
        self.assertEqual(counts["outer_variants_k1_distance3"], 48)
        self.assertEqual(counts["low_order_t2_matches"], 48)
        self.assertEqual(counts["same_exact_distance_three_variants"], 45)
        self.assertEqual(counts["same_distance_compact_scans"], 3)
        self.assertEqual(counts["same_distance_inner_major_hit_variants"], 3)
        self.assertEqual(counts["same_distance_inner_major_intervals_scanned"], 1200)
        self.assertEqual(counts["same_distance_inner_major_total_hits"], 60)
        self.assertEqual(counts["same_distance_inner_major_min_hit_length"], 3)
        self.assertEqual(counts["selected_candidate_intervals_scanned"], 1600)
        self.assertEqual(counts["selected_compact_interval_hits"], 77)
        self.assertEqual(counts["selected_block_contiguous_hits"], 0)
        self.assertEqual(counts["selected_inner_major_hits"], 20)
        self.assertEqual(counts["selected_cell_major_hits"], 22)
        self.assertEqual(counts["selected_witness_strip_hits"], 35)
        self.assertEqual(counts["selected_entropy_gate_passes"], 1352)
        self.assertEqual(counts["selected_entropy_gate_rejections"], 248)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 4)

        family_counts = {
            record["family"]: record
            for record in certificate["tiling_variant_search"]["family_counts"]
        }
        self.assertEqual(family_counts["bridge_identity"]["variants"], 3)
        self.assertEqual(family_counts["bridge_identity"]["same_exact_distance_three"], 0)
        self.assertEqual(family_counts["x_bridge_single_site_axis_swap"]["variants"], 20)
        self.assertEqual(family_counts["x_bridge_single_site_axis_swap"]["same_exact_distance_three"], 20)
        self.assertEqual(family_counts["y_bridge_single_site_axis_swap"]["variants"], 20)
        self.assertEqual(family_counts["y_bridge_single_site_axis_swap"]["same_exact_distance_three"], 20)
        self.assertEqual(family_counts["y_bridge_paired_leg_hadamard"]["variants"], 5)
        self.assertEqual(family_counts["y_bridge_paired_leg_hadamard"]["same_exact_distance_three"], 5)

        compact_scan = certificate["same_distance_compact_scan"]
        self.assertEqual(
            tuple(compact_scan["representative_variant_names"]),
            ("X_q0_HS", "Y_q0_H", "Y_paired_leg0_H"),
        )
        for record in compact_scan["variant_records"]:
            self.assertEqual(record["interval_search"]["hit_count"], 20)
            self.assertEqual(record["interval_search"]["shortest_hit_length"], 3)

        selected = certificate["selected_same_distance_tiling"]
        self.assertEqual(selected["variant_record"]["spec"]["name"], "Y_q0_H")
        distance_audit = selected["variant_record"]["distance_audit_weight3"]
        self.assertTrue(distance_audit["same_exact_distance_three"])
        self.assertEqual(distance_audit["first_exact_distance"], 3)
        self.assertEqual(distance_audit["second_exact_distance"], 3)
        self.assertEqual(distance_audit["first"]["logical_witness"]["qubits"], (4, 9, 14))
        self.assertEqual(distance_audit["second"]["logical_witness"]["qubits"], (4, 9, 24))

        selected_hit = selected["boundary_atlas_search"]["selected_interval_hit"]
        self.assertEqual(selected_hit["region"]["qubits"], (4, 9, 14))
        self.assertEqual(selected_hit["region"]["length"], 3)
        self.assertEqual(selected_hit["first"]["entropy"], 3)
        self.assertEqual(selected_hit["second"]["entropy"], 3)
        self.assertEqual(selected_hit["min_cut"]["value"], 5)
        self.assertEqual(selected_hit["min_cut"]["assignments_checked"], 4)
        self.assertEqual(selected_hit["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected_hit["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected_hit["first"]["erasure_correctable"])
        self.assertTrue(selected_hit["second"]["erasure_correctable"])
        self.assertFalse(selected_hit["first"]["survivor_fixed_point_reconstructs_all"])
        self.assertTrue(selected_hit["second"]["survivor_fixed_point_reconstructs_all"])

        templates = {
            record["name"]: record
            for record in selected["boundary_atlas_search"]["templates"]
        }
        self.assertEqual(templates["two_perfect_block_contiguous"]["interval_search"]["hit_count"], 0)
        self.assertEqual(templates["two_perfect_inner_major"]["interval_search"]["hit_count"], 20)
        self.assertEqual(templates["two_perfect_inner_major"]["interval_search"]["shortest_hit_length"], 3)
        self.assertEqual(templates["two_perfect_cell_major"]["interval_search"]["hit_count"], 22)
        self.assertEqual(templates["two_perfect_cell_major"]["interval_search"]["shortest_hit_length"], 3)
        self.assertEqual(templates["two_perfect_witness_strip"]["interval_search"]["hit_count"], 35)
        self.assertEqual(templates["two_perfect_witness_strip"]["interval_search"]["shortest_hit_length"], 5)

    def test_holography_phase14_three_perfect_chain_ring_certificate(self):
        certificate = bridge_holography_phase14_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_14_three_perfect_chain_ring_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["three_perfect_chain_menu_scored"])
        self.assertTrue(claims["three_perfect_outer_codes_are_k1_distance3"])
        self.assertTrue(claims["all_variants_preserve_labeled_t2_entropy"])
        self.assertTrue(claims["unrepaired_bridge_identities_are_distance_asymmetric"])
        self.assertTrue(claims["single_cell_axis_repairs_are_same_distance"])
        self.assertTrue(claims["selected_variant_is_yy_q0_h"])
        self.assertTrue(claims["chain_and_ring_skeletons_scored"])
        self.assertTrue(claims["block_contiguous_remains_zero_hit_control"])
        self.assertTrue(claims["chain_and_ring_inner_major_hits_match"])
        self.assertTrue(claims["selected_inner_major_witness_matches_across_topologies"])
        self.assertTrue(claims["selected_interval_mincuts_exact"])

        counts = certificate["counts"]
        self.assertEqual(counts["tiling_variants_scored"], 9)
        self.assertEqual(counts["bridge_identity_variants"], 3)
        self.assertEqual(counts["distance_asymmetric_identity_variants"], 3)
        self.assertEqual(counts["outer_variants_k1_distance3"], 9)
        self.assertEqual(counts["low_order_t2_matches"], 9)
        self.assertEqual(counts["same_exact_distance_three_variants"], 6)
        self.assertEqual(counts["selected_topologies_scored"], 2)
        self.assertEqual(counts["selected_templates_per_topology"], 4)
        self.assertEqual(counts["selected_candidate_intervals_scanned"], 4800)
        self.assertEqual(counts["selected_entropy_gate_passes"], 4062)
        self.assertEqual(counts["selected_entropy_gate_rejections"], 738)
        self.assertEqual(counts["selected_compact_interval_hits"], 226)
        self.assertEqual(counts["selected_block_contiguous_hits"], 0)
        self.assertEqual(counts["selected_inner_major_hits"], 54)
        self.assertEqual(counts["selected_cell_major_hits"], 66)
        self.assertEqual(counts["selected_witness_strip_hits"], 106)
        self.assertEqual(counts["chain_compact_interval_hits"], 113)
        self.assertEqual(counts["ring_compact_interval_hits"], 113)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 8)

        family_counts = {
            record["family"]: record
            for record in certificate["tiling_variant_search"]["family_counts"]
        }
        self.assertEqual(family_counts["bridge_identity"]["variants"], 3)
        self.assertEqual(family_counts["bridge_identity"]["same_exact_distance_three"], 0)
        self.assertEqual(family_counts["xx_bridge_single_cell_axis_swap"]["variants"], 3)
        self.assertEqual(family_counts["xx_bridge_single_cell_axis_swap"]["same_exact_distance_three"], 3)
        self.assertEqual(family_counts["yy_bridge_single_cell_axis_swap"]["variants"], 3)
        self.assertEqual(family_counts["yy_bridge_single_cell_axis_swap"]["same_exact_distance_three"], 3)

        selected = certificate["selected_same_distance_tiling"]
        self.assertEqual(selected["variant_record"]["spec"]["name"], "YY_q0_H")
        distance_audit = selected["variant_record"]["distance_audit_weight3"]
        self.assertEqual(distance_audit["distance_certification_method"], "weight2_lower_bound_plus_explicit_weight3_witness")
        self.assertTrue(distance_audit["same_exact_distance_three"])
        self.assertEqual(distance_audit["first_exact_distance"], 3)
        self.assertEqual(distance_audit["second_exact_distance"], 3)
        self.assertTrue(distance_audit["first"]["exact_distance_three_certified"])
        self.assertTrue(distance_audit["second"]["exact_distance_three_certified"])
        self.assertEqual(distance_audit["first"]["logical_witness"]["qubits"], (4, 9, 14))
        self.assertEqual(distance_audit["second"]["logical_witness"]["qubits"], (4, 9, 24))

        summaries = {
            record["topology"]: record
            for record in selected["topology_summaries"]
        }
        for topology in ("chain", "ring"):
            self.assertEqual(summaries[topology]["candidate_intervals_scanned"], 2400)
            self.assertEqual(summaries[topology]["compact_interval_hits"], 113)
            self.assertEqual(summaries[topology]["block_contiguous_hits"], 0)
            self.assertEqual(summaries[topology]["inner_major_hits"], 27)
            self.assertEqual(summaries[topology]["cell_major_hits"], 33)
            self.assertEqual(summaries[topology]["witness_strip_hits"], 53)

        for key in ("selected_chain_inner_major_hit", "selected_ring_inner_major_hit"):
            hit = selected[key]
            self.assertEqual(hit["region"]["qubits"], (4, 9, 14))
            self.assertEqual(hit["region"]["length"], 3)
            self.assertEqual(hit["first"]["entropy"], 3)
            self.assertEqual(hit["second"]["entropy"], 3)
            self.assertEqual(hit["min_cut"]["value"], 5)
            self.assertEqual(hit["min_cut"]["assignments_checked"], 8)
            self.assertEqual(hit["first"]["algebra_signature"], (1, 1, 1, False))
            self.assertEqual(hit["second"]["algebra_signature"], (0, 0, 2, False))
            self.assertFalse(hit["first"]["erasure_correctable"])
            self.assertTrue(hit["second"]["erasure_correctable"])
            self.assertFalse(hit["first"]["survivor_fixed_point_reconstructs_all"])
            self.assertTrue(hit["second"]["survivor_fixed_point_reconstructs_all"])

    def test_holography_phase15_capacity_branching_fixed_witness_certificate(self):
        certificate = bridge_holography_phase15_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_15_capacity_branching_grammar_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["selected_phase14_tiling_loaded"])
        self.assertTrue(claims["capacity_branching_skeleton_grammar_scored"])
        self.assertTrue(claims["branching_skeletons_included"])
        self.assertTrue(claims["all_mincuts_exact"])
        self.assertTrue(claims["all_fixed_regions_keep_entropy_match"])
        self.assertTrue(claims["all_fixed_regions_keep_operator_or_channel_split"])
        self.assertTrue(claims["all_fixed_region_mincuts_invariant_across_capacity_grammar"])
        self.assertTrue(claims["cross_cell_witnesses_included"])

        counts = certificate["counts"]
        self.assertEqual(counts["skeletons_scored"], 18)
        self.assertEqual(counts["fixed_regions_scored"], 3)
        self.assertEqual(counts["region_skeleton_records"], 54)
        self.assertEqual(counts["topologies_scored"], 4)
        self.assertEqual(counts["branching_skeletons"], 8)
        self.assertEqual(counts["min_cut_invariant_regions"], 3)
        self.assertEqual(counts["min_cut_variable_regions"], 0)
        self.assertEqual(counts["entropy_match_records"], 54)
        self.assertEqual(counts["operator_or_channel_split_records"], 54)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 8)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 16)

        topology_counts = {
            record["topology"]: record
            for record in certificate["capacity_branching_grammar"]["topology_counts"]
        }
        self.assertEqual(topology_counts["chain"]["skeletons"], 5)
        self.assertEqual(topology_counts["ring"]["skeletons"], 5)
        self.assertEqual(topology_counts["rooted_branch"]["skeletons"], 5)
        self.assertEqual(topology_counts["branch_plus_chain"]["skeletons"], 3)

        region_summaries = {
            record["region"]: record
            for record in certificate["capacity_branching_grammar"]["region_summaries"]
        }
        self.assertEqual(region_summaries["inner_major_local_short"]["min_cut_values"], (5,))
        self.assertEqual(region_summaries["inner_major_local_short"]["entropy_values"], ((3, 3),))
        self.assertEqual(region_summaries["inner_major_cross_cell_short"]["min_cut_values"], (6,))
        self.assertEqual(region_summaries["inner_major_cross_cell_short"]["entropy_values"], ((4, 4),))
        self.assertEqual(region_summaries["witness_strip_cross_cell"]["min_cut_values"], (8,))
        self.assertEqual(region_summaries["witness_strip_cross_cell"]["entropy_values"], ((6, 6),))
        for summary in region_summaries.values():
            self.assertEqual(summary["records"], 18)
            self.assertEqual(summary["operator_or_channel_split_records"], 18)
            self.assertEqual(
                summary["topologies"],
                ("branch_plus_chain", "chain", "ring", "rooted_branch"),
            )

        first_record = certificate["capacity_branching_grammar"]["records"][0]
        self.assertEqual(first_record["region"]["name"], "inner_major_local_short")
        self.assertEqual(first_record["skeleton"]["name"], "chain_1_1")
        self.assertEqual(first_record["network"]["internal_assignments_per_min_cut"], 8)
        self.assertEqual(first_record["hit"]["min_cut"]["value"], 5)
        self.assertEqual(first_record["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(first_record["hit"]["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertTrue(first_record["hit"]["comparisons"]["entropy_matches"])
        self.assertTrue(first_record["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertTrue(first_record["hit"]["comparisons"]["min_cut_exact"])

    def test_holography_phase16_capacity_sensitive_interval_no_go_certificate(self):
        certificate = bridge_holography_phase16_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_16_capacity_sensitive_interval_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["selected_phase14_tiling_loaded"])
        self.assertTrue(claims["bounded_capacity_sensitive_interval_search_scored"])
        self.assertTrue(claims["min_cut_variation_filter_nonempty"])
        self.assertTrue(claims["entropy_candidates_after_variation_exist"])
        self.assertTrue(claims["all_filtered_mincuts_exact"])
        self.assertTrue(claims["no_capacity_sensitive_operator_or_channel_hits_found"])

        counts = certificate["counts"]
        self.assertEqual(counts["templates_scored"], 2)
        self.assertEqual(counts["probe_skeletons"], 8)
        self.assertEqual(counts["intervals_scanned"], 5550)
        self.assertEqual(counts["variable_min_cut_intervals"], 1888)
        self.assertEqual(counts["entropy_match_after_variation"], 196)
        self.assertEqual(counts["operator_or_channel_hits"], 0)
        self.assertEqual(counts["inner_major_variable_min_cut_intervals"], 450)
        self.assertEqual(counts["inner_major_entropy_match_after_variation"], 196)
        self.assertEqual(counts["witness_strip_variable_min_cut_intervals"], 1438)
        self.assertEqual(counts["witness_strip_entropy_match_after_variation"], 0)

        self.assertEqual(certificate["search_grammar"]["min_interval_length"], 9)
        self.assertEqual(certificate["search_grammar"]["max_interval_length"], 45)
        self.assertEqual(
            tuple(record["name"] for record in certificate["search_grammar"]["skeletons"]),
            (
                "chain_1_1",
                "chain_3_3",
                "ring_1_1_1",
                "ring_3_3_3",
                "rooted_branch_1_1_1",
                "rooted_branch_3_3_3",
                "branch_plus_chain_2_2_1_1_1",
                "branch_plus_chain_2_2_2_2_2",
            ),
        )

        template_records = {
            record["template"]["name"]: record
            for record in certificate["template_searches"]
        }
        inner = template_records["three_perfect_inner_major"]
        witness = template_records["three_perfect_witness_strip"]
        self.assertEqual(inner["interval_search"]["intervals_scanned"], 2775)
        self.assertEqual(inner["interval_search"]["variable_min_cut_intervals"], 450)
        self.assertEqual(inner["interval_search"]["entropy_match_after_variation"], 196)
        self.assertEqual(inner["interval_search"]["operator_or_channel_hits"], 0)
        self.assertEqual(witness["interval_search"]["intervals_scanned"], 2775)
        self.assertEqual(witness["interval_search"]["variable_min_cut_intervals"], 1438)
        self.assertEqual(witness["interval_search"]["entropy_match_after_variation"], 0)
        self.assertEqual(witness["interval_search"]["operator_or_channel_hits"], 0)

        inner_example = inner["entropy_match_examples"][0]
        self.assertEqual(inner_example["region"]["length"], 34)
        self.assertEqual(inner_example["region"]["start"], 0)
        self.assertEqual(inner_example["entropies"], {"first": 26, "second": 26})
        self.assertEqual(
            tuple(record["value"] for record in inner_example["min_cut_values_by_skeleton"]),
            (34, 36, 35, 36, 34, 36, 36, 36),
        )
        witness_example = witness["variable_examples"][0]
        self.assertEqual(witness_example["region"]["length"], 14)
        self.assertEqual(witness_example["region"]["start"], 30)
        self.assertEqual(
            tuple(record["value"] for record in witness_example["min_cut_values_by_skeleton"]),
            (14, 16, 15, 16, 14, 16, 16, 16),
        )

    def test_holography_phase17_four_cell_tree_fixed_witness_certificate(self):
        certificate = bridge_holography_phase17_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_17_four_cell_tree_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["four_cell_tree_outer_built"])
        self.assertTrue(claims["outer_distance_three_witnessed"])
        self.assertTrue(claims["four_tree_concatenation_k1_n100"])
        self.assertTrue(claims["all_labeled_t2_entropy_matches"])
        self.assertTrue(claims["fixed_tree_witnesses_scored"])
        self.assertTrue(claims["all_mincuts_exact"])
        self.assertTrue(claims["all_fixed_regions_keep_entropy_match"])
        self.assertTrue(claims["all_fixed_regions_keep_operator_or_channel_split"])
        self.assertTrue(claims["all_fixed_region_mincuts_invariant_across_tree_capacities"])
        self.assertTrue(claims["all_four_cells_touched"])
        self.assertTrue(claims["branch_spanning_witnesses_included"])

        source = certificate["four_cell_tree_source"]
        self.assertEqual(source["outer_code"]["parameters"], {"n": 20, "k": 1})
        self.assertEqual(
            source["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        self.assertEqual(source["code_pair"]["n"], 100)
        self.assertEqual(source["code_pair"]["k"], 1)
        self.assertEqual(source["low_order_entropy"]["subsets_checked"], 5051)
        self.assertEqual(source["low_order_entropy"]["mismatch_count"], 0)
        self.assertTrue(source["low_order_entropy"]["matches"])

        counts = certificate["counts"]
        self.assertEqual(counts["fixed_regions_scored"], 8)
        self.assertEqual(counts["capacity_profiles_scored"], 7)
        self.assertEqual(counts["region_capacity_records"], 56)
        self.assertEqual(counts["operator_or_channel_split_records"], 56)
        self.assertEqual(counts["exact_min_cut_records"], 56)
        self.assertEqual(counts["min_cut_invariant_regions"], 8)
        self.assertEqual(counts["min_cut_variable_regions"], 0)
        self.assertEqual(counts["branch_spanning_regions"], 3)
        self.assertEqual(counts["touched_perfect_cells"], 4)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 16)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 16)

        region_summaries = {
            record["region"]: record
            for record in certificate["fixed_witness_audit"]["region_summaries"]
        }
        self.assertEqual(region_summaries["cell0_local_compact"]["perfect_cells"], (0,))
        self.assertEqual(region_summaries["cell0_local_compact"]["min_cut_values"], (5,))
        self.assertEqual(region_summaries["cell0_local_compact"]["entropy_values"], ((3, 3),))
        self.assertEqual(region_summaries["cell3_local_compact"]["perfect_cells"], (3,))
        self.assertEqual(region_summaries["cell3_local_compact"]["min_cut_values"], (5,))
        self.assertEqual(region_summaries["adjacent_0_1_cross_cell"]["perfect_cells"], (0, 1))
        self.assertEqual(region_summaries["adjacent_0_1_cross_cell"]["min_cut_values"], (6,))
        self.assertEqual(region_summaries["adjacent_1_2_cross_cell"]["perfect_cells"], (1, 2))
        self.assertEqual(region_summaries["adjacent_1_2_cross_cell"]["min_cut_values"], (6,))
        self.assertEqual(region_summaries["branch_1_3_cross_cell"]["perfect_cells"], (1, 3))
        self.assertEqual(region_summaries["branch_1_3_cross_cell"]["min_cut_values"], (8,))
        self.assertEqual(region_summaries["branch_1_3_cross_cell"]["entropy_values"], ((4, 4),))
        self.assertEqual(region_summaries["cell3_witness_strip"]["perfect_cells"], (3,))
        self.assertEqual(region_summaries["cell3_witness_strip"]["min_cut_values"], (7,))
        self.assertEqual(region_summaries["cell3_witness_strip"]["entropy_values"], ((5, 5),))
        for summary in region_summaries.values():
            self.assertEqual(summary["records"], 7)
            self.assertEqual(summary["operator_or_channel_split_records"], 7)
            self.assertEqual(summary["exact_min_cut_records"], 7)

        first_record = certificate["fixed_witness_audit"]["records"][0]
        self.assertEqual(first_record["region"]["name"], "cell0_local_compact")
        self.assertEqual(first_record["capacity_profile"], (1, 1, 1))
        self.assertEqual(first_record["network"]["internal_assignments_per_min_cut"], 16)
        self.assertEqual(first_record["hit"]["min_cut"]["value"], 5)
        self.assertEqual(first_record["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(first_record["hit"]["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(first_record["hit"]["first"]["erasure_correctable"])
        self.assertTrue(first_record["hit"]["second"]["erasure_correctable"])
        self.assertFalse(first_record["hit"]["first"]["survivor_fixed_point_reconstructs_all"])
        self.assertTrue(first_record["hit"]["second"]["survivor_fixed_point_reconstructs_all"])
        self.assertTrue(first_record["hit"]["comparisons"]["entropy_matches"])
        self.assertTrue(first_record["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertTrue(first_record["hit"]["comparisons"]["min_cut_exact"])

    def test_holography_phase18_shell_bottleneck_certificate(self):
        certificate = bridge_holography_phase18_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_18_shell_bottleneck_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["four_cell_tree_source_rebuilt"])
        self.assertTrue(claims["outer_distance_three_witnessed"])
        self.assertTrue(claims["shell_bottleneck_records_scored"])
        self.assertTrue(claims["all_shell_mincuts_exact"])
        self.assertTrue(claims["all_shell_entropies_match"])
        self.assertTrue(claims["all_shell_operator_and_channel_semantics_match"])
        self.assertTrue(claims["all_shell_regions_capacity_sensitive_in_each_boundary_mode"])
        self.assertTrue(claims["tree_only_and_unit_ring_modes_scored"])
        self.assertTrue(claims["large_shell_regions_only"])

        source = certificate["four_cell_tree_source"]
        self.assertEqual(source["outer_code"]["parameters"], {"n": 20, "k": 1})
        self.assertEqual(
            source["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        self.assertEqual(source["code_pair"], {"n": 100, "k": 1})

        counts = certificate["counts"]
        self.assertEqual(counts["boundary_modes_scored"], 2)
        self.assertEqual(counts["shell_regions_scored"], 8)
        self.assertEqual(counts["capacity_profiles_scored"], 7)
        self.assertEqual(counts["shell_capacity_records"], 112)
        self.assertEqual(counts["exact_min_cut_records"], 112)
        self.assertEqual(counts["entropy_match_records"], 112)
        self.assertEqual(counts["operator_or_channel_split_records"], 0)
        self.assertEqual(counts["capacity_sensitive_mode_region_pairs"], 16)
        self.assertEqual(counts["mode_region_pairs"], 16)
        self.assertEqual(counts["min_shell_length"], 25)
        self.assertEqual(counts["max_shell_length"], 75)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 16)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 16)

        summaries = {
            (record["boundary_mode"], record["region"]): record
            for record in certificate["shell_bottleneck_audit"]["region_summaries"]
        }
        self.assertEqual(
            tuple(item["value"] for item in summaries[("tree_only", "cell0_shell")]["min_cut_values_by_capacity"]),
            (1, 2, 3, 1, 3, 1, 3),
        )
        self.assertEqual(summaries[("tree_only", "cell0_shell")]["min_cut_values"], (1, 2, 3))
        self.assertEqual(summaries[("tree_only", "cell0_shell")]["entropy_values"], ((1, 1),))
        self.assertEqual(
            summaries[("tree_only", "cell0_shell")]["algebra_signatures"],
            (((1, 1, 1, False), (1, 1, 1, False)),),
        )
        self.assertEqual(summaries[("tree_only", "cell0_shell")]["operator_or_channel_split_records"], 0)

        self.assertEqual(
            tuple(
                item["value"]
                for item in summaries[("tree_only", "cell1_root_shell")]["min_cut_values_by_capacity"]
            ),
            (3, 6, 9, 7, 5, 5, 7),
        )
        self.assertEqual(
            tuple(
                item["value"]
                for item in summaries[("tree_only", "root_plus_side_leaf_shell")][
                    "min_cut_values_by_capacity"
                ]
            ),
            (2, 4, 6, 4, 4, 2, 6),
        )
        self.assertEqual(
            tuple(
                item["value"]
                for item in summaries[("unit_boundary_ring", "cell0_shell")]["min_cut_values_by_capacity"]
            ),
            (3, 4, 5, 3, 5, 3, 5),
        )
        self.assertEqual(
            tuple(
                item["value"]
                for item in summaries[("unit_boundary_ring", "complement_root_shell")][
                    "min_cut_values_by_capacity"
                ]
            ),
            (5, 8, 11, 9, 7, 7, 9),
        )

        first_record = certificate["shell_bottleneck_audit"]["records"][0]
        self.assertEqual(first_record["boundary_mode"], "tree_only")
        self.assertEqual(first_record["region"]["name"], "cell0_shell")
        self.assertEqual(first_record["region"]["length"], 25)
        self.assertEqual(first_record["capacity_profile"], (1, 1, 1))
        self.assertEqual(first_record["network"]["internal_assignments_per_min_cut"], 16)
        self.assertEqual(first_record["hit"]["min_cut"]["value"], 1)
        self.assertEqual(first_record["hit"]["first"]["entropy"], 1)
        self.assertEqual(first_record["hit"]["second"]["entropy"], 1)
        self.assertEqual(first_record["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(first_record["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertFalse(first_record["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertTrue(first_record["hit"]["comparisons"]["entropy_matches"])
        self.assertTrue(first_record["hit"]["comparisons"]["min_cut_exact"])

    def test_holography_phase19_hybrid_core_shell_no_go_certificate(self):
        certificate = bridge_holography_phase19_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_19_hybrid_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["four_cell_tree_source_rebuilt"])
        self.assertTrue(claims["outer_distance_three_witnessed"])
        self.assertTrue(claims["bounded_hybrid_core_shell_menu_scored"])
        self.assertTrue(claims["all_hybrid_mincuts_exact"])
        self.assertTrue(claims["all_noncontained_hybrids_min_cut_variable"])
        self.assertTrue(claims["entropy_candidates_after_variation_exist"])
        self.assertTrue(claims["no_entropy_matched_hybrid_operator_or_channel_hits"])
        self.assertTrue(claims["both_boundary_modes_scored"])

        source = certificate["four_cell_tree_source"]
        self.assertEqual(source["outer_code"]["parameters"], {"n": 20, "k": 1})
        self.assertEqual(
            source["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        self.assertEqual(source["code_pair"], {"n": 100, "k": 1})

        counts = certificate["counts"]
        self.assertEqual(counts["boundary_modes_scored"], 2)
        self.assertEqual(counts["compact_cores_scored"], 8)
        self.assertEqual(counts["shell_regions_scored"], 8)
        self.assertEqual(counts["core_shell_pairs_per_mode"], 64)
        self.assertEqual(counts["contained_core_shell_skips"], 38)
        self.assertEqual(counts["hybrid_candidates"], 90)
        self.assertEqual(counts["min_cut_variable_candidates"], 90)
        self.assertEqual(counts["entropy_match_after_variation"], 12)
        self.assertEqual(counts["entropy_mismatch_after_variation"], 78)
        self.assertEqual(counts["operator_or_channel_hits"], 0)
        self.assertEqual(counts["exact_min_cut_candidate_records"], 90)
        self.assertEqual(counts["min_hybrid_length"], 26)
        self.assertEqual(counts["max_hybrid_length"], 78)

        mode_summaries = {
            record["boundary_mode"]: record
            for record in certificate["hybrid_search"]["mode_summaries"]
        }
        for boundary_mode in ("tree_only", "unit_boundary_ring"):
            self.assertEqual(mode_summaries[boundary_mode]["core_shell_pairs"], 64)
            self.assertEqual(mode_summaries[boundary_mode]["contained_core_shell_skips"], 19)
            self.assertEqual(mode_summaries[boundary_mode]["hybrid_candidates"], 45)
            self.assertEqual(mode_summaries[boundary_mode]["min_cut_variable_candidates"], 45)
            self.assertEqual(mode_summaries[boundary_mode]["entropy_match_after_variation"], 6)
            self.assertEqual(mode_summaries[boundary_mode]["entropy_mismatch_after_variation"], 39)
            self.assertEqual(mode_summaries[boundary_mode]["operator_or_channel_hits"], 0)

        entropy_candidates = {
            (record["boundary_mode"], record["region"]["core"], record["region"]["shell"]): record
            for record in certificate["hybrid_search"]["entropy_candidate_records"]
        }
        first_candidate = entropy_candidates[("tree_only", "adjacent_0_1_cross_cell", "cell0_shell")]
        self.assertEqual(first_candidate["region"]["length"], 26)
        self.assertEqual(
            tuple(item["value"] for item in first_candidate["min_cut_values_by_capacity"]),
            (2, 3, 4, 2, 4, 2, 4),
        )
        self.assertEqual(first_candidate["entropies"], {"first": 2, "second": 2})
        self.assertEqual(first_candidate["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(first_candidate["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertFalse(first_candidate["hit"]["comparisons"]["operator_or_channel_visible_differs"])

        branch_candidate = entropy_candidates[
            ("tree_only", "branch_1_3_cross_cell", "root_plus_leaf2_shell")
        ]
        self.assertEqual(branch_candidate["region"]["length"], 51)
        self.assertEqual(
            tuple(item["value"] for item in branch_candidate["min_cut_values_by_capacity"]),
            (3, 5, 7, 5, 5, 5, 5),
        )
        self.assertFalse(branch_candidate["hit"]["comparisons"]["operator_or_channel_visible_differs"])

        unit_ring_candidate = entropy_candidates[
            ("unit_boundary_ring", "branch_1_3_cross_cell", "root_plus_leaf2_shell")
        ]
        self.assertEqual(
            tuple(item["value"] for item in unit_ring_candidate["min_cut_values_by_capacity"]),
            (7, 9, 11, 9, 9, 9, 9),
        )
        self.assertFalse(unit_ring_candidate["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(certificate["hybrid_search"]["hit_records"], ())

    def test_holography_phase20_outer_tree_variant_no_go_certificate(self):
        certificate = bridge_holography_phase20_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_20_outer_variant_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["axis_commutation_audit_scored"])
        self.assertTrue(claims["bounded_outer_tree_variant_menu_scored"])
        self.assertTrue(claims["all_variants_outer_distance_three_witnessed"])
        self.assertTrue(claims["all_variant_code_pairs_are_n100_k1"])
        self.assertTrue(claims["all_variant_probe_mincuts_exact"])
        self.assertTrue(claims["all_variant_probes_min_cut_variable"])
        self.assertTrue(claims["all_variant_probes_entropy_match"])
        self.assertTrue(claims["no_variant_probe_operator_or_channel_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["axis_patterns_scored"], 27)
        self.assertEqual(counts["commuting_axis_patterns"], 3)
        self.assertEqual(counts["rejected_mixed_axis_patterns"], 24)
        self.assertEqual(counts["local_repair_specs_scored"], 13)
        self.assertEqual(counts["variant_records"], 39)
        self.assertEqual(counts["probe_pairs"], 6)
        self.assertEqual(counts["boundary_modes_scored"], 2)
        self.assertEqual(counts["variant_probe_records"], 468)
        self.assertEqual(counts["exact_min_cut_probe_records"], 468)
        self.assertEqual(counts["min_cut_variable_probe_records"], 468)
        self.assertEqual(counts["entropy_match_probe_records"], 468)
        self.assertEqual(counts["entropy_mismatch_probe_records"], 0)
        self.assertEqual(counts["operator_or_channel_hits"], 0)
        self.assertEqual(counts["outer_distance_three_variants"], 39)

        axis_audit = certificate["axis_commutation_audit"]
        self.assertEqual(axis_audit["valid_count"], 3)
        self.assertEqual(axis_audit["rejected_count"], 24)
        self.assertEqual(
            tuple(record["bridge_axes"] for record in axis_audit["valid_axis_patterns"]),
            (("X", "X", "X"), ("Y", "Y", "Y"), ("Z", "Z", "Z")),
        )

        axis_summaries = {
            record["bridge_axes"]: record
            for record in certificate["variant_search"]["axis_summaries"]
        }
        for axes in (("X", "X", "X"), ("Y", "Y", "Y"), ("Z", "Z", "Z")):
            self.assertEqual(axis_summaries[axes]["variants"], 13)
            self.assertEqual(axis_summaries[axes]["operator_or_channel_hits"], 0)

        first_variant = certificate["variant_search"]["variant_records"][0]
        self.assertEqual(first_variant["variant"]["name"], "XXX_identity")
        self.assertEqual(first_variant["variant"]["bridge_axes"], ("X", "X", "X"))
        self.assertEqual(first_variant["outer_code"]["parameters"], {"n": 20, "k": 1})
        self.assertEqual(
            first_variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        self.assertEqual(first_variant["code_pair"], {"n": 100, "k": 1})
        self.assertEqual(first_variant["summary"]["probe_records"], 12)
        self.assertEqual(first_variant["summary"]["min_cut_variable_probe_records"], 12)
        self.assertEqual(first_variant["summary"]["exact_min_cut_probe_records"], 12)
        self.assertEqual(first_variant["summary"]["entropy_match_probe_records"], 12)
        self.assertEqual(first_variant["summary"]["entropy_mismatch_probe_records"], 0)
        self.assertEqual(first_variant["summary"]["operator_or_channel_hits"], 0)

        first_probe = first_variant["probe_records"][0]
        self.assertEqual(first_probe["boundary_mode"], "tree_only")
        self.assertEqual(first_probe["region"]["core"], "adjacent_0_1_cross_cell")
        self.assertEqual(first_probe["region"]["shell"], "cell0_shell")
        self.assertEqual(
            tuple(item["value"] for item in first_probe["min_cut_values_by_capacity"]),
            (2, 3, 4, 2, 4, 2, 4),
        )
        self.assertTrue(first_probe["min_cut_variable"])
        self.assertTrue(first_probe["entropy_matches"])
        self.assertFalse(first_probe["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(certificate["variant_search"]["hit_records"], ())

    def test_holography_phase21_outer_tree_topology_no_go_certificate(self):
        certificate = bridge_holography_phase21_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_21_outer_tree_topology_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["all_labeled_four_cell_trees_scored"])
        self.assertTrue(claims["all_topology_outer_codes_distance_three_witnessed"])
        self.assertTrue(claims["all_topology_code_pairs_are_n100_k1"])
        self.assertTrue(claims["all_topology_probe_mincuts_exact"])
        self.assertTrue(claims["all_topology_probes_min_cut_variable"])
        self.assertTrue(claims["all_topology_probes_entropy_match"])
        self.assertTrue(claims["no_topology_probe_operator_or_channel_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["labeled_tree_topologies"], 16)
        self.assertEqual(counts["topology_records"], 16)
        self.assertEqual(counts["probe_pairs"], 6)
        self.assertEqual(counts["boundary_modes_scored"], 2)
        self.assertEqual(counts["topology_probe_records"], 192)
        self.assertEqual(counts["exact_min_cut_probe_records"], 192)
        self.assertEqual(counts["min_cut_variable_probe_records"], 192)
        self.assertEqual(counts["entropy_match_probe_records"], 192)
        self.assertEqual(counts["entropy_mismatch_probe_records"], 0)
        self.assertEqual(counts["operator_or_channel_hits"], 0)
        self.assertEqual(counts["outer_distance_three_topologies"], 16)

        topologies = certificate["topology_search"]["topology_records"]
        self.assertEqual(topologies[0]["topology"]["name"], "tree_01_02_03")
        self.assertEqual(topologies[0]["topology"]["tree_edges"], ((0, 1), (0, 2), (0, 3)))
        self.assertEqual(topologies[-1]["topology"]["name"], "tree_03_13_23")
        self.assertEqual(topologies[-1]["topology"]["tree_edges"], ((0, 3), (1, 3), (2, 3)))
        for topology in topologies:
            self.assertEqual(topology["outer_code"]["parameters"], {"n": 20, "k": 1})
            self.assertEqual(
                topology["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
                3,
            )
            self.assertEqual(topology["code_pair"], {"n": 100, "k": 1})
            self.assertEqual(topology["summary"]["probe_records"], 12)
            self.assertEqual(topology["summary"]["min_cut_variable_probe_records"], 12)
            self.assertEqual(topology["summary"]["exact_min_cut_probe_records"], 12)
            self.assertEqual(topology["summary"]["entropy_match_probe_records"], 12)
            self.assertEqual(topology["summary"]["entropy_mismatch_probe_records"], 0)
            self.assertEqual(topology["summary"]["operator_or_channel_hits"], 0)

        first_probe = topologies[0]["probe_records"][0]
        self.assertEqual(first_probe["boundary_mode"], "tree_only")
        self.assertEqual(first_probe["region"]["core"], "adjacent_0_1_cross_cell")
        self.assertEqual(first_probe["region"]["shell"], "cell0_shell")
        self.assertEqual(
            tuple(item["value"] for item in first_probe["min_cut_values_by_capacity"]),
            (4, 7, 10, 8, 6, 6, 8),
        )
        self.assertTrue(first_probe["min_cut_variable"])
        self.assertTrue(first_probe["entropy_matches"])
        self.assertFalse(first_probe["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(certificate["topology_search"]["hit_records"], ())

    def test_holography_phase22_five_cell_branching_no_go_certificate(self):
        certificate = bridge_holography_phase22_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_22_five_cell_branching_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["five_cell_outer_built"])
        self.assertTrue(claims["outer_distance_three_witnessed"])
        self.assertTrue(claims["five_cell_concatenation_k1_n125"])
        self.assertTrue(claims["all_labeled_t2_entropy_matches"])
        self.assertTrue(claims["compact_witnesses_keep_operator_or_channel_split"])
        self.assertTrue(claims["compact_witness_mincuts_invariant"])
        self.assertTrue(claims["shell_bottlenecks_are_capacity_sensitive"])
        self.assertTrue(claims["shell_bottlenecks_keep_semantics_matched"])
        self.assertTrue(claims["core_shell_family_exhausted"])
        self.assertTrue(claims["core_shell_entropy_variable_survivors_scored"])
        self.assertTrue(claims["no_core_shell_entropy_variable_operator_or_channel_hits"])
        self.assertTrue(claims["all_reported_mincuts_exact"])

        source = certificate["five_cell_source"]
        self.assertEqual(source["outer_code"]["parameters"], {"n": 25, "k": 1})
        self.assertEqual(source["outer_code"]["tree_edges"], ((0, 1), (1, 2), (1, 3), (3, 4)))
        self.assertEqual(
            source["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        self.assertEqual(source["code_pair"]["n"], 125)
        self.assertEqual(source["code_pair"]["k"], 1)
        self.assertEqual(source["low_order_entropy"]["subsets_checked"], 7876)
        self.assertEqual(source["low_order_entropy"]["mismatch_count"], 0)
        self.assertTrue(source["low_order_entropy"]["matches"])

        counts = certificate["counts"]
        self.assertEqual(counts["compact_witness_regions"], 9)
        self.assertEqual(counts["shell_regions"], 5)
        self.assertEqual(counts["capacity_profiles_scored"], 9)
        self.assertEqual(counts["compact_operator_or_channel_split_records"], 9)
        self.assertEqual(counts["compact_min_cut_variable_records"], 0)
        self.assertEqual(counts["shell_operator_or_channel_split_records"], 0)
        self.assertEqual(counts["shell_min_cut_variable_records"], 5)
        self.assertEqual(counts["core_shell_candidates_scanned"], 225)
        self.assertEqual(counts["core_shell_entropy_matches"], 99)
        self.assertEqual(counts["core_shell_min_cut_variable_candidates"], 225)
        self.assertEqual(counts["core_shell_entropy_variable_candidates"], 99)
        self.assertEqual(counts["core_shell_operator_or_channel_hits"], 0)
        self.assertEqual(counts["low_order_subsets_checked"], 7876)
        self.assertEqual(counts["low_order_entropy_mismatches"], 0)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 32)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 32)

        compact = certificate["branching_audit"]["compact_summaries"][0]
        self.assertEqual(compact["region"], "cell0_local_compact")
        self.assertEqual(compact["length"], 3)
        self.assertEqual(compact["perfect_cells"], (0,))
        self.assertEqual(compact["min_cut_values"], (3,))
        self.assertEqual(compact["entropy_pair"], (3, 3))
        self.assertEqual(compact["algebra_pair"], ((1, 1, 1, False), (0, 0, 2, False)))
        self.assertTrue(compact["operator_or_channel_split"])

        shell = certificate["branching_audit"]["shell_summaries"][0]
        self.assertEqual(shell["region"], "cell0_shell")
        self.assertEqual(shell["length"], 25)
        self.assertEqual(shell["min_cut_values"], (1, 2, 3))
        self.assertEqual(shell["entropy_pair"], (1, 1))
        self.assertEqual(shell["algebra_pair"], ((1, 1, 1, False), (1, 1, 1, False)))
        self.assertFalse(shell["operator_or_channel_split"])

        survivors = certificate["branching_audit"]["core_shell_search"]["entropy_variable_candidate_records"]
        self.assertEqual(len(survivors), 99)
        first_survivor = survivors[0]
        self.assertEqual(first_survivor["core"], "cell0_local_compact")
        self.assertEqual(first_survivor["shell_cells"], (0,))
        self.assertEqual(first_survivor["length"], 25)
        self.assertEqual(
            tuple(record["value"] for record in first_survivor["min_cut_values_by_capacity"]),
            (1, 2, 3, 1, 3, 1, 1, 3, 1),
        )
        self.assertFalse(first_survivor["hit"]["comparisons"]["operator_or_channel_visible_differs"])

        last_survivor = survivors[-1]
        self.assertEqual(last_survivor["core"], "edge_3_4_cross_cell")
        self.assertEqual(last_survivor["shell_cells"], (2, 3, 4))
        self.assertEqual(last_survivor["length"], 75)
        self.assertEqual(
            tuple(record["value"] for record in last_survivor["min_cut_values_by_capacity"]),
            (2, 4, 6, 6, 2, 4, 2, 4, 4),
        )
        self.assertFalse(last_survivor["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(certificate["branching_audit"]["core_shell_search"]["hit_records"], ())

    def test_holography_phase23_interface_star_no_go_certificate(self):
        certificate = bridge_holography_phase23_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_23_interface_star_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["interface_outer_built"])
        self.assertTrue(claims["outer_distance_three_witnessed"])
        self.assertTrue(claims["interface_concatenation_k1_n150"])
        self.assertTrue(claims["all_labeled_t2_entropy_matches"])
        self.assertTrue(claims["compact_witnesses_keep_operator_or_channel_split"])
        self.assertTrue(claims["compact_witness_mincuts_invariant"])
        self.assertTrue(claims["interface_regions_are_capacity_sensitive"])
        self.assertTrue(claims["interface_regions_keep_semantics_matched"])
        self.assertTrue(claims["root_shell_edge_probes_scored"])
        self.assertTrue(claims["root_leaf_shell_probes_scored"])
        self.assertTrue(claims["all_reported_mincuts_exact"])

        source = certificate["interface_star_source"]
        self.assertEqual(source["outer_code"]["parameters"], {"n": 30, "k": 1})
        self.assertEqual(source["outer_code"]["interface_cell"], 5)
        self.assertEqual(source["outer_code"]["leaf_cells"], (0, 1, 2, 3, 4))
        self.assertEqual(source["outer_code"]["tree_edges"], ((5, 0), (5, 1), (5, 2), (5, 3), (5, 4)))
        self.assertEqual(
            source["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        self.assertEqual(source["code_pair"]["n"], 150)
        self.assertEqual(source["code_pair"]["k"], 1)
        self.assertEqual(source["low_order_entropy"]["subsets_checked"], 11326)
        self.assertEqual(source["low_order_entropy"]["mismatch_count"], 0)
        self.assertTrue(source["low_order_entropy"]["matches"])

        counts = certificate["counts"]
        self.assertEqual(counts["compact_regions"], 11)
        self.assertEqual(counts["interface_regions"], 10)
        self.assertEqual(counts["root_shell_plus_edge_regions"], 5)
        self.assertEqual(counts["root_leaf_shell_regions"], 5)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["compact_operator_or_channel_split_records"], 11)
        self.assertEqual(counts["compact_min_cut_variable_records"], 0)
        self.assertEqual(counts["interface_operator_or_channel_split_records"], 0)
        self.assertEqual(counts["interface_min_cut_variable_records"], 10)
        self.assertEqual(counts["low_order_subsets_checked"], 11326)
        self.assertEqual(counts["low_order_entropy_mismatches"], 0)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        compact = certificate["interface_audit"]["compact_summaries"][0]
        self.assertEqual(compact["region"], "cell0_local_compact")
        self.assertEqual(compact["length"], 3)
        self.assertEqual(compact["perfect_cells"], (0,))
        self.assertEqual(compact["min_cut_values"], (3,))
        self.assertEqual(compact["entropy_pair"], (3, 3))
        self.assertEqual(compact["algebra_pair"], ((1, 1, 1, False), (0, 0, 2, False)))
        self.assertTrue(compact["operator_or_channel_split"])

        root_edge = certificate["interface_audit"]["interface_summaries"][0]
        self.assertEqual(root_edge["region"], "root_shell_plus_edge_0")
        self.assertEqual(root_edge["region_type"], "phase23_root_shell_plus_interface_edge")
        self.assertEqual(root_edge["length"], 26)
        self.assertEqual(root_edge["perfect_cells"], (5, 0))
        self.assertEqual(root_edge["min_cut_values"], (6, 8, 10, 11, 14, 16))
        self.assertEqual(root_edge["entropy_pair"], (2, 2))
        self.assertEqual(root_edge["algebra_pair"], ((1, 1, 1, False), (1, 1, 1, False)))
        self.assertFalse(root_edge["operator_or_channel_split"])

        root_leaf = certificate["interface_audit"]["interface_summaries"][1]
        self.assertEqual(root_leaf["region"], "root_leaf_0_shells")
        self.assertEqual(root_leaf["region_type"], "phase23_root_leaf_shell_pair")
        self.assertEqual(root_leaf["length"], 50)
        self.assertEqual(root_leaf["perfect_cells"], (5, 0))
        self.assertEqual(root_leaf["min_cut_values"], (4, 6, 8, 12))
        self.assertEqual(root_leaf["entropy_pair"], (1, 1))
        self.assertEqual(root_leaf["algebra_pair"], ((1, 1, 1, False), (1, 1, 1, False)))
        self.assertFalse(root_leaf["operator_or_channel_split"])

    def test_holography_phase24_punctured_interface_shell_no_go_certificate(self):
        certificate = bridge_holography_phase24_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_24_punctured_interface_shell_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["interface_outer_reused"])
        self.assertTrue(claims["outer_distance_three_witnessed"])
        self.assertTrue(claims["interface_concatenation_k1_n150"])
        self.assertTrue(claims["all_labeled_t2_entropy_matches"])
        self.assertTrue(claims["punctured_frontier_exhausted"])
        self.assertTrue(claims["all_punctured_regions_entropy_match"])
        self.assertTrue(claims["all_punctured_regions_min_cut_variable"])
        self.assertTrue(claims["no_punctured_operator_or_channel_hits"])
        self.assertTrue(claims["all_punctured_mincuts_exact"])
        self.assertTrue(claims["all_holes_scored_for_all_leaves"])

        source = certificate["interface_star_source"]
        self.assertEqual(source["outer_code"]["parameters"], {"n": 30, "k": 1})
        self.assertEqual(source["outer_code"]["tree_edges"], ((5, 0), (5, 1), (5, 2), (5, 3), (5, 4)))
        self.assertEqual(
            source["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        self.assertEqual(source["code_pair"]["n"], 150)
        self.assertEqual(source["code_pair"]["k"], 1)
        self.assertEqual(source["low_order_entropy"]["subsets_checked"], 11326)
        self.assertEqual(source["low_order_entropy"]["mismatch_count"], 0)
        self.assertTrue(source["low_order_entropy"]["matches"])

        counts = certificate["counts"]
        self.assertEqual(counts["root_witness_holes"], 5)
        self.assertEqual(counts["leaf_cells_scored"], 5)
        self.assertEqual(counts["punctured_records"], 25)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 25)
        self.assertEqual(counts["min_cut_variable_records"], 25)
        self.assertEqual(counts["operator_or_channel_hits"], 0)
        self.assertEqual(counts["low_order_subsets_checked"], 11326)
        self.assertEqual(counts["low_order_entropy_mismatches"], 0)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        self.assertEqual(
            certificate["punctured_frontier"]["root_witness_holes"],
            (129, 134, 139, 144, 149),
        )
        first_hole = certificate["punctured_frontier"]["hole_summaries"][0]
        self.assertEqual(first_hole["removed_root_qubit"], 129)
        self.assertEqual(first_hole["removed_root_offset"], 4)
        self.assertEqual(first_hole["records"], 5)
        self.assertEqual(first_hole["entropy_match_records"], 5)
        self.assertEqual(first_hole["min_cut_variable_records"], 5)
        self.assertEqual(first_hole["operator_or_channel_hits"], 0)

        records = certificate["punctured_frontier"]["records"]
        self.assertEqual(len(records), 25)
        first = records[0]
        self.assertEqual(first["leaf_cell"], 0)
        self.assertEqual(first["removed_root_qubit"], 129)
        self.assertEqual(first["removed_root_offset"], 4)
        self.assertEqual(first["region"]["length"], 25)
        self.assertEqual(first["hit"]["first"]["entropy"], 3)
        self.assertEqual(first["hit"]["second"]["entropy"], 3)
        self.assertEqual(first["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(first["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(
            tuple(record["value"] for record in first["min_cut_values_by_capacity"]),
            (7, 12, 17, 15, 9, 9, 9, 9, 11, 11),
        )
        self.assertFalse(first["hit"]["comparisons"]["operator_or_channel_visible_differs"])

        last = records[-1]
        self.assertEqual(last["leaf_cell"], 4)
        self.assertEqual(last["removed_root_qubit"], 149)
        self.assertEqual(last["removed_root_offset"], 24)
        self.assertEqual(last["region"]["length"], 25)
        self.assertEqual(
            tuple(record["value"] for record in last["min_cut_values_by_capacity"]),
            (7, 12, 17, 15, 9, 9, 9, 9, 11, 11),
        )
        self.assertFalse(last["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(certificate["punctured_frontier"]["hit_records"], ())

    def test_holography_phase25_two_layer_clifford_frontier_certificate(self):
        certificate = bridge_holography_phase25_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_25_two_layer_clifford_menu_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["interface_outer_loaded"])
        self.assertTrue(claims["two_layer_circuit_menu_scored"])
        self.assertTrue(claims["all_variant_code_pairs_are_n150_k1"])
        self.assertTrue(claims["punctured_frontier_replayed_for_each_variant"])
        self.assertTrue(claims["all_variant_punctured_mincuts_exact"])
        self.assertTrue(claims["all_variant_punctures_min_cut_variable"])
        self.assertTrue(claims["no_admissible_entropy_matched_operator_hits"])
        self.assertTrue(claims["entropy_mismatched_operator_near_hits_exist"])
        self.assertTrue(claims["distance_three_or_better_bounded"])

        counts = certificate["counts"]
        self.assertEqual(counts["two_layer_variants"], 4)
        self.assertEqual(counts["punctured_regions_per_variant"], 25)
        self.assertEqual(counts["variant_punctured_records"], 100)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 20)
        self.assertEqual(counts["entropy_mismatch_records"], 80)
        self.assertEqual(counts["min_cut_variable_records"], 100)
        self.assertEqual(counts["operator_or_channel_split_records"], 30)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["entropy_mismatch_operator_near_hits"], 30)
        self.assertEqual(counts["distance_three_witness_variants"], 2)
        self.assertEqual(counts["distance_lower_bound_four_variants"], 2)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        variants = certificate["two_layer_menu"]["variant_records"]
        self.assertEqual(tuple(variant["variant"]["name"] for variant in variants), (
            "root_to_leaf_same_position",
            "leaf_to_root_same_position",
            "alternating_disentangler_isometry",
            "sparse_offset_ladder",
        ))

        root_to_leaf = variants[0]
        self.assertEqual(root_to_leaf["variant"]["gate_count"], 25)
        self.assertEqual(root_to_leaf["outer_code"]["parameters"], {"n": 30, "k": 1})
        self.assertEqual(root_to_leaf["code_pair"], {"n": 150, "k": 1})
        self.assertEqual(root_to_leaf["summary"]["entropy_match_records"], 0)
        self.assertEqual(root_to_leaf["summary"]["operator_or_channel_split_records"], 0)
        self.assertEqual(
            root_to_leaf["outer_code"]["distance_audit_weight3"]["distance_lower_bound"],
            4,
        )
        self.assertIsNone(
            root_to_leaf["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"]
        )

        leaf_to_root = variants[1]
        self.assertEqual(leaf_to_root["summary"]["entropy_match_records"], 0)
        self.assertEqual(leaf_to_root["summary"]["operator_or_channel_split_records"], 25)
        self.assertEqual(leaf_to_root["summary"]["entropy_mismatch_operator_near_hits"], 25)
        first_near = leaf_to_root["near_hit_records"][0]
        self.assertEqual(first_near["leaf_cell"], 0)
        self.assertEqual(first_near["removed_root_qubit"], 129)
        self.assertEqual(first_near["hit"]["first"]["entropy"], 5)
        self.assertEqual(first_near["hit"]["second"]["entropy"], 6)
        self.assertEqual(first_near["hit"]["first"]["algebra_signature"], (0, 0, 2, False))
        self.assertEqual(first_near["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertTrue(first_near["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(
            tuple(record["value"] for record in first_near["min_cut_values_by_capacity"]),
            (7, 12, 17, 15, 9, 9, 9, 9, 11, 11),
        )

        alternating = variants[2]
        self.assertEqual(alternating["summary"]["entropy_match_records"], 20)
        self.assertEqual(alternating["summary"]["operator_or_channel_split_records"], 5)
        self.assertEqual(alternating["summary"]["entropy_mismatch_operator_near_hits"], 5)
        self.assertEqual(
            alternating["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )
        first_record = alternating["records"][0]
        self.assertEqual(first_record["hit"]["first"]["entropy"], 4)
        self.assertEqual(first_record["hit"]["second"]["entropy"], 4)
        self.assertFalse(first_record["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        alternating_near = alternating["near_hit_records"][0]
        self.assertEqual(alternating_near["removed_root_qubit"], 139)
        self.assertEqual(alternating_near["hit"]["first"]["entropy"], 4)
        self.assertEqual(alternating_near["hit"]["second"]["entropy"], 5)

        ladder = variants[3]
        self.assertEqual(ladder["variant"]["gate_count"], 10)
        self.assertEqual(ladder["summary"]["entropy_match_records"], 0)
        self.assertEqual(ladder["summary"]["operator_or_channel_split_records"], 0)
        self.assertEqual(
            ladder["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"],
            3,
        )

        self.assertEqual(certificate["two_layer_menu"]["admissible_hit_records"], ())
        self.assertEqual(len(certificate["two_layer_menu"]["near_hit_records"]), 30)

    def test_holography_phase26_offset_flip_entropy_gated_no_go_certificate(self):
        certificate = bridge_holography_phase26_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_26_offset_flip_entropy_gated_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["interface_outer_loaded"])
        self.assertTrue(claims["offset_flip_neighborhood_scored"])
        self.assertTrue(claims["all_neighbor_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_neighbor_outer_distance_three_witnessed"])
        self.assertTrue(claims["punctured_frontier_replayed_for_each_neighbor"])
        self.assertTrue(claims["all_neighbor_punctured_mincuts_exact"])
        self.assertTrue(claims["all_neighbor_punctures_min_cut_variable"])
        self.assertTrue(claims["all_entropy_matched_records_operator_checked"])
        self.assertTrue(claims["no_entropy_matched_operator_hits_in_neighborhood"])
        self.assertTrue(claims["entropy_mismatch_near_hits_audited_if_requested"])

        counts = certificate["counts"]
        self.assertEqual(counts["offset_flip_variants"], 10)
        self.assertEqual(counts["parent_circuits"], 2)
        self.assertEqual(counts["punctured_regions_per_variant"], 25)
        self.assertEqual(counts["candidate_records"], 250)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 90)
        self.assertEqual(counts["entropy_mismatch_records"], 160)
        self.assertEqual(counts["operator_channel_checked_records"], 90)
        self.assertEqual(counts["entropy_gate_rejections"], 160)
        self.assertEqual(counts["min_cut_variable_records"], 250)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertIsNone(counts["entropy_mismatch_operator_near_hits"])
        self.assertEqual(counts["distance_three_witness_variants"], 10)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        variants = certificate["neighborhood"]["variant_records"]
        self.assertEqual(len(variants), 10)
        self.assertEqual(tuple(variant["variant"]["name"] for variant in variants[:5]), (
            "leaf_to_root_same_position__flip_offset_0_to_root_to_leaf",
            "leaf_to_root_same_position__flip_offset_1_to_root_to_leaf",
            "leaf_to_root_same_position__flip_offset_2_to_root_to_leaf",
            "leaf_to_root_same_position__flip_offset_3_to_root_to_leaf",
            "leaf_to_root_same_position__flip_offset_4_to_root_to_leaf",
        ))
        self.assertEqual(tuple(variant["variant"]["name"] for variant in variants[5:]), (
            "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root",
            "alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf",
            "alternating_disentangler_isometry__flip_offset_2_to_leaf_to_root",
            "alternating_disentangler_isometry__flip_offset_3_to_root_to_leaf",
            "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root",
        ))
        self.assertTrue(
            all(
                variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3
                for variant in variants
            )
        )

        first_leaf_flip = variants[0]
        self.assertEqual(first_leaf_flip["variant"]["parent"], "leaf_to_root_same_position")
        self.assertEqual(first_leaf_flip["variant"]["flipped_offset"], 0)
        self.assertEqual(first_leaf_flip["variant"]["to_direction"], "root_to_leaf")
        self.assertEqual(first_leaf_flip["summary"]["entropy_match_records"], 10)
        self.assertEqual(first_leaf_flip["summary"]["operator_channel_checked_records"], 10)
        self.assertEqual(first_leaf_flip["summary"]["entropy_gate_rejections"], 15)
        self.assertEqual(first_leaf_flip["summary"]["operator_or_channel_split_records"], 0)
        self.assertEqual(first_leaf_flip["summary"]["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertIsNone(first_leaf_flip["summary"]["entropy_mismatch_operator_near_hits"])

        alternating_offset_zero = variants[5]
        self.assertEqual(alternating_offset_zero["variant"]["parent"], "alternating_disentangler_isometry")
        self.assertEqual(alternating_offset_zero["variant"]["flipped_offset"], 0)
        self.assertEqual(alternating_offset_zero["summary"]["entropy_match_records"], 15)
        self.assertEqual(alternating_offset_zero["summary"]["operator_channel_checked_records"], 15)
        self.assertEqual(alternating_offset_zero["summary"]["operator_or_channel_split_records"], 0)

        alternating_offset_one = variants[6]
        self.assertEqual(alternating_offset_one["variant"]["flipped_offset"], 1)
        self.assertEqual(alternating_offset_one["summary"]["entropy_match_records"], 0)
        self.assertEqual(alternating_offset_one["summary"]["operator_channel_checked_records"], 0)
        self.assertEqual(alternating_offset_one["summary"]["entropy_gate_rejections"], 25)
        self.assertIsNone(alternating_offset_one["records"][0]["hit"])
        self.assertEqual(
            alternating_offset_one["records"][0]["strict_filter_stage"],
            "entropy_gate_rejected_before_operator_channel_check",
        )

        parent_summaries = {summary["parent"]: summary for summary in certificate["neighborhood"]["parent_summaries"]}
        leaf_summary = parent_summaries["leaf_to_root_same_position"]
        self.assertEqual(leaf_summary["variants"], 5)
        self.assertEqual(leaf_summary["punctured_records"], 125)
        self.assertEqual(leaf_summary["entropy_match_records"], 50)
        self.assertEqual(leaf_summary["operator_channel_checked_records"], 50)
        self.assertEqual(leaf_summary["operator_or_channel_split_records"], 0)
        self.assertEqual(leaf_summary["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertIsNone(leaf_summary["entropy_mismatch_operator_near_hits"])

        alternating_summary = parent_summaries["alternating_disentangler_isometry"]
        self.assertEqual(alternating_summary["variants"], 5)
        self.assertEqual(alternating_summary["punctured_records"], 125)
        self.assertEqual(alternating_summary["entropy_match_records"], 40)
        self.assertEqual(alternating_summary["operator_channel_checked_records"], 40)
        self.assertEqual(alternating_summary["operator_or_channel_split_records"], 0)
        self.assertEqual(alternating_summary["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertIsNone(alternating_summary["entropy_mismatch_operator_near_hits"])

        self.assertEqual(certificate["neighborhood"]["admissible_hit_records"], ())
        self.assertIsNone(certificate["neighborhood"]["entropy_mismatch_near_hit_records"])

    def test_holography_phase27_second_root_hole_region_grammar_no_go_certificate(self):
        certificate = bridge_holography_phase27_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_27_second_root_hole_region_grammar_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["interface_outer_loaded"])
        self.assertTrue(claims["offset_flip_neighborhood_reused"])
        self.assertTrue(claims["all_neighbor_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_neighbor_outer_distance_three_witnessed"])
        self.assertTrue(claims["second_root_hole_grammar_exhausted_around_entropy_passes"])
        self.assertTrue(claims["all_second_hole_mincuts_exact"])
        self.assertTrue(claims["all_second_hole_records_min_cut_variable"])
        self.assertTrue(claims["all_second_hole_entropy_matches_operator_checked"])
        self.assertTrue(claims["no_second_hole_admissible_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["offset_flip_variants"], 10)
        self.assertEqual(counts["parent_circuits"], 2)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["base_entropy_pass_records"], 90)
        self.assertEqual(counts["candidate_second_hole_records"], 360)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 60)
        self.assertEqual(counts["entropy_mismatch_records"], 300)
        self.assertEqual(counts["operator_channel_checked_records"], 60)
        self.assertEqual(counts["second_hole_entropy_gate_rejections"], 300)
        self.assertEqual(counts["min_cut_variable_records"], 360)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_variants"], 10)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        variants = certificate["second_hole_frontier"]["variant_records"]
        self.assertEqual(len(variants), 10)
        leaf_first = variants[0]
        self.assertEqual(leaf_first["variant"]["name"], "leaf_to_root_same_position__flip_offset_0_to_root_to_leaf")
        self.assertEqual(leaf_first["summary"]["base_entropy_pass_records"], 10)
        self.assertEqual(leaf_first["summary"]["candidate_second_hole_records"], 40)
        self.assertEqual(leaf_first["summary"]["entropy_match_records"], 0)
        self.assertEqual(leaf_first["summary"]["entropy_mismatch_records"], 40)
        self.assertEqual(leaf_first["summary"]["operator_channel_checked_records"], 0)
        self.assertEqual(leaf_first["summary"]["min_cut_variable_records"], 40)
        self.assertEqual(leaf_first["summary"]["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(leaf_first["records"][0]["strict_filter_stage"], "second_hole_entropy_gate_rejected")

        alternating_zero = variants[5]
        self.assertEqual(
            alternating_zero["variant"]["name"],
            "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root",
        )
        self.assertEqual(alternating_zero["summary"]["base_entropy_pass_records"], 15)
        self.assertEqual(alternating_zero["summary"]["candidate_second_hole_records"], 60)
        self.assertEqual(alternating_zero["summary"]["entropy_match_records"], 30)
        self.assertEqual(alternating_zero["summary"]["entropy_mismatch_records"], 30)
        self.assertEqual(alternating_zero["summary"]["operator_channel_checked_records"], 30)
        self.assertEqual(alternating_zero["summary"]["operator_or_channel_split_records"], 0)
        self.assertEqual(alternating_zero["summary"]["admissible_entropy_match_min_cut_operator_hits"], 0)

        alternating_one = variants[6]
        self.assertEqual(alternating_one["summary"]["base_entropy_pass_records"], 0)
        self.assertEqual(alternating_one["summary"]["candidate_second_hole_records"], 0)

        alternating_two = variants[7]
        self.assertEqual(alternating_two["summary"]["base_entropy_pass_records"], 10)
        self.assertEqual(alternating_two["summary"]["candidate_second_hole_records"], 40)
        self.assertEqual(alternating_two["summary"]["entropy_match_records"], 0)

        alternating_four = variants[9]
        self.assertEqual(alternating_four["summary"]["base_entropy_pass_records"], 15)
        self.assertEqual(alternating_four["summary"]["candidate_second_hole_records"], 60)
        self.assertEqual(alternating_four["summary"]["entropy_match_records"], 30)
        self.assertEqual(alternating_four["summary"]["operator_channel_checked_records"], 30)

        parent_summaries = {
            summary["parent"]: summary for summary in certificate["second_hole_frontier"]["parent_summaries"]
        }
        leaf_summary = parent_summaries["leaf_to_root_same_position"]
        self.assertEqual(leaf_summary["variants"], 5)
        self.assertEqual(leaf_summary["base_entropy_pass_records"], 50)
        self.assertEqual(leaf_summary["candidate_second_hole_records"], 200)
        self.assertEqual(leaf_summary["entropy_match_records"], 0)
        self.assertEqual(leaf_summary["operator_channel_checked_records"], 0)
        self.assertEqual(leaf_summary["admissible_entropy_match_min_cut_operator_hits"], 0)

        alternating_summary = parent_summaries["alternating_disentangler_isometry"]
        self.assertEqual(alternating_summary["variants"], 5)
        self.assertEqual(alternating_summary["base_entropy_pass_records"], 40)
        self.assertEqual(alternating_summary["candidate_second_hole_records"], 160)
        self.assertEqual(alternating_summary["entropy_match_records"], 60)
        self.assertEqual(alternating_summary["operator_channel_checked_records"], 60)
        self.assertEqual(alternating_summary["operator_or_channel_split_records"], 0)
        self.assertEqual(alternating_summary["admissible_entropy_match_min_cut_operator_hits"], 0)

        selected = certificate["second_hole_frontier"]["selected_entropy_matched_record"]
        self.assertEqual(selected["region"]["name"], "root_shell_plus_edge_0_minus_q129__second_root_hole_q134")
        self.assertEqual(selected["entropy_pair"], (4, 4))
        self.assertEqual(selected["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertFalse(selected["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(selected["min_cut_values"], (8, 10, 12, 13, 16, 18))

        self.assertEqual(certificate["second_hole_frontier"]["admissible_hit_records"], ())

    def test_holography_phase28_leaf_private_sentinel_no_go_certificate(self):
        certificate = bridge_holography_phase28_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_28_leaf_private_sentinel_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["interface_outer_loaded"])
        self.assertTrue(claims["leaf_private_sentinel_variants_scored"])
        self.assertTrue(claims["all_sentinel_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_sentinel_outer_distance_three_witnessed"])
        self.assertTrue(claims["leaf_private_grammar_exhausted_for_sentinel_entropy_passes"])
        self.assertTrue(claims["all_leaf_private_mincuts_exact"])
        self.assertTrue(claims["all_leaf_private_records_entropy_match"])
        self.assertTrue(claims["all_leaf_private_records_min_cut_variable"])
        self.assertTrue(claims["all_leaf_private_records_operator_checked"])
        self.assertTrue(claims["no_leaf_private_sentinel_admissible_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["sentinel_variants"], 2)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["base_entropy_pass_records"], 30)
        self.assertEqual(counts["candidate_leaf_private_records"], 120)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 120)
        self.assertEqual(counts["entropy_mismatch_records"], 0)
        self.assertEqual(counts["operator_channel_checked_records"], 120)
        self.assertEqual(counts["leaf_private_entropy_gate_rejections"], 0)
        self.assertEqual(counts["min_cut_variable_records"], 120)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_variants"], 2)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        variants = certificate["leaf_private_frontier"]["variant_records"]
        self.assertEqual(len(variants), 2)
        self.assertEqual(
            tuple(variant["variant"]["name"] for variant in variants),
            (
                "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root",
                "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root",
            ),
        )
        for variant in variants:
            summary = variant["summary"]
            self.assertEqual(summary["base_entropy_pass_records"], 15)
            self.assertEqual(summary["candidate_leaf_private_records"], 60)
            self.assertEqual(summary["entropy_match_records"], 60)
            self.assertEqual(summary["entropy_mismatch_records"], 0)
            self.assertEqual(summary["operator_channel_checked_records"], 60)
            self.assertEqual(summary["leaf_private_entropy_gate_rejections"], 0)
            self.assertEqual(summary["min_cut_variable_records"], 60)
            self.assertEqual(summary["operator_or_channel_split_records"], 0)
            self.assertEqual(summary["admissible_entropy_match_min_cut_operator_hits"], 0)

        selected = certificate["leaf_private_frontier"]["selected_entropy_matched_record"]
        self.assertEqual(selected["region"]["name"], "root_shell_plus_edge_0_minus_q129__add_leaf_private_q0")
        self.assertEqual(selected["entropy_pair"], (5, 5))
        self.assertEqual(selected["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertFalse(selected["hit"]["first"]["erasure_correctable"])
        self.assertFalse(selected["hit"]["second"]["erasure_correctable"])
        self.assertFalse(selected["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(selected["min_cut_values"], (8, 10, 12, 13, 16, 18))

        self.assertEqual(certificate["leaf_private_frontier"]["admissible_hit_records"], ())

    def test_holography_phase29_full_leaf_private_region_grammar_no_go_certificate(self):
        certificate = bridge_holography_phase29_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_29_full_leaf_private_region_grammar_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["interface_outer_loaded"])
        self.assertTrue(claims["offset_flip_neighborhood_reused"])
        self.assertTrue(claims["all_neighbor_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_neighbor_outer_distance_three_witnessed"])
        self.assertTrue(claims["full_leaf_private_grammar_exhausted_around_entropy_passes"])
        self.assertTrue(claims["all_full_leaf_private_mincuts_exact"])
        self.assertTrue(claims["all_full_leaf_private_records_entropy_match"])
        self.assertTrue(claims["all_full_leaf_private_records_min_cut_variable"])
        self.assertTrue(claims["all_full_leaf_private_records_operator_checked"])
        self.assertTrue(claims["no_full_leaf_private_admissible_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["offset_flip_variants"], 10)
        self.assertEqual(counts["parent_circuits"], 2)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["base_entropy_pass_records"], 90)
        self.assertEqual(counts["candidate_leaf_private_records"], 360)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 360)
        self.assertEqual(counts["entropy_mismatch_records"], 0)
        self.assertEqual(counts["operator_channel_checked_records"], 360)
        self.assertEqual(counts["leaf_private_entropy_gate_rejections"], 0)
        self.assertEqual(counts["min_cut_variable_records"], 360)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_variants"], 10)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        variants = certificate["full_leaf_private_frontier"]["variant_records"]
        self.assertEqual(len(variants), 10)
        variant_by_name = {variant["variant"]["name"]: variant for variant in variants}
        leaf_summary = variant_by_name[
            "leaf_to_root_same_position__flip_offset_0_to_root_to_leaf"
        ]["summary"]
        self.assertEqual(leaf_summary["base_entropy_pass_records"], 10)
        self.assertEqual(leaf_summary["candidate_leaf_private_records"], 40)
        self.assertEqual(leaf_summary["entropy_match_records"], 40)
        self.assertEqual(leaf_summary["operator_channel_checked_records"], 40)
        self.assertEqual(leaf_summary["operator_or_channel_split_records"], 0)

        alternating_zero_summary = variant_by_name[
            "alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf"
        ]["summary"]
        self.assertEqual(alternating_zero_summary["base_entropy_pass_records"], 0)
        self.assertEqual(alternating_zero_summary["candidate_leaf_private_records"], 0)
        self.assertEqual(alternating_zero_summary["entropy_match_records"], 0)
        self.assertEqual(alternating_zero_summary["operator_channel_checked_records"], 0)

        alternating_rich_summary = variant_by_name[
            "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root"
        ]["summary"]
        self.assertEqual(alternating_rich_summary["base_entropy_pass_records"], 15)
        self.assertEqual(alternating_rich_summary["candidate_leaf_private_records"], 60)
        self.assertEqual(alternating_rich_summary["entropy_match_records"], 60)
        self.assertEqual(alternating_rich_summary["operator_channel_checked_records"], 60)
        self.assertEqual(alternating_rich_summary["operator_or_channel_split_records"], 0)

        parent_summaries = {
            summary["parent"]: summary for summary in certificate["full_leaf_private_frontier"]["parent_summaries"]
        }
        leaf_parent = parent_summaries["leaf_to_root_same_position"]
        self.assertEqual(leaf_parent["variants"], 5)
        self.assertEqual(leaf_parent["base_entropy_pass_records"], 50)
        self.assertEqual(leaf_parent["candidate_leaf_private_records"], 200)
        self.assertEqual(leaf_parent["entropy_match_records"], 200)
        self.assertEqual(leaf_parent["operator_channel_checked_records"], 200)
        self.assertEqual(leaf_parent["operator_or_channel_split_records"], 0)
        self.assertEqual(leaf_parent["admissible_entropy_match_min_cut_operator_hits"], 0)

        alternating_parent = parent_summaries["alternating_disentangler_isometry"]
        self.assertEqual(alternating_parent["variants"], 5)
        self.assertEqual(alternating_parent["base_entropy_pass_records"], 40)
        self.assertEqual(alternating_parent["candidate_leaf_private_records"], 160)
        self.assertEqual(alternating_parent["entropy_match_records"], 160)
        self.assertEqual(alternating_parent["operator_channel_checked_records"], 160)
        self.assertEqual(alternating_parent["operator_or_channel_split_records"], 0)
        self.assertEqual(alternating_parent["admissible_entropy_match_min_cut_operator_hits"], 0)

        selected = certificate["full_leaf_private_frontier"]["selected_entropy_matched_record"]
        self.assertEqual(selected["region"]["name"], "root_shell_plus_edge_0_minus_q134__add_leaf_private_q0")
        self.assertEqual(selected["entropy_pair"], (6, 6))
        self.assertEqual(selected["hit"]["first"]["algebra_signature"], (0, 0, 2, False))
        self.assertEqual(selected["hit"]["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(selected["min_cut_values"], (8, 10, 12, 13, 16, 18))

        self.assertEqual(certificate["full_leaf_private_frontier"]["admissible_hit_records"], ())

    def test_holography_phase30_bridge_axis_source_pairing_no_go_certificate(self):
        certificate = bridge_holography_phase30_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_30_bridge_axis_source_pairing_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["single_source_pairing_loaded"])
        self.assertTrue(claims["all_bridge_axes_scored"])
        self.assertTrue(claims["all_axis_outer_codes_are_n30_k1"])
        self.assertTrue(claims["all_axis_neighbor_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_axis_neighbor_outer_distance_three_witnessed"])
        self.assertTrue(claims["axis_offset_flip_neighborhood_exhausted"])
        self.assertTrue(claims["bridge_axis_changes_entropy_gate_profile"])
        self.assertTrue(claims["all_axis_punctured_mincuts_exact"])
        self.assertTrue(claims["all_axis_punctured_records_min_cut_variable"])
        self.assertTrue(claims["all_axis_entropy_matches_operator_checked"])
        self.assertTrue(claims["no_bridge_axis_admissible_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["bridge_axes"], 3)
        self.assertEqual(counts["source_pairings"], 1)
        self.assertEqual(counts["offset_flip_variants_per_axis"], 10)
        self.assertEqual(counts["axis_variant_records"], 30)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["candidate_punctured_records"], 750)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 165)
        self.assertEqual(counts["entropy_mismatch_records"], 585)
        self.assertEqual(counts["operator_channel_checked_records"], 165)
        self.assertEqual(counts["entropy_gate_rejections"], 585)
        self.assertEqual(counts["min_cut_variable_records"], 750)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_axis_variants"], 30)
        self.assertEqual(counts["axis_entropy_match_profile"], {"X": 30, "Y": 90, "Z": 45})
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        axis_records = certificate["axis_source_pairing_frontier"]["axis_records"]
        self.assertEqual(tuple(record["bridge_axis"] for record in axis_records), ("X", "Y", "Z"))
        summary_by_axis = {record["bridge_axis"]: record["summary"] for record in axis_records}
        self.assertEqual(summary_by_axis["X"]["entropy_match_records"], 30)
        self.assertEqual(summary_by_axis["X"]["entropy_mismatch_records"], 220)
        self.assertEqual(summary_by_axis["X"]["operator_channel_checked_records"], 30)
        self.assertEqual(summary_by_axis["Y"]["entropy_match_records"], 90)
        self.assertEqual(summary_by_axis["Y"]["entropy_mismatch_records"], 160)
        self.assertEqual(summary_by_axis["Y"]["operator_channel_checked_records"], 90)
        self.assertEqual(summary_by_axis["Z"]["entropy_match_records"], 45)
        self.assertEqual(summary_by_axis["Z"]["entropy_mismatch_records"], 205)
        self.assertEqual(summary_by_axis["Z"]["operator_channel_checked_records"], 45)
        for summary in summary_by_axis.values():
            self.assertEqual(summary["punctured_records"], 250)
            self.assertEqual(summary["min_cut_variable_records"], 250)
            self.assertEqual(summary["operator_or_channel_split_records"], 0)
            self.assertEqual(summary["admissible_entropy_match_min_cut_operator_hits"], 0)
            self.assertEqual(summary["distance_three_witness_variants"], 10)
            self.assertTrue(summary["all_mincuts_exact"])

        variants_by_axis = {
            record["bridge_axis"]: {variant["variant"]["name"]: variant for variant in record["variant_records"]}
            for record in axis_records
        }
        self.assertEqual(
            variants_by_axis["X"]["leaf_to_root_same_position__flip_offset_0_to_root_to_leaf"]["summary"][
                "entropy_match_records"
            ],
            0,
        )
        self.assertEqual(
            variants_by_axis["Y"]["leaf_to_root_same_position__flip_offset_0_to_root_to_leaf"]["summary"][
                "entropy_match_records"
            ],
            10,
        )
        self.assertEqual(
            variants_by_axis["Z"]["alternating_disentangler_isometry__flip_offset_2_to_leaf_to_root"]["summary"][
                "entropy_match_records"
            ],
            15,
        )
        self.assertEqual(
            variants_by_axis["Z"]["alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf"]["summary"][
                "entropy_match_records"
            ],
            5,
        )

        parent_summaries_by_axis = {
            record["bridge_axis"]: {summary["parent"]: summary for summary in record["parent_summaries"]}
            for record in axis_records
        }
        self.assertEqual(
            parent_summaries_by_axis["X"]["leaf_to_root_same_position"]["entropy_match_records"], 0
        )
        self.assertEqual(
            parent_summaries_by_axis["X"]["alternating_disentangler_isometry"]["entropy_match_records"], 30
        )
        self.assertEqual(
            parent_summaries_by_axis["Y"]["leaf_to_root_same_position"]["entropy_match_records"], 50
        )
        self.assertEqual(
            parent_summaries_by_axis["Y"]["alternating_disentangler_isometry"]["entropy_match_records"], 40
        )
        self.assertEqual(
            parent_summaries_by_axis["Z"]["leaf_to_root_same_position"]["entropy_match_records"], 0
        )
        self.assertEqual(
            parent_summaries_by_axis["Z"]["alternating_disentangler_isometry"]["entropy_match_records"], 45
        )

        selected_by_axis = {
            selected["bridge_axis"]: selected["record"]
            for selected in certificate["axis_source_pairing_frontier"]["selected_entropy_matched_records"]
        }
        self.assertEqual(selected_by_axis["X"]["region"]["name"], "root_shell_plus_edge_0_minus_q129")
        self.assertEqual(selected_by_axis["X"]["entropy_pair"], (5, 5))
        self.assertEqual(selected_by_axis["X"]["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected_by_axis["X"]["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertFalse(selected_by_axis["X"]["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(selected_by_axis["Y"]["region"]["name"], "root_shell_plus_edge_0_minus_q134")
        self.assertEqual(selected_by_axis["Y"]["entropy_pair"], (5, 5))
        self.assertEqual(selected_by_axis["Y"]["hit"]["first"]["algebra_signature"], (0, 0, 2, False))
        self.assertEqual(selected_by_axis["Y"]["hit"]["second"]["algebra_signature"], (0, 0, 2, False))
        self.assertFalse(selected_by_axis["Y"]["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(selected_by_axis["Z"]["region"]["name"], "root_shell_plus_edge_0_minus_q129")
        self.assertEqual(selected_by_axis["Z"]["entropy_pair"], (5, 5))
        self.assertEqual(selected_by_axis["Z"]["hit"]["first"]["algebra_signature"], (1, 1, 1, False))
        self.assertEqual(selected_by_axis["Z"]["hit"]["second"]["algebra_signature"], (1, 1, 1, False))
        self.assertFalse(selected_by_axis["Z"]["hit"]["comparisons"]["operator_or_channel_visible_differs"])

        self.assertEqual(certificate["axis_source_pairing_frontier"]["admissible_hit_records"], ())

    def test_holography_phase31_shared_logical_basis_twist_no_go_certificate(self):
        certificate = bridge_holography_phase31_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_31_shared_logical_basis_twist_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["bridge_axis_y_loaded"])
        self.assertTrue(claims["all_shared_logical_basis_twists_scored"])
        self.assertTrue(claims["all_twist_neighbor_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_twist_neighbor_outer_distance_three_witnessed"])
        self.assertTrue(claims["twist_offset_flip_frontier_exhausted"])
        self.assertTrue(claims["logical_basis_twists_change_entropy_gate_profile"])
        self.assertTrue(claims["all_twist_punctured_mincuts_exact"])
        self.assertTrue(claims["all_twist_punctured_records_min_cut_variable"])
        self.assertTrue(claims["all_twist_entropy_matches_operator_checked"])
        self.assertTrue(claims["no_shared_logical_twist_admissible_hits"])

        expected_profile = {
            "Z_as_Z__X_as_X": 90,
            "Z_as_Z__Y_as_X": 90,
            "X_as_Z__Z_as_X": 55,
            "X_as_Z__Y_as_X": 0,
            "Y_as_Z__Z_as_X": 55,
            "Y_as_Z__X_as_X": 0,
        }
        counts = certificate["counts"]
        self.assertEqual(counts["shared_logical_basis_twists"], 6)
        self.assertEqual(counts["bridge_axes"], 1)
        self.assertEqual(counts["source_pairings"], 1)
        self.assertEqual(counts["offset_flip_variants_per_twist"], 10)
        self.assertEqual(counts["twist_variant_records"], 60)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["candidate_punctured_records"], 1500)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 290)
        self.assertEqual(counts["entropy_mismatch_records"], 1210)
        self.assertEqual(counts["operator_channel_checked_records"], 290)
        self.assertEqual(counts["entropy_gate_rejections"], 1210)
        self.assertEqual(counts["min_cut_variable_records"], 1500)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_twist_variants"], 60)
        self.assertEqual(counts["twist_entropy_match_profile"], expected_profile)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        twist_records = certificate["shared_logical_twist_frontier"]["twist_records"]
        self.assertEqual(tuple(record["twist"]["name"] for record in twist_records), tuple(expected_profile))
        summary_by_twist = {record["twist"]["name"]: record["summary"] for record in twist_records}
        for twist_name, expected_matches in expected_profile.items():
            summary = summary_by_twist[twist_name]
            self.assertEqual(summary["punctured_records"], 250)
            self.assertEqual(summary["entropy_match_records"], expected_matches)
            self.assertEqual(summary["entropy_mismatch_records"], 250 - expected_matches)
            self.assertEqual(summary["operator_channel_checked_records"], expected_matches)
            self.assertEqual(summary["entropy_gate_rejections"], 250 - expected_matches)
            self.assertEqual(summary["min_cut_variable_records"], 250)
            self.assertEqual(summary["operator_or_channel_split_records"], 0)
            self.assertEqual(summary["admissible_entropy_match_min_cut_operator_hits"], 0)
            self.assertEqual(summary["distance_three_witness_variants"], 10)
            self.assertTrue(summary["all_mincuts_exact"])

        parent_summaries_by_twist = {
            record["twist"]["name"]: {summary["parent"]: summary for summary in record["parent_summaries"]}
            for record in twist_records
        }
        self.assertEqual(
            parent_summaries_by_twist["Z_as_Z__X_as_X"]["leaf_to_root_same_position"][
                "entropy_match_records"
            ],
            50,
        )
        self.assertEqual(
            parent_summaries_by_twist["Z_as_Z__X_as_X"]["alternating_disentangler_isometry"][
                "entropy_match_records"
            ],
            40,
        )
        self.assertEqual(
            parent_summaries_by_twist["X_as_Z__Z_as_X"]["leaf_to_root_same_position"][
                "entropy_match_records"
            ],
            25,
        )
        self.assertEqual(
            parent_summaries_by_twist["X_as_Z__Z_as_X"]["alternating_disentangler_isometry"][
                "entropy_match_records"
            ],
            30,
        )
        self.assertEqual(
            parent_summaries_by_twist["X_as_Z__Y_as_X"]["leaf_to_root_same_position"][
                "entropy_match_records"
            ],
            0,
        )
        self.assertEqual(
            parent_summaries_by_twist["X_as_Z__Y_as_X"]["alternating_disentangler_isometry"][
                "entropy_match_records"
            ],
            0,
        )
        self.assertEqual(
            parent_summaries_by_twist["Y_as_Z__Z_as_X"]["leaf_to_root_same_position"][
                "entropy_match_records"
            ],
            25,
        )
        self.assertEqual(
            parent_summaries_by_twist["Y_as_Z__Z_as_X"]["alternating_disentangler_isometry"][
                "entropy_match_records"
            ],
            30,
        )

        selected_by_twist = {
            selected["twist"]: selected["record"]
            for selected in certificate["shared_logical_twist_frontier"]["selected_entropy_matched_records"]
        }
        self.assertEqual(selected_by_twist["Z_as_Z__X_as_X"]["region"]["name"], "root_shell_plus_edge_0_minus_q134")
        self.assertEqual(selected_by_twist["Z_as_Z__X_as_X"]["entropy_pair"], (5, 5))
        self.assertEqual(
            selected_by_twist["Z_as_Z__X_as_X"]["hit"]["first"]["algebra_signature"],
            (0, 0, 2, False),
        )
        self.assertEqual(
            selected_by_twist["Z_as_Z__X_as_X"]["hit"]["second"]["algebra_signature"],
            (0, 0, 2, False),
        )
        self.assertFalse(
            selected_by_twist["Z_as_Z__X_as_X"]["hit"]["comparisons"]["operator_or_channel_visible_differs"]
        )
        self.assertEqual(selected_by_twist["X_as_Z__Z_as_X"]["region"]["name"], "root_shell_plus_edge_0_minus_q129")
        self.assertEqual(selected_by_twist["X_as_Z__Z_as_X"]["entropy_pair"], (5, 5))
        self.assertEqual(
            selected_by_twist["X_as_Z__Z_as_X"]["hit"]["first"]["algebra_signature"],
            (0, 0, 2, False),
        )
        self.assertEqual(
            selected_by_twist["X_as_Z__Z_as_X"]["hit"]["second"]["algebra_signature"],
            (0, 0, 2, False),
        )
        self.assertFalse(
            selected_by_twist["X_as_Z__Z_as_X"]["hit"]["comparisons"]["operator_or_channel_visible_differs"]
        )
        self.assertIsNone(selected_by_twist["X_as_Z__Y_as_X"])
        self.assertIsNone(selected_by_twist["Y_as_Z__X_as_X"])

        self.assertEqual(certificate["shared_logical_twist_frontier"]["admissible_hit_records"], ())

    def test_holography_phase32_independent_logical_basis_twist_priority_certificate(self):
        certificate = bridge_holography_phase32_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_32_independent_logical_basis_twist_priority_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["bridge_axis_y_loaded"])
        self.assertTrue(claims["all_independent_logical_basis_pairs_scored"])
        self.assertTrue(claims["all_priority_pairs_semantically_scored"])
        self.assertTrue(claims["independent_twist_entropy_mincut_atlas_exhausted"])
        self.assertTrue(claims["independent_twist_entropy_profile_matches_scout"])
        self.assertTrue(claims["all_atlas_punctured_mincuts_exact"])
        self.assertTrue(claims["all_atlas_punctured_records_min_cut_variable"])
        self.assertTrue(claims["priority_entropy_matches_operator_checked"])
        self.assertTrue(claims["no_priority_independent_twist_admissible_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["independent_twist_pairs"], 36)
        self.assertEqual(counts["first_twists"], 6)
        self.assertEqual(counts["second_twists"], 6)
        self.assertEqual(counts["bridge_axes"], 1)
        self.assertEqual(counts["source_pairings"], 1)
        self.assertEqual(counts["offset_flip_variants_per_pair"], 10)
        self.assertEqual(counts["independent_pair_variant_records"], 360)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["candidate_punctured_records"], 9000)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 1740)
        self.assertEqual(counts["entropy_mismatch_records"], 7260)
        self.assertEqual(counts["priority_semantic_pairs"], 4)
        self.assertEqual(counts["priority_candidate_punctured_records"], 1000)
        self.assertEqual(counts["priority_entropy_match_records"], 290)
        self.assertEqual(counts["priority_entropy_mismatch_records"], 710)
        self.assertEqual(counts["priority_operator_channel_checked_records"], 290)
        self.assertEqual(counts["semantic_audit_deferred_entropy_match_records"], 1450)
        self.assertEqual(counts["min_cut_variable_records"], 9000)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_outer_variants"], 10)
        self.assertEqual(counts["pair_entropy_match_profile_distribution"], {0: 12, 55: 12, 90: 12})
        self.assertEqual(
            counts["priority_pair_entropy_match_profile"],
            {"shared_high": 90, "offdiag_high": 90, "shared_medium": 55, "offdiag_medium": 55},
        )
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["independent_twist_frontier"]
        self.assertEqual(frontier["semantic_audit_deferred_entropy_match_records"], 1450)
        self.assertEqual(frontier["profile_distribution"], {0: 12, 55: 12, 90: 12})
        pair_profile = frontier["pair_entropy_profile"]
        self.assertEqual(
            pair_profile["first_Z_as_Z__X_as_X__second_Z_as_Z__X_as_X"],
            90,
        )
        self.assertEqual(
            pair_profile["first_X_as_Z__Y_as_X__second_Z_as_Z__X_as_X"],
            90,
        )
        self.assertEqual(
            pair_profile["first_X_as_Z__Z_as_X__second_X_as_Z__Z_as_X"],
            55,
        )
        self.assertEqual(
            pair_profile["first_Z_as_Z__X_as_X__second_X_as_Z__Y_as_X"],
            0,
        )

        atlas_by_name = {record["pair"]["name"]: record for record in frontier["pair_atlas_records"]}
        self.assertEqual(
            atlas_by_name["first_Z_as_Z__X_as_X__second_Z_as_Z__X_as_X"]["summary"][
                "entropy_match_records"
            ],
            90,
        )
        self.assertEqual(
            atlas_by_name["first_Z_as_Z__X_as_X__second_Z_as_Z__X_as_X"]["summary"][
                "semantic_audit_deferred_records"
            ],
            90,
        )
        self.assertEqual(
            atlas_by_name["first_Z_as_Z__X_as_X__second_X_as_Z__Y_as_X"]["summary"][
                "entropy_match_records"
            ],
            0,
        )
        self.assertIsNone(
            atlas_by_name["first_Z_as_Z__X_as_X__second_X_as_Z__Y_as_X"][
                "selected_entropy_matched_record"
            ]
        )

        priority_by_label = {
            record["priority_pair"]["priority_label"]: record for record in frontier["priority_pair_records"]
        }
        for label, expected_matches in (
            ("shared_high", 90),
            ("offdiag_high", 90),
            ("shared_medium", 55),
            ("offdiag_medium", 55),
        ):
            summary = priority_by_label[label]["summary"]
            self.assertEqual(summary["punctured_records"], 250)
            self.assertEqual(summary["entropy_match_records"], expected_matches)
            self.assertEqual(summary["operator_channel_checked_records"], expected_matches)
            self.assertEqual(summary["operator_or_channel_split_records"], 0)
            self.assertEqual(summary["admissible_entropy_match_min_cut_operator_hits"], 0)
            self.assertEqual(summary["min_cut_variable_records"], 250)
            self.assertTrue(summary["all_mincuts_exact"])

        self.assertEqual(
            priority_by_label["shared_high"]["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q134",
        )
        self.assertEqual(
            priority_by_label["shared_high"]["selected_entropy_matched_record"]["hit"]["first"][
                "algebra_signature"
            ],
            (0, 0, 2, False),
        )
        self.assertFalse(
            priority_by_label["shared_high"]["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )
        self.assertEqual(
            priority_by_label["offdiag_high"]["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q134",
        )
        self.assertFalse(
            priority_by_label["offdiag_high"]["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )
        self.assertEqual(
            priority_by_label["shared_medium"]["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q129",
        )
        self.assertFalse(
            priority_by_label["shared_medium"]["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )
        self.assertEqual(
            priority_by_label["offdiag_medium"]["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q129",
        )
        self.assertFalse(
            priority_by_label["offdiag_medium"]["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )
        self.assertEqual(frontier["priority_admissible_hit_records"], ())

    def test_holography_phase33_full_independent_logical_basis_twist_no_go_certificate(self):
        certificate = bridge_holography_phase33_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_33_full_independent_logical_basis_twist_no_go_certificate"])
        self.assertTrue(claims["phase2_graph_source_loaded"])
        self.assertTrue(claims["bridge_axis_y_loaded"])
        self.assertTrue(claims["all_independent_logical_basis_pairs_semantically_scored"])
        self.assertTrue(claims["independent_twist_full_semantic_frontier_exhausted"])
        self.assertTrue(claims["independent_twist_entropy_profile_matches_phase32"])
        self.assertTrue(claims["all_full_semantic_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_full_semantic_outer_distance_three_witnessed"])
        self.assertTrue(claims["all_full_semantic_mincuts_exact"])
        self.assertTrue(claims["all_full_semantic_punctured_records_min_cut_variable"])
        self.assertTrue(claims["all_entropy_matches_operator_checked"])
        self.assertTrue(claims["no_full_independent_twist_admissible_hits"])

        counts = certificate["counts"]
        self.assertEqual(counts["independent_twist_pairs"], 36)
        self.assertEqual(counts["first_twists"], 6)
        self.assertEqual(counts["second_twists"], 6)
        self.assertEqual(counts["bridge_axes"], 1)
        self.assertEqual(counts["source_pairings"], 1)
        self.assertEqual(counts["offset_flip_variants_per_pair"], 10)
        self.assertEqual(counts["independent_pair_variant_records"], 360)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["candidate_punctured_records"], 9000)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 1740)
        self.assertEqual(counts["entropy_mismatch_records"], 7260)
        self.assertEqual(counts["operator_channel_checked_records"], 1740)
        self.assertEqual(counts["entropy_gate_rejections"], 7260)
        self.assertEqual(counts["semantic_audit_deferred_entropy_match_records"], 0)
        self.assertEqual(counts["min_cut_variable_records"], 9000)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_twist_variants"], 360)
        self.assertEqual(counts["pair_entropy_match_profile_distribution"], {0: 12, 55: 12, 90: 12})
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["full_independent_twist_frontier"]
        self.assertEqual(frontier["profile_distribution"], {0: 12, 55: 12, 90: 12})
        self.assertEqual(frontier["operator_or_channel_split_records"], ())
        self.assertEqual(frontier["admissible_hit_records"], ())
        pair_profile = frontier["pair_entropy_profile"]
        self.assertEqual(pair_profile["first_Z_as_Z__X_as_X__second_Z_as_Z__X_as_X"], 90)
        self.assertEqual(pair_profile["first_X_as_Z__Y_as_X__second_Z_as_Z__X_as_X"], 90)
        self.assertEqual(pair_profile["first_X_as_Z__Z_as_X__second_X_as_Z__Z_as_X"], 55)
        self.assertEqual(pair_profile["first_Z_as_Z__X_as_X__second_X_as_Z__Y_as_X"], 0)

        pair_by_name = {record["pair"]["name"]: record for record in frontier["pair_records"]}
        high_pair = pair_by_name["first_Z_as_Z__X_as_X__second_Z_as_Z__X_as_X"]
        self.assertEqual(high_pair["summary"]["entropy_match_records"], 90)
        self.assertEqual(high_pair["summary"]["operator_channel_checked_records"], 90)
        self.assertEqual(high_pair["summary"]["operator_or_channel_split_records"], 0)
        self.assertEqual(high_pair["selected_entropy_matched_record"]["region"]["name"], "root_shell_plus_edge_0_minus_q134")
        self.assertEqual(
            high_pair["selected_entropy_matched_record"]["hit"]["first"]["algebra_signature"],
            (0, 0, 2, False),
        )
        self.assertEqual(
            high_pair["selected_entropy_matched_record"]["hit"]["second"]["algebra_signature"],
            (0, 0, 2, False),
        )
        self.assertFalse(
            high_pair["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )

        offdiag_high = pair_by_name["first_X_as_Z__Y_as_X__second_Z_as_Z__X_as_X"]
        self.assertEqual(offdiag_high["summary"]["entropy_match_records"], 90)
        self.assertEqual(offdiag_high["summary"]["operator_channel_checked_records"], 90)
        self.assertEqual(offdiag_high["summary"]["operator_or_channel_split_records"], 0)
        self.assertEqual(
            offdiag_high["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q134",
        )
        self.assertFalse(
            offdiag_high["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )

        medium_pair = pair_by_name["first_X_as_Z__Z_as_X__second_X_as_Z__Z_as_X"]
        self.assertEqual(medium_pair["summary"]["entropy_match_records"], 55)
        self.assertEqual(medium_pair["summary"]["operator_channel_checked_records"], 55)
        self.assertEqual(medium_pair["summary"]["operator_or_channel_split_records"], 0)
        self.assertEqual(
            medium_pair["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q129",
        )
        self.assertFalse(
            medium_pair["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )

        zero_pair = pair_by_name["first_Z_as_Z__X_as_X__second_X_as_Z__Y_as_X"]
        self.assertEqual(zero_pair["summary"]["entropy_match_records"], 0)
        self.assertEqual(zero_pair["summary"]["operator_channel_checked_records"], 0)
        self.assertIsNone(zero_pair["selected_entropy_matched_record"])

    def test_holography_phase34_bounded_alternative_source_pair_scout_certificate(self):
        certificate = bridge_holography_phase34_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_34_bounded_alternative_source_pair_scout_certificate"])
        self.assertTrue(claims["bounded_graph_cws_source_atlas_exhausted"])
        self.assertTrue(claims["all_reconstruction_discordant_labeled_t2_source_pairs_loaded"])
        self.assertTrue(claims["phase2_primary_pair_retained_with_three_alternatives"])
        self.assertTrue(claims["bridge_axis_y_loaded"])
        self.assertTrue(claims["phase26_frontier_scored_for_each_source_pair"])
        self.assertTrue(claims["alternative_source_pair_full_entropy_frontier_found"])
        self.assertTrue(claims["all_candidate_mincuts_exact_and_variable"])
        self.assertTrue(claims["priority_semantic_audit_scored_per_parent"])
        self.assertTrue(claims["priority_entropy_matched_records_have_no_admissible_hits"])
        self.assertTrue(claims["priority_entropy_mismatch_near_hits_recorded"])

        counts = certificate["counts"]
        self.assertEqual(counts["raw_graph_codes"], 33)
        self.assertEqual(counts["relaxed_codes_checked"], 33)
        self.assertEqual(counts["entropy_classes"], 28)
        self.assertEqual(counts["source_pairs"], 4)
        self.assertEqual(counts["phase2_primary_source_pairs"], 1)
        self.assertEqual(counts["non_primary_alternative_source_pairs"], 3)
        self.assertEqual(counts["source_pair_ordinals"], ((16, 23), (21, 26), (21, 27), (26, 27)))
        self.assertEqual(counts["offset_flip_variants_per_source_pair"], 10)
        self.assertEqual(counts["source_pair_variant_records"], 40)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["candidate_records"], 1000)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 520)
        self.assertEqual(counts["entropy_mismatch_records"], 480)
        self.assertEqual(counts["operator_channel_checked_records"], 14)
        self.assertEqual(counts["priority_entropy_match_checked_records"], 8)
        self.assertEqual(counts["priority_entropy_mismatch_checked_records"], 6)
        self.assertEqual(counts["semantic_audit_deferred_entropy_match_records"], 512)
        self.assertEqual(counts["entropy_mismatch_near_hit_deferred_records"], 474)
        self.assertEqual(counts["min_cut_variable_records"], 1000)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 3)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["priority_entropy_mismatch_operator_near_hits"], 3)
        self.assertEqual(counts["distance_three_witness_source_variants"], 40)
        self.assertEqual(counts["pair_entropy_match_profile_distribution"], {90: 3, 250: 1})
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["alternative_source_frontier"]
        self.assertEqual(frontier["profile_distribution"], {90: 3, 250: 1})
        self.assertEqual(frontier["admissible_hit_records"], ())
        self.assertEqual(len(frontier["priority_entropy_mismatch_near_hit_records"]), 3)
        pair_profile = frontier["pair_entropy_profile"]
        self.assertEqual(pair_profile["graph_cws_labeled_source_ord16_ord23"], 90)
        self.assertEqual(pair_profile["graph_cws_labeled_source_ord21_ord26"], 250)
        self.assertEqual(pair_profile["graph_cws_labeled_source_ord21_ord27"], 90)
        self.assertEqual(pair_profile["graph_cws_labeled_source_ord26_ord27"], 90)

        pair_by_name = {record["pair"]["name"]: record for record in frontier["pair_records"]}
        full_entropy_pair = pair_by_name["graph_cws_labeled_source_ord21_ord26"]
        self.assertFalse(full_entropy_pair["pair"]["phase2_primary_pair"])
        self.assertEqual(full_entropy_pair["summary"]["entropy_match_records"], 250)
        self.assertEqual(full_entropy_pair["summary"]["entropy_mismatch_records"], 0)
        self.assertEqual(full_entropy_pair["summary"]["operator_channel_checked_records"], 2)
        self.assertEqual(full_entropy_pair["summary"]["priority_entropy_mismatch_operator_near_hits"], 0)
        self.assertIsNone(full_entropy_pair["selected_entropy_mismatch_record"])
        self.assertEqual(
            full_entropy_pair["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q129",
        )
        self.assertFalse(
            full_entropy_pair["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )

        primary_pair = pair_by_name["graph_cws_labeled_source_ord16_ord23"]
        self.assertTrue(primary_pair["pair"]["phase2_primary_pair"])
        self.assertEqual(primary_pair["summary"]["entropy_match_records"], 90)
        self.assertEqual(primary_pair["summary"]["priority_entropy_mismatch_operator_near_hits"], 1)
        self.assertEqual(
            primary_pair["selected_entropy_mismatch_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q129",
        )
        self.assertFalse(
            primary_pair["selected_entropy_mismatch_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )

    def test_holography_phase35_full_alternative_source_pair_semantic_audit_certificate(self):
        certificate = bridge_holography_phase35_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_35_full_alternative_source_pair_semantic_audit_certificate"])
        self.assertTrue(claims["phase34_source_pair_21_26_loaded"])
        self.assertTrue(claims["bridge_axis_y_loaded"])
        self.assertTrue(claims["phase26_frontier_fully_semantically_scored"])
        self.assertTrue(claims["all_source_pair_records_entropy_matched"])
        self.assertTrue(claims["all_source_pair_mincuts_exact_and_variable"])
        self.assertTrue(claims["all_source_pair_code_pairs_are_n150_k1"])
        self.assertTrue(claims["all_source_pair_outer_distance_three_witnessed"])
        self.assertTrue(claims["full_semantic_hit_outcome_classified"])

        counts = certificate["counts"]
        self.assertEqual(counts["source_pairs_loaded"], 1)
        self.assertEqual(counts["raw_graph_codes"], 33)
        self.assertEqual(counts["relaxed_codes_checked"], 33)
        self.assertEqual(counts["source_pair_ordinals"], (21, 26))
        self.assertEqual(counts["offset_flip_variants"], 10)
        self.assertEqual(counts["parent_circuits"], 2)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["candidate_records"], 250)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 250)
        self.assertEqual(counts["entropy_mismatch_records"], 0)
        self.assertEqual(counts["operator_channel_checked_records"], 250)
        self.assertEqual(counts["entropy_gate_rejections"], 0)
        self.assertEqual(counts["semantic_audit_deferred_entropy_match_records"], 0)
        self.assertEqual(counts["min_cut_variable_records"], 250)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["entropy_mismatch_operator_near_hits"], 0)
        self.assertEqual(counts["distance_three_witness_source_variants"], 10)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["full_source_pair_frontier"]
        self.assertEqual(frontier["operator_or_channel_split_records"], ())
        self.assertEqual(frontier["admissible_hit_records"], ())
        self.assertIsNone(frontier["selected_entropy_mismatch_record"])
        self.assertEqual(
            frontier["selected_entropy_matched_record"]["region"]["name"],
            "root_shell_plus_edge_0_minus_q129",
        )
        self.assertFalse(
            frontier["selected_entropy_matched_record"]["hit"]["comparisons"][
                "operator_or_channel_visible_differs"
            ]
        )

    def test_holography_phase36_full_entropy_mismatch_near_hit_audit_certificate(self):
        certificate = bridge_holography_phase36_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_36_full_entropy_mismatch_near_hit_audit_certificate"])
        self.assertTrue(claims["phase34_entropy_mismatch_source_pairs_loaded"])
        self.assertTrue(claims["bridge_axis_y_loaded"])
        self.assertTrue(claims["phase26_entropy_mismatch_surface_fully_audited"])
        self.assertTrue(claims["entropy_match_records_deliberately_skipped_by_near_hit_audit"])
        self.assertTrue(claims["all_entropy_mismatch_mincuts_exact_and_variable"])
        self.assertTrue(claims["near_hits_partition_by_parent"])
        self.assertTrue(claims["near_hit_profile_repeats_across_source_pairs"])
        self.assertTrue(claims["near_hits_classified_by_channel_visibility"])
        self.assertTrue(claims["no_entropy_matched_admissible_hits_claimed"])

        counts = certificate["counts"]
        self.assertEqual(counts["source_pairs_loaded"], 3)
        self.assertEqual(counts["raw_graph_codes"], 33)
        self.assertEqual(counts["relaxed_codes_checked"], 33)
        self.assertEqual(counts["source_pair_ordinals"], ((16, 23), (21, 27), (26, 27)))
        self.assertEqual(counts["offset_flip_variants_per_source_pair"], 10)
        self.assertEqual(counts["source_pair_variant_records"], 30)
        self.assertEqual(counts["parent_circuits"], 2)
        self.assertEqual(counts["base_punctured_regions"], 25)
        self.assertEqual(counts["candidate_records"], 750)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 270)
        self.assertEqual(counts["entropy_mismatch_records"], 480)
        self.assertEqual(counts["operator_channel_checked_records"], 480)
        self.assertEqual(counts["semantic_audit_skipped_entropy_match_records"], 270)
        self.assertEqual(counts["mismatch_min_cut_variable_records"], 480)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 165)
        self.assertEqual(counts["entropy_mismatch_operator_near_hits"], 165)
        self.assertEqual(counts["channel_visible_near_hits"], 85)
        self.assertEqual(counts["operator_only_near_hits"], 80)
        self.assertEqual(counts["leaf_to_root_near_hits"], 0)
        self.assertEqual(counts["alternating_near_hits"], 165)
        self.assertEqual(counts["distance_three_witness_source_variants"], 30)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["near_hit_frontier"]
        self.assertEqual(
            frontier["pair_near_hit_profile"],
            {
                "graph_cws_labeled_source_ord16_ord23": 55,
                "graph_cws_labeled_source_ord21_ord27": 55,
                "graph_cws_labeled_source_ord26_ord27": 55,
            },
        )
        self.assertEqual(
            frontier["parent_near_hit_profile"],
            {
                "leaf_to_root_same_position": 0,
                "alternating_disentangler_isometry": 165,
            },
        )
        self.assertEqual(frontier["variant_near_hit_profile"]["alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root"], 30)
        self.assertEqual(frontier["variant_near_hit_profile"]["alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf"], 45)
        self.assertEqual(frontier["variant_near_hit_profile"]["alternating_disentangler_isometry__flip_offset_2_to_leaf_to_root"], 15)
        self.assertEqual(frontier["variant_near_hit_profile"]["alternating_disentangler_isometry__flip_offset_3_to_root_to_leaf"], 45)
        self.assertEqual(frontier["variant_near_hit_profile"]["alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root"], 30)
        self.assertEqual(frontier["variant_near_hit_profile"]["leaf_to_root_same_position__flip_offset_0_to_root_to_leaf"], 0)
        self.assertEqual(len(frontier["region_near_hit_profile"]), 25)
        self.assertEqual(frontier["region_near_hit_profile"]["root_shell_plus_edge_0_minus_q139"], 15)
        self.assertEqual(frontier["region_near_hit_profile"]["root_shell_plus_edge_0_minus_q129"], 6)
        self.assertEqual(len(frontier["near_hit_records"]), 165)
        self.assertTrue(all(not record["entropy_matches"] for record in frontier["near_hit_records"]))

    def test_holography_phase37_split_support_region_grammar_certificate(self):
        certificate = bridge_holography_phase37_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_37_split_support_region_grammar_certificate"])
        self.assertTrue(claims["phase36_source_pairs_reused"])
        self.assertTrue(claims["phase36_alternating_seed_profile_replayed"])
        self.assertTrue(claims["split_support_edit_grammar_bounded"])
        self.assertTrue(claims["all_split_support_mincuts_exact_and_variable"])
        self.assertTrue(claims["split_support_frontier_exhausted"])
        self.assertTrue(claims["all_split_support_candidates_entropy_rejected"])
        self.assertTrue(claims["no_split_support_admissible_hits"])
        self.assertTrue(claims["candidate_profile_matches_phase36_seed_multiplicity"])

        counts = certificate["counts"]
        self.assertEqual(counts["source_pairs_loaded"], 3)
        self.assertEqual(counts["raw_graph_codes"], 33)
        self.assertEqual(counts["relaxed_codes_checked"], 33)
        self.assertEqual(counts["source_pair_ordinals"], ((16, 23), (21, 27), (26, 27)))
        self.assertEqual(counts["seed_alternating_variants"], 5)
        self.assertEqual(counts["seed_variant_hole_rules"], 11)
        self.assertEqual(counts["seed_base_records"], 165)
        self.assertEqual(counts["unique_split_support_region_specs"], 200)
        self.assertEqual(counts["edit_kinds"], 2)
        self.assertEqual(counts["candidate_split_support_records"], 1320)
        self.assertEqual(counts["add_leaf_private_records"], 660)
        self.assertEqual(counts["swap_leaf_handle_records"], 660)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 0)
        self.assertEqual(counts["entropy_mismatch_records"], 1320)
        self.assertEqual(counts["operator_channel_checked_records"], 0)
        self.assertEqual(counts["split_support_entropy_gate_rejections"], 1320)
        self.assertEqual(counts["min_cut_variable_records"], 1320)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 0)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 0)
        self.assertEqual(counts["distance_three_witness_source_variants"], 15)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["split_support_frontier"]
        self.assertEqual(
            frontier["pair_candidate_profile"],
            {
                "graph_cws_labeled_source_ord16_ord23": 440,
                "graph_cws_labeled_source_ord21_ord27": 440,
                "graph_cws_labeled_source_ord26_ord27": 440,
            },
        )
        self.assertEqual(frontier["edit_profile"], {"add_leaf_private": 660, "swap_leaf_handle": 660})
        self.assertEqual(
            frontier["variant_candidate_profile"],
            {
                "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root": 240,
                "alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf": 360,
                "alternating_disentangler_isometry__flip_offset_2_to_leaf_to_root": 120,
                "alternating_disentangler_isometry__flip_offset_3_to_root_to_leaf": 360,
                "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root": 240,
            },
        )
        self.assertEqual(
            frontier["removed_root_qubit_profile"],
            {"129": 240, "134": 120, "139": 600, "144": 120, "149": 240},
        )
        self.assertEqual(
            frontier["entropy_pair_profile"],
            {
                "(4, 5)": 100,
                "(5, 4)": 240,
                "(5, 6)": 220,
                "(6, 5)": 140,
                "(6, 7)": 120,
                "(7, 6)": 380,
                "(8, 7)": 120,
            },
        )
        self.assertEqual(
            frontier["min_cut_value_profile"],
            {"(7, 9, 11, 12, 15, 17)": 660, "(8, 10, 12, 13, 16, 18)": 660},
        )
        self.assertEqual(frontier["operator_or_channel_split_records"], ())
        self.assertEqual(frontier["admissible_hit_records"], ())
        first_pair = frontier["pair_records"][0]
        self.assertIsNotNone(first_pair["selected_entropy_mismatch_record"])
        self.assertIsNone(first_pair["selected_entropy_matched_record"])

    def test_holography_phase38_q139_support_scale_strict_hit_certificate(self):
        certificate = bridge_holography_phase38_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_38_q139_support_scale_strict_hit_certificate"])
        self.assertTrue(claims["phase37_q139_seed_surface_reused"])
        self.assertTrue(claims["q139_support_scale_grammar_bounded"])
        self.assertTrue(claims["q139_frontier_exhausted"])
        self.assertTrue(claims["all_q139_support_mincuts_exact_and_variable"])
        self.assertTrue(claims["strict_holographic_cousin_hits_found"])
        self.assertTrue(claims["strict_hits_localized_to_source_21_27_and_same_leaf_0_3"])
        self.assertTrue(claims["strict_hits_repeat_across_variants_and_leaf_cells"])
        self.assertTrue(claims["strict_hits_classified_by_channel_visibility"])

        counts = certificate["counts"]
        self.assertEqual(counts["source_pairs_loaded"], 3)
        self.assertEqual(counts["raw_graph_codes"], 33)
        self.assertEqual(counts["relaxed_codes_checked"], 33)
        self.assertEqual(counts["source_pair_ordinals"], ((16, 23), (21, 27), (26, 27)))
        self.assertEqual(counts["q139_base_regions"], 5)
        self.assertEqual(counts["seed_alternating_variants"], 5)
        self.assertEqual(counts["seed_base_records"], 75)
        self.assertEqual(counts["unique_q139_support_region_specs"], 110)
        self.assertEqual(counts["edit_kinds"], 2)
        self.assertEqual(counts["candidate_q139_support_records"], 1650)
        self.assertEqual(counts["same_leaf_two_private_add_records"], 450)
        self.assertEqual(counts["cross_leaf_private_add_records"], 1200)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["entropy_match_records"], 25)
        self.assertEqual(counts["entropy_mismatch_records"], 1625)
        self.assertEqual(counts["operator_channel_checked_records"], 25)
        self.assertEqual(counts["q139_support_entropy_gate_rejections"], 1625)
        self.assertEqual(counts["min_cut_variable_records"], 1650)
        self.assertEqual(counts["operator_or_channel_split_records_checked"], 25)
        self.assertEqual(counts["admissible_entropy_match_min_cut_operator_hits"], 25)
        self.assertEqual(counts["channel_visible_admissible_hits"], 15)
        self.assertEqual(counts["operator_only_admissible_hits"], 10)
        self.assertEqual(counts["distance_three_witness_source_variants"], 15)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["q139_support_frontier"]
        self.assertEqual(
            frontier["pair_candidate_profile"],
            {
                "graph_cws_labeled_source_ord16_ord23": 550,
                "graph_cws_labeled_source_ord21_ord27": 550,
                "graph_cws_labeled_source_ord26_ord27": 550,
            },
        )
        self.assertEqual(
            frontier["pair_admissible_profile"],
            {
                "graph_cws_labeled_source_ord16_ord23": 0,
                "graph_cws_labeled_source_ord21_ord27": 25,
                "graph_cws_labeled_source_ord26_ord27": 0,
            },
        )
        self.assertEqual(
            frontier["variant_admissible_profile"],
            {
                "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root": 5,
                "alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf": 5,
                "alternating_disentangler_isometry__flip_offset_2_to_leaf_to_root": 5,
                "alternating_disentangler_isometry__flip_offset_3_to_root_to_leaf": 5,
                "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root": 5,
            },
        )
        self.assertEqual(
            frontier["edit_candidate_profile"],
            {"cross_leaf_private_add": 1200, "same_leaf_two_private_add": 450},
        )
        self.assertEqual(frontier["edit_admissible_profile"], {"same_leaf_two_private_add": 25})
        self.assertEqual(
            frontier["admissible_entropy_pair_profile"],
            {"(4, 4)": 10, "(5, 5)": 5, "(6, 6)": 10},
        )
        self.assertEqual(
            frontier["admissible_min_cut_value_profile"],
            {"(9, 11, 13, 14, 17, 19)": 25},
        )
        self.assertEqual(frontier["admissible_offset_profile"], {"(0, 3)": 25})
        self.assertEqual(frontier["admissible_leaf_profile"], {"0": 5, "1": 5, "2": 5, "3": 5, "4": 5})
        self.assertEqual(frontier["channel_visibility_profile"], {"channel_visible": 15, "operator_only": 10})
        self.assertEqual(len(frontier["admissible_hit_records"]), 25)
        self.assertEqual(len(frontier["operator_or_channel_split_records"]), 25)
        first_hit = frontier["admissible_hit_records"][0]
        self.assertTrue(first_hit["entropy_matches"])
        self.assertTrue(first_hit["min_cut_variable"])
        self.assertTrue(first_hit["hit"]["comparisons"]["operator_or_channel_visible_differs"])
        self.assertEqual(frontier["pair_records"][0]["admissible_hit_records"], ())
        self.assertIsNotNone(frontier["pair_records"][1]["selected_admissible_hit_record"])
        self.assertEqual(frontier["pair_records"][2]["admissible_hit_records"], ())

    def test_holography_phase39_representative_witness_robustness_certificate(self):
        certificate = bridge_holography_phase39_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_39_representative_witness_robustness_certificate"])
        self.assertTrue(claims["phase38_representative_loaded"])
        self.assertTrue(claims["alternative_offsets_certify_unique_pair_0_3"])
        self.assertTrue(claims["single_deletion_plateau_audited"])
        self.assertTrue(claims["local_single_addition_plateau_audited"])
        self.assertTrue(claims["all_phase39_records_exact_and_capacity_sensitive"])
        self.assertTrue(claims["representative_is_not_locally_minimal_but_is_robust"])

        representative = certificate["representative"]["record"]
        self.assertEqual(representative["region"]["name"], "root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3")
        self.assertEqual(representative["region"]["length"], 27)
        self.assertEqual(representative["entropy_pair"], (4, 4))
        self.assertEqual(representative["min_cut_values"], (9, 11, 13, 14, 17, 19))
        self.assertTrue(representative["admissible_entropy_match_min_cut_operator_hit"])
        self.assertTrue(representative["channel_visible_admissible_hit"])
        self.assertTrue(representative["hit"]["comparisons"]["reconstruction_visible_differs"])
        self.assertTrue(representative["hit"]["comparisons"]["channel_visible_differs"])

        counts = certificate["counts"]
        self.assertEqual(counts["source_pairs_loaded"], 1)
        self.assertEqual(counts["raw_graph_codes"], 33)
        self.assertEqual(counts["relaxed_codes_checked"], 33)
        self.assertEqual(counts["representative_region_length"], 27)
        self.assertEqual(counts["capacity_profiles_scored"], 10)
        self.assertEqual(counts["alternative_offset_records"], 6)
        self.assertEqual(counts["alternative_offset_admissible_hits"], 1)
        self.assertEqual(counts["single_deletion_records"], 27)
        self.assertEqual(counts["single_deletion_admissible_hits"], 15)
        self.assertEqual(counts["local_single_addition_records"], 19)
        self.assertEqual(counts["local_single_addition_admissible_hits"], 18)
        self.assertEqual(counts["neighborhood_records"], 52)
        self.assertEqual(counts["neighborhood_admissible_hits"], 34)
        self.assertEqual(counts["all_records_including_representative"], 53)
        self.assertEqual(counts["all_records_exact"], 53)
        self.assertEqual(counts["all_records_min_cut_variable"], 53)
        self.assertEqual(counts["channel_visible_neighbor_hits"], 34)
        self.assertEqual(counts["operator_only_neighbor_hits"], 0)
        self.assertEqual(counts["max_candidate_min_cut_internal_assignments"], 64)
        self.assertEqual(counts["min_candidate_min_cut_internal_assignments"], 64)

        frontier = certificate["robustness_frontier"]
        self.assertEqual(frontier["alternative_offset_summary"]["records"], 6)
        self.assertEqual(frontier["alternative_offset_summary"]["admissible_entropy_match_min_cut_operator_hits"], 1)
        self.assertEqual(frontier["single_deletion_summary"]["admissible_entropy_match_min_cut_operator_hits"], 15)
        self.assertEqual(frontier["local_single_addition_summary"]["admissible_entropy_match_min_cut_operator_hits"], 18)
        self.assertEqual(
            frontier["strict_deletion_qubits"],
            (125, 128, 129, 130, 133, 134, 135, 136, 137, 138, 140, 143, 144, 146, 147),
        )
        self.assertEqual(
            frontier["strict_addition_qubits"],
            (1, 2, 25, 26, 27, 28, 50, 51, 52, 53, 75, 76, 77, 78, 100, 101, 102, 103),
        )
        self.assertEqual(frontier["alternative_entropy_pair_profile"], {"(4, 4)": 1, "(6, 4)": 1, "(6, 5)": 4})
        self.assertEqual(
            frontier["deletion_entropy_pair_profile"],
            {"(4, 4)": 2, "(4, 5)": 6, "(5, 4)": 6, "(5, 5)": 13},
        )
        self.assertEqual(frontier["addition_entropy_pair_profile"], {"(3, 4)": 1, "(5, 5)": 18})
        self.assertEqual(len(frontier["neighborhood_admissible_records"]), 34)

    def test_holography_phase40_theorem_style_package_certificate(self):
        certificate = bridge_holography_phase40_certificate()
        self.assertEqual(certificate["status"], "pass")
        claims = certificate["certified_claims"]
        self.assertTrue(claims["goal_3_phase_40_theorem_style_package_certificate"])
        self.assertTrue(claims["phase38_strict_family_certificate_loaded"])
        self.assertTrue(claims["phase39_representative_robustness_certificate_loaded"])
        self.assertTrue(claims["compact_witness_index_identifies_single_channel_visible_hit"])
        self.assertTrue(claims["three_geometry_separation_obligations_satisfied"])

        counts = certificate["counts"]
        self.assertEqual(counts["source_certificates_loaded"], 2)
        self.assertEqual(counts["strict_family_hits"], 25)
        self.assertEqual(counts["strict_family_channel_visible_hits"], 15)
        self.assertEqual(counts["representative_region_length"], 27)
        self.assertEqual(counts["representative_entropy"], (4, 4))
        self.assertEqual(counts["representative_min_cut_values"], (9, 11, 13, 14, 17, 19))
        self.assertEqual(counts["neighborhood_records"], 52)
        self.assertEqual(counts["neighborhood_admissible_hits"], 34)
        self.assertEqual(counts["proof_obligations"], 6)
        self.assertEqual(counts["proof_obligations_satisfied"], 6)

        witness = certificate["witness_index"]
        self.assertEqual(witness["source_pair"]["source_ordinals"], (21, 27))
        self.assertEqual(witness["bridge_axis"], "Y")
        self.assertEqual(witness["outer_variant"]["name"], "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root")
        self.assertEqual(witness["region"]["name"], "root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3")
        self.assertEqual(witness["entropy_pair"], (4, 4))
        self.assertEqual(witness["min_cut_values"], (9, 11, 13, 14, 17, 19))
        self.assertTrue(witness["diagnostic_separation"]["entropy_matches"])
        self.assertTrue(witness["diagnostic_separation"]["min_cut_variable"])
        self.assertTrue(witness["diagnostic_separation"]["reconstruction_visible_differs"])
        self.assertTrue(witness["diagnostic_separation"]["channel_visible_differs"])

        proof = certificate["proof_obligations"]
        self.assertTrue(all(record["satisfied"] for record in proof.values()))
        self.assertEqual(certificate["source_certificates"]["phase38"]["counts"]["admissible_entropy_match_min_cut_operator_hits"], 25)
        self.assertEqual(certificate["source_certificates"]["phase39"]["counts"]["neighborhood_admissible_hits"], 34)
        self.assertEqual(certificate["recommendation"]["next_phase"], "stop")


if __name__ == "__main__":
    unittest.main()
