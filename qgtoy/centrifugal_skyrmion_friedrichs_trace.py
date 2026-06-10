"""Local finite-energy origin trace for the centrifugal weak form.

For a solution branch ``y=x^p(v+O(x^2))``, the regular weak-form scaling

``C=Cbar(x^2)``, ``M=x Mbar(x^2)``, ``P=x^2 Pbar(x^2)``

gives a quadratic density ``H[y]=Q_p(b) x^(2p)+O(x^(2p+2))``.  This module
computes ``Q_p`` exactly on all four indicial branches.  Every coefficient is
a polynomial in the origin slope, and its strict positivity makes local form
integrability equivalent to ``p > -1/2``.

The conclusion is deliberately about solution germs of the symmetric local
weak-form equation.  It identifies germs satisfying the finite-energy origin
condition associated with a Friedrichs realization, but does not classify the
full form domain or prove global semiboundedness.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .centrifugal_skyrmion_origin import (
    Polynomial,
    _indicial_matrix,
    _poly,
    _poly_add,
    _poly_mul,
    _poly_scale,
    centrifugal_origin_leading_hessian,
)
from .validated_centrifugal_physical_origin_transfer import (
    IntervalVector2,
    ValidatedPhysicalOriginTransfer,
)
from .validated_interval import RationalInterval


VectorPolynomial = tuple[Polynomial, Polynomial]


@dataclass(frozen=True)
class IndicialEnergyBranch:
    """Exact leading data for one one-dimensional indicial eigenspace."""

    exponent: int
    mode: VectorPolynomial
    indicial_residual: VectorPolynomial
    leading_energy_polynomial: Polynomial
    finite_local_energy: bool


@dataclass(frozen=True)
class FriedrichsEndpointCell:
    """Certified physical endpoint columns on one shooting-slope cell."""

    shooting_slopes: RationalInterval
    homogeneous_fields: tuple[IntervalVector2, IntervalVector2]
    homogeneous_derivatives: tuple[IntervalVector2, IntervalVector2]
    forced_field: IntervalVector2
    forced_derivative: IntervalVector2


@dataclass(frozen=True)
class FriedrichsPhysicalEndpointTrace:
    """Finite-cell image of the locally admissible affine germ family."""

    cutoff: Fraction
    shooting_slopes: RationalInterval
    cells: tuple[FriedrichsEndpointCell, ...]
    homogeneous_dimension: int
    homogeneous_branch_order: tuple[str, str]
    forced_branch: str
    affine_combination_rule: str
    scope: str


def power_branch_has_finite_local_energy(exponent: int | Fraction) -> bool:
    """Return the exact criterion for ``integral_0^eps x^(2p) dx``."""
    if isinstance(exponent, bool) or not isinstance(exponent, (int, Fraction)):
        raise TypeError("exponent must be an int or Fraction")
    return Fraction(exponent) > Fraction(-1, 2)


def local_power_energy_integral(
    exponent: int | Fraction,
    cutoff: Fraction,
) -> Fraction | None:
    """Integrate ``x^(2p)`` exactly, returning ``None`` when it diverges."""
    if isinstance(exponent, bool) or not isinstance(exponent, (int, Fraction)):
        raise TypeError("exponent must be an int or Fraction")
    if not isinstance(cutoff, Fraction) or cutoff <= 0:
        raise ValueError("cutoff must be a positive Fraction")
    power = Fraction(2) * Fraction(exponent)
    if power <= -1:
        return None
    if power.denominator != 1:
        raise ValueError("an exact Fraction result requires integral 2p+1")
    return cutoff ** (power.numerator + 1) / (power + 1)


def _quadratic_polynomial(
    hessian: tuple[tuple[Polynomial, ...], ...],
    vector: tuple[Polynomial, Polynomial, Polynomial, Polynomial],
) -> Polynomial:
    result = _poly(0)
    for row in range(4):
        for column in range(4):
            result = _poly_add(
                result,
                _poly_mul(
                    _poly_mul(vector[row], hessian[row][column]),
                    vector[column],
                ),
            )
    return result


def _positive_even_polynomial(value: Polynomial) -> bool:
    """Certify positivity on the real slope axis by coefficients in ``b^2``."""
    return (
        value[0] > 0
        and all(coefficient == 0 for coefficient in value[1::2])
        and all(coefficient >= 0 for coefficient in value[2::2])
    )


def _canonical_modes() -> dict[int, VectorPolynomial]:
    """Use the established regular normalization and exact singular nullvectors."""
    return {
        1: (_poly(-1), _poly(1)),
        3: (
            _poly(Fraction(2, 15)),
            _poly(Fraction(4, 45), 0, Fraction(56, 45)),
        ),
        -2: (
            _poly(Fraction(2, 15), 0, Fraction(4, 3)),
            _poly(Fraction(-2, 15), 0, Fraction(-8, 15)),
        ),
        -4: (
            _poly(Fraction(2, 15), 0, Fraction(28, 15)),
            _poly(Fraction(4, 45), 0, Fraction(56, 45)),
        ),
    }


def _branch(exponent: int, mode: VectorPolynomial) -> IndicialEnergyBranch:
    hessian = centrifugal_origin_leading_hessian()
    pencil = _indicial_matrix(hessian, exponent)
    residual = tuple(
        _poly_add(
            _poly_mul(pencil[row][0], mode[0]),
            _poly_mul(pencil[row][1], mode[1]),
        )
        for row in range(2)
    )
    state = (
        mode[0],
        mode[1],
        _poly_scale(mode[0], exponent),
        _poly_scale(mode[1], exponent),
    )
    return IndicialEnergyBranch(
        exponent=exponent,
        mode=mode,
        indicial_residual=(residual[0], residual[1]),
        leading_energy_polynomial=_quadratic_polynomial(hessian, state),
        finite_local_energy=power_branch_has_finite_local_energy(exponent),
    )


def centrifugal_friedrichs_origin_trace_certificate() -> dict[str, object]:
    """Return the exact local solution-germ admissibility classification."""
    branches = tuple(
        _branch(exponent, mode) for exponent, mode in _canonical_modes().items()
    )
    principal = tuple(
        tuple(
            centrifugal_origin_leading_hessian()[2 + row][2 + column]
            for column in range(2)
        )
        for row in range(2)
    )
    branch_checks = {
        branch.exponent: {
            "indicial_residual_vanishes": all(
                value == _poly(0) for value in branch.indicial_residual
            ),
            "leading_energy_polynomial": tuple(
                str(value) for value in branch.leading_energy_polynomial
            ),
            "leading_energy_positive_for_every_real_slope": (
                _positive_even_polynomial(branch.leading_energy_polynomial)
            ),
            "finite_local_energy": branch.finite_local_energy,
        }
        for branch in branches
    }
    return {
        "result_type": "local_solution_germ_friedrichs_admissibility",
        "weak_form_scaling": ("C=Cbar(x^2), M=x Mbar(x^2), P=x^2 Pbar(x^2)"),
        "leading_principal_block": tuple(
            tuple(tuple(str(value) for value in entry) for entry in row)
            for row in principal
        ),
        "leading_principal_block_positive_for_every_real_slope": (
            principal[0][1] == _poly(0)
            and principal[1][0] == _poly(0)
            and _positive_even_polynomial(principal[0][0])
            and _positive_even_polynomial(principal[1][1])
        ),
        "indicial_powers": tuple(branch.exponent for branch in branches),
        "branch_checks": branch_checks,
        "energy_integrability_criterion": "integral x^(2p) dx is finite iff p>-1/2",
        "finite_energy_homogeneous_powers": (1, 3),
        "excluded_singular_powers": (-2, -4),
        "homogeneous_solution_trace_dimension": 2,
        "forced_affine_column_power": 3,
        "forced_affine_column_is_finite_energy": True,
        "singular_cancellation_rule": (
            "if the p=-4 coefficient is nonzero, its positive x^-8 square "
            "dominates; after it vanishes, a nonzero p=-2 coefficient has a "
            "positive x^-4 square. Cross terms occur at different powers and "
            "cannot remove either first nonzero singular square"
        ),
        "admissible_affine_germ": ("alpha*y_p=1 + beta*y_p=3 + sigma*y_forced,p=3"),
        "scope": (
            "local solution germs of the symmetric weak-form equation only; "
            "this does not classify the entire form domain or prove global "
            "semiboundedness"
        ),
    }


def certify_friedrichs_physical_endpoint_trace(
    transfer: ValidatedPhysicalOriginTransfer,
) -> FriedrichsPhysicalEndpointTrace:
    """Attach the local admissible germ family to certified endpoint tubes."""
    if not isinstance(transfer, ValidatedPhysicalOriginTransfer):
        raise TypeError("transfer must be a ValidatedPhysicalOriginTransfer")
    if not transfer.is_finite_cell_enclosure:
        raise ValueError("transfer must be a certified finite-cell enclosure")
    expected_order = (
        "linear_homogeneous",
        "cubic_homogeneous",
        "forced_particular",
    )
    if transfer.branch_order != expected_order:
        raise ValueError("transfer branch order does not match the admissible germs")
    cells: list[FriedrichsEndpointCell] = []
    for cell in transfer.cells:
        names = tuple(branch.name for branch in cell.branches)
        sigmas = tuple(branch.sigma for branch in cell.branches)
        if names != expected_order or sigmas != (0, 0, 1):
            raise ValueError("cell columns do not match two homogeneous and one force")
        cells.append(
            FriedrichsEndpointCell(
                shooting_slopes=cell.shooting_slopes,
                homogeneous_fields=(
                    cell.branches[0].field,
                    cell.branches[1].field,
                ),
                homogeneous_derivatives=(
                    cell.branches[0].derivative,
                    cell.branches[1].derivative,
                ),
                forced_field=cell.branches[2].field,
                forced_derivative=cell.branches[2].derivative,
            )
        )
    return FriedrichsPhysicalEndpointTrace(
        cutoff=transfer.cutoff,
        shooting_slopes=transfer.shooting_slopes,
        cells=tuple(cells),
        homogeneous_dimension=2,
        homogeneous_branch_order=expected_order[:2],
        forced_branch=expected_order[2],
        affine_combination_rule=transfer.affine_combination_rule,
        scope=(
            "certified finite-cell image of the local admissible solution-germ "
            "family, not a classification of the full Friedrichs form domain"
        ),
    )
