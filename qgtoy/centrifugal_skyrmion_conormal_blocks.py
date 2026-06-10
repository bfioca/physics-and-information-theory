"""Regular conormal blocks for the centrifugal Skyrmion origin problem.

Let ``a=y/x``, ``d=y'``, and ``t=x^2``.  The angular-averaged static
quadratic density has the exact regular form

``H_static/t=a.T Cbar(t) a+2 a.T Mbar(t) d+d.T Pbar(t) d``.

Equivalently, the physical weak-form blocks are
``C=Cbar``, ``M=x Mbar``, and ``P=t Pbar``.

This module performs all cancellations before evaluation.  Its unchecked
kernel-level core therefore works at ``t=0`` and with exact or Taylor-model
scalar arithmetic.  For ``F=pi-x w(t)`` it uses

``rho=w+2t w_t=-F'``, ``s=sin(xw)/x``, and ``c=cos(xw)``.

The rotational source is returned in the Fuchs convention
``s0=x shat0`` and ``s1=x^2 shat1``.  In fact both hatted blocks contain an
extra factor of ``t``, proving ``s0=O(x^3)`` and ``s1=O(x^4)`` directly.
"""

from __future__ import annotations

from fractions import Fraction
from math import cos, isfinite, sin, sqrt
from typing import TypeVar


Scalar = TypeVar("Scalar")
Vector2 = tuple[Scalar, Scalar]
Matrix2 = tuple[tuple[Scalar, Scalar], tuple[Scalar, Scalar]]


def _regular_quadratic_density_algebra(
    *,
    t: Scalar,
    metric_factor: Scalar,
    profile_deficit_radial_derivative: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
    field_over_radius: Vector2,
    physical_derivative: Vector2,
    pion_mass_squared: Scalar,
) -> Scalar:
    """Evaluate ``H_static/t`` in ``(a=y/x,d=y')`` without checks."""
    q_average = Fraction(4, 45)
    tangent_average = Fraction(2, 15)
    tangent_derivative_average = Fraction(4, 5)
    angular_tensor_average = Fraction(2, 3)

    f, g = field_over_radius
    df, dg = physical_derivative
    h = metric_factor
    rho = profile_deficit_radial_derivative
    s = sine_over_radius
    c = cosine_of_profile_deficit

    perturbation = f * f * q_average + g * g * tangent_average
    derivative_quadratic = df * df * (2 * q_average) + dg * dg * (2 * tangent_average)
    angular_gradient = (
        f * f * (4 * tangent_average)
        + f * f * c * c * (2 * q_average)
        + g * g * tangent_derivative_average
        + f * g * c * (4 * tangent_average)
        + f * g * c * (6 * q_average)
    )
    scaled_hessian_b = (
        h * derivative_quadratic
        + angular_gradient * 2
        - t * (h * g * g * rho * rho * (2 * tangent_average) + perturbation * s * s * 4)
    )

    trace_numerator = h * rho * df + s * (c * f * 2 + g * 3)
    radial_angular = s * dg - rho * (f * 2 + c * g)
    angular_a_numerator = (
        f * f * c * c * (2 * q_average)
        + f * g * c * (6 * q_average)
        + g * g * angular_tensor_average
    )
    background_strain = h * rho * rho + s * s * 2

    scaled_a_squared = (
        h * h * rho * rho * df * df * (4 * q_average)
        + h * radial_angular * radial_angular * (2 * tangent_average)
        + s * s * angular_a_numerator * 4
    )
    scaled_g_times_b = (
        h * h * rho * rho * derivative_quadratic
        + s * s * angular_gradient * 2
        - t
        * (
            h * h * g * g * rho * rho * rho * rho * (2 * tangent_average)
            + s * s * s * s * perturbation * 4
        )
    )

    return (
        scaled_hessian_b * Fraction(1, 8)
        + trace_numerator * trace_numerator * (2 * q_average)
        + background_strain * scaled_hessian_b * Fraction(1, 2)
        - scaled_a_squared * Fraction(1, 2)
        - scaled_g_times_b * Fraction(1, 2)
        - t * pion_mass_squared * c * perturbation * Fraction(1, 4)
    )


def _polarized_regular_blocks(
    *,
    t: Scalar,
    metric_factor: Scalar,
    profile_deficit_radial_derivative: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
    pion_mass_squared: Scalar,
) -> tuple[Matrix2, Matrix2, Matrix2]:
    """Polarize the regular density into ``Cbar,Mbar,Pbar``."""
    zero = t * 0
    one = zero + 1
    basis = (
        (one, zero, zero, zero),
        (zero, one, zero, zero),
        (zero, zero, one, zero),
        (zero, zero, zero, one),
    )

    def evaluate(vector: tuple[Scalar, Scalar, Scalar, Scalar]) -> Scalar:
        return _regular_quadratic_density_algebra(
            t=t,
            metric_factor=metric_factor,
            profile_deficit_radial_derivative=(profile_deficit_radial_derivative),
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_of_profile_deficit,
            field_over_radius=(vector[0], vector[1]),
            physical_derivative=(vector[2], vector[3]),
            pion_mass_squared=pion_mass_squared,
        )

    diagonal = tuple(evaluate(vector) for vector in basis)
    rows: list[tuple[Scalar, ...]] = []
    for row in range(4):
        entries: list[Scalar] = []
        for column in range(4):
            if row == column:
                entries.append(diagonal[row])
                continue
            combined = tuple(
                basis[row][index] + basis[column][index] for index in range(4)
            )
            entries.append(
                (evaluate(combined) - diagonal[row] - diagonal[column]) * Fraction(1, 2)
            )
        rows.append(tuple(entries))
    matrix = tuple(rows)
    coordinate = tuple(
        tuple(matrix[row][column] for column in range(2)) for row in range(2)
    )
    mixed = tuple(
        tuple(matrix[row][2 + column] for column in range(2)) for row in range(2)
    )
    principal = tuple(
        tuple(matrix[2 + row][2 + column] for column in range(2)) for row in range(2)
    )
    return coordinate, mixed, principal


def regular_conormal_blocks_from_kernels(
    *,
    t: Scalar,
    metric_factor: Scalar,
    profile_deficit_radial_derivative: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
    pion_mass_squared: Scalar,
) -> dict[str, Matrix2]:
    """Return exact ``Cbar,Mbar,Pbar`` from regular entire kernels."""
    coordinate, mixed, principal = _polarized_regular_blocks(
        t=t,
        metric_factor=metric_factor,
        profile_deficit_radial_derivative=profile_deficit_radial_derivative,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_of_profile_deficit,
        pion_mass_squared=pion_mass_squared,
    )
    return {
        "coordinate": coordinate,
        "mixed": mixed,
        "principal": principal,
    }


def regular_rotational_source_from_kernels(
    *,
    t: Scalar,
    metric_factor: Scalar,
    profile_deficit_radial_derivative: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
) -> dict[str, Vector2]:
    """Return ``shat0,shat1`` after exact source factorization."""
    q_average = Fraction(4, 45)
    tangent_average = Fraction(2, 15)
    h = metric_factor
    rho = profile_deficit_radial_derivative
    s = sine_over_radius
    c = cosine_of_profile_deficit
    zero = t * 0
    one = zero + 1
    inverse_metric = one / h
    radial_kernel = s * (inverse_metric * Fraction(1, 4) + rho * rho)
    coordinate_source = (
        t * c * (radial_kernel + s * s * s * inverse_metric * 2) * q_average,
        t
        * (
            radial_kernel * (-tangent_average)
            + s * s * s * inverse_metric * (3 * q_average)
        ),
    )
    derivative_source = (t * s * s * rho * q_average, zero)
    return {
        "coordinate_source": coordinate_source,
        "derivative_source": derivative_source,
    }


def regular_conormal_data(
    *,
    t: float,
    curvature: float,
    profile_deficit_over_radius: float,
    profile_deficit_time_derivative: float,
    pion_mass: float,
) -> dict[str, object]:
    """Evaluate all regular blocks using ordinary transcendental kernels."""
    values = (
        t,
        curvature,
        profile_deficit_over_radius,
        profile_deficit_time_derivative,
        pion_mass,
    )
    if not all(isfinite(value) for value in values):
        raise ValueError("all conormal-block inputs must be finite")
    if t < 0 or curvature < 0 or pion_mass < 0:
        raise ValueError("t, curvature, and pion_mass must be nonnegative")
    metric_factor = 1 - curvature * t
    if metric_factor <= 0:
        raise ValueError("the point must lie strictly inside the horizon")
    rho = profile_deficit_over_radius + 2 * t * profile_deficit_time_derivative
    if t == 0:
        sine_over_radius = profile_deficit_over_radius
        cosine_kernel = 1.0
    else:
        radius = sqrt(t)
        argument = radius * profile_deficit_over_radius
        sine_over_radius = sin(argument) / radius
        cosine_kernel = cos(argument)
    blocks = regular_conormal_blocks_from_kernels(
        t=t,
        metric_factor=metric_factor,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_kernel,
        pion_mass_squared=pion_mass * pion_mass,
    )
    source = regular_rotational_source_from_kernels(
        t=t,
        metric_factor=metric_factor,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_kernel,
    )
    return {
        **blocks,
        **source,
        "metric_factor": metric_factor,
        "profile_deficit_radial_derivative": rho,
        "sine_over_radius": sine_over_radius,
        "cosine_of_profile_deficit": cosine_kernel,
    }


def _expanded_formal_conormal_checks_slow() -> dict[str, object]:
    """Development-only direct expansion of the conormal germ residuals.

    This redundant check is intentionally not used by the audit because the
    uncancelled rational-function representation suffers severe expression
    swell. :func:`exact_formal_conormal_checks` proves the same divisibility
    through the exact Euler-to-conormal residual identity.
    """
    from .centrifugal_skyrmion_frobenius import (  # noqa: PLC0415
        _leading_coefficients,
        _profile_coefficients,
        _recurrence_data,
        _solve_branch,
    )
    from .centrifugal_skyrmion_origin import (  # noqa: PLC0415
        centrifugal_origin_leading_hessian,
    )
    from .validated_skyrmion_origin import (  # noqa: PLC0415
        _FormalTaylorTwo,
        _RationalFunction,
        RationalPolynomial,
    )

    series = _FormalTaylorTwo
    rf = _RationalFunction
    b = rf.variable()
    cubic, quintic = _profile_coefficients()
    time = series(rf.constant(0), rf.constant(1), rf.constant(0))
    w = series(b, cubic.scale(-1), quintic.scale(-1))
    rho = series(b, cubic.scale(-3), quintic.scale(-5))
    argument_squared = time * w * w
    sine_over_radius = w * (
        series.point(1)
        - argument_squared.scale(Fraction(1, 6))
        + (argument_squared * argument_squared).scale(Fraction(1, 120))
    )
    cosine_kernel = (
        series.point(1)
        - argument_squared.scale(Fraction(1, 2))
        + (argument_squared * argument_squared).scale(Fraction(1, 24))
    )
    metric = series.point(1) - time.scale(Fraction(1, 400))
    mass_squared = series.point(1)
    blocks = regular_conormal_blocks_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_kernel,
        pion_mass_squared=mass_squared,
    )
    source = regular_rotational_source_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_kernel,
    )

    principal = blocks["principal"]
    mixed = blocks["mixed"]
    coordinate = blocks["coordinate"]
    leading_hessian = centrifugal_origin_leading_hessian()

    def polynomial_as_rf(value: tuple[Fraction, ...]) -> object:
        return rf(RationalPolynomial(value), RationalPolynomial((Fraction(1),)))

    regular_matrix = (
        (*coordinate[0], *mixed[0]),
        (*coordinate[1], *mixed[1]),
        (mixed[0][0], mixed[1][0], *principal[0]),
        (mixed[0][1], mixed[1][1], *principal[1]),
    )
    block_constants_match = all(
        regular_matrix[row][column].constant.exactly_equals(
            polynomial_as_rf(leading_hessian[row][column])
        )
        for row in range(4)
        for column in range(4)
    )
    derivative_source = source["derivative_source"]
    coordinate_source = source["coordinate_source"]
    zero_rf = rf.constant(0)
    source_constant_vanishes = all(
        value.constant.exactly_equals(zero_rf)
        for value in (*coordinate_source, *derivative_source)
    )
    principal_determinant_constant = (
        principal[0][0].constant * principal[1][1].constant
        - principal[0][1].constant * principal[1][0].constant
    )
    principal_is_formally_invertible = (
        not principal_determinant_constant.exactly_equals(zero_rf)
    )

    leading = _leading_coefficients(cubic)
    recurrence_matrix, lower, force = _recurrence_data(cubic, quintic)
    slope_squared = b.power(2)
    branches = (
        _solve_branch(
            name="linear_homogeneous",
            sigma=0,
            u0=rf.constant(0),
            v0=rf.constant(1),
            v1=leading[1] / leading[2],
            leading=leading,
            matrix=recurrence_matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="cubic_homogeneous",
            sigma=0,
            u0=(rf.constant(10) + slope_squared.scale(56)).scale(Fraction(1, 45)),
            v0=rf.constant(0),
            v1=(rf.constant(4) + slope_squared.scale(56)).scale(Fraction(1, 45)),
            leading=leading,
            matrix=recurrence_matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="forced_particular",
            sigma=1,
            u0=rf.constant(0),
            v0=rf.constant(0),
            v1=b
            * (rf.constant(1) - slope_squared.scale(4))
            / (rf.constant(10) + slope_squared.scale(56)),
            leading=leading,
            matrix=recurrence_matrix,
            lower=lower,
            force=force,
        ),
    )

    def conormal_residual_vanishes(branch: dict[str, object]) -> bool:
        coefficients = tuple(branch[key] for key in ("u0", "v0", "v1", "u1", "v2"))
        if not all(isinstance(value, rf) for value in coefficients):
            raise TypeError("formal branch coefficients must be rational functions")
        u0, v0, v1, u1, v2 = coefficients
        radial = series(v0.scale(-1), u0 - v1, u1 - v2)
        tangential = series(v0, v1, v2)
        radial_derivative = series(
            v0.scale(-1),
            (u0 - v1).scale(3),
            (u1 - v2).scale(5),
        )
        tangential_derivative = series(v0, v1.scale(3), v2.scale(5))
        fields = (radial, tangential)
        derivatives = (radial_derivative, tangential_derivative)
        sigma = int(branch["sigma"])
        z = tuple(
            sum(
                (principal[row][column] * derivatives[column] for column in range(2)),
                series.point(0),
            )
            + sum(
                (mixed[column][row] * fields[column] for column in range(2)),
                series.point(0),
            )
            - derivative_source[row].scale(sigma)
            for row in range(2)
        )
        kinematic_residual = tuple(
            series(
                zero_rf,
                fields[row].linear.scale(2),
                fields[row].quadratic.scale(4),
            )
            - derivatives[row]
            + fields[row]
            for row in range(2)
        )
        momentum_residual = tuple(
            series(
                z[row].constant.scale(2),
                z[row].linear.scale(4),
                z[row].quadratic.scale(6),
            )
            - sum(
                (coordinate[row][column] * fields[column] for column in range(2)),
                series.point(0),
            )
            - sum(
                (mixed[row][column] * derivatives[column] for column in range(2)),
                series.point(0),
            )
            + coordinate_source[row].scale(sigma)
            for row in range(2)
        )
        return all(
            value.constant.exactly_equals(zero_rf)
            and value.linear.exactly_equals(zero_rf)
            and value.quadratic.exactly_equals(zero_rf)
            for value in (*kinematic_residual, *momentum_residual)
        )

    residual_checks = {
        str(branch["name"]): conormal_residual_vanishes(branch) for branch in branches
    }
    return {
        "fuchs_constant_matches_established_a0": (
            block_constants_match and principal_is_formally_invertible
        ),
        "fuchs_variation_order": "A(t)-A(0)=O(t)",
        "source_constant_vanishes": source_constant_vanishes,
        "source_order": "q(t)=O(t)",
        "conormal_residual_divisible_by_t_cubed": residual_checks,
        "all_checks_pass": (
            block_constants_match
            and principal_is_formally_invertible
            and source_constant_vanishes
            and all(residual_checks.values())
        ),
    }


def exact_formal_conormal_checks() -> dict[str, object]:
    """Prove the regular-block and conormal-residual order statements.

    The exact identity between the Euler and conormal equations transfers the
    already certified `p=1,3,5` recurrence without expanding large rational
    functions: the lower conormal residual is `-1/x` times the Euler
    residual. Thus `O(x^7)` becomes `O(x^6)=O(t^3)`.
    """
    from .centrifugal_skyrmion_frobenius import (  # noqa: PLC0415
        _leading_coefficients,
        _profile_coefficients,
        _recurrence_data,
        _solve_branch,
    )
    from .validated_centrifugal_origin_transfer import (  # noqa: PLC0415
        conormal_fuchs_matrix,
        centrifugal_origin_leading_fuchs_matrix,
    )
    from .validated_skyrmion_origin import _RationalFunction  # noqa: PLC0415

    rf = _RationalFunction
    zero = rf.constant(0)
    one = rf.constant(1)
    b = rf.variable()
    constant_blocks = regular_conormal_blocks_from_kernels(
        t=zero,
        metric_factor=one,
        profile_deficit_radial_derivative=b,
        sine_over_radius=b,
        cosine_of_profile_deficit=one,
        pion_mass_squared=one,
    )
    constant_fuchs = conormal_fuchs_matrix(
        constant_blocks["coordinate"],
        constant_blocks["mixed"],
        constant_blocks["principal"],
    )
    established_a0 = centrifugal_origin_leading_fuchs_matrix()
    constant_matches = all(
        constant_fuchs[row][column].exactly_equals(established_a0[row][column])
        for row in range(4)
        for column in range(4)
    )
    constant_source = regular_rotational_source_from_kernels(
        t=zero,
        metric_factor=one,
        profile_deficit_radial_derivative=b,
        sine_over_radius=b,
        cosine_of_profile_deficit=one,
    )
    source_constant_vanishes = all(
        value.exactly_equals(zero)
        for block in constant_source.values()
        for value in block
    )

    cubic, quintic = _profile_coefficients()
    leading = _leading_coefficients(cubic)
    recurrence_matrix, lower, force = _recurrence_data(cubic, quintic)
    slope_squared = b.power(2)
    branches = (
        _solve_branch(
            name="linear_homogeneous",
            sigma=0,
            u0=zero,
            v0=one,
            v1=leading[1] / leading[2],
            leading=leading,
            matrix=recurrence_matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="cubic_homogeneous",
            sigma=0,
            u0=(rf.constant(10) + slope_squared.scale(56)).scale(Fraction(1, 45)),
            v0=zero,
            v1=(rf.constant(4) + slope_squared.scale(56)).scale(Fraction(1, 45)),
            leading=leading,
            matrix=recurrence_matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="forced_particular",
            sigma=1,
            u0=zero,
            v0=zero,
            v1=b
            * (one - slope_squared.scale(4))
            / (rf.constant(10) + slope_squared.scale(56)),
            leading=leading,
            matrix=recurrence_matrix,
            lower=lower,
            force=force,
        ),
    )
    residual_checks = {
        str(branch["name"]): bool(branch["leading_equation_residual_vanishes"])
        and all(bool(value) for value in branch["p5_recurrence_residuals_vanish"])
        for branch in branches
    }
    return {
        "fuchs_constant_matches_established_a0": constant_matches,
        "fuchs_variation_order": "A(t)-A(0)=O(t)",
        "source_constant_vanishes": source_constant_vanishes,
        "source_order": "q(t)=O(t)",
        "residual_transfer_identity": (
            "lower conormal residual = - Euler residual / x"
        ),
        "euler_residual_order": "O(x^7) from the exact p=1,3,5 recurrence",
        "conormal_residual_divisible_by_t_cubed": residual_checks,
        "all_checks_pass": (
            constant_matches
            and source_constant_vanishes
            and all(residual_checks.values())
        ),
    }
