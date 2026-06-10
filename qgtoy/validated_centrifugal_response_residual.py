"""Validated positive-radius residuals for the centrifugal weak problem.

The authenticated profile replay supplies interval boxes for ``F``, ``F'``,
and ``F''``.  This module converts one such box into interval enclosures of
the physical conormal blocks

``q(y,v)=integral v^T C y+v^T M y'+v'^T M^T y+v'^T P y'``

and of the strong rotational source.  Exact rational piecewise-polynomial
trials can then be ranged cell by cell without numerical differentiation.

Only cells with strictly positive left endpoint are accepted.  The regular
``t=x^2`` origin calculation has different cancellation requirements and must
be certified separately before these bounds cover the full interval.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TYPE_CHECKING, TypeAlias

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
    regular_rotational_source_from_kernels,
)
from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    cos_center_lipschitz_interval,
    sin_center_lipschitz_interval,
    sqrt_fraction_interval,
)
from .validated_centrifugal_global_form import (
    validate_centrifugal_wall_trace,
)

if TYPE_CHECKING:
    from .validated_skyrmion_sharp_profile import (
        ValidatedSkyrmionSharpRadialCell,
    )


IntervalVector2: TypeAlias = tuple[RationalInterval, RationalInterval]
IntervalMatrix2: TypeAlias = tuple[IntervalVector2, IntervalVector2]


COMPACT_PI_INTERVAL = RationalInterval(
    Fraction(103993, 33102),
    Fraction(104348, 33215),
)


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _outward_round_interval(
    value: RationalInterval,
    denominator: int,
) -> RationalInterval:
    if (
        isinstance(denominator, bool)
        or not isinstance(denominator, int)
        or denominator < 1
    ):
        raise ValueError("rounding denominator must be a positive integer")
    lower = value.lower.numerator * denominator // value.lower.denominator
    upper = -((-value.upper.numerator * denominator) // value.upper.denominator)
    return RationalInterval(Fraction(lower, denominator), Fraction(upper, denominator))


@dataclass(frozen=True)
class ValidatedProfileJetCell:
    """Authenticated-enclosure input on one positive-radius cell."""

    radius: RationalInterval
    profile: RationalInterval
    derivative: RationalInterval
    second_derivative: RationalInterval

    def __post_init__(self) -> None:
        if self.radius.lower <= 0 or self.radius.width <= 0:
            raise ValueError("profile cell must have positive radius and width")


def profile_jet_cell_from_sharp_replay(
    cell: ValidatedSkyrmionSharpRadialCell,
) -> ValidatedProfileJetCell:
    """Adapt one authenticated sharp-replay cell without widening it."""
    return ValidatedProfileJetCell(
        radius=cell.radius,
        profile=cell.solution_profile,
        derivative=cell.solution_derivative,
        second_derivative=cell.solution_second_derivative,
    )


def reduced_profile_trigonometric_intervals(
    profile: RationalInterval,
    *,
    trigonometric_terms: int = 12,
    rounding_denominator: int = 10**18,
) -> tuple[RationalInterval, RationalInterval]:
    """Enclose ``sin(F)`` and ``cos(pi-F)`` using the smaller half-period angle.

    The authenticated hedgehog runs from ``F`` near ``pi`` to ``F=0``. Direct
    Taylor evaluation near ``pi`` creates enormous exact fractions.  A Machin
    enclosure ``Pi`` contains the true value of pi, so ``D=Pi-F`` contains the
    exact deficit and safely gives ``sin(F)=sin(D)`` and
    ``cos(pi-F)=cos(D)``.  The narrower of the direct and deficit angles is
    used only to improve the enclosure; either branch is mathematically valid.
    """
    if not isinstance(profile, RationalInterval):
        raise TypeError("profile must be a RationalInterval")
    direct = _outward_round_interval(profile, rounding_denominator)
    deficit = _outward_round_interval(
        COMPACT_PI_INTERVAL - profile,
        rounding_denominator,
    )
    direct_size = max(abs(direct.lower), abs(direct.upper))
    deficit_size = max(abs(deficit.lower), abs(deficit.upper))
    if deficit_size < direct_size:
        return tuple(
            _outward_round_interval(value, rounding_denominator)
            for value in (
                sin_center_lipschitz_interval(
                    deficit, terms=trigonometric_terms
                ),
                cos_center_lipschitz_interval(
                    deficit, terms=trigonometric_terms
                ),
            )
        )
    return tuple(
        _outward_round_interval(value, rounding_denominator)
        for value in (
            sin_center_lipschitz_interval(
                direct, terms=trigonometric_terms
            ),
            -cos_center_lipschitz_interval(
                direct, terms=trigonometric_terms
            ),
        )
    )


@dataclass(frozen=True)
class RationalC1TrialCell:
    """Two trial polynomials in the normalized coordinate ``u in [0,1]``."""

    radius: RationalInterval
    radial_field: RationalPolynomial
    tangential_field: RationalPolynomial

    def __post_init__(self) -> None:
        if self.radius.width <= 0:
            raise ValueError("trial cell must have positive width")

    def jet_range(
        self,
    ) -> tuple[IntervalVector2, IntervalVector2, IntervalVector2]:
        unit = RationalInterval(Fraction(0), Fraction(1))
        width = self.radius.width
        fields = (self.radial_field, self.tangential_field)
        value = tuple(polynomial.evaluate(unit) for polynomial in fields)
        derivative = tuple(
            polynomial.derivative().evaluate(unit).scale(1 / width)
            for polynomial in fields
        )
        second_derivative = tuple(
            polynomial.derivative()
            .derivative()
            .evaluate(unit)
            .scale(1 / width**2)
            for polynomial in fields
        )
        return value, derivative, second_derivative  # type: ignore[return-value]

    def endpoint_jet(
        self, *, right: bool
    ) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
        argument = Fraction(1 if right else 0)
        width = self.radius.width
        fields = (self.radial_field, self.tangential_field)
        values = tuple(
            polynomial.evaluate(argument).lower for polynomial in fields
        )
        derivatives = tuple(
            polynomial.derivative().evaluate(argument).lower / width
            for polynomial in fields
        )
        return values, derivatives  # type: ignore[return-value]


def validate_rational_c1_trial_cells(
    cells: tuple[RationalC1TrialCell, ...],
    *,
    require_zero_tangential_wall_trace: bool = True,
) -> None:
    """Check exact contiguity, ``C1`` joins, and the essential wall trace."""
    if not cells:
        raise ValueError("at least one trial cell is required")
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("trial cells are not contiguous")
        if left.endpoint_jet(right=True) != right.endpoint_jet(right=False):
            raise ValueError("trial cells do not have an exact C1 join")
    if require_zero_tangential_wall_trace:
        values, _ = cells[-1].endpoint_jet(right=True)
        if values[1] != 0:
            raise ValueError("the essential tangential wall trace is nonzero")


@dataclass(frozen=True)
class _IntervalRadialJet:
    value: RationalInterval
    derivative: RationalInterval

    @classmethod
    def constant(cls, value: RationalInterval) -> _IntervalRadialJet:
        return cls(value, RationalInterval.point(0))

    def _coerce(
        self, other: _IntervalRadialJet | RationalInterval | int | Fraction
    ) -> _IntervalRadialJet:
        if isinstance(other, _IntervalRadialJet):
            return other
        if isinstance(other, RationalInterval):
            return self.constant(other)
        return self.constant(RationalInterval.point(other))

    def __add__(
        self, other: _IntervalRadialJet | RationalInterval | int | Fraction
    ) -> _IntervalRadialJet:
        right = self._coerce(other)
        return _IntervalRadialJet(
            self.value + right.value,
            self.derivative + right.derivative,
        )

    __radd__ = __add__

    def __neg__(self) -> _IntervalRadialJet:
        return _IntervalRadialJet(-self.value, -self.derivative)

    def __sub__(
        self, other: _IntervalRadialJet | RationalInterval | int | Fraction
    ) -> _IntervalRadialJet:
        return self + (-self._coerce(other))

    def __rsub__(
        self, other: _IntervalRadialJet | RationalInterval | int | Fraction
    ) -> _IntervalRadialJet:
        return self._coerce(other) - self

    def __mul__(
        self, other: _IntervalRadialJet | RationalInterval | int | Fraction
    ) -> _IntervalRadialJet:
        right = self._coerce(other)
        return _IntervalRadialJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(
        self, other: _IntervalRadialJet | RationalInterval | int | Fraction
    ) -> _IntervalRadialJet:
        right = self._coerce(other)
        denominator = right.value.power(2)
        return _IntervalRadialJet(
            self.value / right.value,
            (
                self.derivative * right.value
                - self.value * right.derivative
            )
            / denominator,
        )

    def __rtruediv__(
        self, other: _IntervalRadialJet | RationalInterval | int | Fraction
    ) -> _IntervalRadialJet:
        return self._coerce(other) / self


@dataclass(frozen=True)
class ValidatedConormalStrongCell:
    """Interval strong-form coefficients on one positive-radius cell."""

    radius: RationalInterval
    coordinate: IntervalMatrix2
    mixed: IntervalMatrix2
    principal: IntervalMatrix2
    mixed_derivative: IntervalMatrix2
    principal_derivative: IntervalMatrix2
    strong_source: IntervalVector2


@dataclass(frozen=True)
class ValidatedWallConormalCoefficients:
    """Exact endpoint blocks and pure-tension Robin completion at the wall."""

    wall_radius: Fraction
    mixed: IntervalMatrix2
    principal: IntervalMatrix2
    robin_multiplier: RationalInterval
    wall_form_coefficient: RationalInterval
    wall_trace_margin: RationalInterval


def validated_wall_conormal_coefficients(
    wall_profile_derivative: RationalInterval,
    *,
    wall_radius: Fraction = Fraction(4),
    curvature: Fraction = Fraction(1, 400),
    pion_mass_squared: Fraction = Fraction(1),
    membrane_tension: Fraction = Fraction(1931779647, 10**12),
    rounding_denominator: int = 10**18,
) -> ValidatedWallConormalCoefficients:
    """Build the physical endpoint ``M,P`` blocks and completed wall form."""
    trace = validate_centrifugal_wall_trace(
        wall_profile_derivative,
        wall_radius=wall_radius,
        curvature=curvature,
        membrane_tension=membrane_tension,
    )
    metric = Fraction(1) - curvature * wall_radius**2
    if metric <= 0:
        raise ValueError("wall must lie strictly inside the horizon")
    point = RationalInterval.point
    blocks = regular_conormal_blocks_from_kernels(
        t=point(wall_radius**2),
        metric_factor=point(metric),
        profile_deficit_radial_derivative=-wall_profile_derivative,
        sine_over_radius=point(0),
        cosine_of_profile_deficit=point(-1),
        pion_mass_squared=point(pion_mass_squared),
    )
    mixed = tuple(
        tuple(
            _outward_round_interval(
                entry.scale(wall_radius), rounding_denominator
            )
            for entry in row
        )
        for row in blocks["mixed"]
    )
    principal = tuple(
        tuple(
            _outward_round_interval(
                entry.scale(wall_radius**2), rounding_denominator
            )
            for entry in row
        )
        for row in blocks["principal"]
    )
    wall_form = -(
        principal[0][0] * trace.wall_robin_multiplier + mixed[0][0]
    )
    return ValidatedWallConormalCoefficients(
        wall_radius=wall_radius,
        mixed=mixed,  # type: ignore[arg-type]
        principal=principal,  # type: ignore[arg-type]
        robin_multiplier=trace.wall_robin_multiplier,
        wall_form_coefficient=_outward_round_interval(
            wall_form, rounding_denominator
        ),
        wall_trace_margin=trace.wall_trace_margin,
    )


def wall_endpoint_conormal_residual(
    *,
    coefficients: ValidatedWallConormalCoefficients,
    trial: RationalC1TrialCell,
    wall_load: RationalInterval = RationalInterval.point(0),
) -> RationalInterval:
    """Enclose the free radial endpoint equation for a supplied exact trial."""
    if trial.radius.upper != coefficients.wall_radius:
        raise ValueError("trial does not terminate at the certified wall")
    values, derivatives = trial.endpoint_jet(right=True)
    value = tuple(RationalInterval.point(entry) for entry in values)
    derivative = tuple(RationalInterval.point(entry) for entry in derivatives)
    conormal = tuple(
        left + right
        for left, right in zip(
            _matrix_vector(_transpose(coefficients.mixed), value),
            _matrix_vector(coefficients.principal, derivative),
            strict=True,
        )
    )
    return (
        conormal[0]
        + coefficients.wall_form_coefficient.scale(values[0])
        - wall_load
    )


def _jet_matrix_value(matrix: tuple[tuple[_IntervalRadialJet, ...], ...]) -> IntervalMatrix2:
    return tuple(
        tuple(entry.value for entry in row) for row in matrix
    )  # type: ignore[return-value]


def _jet_matrix_derivative(
    matrix: tuple[tuple[_IntervalRadialJet, ...], ...],
) -> IntervalMatrix2:
    return tuple(
        tuple(entry.derivative for entry in row) for row in matrix
    )  # type: ignore[return-value]


def validated_conormal_strong_cell_from_profile(
    profile: ValidatedProfileJetCell,
    *,
    curvature: Fraction = Fraction(1, 400),
    pion_mass_squared: Fraction = Fraction(1),
    trigonometric_terms: int = 12,
    rounding_denominator: int = 10**18,
) -> ValidatedConormalStrongCell:
    """Build strong-form coefficient boxes from an authenticated profile jet."""
    if not isinstance(curvature, Fraction) or not isinstance(
        pion_mass_squared, Fraction
    ):
        raise TypeError("curvature and pion_mass_squared must be Fractions")
    if curvature < 0 or pion_mass_squared < 0:
        raise ValueError("curvature and pion_mass_squared must be nonnegative")
    profile_value = _outward_round_interval(
        profile.profile, rounding_denominator
    )
    profile_derivative = _outward_round_interval(
        profile.derivative, rounding_denominator
    )
    profile_second_derivative = _outward_round_interval(
        profile.second_derivative, rounding_denominator
    )
    x = _IntervalRadialJet(profile.radius, RationalInterval.point(1))
    t = x * x
    metric = 1 - t * curvature
    if metric.value.lower <= 0:
        raise ValueError("profile cell must lie strictly inside the horizon")

    sine, cosine_deficit = reduced_profile_trigonometric_intervals(
        profile_value,
        trigonometric_terms=trigonometric_terms,
        rounding_denominator=rounding_denominator,
    )
    rho = _IntervalRadialJet(-profile_derivative, -profile_second_derivative)
    sine_over_radius_value = sine / profile.radius
    sine_over_radius = _IntervalRadialJet(
        sine_over_radius_value,
        (cosine_deficit * rho.value - sine_over_radius_value) / profile.radius,
    )
    cosine = _IntervalRadialJet(
        cosine_deficit,
        -(profile.radius * sine_over_radius_value * rho.value),
    )
    blocks = regular_conormal_blocks_from_kernels(
        t=t,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine,
        pion_mass_squared=_IntervalRadialJet.constant(
            RationalInterval.point(pion_mass_squared)
        ),
    )
    source = regular_rotational_source_from_kernels(
        t=t,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine,
    )
    coordinate_jets = blocks["coordinate"]
    mixed_jets = tuple(
        tuple(x * entry for entry in row) for row in blocks["mixed"]
    )
    principal_jets = tuple(
        tuple(t * entry for entry in row) for row in blocks["principal"]
    )
    coordinate_source = tuple(
        x * entry for entry in source["coordinate_source"]
    )
    derivative_source = tuple(
        t * entry for entry in source["derivative_source"]
    )
    strong_source = tuple(
        coordinate.value - derivative.derivative
        for coordinate, derivative in zip(
            coordinate_source, derivative_source, strict=True
        )
    )
    round_matrix = lambda matrix: tuple(  # noqa: E731
        tuple(
            _outward_round_interval(entry, rounding_denominator)
            for entry in row
        )
        for row in matrix
    )
    round_vector = lambda vector: tuple(  # noqa: E731
        _outward_round_interval(entry, rounding_denominator)
        for entry in vector
    )
    return ValidatedConormalStrongCell(
        radius=profile.radius,
        coordinate=round_matrix(_jet_matrix_value(coordinate_jets)),  # type: ignore[arg-type]
        mixed=round_matrix(_jet_matrix_value(mixed_jets)),  # type: ignore[arg-type]
        principal=round_matrix(_jet_matrix_value(principal_jets)),  # type: ignore[arg-type]
        mixed_derivative=round_matrix(_jet_matrix_derivative(mixed_jets)),  # type: ignore[arg-type]
        principal_derivative=round_matrix(
            _jet_matrix_derivative(principal_jets)
        ),  # type: ignore[arg-type]
        strong_source=round_vector(strong_source),  # type: ignore[arg-type]
    )


def _matrix_vector(
    matrix: IntervalMatrix2, vector: IntervalVector2
) -> IntervalVector2:
    return tuple(
        row[0] * vector[0] + row[1] * vector[1] for row in matrix
    )  # type: ignore[return-value]


def _matrix_subtract(left: IntervalMatrix2, right: IntervalMatrix2) -> IntervalMatrix2:
    return tuple(
        tuple(
            left[row][column] - right[row][column] for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _transpose(matrix: IntervalMatrix2) -> IntervalMatrix2:
    return tuple(
        tuple(matrix[column][row] for column in range(2)) for row in range(2)
    )  # type: ignore[return-value]


@dataclass(frozen=True)
class ValidatedStrongResidualCell:
    radius: RationalInterval
    residual: IntervalVector2
    l2_squared_upper: Fraction


def validated_strong_residual_cell(
    coefficients: ValidatedConormalStrongCell,
    trial: RationalC1TrialCell,
    *,
    additional_strong_load: IntervalVector2 | None = None,
) -> ValidatedStrongResidualCell:
    """Range ``load-A y`` and integrate a rigorous cellwise square bound."""
    if coefficients.radius != trial.radius:
        raise ValueError("coefficient and trial cells must have the same radius")
    value, derivative, second_derivative = trial.jet_range()
    mixed_transpose = _transpose(coefficients.mixed)
    mixed_derivative_transpose = _transpose(coefficients.mixed_derivative)
    coordinate_part = _matrix_subtract(
        coefficients.coordinate, mixed_derivative_transpose
    )
    derivative_part = _matrix_subtract(
        _matrix_subtract(coefficients.mixed, mixed_transpose),
        coefficients.principal_derivative,
    )
    operator = tuple(
        coordinate_value + derivative_value - principal_value
        for coordinate_value, derivative_value, principal_value in zip(
            _matrix_vector(coordinate_part, value),
            _matrix_vector(derivative_part, derivative),
            _matrix_vector(coefficients.principal, second_derivative),
            strict=True,
        )
    )
    load = coefficients.strong_source
    if additional_strong_load is not None:
        load = tuple(
            left + right
            for left, right in zip(load, additional_strong_load, strict=True)
        )  # type: ignore[assignment]
    residual = tuple(
        load_value - operator_value
        for load_value, operator_value in zip(load, operator, strict=True)
    )
    square_upper = coefficients.radius.width * sum(
        _absolute_upper(entry) ** 2 for entry in residual
    )
    return ValidatedStrongResidualCell(
        radius=coefficients.radius,
        residual=residual,  # type: ignore[arg-type]
        l2_squared_upper=square_upper,
    )


@dataclass(frozen=True)
class ValidatedResidualNorm:
    l2_squared_upper: Fraction
    l2_norm_upper: Fraction
    wall_residual_absolute_upper: Fraction
    bulk_energy_dual_upper: Fraction
    wall_energy_dual_upper: Fraction
    energy_dual_upper: Fraction


def certify_energy_dual_residual_upper(
    cells: tuple[ValidatedStrongResidualCell, ...],
    *,
    residual_domain: RationalInterval,
    interface_distribution_free: bool,
    operator_lower_bound: Fraction,
    wall_trace_margin_lower_bound: Fraction,
    wall_residual: RationalInterval = RationalInterval.point(0),
    sqrt_bisection_steps: int = 160,
) -> ValidatedResidualNorm:
    """Lift bulk ``L2`` and wall conormal residuals to an energy-dual bound."""
    if not cells:
        raise ValueError("at least one residual cell is required")
    if (
        cells[0].radius.lower != residual_domain.lower
        or cells[-1].radius.upper != residual_domain.upper
    ):
        raise ValueError("residual cells do not cover the declared domain")
    if not interface_distribution_free:
        raise ValueError("internal conormal distributions must be excluded")
    if operator_lower_bound <= 0 or wall_trace_margin_lower_bound <= 0:
        raise ValueError("coercivity and wall trace margin must be positive")
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("residual cells are not contiguous")
    l2_squared = sum(
        (cell.l2_squared_upper for cell in cells), start=Fraction(0)
    )
    l2_norm = sqrt_fraction_interval(
        l2_squared, bisection_steps=sqrt_bisection_steps
    ).upper
    bulk_dual = sqrt_fraction_interval(
        l2_squared / operator_lower_bound,
        bisection_steps=sqrt_bisection_steps,
    ).upper
    wall_absolute = _absolute_upper(wall_residual)
    wall_dual = sqrt_fraction_interval(
        wall_absolute**2 / wall_trace_margin_lower_bound,
        bisection_steps=sqrt_bisection_steps,
    ).upper
    return ValidatedResidualNorm(
        l2_squared_upper=l2_squared,
        l2_norm_upper=l2_norm,
        wall_residual_absolute_upper=wall_absolute,
        bulk_energy_dual_upper=bulk_dual,
        wall_energy_dual_upper=wall_dual,
        energy_dual_upper=bulk_dual + wall_dual,
    )


def wall_conormal_residual(
    *,
    coefficients: ValidatedConormalStrongCell,
    trial: RationalC1TrialCell,
    wall_form_coefficient: RationalInterval,
    wall_load: RationalInterval = RationalInterval.point(0),
) -> RationalInterval:
    """Enclose the free radial-field wall residual ``p_f+k f-load``."""
    if coefficients.radius != trial.radius:
        raise ValueError("coefficient and trial cells must have the same radius")
    values, derivatives = trial.endpoint_jet(right=True)
    value = tuple(RationalInterval.point(entry) for entry in values)
    derivative = tuple(RationalInterval.point(entry) for entry in derivatives)
    conormal = tuple(
        left + right
        for left, right in zip(
            _matrix_vector(_transpose(coefficients.mixed), value),
            _matrix_vector(coefficients.principal, derivative),
            strict=True,
        )
    )
    return conormal[0] + wall_form_coefficient.scale(values[0]) - wall_load
