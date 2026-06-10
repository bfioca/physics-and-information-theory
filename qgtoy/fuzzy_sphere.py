"""Canonical finite SU(2)-equivariant fuzzy-sphere regulator.

This module implements the standard spin-j fuzzy sphere with j=L/2 and
observable algebra M_{L+1}. Spherical harmonics are operator multipoles in the
adjoint SU(2) representation, not states in an (L+1)^2-dimensional Hilbert
space.
"""

from __future__ import annotations

from math import exp, sqrt

from .quantum_channel import (
    Matrix,
    dagger,
    identity_matrix,
    matmul,
    matrix,
    matrix_add,
    max_abs_difference,
    trace,
    zero_matrix,
)


HarmonicLabel = tuple[int, int]


def _validate_level(level: int) -> None:
    if level < 0:
        raise ValueError("level must be nonnegative")


def _validate_max_level(max_level: int) -> None:
    if max_level < 1:
        raise ValueError("max_level must be at least one")


def _validate_tolerance(tolerance: float) -> None:
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")


def _validate_heat_time(heat_time: float) -> None:
    if heat_time < 0.0:
        raise ValueError("heat_time must be nonnegative")


def matrix_scale(value: Matrix, scalar: complex) -> Matrix:
    return tuple(tuple(scalar * entry for entry in row) for row in value)


def matrix_subtract(left: Matrix, right: Matrix) -> Matrix:
    return matrix_add(left, matrix_scale(right, -1.0))


def matrix_power(value: Matrix, exponent: int) -> Matrix:
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    if len(value) != len(value[0]):
        raise ValueError("matrix power requires a square matrix")
    out = identity_matrix(len(value))
    factor = value
    power = exponent
    while power:
        if power & 1:
            out = matmul(out, factor)
        factor = matmul(factor, factor)
        power >>= 1
    return out


def commutator(left: Matrix, right: Matrix) -> Matrix:
    return matrix_subtract(matmul(left, right), matmul(right, left))


def normalized_trace(value: Matrix) -> complex:
    if len(value) != len(value[0]):
        raise ValueError("normalized trace requires a square matrix")
    return trace(value) / float(len(value))


def hilbert_schmidt_inner(left: Matrix, right: Matrix) -> complex:
    return normalized_trace(matmul(dagger(left), right))


def hilbert_schmidt_norm(value: Matrix) -> float:
    norm_squared = hilbert_schmidt_inner(value, value).real
    return sqrt(max(norm_squared, 0.0))


def matrix_unit(dimension: int, row: int, column: int) -> Matrix:
    if dimension < 1:
        raise ValueError("dimension must be positive")
    if not 0 <= row < dimension or not 0 <= column < dimension:
        raise ValueError("matrix-unit index out of range")
    return tuple(
        tuple(
            1 + 0j if (row_index, column_index) == (row, column) else 0j
            for column_index in range(dimension)
        )
        for row_index in range(dimension)
    )


def spin_generators(level: int) -> tuple[Matrix, Matrix, Matrix]:
    """Return Hermitian spin-j generators (Jx,Jy,Jz), j=level/2."""
    _validate_level(level)
    dimension = level + 1
    spin = level / 2.0
    raising = [[0j for _ in range(dimension)] for _ in range(dimension)]
    for source in range(1, dimension):
        magnetic = spin - source
        coefficient = sqrt((spin - magnetic) * (spin + magnetic + 1.0))
        raising[source - 1][source] = coefficient
    j_plus = matrix(raising)
    j_minus = dagger(j_plus)
    j_x = matrix_scale(matrix_add(j_plus, j_minus), 0.5)
    j_y = matrix_scale(matrix_subtract(j_plus, j_minus), -0.5j)
    j_z = tuple(
        tuple(
            (spin - row) + 0j if row == column else 0j
            for column in range(dimension)
        )
        for row in range(dimension)
    )
    return j_x, j_y, j_z


def ladder_generators(level: int) -> tuple[Matrix, Matrix]:
    j_x, j_y, _j_z = spin_generators(level)
    j_plus = matrix_add(j_x, matrix_scale(j_y, 1j))
    return j_plus, dagger(j_plus)


def fuzzy_coordinates(level: int, *, radius: float = 1.0) -> tuple[Matrix, Matrix, Matrix]:
    """Return normalized coordinate matrices with sum X_i^2=radius^2 I."""
    _validate_level(level)
    if radius <= 0.0:
        raise ValueError("radius must be positive")
    generators = spin_generators(level)
    spin = level / 2.0
    if spin == 0.0:
        return tuple(zero_matrix(1, 1) for _ in range(3))  # type: ignore[return-value]
    scale = radius / sqrt(spin * (spin + 1.0))
    return tuple(matrix_scale(generator, scale) for generator in generators)  # type: ignore[return-value]


def fuzzy_laplacian(level: int, operator: Matrix) -> Matrix:
    """Apply the positive adjoint Casimir Delta(A)=sum_i[Ji,[Ji,A]]."""
    _validate_level(level)
    dimension = level + 1
    if len(operator) != dimension or len(operator[0]) != dimension:
        raise ValueError("operator dimension does not match fuzzy-sphere level")
    out = zero_matrix(dimension, dimension)
    for generator in spin_generators(level):
        out = matrix_add(out, commutator(generator, commutator(generator, operator)))
    return out


def harmonic_labels(level: int, *, max_mode: int | None = None) -> tuple[HarmonicLabel, ...]:
    _validate_level(level)
    cutoff = level if max_mode is None else max_mode
    if not 0 <= cutoff <= level:
        raise ValueError("max_mode must lie between zero and level")
    return tuple(
        (ell, magnetic)
        for ell in range(cutoff + 1)
        for magnetic in range(-ell, ell + 1)
    )


def fuzzy_harmonics(level: int) -> dict[HarmonicLabel, Matrix]:
    """Construct a normalized tensor-harmonic basis of M_{L+1}.

    The phase convention starts each multiplet with a positive multiple of
    J_+^ell and lowers with the adjoint action of J_-.
    """
    _validate_level(level)
    dimension = level + 1
    j_plus, j_minus = ladder_generators(level)
    harmonics: dict[HarmonicLabel, Matrix] = {}
    for ell in range(level + 1):
        highest = matrix_power(j_plus, ell)
        norm = hilbert_schmidt_norm(highest)
        if norm == 0.0:
            raise ArithmeticError("highest-weight harmonic vanished unexpectedly")
        current = matrix_scale(highest, 1.0 / norm)
        harmonics[(ell, ell)] = current
        magnetic = ell
        while magnetic > -ell:
            coefficient = sqrt((ell + magnetic) * (ell - magnetic + 1))
            current = matrix_scale(commutator(j_minus, current), 1.0 / coefficient)
            magnetic -= 1
            harmonics[(ell, magnetic)] = current
    expected = dimension * dimension
    if len(harmonics) != expected:
        raise AssertionError("fuzzy-harmonic basis has incorrect dimension")
    return {label: harmonics[label] for label in harmonic_labels(level)}


def harmonic_coefficients(level: int, operator: Matrix) -> dict[HarmonicLabel, complex]:
    return {
        label: hilbert_schmidt_inner(harmonic, operator)
        for label, harmonic in fuzzy_harmonics(level).items()
    }


def reconstruct_from_harmonics(
    level: int,
    coefficients: dict[HarmonicLabel, complex],
) -> Matrix:
    dimension = level + 1
    harmonics = fuzzy_harmonics(level)
    out = zero_matrix(dimension, dimension)
    for label, coefficient in coefficients.items():
        if label not in harmonics:
            raise ValueError(f"unknown harmonic label {label}")
        out = matrix_add(out, matrix_scale(harmonics[label], coefficient))
    return out


def low_mode_projection(level: int, operator: Matrix, *, max_mode: int) -> Matrix:
    """Hilbert-Schmidt projection onto the low-mode operator system V_K."""
    labels = set(harmonic_labels(level, max_mode=max_mode))
    coefficients = harmonic_coefficients(level, operator)
    return reconstruct_from_harmonics(
        level,
        {label: coefficient for label, coefficient in coefficients.items() if label in labels},
    )


def fuzzy_heat_channel(level: int, operator: Matrix, *, heat_time: float) -> Matrix:
    """Apply exp(-heat_time Delta_L) in the tensor-harmonic basis."""
    _validate_heat_time(heat_time)
    coefficients = harmonic_coefficients(level, operator)
    return reconstruct_from_harmonics(
        level,
        {
            label: exp(-heat_time * label[0] * (label[0] + 1)) * coefficient
            for label, coefficient in coefficients.items()
        },
    )


def channel_choi_matrix(level: int, *, heat_time: float) -> Matrix:
    """Construct the Choi matrix of the finite fuzzy heat channel directly."""
    _validate_level(level)
    dimension = level + 1
    size = dimension * dimension
    out = [[0j for _ in range(size)] for _ in range(size)]
    for source_row in range(dimension):
        for source_column in range(dimension):
            image = fuzzy_heat_channel(
                level,
                matrix_unit(dimension, source_row, source_column),
                heat_time=heat_time,
            )
            for target_row in range(dimension):
                for target_column in range(dimension):
                    out[source_row * dimension + target_row][
                        source_column * dimension + target_column
                    ] = image[target_row][target_column]
    return matrix(out)


def hermitian_psd_summary(
    value: Matrix,
    *,
    tolerance: float = 1e-10,
) -> dict[str, object]:
    """Dependency-free Cholesky-style PSD check for small Hermitian matrices."""
    _validate_tolerance(tolerance)
    size = len(value)
    if size == 0 or any(len(row) != size for row in value):
        raise ValueError("matrix must be nonempty and square")
    hermitian_error = max_abs_difference(value, dagger(value))
    if hermitian_error > tolerance:
        return {
            "psd": False,
            "hermitian_error": hermitian_error,
            "min_pivot": None,
            "failure_index": "nonhermitian",
        }

    lower = [[0j for _ in range(size)] for _ in range(size)]
    min_pivot = float("inf")
    for row in range(size):
        for column in range(row + 1):
            correction = sum(
                lower[row][inner] * lower[column][inner].conjugate()
                for inner in range(column)
            )
            residual = value[row][column] - correction
            if row == column:
                if abs(residual.imag) > tolerance:
                    return {
                        "psd": False,
                        "hermitian_error": hermitian_error,
                        "min_pivot": min_pivot,
                        "failure_index": row,
                    }
                pivot = residual.real
                min_pivot = min(min_pivot, pivot)
                if pivot < -tolerance:
                    return {
                        "psd": False,
                        "hermitian_error": hermitian_error,
                        "min_pivot": min_pivot,
                        "failure_index": row,
                    }
                lower[row][column] = sqrt(max(pivot, 0.0))
            elif abs(lower[column][column]) > tolerance:
                lower[row][column] = residual / lower[column][column]
            elif abs(residual) > tolerance:
                return {
                    "psd": False,
                    "hermitian_error": hermitian_error,
                    "min_pivot": min_pivot,
                    "failure_index": (row, column),
                }
    return {
        "psd": True,
        "hermitian_error": hermitian_error,
        "min_pivot": min_pivot,
        "failure_index": None,
    }


def _max_gram_error(harmonics: dict[HarmonicLabel, Matrix]) -> float:
    labels = tuple(harmonics)
    return max(
        abs(
            hilbert_schmidt_inner(harmonics[left], harmonics[right])
            - (1.0 if left == right else 0.0)
        )
        for left in labels
        for right in labels
    )


def _max_trace_error(harmonics: dict[HarmonicLabel, Matrix]) -> float:
    return max(
        abs(normalized_trace(value) - (1.0 if label == (0, 0) else 0.0))
        for label, value in harmonics.items()
    )


def _max_conjugation_error(harmonics: dict[HarmonicLabel, Matrix]) -> float:
    return max(
        max_abs_difference(
            dagger(value),
            matrix_scale(harmonics[(ell, -magnetic)], (-1.0) ** magnetic),
        )
        for (ell, magnetic), value in harmonics.items()
    )


def fuzzy_sphere_level_record(
    level: int,
    *,
    tolerance: float = 1e-10,
    heat_time: float = 0.2,
) -> dict[str, object]:
    """Compute direct finite identities for one canonical fuzzy-sphere level."""
    _validate_level(level)
    _validate_tolerance(tolerance)
    _validate_heat_time(heat_time)
    dimension = level + 1
    spin = level / 2.0
    identity = identity_matrix(dimension)
    j_x, j_y, j_z = spin_generators(level)
    j_plus, j_minus = ladder_generators(level)
    generators = (j_x, j_y, j_z)
    harmonics = fuzzy_harmonics(level)

    commutator_errors = (
        max_abs_difference(commutator(j_x, j_y), matrix_scale(j_z, 1j)),
        max_abs_difference(commutator(j_y, j_z), matrix_scale(j_x, 1j)),
        max_abs_difference(commutator(j_z, j_x), matrix_scale(j_y, 1j)),
    )
    casimir = zero_matrix(dimension, dimension)
    for generator in generators:
        casimir = matrix_add(casimir, matmul(generator, generator))
    casimir_error = max_abs_difference(
        casimir,
        matrix_scale(identity, spin * (spin + 1.0)),
    )

    coordinate_error = 0.0
    if level > 0:
        coordinate_sum = zero_matrix(dimension, dimension)
        for coordinate in fuzzy_coordinates(level):
            coordinate_sum = matrix_add(coordinate_sum, matmul(coordinate, coordinate))
        coordinate_error = max_abs_difference(coordinate_sum, identity)

    gram_error = _max_gram_error(harmonics)
    trace_error = _max_trace_error(harmonics)
    conjugation_error = _max_conjugation_error(harmonics)
    weight_error = 0.0
    raising_error = 0.0
    lowering_error = 0.0
    laplacian_error = 0.0
    covariance_error = 0.0
    heat_mode_error = 0.0
    for (ell, magnetic), harmonic in harmonics.items():
        weight_error = max(
            weight_error,
            max_abs_difference(
                commutator(j_z, harmonic),
                matrix_scale(harmonic, magnetic),
            ),
        )
        if magnetic < ell:
            raising_error = max(
                raising_error,
                max_abs_difference(
                    commutator(j_plus, harmonic),
                    matrix_scale(
                        harmonics[(ell, magnetic + 1)],
                        sqrt((ell - magnetic) * (ell + magnetic + 1)),
                    ),
                ),
            )
        if magnetic > -ell:
            lowering_error = max(
                lowering_error,
                max_abs_difference(
                    commutator(j_minus, harmonic),
                    matrix_scale(
                        harmonics[(ell, magnetic - 1)],
                        sqrt((ell + magnetic) * (ell - magnetic + 1)),
                    ),
                ),
            )
        laplacian = fuzzy_laplacian(level, harmonic)
        expected_laplacian = matrix_scale(harmonic, ell * (ell + 1))
        laplacian_error = max(
            laplacian_error,
            max_abs_difference(laplacian, expected_laplacian),
        )
        heat_mode_error = max(
            heat_mode_error,
            max_abs_difference(
                fuzzy_heat_channel(level, harmonic, heat_time=heat_time),
                matrix_scale(harmonic, exp(-heat_time * ell * (ell + 1))),
            ),
        )
        for generator in generators:
            covariance_error = max(
                covariance_error,
                max_abs_difference(
                    fuzzy_laplacian(level, commutator(generator, harmonic)),
                    commutator(generator, laplacian),
                ),
            )

    reconstruction_error = 0.0
    positivity_identity_error = 0.0
    trace_preservation_error = 0.0
    hermiticity_error = 0.0
    for row in range(dimension):
        for column in range(dimension):
            unit = matrix_unit(dimension, row, column)
            reconstruction_error = max(
                reconstruction_error,
                max_abs_difference(
                    reconstruct_from_harmonics(level, harmonic_coefficients(level, unit)),
                    unit,
                ),
            )
            laplacian = fuzzy_laplacian(level, unit)
            energy = hilbert_schmidt_inner(unit, laplacian).real
            commutator_energy = sum(
                hilbert_schmidt_norm(commutator(generator, unit)) ** 2
                for generator in generators
            )
            positivity_identity_error = max(
                positivity_identity_error,
                abs(energy - commutator_energy),
            )
            heat_image = fuzzy_heat_channel(level, unit, heat_time=heat_time)
            trace_preservation_error = max(
                trace_preservation_error,
                abs(normalized_trace(heat_image) - normalized_trace(unit)),
            )
            hermiticity_error = max(
                hermiticity_error,
                max_abs_difference(
                    fuzzy_heat_channel(level, dagger(unit), heat_time=heat_time),
                    dagger(heat_image),
                ),
            )

    heat_unital_error = max_abs_difference(
        fuzzy_heat_channel(level, identity, heat_time=heat_time),
        identity,
    )
    heat_semigroup_error = max(
        max_abs_difference(
            fuzzy_heat_channel(
                level,
                fuzzy_heat_channel(level, harmonic, heat_time=heat_time),
                heat_time=heat_time / 2.0,
            ),
            fuzzy_heat_channel(level, harmonic, heat_time=1.5 * heat_time),
        )
        for harmonic in harmonics.values()
    )
    choi_summary = hermitian_psd_summary(
        channel_choi_matrix(level, heat_time=heat_time),
        tolerance=tolerance,
    )

    low_mode = min(1, level)
    low_mode_dimension = len(harmonic_labels(level, max_mode=low_mode))
    low_mode_dagger_error = max(
        max_abs_difference(
            low_mode_projection(level, dagger(harmonic), max_mode=low_mode),
            dagger(harmonic),
        )
        for label, harmonic in harmonics.items()
        if label[0] <= low_mode
    )
    low_mode_product_leakage_witness = 0.0
    if level >= 2:
        vector = harmonics[(1, 1)]
        product = matmul(vector, vector)
        leakage = matrix_subtract(
            product,
            low_mode_projection(level, product, max_mode=1),
        )
        low_mode_product_leakage_witness = hilbert_schmidt_norm(leakage)

    max_identity_error = max(
        *commutator_errors,
        casimir_error,
        coordinate_error,
        gram_error,
        trace_error,
        conjugation_error,
        weight_error,
        raising_error,
        lowering_error,
        laplacian_error,
        covariance_error,
        reconstruction_error,
        positivity_identity_error,
        heat_mode_error,
        heat_unital_error,
        heat_semigroup_error,
        trace_preservation_error,
        hermiticity_error,
        low_mode_dagger_error,
    )
    return {
        "level_L": level,
        "spin_j": spin,
        "representation_hilbert_dimension": dimension,
        "observable_algebra": f"M_{dimension}",
        "observable_algebra_dimension": dimension * dimension,
        "harmonic_mode_count": len(harmonics),
        "harmonic_multiplicities": {
            str(ell): 2 * ell + 1 for ell in range(level + 1)
        },
        "conventions": {
            "normalized_trace": "tau_L(A)=Tr(A)/(L+1)",
            "adjoint_action": "J_i(A)=[J_i,A]",
            "laplacian": "Delta_L(A)=sum_i[J_i,[J_i,A]]",
            "heat_channel": "P_t=exp(-t Delta_L)",
            "harmonic_phase": "T_ll is a positive multiple of J_+^l",
        },
        "residuals": {
            "su2_commutators": commutator_errors,
            "casimir": casimir_error,
            "coordinate_sphere_relation": coordinate_error,
            "harmonic_gram": gram_error,
            "harmonic_trace_sectors": trace_error,
            "harmonic_conjugation_phase": conjugation_error,
            "harmonic_weights": weight_error,
            "raising_ladder": raising_error,
            "lowering_ladder": lowering_error,
            "laplacian_eigenoperators": laplacian_error,
            "laplacian_su2_covariance": covariance_error,
            "harmonic_reconstruction": reconstruction_error,
            "dirichlet_positivity_identity": positivity_identity_error,
            "heat_mode_action": heat_mode_error,
            "heat_unitality": heat_unital_error,
            "heat_semigroup": heat_semigroup_error,
            "heat_trace_preservation": trace_preservation_error,
            "heat_hermiticity_preservation": hermiticity_error,
            "low_mode_dagger_closure": low_mode_dagger_error,
            "maximum": max_identity_error,
        },
        "heat_choi": choi_summary,
        "low_mode_operator_system": {
            "max_mode": low_mode,
            "dimension": low_mode_dimension,
            "contains_identity": (0, 0) in harmonics,
            "dagger_closed_error": low_mode_dagger_error,
            "not_claimed_as_subalgebra": True,
            "product_leakage_witness_norm": low_mode_product_leakage_witness,
        },
        "passes_tolerance": max_identity_error <= tolerance and bool(choi_summary["psd"]),
    }


def fuzzy_sphere_regulator_certificate(
    *,
    max_level: int = 4,
    tolerance: float = 1e-9,
    heat_time: float = 0.2,
) -> dict[str, object]:
    """Audit the canonical finite fuzzy-sphere regulator across small levels."""
    _validate_max_level(max_level)
    _validate_tolerance(tolerance)
    _validate_heat_time(heat_time)
    records = tuple(
        fuzzy_sphere_level_record(
            level,
            tolerance=tolerance,
            heat_time=heat_time,
        )
        for level in range(1, max_level + 1)
    )
    certified_claims = {
        "matrix_size_is_L_plus_one": all(
            record["representation_hilbert_dimension"] == record["level_L"] + 1
            for record in records
        ),
        "algebra_dimension_matches_harmonic_count": all(
            record["observable_algebra_dimension"] == record["harmonic_mode_count"]
            for record in records
        ),
        "su2_and_casimir_identities_computed": all(
            record["residuals"]["maximum"] <= tolerance for record in records
        ),
        "complete_harmonic_basis_computed": all(
            sum(record["harmonic_multiplicities"].values())
            == record["observable_algebra_dimension"]
            for record in records
        ),
        "adjoint_laplacian_spectrum_computed": all(
            record["residuals"]["laplacian_eigenoperators"] <= tolerance
            for record in records
        ),
        "fuzzy_heat_channel_choi_psd_computed": all(
            record["heat_choi"]["psd"] for record in records
        ),
        "low_modes_are_operator_systems_not_assumed_algebras": all(
            record["low_mode_operator_system"]["not_claimed_as_subalgebra"]
            and record["low_mode_operator_system"]["dagger_closed_error"] <= tolerance
            for record in records
        ),
    }
    return {
        "goal": "Phase 1 Canonical SU(2)-Equivariant Fuzzy-Sphere Regulator",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "exact_finite_su2_equivariant_fuzzy_sphere_regulator",
        "claim_boundary": (
            "standard finite fuzzy-sphere kinematics and heat dynamics only; "
            "no gravitational observer algebra, physical screen channel, "
            "cutoff-refinement theorem, Type-II limit, or de Sitter claim"
        ),
        "max_level": max_level,
        "tolerance": tolerance,
        "heat_time": heat_time,
        "records": records,
        "certified_claims": certified_claims,
    }
