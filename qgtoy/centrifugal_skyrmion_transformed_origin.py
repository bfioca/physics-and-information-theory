"""Regular variables for the centrifugal Skyrmion origin density.

Write ``t=x^2`` and parameterize the regular physical quadrupole fields by

``g=x v(t)``, ``f=x[-v(t)+t u(t)]``.

For a regular hedgehog, write ``pi-F=x w(t)``.  This module rewrites the full
local static Hessian density in terms of ``t`` and the entire kernels
``s=sin(x w)/x`` and ``c=cos(x w)``.  The resulting expression contains no
negative powers of ``t`` and satisfies ``H_static=x^2 H_hat`` exactly.

This is a density desingularization, not a finite-radius Frobenius-transfer
bound.  After ``dx=dt/(2 sqrt(t))`` the variational problem still has the
regular-singular weight ``sqrt(t)/2``.
"""

from __future__ import annotations

from fractions import Fraction
from math import cos, isfinite, pi, sin, sqrt

from .centrifugal_skyrmion_deformation import (
    quadrupole_static_hessian_density,
)
from .centrifugal_skyrmion_origin import (
    _indicial_matrix,
    _poly,
    _poly_add,
    _poly_neg,
    _poly_scale,
    centrifugal_origin_leading_hessian,
)


Scalar = int | float | Fraction


def _transformed_quadrupole_reduced_density_algebra(
    *,
    t: Scalar,
    metric_factor: Scalar,
    profile_deficit_over_radius: Scalar,
    profile_deficit_time_derivative: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
    v: Scalar,
    u: Scalar,
    v_time_derivative: Scalar,
    u_time_derivative: Scalar,
    pion_mass_squared: Scalar,
) -> dict[str, Scalar]:
    """Evaluate the regular factor without domain checks.

    ``sine_over_radius`` means ``sin(x*w)/x`` and
    ``cosine_of_profile_deficit`` means ``cos(x*w)``.  Supplying these kernels
    explicitly keeps the cancellation identity algebraic. The unchecked core
    also supports exact formal-series arithmetic used by the Frobenius audit.
    """
    q_average = Fraction(4, 45)
    tangent_average = Fraction(2, 15)
    tangent_derivative_average = Fraction(4, 5)
    angular_tensor_average = Fraction(2, 3)

    w = profile_deficit_over_radius
    w_t = profile_deficit_time_derivative
    s = sine_over_radius
    c = cosine_of_profile_deficit
    v_t = v_time_derivative
    u_t = u_time_derivative

    # F=pi-xw(t), f=x*a(t), and g=x*v(t).
    profile_deficit_radial_derivative = w + 2 * t * w_t
    a = -v + t * u
    f_radial_derivative = -v + 3 * t * u - 2 * t * v_t + 2 * t * t * u_t
    g_radial_derivative = v + 2 * t * v_t

    perturbation = q_average * a * a + tangent_average * v * v
    radial_b = (
        2 * q_average * f_radial_derivative * f_radial_derivative
        + 2 * tangent_average * g_radial_derivative * g_radial_derivative
        - 2
        * tangent_average
        * t
        * v
        * v
        * profile_deficit_radial_derivative
        * profile_deficit_radial_derivative
    )
    angular_gradient = (
        4 * tangent_average * a * a
        + 2 * q_average * a * a * c * c
        + tangent_derivative_average * v * v
        + 4 * tangent_average * a * v * c
        + 6 * q_average * a * v * c
    )
    angular_b = 2 * angular_gradient - 4 * t * perturbation * s * s
    hessian_b = metric_factor * radial_b + angular_b

    a_trace = (
        -2
        * metric_factor
        * profile_deficit_radial_derivative
        * f_radial_derivative
        + 2 * s * (-2 * a * c - 3 * v)
    )
    radial_angular_a = (
        s * g_radial_derivative
        - profile_deficit_radial_derivative * (2 * a + c * v)
    )
    angular_a = 4 * s * s * (
        2 * q_average * a * a * c * c
        + 6 * q_average * a * v * c
        + angular_tensor_average * v * v
    )
    a_squared = (
        4
        * metric_factor
        * metric_factor
        * profile_deficit_radial_derivative
        * profile_deficit_radial_derivative
        * f_radial_derivative
        * f_radial_derivative
        * q_average
        + 2
        * metric_factor
        * radial_angular_a
        * radial_angular_a
        * tangent_average
        + angular_a
    )
    background_strain = (
        metric_factor
        * profile_deficit_radial_derivative
        * profile_deficit_radial_derivative
        + 2 * s * s
    )
    g_times_b = (
        metric_factor
        * metric_factor
        * profile_deficit_radial_derivative
        * profile_deficit_radial_derivative
        * radial_b
        + s * s * angular_b
    )
    reduced_density = (
        hessian_b / 8
        + (
            q_average * a_trace * a_trace
            + background_strain * hessian_b
            - a_squared
            - g_times_b
        )
        / 2
        - pion_mass_squared * t * c * perturbation / 4
    )
    return {
        "reduced_density": reduced_density,
        "original_density": t * reduced_density,
        "radial_field_over_radius": a,
        "tangential_field_over_radius": v,
        "radial_field_derivative": f_radial_derivative,
        "tangential_field_derivative": g_radial_derivative,
        "profile_derivative": -profile_deficit_radial_derivative,
    }


def transformed_quadrupole_reduced_density_from_kernels(
    *,
    t: Scalar,
    metric_factor: Scalar,
    profile_deficit_over_radius: Scalar,
    profile_deficit_time_derivative: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
    v: Scalar,
    u: Scalar,
    v_time_derivative: Scalar,
    u_time_derivative: Scalar,
    pion_mass_squared: Scalar,
) -> dict[str, Scalar]:
    """Return the exact regular factor ``H_hat=H_static/x^2``."""
    if t < 0:
        raise ValueError("t must be nonnegative")
    if metric_factor <= 0:
        raise ValueError("metric_factor must be positive")
    if pion_mass_squared < 0:
        raise ValueError("pion_mass_squared must be nonnegative")
    return _transformed_quadrupole_reduced_density_algebra(
        t=t,
        metric_factor=metric_factor,
        profile_deficit_over_radius=profile_deficit_over_radius,
        profile_deficit_time_derivative=profile_deficit_time_derivative,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_of_profile_deficit,
        v=v,
        u=u,
        v_time_derivative=v_time_derivative,
        u_time_derivative=u_time_derivative,
        pion_mass_squared=pion_mass_squared,
    )


def transformed_quadrupole_reduced_density(
    *,
    t: float,
    curvature: float,
    profile_deficit_over_radius: float,
    profile_deficit_time_derivative: float,
    v: float,
    u: float,
    v_time_derivative: float,
    u_time_derivative: float,
    pion_mass: float,
) -> dict[str, float]:
    """Evaluate the regular density using ordinary transcendental kernels."""
    values = (
        t,
        curvature,
        profile_deficit_over_radius,
        profile_deficit_time_derivative,
        v,
        u,
        v_time_derivative,
        u_time_derivative,
        pion_mass,
    )
    if not all(isfinite(value) for value in values):
        raise ValueError("all transformed-origin inputs must be finite")
    if t < 0.0 or curvature < 0.0 or pion_mass < 0.0:
        raise ValueError("t, curvature, and pion_mass must be nonnegative")
    metric_factor = 1.0 - curvature * t
    if metric_factor <= 0.0:
        raise ValueError("the point must lie strictly inside the horizon")
    if t == 0.0:
        sine_over_radius = profile_deficit_over_radius
        cosine_kernel = 1.0
    else:
        radius = sqrt(t)
        argument = radius * profile_deficit_over_radius
        sine_over_radius = sin(argument) / radius
        cosine_kernel = cos(argument)
    record = transformed_quadrupole_reduced_density_from_kernels(
        t=t,
        metric_factor=metric_factor,
        profile_deficit_over_radius=profile_deficit_over_radius,
        profile_deficit_time_derivative=profile_deficit_time_derivative,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_kernel,
        v=v,
        u=u,
        v_time_derivative=v_time_derivative,
        u_time_derivative=u_time_derivative,
        pion_mass_squared=pion_mass * pion_mass,
    )
    return {key: float(value) for key, value in record.items()}


def _direct_density_check(probe: tuple[float, ...]) -> float:
    (
        t,
        curvature,
        w,
        w_t,
        v,
        u,
        v_t,
        u_t,
        pion_mass,
    ) = probe
    transformed = transformed_quadrupole_reduced_density(
        t=t,
        curvature=curvature,
        profile_deficit_over_radius=w,
        profile_deficit_time_derivative=w_t,
        v=v,
        u=u,
        v_time_derivative=v_t,
        u_time_derivative=u_t,
        pion_mass=pion_mass,
    )
    radius = sqrt(t)
    profile = pi - radius * w
    direct = quadrupole_static_hessian_density(
        radius=radius,
        metric_factor=1.0 - curvature * t,
        profile=profile,
        profile_derivative=float(transformed["profile_derivative"]),
        radial_field=radius * float(transformed["radial_field_over_radius"]),
        tangential_field=radius * v,
        radial_field_derivative=float(transformed["radial_field_derivative"]),
        tangential_field_derivative=float(
            transformed["tangential_field_derivative"]
        ),
        pion_mass=pion_mass,
    )
    denominator = max(1.0, abs(direct), abs(transformed["original_density"]))
    return abs(direct - transformed["original_density"]) / denominator


def _forced_cubic_compatibility_record() -> dict[str, object]:
    """Verify that the leading rotational source is in ``range K(3)``."""
    cubic_matrix = _indicial_matrix(centrifugal_origin_leading_hessian(), 3)
    source_radial = _poly(0, Fraction(1, 45), 0, Fraction(-4, 45))
    source_tangential = _poly_scale(source_radial, Fraction(-3, 2))
    row_ratio_checks = tuple(
        cubic_matrix[1][column]
        == _poly_scale(cubic_matrix[0][column], Fraction(-3, 2))
        for column in range(2)
    )

    # At cubic order, (f_3,g_3)=(u_0-v_1,v_1).  The first row of
    # K(3)(f_3,g_3)=F_3 gives the displayed scalar compatibility relation.
    u_coefficient = cubic_matrix[0][0]
    v_time_coefficient = _poly_add(
        _poly_neg(cubic_matrix[0][0]), cubic_matrix[0][1]
    )
    expected_u = _poly(Fraction(-4, 45), 0, Fraction(-56, 45))
    expected_v_time = _poly(Fraction(10, 45), 0, Fraction(56, 45))
    relation_verified = (
        u_coefficient == expected_u
        and v_time_coefficient == expected_v_time
        and cubic_matrix[1][0]
        == _poly_scale(cubic_matrix[0][0], Fraction(-3, 2))
        and cubic_matrix[1][1]
        == _poly_scale(cubic_matrix[0][1], Fraction(-3, 2))
        and source_tangential
        == _poly_scale(source_radial, Fraction(-3, 2))
    )
    return {
        "leading_original_source": (
            "F_3=b(1-4b^2)(1,-3/2)/45"
        ),
        "cubic_indicial_rows_have_ratio_minus_three_halves": row_ratio_checks,
        "source_has_same_ratio": (
            source_tangential
            == _poly_scale(source_radial, Fraction(-3, 2))
        ),
        "source_is_in_range_of_K3": all(row_ratio_checks) and relation_verified,
        "particular_cubic_initial_relation": (
            "(10+56b^2)v_t(0)-(4+56b^2)u(0)=b(1-4b^2)"
        ),
        "particular_cubic_initial_relation_verified": relation_verified,
        "interpretation": (
            "The zero-linear-amplitude forced particular branch admits a "
            "log-free cubic start; no x^3 log(x) term is forced by the "
            "leading rotational source."
        ),
    }


def centrifugal_transformed_origin_certificate() -> dict[str, object]:
    """Return the scoped exact desingularization and floating replay record."""
    center_probes = (
        (Fraction(7, 5), Fraction(-2, 3), Fraction(11, 7), Fraction(5, 9)),
        (Fraction(13, 8), Fraction(3, 4), Fraction(-4, 5), Fraction(2, 11)),
    )
    center_checks: list[bool] = []
    for w, w_t, u, u_t in center_probes:
        record = transformed_quadrupole_reduced_density_from_kernels(
            t=Fraction(0),
            metric_factor=Fraction(1),
            profile_deficit_over_radius=w,
            profile_deficit_time_derivative=w_t,
            sine_over_radius=w,
            cosine_of_profile_deficit=Fraction(1),
            v=Fraction(1),
            u=u,
            v_time_derivative=Fraction(-7, 6),
            u_time_derivative=u_t,
            pion_mass_squared=Fraction(17, 10),
        )
        center_checks.append(record["reduced_density"] == Fraction(1, 6))

    probes = (
        (1.0e-4, 0.0025, 1.58, -0.23, 0.7, -0.4, 0.2, -0.1, 1.0),
        (0.015, 0.0025, 1.55, -0.18, -0.3, 0.8, -0.15, 0.25, 1.0),
        (0.21, 0.0025, 1.32, -0.09, 0.5, 0.1, 0.31, -0.27, 1.0),
    )
    direct_errors = tuple(_direct_density_check(probe) for probe in probes)
    cubic_compatibility = _forced_cubic_compatibility_record()
    return {
        "result_type": "exact_transformed_origin_density_identity",
        "change_of_variables": {
            "radial_coordinate": "t=x^2",
            "profile": "F=pi-x w(t)",
            "tangential_field": "g=x v(t)",
            "radial_field": "f=x[-v(t)+t u(t)]",
        },
        "entire_kernels": (
            "s(t)=sin(sqrt(t) w(t))/sqrt(t), with s(0)=w(0)",
            "c(t)=cos(sqrt(t) w(t))",
        ),
        "density_factorization": "H_static=x^2 H_hat(t)",
        "negative_powers_of_t_in_H_hat": 0,
        "center_reduced_density": "H_hat(0)=v(0)^2/6",
        "exact_fraction_center_checks": tuple(center_checks),
        "floating_direct_replay_relative_errors": direct_errors,
        "maximum_floating_direct_replay_relative_error": max(direct_errors),
        "forced_cubic_compatibility": cubic_compatibility,
        "transformed_action_measure": (
            "H_static dx=(sqrt(t)/2) H_hat(t) dt"
        ),
        "claim_boundary": (
            "Exact term-by-term algebraic desingularization of the full local "
            "K=2 static Hessian density. The transformed action retains the "
            "regular-singular sqrt(t) weight. This does not prove the "
            "Friedrichs-domain equivalence, a finite-cutoff Frobenius "
            "remainder, the two-parameter transfer map, coercivity, or a "
            "validated forced response."
        ),
    }
