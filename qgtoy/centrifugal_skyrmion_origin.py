"""Exact indicial algebra for the centrifugal Skyrmion quadrupole.

Near the regular hedgehog origin,

``F=pi-b x+O(x^3)``, ``sin(F)=b x+O(x^3)``, ``cos(F)=-1+O(x^2)``.

The local Hessian blocks have ``C=C0+O(x^2)``, ``M=x M0+O(x^3)``, and
``P=x^2 P0+O(x^4)``. This module extracts ``C0,M0,P0`` from the same exact
quadratic-density formula using rational polynomial/Laurent arithmetic. It
then audits the indicial pencil

``K(p)=-p(p+1)P0-(p+1)M0^T+p M0+C0``.

All returned polynomial coefficients are exact rationals in the origin slope
``b``. No small probe radius or floating singular-value decomposition enters.
"""

from __future__ import annotations

from fractions import Fraction

from .validated_interval import RationalInterval


Polynomial = tuple[Fraction, ...]
LaurentPolynomial = dict[int, Polynomial]
Matrix2 = tuple[tuple[Polynomial, Polynomial], tuple[Polynomial, Polynomial]]


def _poly(*coefficients: int | Fraction) -> Polynomial:
    values = tuple(Fraction(value) for value in coefficients)
    while len(values) > 1 and values[-1] == 0:
        values = values[:-1]
    return values or (Fraction(0),)


def _poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    size = max(len(left), len(right))
    return _poly(
        *tuple(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        )
    )


def _poly_neg(value: Polynomial) -> Polynomial:
    return _poly(*(-coefficient for coefficient in value))


def _poly_sub(left: Polynomial, right: Polynomial) -> Polynomial:
    return _poly_add(left, _poly_neg(right))


def _poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_power, left_coefficient in enumerate(left):
        for right_power, right_coefficient in enumerate(right):
            result[left_power + right_power] += left_coefficient * right_coefficient
    return _poly(*result)


def _poly_scale(value: Polynomial, scalar: int | Fraction) -> Polynomial:
    factor = Fraction(scalar)
    return _poly(*(factor * coefficient for coefficient in value))


def _poly_evaluate(value: Polynomial, argument: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(value):
        result = result * argument + coefficient
    return result


def _laurent_monomial(exponent: int, coefficient: Polynomial) -> LaurentPolynomial:
    return {} if coefficient == _poly(0) else {exponent: coefficient}


def _laurent_constant(value: int | Fraction | Polynomial) -> LaurentPolynomial:
    coefficient = value if isinstance(value, tuple) else _poly(value)
    return _laurent_monomial(0, coefficient)


def _laurent_add(
    left: LaurentPolynomial, right: LaurentPolynomial
) -> LaurentPolynomial:
    result = dict(left)
    for exponent, coefficient in right.items():
        combined = _poly_add(result.get(exponent, _poly(0)), coefficient)
        if combined == _poly(0):
            result.pop(exponent, None)
        else:
            result[exponent] = combined
    return result


def _laurent_neg(value: LaurentPolynomial) -> LaurentPolynomial:
    return {exponent: _poly_neg(coefficient) for exponent, coefficient in value.items()}


def _laurent_sub(
    left: LaurentPolynomial, right: LaurentPolynomial
) -> LaurentPolynomial:
    return _laurent_add(left, _laurent_neg(right))


def _laurent_mul(
    left: LaurentPolynomial, right: LaurentPolynomial
) -> LaurentPolynomial:
    result: LaurentPolynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            coefficient = _poly_mul(left_coefficient, right_coefficient)
            result = _laurent_add(result, _laurent_monomial(exponent, coefficient))
    return result


def _laurent_scale(
    value: LaurentPolynomial, scalar: int | Fraction
) -> LaurentPolynomial:
    return {
        exponent: _poly_scale(coefficient, scalar)
        for exponent, coefficient in value.items()
        if _poly_scale(coefficient, scalar) != _poly(0)
    }


def _laurent_square(value: LaurentPolynomial) -> LaurentPolynomial:
    return _laurent_mul(value, value)


def _leading_density(vector: tuple[Fraction, ...]) -> Polynomial:
    """Return the exact ``x^0`` leading density for ``(f,g,x f',x g')``."""
    if len(vector) != 4:
        raise ValueError("vector must have four entries")
    f = _laurent_constant(vector[0])
    g = _laurent_constant(vector[1])
    fp = _laurent_monomial(-1, _poly(vector[2]))
    gp = _laurent_monomial(-1, _poly(vector[3]))
    x2 = _laurent_monomial(2, _poly(1))
    inv_x2 = _laurent_monomial(-2, _poly(1))
    slope = _poly(0, 1)
    sine = _laurent_monomial(1, slope)
    cosine = _laurent_constant(-1)
    profile_derivative = _laurent_constant(_poly_neg(slope))

    q_average = Fraction(4, 45)
    tangent_average = Fraction(2, 15)
    tangent_derivative_average = Fraction(4, 5)
    angular_tensor_average = Fraction(2, 3)

    perturbation_squared = _laurent_add(
        _laurent_scale(_laurent_square(f), q_average),
        _laurent_scale(_laurent_square(g), tangent_average),
    )
    radial_b = _laurent_sub(
        _laurent_add(
            _laurent_scale(_laurent_square(fp), 2 * q_average),
            _laurent_scale(_laurent_square(gp), 2 * tangent_average),
        ),
        _laurent_scale(
            _laurent_mul(_laurent_square(g), _laurent_square(profile_derivative)),
            2 * tangent_average,
        ),
    )
    angular_gradient = _laurent_add(
        _laurent_add(
            _laurent_scale(_laurent_square(f), 4 * tangent_average),
            _laurent_scale(
                _laurent_mul(_laurent_square(f), _laurent_square(cosine)),
                2 * q_average,
            ),
        ),
        _laurent_add(
            _laurent_add(
                _laurent_scale(
                    _laurent_square(g), tangent_derivative_average
                ),
                _laurent_scale(
                    _laurent_mul(_laurent_mul(f, g), cosine),
                    -4 * tangent_average,
                ),
            ),
            _laurent_scale(
                _laurent_mul(_laurent_mul(f, g), cosine),
                -6 * q_average,
            ),
        ),
    )
    angular_b_trace = _laurent_sub(
        _laurent_scale(angular_gradient, 2),
        _laurent_scale(
            _laurent_mul(perturbation_squared, _laurent_square(sine)), 4
        ),
    )
    hessian_b_trace = _laurent_add(
        radial_b, _laurent_mul(angular_b_trace, inv_x2)
    )

    a_trace_coefficient = _laurent_add(
        _laurent_scale(_laurent_mul(profile_derivative, fp), 2),
        _laurent_scale(
            _laurent_mul(
                _laurent_mul(sine, inv_x2),
                _laurent_sub(
                    _laurent_scale(_laurent_mul(f, cosine), 2),
                    _laurent_scale(g, 3),
                ),
            ),
            2,
        ),
    )
    a_trace_squared = _laurent_scale(
        _laurent_square(a_trace_coefficient), q_average
    )
    radial_angular_a = _laurent_add(
        _laurent_mul(sine, gp),
        _laurent_mul(
            profile_derivative,
            _laurent_sub(_laurent_scale(f, 2), _laurent_mul(cosine, g)),
        ),
    )
    angular_a_squared = _laurent_scale(
        _laurent_mul(
            _laurent_square(sine),
            _laurent_add(
                _laurent_add(
                    _laurent_scale(
                        _laurent_mul(_laurent_square(f), _laurent_square(cosine)),
                        2 * q_average,
                    ),
                    _laurent_scale(
                        _laurent_mul(_laurent_mul(f, cosine), g),
                        -6 * q_average,
                    ),
                ),
                _laurent_scale(_laurent_square(g), angular_tensor_average),
            ),
        ),
        4,
    )
    a_squared_trace = _laurent_add(
        _laurent_add(
            _laurent_scale(
                _laurent_mul(
                    _laurent_square(profile_derivative), _laurent_square(fp)
                ),
                4 * q_average,
            ),
            _laurent_scale(
                _laurent_mul(_laurent_square(radial_angular_a), inv_x2),
                2 * tangent_average,
            ),
        ),
        _laurent_mul(angular_a_squared, _laurent_monomial(-4, _poly(1))),
    )
    background_strain = _laurent_add(
        _laurent_square(profile_derivative),
        _laurent_scale(
            _laurent_mul(_laurent_square(sine), inv_x2), 2
        ),
    )
    g_times_b = _laurent_add(
        _laurent_mul(_laurent_square(profile_derivative), radial_b),
        _laurent_mul(
            _laurent_mul(_laurent_square(sine), angular_b_trace),
            _laurent_monomial(-4, _poly(1)),
        ),
    )
    density = _laurent_add(
        _laurent_scale(_laurent_mul(x2, hessian_b_trace), Fraction(1, 8)),
        _laurent_scale(
            _laurent_mul(
                x2,
                _laurent_sub(
                    _laurent_add(
                        a_trace_squared,
                        _laurent_mul(background_strain, hessian_b_trace),
                    ),
                    _laurent_add(a_squared_trace, g_times_b),
                ),
            ),
            Fraction(1, 2),
        ),
    )
    return density.get(0, _poly(0))


def centrifugal_origin_leading_hessian() -> tuple[tuple[Polynomial, ...], ...]:
    """Return the exact leading Hessian in ``(f,g,x f',x g')``."""
    basis = tuple(
        tuple(Fraction(1 if row == column else 0) for row in range(4))
        for column in range(4)
    )
    diagonal = tuple(_leading_density(vector) for vector in basis)
    rows: list[tuple[Polynomial, ...]] = []
    for row in range(4):
        entries: list[Polynomial] = []
        for column in range(4):
            if row == column:
                entries.append(diagonal[row])
            else:
                combined = tuple(
                    basis[row][index] + basis[column][index] for index in range(4)
                )
                entries.append(
                    _poly_scale(
                        _poly_sub(
                            _poly_sub(_leading_density(combined), diagonal[row]),
                            diagonal[column],
                        ),
                        Fraction(1, 2),
                    )
                )
        rows.append(tuple(entries))
    return tuple(rows)


def _indicial_matrix(
    hessian: tuple[tuple[Polynomial, ...], ...], exponent: int
) -> Matrix2:
    p = Fraction(exponent)
    coordinate = tuple(tuple(hessian[row][column] for column in range(2)) for row in range(2))
    mixed = tuple(tuple(hessian[row][2 + column] for column in range(2)) for row in range(2))
    principal = tuple(tuple(hessian[2 + row][2 + column] for column in range(2)) for row in range(2))
    rows: list[tuple[Polynomial, Polynomial]] = []
    for row in range(2):
        entries: list[Polynomial] = []
        for column in range(2):
            value = _poly_add(
                _poly_scale(principal[row][column], -p * (p + 1)),
                _poly_scale(mixed[column][row], -(p + 1)),
            )
            value = _poly_add(value, _poly_scale(mixed[row][column], p))
            value = _poly_add(value, coordinate[row][column])
            entries.append(value)
        rows.append((entries[0], entries[1]))
    return (rows[0], rows[1])


def _determinant(matrix: Matrix2) -> Polynomial:
    return _poly_sub(
        _poly_mul(matrix[0][0], matrix[1][1]),
        _poly_mul(matrix[0][1], matrix[1][0]),
    )


def _polynomial_record(value: Polynomial) -> tuple[str, ...]:
    return tuple(str(coefficient) for coefficient in value)


def centrifugal_origin_leading_robin_enclosure(
    *,
    cutoff: Fraction = Fraction(1, 16),
    slope_lower: Fraction = Fraction(546684696508091, 347185136818875),
    slope_upper: Fraction = Fraction(550388004634159, 347185136818875),
) -> tuple[tuple[RationalInterval, RationalInterval], ...]:
    """Enclose the leading regular-subspace Robin matrix at a cutoff.

    The regular basis columns are ``(-1,1)`` at power one and
    ``(a,d)=(2/15,4/45+56b^2/45)`` at power three. Thus

    With the convention ``y'=R y``, the leading matrix is
    ``R=B diag(1,3) B^{-1}/cutoff``.

    This is the exact leading indicial transfer over the supplied slope box. It
    does not include finite-cutoff Frobenius remainders.
    """
    if not isinstance(cutoff, Fraction) or cutoff <= 0:
        raise ValueError("cutoff must be a positive Fraction")
    if not isinstance(slope_lower, Fraction) or not isinstance(
        slope_upper, Fraction
    ):
        raise ValueError("slope endpoints must be Fractions")
    if slope_lower <= 0 or slope_lower > slope_upper:
        raise ValueError("slope interval must be positive and ordered")
    a = Fraction(2, 15)
    d_lower = Fraction(4, 45) + Fraction(56, 45) * slope_lower**2
    d_upper = Fraction(4, 45) + Fraction(56, 45) * slope_upper**2
    scale = Fraction(1, cutoff)
    # Each entry is monotone in d. Endpoint evaluation avoids dependency
    # inflation from dividing a box by a correlated copy of itself.
    return (
        (
            RationalInterval(
                scale * (1 + 2 * a / (a + d_upper)),
                scale * (1 + 2 * a / (a + d_lower)),
            ),
            RationalInterval(
                scale * 2 * a / (a + d_upper),
                scale * 2 * a / (a + d_lower),
            ),
        ),
        (
            RationalInterval(
                scale * 2 * d_lower / (a + d_lower),
                scale * 2 * d_upper / (a + d_upper),
            ),
            RationalInterval(
                scale * (1 + 2 * d_lower / (a + d_lower)),
                scale * (1 + 2 * d_upper / (a + d_upper)),
            ),
        ),
    )


def _interval_record(value: RationalInterval) -> dict[str, str]:
    return {
        "lower": str(value.lower),
        "upper": str(value.upper),
        "width": str(value.width),
    }


def centrifugal_origin_indicial_certificate(
    *,
    reference_slope: Fraction = Fraction(1462763601523, 925827031517),
) -> dict[str, object]:
    """Prove the four exact indicial roots and identify the regular modes."""
    if not isinstance(reference_slope, Fraction) or reference_slope <= 0:
        raise ValueError("reference_slope must be a positive Fraction")
    hessian = centrifugal_origin_leading_hessian()
    roots = (1, 3, -2, -4)
    matrices = {root: _indicial_matrix(hessian, root) for root in roots}
    determinants = {root: _determinant(matrix) for root, matrix in matrices.items()}
    root_checks = {root: determinants[root] == _poly(0) for root in roots}
    linear = matrices[1]
    linear_mode = (_poly(-1), _poly(1))
    linear_residual = tuple(
        _poly_add(
            _poly_mul(linear[row][0], linear_mode[0]),
            _poly_mul(linear[row][1], linear_mode[1]),
        )
        for row in range(2)
    )
    cubic = matrices[3]
    cubic_vector = (cubic[0][1], _poly_neg(cubic[0][0]))
    cubic_residual = tuple(
        _poly_add(
            _poly_mul(cubic[row][0], cubic_vector[0]),
            _poly_mul(cubic[row][1], cubic_vector[1]),
        )
        for row in range(2)
    )
    principal: Matrix2 = (
        (hessian[2][2], hessian[2][3]),
        (hessian[3][2], hessian[3][3]),
    )
    principal_determinant = _determinant(principal)
    principal_positive = (
        principal[0][1] == _poly(0)
        and principal[1][0] == _poly(0)
        and all(
            coefficient >= 0 for coefficient in principal[0][0]
        )
        and principal[0][0][0] > 0
        and all(
            coefficient >= 0 for coefficient in principal[1][1]
        )
        and principal[1][1][0] > 0
        and all(coefficient >= 0 for coefficient in principal_determinant)
        and principal_determinant[0] > 0
    )
    cubic_f = _poly_evaluate(cubic_vector[0], reference_slope)
    cubic_g = _poly_evaluate(cubic_vector[1], reference_slope)
    leading_robin = centrifugal_origin_leading_robin_enclosure()
    return {
        "result_type": "exact_rational_origin_indicial_identity",
        "slope_variable": "b in F=pi-b x+O(x^3)",
        "leading_hessian_polynomials": tuple(
            tuple(_polynomial_record(entry) for entry in row) for row in hessian
        ),
        "principal_determinant_polynomial": _polynomial_record(
            principal_determinant
        ),
        "principal_block_positive_for_every_real_slope": principal_positive,
        "indicial_roots": roots,
        "root_determinant_polynomials_vanish": root_checks,
        "quartic_factorization": (
            "det K(p)=det(P0)(p-1)(p-3)(p+2)(p+4)"
        ),
        "quartic_factorization_verified": (
            principal_positive and all(root_checks.values())
        ),
        "linear_regular_mode": "(f,g)=(-1,1)x",
        "linear_mode_polynomial_residuals": tuple(
            _polynomial_record(value) for value in linear_residual
        ),
        "cubic_mode_polynomial_vector": tuple(
            _polynomial_record(value) for value in cubic_vector
        ),
        "cubic_mode_polynomial_residuals": tuple(
            _polynomial_record(value) for value in cubic_residual
        ),
        "reference_slope": str(reference_slope),
        "reference_cubic_mode_f_over_g": str(cubic_f / cubic_g),
        "regular_origin_change_of_variables": (
            "g=x v(x^2), f=-x v(x^2)+x^3 u(x^2)"
        ),
        "authenticated_slope_interval": {
            "lower": "546684696508091/347185136818875",
            "upper": "550388004634159/347185136818875",
        },
        "leading_robin_cutoff": "1/16",
        "leading_robin_matrix_enclosure": tuple(
            tuple(_interval_record(entry) for entry in row)
            for row in leading_robin
        ),
        "claim_boundary": (
            "Exact leading indicial identity for the declared K=2 Hessian. It "
            "also encloses the leading regular-subspace Robin matrix over the "
            "authenticated slope interval, but does not include its finite-"
            "cutoff Frobenius remainder. It does not yet prove the transformed "
            "full nonlinear-coefficient operator is regular, identify its "
            "Friedrichs form domain, or bound the exact finite-radius transfer."
        ),
    }
