"""Finite-pointer dephasing, observer purity, and branchwise gravity bounds.

This module is the executable algebra behind the proposed upgrade from a
binary pointer error to a finite-pointer second-Renyi resource theorem.  It
does not discretize the continuum localization proof.  Instead it composes
that proof's exact coefficient with identities that hold for any finite set
of conditional field data.

The controlled free-field evolution gives a Schur dephasing channel

    |i><j| -> G_ij |i><j|,

where ``G`` is the Gram matrix of conditional purified field states and
``|G_ij|=exp(-Gamma_ij)``.  For momentum data, the normalization inherited
from the binary paper is

    Gamma_ij = <p_i-p_j, B(p_i-p_j)>/4.

The source, pointer, and gravity qualifications of the binary theorem remain
in force: the pointer is prescribed, and the gravity statements concern
branchwise final-slice constraint data rather than a coupled evolution.
"""

from __future__ import annotations

from math import cosh, exp, isfinite, log, sqrt, tanh
from typing import Sequence


_TOLERANCE = 1.0e-12


def _validated_weights(weights: Sequence[float]) -> tuple[float, ...]:
    values = tuple(float(value) for value in weights)
    if not values:
        raise ValueError("weights must be nonempty")
    if any(not isfinite(value) or value < 0.0 for value in values):
        raise ValueError("weights must be finite and nonnegative")
    if abs(sum(values) - 1.0) > _TOLERANCE:
        raise ValueError("weights must sum to one")
    return values


def _validated_profiles(
    profiles: Sequence[Sequence[float]],
    *,
    expected_count: int,
) -> tuple[tuple[float, ...], ...]:
    values = tuple(tuple(float(value) for value in row) for row in profiles)
    if len(values) != expected_count:
        raise ValueError("one conditional profile is required per weight")
    if not values or not values[0]:
        raise ValueError("conditional profiles must have positive dimension")
    dimension = len(values[0])
    if any(len(row) != dimension for row in values):
        raise ValueError("conditional profiles must have equal dimension")
    if any(not isfinite(value) for row in values for value in row):
        raise ValueError("conditional profiles must be finite")
    return values


def _validated_symmetric_matrix(
    matrix: Sequence[Sequence[float]],
    *,
    dimension: int,
) -> tuple[tuple[float, ...], ...]:
    values = tuple(tuple(float(value) for value in row) for row in matrix)
    if len(values) != dimension or any(len(row) != dimension for row in values):
        raise ValueError("covariance matrix has the wrong dimension")
    if any(not isfinite(value) for row in values for value in row):
        raise ValueError("covariance matrix must be finite")
    for row in range(dimension):
        for column in range(row):
            if abs(values[row][column] - values[column][row]) > _TOLERANCE:
                raise ValueError("covariance matrix must be symmetric")
    return values


def _dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _difference(left: Sequence[float], right: Sequence[float]) -> tuple[float, ...]:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def _quadratic_form(
    vector: Sequence[float],
    matrix: Sequence[Sequence[float]],
) -> float:
    image = tuple(_dot(row, vector) for row in matrix)
    return _dot(vector, image)


def classical_pointer_purity(weights: Sequence[float]) -> float:
    """Return ``P_cl=sum_i w_i^2`` for the ideal classical pointer."""
    values = _validated_weights(weights)
    return sum(value * value for value in values)


def renyi_two_entropy_from_purity(purity: float) -> float:
    """Return ``S_2=-log(purity)`` for a normalized density matrix."""
    if not isfinite(purity) or purity <= 0.0 or purity > 1.0 + _TOLERANCE:
        raise ValueError("purity must lie in (0,1]")
    return -log(min(purity, 1.0))


def conditional_profile_energy_record(
    weights: Sequence[float],
    conditional_profiles: Sequence[Sequence[float]],
) -> dict[str, object]:
    """Return absolute and centered energies of conditional momentum data."""
    probabilities = _validated_weights(weights)
    profiles = _validated_profiles(
        conditional_profiles,
        expected_count=len(probabilities),
    )
    dimension = len(profiles[0])
    mean = tuple(
        sum(weight * profile[index] for weight, profile in zip(
            probabilities,
            profiles,
            strict=True,
        ))
        for index in range(dimension)
    )
    branch_energies = tuple(0.5 * _dot(profile, profile) for profile in profiles)
    centered_energies = tuple(
        0.5 * _dot(centered, centered)
        for centered in (_difference(profile, mean) for profile in profiles)
    )
    mean_branch_energy = sum(
        weight * energy
        for weight, energy in zip(probabilities, branch_energies, strict=True)
    )
    centered_energy = sum(
        weight * energy
        for weight, energy in zip(probabilities, centered_energies, strict=True)
    )
    mean_profile_energy = 0.5 * _dot(mean, mean)
    pairwise_squared_distance = sum(
        left_weight
        * right_weight
        * _dot(difference, difference)
        for left_weight, left in zip(probabilities, profiles, strict=True)
        for right_weight, right in zip(probabilities, profiles, strict=True)
        for difference in (_difference(left, right),)
    )
    return {
        "weights": probabilities,
        "conditional_profiles": profiles,
        "weighted_mean_profile": mean,
        "branch_energies": branch_energies,
        "mean_branch_energy": mean_branch_energy,
        "mean_profile_energy": mean_profile_energy,
        "centered_branch_energies": centered_energies,
        "centered_energy_Ebar": centered_energy,
        "pairwise_squared_distance_average": pairwise_squared_distance,
        "pairwise_variance_identity_rhs": 4.0 * centered_energy,
        "centering_identity_rhs": mean_branch_energy - mean_profile_energy,
    }


def finite_pointer_dephasing_record(
    weights: Sequence[float],
    conditional_profiles: Sequence[Sequence[float]],
    covariance_matrix: Sequence[Sequence[float]],
) -> dict[str, object]:
    """Evaluate a finite-dimensional proxy of the exact Schur channel.

    ``covariance_matrix`` represents the positive thermal form ``B``.  The
    continuum theorem supplies its localized norm; this helper checks the
    finite-pointer algebra without claiming that a Galerkin matrix proves the
    continuum operator statement.
    """
    probabilities = _validated_weights(weights)
    profiles = _validated_profiles(
        conditional_profiles,
        expected_count=len(probabilities),
    )
    covariance = _validated_symmetric_matrix(
        covariance_matrix,
        dimension=len(profiles[0]),
    )
    gamma_rows: list[tuple[float, ...]] = []
    gram_magnitude_rows: list[tuple[float, ...]] = []
    density_magnitude_rows: list[tuple[float, ...]] = []
    for left_index, left in enumerate(profiles):
        gamma_row: list[float] = []
        gram_row: list[float] = []
        density_row: list[float] = []
        for right_index, right in enumerate(profiles):
            difference = _difference(left, right)
            quadratic = _quadratic_form(difference, covariance)
            if quadratic < -_TOLERANCE:
                raise ValueError("covariance matrix is negative on a profile difference")
            gamma = 0.25 * max(quadratic, 0.0)
            gram_magnitude = exp(-gamma)
            gamma_row.append(gamma)
            gram_row.append(gram_magnitude)
            density_row.append(
                sqrt(probabilities[left_index] * probabilities[right_index])
                * gram_magnitude
            )
        gamma_rows.append(tuple(gamma_row))
        gram_magnitude_rows.append(tuple(gram_row))
        density_magnitude_rows.append(tuple(density_row))
    gamma_matrix = tuple(gamma_rows)
    gram_magnitude = tuple(gram_magnitude_rows)
    density_magnitude = tuple(density_magnitude_rows)
    purity = sum(
        probabilities[left]
        * probabilities[right]
        * exp(-2.0 * gamma_matrix[left][right])
        for left in range(len(probabilities))
        for right in range(len(probabilities))
    )
    return {
        "channel": "|i><j| -> G_ij |i><j|",
        "gram_magnitude_formula": "|G_ij|=exp(-Gamma_ij)",
        "pairwise_exponent_formula": "Gamma_ij=<p_i-p_j,B(p_i-p_j)>/4",
        "weights": probabilities,
        "pairwise_dephasing_exponents": gamma_matrix,
        "gram_magnitudes": gram_magnitude,
        "reduced_pointer_density_magnitudes": density_magnitude,
        "physical_pointer_purity": purity,
        "physical_pointer_renyi_two": renyi_two_entropy_from_purity(purity),
        "ideal_classical_pointer_purity": classical_pointer_purity(probabilities),
        "phase_scope": (
            "Weyl and source phases are omitted because Tr(rho^2) depends only "
            "on |G_ij|."
        ),
    }


def finite_pointer_renyi_bound(
    weights: Sequence[float],
    *,
    centered_field_energy: float,
    cost_coefficient: float,
) -> dict[str, float | str]:
    """Return the exact Jensen lower bound on purity and upper bound on ``S_2``."""
    probabilities = _validated_weights(weights)
    if not isfinite(centered_field_energy) or centered_field_energy < 0.0:
        raise ValueError("centered_field_energy must be finite and nonnegative")
    if not isfinite(cost_coefficient) or cost_coefficient <= 0.0:
        raise ValueError("cost_coefficient must be finite and positive")
    classical_purity = classical_pointer_purity(probabilities)
    off_diagonal_weight = 1.0 - classical_purity
    classical_entropy = renyi_two_entropy_from_purity(classical_purity)
    linear_entropy_bound = cost_coefficient * centered_field_energy
    if off_diagonal_weight <= _TOLERANCE:
        purity_lower = 1.0
        exponent = 0.0
    else:
        exponent = linear_entropy_bound / off_diagonal_weight
        purity_lower = classical_purity + off_diagonal_weight * exp(-exponent)
    entropy_upper = renyi_two_entropy_from_purity(purity_lower)
    return {
        "classical_pointer_purity_Pcl": classical_purity,
        "classical_pointer_renyi_H2": classical_entropy,
        "off_diagonal_weight": off_diagonal_weight,
        "centered_field_energy_Ebar": centered_field_energy,
        "cost_coefficient_C": cost_coefficient,
        "jensen_exponent": exponent,
        "physical_purity_lower_bound": purity_lower,
        "physical_renyi_upper_bound": entropy_upper,
        "simplified_renyi_upper_bound": min(
            classical_entropy,
            linear_entropy_bound,
        ),
        "purity_formula": (
            "Tr(rho^2)>=Pcl+(1-Pcl)*"
            "exp[-C*Ebar/(1-Pcl)]"
        ),
        "entropy_formula": "S2(rho)<=min{H2(w),C*Ebar}",
    }


def finite_pointer_cost_composition_record(
    weights: Sequence[float],
    conditional_profiles: Sequence[Sequence[float]],
    covariance_matrix: Sequence[Sequence[float]],
    *,
    cost_coefficient: float,
) -> dict[str, object]:
    """Compose the exact channel algebra with a proposed operator-norm bound."""
    energy = conditional_profile_energy_record(weights, conditional_profiles)
    channel = finite_pointer_dephasing_record(
        weights,
        conditional_profiles,
        covariance_matrix,
    )
    covariance = _validated_symmetric_matrix(
        covariance_matrix,
        dimension=len(energy["weighted_mean_profile"]),
    )
    profiles = energy["conditional_profiles"]
    pairwise_checks = []
    for left in profiles:
        for right in profiles:
            difference = _difference(left, right)
            norm_squared = _dot(difference, difference)
            quadratic = _quadratic_form(difference, covariance)
            pairwise_checks.append(
                quadratic <= 0.5 * cost_coefficient * norm_squared + _TOLERANCE
            )
    bound = finite_pointer_renyi_bound(
        weights,
        centered_field_energy=float(energy["centered_energy_Ebar"]),
        cost_coefficient=cost_coefficient,
    )
    actual_purity = float(channel["physical_pointer_purity"])
    return {
        "energy": energy,
        "channel": channel,
        "renyi_bound": bound,
        "pairwise_cost_bound_holds": all(pairwise_checks),
        "purity_bound_holds": actual_purity
        + _TOLERANCE
        >= float(bound["physical_purity_lower_bound"]),
        "renyi_bound_holds": float(channel["physical_pointer_renyi_two"])
        <= float(bound["physical_renyi_upper_bound"]) + _TOLERANCE,
    }


def harlow_orthogonal_code_fluctuation_record(
    *,
    observer_purity: float,
    observer_purity_lower_bound: float,
    encoding_dimension: int,
) -> dict[str, float | int | str | bool]:
    """Insert physical observer purity into Harlow--Usatyuk--Zhao Eq. (4.2).

    For orthogonal CRT-real matter states, both matter-overlap terms vanish.
    Their Haar-averaged squared inner-product fluctuation is therefore exactly
    ``D/(D+2) Tr(rho_Ob'^2)``.  A physical purity lower bound consequently
    gives an ensemble-averaged fluctuation floor.  This does not by itself
    prove a lower bound for every fixed encoding map.
    """
    for name, value in (
        ("observer_purity", observer_purity),
        ("observer_purity_lower_bound", observer_purity_lower_bound),
    ):
        if not isfinite(value) or value <= 0.0 or value > 1.0 + _TOLERANCE:
            raise ValueError(f"{name} must lie in (0,1]")
    if observer_purity + _TOLERANCE < observer_purity_lower_bound:
        raise ValueError("observer purity cannot be below its certified lower bound")
    if not isinstance(encoding_dimension, int) or encoding_dimension <= 0:
        raise ValueError("encoding_dimension must be a positive integer")
    factor = encoding_dimension / (encoding_dimension + 2.0)
    return {
        "encoding_dimension_D": encoding_dimension,
        "finite_D_factor": factor,
        "physical_observer_purity": min(observer_purity, 1.0),
        "physical_observer_renyi_two": renyi_two_entropy_from_purity(
            observer_purity
        ),
        "exact_orthogonal_state_mean_square_fluctuation": factor
        * observer_purity,
        "certified_mean_square_fluctuation_floor": factor
        * observer_purity_lower_bound,
        "harlow_equation": (
            "For <phi|psi>=<phi*|psi>=0, HUZ Eq. (4.2) gives "
            "E_O |<phi|Vhat^dagger Vhat|psi>|^2="
            "D*Tr(rho_Ob'^2)/(D+2)."
        ),
        "state_identification": (
            "A purified controlled-displacement record state has equal "
            "nonzero reduced spectra on the pointer and record systems, so "
            "Tr(rho_Ob'^2)=Tr(rho_pointer^2)."
        ),
        "scope": (
            "This is a Haar-ensemble mean-square floor for an orthogonal "
            "matter pair, not a deterministic lower bound for every fixed code."
        ),
        "gate_three_closed": True,
    }


def branchwise_gravity_renyi_bound(
    *,
    support_ratio: float,
    dimensionless_cost_coefficient: float,
    maximum_constraint_ratio: float,
    static_patch_radius: float,
    newton_constant: float,
) -> dict[str, float | str]:
    """Compose a branchwise final-slice gravity budget with the Renyi bound."""
    for name, value in (
        ("support_ratio", support_ratio),
        ("dimensionless_cost_coefficient", dimensionless_cost_coefficient),
        ("static_patch_radius", static_patch_radius),
        ("newton_constant", newton_constant),
    ):
        if not isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be finite and positive")
    if (
        not isfinite(maximum_constraint_ratio)
        or maximum_constraint_ratio < 0.0
        or maximum_constraint_ratio >= 1.0
    ):
        raise ValueError("maximum_constraint_ratio must lie in [0,1)")
    areal_ratio = tanh(support_ratio)
    lapse = 1.0 / cosh(support_ratio) ** 2
    output_areal_radius = static_patch_radius * areal_ratio
    maximum_branch_energy = (
        maximum_constraint_ratio
        * output_areal_radius
        * lapse
        / (2.0 * newton_constant)
    )
    area_coefficient = (
        0.5
        * dimensionless_cost_coefficient
        * areal_ratio
        * lapse
    )
    entropy_upper = (
        maximum_constraint_ratio
        * static_patch_radius**2
        * area_coefficient
        / newton_constant
    )
    return {
        "support_ratio_y": support_ratio,
        "output_areal_radius_b": output_areal_radius,
        "de_sitter_N_at_b": lapse,
        "maximum_constraint_ratio_delta": maximum_constraint_ratio,
        "maximum_energy_of_every_branch": maximum_branch_energy,
        "centered_energy_upper_bound": maximum_branch_energy,
        "dimensionless_area_coefficient": area_coefficient,
        "observer_renyi_upper_bound": entropy_upper,
        "exact_form": (
            "S2<=delta*(R^2/G)*"
            "C_opt(y)*tanh(y)*sech(y)^2/2"
        ),
        "branchwise_hypothesis": (
            "Every conditional spherical q=0 datum obeys Q_b,i<=delta; "
            "then Ebar<=sum_i w_i E_i<=max_i E_i."
        ),
        "scope": (
            "Final-slice constraint corollary only; the channel is not "
            "rederived on the branch-dependent geometries."
        ),
    }


def finite_pointer_observer_certificate(
    *,
    illustrative_cost_coefficient: float = 1.0295979905445,
) -> dict[str, object]:
    """Return a deterministic four-gate algebra certificate."""
    if (
        not isfinite(illustrative_cost_coefficient)
        or illustrative_cost_coefficient <= 0.0
    ):
        raise ValueError("illustrative_cost_coefficient must be finite and positive")
    weights = (0.5, 0.3, 0.2)
    profiles = ((-1.0, 0.0), (0.5, 0.0), (2.0, 0.0))
    covariance = ((1.0, 0.0), (0.0, 0.25))
    cost_coefficient = 2.0
    composition = finite_pointer_cost_composition_record(
        weights,
        profiles,
        covariance,
        cost_coefficient=cost_coefficient,
    )
    binary = finite_pointer_cost_composition_record(
        (0.5, 0.5),
        ((-1.0,), (1.0,)),
        ((1.0,),),
        cost_coefficient=2.0,
    )
    channel = composition["channel"]
    bound = composition["renyi_bound"]
    harlow = harlow_orthogonal_code_fluctuation_record(
        observer_purity=float(channel["physical_pointer_purity"]),
        observer_purity_lower_bound=float(bound["physical_purity_lower_bound"]),
        encoding_dimension=1000,
    )
    from qgtoy.local_scalar_observer_cost import sharp_observer_cost_characterization

    sharp_cost = sharp_observer_cost_characterization(
        1.0,
        static_patch_radius=1.0,
    )
    rigorous_cost_upper = float(sharp_cost["rigorous_explicit_upper_coefficient"])
    gravity_numerical = branchwise_gravity_renyi_bound(
        support_ratio=1.0,
        dimensionless_cost_coefficient=illustrative_cost_coefficient,
        maximum_constraint_ratio=0.25,
        static_patch_radius=1.0,
        newton_constant=1.0e-6,
    )
    gravity_numerical["coefficient_status"] = (
        "nonrigorous Galerkin illustration of the exact C_opt(1) formula"
    )
    gravity_rigorous = branchwise_gravity_renyi_bound(
        support_ratio=1.0,
        dimensionless_cost_coefficient=rigorous_cost_upper,
        maximum_constraint_ratio=0.25,
        static_patch_radius=1.0,
        newton_constant=1.0e-6,
    )
    gravity_rigorous["coefficient_status"] = (
        "rigorous explicit upper bound on C_opt(1)"
    )
    binary_actual = float(binary["channel"]["physical_pointer_purity"])
    binary_lower = float(binary["renyi_bound"]["physical_purity_lower_bound"])
    energy = composition["energy"]
    claims = {
        "finite_pointer_exact_schur_channel": (
            channel["channel"] == "|i><j| -> G_ij |i><j|"
        ),
        "pairwise_variance_identity": abs(
            float(energy["pairwise_squared_distance_average"])
            - float(energy["pairwise_variance_identity_rhs"])
        )
        <= _TOLERANCE,
        "centered_energy_identity": abs(
            float(energy["centered_energy_Ebar"])
            - float(energy["centering_identity_rhs"])
        )
        <= _TOLERANCE,
        "renyi_jensen_bound": bool(composition["renyi_bound_holds"]),
        "binary_bound_is_saturated": abs(binary_actual - binary_lower)
        <= _TOLERANCE,
        "harlow_orthogonal_code_insertion": bool(harlow["gate_three_closed"]),
        "branchwise_gravity_composition": (
            "Every conditional" in gravity_numerical["branchwise_hypothesis"]
        ),
        "rigorous_gravity_coefficient_dominates_numerical_illustration": (
            float(gravity_rigorous["dimensionless_area_coefficient"])
            >= float(gravity_numerical["dimensionless_area_coefficient"])
        ),
    }
    passed = all(claims.values())
    return {
        "artifact": "finite_pointer_observer_entropy_upgrade",
        "status": "pass_four_gate_algebra" if passed else "fail",
        "finite_pointer_example": composition,
        "binary_saturation_check": binary,
        "harlow_code_insertion": harlow,
        "branchwise_gravity_example": gravity_numerical,
        "branchwise_gravity_rigorous_bound": gravity_rigorous,
        "certified_claims": claims,
        "claim_boundary": (
            "The finite-pointer channel and Renyi inequality are exact. The "
            "Harlow insertion is an ensemble-averaged orthogonal-state code "
            "fluctuation statement. The gravity result assumes a local "
            "constraint budget on every conditional spherical q=0 branch and "
            "does not constitute coupled Einstein-matter evolution. General-d "
            "global sharpness and standalone literature novelty are not "
            "certified."
        ),
    }
