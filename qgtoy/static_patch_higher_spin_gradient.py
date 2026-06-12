"""Higher-spin singlet obstruction for the static-patch gradient channel.

The ideal collective ``SO(3)`` heat channel fixes the total-spin singlet in
``V_L tensor V_L``.  A separated optical-gradient bath has correlations
``(c_parallel,c_perp,c_perp)`` and introduces relative-charge noise.  Expanding
the exact semigroup about perfect common mode gives a Casimir-enhanced singlet
leakage coefficient and a representation-explicit Duhamel remainder bound.
"""

from __future__ import annotations

from math import exp, isfinite, log, sqrt

from .static_patch_gradient_torque import gradient_zero_frequency_correlations


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _twice_spin(name: str, value: int | float) -> int:
    """Validate a positive integer or half-integer spin and return ``2L``."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a positive integer or half-integer")
    numeric = float(value)
    if not isfinite(numeric) or numeric <= 0.0:
        raise ValueError(f"{name} must be a positive integer or half-integer")
    twice = round(2.0 * numeric)
    if abs(2.0 * numeric - twice) > 1.0e-12:
        raise ValueError(f"{name} must be a positive integer or half-integer")
    return twice


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def gradient_correlation_defect_sum(
    center_distance_over_radius: float,
) -> float:
    """Return ``(1-c_parallel)+2(1-c_perp)``."""
    longitudinal, transverse = gradient_zero_frequency_correlations(
        center_distance_over_radius
    )
    return (1.0 - longitudinal) + 2.0 * (1.0 - transverse)


def gradient_correlation_defect_quadratic_bounds(
    center_distance_over_radius: float,
) -> tuple[float, float]:
    """Bound the total gradient defect explicitly on ``0<=y<=1``.

    With ``z=y/2``, the exact defect is

    ``3 tanh(z)^2+3 z tanh(z) sech(z)^2``.

    The inequalities ``z-z^3/3<=tanh(z)<=z`` and
    ``1-z^2<=sech(z)^2<=1`` give the returned lower and upper bounds.
    """
    y = center_distance_over_radius
    _validate_nonnegative("center_distance_over_radius", y)
    if y > 1.0:
        raise ValueError("quadratic defect bounds require distance at most one")
    y_squared = y * y
    return (
        1.5 * y_squared * (1.0 - 0.25 * y_squared),
        1.5 * y_squared,
    )


def higher_spin_singlet_linear_leakage(
    spin: int | float,
    dimensionless_time: float,
    *,
    center_distance_over_radius: float,
) -> float:
    """Return the exact term linear in the common-mode covariance defect."""
    _twice_spin("spin", spin)
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    defect_sum = gradient_correlation_defect_sum(center_distance_over_radius)
    return (
        4.0
        * spin
        * (spin + 1)
        * defect_sum
        * dimensionless_time
        / 3.0
    )


def higher_spin_dyson_scale(
    spin: int | float,
    dimensionless_time: float,
    *,
    center_distance_over_radius: float,
) -> float:
    """Return the Hilbert-Schmidt perturbation scale ``s ||V|| <= x``."""
    _twice_spin("spin", spin)
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    defect_sum = gradient_correlation_defect_sum(center_distance_over_radius)
    return 8.0 * spin**2 * defect_sum * dimensionless_time


def higher_spin_dyson_remainder_bound(
    spin: int | float,
    dimensionless_time: float,
    *,
    center_distance_over_radius: float,
) -> float:
    """Bound all terms beyond first order in the semigroup perturbation."""
    scale = higher_spin_dyson_scale(
        spin,
        dimensionless_time,
        center_distance_over_radius=center_distance_over_radius,
    )
    return 0.5 * scale**2


def _symmetric_jacobi_eigendecomposition(
    matrix: list[list[float]],
) -> tuple[tuple[float, ...], tuple[tuple[float, ...], ...]]:
    """Diagonalize a small real symmetric matrix without optional dependencies."""
    size = len(matrix)
    if size == 1:
        return (matrix[0][0],), ((1.0,),)
    work = [row[:] for row in matrix]
    vectors = [
        [1.0 if row == column else 0.0 for column in range(size)]
        for row in range(size)
    ]
    scale = max(1.0, max(abs(value) for row in work for value in row))
    tolerance = 1.0e-14 * scale
    for _ in range(80 * size**2):
        row_index = 0
        column_index = 1
        maximum = abs(work[row_index][column_index])
        for row in range(size):
            for column in range(row + 1, size):
                candidate = abs(work[row][column])
                if candidate > maximum:
                    maximum = candidate
                    row_index = row
                    column_index = column
        if maximum <= tolerance:
            break
        p = row_index
        q = column_index
        off_diagonal = work[p][q]
        tau = (work[q][q] - work[p][p]) / (2.0 * off_diagonal)
        tangent = (
            1.0 / (tau + sqrt(1.0 + tau * tau))
            if tau >= 0.0
            else -1.0 / (-tau + sqrt(1.0 + tau * tau))
        )
        cosine = 1.0 / sqrt(1.0 + tangent * tangent)
        sine = tangent * cosine
        diagonal_p = work[p][p]
        diagonal_q = work[q][q]
        work[p][p] = diagonal_p - tangent * off_diagonal
        work[q][q] = diagonal_q + tangent * off_diagonal
        work[p][q] = 0.0
        work[q][p] = 0.0
        for index in range(size):
            if index in (p, q):
                continue
            old_p = work[index][p]
            old_q = work[index][q]
            new_p = cosine * old_p - sine * old_q
            new_q = sine * old_p + cosine * old_q
            work[index][p] = new_p
            work[p][index] = new_p
            work[index][q] = new_q
            work[q][index] = new_q
        for index in range(size):
            old_p = vectors[index][p]
            old_q = vectors[index][q]
            vectors[index][p] = cosine * old_p - sine * old_q
            vectors[index][q] = sine * old_p + cosine * old_q
    else:
        raise RuntimeError("Jacobi eigendecomposition did not converge")
    return (
        tuple(work[index][index] for index in range(size)),
        tuple(tuple(row) for row in vectors),
    )


def higher_spin_singlet_survival_probability(
    spin: int | float,
    dimensionless_time: float,
    *,
    longitudinal_correlation: float,
    transverse_correlation: float,
) -> float:
    """Return exact integer or half-integer singlet survival via rank blocks.

    On ``End(V_L) tensor End(V_L)``, the singlet projector decomposes into one
    scalar vector in each equal tensor-rank block ``ell tensor ell``.  Axial
    anisotropy preserves the zero-total-magnetic-number subspace, leaving a
    real symmetric tridiagonal block of size ``2 ell+1``.  The dependency-free
    dense Jacobi backend is intended as a moderate-spin research verifier; the
    perturbative certificate below handles asymptotically large spins without
    diagonalizing these blocks.
    """
    twice_spin = _twice_spin("spin", spin)
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    for name, value in (
        ("longitudinal_correlation", longitudinal_correlation),
        ("transverse_correlation", transverse_correlation),
    ):
        if not isfinite(value) or value < -1.0 or value > 1.0:
            raise ValueError(f"{name} must lie in [-1,1]")
    if dimensionless_time == 0.0:
        return 1.0
    if longitudinal_correlation == 1.0 and transverse_correlation == 1.0:
        return 1.0
    dimension = twice_spin + 1
    survival = 0.0
    for tensor_rank in range(twice_spin + 1):
        block_size = 2 * tensor_rank + 1
        block = [[0.0 for _ in range(block_size)] for _ in range(block_size)]
        magnetic_numbers = tuple(range(-tensor_rank, tensor_rank + 1))
        for index, magnetic_number in enumerate(magnetic_numbers):
            block[index][index] = (
                -2.0 * tensor_rank * (tensor_rank + 1)
                + 2.0 * longitudinal_correlation * magnetic_number**2
            )
            if index + 1 < block_size:
                coupling = -transverse_correlation * (
                    tensor_rank - magnetic_number
                ) * (tensor_rank + magnetic_number + 1)
                block[index][index + 1] = coupling
                block[index + 1][index] = coupling
        eigenvalues, eigenvectors = _symmetric_jacobi_eigendecomposition(block)
        normalization = sqrt(float(block_size))
        scalar_vector = tuple(
            (-1.0) ** (tensor_rank - magnetic_number) / normalization
            for magnetic_number in magnetic_numbers
        )
        block_survival = 0.0
        for eigen_index, eigenvalue in enumerate(eigenvalues):
            overlap = sum(
                eigenvectors[basis_index][eigen_index]
                * scalar_vector[basis_index]
                for basis_index in range(block_size)
            )
            eigenvalue_tolerance = 2.0e-12 * max(
                1.0,
                float(tensor_rank * (tensor_rank + 1)),
            )
            if eigenvalue > eigenvalue_tolerance:
                raise RuntimeError(
                    "tensor-rank generator has a positive eigenvalue"
                )
            checked_eigenvalue = 0.0 if eigenvalue > 0.0 else eigenvalue
            block_survival += overlap**2 * exp(
                dimensionless_time * checked_eigenvalue
            )
        survival += block_size * block_survival / float(dimension**2)
    if survival < -1.0e-10 or survival > 1.0 + 1.0e-10:
        raise RuntimeError("tensor-rank survival left the physical interval")
    return min(1.0, max(0.0, survival))


def higher_spin_exact_gradient_mismatch_lower_bound(
    spin: int | float,
    dimensionless_time: float,
    *,
    center_distance_over_radius: float,
) -> float:
    """Return the exact singlet channel witness for integer or half-integer spin."""
    longitudinal, transverse = gradient_zero_frequency_correlations(
        center_distance_over_radius
    )
    survival = higher_spin_singlet_survival_probability(
        spin,
        dimensionless_time,
        longitudinal_correlation=longitudinal,
        transverse_correlation=transverse,
    )
    return 1.0 - survival


def higher_spin_singlet_mismatch_lower_bound(
    spin: int | float,
    dimensionless_time: float,
    *,
    center_distance_over_radius: float,
) -> float:
    """Return the rigorous singlet-output channel mismatch lower bound.

    If ``P_L`` is the spin-``L`` singlet, then

    ``(1/2)||E_s-E_s^collective||_diamond >= 1-Tr[P_L E_s(P_L)]``.

    The returned lower bound is the exact linear term minus the norm-convergent
    Duhamel tail.  It is deliberately clipped at zero outside its useful local
    common-mode regime.
    """
    linear = higher_spin_singlet_linear_leakage(
        spin,
        dimensionless_time,
        center_distance_over_radius=center_distance_over_radius,
    )
    remainder = higher_spin_dyson_remainder_bound(
        spin,
        dimensionless_time,
        center_distance_over_radius=center_distance_over_radius,
    )
    return max(0.0, linear - remainder)


def higher_spin_certified_local_distance_ceiling(
    spin: int | float,
    dimensionless_time: float,
    mismatch_budget: float,
) -> float:
    """Return a finite-``y`` ceiling inside the certified local window.

    If ``0<=y<=1``, the Duhamel half-slope condition holds, and the channel
    mismatch is at most ``mismatch_budget``, then

    ``y^2 <= 4 mismatch_budget/[3 L(L+1) s]``.

    The returned value is capped at one because the analytic defect lower
    bound is asserted only on that interval.
    """
    _twice_spin("spin", spin)
    _validate_positive("dimensionless_time", dimensionless_time)
    _validate_nonnegative("mismatch_budget", mismatch_budget)
    ceiling = sqrt(
        4.0
        * mismatch_budget
        / (3.0 * spin * (spin + 1.0) * dimensionless_time)
    )
    return min(1.0, ceiling)


def higher_spin_perturbative_record(
    spin: int | float,
    *,
    center_distance_over_radius: float,
    mismatch_coefficient: float = 1.0,
) -> dict[str, object]:
    """Audit the rigorous and leading higher-spin co-location bounds."""
    twice_spin = _twice_spin("spin", spin)
    _validate_nonnegative(
        "center_distance_over_radius",
        center_distance_over_radius,
    )
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    dimension = twice_spin + 1
    dimensionless_time = 0.5 * log(float(dimension))
    allocated_mismatch = mismatch_coefficient / float(dimension)
    defect_sum = gradient_correlation_defect_sum(center_distance_over_radius)
    linear = higher_spin_singlet_linear_leakage(
        spin,
        dimensionless_time,
        center_distance_over_radius=center_distance_over_radius,
    )
    dyson_scale = higher_spin_dyson_scale(
        spin,
        dimensionless_time,
        center_distance_over_radius=center_distance_over_radius,
    )
    remainder = higher_spin_dyson_remainder_bound(
        spin,
        dimensionless_time,
        center_distance_over_radius=center_distance_over_radius,
    )
    lower_bound = max(0.0, linear - remainder)
    target_defect_budget = (
        3.0
        * mismatch_coefficient
        / (
            2.0
            * dimension
            * spin
            * (spin + 1)
            * dimensionless_time
        )
    )
    perturbative_defect_window = (spin + 1.0) / (
        48.0 * dimensionless_time * spin**3
    )
    half_slope_window = defect_sum <= perturbative_defect_window
    half_slope_lower_bound = 0.5 * linear if half_slope_window else None
    leading_distance = sqrt(
        mismatch_coefficient
        / (
            dimension
            * spin
            * (spin + 1)
            * log(float(dimension))
        )
    )
    certified_local_distance = higher_spin_certified_local_distance_ceiling(
        spin,
        dimensionless_time,
        allocated_mismatch,
    )
    return {
        "spin_L": spin,
        "sector_dimension_d": dimension,
        "dimensionless_protocol_time_s": dimensionless_time,
        "center_distance_over_radius_y": center_distance_over_radius,
        "gradient_defect_sum_delta_parallel_plus_2_delta_perp": defect_sum,
        "exact_linear_singlet_leakage": linear,
        "dyson_perturbation_scale_x": dyson_scale,
        "dyson_remainder_upper_bound": remainder,
        "rigorous_singlet_channel_mismatch_lower_bound": lower_bound,
        "allocated_mismatch_A_over_d": allocated_mismatch,
        "inside_half_slope_perturbative_window": half_slope_window,
        "half_linear_leakage_lower_bound_in_window": half_slope_lower_bound,
        "rigorous_lower_bound_exceeds_allocated_mismatch": (
            lower_bound > allocated_mismatch
        ),
        "necessary_defect_budget_if_inside_window": target_defect_budget,
        "maximum_defect_for_certified_half_slope_window": (
            perturbative_defect_window
        ),
        "leading_small_y_maximum_distance_over_radius": leading_distance,
        "finite_y_distance_ceiling_if_inside_half_slope_window": (
            certified_local_distance
        ),
        "leading_scaled_distance_y_d_to_3_over_2_sqrt_log_d": (
            leading_distance
            * dimension**1.5
            * sqrt(log(float(dimension)))
        ),
    }


def static_patch_higher_spin_gradient_certificate(
    *,
    maximum_spin: int = 4096,
    center_distance_over_radius: float = 1.0e-6,
    mismatch_coefficient: float = 1.0,
) -> dict[str, object]:
    """Certify Casimir-enhanced higher-spin singlet leakage."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 16:
        raise ValueError("maximum_spin must be at least sixteen")
    spins = tuple(
        sorted(
            {
                spin
                for spin in (16, 64, 256, 1024, maximum_spin)
                if spin <= maximum_spin
            }
            | {maximum_spin}
        )
    )
    records = tuple(
        higher_spin_perturbative_record(
            spin,
            center_distance_over_radius=center_distance_over_radius,
            mismatch_coefficient=mismatch_coefficient,
        )
        for spin in spins
    )
    leading_distances = tuple(
        record["leading_small_y_maximum_distance_over_radius"]
        for record in records
    )
    scaled_distances = tuple(
        record["leading_scaled_distance_y_d_to_3_over_2_sqrt_log_d"]
        for record in records
    )
    large_spin_records = tuple(
        record
        for record in records
        if record["necessary_defect_budget_if_inside_window"]
        <= record["maximum_defect_for_certified_half_slope_window"]
    )
    exact_records = tuple(
        {
            "spin_L": spin,
            "perfect_common_mode_survival": (
                higher_spin_singlet_survival_probability(
                    spin,
                    0.7,
                    longitudinal_correlation=1.0,
                    transverse_correlation=1.0,
                )
            ),
            "independent_bath_survival": (
                higher_spin_singlet_survival_probability(
                    spin,
                    0.7,
                    longitudinal_correlation=0.0,
                    transverse_correlation=0.0,
                )
            ),
            "physical_gradient_mismatch": (
                higher_spin_exact_gradient_mismatch_lower_bound(
                    spin,
                    0.7,
                    center_distance_over_radius=0.01,
                )
            ),
        }
        for spin in (0.5, 1, 1.5, 2, 3, 4)
    )
    perturbative_cross_checks = tuple(
        {
            "spin_L": spin,
            "exact_mismatch": higher_spin_exact_gradient_mismatch_lower_bound(
                spin,
                0.2,
                center_distance_over_radius=0.01,
            ),
            "duhamel_lower_bound": higher_spin_singlet_mismatch_lower_bound(
                spin,
                0.2,
                center_distance_over_radius=0.01,
            ),
        }
        for spin in (1, 2, 3, 4)
    )
    certified_claims = {
        "leading_distance_decreases_with_spin": all(
            right < left
            for left, right in zip(leading_distances, leading_distances[1:])
        ),
        "scaled_distance_approaches_two_sqrt_A": abs(
            scaled_distances[-1] - 2.0 * sqrt(mismatch_coefficient)
        )
        < 5.0e-4,
        "fixed_separation_dyson_scale_grows_with_spin": (
            records[-1]["dyson_perturbation_scale_x"]
            > records[0]["dyson_perturbation_scale_x"]
        ),
        "target_budget_enters_the_rigorous_window_at_large_spin": bool(
            large_spin_records
        ),
        "exact_mismatch_dominates_duhamel_lower_bound": all(
            record["exact_mismatch"] + 1.0e-12
            >= record["duhamel_lower_bound"]
            for record in perturbative_cross_checks
        ),
        "exact_blocks_fix_the_singlet_at_perfect_common_mode": all(
            abs(record["perfect_common_mode_survival"] - 1.0) < 2.0e-12
            for record in exact_records
        ),
        "exact_gradient_mismatch_grows_across_sampled_spins": all(
            right["physical_gradient_mismatch"]
            > left["physical_gradient_mismatch"]
            for left, right in zip(exact_records, exact_records[1:])
        ),
    }
    return {
        "goal": "Higher-Spin Static-Patch Gradient Singlet Obstruction",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "casimir_enhanced_higher_spin_common_mode_obstruction",
        "central_result": (
            "For the spin-L singlet, the exact term linear in the gradient "
            "covariance defects is (4/3)L(L+1)s(delta_parallel+2delta_perp). "
            "The exact survival is a sum of tridiagonal tensor-rank block "
            "exponentials. Its first-order term is "
            "(4/3)L(L+1)s(delta_parallel+2delta_perp), and the all-orders "
            "Duhamel remainder is at most x^2/2 with "
            "x=8L^2 s(delta_parallel+2delta_perp)."
        ),
        "scaling_consequence": (
            "Since delta_parallel+2delta_perp=(3/2)y^2+O(y^4), the local "
            "common-mode mismatch is 2L(L+1)s y^2 at leading order. With "
            "d=2L+1, s=(1/2)log d, and an A/d allocation, this requires "
            "y=O(d^(-3/2)/sqrt(log d)) inside the certified perturbative window."
        ),
        "claim_boundary": (
            "the theorem is a controlled expansion around perfect common mode. "
            "It does not assert the lower bound after x leaves the Duhamel "
            "window, derive a finite-top matter coupling, control the Davies "
            "limit, or include support stress and gravitational backreaction."
        ),
        "certified_claims": certified_claims,
        "exact_spin_block_records": exact_records,
        "exact_vs_duhamel_cross_checks": perturbative_cross_checks,
        "records": records,
        "next_physics_gate": (
            "derive the same spin-L channel from a smooth local hard-target/top "
            "action and prove a joint localization, lifetime, and backreaction "
            "window at y=O(d^(-3/2)/sqrt(log d))"
        ),
    }
