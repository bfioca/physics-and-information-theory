"""Finite-size compact rotation observer in a de Sitter static patch.

The observer is a marked spherical top with orientation ``Q in SO(3)`` and
proper-time action

    S = integral d tau [-m + I |Q^{-1} D_tau Q|^2 / 2],
    I = kappa m a^2.

Quantization gives ``L^2(SO(3))`` and ``H_rot=C_left/(2I)``.  Declared mean
compactness and excitation bounds limit the mean Casimir.  Markov truncation,
gentle measurement, and the exact finite-multiplicity obstruction then give an
any-decoder recovery lower bound for every admissible rotor state under the
fixed append-and-twirl channel.

This is a compact ``SO(3)`` worldtube EFT with a semiclassical compactness
hypothesis, not a full rotating Einstein-matter solution or ``SO(1,d)`` model.
"""

from __future__ import annotations

from math import floor, isfinite, sqrt

from .redshifted_frame_capacity import (
    angular_cutoff_asymptotic_coefficient,
    maximum_bounded_energy_angular_momentum,
    stretched_horizon_proper_distance,
)
from .redshifted_rotation_reference_tradeoff import (
    peter_weyl_constructive_diamond_upper_bound,
    sufficient_peter_weyl_reference_cutoff,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_fraction(name: str, value: float, *, inclusive_one: bool) -> None:
    _validate_positive(name, value)
    if value > 1.0 or (not inclusive_one and value == 1.0):
        endpoint = "at most" if inclusive_one else "smaller than"
        raise ValueError(f"{name} must be {endpoint} one")


def _validate_cutoff(reference_cutoff: int) -> None:
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")


def _validate_inertia_coefficient(value: float) -> None:
    _validate_positive("inertia_coefficient", value)
    if value > 2.0 / 3.0:
        raise ValueError("inertia_coefficient must be at most two thirds")


def spherical_top_mean_rotor_load(reference_cutoff: int) -> float:
    """Return ``s_J`` in ``<H_rot>=s_J/I`` for the canonical token."""
    _validate_cutoff(reference_cutoff)
    return 3.0 * reference_cutoff * (reference_cutoff + 2) / 10.0


def spherical_top_peak_rotor_load(reference_cutoff: int) -> float:
    """Return ``s_J`` in the top occupied-sector energy ``E_J=s_J/I``."""
    _validate_cutoff(reference_cutoff)
    return reference_cutoff * (reference_cutoff + 1) / 2.0


def minimum_rest_energy_for_cutoff(
    reference_cutoff: int,
    *,
    observer_radius: float,
    inertia_coefficient: float,
    maximum_excitation_fraction: float,
) -> float:
    """Minimum rest energy when ``E_rot/m <= zeta <= 1``.

    With ``I=kappa m a^2`` and ``E_rot=s_J/I``, the excitation constraint
    requires ``m >= sqrt(s_J/(kappa zeta a^2))``.
    """
    _validate_cutoff(reference_cutoff)
    _validate_positive("observer_radius", observer_radius)
    _validate_inertia_coefficient(inertia_coefficient)
    _validate_fraction(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
        inclusive_one=True,
    )
    load = spherical_top_mean_rotor_load(reference_cutoff)
    if load == 0.0:
        return 0.0
    return sqrt(
        load
        / (
            inertia_coefficient
            * maximum_excitation_fraction
            * observer_radius**2
        )
    )


def minimum_total_observer_energy_for_cutoff(
    reference_cutoff: int,
    *,
    observer_radius: float,
    inertia_coefficient: float,
    maximum_excitation_fraction: float,
) -> float:
    """Minimum ``m+E_rot`` compatible with the excitation-fraction cap."""
    rest_energy = minimum_rest_energy_for_cutoff(
        reference_cutoff,
        observer_radius=observer_radius,
        inertia_coefficient=inertia_coefficient,
        maximum_excitation_fraction=maximum_excitation_fraction,
    )
    return (1.0 + maximum_excitation_fraction) * rest_energy


def minimum_total_observer_energy_for_spectral_cutoff(
    reference_cutoff: int,
    *,
    observer_radius: float,
    inertia_coefficient: float,
    maximum_excitation_fraction: float,
) -> float:
    """Minimum total energy when every occupied sector through ``J`` is safe."""
    _validate_cutoff(reference_cutoff)
    _validate_positive("observer_radius", observer_radius)
    _validate_inertia_coefficient(inertia_coefficient)
    _validate_fraction(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
        inclusive_one=True,
    )
    load = spherical_top_peak_rotor_load(reference_cutoff)
    if load == 0.0:
        return 0.0
    rest_energy = sqrt(
        load
        / (
            inertia_coefficient
            * maximum_excitation_fraction
            * observer_radius**2
        )
    )
    return (1.0 + maximum_excitation_fraction) * rest_energy


def compactness_energy_capacity(
    *,
    observer_radius: float,
    newton_constant: float,
    compactness_margin: float,
) -> float:
    """Energy ceiling from the declared local bound ``2 G E/a <= chi``."""
    _validate_positive("observer_radius", observer_radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_fraction("compactness_margin", compactness_margin, inclusive_one=False)
    return compactness_margin * observer_radius / (2.0 * newton_constant)


def maximum_mean_casimir_from_compactness(
    *,
    observer_radius: float,
    newton_constant: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> float:
    """Maximum mean ``<C_left>`` under the declared energy inequalities."""
    _validate_positive("observer_radius", observer_radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_inertia_coefficient(inertia_coefficient)
    _validate_fraction("compactness_margin", compactness_margin, inclusive_one=False)
    _validate_fraction(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
        inclusive_one=True,
    )
    zeta = maximum_excitation_fraction
    return (
        inertia_coefficient
        * compactness_margin**2
        * zeta
        * observer_radius**4
        / (2.0 * newton_constant**2 * (1.0 + zeta) ** 2)
    )


def maximum_finite_size_reference_cutoff(
    *,
    observer_radius: float,
    newton_constant: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> int:
    """Largest spectrally safe occupied spin under branchwise compactness."""
    _validate_positive("observer_radius", observer_radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_inertia_coefficient(inertia_coefficient)
    _validate_fraction("compactness_margin", compactness_margin, inclusive_one=False)
    _validate_fraction(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
        inclusive_one=True,
    )
    zeta = maximum_excitation_fraction
    bound = (
        inertia_coefficient
        * compactness_margin**2
        * zeta
        * observer_radius**4
        / (2.0 * newton_constant**2 * (1.0 + zeta) ** 2)
    )
    return max(0, floor((sqrt(1.0 + 4.0 * bound) - 1.0) / 2.0))


def maximum_canonical_mean_energy_cutoff(
    *,
    observer_radius: float,
    newton_constant: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> int:
    """Largest canonical hard cutoff allowed by mean-energy compactness only."""
    _validate_positive("observer_radius", observer_radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_inertia_coefficient(inertia_coefficient)
    _validate_fraction("compactness_margin", compactness_margin, inclusive_one=False)
    _validate_fraction(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
        inclusive_one=True,
    )
    zeta = maximum_excitation_fraction
    bound = (
        5.0
        * inertia_coefficient
        * compactness_margin**2
        * zeta
        * observer_radius**4
        / (6.0 * newton_constant**2 * (1.0 + zeta) ** 2)
    )
    return max(0, floor(sqrt(1.0 + bound) - 1.0))


def peter_weyl_any_decoder_error_lower_bound(
    system_spin: int,
    reference_cutoff: int,
) -> float:
    """Multiplicity lower bound for a Peter-Weyl reference through ``J``.

    The total available reference multiplicity is ``sum_(j<=J)(2j+1)=(J+1)^2``.
    Hence the maximum joint multiplicity is no larger than this number.  For
    ``L>=J`` it is attained in the total-spin ``K=L`` block.
    """
    if isinstance(system_spin, bool) or not isinstance(system_spin, int) or system_spin < 1:
        raise ValueError("system_spin must be a positive integer")
    _validate_cutoff(reference_cutoff)
    system_dimension = 2 * system_spin + 1
    multiplicity_upper_bound = (reference_cutoff + 1) ** 2
    return max(0.0, 1.0 - multiplicity_upper_bound / float(system_dimension))


def energy_constrained_rotor_recovery_bound_record(
    system_spin: int,
    *,
    maximum_mean_casimir: float,
) -> dict[str, object]:
    """Any-decoder bound for every rotor state with bounded mean Casimir.

    Project the reference to spins ``j<=J``.  The tail probability is at most
    ``Cbar/[(J+1)(J+2)]``.  When the projected weight is positive, the normalized
    conditional state is within trace distance ``sqrt(q)`` by the fidelity
    bound. Candidates whose tail bound reaches one give no positive transferred
    lower bound and are discarded by clipping. Contractivity then transfers the
    finite-multiplicity obstruction to the original append-and-twirl channel.
    """
    if isinstance(system_spin, bool) or not isinstance(system_spin, int) or system_spin < 1:
        raise ValueError("system_spin must be a positive integer")
    if not isfinite(maximum_mean_casimir) or maximum_mean_casimir < 0.0:
        raise ValueError("maximum_mean_casimir must be finite and nonnegative")
    system_dimension = 2 * system_spin + 1
    maximum_useful_cutoff = max(0, floor(sqrt(float(system_dimension))) - 1)
    candidates = []
    for cutoff in range(maximum_useful_cutoff + 1):
        tail_bound = min(
            1.0,
            maximum_mean_casimir / ((cutoff + 1.0) * (cutoff + 2.0)),
        )
        multiplicity_deficit = 1.0 - (cutoff + 1) ** 2 / float(system_dimension)
        lower_bound = max(0.0, multiplicity_deficit - sqrt(tail_bound))
        candidates.append(
            {
                "truncation_spin_J": cutoff,
                "casimir_tail_probability_upper_bound": tail_bound,
                "gentle_trace_distance_upper_bound": sqrt(tail_bound),
                "finite_multiplicity_error_lower_bound": max(
                    0.0,
                    multiplicity_deficit,
                ),
                "transferred_error_lower_bound": lower_bound,
            }
        )
    optimizer = max(
        candidates,
        key=lambda candidate: candidate["transferred_error_lower_bound"],
    )
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": system_dimension,
        "maximum_mean_left_casimir": maximum_mean_casimir,
        "optimized_truncation_spin_J": optimizer["truncation_spin_J"],
        "normalized_diamond_error_lower_bound": optimizer[
            "transferred_error_lower_bound"
        ],
        "optimizer_record": optimizer,
        "bound_formula": (
            "max_J max(0,1-(J+1)^2/d-"
            "sqrt(Cbar/((J+1)(J+2))))"
        ),
        "uniform_asymptotic_deficit": "O(1/d+(Cbar/d)^(1/3))",
        "scope": (
            "all prepared states on L2(SO(3)) with mean Casimir at most Cbar, "
            "followed by the fixed append-and-twirl channel and any deterministic "
            "CPTP decoder"
        ),
    }


def minimum_cutoff_meeting_constructive_bound(
    system_spin: int,
    target_error: float,
) -> int:
    """Smallest ``J>=L`` whose existing constructive upper bound is <= epsilon."""
    if isinstance(system_spin, bool) or not isinstance(system_spin, int) or system_spin < 1:
        raise ValueError("system_spin must be a positive integer")
    _validate_positive("target_error", target_error)
    if target_error >= 1.0:
        raise ValueError("target_error must be smaller than one")
    low = system_spin
    high = sufficient_peter_weyl_reference_cutoff(system_spin, target_error)
    while low < high:
        middle = (low + high) // 2
        if (
            peter_weyl_constructive_diamond_upper_bound(system_spin, middle)
            <= target_error
        ):
            high = middle
        else:
            low = middle + 1
    return low


def collar_constructive_gap_floor_asymptotic(
    *,
    radius: float,
    newton_constant: float,
    field_energy_budget: float,
    inner_offset: float,
    outer_offset: float,
    target_recovery_error: float,
    collar_size_fraction: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> dict[str, float]:
    """Leading protocol-feasibility scale for ``a=alpha rho_delta``.

    This equates the sufficient asymptotic Peter-Weyl cutoff with the finite-size
    capacity.  It is not a necessary optimal-recovery threshold.
    """
    _validate_positive("radius", radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_positive("target_recovery_error", target_recovery_error)
    _validate_fraction("collar_size_fraction", collar_size_fraction, inclusive_one=True)
    _validate_inertia_coefficient(inertia_coefficient)
    _validate_fraction("compactness_margin", compactness_margin, inclusive_one=False)
    _validate_fraction(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
        inclusive_one=True,
    )
    if target_recovery_error >= 1.0:
        raise ValueError("target_recovery_error must be smaller than one")
    angular_coefficient = angular_cutoff_asymptotic_coefficient(
        radius=radius,
        energy_budget=field_energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    zeta = maximum_excitation_fraction
    cutoff_capacity_coefficient = compactness_margin * sqrt(
        inertia_coefficient * zeta / (2.0 * (1.0 + zeta) ** 2)
    )
    gap_floor = sqrt(
        3.0
        * angular_coefficient
        * newton_constant
        / (
            4.0
            * cutoff_capacity_coefficient
            * collar_size_fraction**2
            * target_recovery_error
        )
    )
    proper_floor = sqrt(2.0 * radius * gap_floor)
    return {
        "angular_cutoff_coefficient_C": angular_coefficient,
        "finite_size_cutoff_coefficient": cutoff_capacity_coefficient,
        "asymptotic_coordinate_gap_floor_delta": gap_floor,
        "asymptotic_proper_distance_floor_rho": proper_floor,
        "proper_distance_floor_in_planck_lengths": proper_floor
        / sqrt(newton_constant),
    }


def finite_size_static_patch_observer_record(
    *,
    radius: float,
    stretched_distance: float,
    newton_constant: float,
    field_energy_budget: float,
    inner_offset: float,
    outer_offset: float,
    target_recovery_error: float,
    fixed_observer_radius: float,
    collar_size_fraction: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> dict[str, object]:
    """Compare fixed-size and collar-following finite observer capacities."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    _validate_positive("fixed_observer_radius", fixed_observer_radius)
    _validate_fraction("collar_size_fraction", collar_size_fraction, inclusive_one=True)
    if fixed_observer_radius >= radius:
        raise ValueError("fixed_observer_radius must be smaller than radius")
    proper_distance = stretched_horizon_proper_distance(
        radius=radius,
        stretched_distance=stretched_distance,
    )
    collar_radius = collar_size_fraction * proper_distance
    if collar_radius >= radius:
        raise ValueError("collar-following observer radius must be smaller than radius")
    target_spin = maximum_bounded_energy_angular_momentum(
        radius=radius,
        stretched_distance=stretched_distance,
        energy_budget=field_energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    if target_spin < 1:
        raise ValueError("parameters must certify at least one nontrivial spin sector")
    constructive_cutoff = minimum_cutoff_meeting_constructive_bound(
        target_spin,
        target_recovery_error,
    )

    def observer_record(observer_radius: float) -> dict[str, object]:
        maximum_mean_casimir = maximum_mean_casimir_from_compactness(
            observer_radius=observer_radius,
            newton_constant=newton_constant,
            inertia_coefficient=inertia_coefficient,
            compactness_margin=compactness_margin,
            maximum_excitation_fraction=maximum_excitation_fraction,
        )
        energy_constrained_bound = energy_constrained_rotor_recovery_bound_record(
            target_spin,
            maximum_mean_casimir=maximum_mean_casimir,
        )
        maximum_spectral_cutoff = maximum_finite_size_reference_cutoff(
            observer_radius=observer_radius,
            newton_constant=newton_constant,
            inertia_coefficient=inertia_coefficient,
            compactness_margin=compactness_margin,
            maximum_excitation_fraction=maximum_excitation_fraction,
        )
        maximum_mean_cutoff = maximum_canonical_mean_energy_cutoff(
            observer_radius=observer_radius,
            newton_constant=newton_constant,
            inertia_coefficient=inertia_coefficient,
            compactness_margin=compactness_margin,
            maximum_excitation_fraction=maximum_excitation_fraction,
        )
        return {
            "observer_proper_radius_a": observer_radius,
            "maximum_spectrally_safe_occupied_spin_J": maximum_spectral_cutoff,
            "maximum_canonical_mean_energy_cutoff_J": maximum_mean_cutoff,
            "maximum_mean_left_casimir_from_compactness": maximum_mean_casimir,
            "energy_constrained_any_decoder_bound": energy_constrained_bound,
            "any_decoder_normalized_diamond_error_lower_bound": (
                energy_constrained_bound["normalized_diamond_error_lower_bound"]
            ),
            "constructive_cutoff_is_admissible": constructive_cutoff
            <= maximum_spectral_cutoff,
            "minimum_spectral_total_energy_at_constructive_cutoff": (
                minimum_total_observer_energy_for_spectral_cutoff(
                    constructive_cutoff,
                    observer_radius=observer_radius,
                    inertia_coefficient=inertia_coefficient,
                    maximum_excitation_fraction=maximum_excitation_fraction,
                )
            ),
            "compactness_energy_capacity": compactness_energy_capacity(
                observer_radius=observer_radius,
                newton_constant=newton_constant,
                compactness_margin=compactness_margin,
            ),
        }

    return {
        "de_sitter_radius_R": radius,
        "stretched_horizon_gap_delta": stretched_distance,
        "horizon_proper_distance_rho": proper_distance,
        "planck_length_sqrt_G": sqrt(newton_constant),
        "hard_energy_target_spin_L_delta": target_spin,
        "target_dimension_2L_plus_1": 2 * target_spin + 1,
        "minimum_cutoff_meeting_constructive_error_bound": constructive_cutoff,
        "constructive_error_target_epsilon": target_recovery_error,
        "fixed_size_observer": observer_record(fixed_observer_radius),
        "collar_following_observer": observer_record(collar_radius),
    }


def finite_size_static_patch_observer_certificate(
    *,
    radius: float = 1.0,
    newton_constant: float = 1e-6,
    field_energy_budget: float = 4.0,
    inner_offset: float = 0.5,
    outer_offset: float = 1.5,
    target_recovery_error: float = 0.1,
    fixed_observer_radius: float = 0.05,
    collar_size_fraction: float = 0.25,
    inertia_coefficient: float = 2.0 / 3.0,
    compactness_margin: float = 0.5,
    maximum_excitation_fraction: float = 0.25,
    minimum_power: int = 64,
    steps: int = 9,
) -> dict[str, object]:
    """Audit the finite-size compact observer obstruction and protocol ceiling."""
    if (
        isinstance(minimum_power, bool)
        or not isinstance(minimum_power, int)
        or minimum_power < 16
    ):
        raise ValueError("minimum_power must be an integer at least sixteen")
    if (
        isinstance(steps, bool)
        or not isinstance(steps, int)
        or steps < 4
        or steps > 32
    ):
        raise ValueError("steps must be an integer from four through thirty-two")
    records = tuple(
        finite_size_static_patch_observer_record(
            radius=radius,
            stretched_distance=radius / float(minimum_power * 4**index),
            newton_constant=newton_constant,
            field_energy_budget=field_energy_budget,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
            target_recovery_error=target_recovery_error,
            fixed_observer_radius=fixed_observer_radius,
            collar_size_fraction=collar_size_fraction,
            inertia_coefficient=inertia_coefficient,
            compactness_margin=compactness_margin,
            maximum_excitation_fraction=maximum_excitation_fraction,
        )
        for index in range(steps)
    )
    collar_errors = tuple(
        record["collar_following_observer"][
            "any_decoder_normalized_diamond_error_lower_bound"
        ]
        for record in records
    )
    fixed_capacities = tuple(
        record["fixed_size_observer"][
            "maximum_spectrally_safe_occupied_spin_J"
        ]
        for record in records
    )
    collar_capacities = tuple(
        record["collar_following_observer"][
            "maximum_spectrally_safe_occupied_spin_J"
        ]
        for record in records
    )
    constructive_feasibility = tuple(
        record["collar_following_observer"]["constructive_cutoff_is_admissible"]
        for record in records
    )
    feasible_indices = tuple(
        index for index, feasible in enumerate(constructive_feasibility) if feasible
    )
    infeasible_indices = tuple(
        index for index, feasible in enumerate(constructive_feasibility) if not feasible
    )
    transition_is_ordered = (
        bool(feasible_indices)
        and bool(infeasible_indices)
        and max(feasible_indices) < min(infeasible_indices)
    )
    asymptotic = collar_constructive_gap_floor_asymptotic(
        radius=radius,
        newton_constant=newton_constant,
        field_energy_budget=field_energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
        target_recovery_error=target_recovery_error,
        collar_size_fraction=collar_size_fraction,
        inertia_coefficient=inertia_coefficient,
        compactness_margin=compactness_margin,
        maximum_excitation_fraction=maximum_excitation_fraction,
    )
    certified_claims = {
        "fixed_size_observer_has_wall_independent_finite_cutoff": len(
            set(fixed_capacities)
        )
        == 1,
        "collar_following_cutoff_decreases_under_wall_removal": all(
            right <= left
            for left, right in zip(collar_capacities, collar_capacities[1:])
        ),
        "collar_any_decoder_obstruction_grows": all(
            right >= left for left, right in zip(collar_errors, collar_errors[1:])
        ),
        "sampled_collar_error_exceeds_0_99_at_requested_depth": (
            collar_errors[-1] > 0.99
        ),
        "constructive_protocol_crosses_from_feasible_to_infeasible": (
            transition_is_ordered
            and all(
                left >= right
                for left, right in zip(
                    constructive_feasibility,
                    constructive_feasibility[1:],
                )
            )
        ),
        "asymptotic_protocol_floor_is_above_planck_length": asymptotic[
            "proper_distance_floor_in_planck_lengths"
        ]
        > 1.0,
        "sampled_transition_brackets_asymptotic_gap_floor": (
            transition_is_ordered
            and records[min(infeasible_indices)]["stretched_horizon_gap_delta"]
            < asymptotic["asymptotic_coordinate_gap_floor_delta"]
            < records[max(feasible_indices)]["stretched_horizon_gap_delta"]
        ),
    }
    return {
        "goal": "Finite-Size Static-Patch Rotation Observer",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "finite_size_rotation_reference_obstruction",
        "certificate_scope": (
            "status combines exact formula checks with evidence on the requested "
            "finite wall-removal sample; changing sample depth can change sampled "
            "threshold claims without changing the analytic theorem"
        ),
        "central_result": (
            "The spherical-top action fixes H_rot=C_left/(2 kappa m a^2). "
            "Mean excitation and compactness bounds imply "
            "<C_left><=kappa chi^2 zeta a^4/[2G^2(1+zeta)^2]. Truncating an "
            "arbitrary rotor state at spin J, Markov plus gentle measurement "
            "transfer the finite Peter-Weyl multiplicity theorem to give error "
            "at least max_J[1-(J+1)^2/(2L+1)-"
            "sqrt(Cbar/((J+1)(J+2)))], clipped at zero."
        ),
        "constructive_protocol_consequence": (
            "For a collar-following apparatus a=alpha rho_delta, the existing "
            "Peter-Weyl decoder's sufficient cutoff eventually exceeds the "
            "finite-size capacity. Its leading coordinate threshold is of order "
            "sqrt(G/epsilon), while the proper threshold is of order "
            "sqrt(R sqrt(G)) epsilon^(-1/4), with declared model constants."
        ),
        "claim_boundary": (
            "compact SO(3), marked spherical-top rest-frame EFT with stipulated "
            "I=kappa m a^2, positive rest and mean rotor energies, declared "
            "compactness and excitation-fraction bounds, full L2(SO(3)) reference, "
            "fixed append-and-twirl channel, and hard-energy free-"
            "field target. This is not a rotating Einstein-matter solution, an "
            "optimal reference theorem, a local interaction/lifetime result, a "
            "noncompact SO(1,d) construction, or a Type-II/generalized-entropy "
            "identity. The any-decoder bound excludes pre-correlated encoders, "
            "postselection, other representations/hardware, and finite-time "
            "evolution during the one-shot protocol; a separate module treats "
            "conditional collective Markov rotation diffusion."
        ),
        "certified_claims": certified_claims,
        "asymptotic_collar_protocol_floor": asymptotic,
        "records": records,
        "next_physics_gate": (
            "derive a local field-top interaction and finite-time decoder, replace "
            "the compactness hypothesis by a controlled Einstein-matter solution, "
            "and add the noncompact boost/clock sector"
        ),
    }
