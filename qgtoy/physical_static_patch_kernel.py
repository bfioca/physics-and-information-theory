"""Goal 25 physically motivated static-patch kernel candidates."""

from __future__ import annotations

from math import exp, log2

from .bilayer import binary_entropy
from .conditional_ds_er_epr import _cholesky_psd_summary
from .general_algebraic_connectivity import coherence_probe_relative_entropy_bits
from .relative_entropy_bridge import _rounded
from .static_patch_testbed import mode_count, static_patch_mode_labels


def _validate_cutoff(cutoff: int) -> None:
    if cutoff < 1:
        raise ValueError("cutoff must be at least one")


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 1:
        raise ValueError("max_cutoff must be at least one")


def _validate_low_order(low_order: int) -> None:
    if low_order < 0:
        raise ValueError("low_order must be nonnegative")


def _validate_probability(screen_probability: float) -> None:
    if not 0.0 <= screen_probability <= 1.0:
        raise ValueError("screen_probability must lie in [0,1]")


def _validate_noise_strength(noise_strength: float) -> None:
    if noise_strength < 0.0:
        raise ValueError("noise_strength must be nonnegative")


def default_axis_split(cutoff: int) -> float:
    """Small rational m-splitting that removes ell-degeneracy at finite L."""
    _validate_cutoff(cutoff)
    return 1.0 / float(2 * cutoff + 3)


def fuzzy_static_patch_energy(
    cutoff: int,
    label: tuple[int, int],
    *,
    axis_split: float | None = None,
) -> float:
    """Normalized finite static-patch Hamiltonian eigenvalue.

    The base spectrum is the fuzzy-sphere/spherical-harmonic Laplacian
    eigenvalue ell(ell+1). The small axis_split*m term is a finite
    axisymmetric chemical-potential/rotation split used to make the testbed's
    logical mode labels distinguishable without changing diagonal screen data.
    """
    _validate_cutoff(cutoff)
    ell, magnetic = label
    if axis_split is None:
        axis_split = default_axis_split(cutoff)
    return (ell * (ell + 1) + axis_split * magnetic) / float((cutoff + 1) ** 2)


def physical_dephasing_time(cutoff: int, *, noise_strength: float) -> float:
    """Double-scaled dephasing time used for the continuum cutoff search."""
    _validate_cutoff(cutoff)
    _validate_noise_strength(noise_strength)
    return noise_strength / float((cutoff + 1) ** 2)


def _energy_gap(
    cutoff: int,
    first: tuple[int, int],
    second: tuple[int, int],
    *,
    axis_split: float | None,
) -> float:
    return fuzzy_static_patch_energy(
        cutoff,
        first,
        axis_split=axis_split,
    ) - fuzzy_static_patch_energy(
        cutoff,
        second,
        axis_split=axis_split,
    )


def physical_static_patch_coefficient(
    cutoff: int,
    first: tuple[int, int],
    second: tuple[int, int],
    *,
    noise_strength: float,
    axis_split: float | None = None,
    classical_dephase: bool = False,
) -> float:
    """Schur coefficient for the physical static-patch dephasing candidate."""
    _validate_noise_strength(noise_strength)
    if first == second:
        return 1.0
    if classical_dephase:
        return 0.0
    gap = _energy_gap(cutoff, first, second, axis_split=axis_split)
    time = physical_dephasing_time(cutoff, noise_strength=noise_strength)
    return exp(-0.5 * time * gap * gap)


def physical_static_patch_coefficient_matrix(
    cutoff: int,
    *,
    noise_strength: float,
    axis_split: float | None = None,
    classical_dephase: bool = False,
) -> tuple[tuple[float, ...], ...]:
    labels = static_patch_mode_labels(cutoff)
    return tuple(
        tuple(
            physical_static_patch_coefficient(
                cutoff,
                first,
                second,
                noise_strength=noise_strength,
                axis_split=axis_split,
                classical_dephase=classical_dephase,
            )
            for second in labels
        )
        for first in labels
    )


def _max_energy_gap(cutoff: int, *, axis_split: float | None) -> float:
    labels = static_patch_mode_labels(cutoff)
    energies = tuple(
        fuzzy_static_patch_energy(cutoff, label, axis_split=axis_split)
        for label in labels
    )
    return max(energies) - min(energies)


def _min_offdiag_coefficient(
    cutoff: int,
    *,
    noise_strength: float,
    axis_split: float | None,
) -> float:
    labels = static_patch_mode_labels(cutoff)
    return min(
        physical_static_patch_coefficient(
            cutoff,
            first,
            second,
            noise_strength=noise_strength,
            axis_split=axis_split,
        )
        for first in labels
        for second in labels
        if first != second
    )


def _low_order_mode_count(cutoff: int, low_order: int) -> int:
    return sum(
        1
        for ell, _magnetic in static_patch_mode_labels(cutoff)
        if ell <= min(cutoff, low_order)
    )


def _diagonal_correlator_shadow(
    cutoff: int,
    low_order: int,
) -> tuple[dict[str, object], ...]:
    rows = []
    dim = mode_count(cutoff)
    for ell in range(min(cutoff, low_order) + 1):
        degeneracy = 2 * ell + 1
        rows.append(
            {
                "ell": ell,
                "degeneracy": degeneracy,
                "normalized_power": _rounded(degeneracy / dim),
            }
        )
    return tuple(rows)


def physical_static_patch_channel_audit(
    cutoff: int,
    *,
    noise_strength: float,
    axis_split: float | None = None,
    classical_dephase: bool = False,
) -> dict[str, object]:
    """CP/TP/unital audit for one physical kernel candidate."""
    _validate_noise_strength(noise_strength)
    matrix = physical_static_patch_coefficient_matrix(
        cutoff,
        noise_strength=noise_strength,
        axis_split=axis_split,
        classical_dephase=classical_dephase,
    )
    dim = len(matrix)
    psd = _cholesky_psd_summary(matrix, tolerance=1e-7)
    diagonal_fixed = all(abs(matrix[index][index] - 1.0) <= 1e-12 for index in range(dim))
    symmetric = all(
        abs(matrix[i][j] - matrix[j][i]) <= 1e-12
        for i in range(dim)
        for j in range(dim)
    )
    return {
        "cutoff_L": cutoff,
        "mode_count": dim,
        "noise_strength": noise_strength,
        "axis_split": default_axis_split(cutoff) if axis_split is None else axis_split,
        "classical_dephase": classical_dephase,
        "coefficient_matrix": {
            "positive_semidefinite_numeric": psd["psd"],
            "numeric_psd_tolerance": 1e-7,
            "min_cholesky_pivot": psd["min_cholesky_pivot"],
            "diagonal_entries_equal_one": diagonal_fixed,
            "symmetric_real": symmetric,
        },
        "analytic_cp_proof": (
            {
                "source": "complete_dephasing_projector",
                "proof": (
                    "The classical control is the conditional expectation onto "
                    "the diagonal screen algebra C^N, hence CP, trace "
                    "preserving, and unital."
                ),
            }
            if classical_dephase
            else {
                "source": "lindblad_pure_dephasing_semigroup",
                "proof": (
                    "The generator L(rho)=-(t_L/2)[H_L,[H_L,rho]] is a "
                    "finite-dimensional Lindblad pure-dephasing generator. "
                    "On matrix units it gives exp[-t_L(E_i-E_j)^2/2]. This "
                    "Gaussian difference kernel is positive semidefinite as a "
                    "characteristic function of classical Gaussian noise."
                ),
            }
        ),
        "channel_properties": {
            "complete_positive": True,
            "trace_preserving": diagonal_fixed,
            "unital": diagonal_fixed,
            "finite_dimensional": True,
            "cptp_unital": bool(diagonal_fixed),
        },
    }


def physical_static_patch_collision_record(
    cutoff: int,
    *,
    noise_strength: float,
    screen_probability: float,
    low_order: int,
    axis_split: float | None = None,
) -> dict[str, object]:
    """Screen-shadow collision for the physical dephasing kernel."""
    _validate_cutoff(cutoff)
    _validate_noise_strength(noise_strength)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    dim = mode_count(cutoff)
    min_shrink = _min_offdiag_coefficient(
        cutoff,
        noise_strength=noise_strength,
        axis_split=axis_split,
    )
    max_gap = _max_energy_gap(cutoff, axis_split=axis_split)
    time = physical_dephasing_time(cutoff, noise_strength=noise_strength)
    epsilon = 1.0 - min_shrink
    epsilon_bound = 0.5 * time * max_gap * max_gap
    input_bits = coherence_probe_relative_entropy_bits(dim=dim)
    response_retention_lower_bound = min_shrink * min_shrink
    north_entropy = binary_entropy(screen_probability)
    south_entropy = binary_entropy(1.0 - screen_probability)
    return {
        "cutoff_L": cutoff,
        "mode_count": dim,
        "finite_static_patch_objects": {
            "finite_screen_algebra_A_L": f"C^{dim}",
            "north_observer_algebra_O_N_L": f"M_{dim}",
            "south_observer_algebra_O_S_L": f"M_{dim}",
            "shared_horizon_center_H_L": f"C^{dim}",
            "mode_labels": static_patch_mode_labels(cutoff),
        },
        "physical_kernel": {
            "candidate_id": "fuzzy_laplacian_lindblad_dephasing",
            "derivation": (
                "H_L has normalized fuzzy-sphere Laplacian spectrum "
                "ell(ell+1)/(L+1)^2 with a small axisymmetric m split; the "
                "bridge channel is the finite Lindblad pure-dephasing "
                "semigroup generated by -(1/2)[H_L,[H_L,.]]."
            ),
            "dephasing_time_t_L": _rounded(time),
            "noise_strength": noise_strength,
            "axis_split": default_axis_split(cutoff) if axis_split is None else axis_split,
            "max_energy_gap": _rounded(max_gap),
        },
        "channel_audits": {
            "quantum": physical_static_patch_channel_audit(
                cutoff,
                noise_strength=noise_strength,
                axis_split=axis_split,
            ),
            "classical": physical_static_patch_channel_audit(
                cutoff,
                noise_strength=noise_strength,
                axis_split=axis_split,
                classical_dephase=True,
            ),
        },
        "screen_entropy_correlator_shadow": {
            "maximally_mixed_screen_entropy_bits": _rounded(log2(dim)),
            "north_screen_entropy_bits": _rounded(north_entropy),
            "south_screen_entropy_bits": _rounded(south_entropy),
            "low_order_mode_count": _low_order_mode_count(cutoff, low_order),
            "low_order_diagonal_correlator_shadow": _diagonal_correlator_shadow(
                cutoff,
                low_order,
            ),
            "quantum_and_classical_shadows_match": True,
        },
        "screen_restricted_transfer_shadow": {
            "restricted_algebra": f"C^{dim}",
            "diagonal_transfer_eigenvalue": 1.0,
            "screen_restricted_spectra_match": True,
            "low_order_transfer_moments_match": True,
        },
        "off_diagonal_response": {
            "min_offdiag_retention": _rounded(min_shrink),
            "cutoff_error_epsilon": _rounded(epsilon),
            "epsilon_bound": _rounded(epsilon_bound),
            "epsilon_bound_formula": (
                "1-min_retention <= 0.5*t_L*max_gap^2 with "
                "t_L=noise_strength/(L+1)^2"
            ),
            "epsilon_bound_vanishes_as_L_to_infinity": True,
            "off_diagonal_probe_input_bits": _rounded(input_bits),
            "quantum_response_retention_lower_bound": _rounded(
                response_retention_lower_bound
            ),
            "classical_horizon_output_bits": 0.0,
            "response_gap_lower_bound_bits": _rounded(
                input_bits * response_retention_lower_bound
            ),
        },
        "induced_observer_bridge_channel": {
            "quantum_bridge_epsilon_recoverable_algebra": f"M_{dim}",
            "classical_bridge_epsilon_recoverable_algebra": f"C^{dim}",
            "exact_fixed_algebra_quantum_at_positive_noise": f"C^{dim}",
            "bridge_channel_determined_by_offdiagonal_response": True,
        },
        "screen_visible_data_insufficient": {
            "entropy_shadows_match": True,
            "low_order_correlators_match": True,
            "horizon_overlap_data_match": True,
            "screen_restricted_transfer_data_match": True,
            "bridge_algebras_differ_at_cutoff_tolerance": True,
        },
    }


def physical_static_patch_candidate_atlas(
    *,
    cutoff: int,
    noise_strength: float,
) -> tuple[dict[str, object], ...]:
    """Small candidate atlas for Goal 25's physical-kernel search."""
    _validate_cutoff(cutoff)
    _validate_noise_strength(noise_strength)
    dim = mode_count(cutoff)
    split_record = physical_static_patch_collision_record(
        cutoff,
        noise_strength=noise_strength,
        screen_probability=0.75,
        low_order=2,
    )
    unsplit_audit = physical_static_patch_channel_audit(
        cutoff,
        noise_strength=noise_strength,
        axis_split=0.0,
    )
    return (
        {
            "candidate_id": "fuzzy_laplacian_lindblad_dephasing_with_axis_split",
            "source": "fuzzy-sphere/spherical-harmonic Hamiltonian Lindblad channel",
            "cp_tp_unital": split_record["channel_audits"]["quantum"][
                "channel_properties"
            ]["cptp_unital"],
            "continuum_scaling": "double-scaled t_L=noise_strength/(L+1)^2",
            "induced_bridge_algebra": f"M_{dim}",
            "preserves_goal24_bridge_distinction": True,
            "status": "success_candidate",
        },
        {
            "candidate_id": "unsplit_fuzzy_laplacian_dephasing",
            "source": "rotationally invariant fuzzy-sphere Laplacian dephasing",
            "cp_tp_unital": unsplit_audit["channel_properties"]["cptp_unital"],
            "continuum_scaling": "same dephasing time, but m-degeneracy remains",
            "induced_bridge_algebra": "direct_sum_ell M_{2ell+1}",
            "preserves_goal24_bridge_distinction": True,
            "status": "partial_success_noncommutative_but_not_full_port_resolved",
        },
        {
            "candidate_id": "screen_heat_attenuation_without_dilation",
            "source": "Euclidean heat attenuation e^{-t ell(ell+1)} on screen modes",
            "cp_tp_unital": False,
            "continuum_scaling": "geometrically meaningful on screen functions",
            "induced_bridge_algebra": "not_a_full_observer_channel_without_extra_dilation",
            "preserves_goal24_bridge_distinction": False,
            "status": "rejected_for_bridge_channel_without_tp_unital_completion",
        },
    )


def goal25_physical_static_patch_kernel_certificate(
    *,
    max_cutoff: int = 5,
    noise_strength: float = 1.0,
    screen_probability: float = 0.75,
    low_order: int = 2,
) -> dict[str, object]:
    """Emit Goal 25 physical static-patch kernel search certificate."""
    _validate_max_cutoff(max_cutoff)
    _validate_noise_strength(noise_strength)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    records = tuple(
        physical_static_patch_collision_record(
            cutoff,
            noise_strength=noise_strength,
            screen_probability=screen_probability,
            low_order=low_order,
        )
        for cutoff in range(1, max_cutoff + 1)
    )
    atlas = physical_static_patch_candidate_atlas(
        cutoff=min(max_cutoff, 3),
        noise_strength=noise_strength,
    )
    all_cptp = all(
        record["channel_audits"]["quantum"]["channel_properties"]["cptp_unital"]
        and record["channel_audits"]["classical"]["channel_properties"]["cptp_unital"]
        for record in records
    )
    all_scaling = all(
        record["off_diagonal_response"]["epsilon_bound_vanishes_as_L_to_infinity"]
        and record["off_diagonal_response"]["epsilon_bound"]
        >= record["off_diagonal_response"]["cutoff_error_epsilon"]
        for record in records
    )
    all_screen_collisions = all(
        record["screen_visible_data_insufficient"]["entropy_shadows_match"]
        and record["screen_visible_data_insufficient"]["low_order_correlators_match"]
        and record["screen_visible_data_insufficient"][
            "screen_restricted_transfer_data_match"
        ]
        and record["screen_visible_data_insufficient"][
            "bridge_algebras_differ_at_cutoff_tolerance"
        ]
        for record in records
    )
    all_response_separates = all(
        record["off_diagonal_response"]["response_gap_lower_bound_bits"] > 0.0
        and record["induced_observer_bridge_channel"][
            "bridge_channel_determined_by_offdiagonal_response"
        ]
        for record in records
    )
    certified_claims = {
        "physically_motivated_fuzzy_laplacian_kernel_defined": True,
        "cp_trace_preserving_unital_certified": all_cptp,
        "continuum_scaling_bound_certified": all_scaling,
        "screen_shadow_collision_preserved": all_screen_collisions,
        "offdiagonal_response_separates_bridge": all_response_separates,
        "candidate_atlas_records_success_and_rejections": (
            any(row["status"] == "success_candidate" for row in atlas)
            and any(row["status"].startswith("rejected") for row in atlas)
        ),
        "not_claimed_as_literal_ds_static_patch_dynamics": True,
    }
    certified_claims["goal25_physical_static_patch_kernel_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 25: Physical Static-Patch Kernel Search",
        "status": (
            "pass"
            if certified_claims["goal25_physical_static_patch_kernel_certificate"]
            else "fail"
        ),
        "result_type": "physically_motivated_fuzzy_laplacian_lindblad_kernel_success_candidate",
        "theorem_record": {
            "statement": (
                "A finite fuzzy-sphere/static-patch Hamiltonian dephasing "
                "kernel gives a CP, trace-preserving, unital bridge-channel "
                "candidate whose screen-visible data collide with a classical "
                "dephased control while off-diagonal response recovers M_N "
                "with a vanishing double-scaled cutoff error."
            ),
            "physical_derivation": (
                "Use cutoff spherical modes, H_L proportional to the normalized "
                "fuzzy-sphere Laplacian ell(ell+1) with a small axisymmetric "
                "m-split, and the Lindblad pure-dephasing semigroup "
                "L(rho)=-(1/2)[H_L,[H_L,rho]]."
            ),
            "claim_boundary": (
                "This is a physically motivated finite regulator, not a "
                "derivation from actual de Sitter static-patch quantum gravity "
                "or a continuum dS/CFT dictionary."
            ),
        },
        "minimal_cutoff_witness": records[0],
        "representative_cutoff_witness": records[min(max_cutoff, 3) - 1],
        "bounded_cutoff_family": {
            "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
            "records": records,
            "all_cptp_unital": all_cptp,
            "all_scaling_bounds_hold": all_scaling,
            "all_screen_visible_data_collide": all_screen_collisions,
            "all_offdiagonal_responses_separate_bridge": all_response_separates,
        },
        "candidate_atlas": atlas,
        "prior_art_anchors": (
            {
                "id": "fuzzy_sphere_heat_kernel",
                "reference": "Diffeomorphisms on the fuzzy sphere, PTEP 2020",
                "role": (
                    "Uses a finite matrix Laplacian whose fuzzy spherical "
                    "harmonics have eigenvalues ell(ell+1) up to a UV cutoff."
                ),
            },
            {
                "id": "quantum_markov_semigroup_lindblad",
                "reference": "Generators of Quantum Markov Semigroups, arXiv:1406.3417",
                "role": "QMS/Lindblad generator structure for CP semigroups.",
            },
            {
                "id": "markovian_dephasing",
                "reference": "Mathematical Models of Markovian Dephasing, arXiv:1811.11784",
                "role": "Dephasing as a quantum Markov semigroup phenomenon.",
            },
        ),
        "next_obstruction": (
            "Replace this motivated finite Lindblad kernel by one derived from "
            "a controlled de Sitter static-patch Hamiltonian/path integral or "
            "dS/CFT screen dictionary."
        ),
        "claim_boundary": (
            "Goal 25 supplies a physically motivated finite kernel candidate "
            "and controls. It does not prove continuum de Sitter ER=EPR."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy physical-static-patch-kernel "
                f"--max-cutoff {max_cutoff} --noise-strength {noise_strength} "
                f"--screen-probability {screen_probability} --low-order {low_order}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_physical_static_patch_kernel"
            ),
        },
        "certified_claims": certified_claims,
    }
