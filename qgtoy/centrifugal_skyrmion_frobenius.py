"""Exact first post-indicial recurrence for the centrifugal origin.

The coefficients below are exact rational functions of the unspecified origin
slope ``b`` for the default profile parameters ``mu^2=1`` and
``lambda=1/400``. They solve the regular transformed equations through the
first nonsingular recurrence, corresponding to physical power ``p=5``.

This is a formal germ through ``x^5``. No Taylor remainder on the finite origin
cell is claimed.
"""

from __future__ import annotations

from fractions import Fraction

from .validated_skyrmion_origin import _RationalFunction


def _rf(value: int | Fraction | _RationalFunction) -> _RationalFunction:
    return value if isinstance(value, _RationalFunction) else _RationalFunction.constant(value)


def _zero(value: _RationalFunction) -> bool:
    return value.exactly_equals(_rf(0))


def _profile_coefficients() -> tuple[_RationalFunction, _RationalFunction]:
    """Return ``c,d`` in ``F=pi-bx+c x^3+d x^5+O(x^7)``."""
    b = _RationalFunction.variable()
    q = b.power(2)
    c = b * (
        Fraction(99, 100)
        + q.scale(Fraction(191, 150))
        + q.power(2).scale(Fraction(8, 3))
    ) / (_rf(10) * (_rf(1) + q.scale(8)))
    d = (
        b * c.power(2).scale(192)
        + c
        * (
            Fraction(-191, 200)
            + q.scale(Fraction(-177, 50))
            + q.power(2).scale(24)
        )
        - b.power(3).scale(Fraction(1, 6))
        - b.power(5).scale(Fraction(6, 25))
        - b.power(7).scale(Fraction(32, 15))
    ) / (_rf(28) * (_rf(1) + q.scale(8)))
    return c, d


def _leading_coefficients(
    c: _RationalFunction,
) -> tuple[_RationalFunction, ...]:
    b = _RationalFunction.variable()
    q = b.power(2)
    coefficient_u0 = (_rf(2) + q.scale(28)).scale(Fraction(1, 9))
    coefficient_v0 = (
        q.power(2).scale(Fraction(16, 27))
        - q.scale(Fraction(1, 18))
        - (b * c).scale(Fraction(28, 9))
        - Fraction(11, 200)
    )
    coefficient_v1 = (_rf(5) + q.scale(28)).scale(Fraction(1, 9))
    force = b.power(3).scale(Fraction(2, 9)) - b.scale(Fraction(1, 18))
    return coefficient_u0, coefficient_v0, coefficient_v1, force


def _recurrence_data(
    c: _RationalFunction,
    d: _RationalFunction,
) -> tuple[
    tuple[tuple[_RationalFunction, _RationalFunction], ...],
    tuple[tuple[_RationalFunction, ...], tuple[_RationalFunction, ...]],
    tuple[_RationalFunction, _RationalFunction],
]:
    b = _RationalFunction.variable()
    q = b.power(2)
    b3c = b.power(3) * c
    bc = b * c
    bd = b * d
    c2 = c.power(2)

    matrix = (
        (
            (_rf(28) + q.scale(308)).scale(Fraction(1, 45)),
            (_rf(-70) - q.scale(392)).scale(Fraction(1, 45)),
        ),
        (
            (_rf(-22) - q.scale(200)).scale(Fraction(1, 45)),
            (_rf(28) + q.scale(176)).scale(Fraction(1, 45)),
        ),
    )
    row_one = (
        q.power(2).scale(Fraction(-62, 45))
        + q.scale(Fraction(17, 1500))
        - bc.scale(Fraction(56, 5))
        + Fraction(191, 9000),
        b.power(6).scale(Fraction(83, 1350))
        + q.power(2).scale(Fraction(19, 500))
        - b3c.scale(Fraction(212, 45))
        + q.scale(Fraction(1003, 36000))
        + bc.scale(Fraction(383, 1500))
        - bd.scale(Fraction(392, 45))
        + c2.scale(Fraction(28, 5)),
        q.power(2).scale(Fraction(92, 45))
        - q.scale(Fraction(67, 1500))
        + bc.scale(Fraction(28, 5))
        - Fraction(191, 3600),
    )
    row_two = (
        q.power(2).scale(Fraction(16, 45))
        - q.scale(Fraction(59, 750))
        + bc.scale(Fraction(112, 15))
        - Fraction(191, 9000),
        b.power(6).scale(Fraction(-67, 675))
        - q.power(2).scale(Fraction(11, 500))
        + b3c.scale(Fraction(28, 9))
        - q.scale(Fraction(1, 90))
        - bc.scale(Fraction(37, 750))
        + bd.scale(Fraction(176, 45))
        - c2.scale(Fraction(8, 5)),
        q.power(2).scale(Fraction(-44, 45))
        + q.scale(Fraction(13, 750))
        - bc.scale(Fraction(8, 5))
        + Fraction(191, 9000),
    )
    force = (
        b.power(5).scale(Fraction(-7, 135))
        + b.power(3).scale(Fraction(139, 6750))
        - (q * c).scale(Fraction(62, 45))
        - b.scale(Fraction(1, 7200))
        + c.scale(Fraction(1, 18)),
        b.power(5).scale(Fraction(-8, 135))
        - b.power(3).scale(Fraction(97, 6750))
        + (q * c).scale(Fraction(68, 45))
        + b.scale(Fraction(1, 18000))
        - c.scale(Fraction(1, 45)),
    )
    return matrix, (row_one, row_two), force


def _solve_branch(
    *,
    name: str,
    sigma: int,
    u0: _RationalFunction,
    v0: _RationalFunction,
    v1: _RationalFunction,
    leading: tuple[_RationalFunction, ...],
    matrix: tuple[tuple[_RationalFunction, _RationalFunction], ...],
    lower: tuple[tuple[_RationalFunction, ...], tuple[_RationalFunction, ...]],
    force: tuple[_RationalFunction, _RationalFunction],
) -> dict[str, object]:
    leading_residual = (
        leading[0] * u0 + leading[1] * v0 - leading[2] * v1 - leading[3].scale(sigma)
    )
    right = tuple(
        force[row].scale(sigma)
        - lower[row][0] * u0
        - lower[row][1] * v0
        - lower[row][2] * v1
        for row in range(2)
    )
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    u1 = (right[0] * matrix[1][1] - matrix[0][1] * right[1]) / determinant
    v2 = (matrix[0][0] * right[1] - right[0] * matrix[1][0]) / determinant
    recurrence_residual = (
        matrix[0][0] * u1 + matrix[0][1] * v2 - right[0],
        matrix[1][0] * u1 + matrix[1][1] * v2 - right[1],
    )
    return {
        "name": name,
        "sigma": sigma,
        "u0": u0,
        "v0": v0,
        "v1": v1,
        "u1": u1,
        "v2": v2,
        "leading_equation_residual_vanishes": _zero(leading_residual),
        "p5_recurrence_residuals_vanish": tuple(
            _zero(value) for value in recurrence_residual
        ),
    }


def _evaluate_polynomial(coefficients: tuple[Fraction, ...], value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def _evaluate(value: _RationalFunction, argument: Fraction) -> Fraction:
    return _evaluate_polynomial(
        value.numerator.coefficients, argument
    ) / _evaluate_polynomial(value.denominator.coefficients, argument)


def _record(value: _RationalFunction, reference_slope: Fraction) -> dict[str, object]:
    evaluated = _evaluate(value, reference_slope)
    return {
        "numerator_coefficients": tuple(str(item) for item in value.numerator.coefficients),
        "denominator_coefficients": tuple(str(item) for item in value.denominator.coefficients),
        "reference_exact": str(evaluated),
        "reference_decimal": float(evaluated),
    }


def centrifugal_skyrmion_first_frobenius_recurrence_certificate(
    *,
    reference_slope: Fraction = Fraction(1462763601523, 925827031517),
) -> dict[str, object]:
    """Prove and report the first exact post-indicial recurrence."""
    if not isinstance(reference_slope, Fraction) or reference_slope <= 0:
        raise ValueError("reference_slope must be a positive Fraction")
    b = _RationalFunction.variable()
    q = b.power(2)
    c, d = _profile_coefficients()
    leading = _leading_coefficients(c)
    matrix, lower, force = _recurrence_data(c, d)
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    expected_determinant = (
        q.power(2).scale(32) + q.scale(12) + 1
    ).scale(Fraction(-28, 75))

    linear_v1 = leading[1] / leading[2]
    cubic_u0 = (_rf(10) + q.scale(56)).scale(Fraction(1, 45))
    cubic_v1 = (_rf(4) + q.scale(56)).scale(Fraction(1, 45))
    forced_v1 = b * (_rf(1) - q.scale(4)) / (_rf(10) + q.scale(56))
    branches = (
        _solve_branch(
            name="linear_homogeneous",
            sigma=0,
            u0=_rf(0),
            v0=_rf(1),
            v1=linear_v1,
            leading=leading,
            matrix=matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="cubic_homogeneous",
            sigma=0,
            u0=cubic_u0,
            v0=_rf(0),
            v1=cubic_v1,
            leading=leading,
            matrix=matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="forced_particular",
            sigma=1,
            u0=_rf(0),
            v0=_rf(0),
            v1=forced_v1,
            leading=leading,
            matrix=matrix,
            lower=lower,
            force=force,
        ),
    )
    rendered = {
        branch["name"]: {
            key: (
                _record(value, reference_slope)
                if isinstance(value, _RationalFunction)
                else value
            )
            for key, value in branch.items()
            if key != "name"
        }
        for branch in branches
    }
    checks = (
        determinant.exactly_equals(expected_determinant),
        *(
            bool(branch["leading_equation_residual_vanishes"])
            for branch in branches
        ),
        *(
            all(branch["p5_recurrence_residuals_vanish"])
            for branch in branches
        ),
    )
    return {
        "result_type": "exact_first_post_indicial_frobenius_recurrence",
        "reference_slope": str(reference_slope),
        "profile_parameters": {"mass_squared": "1", "curvature": "1/400"},
        "coefficient_field": "exact rational functions of b",
        "profile_cubic_coefficient": _record(c, reference_slope),
        "profile_quintic_coefficient": _record(d, reference_slope),
        "series_convention": (
            "u=u0+u1*t+O(t^2), v=v0+v1*t+v2*t^2+O(t^3), t=x^2"
        ),
        "p5_recurrence_determinant": _record(determinant, reference_slope),
        "p5_recurrence_determinant_identity": (
            "Delta5=-(28/75)(32b^4+12b^2+1)<0"
        ),
        "p5_recurrence_determinant_identity_verified": checks[0],
        "branches": rendered,
        "all_exact_recurrence_checks_pass": all(checks),
        "claim_boundary": (
            "Exact formal germs through x^5 for the default profile family. "
            "No Taylor remainder is enclosed on 0<=t<=1/256, so these germs "
            "are not yet a finite-cutoff transfer, Robin enclosure, or "
            "continuum inverse theorem."
        ),
    }
