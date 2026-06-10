"""Untrusted rational certificate data for the global Skyrmion BVP.

The floating hard-wall solver and finite differences in this module are only
proposal mechanisms.  The returned exact-rational splines, jet boxes, and
residual boxes are intended as input to a separate trusted checker.  No field
named ``status`` or boolean proof claim is deliberately provided here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from math import comb, cos, isfinite, sin

from .massive_skyrmion_worldtube import (
    curved_profile_acceleration,
    origin_cubic_coefficient,
    solve_hard_wall_skyrmion_profile,
)
from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    cos_center_lipschitz_interval,
    sin_center_lipschitz_interval,
)
from .validated_skyrmion_origin import (
    validate_skyrmion_origin_quintic_branch_identification,
    validate_skyrmion_origin_quintic_patch,
    validate_skyrmion_origin_sensitivity,
)


@dataclass(frozen=True)
class RationalSplineCell:
    """One normalized-coordinate quintic and its recomputable cell data."""

    radius: RationalInterval
    profile_polynomial: RationalPolynomial
    profile: RationalInterval
    derivative: RationalInterval
    second_derivative: RationalInterval
    coarse_nonlinear_residual: RationalInterval
    coarse_nonlinear_residual_absolute_upper: Fraction
    nonlinear_residual_subcells: tuple[RationalInterval, ...]
    nonlinear_residual: RationalInterval
    nonlinear_residual_absolute_upper: Fraction

    @property
    def width(self) -> Fraction:
        return self.radius.upper - self.radius.lower


@dataclass(frozen=True)
class RationalHomogeneousCell:
    """Untrusted candidate data for one homogeneous Jacobi spline."""

    radius: RationalInterval
    function_polynomial: RationalPolynomial
    function: RationalInterval
    derivative: RationalInterval
    second_derivative: RationalInterval
    coarse_jacobi_residual: RationalInterval
    coarse_jacobi_residual_absolute_upper: Fraction
    jacobi_residual_subcells: tuple[RationalInterval, ...]
    jacobi_residual: RationalInterval
    jacobi_residual_absolute_upper: Fraction


@dataclass(frozen=True)
class GlobalBvpCertificateCandidate:
    """Untrusted data bundle for independent residual/coercivity checking."""

    result_type: str
    shooting_slope: Fraction
    radius_start: Fraction
    radius_end: Fraction
    mesh_width: Fraction | None
    mesh_nodes: tuple[Fraction, ...]
    profile_degree: int
    cells: tuple[RationalSplineCell, ...]
    boundary_residuals: dict[str, RationalInterval]
    maximum_nonlinear_residual_absolute_upper: Fraction
    homogeneous_degree: int | None
    homogeneous_cells: tuple[RationalHomogeneousCell, ...]
    maximum_homogeneous_residual_absolute_upper: Fraction | None
    fundamental_degree: int | None
    fundamental_cells: tuple[RationalHomogeneousCell, ...]
    maximum_fundamental_residual_absolute_upper: Fraction | None
    schur_auxiliary_degree: int | None
    schur_auxiliary_cells: tuple[RationalHomogeneousCell, ...]
    maximum_schur_auxiliary_residual_absolute_upper: Fraction | None
    schur_combination_coefficient: Fraction | None
    raw_schur_candidate: RationalInterval | None
    auxiliary_boundary_residuals: dict[str, RationalInterval]
    floating_diagnostics: dict[str, float | int | str]

    @property
    def shooting_sensitivity_cells(self) -> tuple[RationalHomogeneousCell, ...]:
        """Return the legacy finite-difference proposal ``Y`` explicitly."""
        return self.homogeneous_cells


def _fraction(name: str, value: int | Fraction, *, positive: bool = False) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    result = Fraction(value)
    if positive and result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _explicit_mesh_nodes(
    values: Sequence[int | Fraction],
    *,
    radius_start: Fraction,
    radius_end: Fraction,
) -> tuple[Fraction, ...]:
    """Validate an exact, strictly increasing mesh with fixed endpoints."""
    if isinstance(values, (str, bytes)):
        raise TypeError("mesh_nodes must be a sequence of integers or Fractions")
    nodes = tuple(
        _fraction(f"mesh_nodes[{index}]", value, positive=True)
        for index, value in enumerate(values)
    )
    if len(nodes) < 2:
        raise ValueError("mesh_nodes must contain at least two endpoints")
    if nodes[0] != radius_start or nodes[-1] != radius_end:
        raise ValueError("mesh_nodes must begin at radius_start and end at radius_end")
    if any(right <= left for left, right in zip(nodes, nodes[1:])):
        raise ValueError("mesh_nodes must be strictly increasing")
    return nodes


def subdivide_explicit_mesh_nodes(
    mesh_nodes: Sequence[int | Fraction],
    subdivisions_by_source_cell: Mapping[int, int],
) -> tuple[Fraction, ...]:
    """Insert exact equal-width nodes into selected source mesh cells.

    This is a proposal-only refinement control.  Passing its output back as
    ``mesh_nodes`` regenerates the profile and every auxiliary family on one
    common exact mesh; it does not splice or reinterpret an existing spline.
    Source-cell indices refer to the supplied mesh before refinement.
    """
    if not isinstance(mesh_nodes, Sequence) or isinstance(
        mesh_nodes, (str, bytes)
    ):
        raise TypeError("mesh_nodes must be a sequence of integers or Fractions")
    nodes = tuple(
        _fraction(f"mesh_nodes[{index}]", value, positive=True)
        for index, value in enumerate(mesh_nodes)
    )
    if len(nodes) < 2:
        raise ValueError("mesh_nodes must contain at least two endpoints")
    if any(right <= left for left, right in zip(nodes, nodes[1:])):
        raise ValueError("mesh_nodes must be strictly increasing")
    if not isinstance(subdivisions_by_source_cell, Mapping):
        raise TypeError("subdivisions_by_source_cell must be a mapping")

    cell_count = len(nodes) - 1
    factors: dict[int, int] = {}
    for source_index, factor in subdivisions_by_source_cell.items():
        if isinstance(source_index, bool) or not isinstance(source_index, int):
            raise TypeError("source-cell indices must be integers")
        if source_index < 0 or source_index >= cell_count:
            raise ValueError("source-cell index is outside the supplied mesh")
        if isinstance(factor, bool) or not isinstance(factor, int):
            raise TypeError("subdivision factors must be integers")
        if factor < 1:
            raise ValueError("subdivision factors must be positive")
        factors[source_index] = factor

    refined = [nodes[0]]
    for source_index, (left, right) in enumerate(zip(nodes, nodes[1:])):
        factor = factors.get(source_index, 1)
        width = right - left
        refined.extend(
            left + width * Fraction(part, factor)
            for part in range(1, factor + 1)
        )
    return tuple(refined)


def _rationalize(value: float, denominator: int) -> Fraction:
    if not isfinite(value):
        raise ValueError("floating proposal data must be finite")
    return Fraction(value).limit_denominator(denominator)


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _quintic_hermite_polynomial(
    value_start: Fraction,
    derivative_start: Fraction,
    second_start: Fraction,
    value_end: Fraction,
    derivative_end: Fraction,
    second_end: Fraction,
    width: Fraction,
) -> RationalPolynomial:
    """Interpolate endpoint value, first derivative, and second derivative."""
    a0 = value_start
    a1 = width * derivative_start
    a2 = width**2 * second_start / 2
    value_gap = value_end - a0 - a1 - a2
    derivative_gap = width * derivative_end - a1 - 2 * a2
    second_gap = width**2 * second_end - 2 * a2
    a3 = 10 * value_gap - 4 * derivative_gap + second_gap / 2
    a4 = -15 * value_gap + 7 * derivative_gap - second_gap
    a5 = 6 * value_gap - 3 * derivative_gap + second_gap / 2
    return RationalPolynomial((a0, a1, a2, a3, a4, a5))


def _rk4_step(
    radius: float,
    profile: float,
    derivative: float,
    width: float,
    *,
    pion_mass: float,
    curvature: float,
) -> tuple[float, float]:
    def rhs(x: float, value: float, slope: float) -> tuple[float, float]:
        return slope, curved_profile_acceleration(
            x,
            value,
            slope,
            pion_mass=pion_mass,
            curvature=curvature,
        )

    k1 = rhs(radius, profile, derivative)
    k2 = rhs(
        radius + width / 2,
        profile + width * k1[0] / 2,
        derivative + width * k1[1] / 2,
    )
    k3 = rhs(
        radius + width / 2,
        profile + width * k2[0] / 2,
        derivative + width * k2[1] / 2,
    )
    k4 = rhs(
        radius + width,
        profile + width * k3[0],
        derivative + width * k3[1],
    )
    return (
        profile + width * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6,
        derivative
        + width * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6,
    )


def _sample_profile(
    shooting_slope: float,
    nodes: tuple[Fraction, ...],
    *,
    pion_mass: float,
    curvature: float,
    integration_step: float,
    origin_cutoff: float,
) -> tuple[tuple[float, float, float], ...]:
    cubic = origin_cubic_coefficient(
        shooting_slope,
        pion_mass=pion_mass,
        curvature=curvature,
    )
    radius = origin_cutoff
    profile = 3.141592653589793 - shooting_slope * radius + cubic * radius**3
    derivative = -shooting_slope + 3 * cubic * radius**2
    result: list[tuple[float, float, float]] = []
    for exact_node in nodes:
        target = float(exact_node)
        while radius < target:
            width = min(integration_step, target - radius)
            profile, derivative = _rk4_step(
                radius,
                profile,
                derivative,
                width,
                pion_mass=pion_mass,
                curvature=curvature,
            )
            radius += width
        acceleration = curved_profile_acceleration(
            target,
            profile,
            derivative,
            pion_mass=pion_mass,
            curvature=curvature,
        )
        result.append((profile, derivative, acceleration))
    return tuple(result)


def _floating_jacobi_acceleration(
    radius: float,
    profile: float,
    profile_derivative: float,
    profile_second_derivative: float,
    function: float,
    derivative: float,
    *,
    pion_mass_squared: float,
    curvature: float,
) -> float:
    """Return the floating Jacobi acceleration used only to propose ``K``."""
    radius_squared = radius * radius
    lapse = 1 - curvature * radius_squared
    lapse_derivative = -2 * curvature * radius
    sine = sin(profile)
    sine_twice = sin(2 * profile)
    cosine = cos(profile)
    cosine_twice = cos(2 * profile)
    principal = lapse * (radius_squared + 8 * sine * sine)
    principal_derivative = lapse_derivative * (
        radius_squared + 8 * sine * sine
    ) + lapse * (2 * radius + 8 * sine_twice * profile_derivative)
    potential = (
        4 * sine_twice * sine_twice / radius_squared
        + 2 * (1 + 4 * sine * sine / radius_squared) * cosine_twice
        - 8 * lapse * cosine_twice * profile_derivative * profile_derivative
        + pion_mass_squared * radius_squared * cosine
        - 8 * lapse_derivative * sine_twice * profile_derivative
        - 8 * lapse * sine_twice * profile_second_derivative
    )
    return (potential * function - principal_derivative * derivative) / principal


def _sample_jacobi_fundamental(
    profile_start: float,
    profile_derivative_start: float,
    nodes: tuple[Fraction, ...],
    *,
    pion_mass_squared: float,
    curvature: float,
    integration_step: float,
) -> tuple[tuple[float, float, float], ...]:
    """Propose ``K`` with ``K(a)=0,K'(a)=1`` by floating coupled RK4."""
    radius = float(nodes[0])
    profile = profile_start
    profile_derivative = profile_derivative_start
    function = 0.0
    derivative = 1.0

    def rhs(
        x: float,
        value: float,
        slope: float,
        auxiliary: float,
        auxiliary_slope: float,
    ) -> tuple[float, float, float, float]:
        acceleration = curved_profile_acceleration(
            x,
            value,
            slope,
            pion_mass=pion_mass_squared**0.5,
            curvature=curvature,
        )
        auxiliary_acceleration = _floating_jacobi_acceleration(
            x,
            value,
            slope,
            acceleration,
            auxiliary,
            auxiliary_slope,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
        )
        return slope, acceleration, auxiliary_slope, auxiliary_acceleration

    result: list[tuple[float, float, float]] = []
    for exact_node in nodes:
        target = float(exact_node)
        while radius < target:
            width = min(integration_step, target - radius)
            k1 = rhs(radius, profile, profile_derivative, function, derivative)
            k2 = rhs(
                radius + width / 2,
                profile + width * k1[0] / 2,
                profile_derivative + width * k1[1] / 2,
                function + width * k1[2] / 2,
                derivative + width * k1[3] / 2,
            )
            k3 = rhs(
                radius + width / 2,
                profile + width * k2[0] / 2,
                profile_derivative + width * k2[1] / 2,
                function + width * k2[2] / 2,
                derivative + width * k2[3] / 2,
            )
            k4 = rhs(
                radius + width,
                profile + width * k3[0],
                profile_derivative + width * k3[1],
                function + width * k3[2],
                derivative + width * k3[3],
            )
            profile += width * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
            profile_derivative += width * (
                k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]
            ) / 6
            function += width * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6
            derivative += width * (
                k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]
            ) / 6
            radius += width
        profile_second_derivative = curved_profile_acceleration(
            target,
            profile,
            profile_derivative,
            pion_mass=pion_mass_squared**0.5,
            curvature=curvature,
        )
        second_derivative = _floating_jacobi_acceleration(
            target,
            profile,
            profile_derivative,
            profile_second_derivative,
            function,
            derivative,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
        )
        result.append((function, derivative, second_derivative))
    return tuple(result)


def _jet_boxes(
    polynomial: RationalPolynomial,
    width: Fraction,
) -> tuple[RationalInterval, RationalInterval, RationalInterval]:
    profile = _bernstein_range(polynomial)
    derivative = _bernstein_range(polynomial.derivative()).scale(1 / width)
    second = _bernstein_range(polynomial.derivative().derivative()).scale(
        1 / width**2
    )
    return profile, derivative, second


def _bernstein_range(polynomial: RationalPolynomial) -> RationalInterval:
    """Enclose a power-basis polynomial on ``[0,1]`` by its Bernstein hull."""
    degree = polynomial.degree
    coefficients = polynomial.coefficients
    bernstein = []
    for index in range(degree + 1):
        bernstein.append(
            sum(
                coefficients[power]
                * Fraction(comb(index, power), comb(degree, power))
                for power in range(index + 1)
            )
        )
    return RationalInterval(min(bernstein), max(bernstein))


def _affine_restrict_polynomial(
    polynomial: RationalPolynomial,
    center: Fraction,
    half_width: Fraction,
) -> RationalPolynomial:
    """Return ``p(center + half_width * z)`` with exact coefficients."""
    shifted = polynomial.shift(center)
    return RationalPolynomial(
        tuple(
            coefficient * half_width**power
            for power, coefficient in enumerate(shifted.coefficients)
        )
    )


def _centered_subcell_range(
    polynomial: RationalPolynomial,
    center: Fraction,
    half_width: Fraction,
) -> RationalInterval:
    """Enclose a polynomial on one subcell after exact affine restriction."""
    restricted = _affine_restrict_polynomial(polynomial, center, half_width)
    return restricted.evaluate(RationalInterval(Fraction(-1), Fraction(1)))


def _hull(intervals: tuple[RationalInterval, ...]) -> RationalInterval:
    if not intervals:
        raise ValueError("at least one interval is required")
    return RationalInterval(
        min(interval.lower for interval in intervals),
        max(interval.upper for interval in intervals),
    )


def _centered_profile_subcell_boxes(
    polynomial: RationalPolynomial,
    cell_width: Fraction,
    subdivision_count: int,
) -> tuple[
    tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
        Fraction,
        Fraction,
    ],
    ...,
]:
    """Return local jet boxes and normalized endpoints for every subcell."""
    derivative = polynomial.derivative()
    second = derivative.derivative()
    normalized_half_width = Fraction(1, 2 * subdivision_count)
    result = []
    for index in range(subdivision_count):
        normalized_left = Fraction(index, subdivision_count)
        normalized_right = Fraction(index + 1, subdivision_count)
        normalized_center = (normalized_left + normalized_right) / 2
        result.append(
            (
                _centered_subcell_range(
                    polynomial, normalized_center, normalized_half_width
                ),
                _centered_subcell_range(
                    derivative, normalized_center, normalized_half_width
                ).scale(1 / cell_width),
                _centered_subcell_range(
                    second, normalized_center, normalized_half_width
                ).scale(1 / cell_width**2),
                normalized_left,
                normalized_right,
            )
        )
    return tuple(result)


def _nonlinear_residual_box(
    radius: RationalInterval,
    profile: RationalInterval,
    derivative: RationalInterval,
    second_derivative: RationalInterval,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
) -> RationalInterval:
    sine = sin_center_lipschitz_interval(profile, terms=trigonometric_terms)
    sine_twice = sin_center_lipschitz_interval(
        profile.scale(2), terms=trigonometric_terms
    )
    radius_squared = radius.power(2)
    lapse = RationalInterval.point(1) - radius_squared.scale(curvature)
    lapse_derivative = radius.scale(-2 * curvature)
    u = radius_squared + sine.power(2).scale(8)
    u_derivative = radius.scale(2) + (sine_twice * derivative).scale(8)
    principal = lapse * u
    principal_derivative = lapse_derivative * u + lapse * u_derivative
    source = (
        RationalInterval.point(1)
        + sine.power(2).scale(4) / radius_squared
        + (lapse * derivative.power(2)).scale(4)
    ) * sine_twice + (radius_squared * sine).scale(pion_mass_squared)
    return principal * second_derivative + principal_derivative * derivative - source


def _jacobi_residual_box(
    profile_cell: RationalSplineCell,
    function: RationalInterval,
    derivative: RationalInterval,
    second_derivative: RationalInterval,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
) -> RationalInterval:
    radius = profile_cell.radius
    profile = profile_cell.profile
    profile_derivative = profile_cell.derivative
    profile_second = profile_cell.second_derivative
    radius_squared = radius.power(2)
    lapse = RationalInterval.point(1) - radius_squared.scale(curvature)
    lapse_derivative = radius.scale(-2 * curvature)
    sine = sin_center_lipschitz_interval(profile, terms=trigonometric_terms)
    sine_twice = sin_center_lipschitz_interval(
        profile.scale(2), terms=trigonometric_terms
    )
    cosine = cos_center_lipschitz_interval(profile, terms=trigonometric_terms)
    cosine_twice = cos_center_lipschitz_interval(
        profile.scale(2), terms=trigonometric_terms
    )
    principal = lapse * (radius_squared + sine.power(2).scale(8))
    principal_derivative = lapse_derivative * (
        radius_squared + sine.power(2).scale(8)
    ) + lapse * (
        radius.scale(2) + (sine_twice * profile_derivative).scale(8)
    )
    potential = (
        sine_twice.power(2).scale(4) / radius_squared
        + (
            RationalInterval.point(1)
            + sine.power(2).scale(4) / radius_squared
        )
        * cosine_twice.scale(2)
        - (lapse * cosine_twice * profile_derivative.power(2)).scale(8)
        + (radius_squared * cosine).scale(pion_mass_squared)
        - (lapse_derivative * sine_twice * profile_derivative).scale(8)
        - (lapse * sine_twice * profile_second).scale(8)
    )
    return -(principal * second_derivative + principal_derivative * derivative) + (
        potential * function
    )


def _build_profile_cells(
    nodes: tuple[Fraction, ...],
    samples: tuple[tuple[Fraction, Fraction, Fraction], ...],
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_subdivisions: int,
) -> tuple[RationalSplineCell, ...]:
    result: list[RationalSplineCell] = []
    for index, (left, right) in enumerate(zip(nodes, nodes[1:])):
        width = right - left
        polynomial = _quintic_hermite_polynomial(
            *samples[index], *samples[index + 1], width
        )
        profile, derivative, second = _jet_boxes(polynomial, width)
        radius = RationalInterval(left, right)
        coarse_residual = _nonlinear_residual_box(
            radius,
            profile,
            derivative,
            second,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
            trigonometric_terms=trigonometric_terms,
        )
        residual_subcells = tuple(
            _nonlinear_residual_box(
                RationalInterval(
                    left + width * normalized_left,
                    left + width * normalized_right,
                ),
                local_profile,
                local_derivative,
                local_second,
                pion_mass_squared=pion_mass_squared,
                curvature=curvature,
                trigonometric_terms=trigonometric_terms,
            )
            for (
                local_profile,
                local_derivative,
                local_second,
                normalized_left,
                normalized_right,
            ) in _centered_profile_subcell_boxes(
                polynomial, width, residual_subdivisions
            )
        )
        residual = _hull(residual_subcells)
        result.append(
            RationalSplineCell(
                radius=radius,
                profile_polynomial=polynomial,
                profile=profile,
                derivative=derivative,
                second_derivative=second,
                coarse_nonlinear_residual=coarse_residual,
                coarse_nonlinear_residual_absolute_upper=_absolute_upper(
                    coarse_residual
                ),
                nonlinear_residual_subcells=residual_subcells,
                nonlinear_residual=residual,
                nonlinear_residual_absolute_upper=_absolute_upper(residual),
            )
        )
    return tuple(result)


def _build_jacobi_cells(
    nodes: tuple[Fraction, ...],
    samples: tuple[tuple[Fraction, Fraction, Fraction], ...],
    profile_cells: tuple[RationalSplineCell, ...],
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_subdivisions: int,
) -> tuple[RationalHomogeneousCell, ...]:
    result: list[RationalHomogeneousCell] = []
    for index, (left, right) in enumerate(zip(nodes, nodes[1:])):
        width = right - left
        polynomial = _quintic_hermite_polynomial(
            *samples[index], *samples[index + 1], width
        )
        function, derivative, second = _jet_boxes(polynomial, width)
        coarse_residual = _jacobi_residual_box(
            profile_cells[index],
            function,
            derivative,
            second,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
            trigonometric_terms=trigonometric_terms,
        )
        profile_polynomial = profile_cells[index].profile_polynomial
        profile_subcells = _centered_profile_subcell_boxes(
            profile_polynomial, width, residual_subdivisions
        )
        function_subcells = _centered_profile_subcell_boxes(
            polynomial, width, residual_subdivisions
        )
        residual_subcells_list = []
        for profile_data, function_data in zip(
            profile_subcells, function_subcells
        ):
            (
                local_profile,
                local_profile_derivative,
                local_profile_second,
                normalized_left,
                normalized_right,
            ) = profile_data
            (
                local_function,
                local_function_derivative,
                local_function_second,
                function_left,
                function_right,
            ) = function_data
            if (function_left, function_right) != (
                normalized_left,
                normalized_right,
            ):
                raise AssertionError("profile and Jacobi subcells must coincide")
            local_profile_cell = RationalSplineCell(
                radius=RationalInterval(
                    left + width * normalized_left,
                    left + width * normalized_right,
                ),
                profile_polynomial=profile_polynomial,
                profile=local_profile,
                derivative=local_profile_derivative,
                second_derivative=local_profile_second,
                coarse_nonlinear_residual=RationalInterval.point(0),
                coarse_nonlinear_residual_absolute_upper=Fraction(0),
                nonlinear_residual_subcells=(),
                nonlinear_residual=RationalInterval.point(0),
                nonlinear_residual_absolute_upper=Fraction(0),
            )
            residual_subcells_list.append(
                _jacobi_residual_box(
                    local_profile_cell,
                    local_function,
                    local_function_derivative,
                    local_function_second,
                    pion_mass_squared=pion_mass_squared,
                    curvature=curvature,
                    trigonometric_terms=trigonometric_terms,
                )
            )
        residual_subcells = tuple(residual_subcells_list)
        residual = _hull(residual_subcells)
        result.append(
            RationalHomogeneousCell(
                radius=RationalInterval(left, right),
                function_polynomial=polynomial,
                function=function,
                derivative=derivative,
                second_derivative=second,
                coarse_jacobi_residual=coarse_residual,
                coarse_jacobi_residual_absolute_upper=_absolute_upper(
                    coarse_residual
                ),
                jacobi_residual_subcells=residual_subcells,
                jacobi_residual=residual,
                jacobi_residual_absolute_upper=_absolute_upper(residual),
            )
        )
    return tuple(result)


def _build_finite_difference_sensitivity_cells(
    nodes: tuple[Fraction, ...],
    minus: tuple[tuple[float, float, float], ...],
    plus: tuple[tuple[float, float, float], ...],
    profile_cells: tuple[RationalSplineCell, ...],
    *,
    slope_difference: Fraction,
    coefficient_denominator: int,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_subdivisions: int,
) -> tuple[RationalHomogeneousCell, ...]:
    scale = 1 / (2 * float(slope_difference))
    samples = tuple(
        tuple(
            _rationalize(
                (upper[column] - lower[column]) * scale,
                coefficient_denominator,
            )
            for column in range(3)
        )
        for lower, upper in zip(minus, plus)
    )
    return _build_jacobi_cells(
        nodes,
        samples,
        profile_cells,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
        residual_subdivisions=residual_subdivisions,
    )


def _combine_polynomials(
    left: RationalPolynomial,
    right: RationalPolynomial,
    right_scale: Fraction,
) -> RationalPolynomial:
    degree = max(left.degree, right.degree)
    return RationalPolynomial(
        tuple(
            (left.coefficients[index] if index <= left.degree else Fraction(0))
            + right_scale
            * (
                right.coefficients[index]
                if index <= right.degree
                else Fraction(0)
            )
            for index in range(degree + 1)
        )
    )


def _build_combined_jacobi_cells(
    shooting_cells: tuple[RationalHomogeneousCell, ...],
    fundamental_cells: tuple[RationalHomogeneousCell, ...],
    profile_cells: tuple[RationalSplineCell, ...],
    *,
    combination_coefficient: Fraction,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_subdivisions: int,
) -> tuple[RationalHomogeneousCell, ...]:
    if not (
        len(shooting_cells) == len(fundamental_cells) == len(profile_cells)
    ):
        raise ValueError("Jacobi cell collections must have equal lengths")
    samples: list[tuple[Fraction, Fraction, Fraction]] = []
    nodes = [profile_cells[0].radius.lower]
    for index, (shooting, fundamental, profile) in enumerate(
        zip(shooting_cells, fundamental_cells, profile_cells)
    ):
        if (
            shooting.radius != fundamental.radius
            or shooting.radius != profile.radius
        ):
            raise ValueError("Jacobi and profile meshes must coincide")
        polynomial = _combine_polynomials(
            shooting.function_polynomial,
            fundamental.function_polynomial,
            combination_coefficient,
        )
        width = profile.width
        left_values = []
        right_values = []
        differentiated = polynomial
        for derivative_order in range(3):
            scale = 1 / width**derivative_order
            left_values.append(
                differentiated.evaluate(Fraction(0)).lower * scale
            )
            right_values.append(
                differentiated.evaluate(Fraction(1)).lower * scale
            )
            differentiated = differentiated.derivative()
        if index == 0:
            samples.append(tuple(left_values))
        samples.append(tuple(right_values))
        nodes.append(profile.radius.upper)
    return _build_jacobi_cells(
        tuple(nodes),
        tuple(samples),
        profile_cells,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
        residual_subdivisions=residual_subdivisions,
    )


def generate_global_bvp_certificate_candidate(
    *,
    radius_start: Fraction = Fraction(1, 16),
    radius_end: Fraction = Fraction(4),
    mesh_width: Fraction = Fraction(1, 16),
    mesh_nodes: Sequence[int | Fraction] | None = None,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    coefficient_denominator: int = 10**12,
    integration_step: float = 1 / 2048,
    solver_step: float = 0.002,
    trigonometric_terms: int = 24,
    residual_subdivisions: int = 4,
    include_homogeneous_sensitivity: bool = True,
    sensitivity_slope_difference: Fraction = Fraction(1, 10**5),
) -> GlobalBvpCertificateCandidate:
    """Generate globally C2 exact-rational proposal data on one exact mesh.

    Quintic Hermite cells interpolate rationalized floating values of
    ``F,F',F''``.  The small nonzero floating wall value is retained and
    reported as a boundary residual; snapping it to zero would manufacture a
    high-curvature layer in the final cell.  Optional central differences in
    the shooting slope produce the regular sensitivity proposal ``Y``.  A
    separate floating Jacobi solve proposes ``K(a)=0,K'(a)=1``; exact rational
    polynomial arithmetic then forms ``H=Y-Y(c)K/K(c)``, so ``H(c)=0`` exactly.
    The reported raw Schur interval has not had a certified residual/trace
    correction subtracted and is therefore proposal data, not a proof.

    By default ``mesh_width`` generates the historical uniform mesh.  When
    ``mesh_nodes`` is supplied, it is authoritative, must contain exact
    rational endpoints from ``radius_start`` through ``radius_end``, and may
    be graded.  The returned ``mesh_width`` is then ``None`` so downstream
    consumers cannot accidentally treat the graded mesh as uniform.
    """
    start = _fraction("radius_start", radius_start, positive=True)
    end = _fraction("radius_end", radius_end, positive=True)
    mass_squared = _fraction("pion_mass_squared", pion_mass_squared)
    curvature_value = _fraction("curvature", curvature)
    sensitivity_width = _fraction(
        "sensitivity_slope_difference", sensitivity_slope_difference, positive=True
    )
    if end <= start:
        raise ValueError("radius_end must exceed radius_start")
    if mesh_nodes is None:
        width: Fraction | None = _fraction(
            "mesh_width", mesh_width, positive=True
        )
        if (end - start) / width % 1:
            raise ValueError("mesh_width must divide the requested radius interval")
        cell_count = int((end - start) / width)
        nodes = tuple(start + index * width for index in range(cell_count + 1))
        mesh_kind = "uniform"
    else:
        width = None
        nodes = _explicit_mesh_nodes(
            mesh_nodes,
            radius_start=start,
            radius_end=end,
        )
        cell_count = len(nodes) - 1
        mesh_kind = "explicit"
    if mass_squared < 0 or curvature_value < 0:
        raise ValueError("mass squared and curvature must be nonnegative")
    if curvature_value * end**2 >= 1:
        raise ValueError("the complete mesh must lie inside the static-patch horizon")
    if (
        isinstance(coefficient_denominator, bool)
        or not isinstance(coefficient_denominator, int)
        or coefficient_denominator < 1
    ):
        raise ValueError("coefficient_denominator must be a positive integer")
    if not isfinite(integration_step) or integration_step <= 0:
        raise ValueError("integration_step must be finite and positive")
    if (
        isinstance(trigonometric_terms, bool)
        or not isinstance(trigonometric_terms, int)
        or trigonometric_terms < 1
    ):
        raise ValueError("trigonometric_terms must be a positive integer")
    if (
        isinstance(residual_subdivisions, bool)
        or not isinstance(residual_subdivisions, int)
        or residual_subdivisions < 1
    ):
        raise ValueError("residual_subdivisions must be a positive integer")

    floating_slope, _ = solve_hard_wall_skyrmion_profile(
        pion_mass=float(mass_squared) ** 0.5,
        curvature=float(curvature_value),
        wall_radius=float(end),
        step=solver_step,
    )
    shooting_slope = _rationalize(floating_slope, coefficient_denominator)
    origin = validate_skyrmion_origin_quintic_patch(
        shooting_slope,
        cutoff=start,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
    )
    raw_samples = _sample_profile(
        float(shooting_slope),
        nodes,
        pion_mass=float(mass_squared) ** 0.5,
        curvature=float(curvature_value),
        integration_step=integration_step,
        origin_cutoff=1.0e-4,
    )
    rational_samples = [
        tuple(_rationalize(value, coefficient_denominator) for value in sample)
        for sample in raw_samples
    ]
    anchored_profile = origin.profile_at_cutoff.midpoint
    anchored_derivative = origin.derivative_at_cutoff.midpoint
    anchored_acceleration = _rationalize(
        curved_profile_acceleration(
            float(start),
            float(anchored_profile),
            float(anchored_derivative),
            pion_mass=float(mass_squared) ** 0.5,
            curvature=float(curvature_value),
        ),
        coefficient_denominator,
    )
    rational_samples[0] = (
        anchored_profile,
        anchored_derivative,
        anchored_acceleration,
    )
    floating_wall_value = raw_samples[-1][0]
    samples = tuple(rational_samples)
    cells = _build_profile_cells(
        nodes,
        samples,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        trigonometric_terms=trigonometric_terms,
        residual_subdivisions=residual_subdivisions,
    )

    left_profile = cells[0].profile_polynomial.evaluate(Fraction(0))
    left_derivative = cells[0].profile_polynomial.derivative().evaluate(
        Fraction(0)
    ).scale(1 / cells[0].width)
    right_profile = cells[-1].profile_polynomial.evaluate(Fraction(1))
    boundary_residuals = {
        "left_profile_minus_validated_origin_box": (
            left_profile - origin.profile_at_cutoff
        ),
        "left_derivative_minus_validated_origin_box": (
            left_derivative - origin.derivative_at_cutoff
        ),
        "right_dirichlet_profile": right_profile,
    }

    homogeneous_cells: tuple[RationalHomogeneousCell, ...] = ()
    homogeneous_maximum: Fraction | None = None
    fundamental_cells: tuple[RationalHomogeneousCell, ...] = ()
    fundamental_maximum: Fraction | None = None
    schur_auxiliary_cells: tuple[RationalHomogeneousCell, ...] = ()
    schur_auxiliary_maximum: Fraction | None = None
    schur_combination_coefficient: Fraction | None = None
    raw_schur_candidate: RationalInterval | None = None
    auxiliary_boundary_residuals: dict[str, RationalInterval] = {}
    if include_homogeneous_sensitivity:
        minus = _sample_profile(
            float(shooting_slope - sensitivity_width),
            nodes,
            pion_mass=float(mass_squared) ** 0.5,
            curvature=float(curvature_value),
            integration_step=integration_step,
            origin_cutoff=1.0e-4,
        )
        plus = _sample_profile(
            float(shooting_slope + sensitivity_width),
            nodes,
            pion_mass=float(mass_squared) ** 0.5,
            curvature=float(curvature_value),
            integration_step=integration_step,
            origin_cutoff=1.0e-4,
        )
        homogeneous_cells = _build_finite_difference_sensitivity_cells(
            nodes,
            minus,
            plus,
            cells,
            slope_difference=sensitivity_width,
            coefficient_denominator=coefficient_denominator,
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
            trigonometric_terms=trigonometric_terms,
            residual_subdivisions=residual_subdivisions,
        )
        homogeneous_maximum = max(
            cell.jacobi_residual_absolute_upper for cell in homogeneous_cells
        )

        raw_fundamental_samples = _sample_jacobi_fundamental(
            raw_samples[0][0],
            raw_samples[0][1],
            nodes,
            pion_mass_squared=float(mass_squared),
            curvature=float(curvature_value),
            integration_step=integration_step,
        )
        rational_fundamental_samples = tuple(
            tuple(
                _rationalize(value, coefficient_denominator) for value in sample
            )
            for sample in raw_fundamental_samples
        )
        first_fundamental = list(rational_fundamental_samples[0])
        first_fundamental[0] = Fraction(0)
        first_fundamental[1] = Fraction(1)
        rational_fundamental_samples = (
            tuple(first_fundamental),
        ) + rational_fundamental_samples[1:]
        fundamental_cells = _build_jacobi_cells(
            nodes,
            rational_fundamental_samples,
            cells,
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
            trigonometric_terms=trigonometric_terms,
            residual_subdivisions=residual_subdivisions,
        )
        fundamental_maximum = max(
            cell.jacobi_residual_absolute_upper for cell in fundamental_cells
        )

        shooting_wall = homogeneous_cells[-1].function_polynomial.evaluate(
            Fraction(1)
        ).lower
        fundamental_wall = fundamental_cells[-1].function_polynomial.evaluate(
            Fraction(1)
        ).lower
        if fundamental_wall == 0:
            raise ValueError("floating fundamental proposal has zero wall trace")
        schur_combination_coefficient = -shooting_wall / fundamental_wall
        schur_auxiliary_cells = _build_combined_jacobi_cells(
            homogeneous_cells,
            fundamental_cells,
            cells,
            combination_coefficient=schur_combination_coefficient,
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
            trigonometric_terms=trigonometric_terms,
            residual_subdivisions=residual_subdivisions,
        )
        schur_auxiliary_maximum = max(
            cell.jacobi_residual_absolute_upper
            for cell in schur_auxiliary_cells
        )

        sensitivity = validate_skyrmion_origin_sensitivity(
            RationalInterval(
                shooting_slope - sensitivity_width,
                shooting_slope + sensitivity_width,
            ),
            cutoff=start,
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
        )
        validate_skyrmion_origin_quintic_branch_identification(
            origin,
            sensitivity,
        )

        def endpoint(
            collection: tuple[RationalHomogeneousCell, ...],
            *,
            at_right: bool,
            derivative_order: int = 0,
        ) -> RationalInterval:
            cell = collection[-1] if at_right else collection[0]
            polynomial = cell.function_polynomial
            for _ in range(derivative_order):
                polynomial = polynomial.derivative()
            point = Fraction(1) if at_right else Fraction(0)
            return polynomial.evaluate(point).scale(
                1 / cell.radius.width**derivative_order
            )

        shooting_left = endpoint(homogeneous_cells, at_right=False)
        shooting_left_derivative = endpoint(
            homogeneous_cells, at_right=False, derivative_order=1
        )
        shooting_right = endpoint(homogeneous_cells, at_right=True)
        fundamental_left = endpoint(fundamental_cells, at_right=False)
        fundamental_left_derivative = endpoint(
            fundamental_cells, at_right=False, derivative_order=1
        )
        fundamental_right = endpoint(fundamental_cells, at_right=True)
        auxiliary_left = endpoint(schur_auxiliary_cells, at_right=False)
        auxiliary_left_derivative = endpoint(
            schur_auxiliary_cells, at_right=False, derivative_order=1
        )
        auxiliary_right = endpoint(schur_auxiliary_cells, at_right=True)
        raw_schur_candidate = auxiliary_left_derivative - sensitivity.gamma_b
        auxiliary_boundary_residuals = {
            "shooting_left_value_minus_phi_b": (
                shooting_left - sensitivity.phi_b
            ),
            "shooting_left_derivative_minus_gamma_b": (
                shooting_left_derivative - sensitivity.gamma_b
            ),
            "shooting_right_value": shooting_right,
            "fundamental_left_value": fundamental_left,
            "fundamental_left_derivative_minus_one": (
                fundamental_left_derivative - 1
            ),
            "fundamental_right_value": fundamental_right,
            "schur_auxiliary_left_value_minus_phi_b": (
                auxiliary_left - sensitivity.phi_b
            ),
            "schur_auxiliary_right_value": auxiliary_right,
            "raw_schur_candidate": raw_schur_candidate,
        }

    worst_profile_residual_index = max(
        range(len(cells)),
        key=lambda index: cells[index].nonlinear_residual_absolute_upper,
    )
    worst_profile_residual_cell = cells[worst_profile_residual_index]
    return GlobalBvpCertificateCandidate(
        result_type="untrusted_global_bvp_certificate_candidate_data",
        shooting_slope=shooting_slope,
        radius_start=start,
        radius_end=end,
        mesh_width=width,
        mesh_nodes=nodes,
        profile_degree=5,
        cells=cells,
        boundary_residuals=boundary_residuals,
        maximum_nonlinear_residual_absolute_upper=max(
            cell.nonlinear_residual_absolute_upper for cell in cells
        ),
        homogeneous_degree=5 if homogeneous_cells else None,
        homogeneous_cells=homogeneous_cells,
        maximum_homogeneous_residual_absolute_upper=homogeneous_maximum,
        fundamental_degree=5 if fundamental_cells else None,
        fundamental_cells=fundamental_cells,
        maximum_fundamental_residual_absolute_upper=fundamental_maximum,
        schur_auxiliary_degree=5 if schur_auxiliary_cells else None,
        schur_auxiliary_cells=schur_auxiliary_cells,
        maximum_schur_auxiliary_residual_absolute_upper=(
            schur_auxiliary_maximum
        ),
        schur_combination_coefficient=schur_combination_coefficient,
        raw_schur_candidate=raw_schur_candidate,
        auxiliary_boundary_residuals=auxiliary_boundary_residuals,
        floating_diagnostics={
            "cell_count": cell_count,
            "mesh_kind": mesh_kind,
            "minimum_mesh_width": float(
                min(right - left for left, right in zip(nodes, nodes[1:]))
            ),
            "maximum_mesh_width": float(
                max(right - left for left, right in zip(nodes, nodes[1:]))
            ),
            "residual_subdivisions_per_cell": residual_subdivisions,
            "coarse_maximum_nonlinear_residual_absolute_upper": float(
                max(
                    cell.coarse_nonlinear_residual_absolute_upper
                    for cell in cells
                )
            ),
            "centered_maximum_nonlinear_residual_absolute_upper": float(
                max(cell.nonlinear_residual_absolute_upper for cell in cells)
            ),
            "worst_profile_residual_source_cell": worst_profile_residual_index,
            "worst_profile_residual_radius_lower": float(
                worst_profile_residual_cell.radius.lower
            ),
            "worst_profile_residual_radius_upper": float(
                worst_profile_residual_cell.radius.upper
            ),
            "floating_shooting_slope": floating_slope,
            "floating_wall_dirichlet_residual": floating_wall_value,
            "integration_step": integration_step,
            "floating_fundamental_wall_value": (
                raw_fundamental_samples[-1][0]
                if include_homogeneous_sensitivity
                else "not generated"
            ),
            "rational_schur_combination_coefficient": (
                float(schur_combination_coefficient)
                if schur_combination_coefficient is not None
                else "not generated"
            ),
            "raw_schur_candidate_lower": (
                float(raw_schur_candidate.lower)
                if raw_schur_candidate is not None
                else "not generated"
            ),
            "raw_schur_candidate_upper": (
                float(raw_schur_candidate.upper)
                if raw_schur_candidate is not None
                else "not generated"
            ),
            "warning": (
                "Floating centers, finite differences, the fundamental solve, "
                "and the raw Schur margin are untrusted; a separate checker must "
                "recompute every residual, trace bound, and inequality."
            ),
        },
    )
