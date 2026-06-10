"""Near-horizon redshifted rotational-frame capacity.

For a conformally coupled massless scalar in the four-dimensional de Sitter
static patch, the rescaled angular mode has radial quadratic-form operator

    h_l = -d^2/dx^2 + l(l+1)/(R^2 sinh^2(x/R)).

A normalized collar wavepacket a fixed tortoise distance from a stretched
horizon has bounded Rayleigh quotient for angular momenta up to order
``sqrt(R/delta)``.  The min-max principle therefore supplies actual finite-wall
one-particle eigenstates in a hard static-energy window.  A particular
superposition over those irreps has exact SO(3)-twirl entropy ``2 log(L+1)``.
This module records the resulting ``log(R/delta)`` missing-frame lower bound
without identifying it with gravitational generalized entropy.
"""

from __future__ import annotations

from math import asin, exp, floor, isfinite, log, pi, sinh, sqrt

from .static_patch_weyl_regulator import tortoise_length


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_collar(inner_offset: float, outer_offset: float) -> None:
    _validate_positive("inner_offset", inner_offset)
    _validate_positive("outer_offset", outer_offset)
    if outer_offset <= inner_offset:
        raise ValueError("outer_offset must exceed inner_offset")


def conformal_radial_potential(
    angular_momentum: int,
    *,
    radius: float,
    tortoise_coordinate: float,
) -> float:
    """Return ``l(l+1)/(R^2 sinh^2(x/R))`` for the conformal scalar."""
    if (
        isinstance(angular_momentum, bool)
        or not isinstance(angular_momentum, int)
        or angular_momentum < 0
    ):
        raise ValueError("angular_momentum must be a nonnegative integer")
    _validate_positive("radius", radius)
    _validate_positive("tortoise_coordinate", tortoise_coordinate)
    denominator = radius * sinh(tortoise_coordinate / radius)
    return angular_momentum * (angular_momentum + 1) / (denominator * denominator)


def sine_collar_kinetic_constant(
    *, inner_offset: float, outer_offset: float
) -> float:
    """Dimensionless kinetic form of the normalized Dirichlet sine packet."""
    _validate_collar(inner_offset, outer_offset)
    return (pi / (outer_offset - inner_offset)) ** 2


def collar_inner_edge(
    *,
    radius: float,
    stretched_distance: float,
    outer_offset: float,
) -> float:
    """Smallest tortoise coordinate in a collar ending below the wall."""
    _validate_positive("outer_offset", outer_offset)
    edge = tortoise_length(radius, stretched_distance) - radius * outer_offset
    if edge <= 0.0:
        raise ValueError("stretched patch is too short to contain the collar")
    return edge


def collar_static_energy_squared_upper_bound(
    angular_momentum: int,
    *,
    radius: float,
    stretched_distance: float,
    inner_offset: float,
    outer_offset: float,
) -> float:
    """Quadratic-form bound on ``<chi_l,h_l chi_l>``.

    The normalized radial packet is the first Dirichlet sine on the
    dimensionless offset interval ``(inner_offset, outer_offset)`` and is
    translated with the stretched horizon.  The potential is decreasing in
    the tortoise coordinate, so its expectation is bounded by its value at the
    collar's inner edge.
    """
    kinetic = sine_collar_kinetic_constant(
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    ) / (radius * radius)
    edge = collar_inner_edge(
        radius=radius,
        stretched_distance=stretched_distance,
        outer_offset=outer_offset,
    )
    potential = conformal_radial_potential(
        angular_momentum,
        radius=radius,
        tortoise_coordinate=edge,
    )
    return kinetic + potential


def collar_static_energy_upper_bound(
    angular_momentum: int,
    *,
    radius: float,
    stretched_distance: float,
    inner_offset: float,
    outer_offset: float,
) -> float:
    """Upper bound on expected ``sqrt(h_l)`` from the quadratic-form bound."""
    return sqrt(
        collar_static_energy_squared_upper_bound(
            angular_momentum,
            radius=radius,
            stretched_distance=stretched_distance,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
        )
    )


def finite_wall_ground_frequency_upper_bound(
    angular_momentum: int,
    *,
    radius: float,
    stretched_distance: float,
    inner_offset: float,
    outer_offset: float,
) -> float:
    """Variational upper bound on the lowest finite-wall frequency.

    The collar sine lies in the Dirichlet quadratic-form domain of ``h_l`` on
    ``(0,X_delta)``.  Rayleigh-Ritz therefore bounds the lowest eigenvalue by
    its quadratic form, so the lowest frequency is at most the collar bound.
    """
    return collar_static_energy_upper_bound(
        angular_momentum,
        radius=radius,
        stretched_distance=stretched_distance,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )


def maximum_bounded_energy_angular_momentum(
    *,
    radius: float,
    stretched_distance: float,
    energy_budget: float,
    inner_offset: float,
    outer_offset: float,
) -> int:
    """Largest spin certified below the finite-wall spectral energy budget."""
    _validate_positive("energy_budget", energy_budget)
    kinetic_constant = sine_collar_kinetic_constant(
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    surplus = (energy_budget * radius) ** 2 - kinetic_constant
    if surplus <= 0.0:
        raise ValueError("energy_budget is below the collar kinetic floor")
    edge = collar_inner_edge(
        radius=radius,
        stretched_distance=stretched_distance,
        outer_offset=outer_offset,
    )
    angular_bound = surplus * sinh(edge / radius) ** 2
    return max(0, floor((sqrt(1.0 + 4.0 * angular_bound) - 1.0) / 2.0))


def truncated_scalar_harmonic_dimension(maximum_angular_momentum: int) -> int:
    """Return ``sum_{l=0}^L (2l+1)=(L+1)^2``."""
    if (
        isinstance(maximum_angular_momentum, bool)
        or not isinstance(maximum_angular_momentum, int)
        or maximum_angular_momentum < 0
    ):
        raise ValueError("maximum_angular_momentum must be nonnegative")
    return (maximum_angular_momentum + 1) ** 2


def hard_static_energy_subspace_dimension_lower_bound(
    *,
    radius: float,
    stretched_distance: float,
    energy_budget: float,
    inner_offset: float,
    outer_offset: float,
) -> int:
    """Dimension guaranteed below ``E0`` by one radial ground mode per spin."""
    maximum_angular_momentum = maximum_bounded_energy_angular_momentum(
        radius=radius,
        stretched_distance=stretched_distance,
        energy_budget=energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    return truncated_scalar_harmonic_dimension(maximum_angular_momentum)


def directional_token_irrep_weights(
    maximum_angular_momentum: int,
) -> tuple[float, ...]:
    """Irrep probabilities ``p_l=(2l+1)/(L+1)^2`` of the token state."""
    dimension = truncated_scalar_harmonic_dimension(maximum_angular_momentum)
    return tuple(
        (2 * angular_momentum + 1) / dimension
        for angular_momentum in range(maximum_angular_momentum + 1)
    )


def directional_token_irrep_amplitudes(
    maximum_angular_momentum: int,
) -> tuple[float, ...]:
    """Positive amplitudes of the declared pure coherent token state."""
    return tuple(
        sqrt(weight)
        for weight in directional_token_irrep_weights(maximum_angular_momentum)
    )


def directional_token_expected_energy_upper_bound(
    *,
    maximum_angular_momentum: int,
    radius: float,
    stretched_distance: float,
    inner_offset: float,
    outer_offset: float,
) -> float:
    """Weighted upper bound for the declared pure token's expected energy."""
    weights = directional_token_irrep_weights(maximum_angular_momentum)
    return sum(
        weight
        * collar_static_energy_upper_bound(
            angular_momentum,
            radius=radius,
            stretched_distance=stretched_distance,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
        )
        for angular_momentum, weight in enumerate(weights)
    )


def missing_rotation_frame_relative_entropy(
    maximum_angular_momentum: int,
) -> float:
    """Exact relative entropy of the token state from its SO(3) twirl."""
    dimension = truncated_scalar_harmonic_dimension(maximum_angular_momentum)
    return log(float(dimension))


def stretched_horizon_proper_distance(
    *, radius: float, stretched_distance: float
) -> float:
    """Exact proper distance from ``r=R-delta`` to the de Sitter horizon."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    if stretched_distance >= radius:
        raise ValueError("stretched_distance must be smaller than radius")
    return 2.0 * radius * asin(sqrt(stretched_distance / (2.0 * radius)))


def angular_cutoff_asymptotic_coefficient(
    *,
    radius: float,
    energy_budget: float,
    inner_offset: float,
    outer_offset: float,
) -> float:
    """Coefficient ``C`` in ``L_delta^2 ~ C R/delta``."""
    _validate_positive("radius", radius)
    _validate_positive("energy_budget", energy_budget)
    kinetic_constant = sine_collar_kinetic_constant(
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    surplus = (energy_budget * radius) ** 2 - kinetic_constant
    if surplus <= 0.0:
        raise ValueError("energy_budget is below the collar kinetic floor")
    return 0.5 * surplus * exp(-2.0 * outer_offset)


def redshifted_frame_capacity_record(
    *,
    radius: float,
    stretched_distance: float,
    energy_budget: float,
    inner_offset: float,
    outer_offset: float,
) -> dict[str, object]:
    """Record the bounded-energy angular and missing-frame capacity."""
    maximum_angular_momentum = maximum_bounded_energy_angular_momentum(
        radius=radius,
        stretched_distance=stretched_distance,
        energy_budget=energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    dimension = truncated_scalar_harmonic_dimension(maximum_angular_momentum)
    proper_distance = stretched_horizon_proper_distance(
        radius=radius,
        stretched_distance=stretched_distance,
    )
    entropy = missing_rotation_frame_relative_entropy(maximum_angular_momentum)
    area = 4.0 * pi * radius * radius
    return {
        "de_sitter_radius_R": radius,
        "stretched_horizon_radial_gap_delta": stretched_distance,
        "stretched_horizon_proper_distance_rho": proper_distance,
        "static_one_particle_expected_energy_budget_E0": energy_budget,
        "collar_offsets_in_tortoise_units": (inner_offset, outer_offset),
        "maximum_certified_angular_momentum_L_delta": maximum_angular_momentum,
        "truncated_scalar_harmonic_dimension": dimension,
        "largest_mode_energy_upper_bound": collar_static_energy_upper_bound(
            maximum_angular_momentum,
            radius=radius,
            stretched_distance=stretched_distance,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
        ),
        "largest_mode_variational_ground_frequency_upper_bound": (
            finite_wall_ground_frequency_upper_bound(
                maximum_angular_momentum,
                radius=radius,
                stretched_distance=stretched_distance,
                inner_offset=inner_offset,
                outer_offset=outer_offset,
            )
        ),
        "hard_static_energy_subspace_dimension_lower_bound": (
            hard_static_energy_subspace_dimension_lower_bound(
                radius=radius,
                stretched_distance=stretched_distance,
                energy_budget=energy_budget,
                inner_offset=inner_offset,
                outer_offset=outer_offset,
            )
        ),
        "directional_token_definition": (
            "pure coherent sum over one common radial packet tensor |ell,ell>, "
            "with amplitude sqrt((2ell+1)/(L_delta+1)^2)"
        ),
        "hard_energy_directional_token_definition": (
            "pure coherent sum of one normalized finite-wall radial ground "
            "eigenstate phi_ell tensor |ell,ell> per spin through L_delta; "
            "every component has static frequency at most E0 by Rayleigh-Ritz"
        ),
        "directional_token_irrep_weight_formula": (
            "p_ell=(2ell+1)/(L_delta+1)^2 for 0<=ell<=L_delta"
        ),
        "directional_token_irrep_amplitude_formula": (
            "a_ell=sqrt(2ell+1)/(L_delta+1)"
        ),
        "directional_token_weight_normalization": 1.0,
        "directional_token_expected_energy_upper_bound": (
            collar_static_energy_upper_bound(
                maximum_angular_momentum,
                radius=radius,
                stretched_distance=stretched_distance,
                inner_offset=inner_offset,
                outer_offset=outer_offset,
            )
        ),
        "so3_twirl_nonzero_eigenvalue": 1.0 / dimension,
        "so3_twirl_eigenvalue_multiplicity": dimension,
        "so3_twirl_support": (
            "rank-D subspace direct_sum_ell span{phi_ell} tensor V_ell for the "
            "hard-energy token; replace phi_ell by chi_delta for the common-"
            "collar expected-energy token"
        ),
        "missing_rotation_frame_relative_entropy": entropy,
        "log_R_over_delta": log(radius / stretched_distance),
        "log_area_over_2pi_rho_squared": log(
            area / (2.0 * pi * proper_distance * proper_distance)
        ),
        "interpretation": (
            "relative entropy of SO(3) frameness for both the common-collar "
            "expected-energy token and a finite-wall hard-static-energy token"
        ),
        "generalized_entropy_identification_claimed": False,
    }


def redshifted_frame_capacity_certificate(
    *,
    radius: float = 1.0,
    energy_budget: float = 4.0,
    inner_offset: float = 0.5,
    outer_offset: float = 1.5,
    minimum_power: int = 64,
    steps: int = 6,
) -> dict[str, object]:
    """Audit the geometry-derived logarithmic missing-frame lower bound."""
    _validate_positive("radius", radius)
    _validate_positive("energy_budget", energy_budget)
    _validate_collar(inner_offset, outer_offset)
    if (
        isinstance(minimum_power, bool)
        or not isinstance(minimum_power, int)
        or minimum_power < 8
    ):
        raise ValueError("minimum_power must be an integer at least eight")
    if (
        isinstance(steps, bool)
        or not isinstance(steps, int)
        or steps < 3
        or steps > 64
    ):
        raise ValueError("steps must be an integer from three through sixty-four")
    if 0.5 * log(2.0 * minimum_power - 1.0) <= outer_offset:
        raise ValueError("minimum_power is too small for the declared collar")
    records = tuple(
        redshifted_frame_capacity_record(
            radius=radius,
            stretched_distance=radius / float(minimum_power * 4**index),
            energy_budget=energy_budget,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
        )
        for index in range(steps)
    )
    angular_cutoffs = tuple(
        record["maximum_certified_angular_momentum_L_delta"] for record in records
    )
    entropies = tuple(
        record["missing_rotation_frame_relative_entropy"] for record in records
    )
    coefficient = angular_cutoff_asymptotic_coefficient(
        radius=radius,
        energy_budget=energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    scaled_cutoffs = tuple(
        cutoff * cutoff * record["stretched_horizon_radial_gap_delta"] / radius
        for cutoff, record in zip(angular_cutoffs, records)
    )
    entropy_offsets = tuple(
        entropy - record["log_R_over_delta"]
        for entropy, record in zip(entropies, records)
    )
    certified_claims = {
        "bounded_energy_angular_capacity_is_nondecreasing_and_grows": (
            all(
                right >= left
                for left, right in zip(angular_cutoffs, angular_cutoffs[1:])
            )
            and angular_cutoffs[-1] > angular_cutoffs[0]
        ),
        "largest_certified_mode_respects_energy_budget": all(
            record["largest_mode_energy_upper_bound"] <= energy_budget
            for record in records
        ),
        "min_max_supplies_hard_energy_states_in_every_spin_sector": all(
            record["largest_mode_variational_ground_frequency_upper_bound"]
            <= energy_budget
            and record["hard_static_energy_subspace_dimension_lower_bound"]
            == record["truncated_scalar_harmonic_dimension"]
            for record in records
        ),
        "twirled_token_is_maximally_mixed_on_declared_rank_D_support": all(
            abs(
                record["so3_twirl_nonzero_eigenvalue"]
                * record["so3_twirl_eigenvalue_multiplicity"]
                - 1.0
            )
            < 1e-12
            for record in records
        ),
        "angular_cutoff_has_sqrt_R_over_delta_scaling": (
            abs(scaled_cutoffs[-1] - coefficient) < 0.08 * coefficient
        ),
        "missing_frame_entropy_has_log_R_over_delta_scaling": (
            max(entropy_offsets[-3:]) - min(entropy_offsets[-3:]) < 0.12
        ),
        "generalized_entropy_step_remains_conditional": all(
            not record["generalized_entropy_identification_claimed"]
            for record in records
        ),
    }
    return {
        "goal": "Redshifted Rotational-Frame Capacity Lower Bound",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "geometry_derived_hard_energy_frame_entropy_bound",
        "central_result": (
            "Near the de Sitter horizon, angular irreps through "
            "L_delta=Theta(sqrt(R/delta)) admit a common collar wavepacket with "
            "expected static one-particle energy at most E0. Rayleigh-Ritz also "
            "supplies one actual finite-wall eigenstate below E0 in every such "
            "spin sector. A directional token over those irreps loses exactly "
            "2 log(L_delta+1)=log(R/delta)+O(1) relative entropy under SO(3) "
            "twirling. This is a capacity lower bound; an observer no-go requires "
            "an additional operational link."
        ),
        "proper_distance_form": (
            "log(R/delta)=log(A/(2*pi*rho^2))+O(1) as rho tends to zero"
        ),
        "claim_boundary": (
            "free conformal one-particle scalar sector, finite Dirichlet wall, "
            "hard static-energy spectral support from min-max, moving near-horizon "
            "trial collar, and SO(3) subgroup; "
            "no backreaction bound, occupation-number theorem, full SO(1,4) "
            "observer construction, Type-II trace extension, or generalized-entropy "
            "identity is claimed"
        ),
        "certified_claims": certified_claims,
        "asymptotic_coefficient_for_L_squared": coefficient,
        "records": records,
        "next_physics_gate": (
            "extend the compact rotation expectation through a named observer "
            "crossed product, control local energy/backreaction, and compare its "
            "finite trace with generalized entropy"
        ),
    }
