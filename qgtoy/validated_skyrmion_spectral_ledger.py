"""Directed endpoint and tail ledgers for the Skyrmion spectrum.

This module implements the narrow algebraic part of AU.2.  It converts a
validated wall-slope enclosure and a validated inertia enclosure into directed
intervals for the optical endpoint data used by the continuum tail theorem.
If six independently certified third-derivative ``L1`` upper bounds are
supplied, it also evaluates the exact tail formulas from
``static_patch_skyrmion_tail`` in rational interval arithmetic.

The module does not construct those six derivative bounds and does not perform
the AU.3 finite-frequency quadrature for ``Q0``, ``Q1``, ``Q2``, ``G``, or
``M1``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction

from .validated_interval import (
    RationalInterval,
    atanh_fraction_interval,
    pi_machin_interval,
    sqrt_fraction_interval,
)


def _fraction(name: str, value: int | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def _positive_fraction(name: str, value: int | Fraction) -> Fraction:
    result = _fraction(name, value)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _provenance(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value.strip()


def _interval_record(value: RationalInterval) -> dict[str, str]:
    return {
        "lower": str(value.lower),
        "upper": str(value.upper),
        "width": str(value.width),
    }


@dataclass(frozen=True)
class ValidatedSkyrmionSpectralInput:
    """One directed input interval together with its proof provenance."""

    enclosure: RationalInterval
    provenance: str
    certificate_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.enclosure, RationalInterval):
            raise TypeError("enclosure must be a RationalInterval")
        object.__setattr__(
            self,
            "provenance",
            _provenance("provenance", self.provenance),
        )
        object.__setattr__(
            self,
            "certificate_id",
            _provenance("certificate_id", self.certificate_id),
        )


@dataclass(frozen=True)
class ValidatedSkyrmionDerivativeNormUpperBound:
    """An externally established nonnegative ``L1``-norm upper bound."""

    upper_bound: Fraction
    provenance: str
    certificate_id: str

    def __post_init__(self) -> None:
        upper = _fraction("upper_bound", self.upper_bound)
        if upper < 0:
            raise ValueError("upper_bound must be nonnegative")
        object.__setattr__(self, "upper_bound", upper)
        object.__setattr__(
            self,
            "provenance",
            _provenance("provenance", self.provenance),
        )
        object.__setattr__(
            self,
            "certificate_id",
            _provenance("certificate_id", self.certificate_id),
        )

    @property
    def enclosure(self) -> RationalInterval:
        return RationalInterval(Fraction(0), self.upper_bound)


@dataclass(frozen=True)
class ValidatedSkyrmionSpectralEndpointLedger:
    """Directed optical endpoint data derived from AU.1 observables."""

    curvature: Fraction
    wall_radius: Fraction
    inertia: ValidatedSkyrmionSpectralInput
    wall_slope: ValidatedSkyrmionSpectralInput
    root_curvature: RationalInterval
    radial_horizon_ratio: RationalInterval
    horizon_margin: RationalInterval
    optical_wall: RationalInterval
    wall_slope_magnitude: RationalInterval
    form_factor_prefactor: RationalInterval
    wall_weight_second_derivative: RationalInterval
    wall_a_second_derivative: RationalInterval
    leading_form_factor_tail_amplitude: RationalInterval
    conclusion_scope: str
    certificate_id: str
    newton_radius: Fraction | None = None
    omega: Fraction | None = None
    origin_cutoff: Fraction | None = None


@dataclass(frozen=True)
class ValidatedSkyrmionTailEnvelope:
    """Rational interval evaluation of equations (6)-(10) of the tail note."""

    tail_start: Fraction
    physical_radius: ValidatedSkyrmionSpectralInput
    physical_tail_start: Fraction
    b_transform_bounds: tuple[RationalInterval, RationalInterval, RationalInterval]
    d_transform_bounds: tuple[RationalInterval, RationalInterval, RationalInterval]
    numerator_derivative_coefficients: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]
    form_factor_derivative_coefficients: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]
    positive_signed_factor_coefficients: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]
    negative_signed_factor_coefficients: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]
    squared_dimensionless_h2_tail_bounds: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]
    squared_physical_h2_tail_bounds: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]


@dataclass(frozen=True)
class ValidatedSkyrmionSpectralLedger:
    """Machine-readable AU.2 endpoint/tail status without an AU.3 claim."""

    endpoint: ValidatedSkyrmionSpectralEndpointLedger
    a_third_derivative_l1: tuple[
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
    ]
    w_third_derivative_l1: tuple[
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
    ]
    tail_envelope: ValidatedSkyrmionTailEnvelope | None
    supplied_derivative_norm_count: int
    missing_derivative_norms: tuple[str, ...]
    au2_status: str
    au3_status: str
    claim_boundary: str

    def to_record(self) -> dict[str, object]:
        """Serialize the ledger without converting exact endpoints to floats."""

        endpoint = self.endpoint
        derivative_bounds = {}
        for family_name, family in (
            ("A", self.a_third_derivative_l1),
            ("W", self.w_third_derivative_l1),
        ):
            for order, bound in enumerate(family):
                key = f"M_{order}^{family_name}"
                derivative_bounds[key] = (
                    None
                    if bound is None
                    else {
                        "upper_bound": str(bound.upper_bound),
                        "provenance": bound.provenance,
                        "certificate_id": bound.certificate_id,
                    }
                )
        tail_record = None
        if self.tail_envelope is not None:
            tail = self.tail_envelope
            tail_record = {
                "tail_start": str(tail.tail_start),
                "physical_radius": _interval_record(
                    tail.physical_radius.enclosure
                ),
                "physical_radius_provenance": tail.physical_radius.provenance,
                "physical_tail_start": str(tail.physical_tail_start),
                "b_transform_bounds": tuple(
                    _interval_record(value) for value in tail.b_transform_bounds
                ),
                "d_transform_bounds": tuple(
                    _interval_record(value) for value in tail.d_transform_bounds
                ),
                "numerator_derivative_coefficients": tuple(
                    _interval_record(value)
                    for value in tail.numerator_derivative_coefficients
                ),
                "form_factor_derivative_coefficients": tuple(
                    _interval_record(value)
                    for value in tail.form_factor_derivative_coefficients
                ),
                "positive_signed_factor_coefficients": tuple(
                    _interval_record(value)
                    for value in tail.positive_signed_factor_coefficients
                ),
                "negative_signed_factor_coefficients": tuple(
                    _interval_record(value)
                    for value in tail.negative_signed_factor_coefficients
                ),
                "squared_dimensionless_h2_tail_bounds": tuple(
                    _interval_record(value)
                    for value in tail.squared_dimensionless_h2_tail_bounds
                ),
                "squared_physical_h2_tail_bounds": tuple(
                    _interval_record(value)
                    for value in tail.squared_physical_h2_tail_bounds
                ),
            }
        return {
            "goal": "Validated Skyrmion Spectral Ledger AU.2a",
            "result_type": "directed_endpoint_and_conditional_tail_ledger",
            "au2_status": self.au2_status,
            "au3_status": self.au3_status,
            "endpoint": {
                "curvature": str(endpoint.curvature),
                "wall_radius": str(endpoint.wall_radius),
                "inertia": _interval_record(endpoint.inertia.enclosure),
                "inertia_provenance": endpoint.inertia.provenance,
                "certificate_id": endpoint.certificate_id,
                "wall_slope": _interval_record(endpoint.wall_slope.enclosure),
                "wall_slope_provenance": endpoint.wall_slope.provenance,
                "root_curvature": _interval_record(endpoint.root_curvature),
                "radial_horizon_ratio": _interval_record(
                    endpoint.radial_horizon_ratio
                ),
                "horizon_margin": _interval_record(endpoint.horizon_margin),
                "optical_wall": _interval_record(endpoint.optical_wall),
                "wall_slope_magnitude": _interval_record(
                    endpoint.wall_slope_magnitude
                ),
                "form_factor_prefactor": _interval_record(
                    endpoint.form_factor_prefactor
                ),
                "wall_weight_second_derivative": _interval_record(
                    endpoint.wall_weight_second_derivative
                ),
                "wall_a_second_derivative": _interval_record(
                    endpoint.wall_a_second_derivative
                ),
                "leading_form_factor_tail_amplitude": _interval_record(
                    endpoint.leading_form_factor_tail_amplitude
                ),
                "conclusion_scope": endpoint.conclusion_scope,
                "newton_radius": (
                    None
                    if endpoint.newton_radius is None
                    else str(endpoint.newton_radius)
                ),
                "omega": None if endpoint.omega is None else str(endpoint.omega),
                "origin_cutoff": (
                    None
                    if endpoint.origin_cutoff is None
                    else str(endpoint.origin_cutoff)
                ),
            },
            "derivative_norm_bounds": derivative_bounds,
            "supplied_derivative_norm_count": self.supplied_derivative_norm_count,
            "missing_derivative_norms": self.missing_derivative_norms,
            "tail_envelope": tail_record,
            "claim_boundary": self.claim_boundary,
        }


def validate_skyrmion_spectral_endpoint_ledger(
    *,
    curvature: int | Fraction,
    wall_radius: int | Fraction,
    inertia: ValidatedSkyrmionSpectralInput,
    wall_slope: ValidatedSkyrmionSpectralInput,
    atanh_terms: int = 80,
    pi_terms: int = 80,
    sqrt_bisection_steps: int = 160,
) -> ValidatedSkyrmionSpectralEndpointLedger:
    """Derive the directed endpoint constants in the continuum tail theorem."""

    curvature_value = _positive_fraction("curvature", curvature)
    wall_radius_value = _positive_fraction("wall_radius", wall_radius)
    if not isinstance(inertia, ValidatedSkyrmionSpectralInput):
        raise TypeError("inertia must be a ValidatedSkyrmionSpectralInput")
    if not isinstance(wall_slope, ValidatedSkyrmionSpectralInput):
        raise TypeError("wall_slope must be a ValidatedSkyrmionSpectralInput")
    atanh_count = _positive_integer("atanh_terms", atanh_terms)
    pi_count = _positive_integer("pi_terms", pi_terms)
    sqrt_count = _positive_integer("sqrt_bisection_steps", sqrt_bisection_steps)
    if inertia.enclosure.lower <= 0:
        raise ValueError("inertia enclosure must be strictly positive")
    if wall_slope.enclosure.upper >= 0:
        raise ValueError("wall-slope enclosure must be strictly negative")
    if inertia.certificate_id != wall_slope.certificate_id:
        raise ValueError("inertia and wall slope must share one certificate id")

    root_curvature = sqrt_fraction_interval(
        curvature_value,
        bisection_steps=sqrt_count,
    )
    horizon_ratio = root_curvature.scale(wall_radius_value)
    if horizon_ratio.lower <= 0 or horizon_ratio.upper >= 1:
        raise ValueError("wall must lie strictly inside the positive horizon")
    horizon_margin = RationalInterval.point(1) - RationalInterval.point(
        curvature_value * wall_radius_value**2
    )
    if horizon_margin.lower <= 0:
        raise ValueError("wall must have strictly positive horizon margin")
    optical_wall = RationalInterval(
        atanh_fraction_interval(
            horizon_ratio.lower,
            terms=atanh_count,
        ).lower,
        atanh_fraction_interval(
            horizon_ratio.upper,
            terms=atanh_count,
        ).upper,
    )
    slope_magnitude = -wall_slope.enclosure
    slope_squared = slope_magnitude.power(2)
    pi_interval = pi_machin_interval(terms=pi_count)
    lambda_three_halves = RationalInterval.point(curvature_value) * root_curvature
    wall_weight_second = (
        pi_interval.scale(4)
        * slope_squared
        * horizon_margin.power(2)
        * (RationalInterval.point(1) + (horizon_margin * slope_squared).scale(4))
        / lambda_three_halves.scale(3)
    )
    prefactor = RationalInterval.point(3) / (
        inertia.enclosure.scale(curvature_value)
    )
    wall_a_second = wall_weight_second / horizon_ratio
    leading_amplitude = prefactor * wall_weight_second
    return ValidatedSkyrmionSpectralEndpointLedger(
        curvature=curvature_value,
        wall_radius=wall_radius_value,
        inertia=inertia,
        wall_slope=wall_slope,
        root_curvature=root_curvature,
        radial_horizon_ratio=horizon_ratio,
        horizon_margin=horizon_margin,
        optical_wall=optical_wall,
        wall_slope_magnitude=slope_magnitude,
        form_factor_prefactor=prefactor,
        wall_weight_second_derivative=wall_weight_second,
        wall_a_second_derivative=wall_a_second,
        leading_form_factor_tail_amplitude=leading_amplitude,
        conclusion_scope=(
            "directed endpoint, prefactor, and wall-second-jet constants for "
            "the exact hard-wall continuum tail theorem"
        ),
        certificate_id=inertia.certificate_id,
    )


def validate_skyrmion_tail_endpoint_data(
    physical_observables: object,
    *,
    atanh_terms: int = 80,
    pi_terms: int = 80,
    sqrt_bisection_steps: int = 160,
) -> ValidatedSkyrmionSpectralEndpointLedger:
    """Adapt one fully certified AU.1 result into the AU.2 endpoint ledger."""

    from .validated_skyrmion_bvp import (
        ValidatedSkyrmionNewtonPhysicalObservables,
    )

    if not isinstance(
        physical_observables,
        ValidatedSkyrmionNewtonPhysicalObservables,
    ):
        raise TypeError(
            "physical_observables must be validated Newton observables"
        )
    if not (
        physical_observables.strict_monotonicity_verified
        and physical_observables.negative_wall_slope_verified
        and physical_observables.positive_finite_inertia_verified
    ):
        raise ValueError("AU.2 endpoint data require all AU.1 physical checks")
    tube = physical_observables.newton_tube
    if not (tube.self_map_verified and tube.contraction_verified):
        raise ValueError("AU.2 endpoint data require a closed Newton tube")
    if physical_observables.wall_slope_enclosure != (
        tube.cells[-1].tube_jet.derivative
    ):
        raise ValueError("physical wall slope does not match the Newton tube")
    positive_radius_inertia = RationalInterval.point(0)
    for cell in physical_observables.inertia_cells:
        positive_radius_inertia += cell.integral_enclosure
    expected_inertia = RationalInterval(
        positive_radius_inertia.lower,
        positive_radius_inertia.upper
        + physical_observables.origin_inertia_upper_bound,
    )
    if physical_observables.inertia_enclosure != expected_inertia:
        raise ValueError("physical inertia does not match its certified cells")
    certificate_id = (
        f"au1:{tube.curvature}:{tube.wall_radius}:{tube.origin_cutoff}:"
        f"{tube.radius}:{tube.omega}:"
        f"{physical_observables.wall_slope_enclosure.lower}:"
        f"{physical_observables.wall_slope_enclosure.upper}:"
        f"{physical_observables.inertia_enclosure.lower}:"
        f"{physical_observables.inertia_enclosure.upper}"
    )
    endpoint = validate_skyrmion_spectral_endpoint_ledger(
        curvature=tube.curvature,
        wall_radius=tube.wall_radius,
        inertia=ValidatedSkyrmionSpectralInput(
            physical_observables.inertia_enclosure,
            physical_observables.conclusion_scope,
            certificate_id,
        ),
        wall_slope=ValidatedSkyrmionSpectralInput(
            physical_observables.wall_slope_enclosure,
            physical_observables.conclusion_scope,
            certificate_id,
        ),
        atanh_terms=atanh_terms,
        pi_terms=pi_terms,
        sqrt_bisection_steps=sqrt_bisection_steps,
    )
    return replace(
        endpoint,
        newton_radius=tube.radius,
        omega=tube.omega,
        origin_cutoff=tube.origin_cutoff,
        conclusion_scope=(
            "directed AU.2 endpoint constants inherited from one closed "
            "Newton tube with certified monotonicity, negative wall slope, "
            "and positive finite inertia"
        ),
    )


def _validate_norm_family(
    name: str,
    values: tuple[
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
    ],
) -> tuple[
    ValidatedSkyrmionDerivativeNormUpperBound | None,
    ValidatedSkyrmionDerivativeNormUpperBound | None,
    ValidatedSkyrmionDerivativeNormUpperBound | None,
]:
    if not isinstance(values, tuple) or len(values) != 3:
        raise ValueError(f"{name} must be a three-entry tuple")
    for value in values:
        if value is not None and not isinstance(
            value,
            ValidatedSkyrmionDerivativeNormUpperBound,
        ):
            raise TypeError(
                f"{name} entries must be derivative-norm bounds or None"
            )
    return values


def _evaluate_tail_envelope(
    endpoint: ValidatedSkyrmionSpectralEndpointLedger,
    *,
    a_norms: tuple[
        ValidatedSkyrmionDerivativeNormUpperBound,
        ValidatedSkyrmionDerivativeNormUpperBound,
        ValidatedSkyrmionDerivativeNormUpperBound,
    ],
    w_norms: tuple[
        ValidatedSkyrmionDerivativeNormUpperBound,
        ValidatedSkyrmionDerivativeNormUpperBound,
        ValidatedSkyrmionDerivativeNormUpperBound,
    ],
    tail_start: Fraction,
    physical_radius: ValidatedSkyrmionSpectralInput,
    pi_terms: int,
) -> ValidatedSkyrmionTailEnvelope:
    split = RationalInterval.point(tail_start)
    wall = endpoint.optical_wall
    wall_second = endpoint.wall_weight_second_derivative
    wall_a_second = endpoint.wall_a_second_derivative
    b_bounds = tuple(
        wall.power(order) * wall_second + w_norms[order].enclosure
        for order in range(3)
    )
    d_bounds = tuple(
        wall.power(order) * wall_a_second + a_norms[order].enclosure
        for order in range(3)
    )
    numerator = (
        b_bounds[0] + d_bounds[0] / split,
        b_bounds[1] + d_bounds[1] / split + d_bounds[0] / split.power(2),
        b_bounds[2]
        + d_bounds[2] / split
        + d_bounds[1].scale(2) / split.power(2)
        + d_bounds[0].scale(2) / split.power(3),
    )
    prefactor = endpoint.form_factor_prefactor
    form_factor = (
        prefactor * numerator[0],
        prefactor * (numerator[1] + numerator[0].scale(2) / split),
        prefactor
        * (
            numerator[2]
            + numerator[1].scale(4) / split
            + numerator[0].scale(6) / split.power(2)
        ),
    )
    bare = (Fraction(1, 6), Fraction(81, 480), Fraction(21, 48))
    positive = (
        form_factor[0].scale(bare[0]),
        form_factor[0].scale(bare[1]) + form_factor[1].scale(bare[0]),
        form_factor[0].scale(bare[2])
        + form_factor[1].scale(2 * bare[1])
        + form_factor[2].scale(bare[0]),
    )
    pi_interval = pi_machin_interval(terms=pi_terms)
    negative = (
        positive[0],
        pi_interval * positive[0] + positive[1],
        positive[2]
        + (pi_interval * positive[1]).scale(2)
        + pi_interval.power(2) * positive[0],
    )
    dimensionless_formula = tuple(
        (positive[order].power(2) + negative[order].power(2))
        / split.power(6).scale(6)
        for order in range(3)
    )
    dimensionless = tuple(
        RationalInterval(Fraction(0), value.upper)
        for value in dimensionless_formula
    )
    radius = physical_radius.enclosure.lower
    physical = tuple(
        dimensionless[order].scale(radius ** (2 * order - 4))
        for order in range(3)
    )
    return ValidatedSkyrmionTailEnvelope(
        tail_start=tail_start,
        physical_radius=physical_radius,
        physical_tail_start=tail_start / radius,
        b_transform_bounds=b_bounds,
        d_transform_bounds=d_bounds,
        numerator_derivative_coefficients=numerator,
        form_factor_derivative_coefficients=form_factor,
        positive_signed_factor_coefficients=positive,
        negative_signed_factor_coefficients=negative,
        squared_dimensionless_h2_tail_bounds=dimensionless,
        squared_physical_h2_tail_bounds=physical,
    )


def build_validated_skyrmion_spectral_ledger(
    endpoint: ValidatedSkyrmionSpectralEndpointLedger,
    *,
    a_third_derivative_l1: tuple[
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
    ] = (None, None, None),
    w_third_derivative_l1: tuple[
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
        ValidatedSkyrmionDerivativeNormUpperBound | None,
    ] = (None, None, None),
    tail_start: int | Fraction = 1,
    physical_radius: ValidatedSkyrmionSpectralInput | None = None,
    pi_terms: int = 80,
) -> ValidatedSkyrmionSpectralLedger:
    """Build the endpoint ledger and conditionally evaluate the AU.2 tail."""

    if not isinstance(endpoint, ValidatedSkyrmionSpectralEndpointLedger):
        raise TypeError(
            "endpoint must be a ValidatedSkyrmionSpectralEndpointLedger"
        )
    a_norms = _validate_norm_family(
        "a_third_derivative_l1",
        a_third_derivative_l1,
    )
    w_norms = _validate_norm_family(
        "w_third_derivative_l1",
        w_third_derivative_l1,
    )
    split = _positive_fraction("tail_start", tail_start)
    if split < 1:
        raise ValueError("tail_start must be at least one")
    radius_input = (
        ValidatedSkyrmionSpectralInput(
            RationalInterval.point(1),
            "dimensionless normalization only",
            endpoint.certificate_id,
        )
        if physical_radius is None
        else physical_radius
    )
    if not isinstance(radius_input, ValidatedSkyrmionSpectralInput):
        raise TypeError("physical_radius must be a validated spectral input")
    if radius_input.enclosure.lower <= 0:
        raise ValueError("physical radius must be positive")
    if radius_input.enclosure.width != 0:
        raise ValueError("physical radius must currently be a point interval")
    pi_count = _positive_integer("pi_terms", pi_terms)
    named_norms = tuple(
        (f"M_{order}^A", a_norms[order]) for order in range(3)
    ) + tuple((f"M_{order}^W", w_norms[order]) for order in range(3))
    missing = tuple(name for name, value in named_norms if value is None)
    for name, value in named_norms:
        if value is not None and value.certificate_id != endpoint.certificate_id:
            raise ValueError(f"{name} does not match the endpoint certificate")
    supplied = 6 - len(missing)
    tail = None
    if not missing:
        tail = _evaluate_tail_envelope(
            endpoint,
            a_norms=(a_norms[0], a_norms[1], a_norms[2]),
            w_norms=(w_norms[0], w_norms[1], w_norms[2]),
            tail_start=split,
            physical_radius=radius_input,
            pi_terms=pi_count,
        )
    return ValidatedSkyrmionSpectralLedger(
        endpoint=endpoint,
        a_third_derivative_l1=a_norms,
        w_third_derivative_l1=w_norms,
        tail_envelope=tail,
        supplied_derivative_norm_count=supplied,
        missing_derivative_norms=missing,
        au2_status=(
            "conditional_tail_formula_evaluated_from_supplied_bounds"
            if tail is not None
            else "open_external_derivative_norm_certificates_required"
        ),
        au3_status="open_finite_frequency_quadrature",
        claim_boundary=(
            "This module certifies the algebraic propagation of validated "
            "AU.1 endpoint inputs and, conditionally, six externally proved "
            "third-derivative L1 bounds through the exact continuum tail "
            "formula. It does not establish any of those six L1 bounds and "
            "does not certify global Q0, Q1, Q2, G, or M1."
        ),
    )
