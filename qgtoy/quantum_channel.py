"""Small dense quantum-channel verifier for the bilayer research program.

The stabilizer verifier is ideal for exact entropy and reconstruction questions,
but an operational channel claim should also be checked from an explicit CPTP
map.  This module intentionally stays dependency-free and only targets the
small logical systems used by the finite certificates.
"""

from __future__ import annotations

from math import sqrt
from typing import Iterable, Sequence

from .gf2 import nullspace, rank, rref
from .stabilizer import combine_rows, symplectic_dual, symplectic_product


Matrix = tuple[tuple[complex, ...], ...]


def matrix(rows: Iterable[Iterable[complex]]) -> Matrix:
    out = tuple(tuple(complex(value) for value in row) for row in rows)
    if not out or not out[0] or any(len(row) != len(out[0]) for row in out):
        raise ValueError("matrix rows must form a nonempty rectangle")
    return out


def zero_matrix(rows: int, columns: int) -> Matrix:
    return tuple(tuple(0j for _ in range(columns)) for _ in range(rows))


def identity_matrix(dimension: int) -> Matrix:
    return tuple(
        tuple(1 + 0j if row == column else 0j for column in range(dimension))
        for row in range(dimension)
    )


def dagger(value: Matrix) -> Matrix:
    return tuple(
        tuple(value[row][column].conjugate() for row in range(len(value)))
        for column in range(len(value[0]))
    )


def matmul(left: Matrix, right: Matrix) -> Matrix:
    if len(left[0]) != len(right):
        raise ValueError("matrix dimensions do not compose")
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    if len(left) != len(right) or len(left[0]) != len(right[0]):
        raise ValueError("matrix dimensions must match")
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(len(left[0])))
        for row in range(len(left))
    )


def trace(value: Matrix) -> complex:
    if len(value) != len(value[0]):
        raise ValueError("trace requires a square matrix")
    return sum(value[index][index] for index in range(len(value)))


def max_abs_difference(left: Matrix, right: Matrix) -> float:
    if len(left) != len(right) or len(left[0]) != len(right[0]):
        raise ValueError("matrix dimensions must match")
    return max(
        abs(left[row][column] - right[row][column])
        for row in range(len(left))
        for column in range(len(left[0]))
    )


def complex_matrix_rank(value: Matrix, *, tolerance: float = 1e-10) -> int:
    rows = [list(row) for row in value]
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        if pivot_row >= row_count:
            break
        pivot = max(range(pivot_row, row_count), key=lambda row: abs(rows[row][column]))
        if abs(rows[pivot][column]) <= tolerance:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot_value for entry in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = rows[row][column]
            if abs(factor) <= tolerance:
                continue
            rows[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def compose_kraus(
    after: Sequence[Matrix], before: Sequence[Matrix]
) -> tuple[Matrix, ...]:
    return tuple(matmul(left, right) for left in after for right in before)


def apply_kraus(kraus: Sequence[Matrix], operator: Matrix) -> Matrix:
    output_dimension = len(kraus[0])
    out = zero_matrix(output_dimension, output_dimension)
    for item in kraus:
        out = matrix_add(out, matmul(matmul(item, operator), dagger(item)))
    return out


def trace_preserving_error(kraus: Sequence[Matrix]) -> float:
    input_dimension = len(kraus[0][0])
    total = zero_matrix(input_dimension, input_dimension)
    for item in kraus:
        total = matrix_add(total, matmul(dagger(item), item))
    return max_abs_difference(total, identity_matrix(input_dimension))


def isometry_error(isometry: Matrix) -> float:
    input_dimension = len(isometry[0])
    return max_abs_difference(
        matmul(dagger(isometry), isometry),
        identity_matrix(input_dimension),
    )


def reduced_channel_kraus(
    isometry: Matrix,
    *,
    left_dimension: int,
    right_dimension: int,
    keep: str,
) -> tuple[Matrix, ...]:
    """Trace one output leg of an isometry to obtain the other leg's channel."""
    if len(isometry) != left_dimension * right_dimension:
        raise ValueError(
            "isometry output dimension does not match the bipartite dimensions"
        )
    input_dimension = len(isometry[0])
    if keep == "left":
        return tuple(
            matrix(
                (
                    isometry[left * right_dimension + right][input_]
                    for input_ in range(input_dimension)
                )
                for left in range(left_dimension)
            )
            for right in range(right_dimension)
        )
    if keep == "right":
        return tuple(
            matrix(
                (
                    isometry[left * right_dimension + right][input_]
                    for input_ in range(input_dimension)
                )
                for right in range(right_dimension)
            )
            for left in range(left_dimension)
        )
    raise ValueError("keep must be 'left' or 'right'")


def choi_matrix(kraus: Sequence[Matrix]) -> Matrix:
    input_dimension = len(kraus[0][0])
    output_dimension = len(kraus[0])
    dimension = input_dimension * output_dimension
    out = [[0j for _ in range(dimension)] for _ in range(dimension)]
    for item in kraus:
        vector = tuple(
            item[output][input_]
            for input_ in range(input_dimension)
            for output in range(output_dimension)
        )
        for row in range(dimension):
            for column in range(dimension):
                out[row][column] += vector[row] * vector[column].conjugate()
    return matrix(out)


def entanglement_fidelity_to_unitary(kraus: Sequence[Matrix], unitary: Matrix) -> float:
    dimension = len(unitary)
    if (
        len(unitary[0]) != dimension
        or len(kraus[0]) != dimension
        or len(kraus[0][0]) != dimension
    ):
        raise ValueError("unitary comparison requires a square channel")
    inverse = dagger(unitary)
    return sum(abs(trace(matmul(inverse, item))) ** 2 for item in kraus) / (
        dimension * dimension
    )


def average_gate_fidelity(entanglement_fidelity: float, dimension: int) -> float:
    return (dimension * entanglement_fidelity + 1.0) / (dimension + 1.0)


def permute_bits(value: int, permutation: Sequence[int]) -> int:
    out = 0
    for source, target in enumerate(permutation):
        if (value >> source) & 1:
            out |= 1 << target
    return out


def route_bits(value: int, routing: Sequence[int]) -> int:
    """Read physical bit ``routing[i]`` into logical output bit ``i``."""
    out = 0
    for logical, physical in enumerate(routing):
        if (value >> physical) & 1:
            out |= 1 << logical
    return out


def permutation_matrix(permutation: Sequence[int]) -> Matrix:
    dimension = 1 << len(permutation)
    rows = [[0j for _ in range(dimension)] for _ in range(dimension)]
    for basis in range(dimension):
        rows[permute_bits(basis, permutation)][basis] = 1 + 0j
    return matrix(rows)


def pauli_matrix(label: int, qubits: int) -> Matrix:
    dimension = 1 << qubits
    mask = dimension - 1
    x = label & mask
    z = label >> qubits
    y_count = (x & z).bit_count()
    y_phase = (1j) ** y_count
    rows = [[0j for _ in range(dimension)] for _ in range(dimension)]
    for basis in range(dimension):
        target = basis ^ x
        sign = -1 if ((z & basis).bit_count() & 1) else 1
        rows[target][basis] = y_phase * sign
    return matrix(rows)


def pauli_string(label: int, qubits: int) -> str:
    mask = (1 << qubits) - 1
    x = label & mask
    z = label >> qubits
    letters = []
    for qubit in range(qubits):
        bits = ((x >> qubit) & 1, (z >> qubit) & 1)
        letters.append({(0, 0): "I", (1, 0): "X", (0, 1): "Z", (1, 1): "Y"}[bits])
    return "".join(letters)


def pauli_transfer_coefficient(
    kraus: Sequence[Matrix],
    output_label: int,
    input_label: int,
    qubits: int,
) -> float:
    dimension = 1 << qubits
    output_pauli = pauli_matrix(output_label, qubits)
    input_pauli = pauli_matrix(input_label, qubits)
    value = trace(matmul(output_pauli, apply_kraus(kraus, input_pauli))) / dimension
    if abs(value.imag) > 1e-9:
        raise ValueError(
            "Hermiticity-preserving channel produced a complex Pauli transfer coefficient"
        )
    return float(value.real)


def _validate_permutation(value: Sequence[int], name: str) -> tuple[int, ...]:
    out = tuple(value)
    if sorted(out) != list(range(len(out))):
        raise ValueError(f"{name} must be a permutation")
    return out


def teleportation_kraus(
    resource_pairing: Sequence[int],
    decoder_routing: Sequence[int],
) -> tuple[Matrix, ...]:
    """Construct the logical channel from Bell projections and feed-forward.

    ``resource_pairing[i]`` is the right mouth entangled with left mouth ``i``.
    ``decoder_routing[i]`` is the right mouth corrected and routed to logical
    output ``i`` using Bell-measurement outcome ``i``.
    """
    pairing = _validate_permutation(resource_pairing, "resource_pairing")
    routing = _validate_permutation(decoder_routing, "decoder_routing")
    if len(pairing) != len(routing):
        raise ValueError("resource and decoder permutations must have equal size")
    mouths = len(pairing)
    if mouths > 3:
        raise ValueError(
            "dense teleportation verification is limited to at most three mouths"
        )
    dimension = 1 << mouths
    out: list[Matrix] = []
    for z_outcome in range(dimension):
        for x_outcome in range(dimension):
            rows = [[0j for _ in range(dimension)] for _ in range(dimension)]
            routed_x = permute_bits(x_outcome, routing)
            for input_basis in range(dimension):
                uncorrected = permute_bits(input_basis ^ x_outcome, pairing)
                corrected = uncorrected ^ routed_x
                logical_output = route_bits(corrected, routing)
                bell_phase = -1 if ((z_outcome & input_basis).bit_count() & 1) else 1
                correction_phase = (
                    -1 if ((z_outcome & logical_output).bit_count() & 1) else 1
                )
                rows[logical_output][input_basis] = (
                    bell_phase * correction_phase / dimension
                )
            out.append(matrix(rows))
    return tuple(out)


def _effective_output_permutation(
    pairing: Sequence[int], routing: Sequence[int]
) -> tuple[int, ...]:
    inverse_routing = [0] * len(routing)
    for logical, physical in enumerate(routing):
        inverse_routing[physical] = logical
    return tuple(inverse_routing[pairing[input_]] for input_ in range(len(pairing)))


def _identify_pauli(
    value: Matrix, qubits: int, *, tolerance: float = 1e-9
) -> tuple[int, complex]:
    dimension = 1 << qubits
    best_label = 0
    best_coefficient = 0j
    for label in range(1 << (2 * qubits)):
        candidate = pauli_matrix(label, qubits)
        coefficient = trace(matmul(dagger(candidate), value)) / dimension
        if abs(coefficient) > abs(best_coefficient):
            best_label = label
            best_coefficient = coefficient
    best_pauli = pauli_matrix(best_label, qubits)
    residual = tuple(
        tuple(
            value[row][column] - best_coefficient * best_pauli[row][column]
            for column in range(dimension)
        )
        for row in range(dimension)
    )
    if max(abs(entry) for row in residual for entry in row) > tolerance:
        raise ValueError(
            "teleportation Kraus operator is not proportional to a Pauli after routing correction"
        )
    return best_label, best_coefficient


def teleportation_channel_certificate(
    resource_pairing: Sequence[int],
    decoder_routing: Sequence[int],
) -> dict[str, object]:
    pairing = _validate_permutation(resource_pairing, "resource_pairing")
    routing = _validate_permutation(decoder_routing, "decoder_routing")
    kraus = teleportation_kraus(pairing, routing)
    mouths = len(pairing)
    dimension = 1 << mouths
    effective_permutation = _effective_output_permutation(pairing, routing)
    effective_unitary = permutation_matrix(effective_permutation)
    unrouted_kraus = tuple(matmul(dagger(effective_unitary), item) for item in kraus)

    error_probabilities: dict[int, float] = {}
    for item in unrouted_kraus:
        label, coefficient = _identify_pauli(item, mouths)
        if abs(coefficient) > 1e-12:
            error_probabilities[label] = (
                error_probabilities.get(label, 0.0) + abs(coefficient) ** 2
            )
    error_basis = rref((label for label in error_probabilities if label), 2 * mouths)
    commutant_basis = nullspace(
        (symplectic_dual(label, mouths) for label in error_basis),
        2 * mouths,
    )
    form_rows = []
    for left in commutant_basis:
        row = 0
        for index, right in enumerate(commutant_basis):
            if symplectic_product(left, right, mouths):
                row |= 1 << index
        form_rows.append(row)
    symplectic_rank = rank(form_rows, len(commutant_basis)) if commutant_basis else 0
    center_coefficients = (
        nullspace(form_rows, len(commutant_basis)) if commutant_basis else ()
    )
    center_basis = tuple(
        combine_rows(coefficients, commutant_basis)
        for coefficients in center_coefficients
    )

    fixed_port_rows = []
    fixed_port_count = 0
    for mouth in range(mouths):
        x = 1 << mouth
        z = 1 << (mouths + mouth)
        y = x | z
        diagonal = tuple(
            pauli_transfer_coefficient(kraus, label, label, mouths)
            for label in (x, y, z)
        )
        perfect = all(abs(value - 1.0) < 1e-9 for value in diagonal)
        fixed_port_count += int(perfect)
        fixed_port_rows.append(
            {
                "input_output_mouth": mouth,
                "pauli_transfer_diagonal_XYZ": diagonal,
                "perfect_fixed_port": perfect,
                "average_fidelity_to_identity": 0.5 + sum(diagonal) / 6.0,
            }
        )

    choi = choi_matrix(kraus)
    identity_fidelity = entanglement_fidelity_to_unitary(
        kraus, identity_matrix(dimension)
    )
    permutation_fidelity = entanglement_fidelity_to_unitary(kraus, effective_unitary)
    return {
        "resource_pairing": pairing,
        "decoder_routing": routing,
        "effective_output_permutation": effective_permutation,
        "dimensions": {"input": dimension, "output": dimension},
        "kraus_operator_count": len(kraus),
        "trace_preserving_error": trace_preserving_error(kraus),
        "choi": {
            "trace": float(trace(choi).real),
            "rank": complex_matrix_rank(choi),
            "hermiticity_error": max_abs_difference(choi, dagger(choi)),
        },
        "fidelity": {
            "entanglement_fidelity_to_identity": identity_fidelity,
            "average_gate_fidelity_to_identity": average_gate_fidelity(
                identity_fidelity, dimension
            ),
            "entanglement_fidelity_to_effective_permutation": permutation_fidelity,
        },
        "fixed_port_transmission": {
            "perfect_qubits": fixed_port_count,
            "ports": tuple(fixed_port_rows),
        },
        "post_permutation_noise": {
            "pauli_error_basis": tuple(
                pauli_string(label, mouths) for label in error_basis
            ),
            "pauli_error_distribution": tuple(
                {
                    "pauli": pauli_string(label, mouths),
                    "probability": probability,
                }
                for label, probability in sorted(error_probabilities.items())
            ),
        },
        "preserved_operator_algebra": {
            "pauli_dimension": len(commutant_basis),
            "symplectic_rank": symplectic_rank,
            "center_dimension": len(center_basis),
            "exact_joint_noiseless_qubits": symplectic_rank // 2,
            "commutant_basis": tuple(
                pauli_string(label, mouths) for label in commutant_basis
            ),
            "center_basis": tuple(
                pauli_string(label, mouths) for label in center_basis
            ),
        },
    }


def erasure_channel_kraus(success_probability: float) -> tuple[Matrix, ...]:
    if not 0.0 <= success_probability <= 1.0:
        raise ValueError("success_probability must lie in [0,1]")
    keep = sqrt(success_probability)
    erase = sqrt(1.0 - success_probability)
    return (
        matrix(((keep, 0), (0, keep), (0, 0))),
        matrix(((0, 0), (0, 0), (erase, 0))),
        matrix(((0, 0), (0, 0), (0, erase))),
    )


def coherent_bilayer_isometry(north_probability: float) -> Matrix:
    """Route a qubit coherently to north or south, with an orthogonal erasure flag."""
    if not 0.0 <= north_probability <= 1.0:
        raise ValueError("north_probability must lie in [0,1]")
    north_amplitude = sqrt(north_probability)
    south_amplitude = sqrt(1.0 - north_probability)
    screen_dimension = 3
    erasure = 2
    rows = [[0j for _ in range(2)] for _ in range(screen_dimension * screen_dimension)]
    for basis in range(2):
        rows[basis * screen_dimension + erasure][basis] = north_amplitude
        rows[erasure * screen_dimension + basis][basis] = south_amplitude
    return matrix(rows)


def coherent_bilayer_screen_kraus(
    north_probability: float,
    *,
    screen: str,
) -> tuple[Matrix, ...]:
    isometry = coherent_bilayer_isometry(north_probability)
    if screen == "north":
        return reduced_channel_kraus(
            isometry,
            left_dimension=3,
            right_dimension=3,
            keep="left",
        )
    if screen == "south":
        return reduced_channel_kraus(
            isometry,
            left_dimension=3,
            right_dimension=3,
            keep="right",
        )
    raise ValueError("screen must be 'north' or 'south'")


def erasure_replacement_decoder_kraus() -> tuple[Matrix, ...]:
    return (
        matrix(((1, 0, 0), (0, 1, 0))),
        matrix(((0, 0, 1 / sqrt(2)), (0, 0, 0))),
        matrix(((0, 0, 0), (0, 0, 1 / sqrt(2)))),
    )


def recovered_erasure_channel_kraus(success_probability: float) -> tuple[Matrix, ...]:
    return compose_kraus(
        erasure_replacement_decoder_kraus(), erasure_channel_kraus(success_probability)
    )


def recovered_coherent_bilayer_screen_kraus(
    north_probability: float,
    *,
    screen: str,
) -> tuple[Matrix, ...]:
    return compose_kraus(
        erasure_replacement_decoder_kraus(),
        coherent_bilayer_screen_kraus(north_probability, screen=screen),
    )
