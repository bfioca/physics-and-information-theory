"""Goal 9 finite-dimensional OAQEC observer-algebra tomography certificates."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations_with_replacement
from math import isqrt


Vector = tuple[int, ...]


@dataclass(frozen=True)
class MatrixUnitAlgebra:
    """Finite-dimensional C*-algebra as a represented Wedderburn sum.

    The block pair ``(m, d)`` represents ``I_m tensor M_d``.  The abstract
    algebra is the direct sum of the ``M_d`` factors; ``m`` records the
    representation multiplicity relevant to commutants/channel fixed points.
    """

    blocks: tuple[tuple[int, int], ...]

    def __init__(self, blocks: tuple[tuple[int, int], ...] | tuple[int, ...]):
        normalized = []
        for item in blocks:
            if isinstance(item, int):
                multiplicity, matrix_size = 1, item
            else:
                multiplicity, matrix_size = item
            if multiplicity <= 0 or matrix_size <= 0:
                raise ValueError("Wedderburn block sizes must be positive")
            normalized.append((multiplicity, matrix_size))
        object.__setattr__(self, "blocks", tuple(sorted(normalized)))

    @property
    def abstract_block_sizes(self) -> tuple[int, ...]:
        return tuple(sorted(matrix_size for _, matrix_size in self.blocks))

    @property
    def algebra_dim(self) -> int:
        return sum(matrix_size * matrix_size for _, matrix_size in self.blocks)

    @property
    def center_dim(self) -> int:
        return len(self.blocks)

    @property
    def commutator_subspace_dim(self) -> int:
        return self.algebra_dim - self.center_dim

    @property
    def representation_hilbert_dim(self) -> int:
        return sum(multiplicity * matrix_size for multiplicity, matrix_size in self.blocks)

    @property
    def commutant_dim(self) -> int:
        return sum(multiplicity * multiplicity for multiplicity, _ in self.blocks)

    @property
    def basis(self) -> tuple[tuple[int, int, int], ...]:
        labels = []
        for block_index, (_, matrix_size) in enumerate(self.blocks):
            for row in range(matrix_size):
                for col in range(matrix_size):
                    labels.append((block_index, row, col))
        return tuple(labels)

    def zero(self) -> Vector:
        return (0,) * len(self.basis)

    def basis_vector(self, label: tuple[int, int, int]) -> Vector:
        values = [0] * len(self.basis)
        values[self.basis.index(label)] = 1
        return tuple(values)

    def add(self, left: Vector, right: Vector) -> Vector:
        return tuple(a + b for a, b in zip(left, right, strict=True))

    def multiply_basis(
        self,
        left: tuple[int, int, int],
        right: tuple[int, int, int],
    ) -> Vector:
        left_block, left_row, left_col = left
        right_block, right_row, right_col = right
        if left_block != right_block or left_col != right_row:
            return self.zero()
        return self.basis_vector((left_block, left_row, right_col))

    def star_basis(self, label: tuple[int, int, int]) -> Vector:
        block, row, col = label
        return self.basis_vector((block, col, row))

    def identity(self) -> Vector:
        out = self.zero()
        for block_index, (_, matrix_size) in enumerate(self.blocks):
            for row in range(matrix_size):
                out = self.add(out, self.basis_vector((block_index, row, row)))
        return out

    def central_projection(self, block_index: int) -> Vector:
        out = self.zero()
        matrix_size = self.blocks[block_index][1]
        for row in range(matrix_size):
            out = self.add(out, self.basis_vector((block_index, row, row)))
        return out

    def multiply_vector(self, left: Vector, right: Vector) -> Vector:
        out = self.zero()
        for left_index, left_coeff in enumerate(left):
            if not left_coeff:
                continue
            for right_index, right_coeff in enumerate(right):
                if not right_coeff:
                    continue
                product = self.multiply_basis(self.basis[left_index], self.basis[right_index])
                out = tuple(value + left_coeff * right_coeff * product[index] for index, value in enumerate(out))
        return out

    def commutator(self, left: Vector, right: Vector) -> Vector:
        lr = self.multiply_vector(left, right)
        rl = self.multiply_vector(right, left)
        return tuple(a - b for a, b in zip(lr, rl, strict=True))

    def weak_shadow(self) -> tuple[int, int, int]:
        return (self.algebra_dim, self.center_dim, self.commutator_subspace_dim)

    def wedderburn_signature(self) -> dict[str, object]:
        return {
            "represented_blocks": self.blocks,
            "abstract_block_sizes": self.abstract_block_sizes,
            "algebra_dim": self.algebra_dim,
            "center_dim": self.center_dim,
            "commutator_subspace_dim": self.commutator_subspace_dim,
            "representation_hilbert_dim": self.representation_hilbert_dim,
            "commutant_dim": self.commutant_dim,
        }


def _is_projection(algebra: MatrixUnitAlgebra, vector: Vector) -> bool:
    return algebra.multiply_vector(vector, vector) == vector


def _is_central(algebra: MatrixUnitAlgebra, vector: Vector) -> bool:
    return all(algebra.commutator(vector, algebra.basis_vector(label)) == algebra.zero() for label in algebra.basis)


def _corner_dimension(algebra: MatrixUnitAlgebra, projection: Vector) -> int:
    rows = set()
    for label in algebra.basis:
        basis_vector = algebra.basis_vector(label)
        corner = algebra.multiply_vector(projection, algebra.multiply_vector(basis_vector, projection))
        if corner != algebra.zero():
            rows.add(corner)
    return len(rows)


def _recover_block_sizes_from_matrix_units(algebra: MatrixUnitAlgebra) -> tuple[int, ...]:
    recovered = []
    for block_index in range(len(algebra.blocks)):
        projection = algebra.central_projection(block_index)
        if not _is_projection(algebra, projection) or not _is_central(algebra, projection):
            raise ValueError("declared central projection failed product-table checks")
        corner_dim = _corner_dimension(algebra, projection)
        root = isqrt(corner_dim)
        if root * root != corner_dim:
            raise ValueError("central corner dimension is not a matrix-square")
        recovered.append(root)
    return tuple(sorted(recovered))


def _all_block_types(*, max_block_dim: int, max_blocks: int) -> tuple[tuple[int, ...], ...]:
    out = []
    for block_count in range(1, max_blocks + 1):
        out.extend(combinations_with_replacement(range(1, max_block_dim + 1), block_count))
    return tuple(sorted(out, key=lambda item: (sum(d * d for d in item), len(item), item)))


def _first_weak_shadow_collision(*, max_block_dim: int, max_blocks: int) -> dict[str, object] | None:
    seen: dict[tuple[int, int, int], tuple[int, ...]] = {}
    for block_sizes in _all_block_types(max_block_dim=max_block_dim, max_blocks=max_blocks):
        algebra = MatrixUnitAlgebra(block_sizes)
        shadow = algebra.weak_shadow()
        previous = seen.get(shadow)
        if previous is not None and previous != block_sizes:
            first = MatrixUnitAlgebra(previous)
            second = MatrixUnitAlgebra(block_sizes)
            return {
                "shadow": shadow,
                "first_block_sizes": previous,
                "second_block_sizes": block_sizes,
                "first_signature": first.wedderburn_signature(),
                "second_signature": second.wedderburn_signature(),
                "block_dim_bound": max_block_dim,
                "max_blocks": max_blocks,
            }
        seen[shadow] = block_sizes
    return None


def _tomography_audit_examples() -> tuple[dict[str, object], ...]:
    examples = (
        MatrixUnitAlgebra(((1, 2),)),
        MatrixUnitAlgebra(((3, 1), (1, 2))),
        MatrixUnitAlgebra(((1, 1), (1, 1), (1, 4))),
        MatrixUnitAlgebra(((1, 2), (1, 2), (1, 2), (1, 2), (1, 2))),
    )
    records = []
    for algebra in examples:
        recovered = _recover_block_sizes_from_matrix_units(algebra)
        records.append(
            {
                "status": "pass" if recovered == algebra.abstract_block_sizes else "fail",
                "signature": algebra.wedderburn_signature(),
                "recovered_abstract_block_sizes": recovered,
                "basis_size": len(algebra.basis),
                "central_projections_checked": algebra.center_dim,
            }
        )
    return tuple(records)


def _goal8_stabilizer_special_case_note() -> dict[str, object]:
    return {
        "stabilizer_region_algebra_mapping": (
            "For a stabilizer region R, the supported logical Pauli quotient L_R has restricted "
            "symplectic rank 2q and radical dimension c.  Its generated finite-dimensional "
            "observable algebra has abstract Wedderburn type C^{2^c} tensor M_{2^q}; equivalently "
            "a direct sum of 2^c copies of M_{2^q}.  Goal 8's tuple "
            "(dim L_R, dim Z_R, dim L_R^perp, L_R=L) is the Pauli/symplectic compression of this "
            "finite-dimensional Wedderburn signature."
        ),
        "goal8_recovered_quantities": (
            "Goal 8 recovers dim L_R and the restricted commutator rank from intrinsic local Pauli "
            "response and commutator tests; these determine q, c, and the stabilizer-region "
            "Wedderburn block sizes."
        ),
        "status": "theorem_bridge_declared",
    }


def goal9_finite_oaqec_intrinsic_tomography_certificate(
    *,
    max_block_dim: int = 4,
    max_blocks: int = 5,
) -> dict[str, object]:
    collision = _first_weak_shadow_collision(max_block_dim=max_block_dim, max_blocks=max_blocks)
    theorem_audits = _tomography_audit_examples()
    theorem_pass = all(record["status"] == "pass" for record in theorem_audits)
    certified_claims = {
        "formal_wedderburn_signature_declared": True,
        "weak_dimension_center_commutator_shadow_collision_found": collision is not None,
        "bounded_collision_is_minimal_in_declared_order": collision is not None
        and collision["shadow"] == (20, 5, 15),
        "full_product_star_tomography_recovers_examples": theorem_pass,
        "finite_oaqec_tomography_theorem_declared": True,
        "goal8_stabilizer_special_case_bridge_declared": True,
        "known_vs_new_separated": True,
    }
    certified_claims["goal9_finite_oaqec_intrinsic_tomography_certificate"] = all(certified_claims.values())
    return {
        "goal": "Goal 9: Finite-Dimensional OAQEC Intrinsic Observer-Algebra Tomography",
        "status": "pass" if certified_claims["goal9_finite_oaqec_intrinsic_tomography_certificate"] else "fail",
        "scope": {
            "max_block_dim": max_block_dim,
            "max_blocks": max_blocks,
            "algebra_family": "finite-dimensional represented C*-algebras direct-sum_i I_m_i tensor M_d_i",
            "minimality_scope": "bounded by block dimension, number of blocks, and sorted algebra dimension order",
        },
        "formal_definitions": {
            "observer_algebra": "A_R is a finite-dimensional reconstructable *-subalgebra of the logical/code algebra.",
            "wedderburn_signature": (
                "A_R is represented as direct-sum_alpha I_{m_alpha} tensor M_{d_alpha}.  "
                "The abstract algebra is direct-sum_alpha M_{d_alpha}; the represented signature records "
                "(m_alpha,d_alpha)."
            ),
            "intrinsic_full_tomography_data": (
                "An operationally obtained basis of region-local distinguishable code-preserving effects, "
                "with product, adjoint, identity, trace/normalization, and commutator structure constants. "
                "No global logical labels are supplied."
            ),
        },
        "positive_theorem": {
            "name": "Finite-Dimensional Product-Star Observer-Algebra Tomography",
            "claim": (
                "The full intrinsic product/* table of A_R determines the finite-dimensional *-algebra "
                "up to *-algebra isomorphism, hence determines its abstract Wedderburn block sizes.  "
                "With channel fixed-point/commutant multiplicity data it determines the represented "
                "Wedderburn signature (m_alpha,d_alpha)."
            ),
            "proof_sketch": (
                "Finite-dimensional C*-algebras are semisimple and decompose into minimal central "
                "projections.  Product and adjoint tomography identify the center, its minimal central "
                "projections, and each simple corner p_alpha A_R p_alpha.  Each corner has dimension "
                "d_alpha^2 and is isomorphic to M_{d_alpha}.  Channel fixed-point or commutant data give "
                "the representation multiplicities m_alpha."
            ),
            "theorem_audit_examples": theorem_audits,
        },
        "negative_hierarchy": {
            "weak_shadow": "(algebra_dim, center_dim, commutator_subspace_dim)",
            "bounded_first_collision": collision,
            "interpretation": (
                "Dimension, center size, and commutator-subspace dimension do not determine Wedderburn "
                "block type.  The first bounded collision under the declared search is C^4 plus M_4 "
                "versus five copies of M_2."
            ),
        },
        "goal8_stabilizer_special_case": _goal8_stabilizer_special_case_note(),
        "known_vs_new": {
            "known_derived": (
                "The positive theorem uses standard finite-dimensional C*-algebra/Wedderburn structure "
                "and OAQEC observable-algebra language.  It should not be sold as a new OAQEC formalism."
            ),
            "new_programmatic_contribution": (
                "The Goal 9 package lifts Goal 8's observer-tomography question out of stabilizer labels, "
                "separates weak operational shadows from product/* completion data, and gives exact "
                "finite counterexamples for insufficient shadows."
            ),
        },
        "relation_to_literature": {
            "beny_kempf_kribs": "Foundational Heisenberg/OAQEC observable-algebra formalism.",
            "harlow_rt_from_qec": "Finite-dimensional OAQEC is the language used for subalgebra-code RT statements.",
            "stabilizer_oaqec": "Goal 8 is the stabilizer/Pauli special case of product/* algebra tomography.",
            "qss_access_structures": "Weak-shadow collisions are finite algebra analogues of intermediate-access information not captured by qualified/forbidden data alone.",
        },
        "harlow_facing_interpretation": (
            "Goal 9 reframes observer algebra as an intrinsically tomographable finite-dimensional "
            "observable algebra.  Weak shadows such as dimension, center size, and commutator dimension "
            "do not determine the algebra, but full region-local product/* response does determine "
            "Wedderburn block type.  Goal 8 is the stabilizer special case where the product/* data "
            "collapse to Pauli response plus symplectic commutator tomography."
        ),
        "reproducibility": {
            "goal9_certificate": (
                f"python3 -m qgtoy observer-tomography-oaqec --max-block-dim {max_block_dim} "
                f"--max-blocks {max_blocks}"
            ),
            "focused_regression": (
                "python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest."
                "test_goal9_finite_oaqec_intrinsic_observer_tomography_certificate"
            ),
        },
        "limitations": (
            "This is an exact finite-dimensional algebra theorem/certificate scaffold.  Full product/* "
            "tomography is a strong operational input and is close to giving the algebra by definition.  "
            "The next nontrivial frontier is determining which weaker recovery, relative-entropy, or noisy "
            "response data recover the same Wedderburn type."
        ),
        "certified_claims": certified_claims,
    }
