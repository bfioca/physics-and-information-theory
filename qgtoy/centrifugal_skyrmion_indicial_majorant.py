"""Uniform inverse majorant for post-germ centrifugal indicial matrices.

After the exact fields have been fixed through physical power ``x^5``, all
remaining odd Frobenius powers satisfy ``p>=7``. This module proves a uniform
infinity-norm bound for ``K(p)^{-1}`` over every authenticated origin slope.
The bound is the linear Green constant needed by a Taylor-majorant argument.
"""

from __future__ import annotations

from fractions import Fraction

from .centrifugal_skyrmion_origin import (
    Matrix2,
    Polynomial,
    _determinant,
    _indicial_matrix,
    _poly_add,
    _poly_scale,
    _poly_sub,
    centrifugal_origin_leading_hessian,
)
from .validated_interval import RationalInterval


DEFAULT_SLOPE_LOWER = Fraction(546684696508091, 347185136818875)
DEFAULT_SLOPE_UPPER = Fraction(550388004634159, 347185136818875)


def _polynomial_range(
    value: Polynomial,
    interval: RationalInterval,
) -> RationalInterval:
    result = RationalInterval.point(0)
    for coefficient in reversed(value):
        result = result * interval + coefficient
    return result


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _inverse_infinity_bound(
    matrix: Matrix2,
    slope_box: RationalInterval,
) -> Fraction:
    determinant = _polynomial_range(_determinant(matrix), slope_box)
    if determinant.lower <= 0:
        raise ValueError("indicial determinant is not certified positive")
    entry = tuple(
        tuple(
            _absolute_upper(_polynomial_range(matrix[row][column], slope_box))
            for column in range(2)
        )
        for row in range(2)
    )
    adjugate_row_sum = max(
        entry[1][1] + entry[0][1],
        entry[1][0] + entry[0][0],
    )
    return adjugate_row_sum / determinant.lower


def _generic_power_coefficients(
    hessian: tuple[tuple[Polynomial, ...], ...],
) -> tuple[tuple[tuple[Polynomial, Polynomial, Polynomial], ...], ...]:
    coordinate = tuple(
        tuple(hessian[row][column] for column in range(2)) for row in range(2)
    )
    mixed = tuple(
        tuple(hessian[row][2 + column] for column in range(2)) for row in range(2)
    )
    principal = tuple(
        tuple(hessian[2 + row][2 + column] for column in range(2))
        for row in range(2)
    )
    return tuple(
        tuple(
            (
                _poly_scale(principal[row][column], -1),
                _poly_add(
                    _poly_scale(principal[row][column], -1),
                    _poly_sub(mixed[row][column], mixed[column][row]),
                ),
                _poly_sub(coordinate[row][column], mixed[column][row]),
            )
            for column in range(2)
        )
        for row in range(2)
    )


def centrifugal_indicial_inverse_majorant_certificate(
    *,
    slope_lower: Fraction = DEFAULT_SLOPE_LOWER,
    slope_upper: Fraction = DEFAULT_SLOPE_UPPER,
) -> dict[str, object]:
    """Certify ``sup ||K(p)^-1||_infinity`` for odd ``p>=7``."""
    if not isinstance(slope_lower, Fraction) or not isinstance(
        slope_upper, Fraction
    ):
        raise TypeError("slope endpoints must be Fractions")
    if slope_lower <= 0 or slope_lower > slope_upper:
        raise ValueError("slope interval must be positive and ordered")
    slope_box = RationalInterval(slope_lower, slope_upper)
    hessian = centrifugal_origin_leading_hessian()
    coefficients = _generic_power_coefficients(hessian)
    # Adjugate rows are (K22,-K12) and (-K21,K11).
    adjugate_rows = (((1, 1), (0, 1)), ((1, 0), (0, 0)))
    coefficient_bounds = []
    for power_index in range(3):
        coefficient_bounds.append(
            max(
                sum(
                    _absolute_upper(
                        _polynomial_range(
                            coefficients[row][column][power_index], slope_box
                        )
                    )
                    for row, column in adjugate_row
                )
                for adjugate_row in adjugate_rows
            )
        )
    n2, n1, n0 = coefficient_bounds

    principal: Matrix2 = (
        (hessian[2][2], hessian[2][3]),
        (hessian[3][2], hessian[3][3]),
    )
    principal_determinant_lower = _polynomial_range(
        _determinant(principal), slope_box
    ).lower
    if principal_determinant_lower <= 0:
        raise ValueError("leading principal determinant is not positive")

    p7_bound = _inverse_infinity_bound(_indicial_matrix(hessian, 7), slope_box)
    p9_bound = _inverse_infinity_bound(_indicial_matrix(hessian, 9), slope_box)
    # For p>=11, (p-1)(p-3)(p+2)(p+4)>=(80/121)p^4 and
    # N2*p^2+N1*p+N0<=(N2+N1/11+N0/121)p^2.
    tail_bound = (
        n2 + n1 / 11 + n0 / 121
    ) / (80 * principal_determinant_lower)
    uniform_bound = max(p7_bound, p9_bound, tail_bound)
    return {
        "result_type": "exact_post_germ_indicial_inverse_majorant",
        "slope_interval": {
            "lower": str(slope_lower),
            "upper": str(slope_upper),
        },
        "power_set": "odd integers p>=7",
        "adjugate_power_coefficient_bounds": {
            "quadratic": str(n2),
            "linear": str(n1),
            "constant": str(n0),
        },
        "principal_determinant_lower_bound": str(principal_determinant_lower),
        "p7_inverse_infinity_norm_upper_bound": str(p7_bound),
        "p9_inverse_infinity_norm_upper_bound": str(p9_bound),
        "p_ge_11_inverse_infinity_norm_upper_bound": str(tail_bound),
        "uniform_inverse_infinity_norm_upper_bound": str(uniform_bound),
        "uniform_inverse_infinity_norm_upper_bound_decimal": float(uniform_bound),
        "uniform_bound_below_79_over_1000": uniform_bound < Fraction(79, 1000),
        "tail_proof": (
            "For p>=11, the determinant factor is at least "
            "det(P0)*(80/121)*p^4 and the adjugate row sum is at most "
            "(N2+N1/11+N0/121)*p^2."
        ),
        "claim_boundary": (
            "Exact uniform inverse bound for the leading indicial matrices "
            "only. A finite-cell remainder theorem still requires interval "
            "majorants for the nonleading operator coefficients and source."
        ),
    }
