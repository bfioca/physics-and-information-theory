"""Trusted interval checks for the hard-wall Skyrmion profile.

This module deliberately keeps the positive-radius results conditional.  It
evaluates the nonlinear curved-profile vector field on exact rational boxes
and verifies both Picard steps and normalized-polynomial Taylor tracks.  A
checked track proves that every exact solution entering through its supplied
initial box exists uniquely across all cells, remains in the declared tubes,
and ends in the returned exact-rational box.  An unconditional AU.1 shooting
result still requires a uniform regular-origin slope family to enter the first
track box.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    cos_center_lipschitz_interval,
    sin_center_lipschitz_interval,
    sin_interval,
)


def _positive_fraction(name: str, value: Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    fraction = Fraction(value)
    if fraction <= 0:
        raise ValueError(f"{name} must be positive")
    return fraction


def _nonnegative_fraction(name: str, value: Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    fraction = Fraction(value)
    if fraction < 0:
        raise ValueError(f"{name} must be nonnegative")
    return fraction


@dataclass(frozen=True)
class SkyrmionStateBox:
    """Interval enclosure of ``(F,F')`` at one radius or across a tube."""

    profile: RationalInterval
    derivative: RationalInterval


@dataclass(frozen=True)
class ValidatedPicardStep:
    """Result of one conditional positive-radius Picard enclosure."""

    radius_start: Fraction
    radius_end: Fraction
    initial: SkyrmionStateBox
    tube: SkyrmionStateBox
    endpoint: SkyrmionStateBox
    profile_picard_image: RationalInterval
    derivative_picard_image: RationalInterval
    acceleration_box: RationalInterval


@dataclass(frozen=True)
class SkyrmionTaylorCell:
    """Untrusted normalized-polynomial data for one positive-radius cell."""

    radius_start: Fraction
    step: Fraction
    profile_polynomial: RationalPolynomial
    profile_radius: Fraction
    derivative_radius: Fraction


@dataclass(frozen=True)
class SkyrmionAccelerationJacobianBox:
    """Trusted interval enclosure of ``Phi`` and its state derivatives."""

    acceleration: RationalInterval
    profile_derivative: RationalInterval
    derivative_derivative: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionTaylorCell:
    """A checked conditional Taylor enclosure on one normalized cell."""

    radius_start: Fraction
    radius_end: Fraction
    initial: SkyrmionStateBox
    profile_polynomial: RationalPolynomial
    profile_radius: Fraction
    derivative_radius: Fraction
    center_tube: SkyrmionStateBox
    solution_tube: SkyrmionStateBox
    endpoint: SkyrmionStateBox
    defect_box: RationalInterval
    acceleration_box: RationalInterval
    profile_jacobian_box: RationalInterval
    derivative_jacobian_box: RationalInterval
    profile_self_map_bound: Fraction
    derivative_self_map_bound: Fraction
    contraction_bound: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionTaylorTrack:
    """A sequence of cells chained through checker-computed endpoint boxes."""

    initial: SkyrmionStateBox
    cells: tuple[ValidatedSkyrmionTaylorCell, ...]
    endpoint: SkyrmionStateBox


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _expand_interval(
    value: RationalInterval,
    radius: Fraction,
) -> RationalInterval:
    return value + RationalInterval(-radius, radius)


def _weighted_row_bound(numerator: Fraction, radius: Fraction) -> Fraction:
    if radius == 0:
        if numerator != 0:
            raise ValueError("a zero Taylor radius has a nonzero Lipschitz image")
        return Fraction(0)
    return numerator / radius


def skyrmion_origin_cubic_coefficient_interval(
    shooting_slope: RationalInterval,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
) -> RationalInterval:
    """Enclose the exact cubic coefficient ``c(b)`` algebraically.

    This evaluates the coefficient in ``F=pi-bx+c(b)x^3+O(x^5)``.  It does not
    enclose the ``O(x^5)`` remainder.
    """
    if not isinstance(shooting_slope, RationalInterval):
        raise TypeError("shooting_slope must be a RationalInterval")
    if shooting_slope.lower <= 0:
        raise ValueError("shooting_slope must be strictly positive")
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)
    slope_squared = shooting_slope.power(2)
    bracket = (
        RationalInterval.point(mass_squared - 4 * curvature_value)
        + slope_squared.scale(Fraction(4, 3) - 24 * curvature_value)
        + slope_squared.power(2).scale(Fraction(8, 3))
    )
    denominator = RationalInterval.point(10) * (
        RationalInterval.point(1) + slope_squared.scale(8)
    )
    return shooting_slope * bracket / denominator


def curved_skyrmion_acceleration_box(
    radius: RationalInterval,
    profile: RationalInterval,
    derivative: RationalInterval,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> RationalInterval:
    """Enclose ``F''`` on a positive-radius state box."""
    if not all(
        isinstance(value, RationalInterval)
        for value in (radius, profile, derivative)
    ):
        raise TypeError("radius, profile, and derivative must be intervals")
    if radius.lower <= 0:
        raise ValueError("radius interval must be strictly positive")
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)
    radius_squared = radius.power(2)
    lapse = RationalInterval.point(1) - radius_squared.scale(curvature_value)
    if lapse.lower <= 0:
        raise ValueError("radius tube must lie strictly inside the horizon")
    lapse_derivative = radius.scale(-2 * curvature_value)
    sine = sin_interval(profile, terms=trigonometric_terms)
    sine_twice = sin_interval(profile.scale(2), terms=trigonometric_terms)
    sine_squared = sine.power(2)
    u = radius_squared + sine_squared.scale(8)
    if u.lower <= 0:
        raise ValueError("profile denominator must be strictly positive")
    first = (
        RationalInterval.point(1)
        + sine_squared.scale(4) / radius_squared
    ) * sine_twice
    mass = sine * radius_squared.scale(mass_squared)
    drift = (
        lapse_derivative * u + lapse * radius.scale(2)
    ) * derivative
    nonlinear = (
        lapse
        * sine_twice
        * derivative.power(2)
    ).scale(4)
    return (first + mass - drift - nonlinear) / (lapse * u)


def curved_skyrmion_acceleration_jacobian_box(
    radius: RationalInterval,
    profile: RationalInterval,
    derivative: RationalInterval,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> SkyrmionAccelerationJacobianBox:
    """Enclose ``Phi``, ``partial_F Phi``, and ``partial_G Phi``.

    The formulas are differentiated from the rational-trigonometric vector
    field inside this trusted routine.  No defect or derivative bound supplied
    by a Taylor certificate is accepted.
    """
    if not all(
        isinstance(value, RationalInterval)
        for value in (radius, profile, derivative)
    ):
        raise TypeError("radius, profile, and derivative must be intervals")
    if radius.lower <= 0:
        raise ValueError("radius interval must be strictly positive")
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)
    radius_squared = radius.power(2)
    lapse = RationalInterval.point(1) - radius_squared.scale(curvature_value)
    if lapse.lower <= 0:
        raise ValueError("radius tube must lie strictly inside the horizon")
    lapse_derivative = radius.scale(-2 * curvature_value)
    sine = sin_center_lipschitz_interval(
        profile, terms=trigonometric_terms
    )
    cosine = cos_center_lipschitz_interval(
        profile, terms=trigonometric_terms
    )
    sine_twice = sin_center_lipschitz_interval(
        profile.scale(2), terms=trigonometric_terms
    )
    cosine_twice = cos_center_lipschitz_interval(
        profile.scale(2), terms=trigonometric_terms
    )
    sine_squared = sine.power(2)
    u = radius_squared + sine_squared.scale(8)
    if u.lower <= 0:
        raise ValueError("profile denominator must be strictly positive")
    u_profile = sine_twice.scale(8)
    first_factor = (
        RationalInterval.point(1)
        + sine_squared.scale(4) / radius_squared
    )
    first = first_factor * sine_twice
    first_profile = (
        sine_twice.scale(4) / radius_squared
    ) * sine_twice + first_factor * cosine_twice.scale(2)
    mass = sine * radius_squared.scale(mass_squared)
    mass_profile = cosine * radius_squared.scale(mass_squared)
    drift_factor = lapse_derivative * u + lapse * radius.scale(2)
    drift = drift_factor * derivative
    drift_profile = lapse_derivative * u_profile * derivative
    nonlinear = (
        lapse * sine_twice * derivative.power(2)
    ).scale(4)
    nonlinear_profile = (
        lapse * cosine_twice * derivative.power(2)
    ).scale(8)
    numerator = first + mass - drift - nonlinear
    numerator_profile = (
        first_profile + mass_profile - drift_profile - nonlinear_profile
    )
    denominator = lapse * u
    denominator_profile = lapse * u_profile
    acceleration = numerator / denominator
    profile_jacobian = (
        numerator_profile * denominator
        - numerator * denominator_profile
    ) / denominator.power(2)
    derivative_jacobian = (
        -drift_factor
        - (lapse * sine_twice * derivative).scale(8)
    ) / denominator
    return SkyrmionAccelerationJacobianBox(
        acceleration=acceleration,
        profile_derivative=profile_jacobian,
        derivative_derivative=derivative_jacobian,
    )


def validate_skyrmion_taylor_cell(
    initial: SkyrmionStateBox,
    cell: SkyrmionTaylorCell,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> ValidatedSkyrmionTaylorCell:
    """Validate one normalized-polynomial conditional Taylor cell.

    With ``x=a+h*s``, the certificate center is ``F=P(s)`` and
    ``G=P_s(s)/h``.  The checker recomputes the acceleration defect on the
    center track and the state Jacobian on the full correction tube.  A
    componentwise radii inequality and a weighted sup-norm contraction then
    prove a unique solution in that tube for every state in ``initial``.
    """
    if not isinstance(initial, SkyrmionStateBox):
        raise TypeError("initial must be a SkyrmionStateBox")
    if not isinstance(initial.profile, RationalInterval) or not isinstance(
        initial.derivative, RationalInterval
    ):
        raise TypeError("initial state components must be RationalInterval values")
    if not isinstance(cell, SkyrmionTaylorCell):
        raise TypeError("cell must be a SkyrmionTaylorCell")
    if not isinstance(cell.profile_polynomial, RationalPolynomial):
        raise TypeError("profile_polynomial must be a RationalPolynomial")
    start = _positive_fraction("radius_start", cell.radius_start)
    width = _positive_fraction("step", cell.step)
    profile_radius = _nonnegative_fraction(
        "profile_radius", cell.profile_radius
    )
    derivative_radius = _nonnegative_fraction(
        "derivative_radius", cell.derivative_radius
    )
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)

    unit = RationalInterval(Fraction(0), Fraction(1))
    radius = RationalInterval(start, start + width)
    profile_center = cell.profile_polynomial.evaluate(unit)
    derivative_polynomial = cell.profile_polynomial.derivative()
    derivative_center = derivative_polynomial.evaluate(unit).scale(1 / width)
    center_tube = SkyrmionStateBox(profile_center, derivative_center)
    solution_tube = SkyrmionStateBox(
        _expand_interval(profile_center, profile_radius),
        _expand_interval(derivative_center, derivative_radius),
    )

    center_field = curved_skyrmion_acceleration_jacobian_box(
        radius,
        profile_center,
        derivative_center,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        trigonometric_terms=trigonometric_terms,
    )
    normalized_second_derivative = (
        derivative_polynomial.derivative().evaluate(unit).scale(1 / width**2)
    )
    defect = normalized_second_derivative - center_field.acceleration
    tube_field = curved_skyrmion_acceleration_jacobian_box(
        radius,
        solution_tube.profile,
        solution_tube.derivative,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        trigonometric_terms=trigonometric_terms,
    )

    profile_initial_center = cell.profile_polynomial.evaluate(Fraction(0))
    derivative_initial_center = derivative_polynomial.evaluate(
        Fraction(0)
    ).scale(1 / width)
    initial_profile_error = _absolute_upper(
        initial.profile - profile_initial_center
    )
    initial_derivative_error = _absolute_upper(
        initial.derivative - derivative_initial_center
    )
    defect_bound = _absolute_upper(defect)
    profile_jacobian_bound = _absolute_upper(tube_field.profile_derivative)
    derivative_jacobian_bound = _absolute_upper(
        tube_field.derivative_derivative
    )
    profile_self_map_bound = (
        initial_profile_error + width * derivative_radius
    )
    derivative_lipschitz_image = (
        profile_jacobian_bound * profile_radius
        + derivative_jacobian_bound * derivative_radius
    )
    derivative_self_map_bound = initial_derivative_error + width * (
        defect_bound + derivative_lipschitz_image
    )
    if profile_self_map_bound > profile_radius:
        raise ValueError("Taylor profile self-map inequality does not close")
    if derivative_self_map_bound > derivative_radius:
        raise ValueError("Taylor derivative self-map inequality does not close")
    contraction_bound = max(
        _weighted_row_bound(width * derivative_radius, profile_radius),
        _weighted_row_bound(
            width * derivative_lipschitz_image,
            derivative_radius,
        ),
    )
    if contraction_bound >= 1:
        raise ValueError("Taylor correction map is not a contraction")

    profile_endpoint_center = cell.profile_polynomial.evaluate(Fraction(1))
    derivative_endpoint_center = derivative_polynomial.evaluate(
        Fraction(1)
    ).scale(1 / width)
    endpoint = SkyrmionStateBox(
        _expand_interval(profile_endpoint_center, profile_self_map_bound),
        _expand_interval(
            derivative_endpoint_center,
            derivative_self_map_bound,
        ),
    )
    return ValidatedSkyrmionTaylorCell(
        radius_start=start,
        radius_end=start + width,
        initial=initial,
        profile_polynomial=cell.profile_polynomial,
        profile_radius=profile_radius,
        derivative_radius=derivative_radius,
        center_tube=center_tube,
        solution_tube=solution_tube,
        endpoint=endpoint,
        defect_box=defect,
        acceleration_box=tube_field.acceleration,
        profile_jacobian_box=tube_field.profile_derivative,
        derivative_jacobian_box=tube_field.derivative_derivative,
        profile_self_map_bound=profile_self_map_bound,
        derivative_self_map_bound=derivative_self_map_bound,
        contraction_bound=contraction_bound,
    )


def validate_skyrmion_taylor_track(
    initial: SkyrmionStateBox,
    cells: tuple[SkyrmionTaylorCell, ...],
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> ValidatedSkyrmionTaylorTrack:
    """Validate a nonempty sequence with exact endpoint-box chaining."""
    if not isinstance(cells, tuple):
        raise TypeError("cells must be a tuple of SkyrmionTaylorCell values")
    if not cells:
        raise ValueError("Taylor track must contain at least one cell")
    current = initial
    expected_start: Fraction | None = None
    validated: list[ValidatedSkyrmionTaylorCell] = []
    for cell in cells:
        if not isinstance(cell, SkyrmionTaylorCell):
            raise TypeError("cells must contain only SkyrmionTaylorCell values")
        start = _positive_fraction("radius_start", cell.radius_start)
        if expected_start is not None and start != expected_start:
            raise ValueError("Taylor cells must be contiguous in radius")
        checked = validate_skyrmion_taylor_cell(
            current,
            cell,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
            trigonometric_terms=trigonometric_terms,
        )
        validated.append(checked)
        current = checked.endpoint
        expected_start = checked.radius_end
    return ValidatedSkyrmionTaylorTrack(
        initial=initial,
        cells=tuple(validated),
        endpoint=current,
    )


def validate_skyrmion_picard_step(
    radius_start: Fraction,
    step: Fraction,
    initial: SkyrmionStateBox,
    tube: SkyrmionStateBox,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> ValidatedPicardStep:
    """Verify one conditional Picard tube and return its endpoint enclosure.

    The Picard image uses the integral form of ``F'=G, G'=Phi(x,F,G)``.  Strict
    containment of that image in ``tube`` proves existence.  The vector field
    is analytic on the checked positive-denominator box, hence locally
    Lipschitz and the enclosed solution is unique.
    """
    start = _positive_fraction("radius_start", radius_start)
    width = _positive_fraction("step", step)
    if not isinstance(initial, SkyrmionStateBox) or not isinstance(
        tube, SkyrmionStateBox
    ):
        raise TypeError("initial and tube must be SkyrmionStateBox values")
    if not initial.profile.is_subset_of(tube.profile) or not (
        initial.derivative.is_subset_of(tube.derivative)
    ):
        raise ValueError("initial box must lie in the candidate tube")
    radius = RationalInterval(start, start + width)
    time = RationalInterval(Fraction(0), width)
    acceleration = curved_skyrmion_acceleration_box(
        radius,
        tube.profile,
        tube.derivative,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    profile_image = initial.profile + time * tube.derivative
    derivative_image = initial.derivative + time * acceleration
    if not tube.profile.interior_contains(profile_image):
        raise ValueError("profile Picard image is not strictly inside the tube")
    if not tube.derivative.interior_contains(derivative_image):
        raise ValueError("derivative Picard image is not strictly inside the tube")
    endpoint = SkyrmionStateBox(
        initial.profile + tube.derivative.scale(width),
        initial.derivative + acceleration.scale(width),
    )
    return ValidatedPicardStep(
        radius_start=start,
        radius_end=start + width,
        initial=initial,
        tube=tube,
        endpoint=endpoint,
        profile_picard_image=profile_image,
        derivative_picard_image=derivative_image,
        acceleration_box=acceleration,
    )


def conditional_picard_foundation_certificate() -> dict[str, object]:
    """Exercise a real nonlinear Skyrmion cell with conditional initial data."""
    initial = SkyrmionStateBox(
        RationalInterval(Fraction(2983595, 1_000_000), Fraction(2983596, 1_000_000)),
        RationalInterval(Fraction(-1575269, 1_000_000), Fraction(-1575267, 1_000_000)),
    )
    tube = SkyrmionStateBox(
        RationalInterval(Fraction(2983436, 1_000_000), Fraction(2983597, 1_000_000)),
        RationalInterval(Fraction(-1575280, 1_000_000), Fraction(-1575240, 1_000_000)),
    )
    step = validate_skyrmion_picard_step(
        Fraction(1001, 10_000),
        Fraction(1, 1_000_000),
        initial,
        tube,
    )
    cubic = skyrmion_origin_cubic_coefficient_interval(
        RationalInterval(Fraction(1579953, 1_000_000), Fraction(1579954, 1_000_000))
    )
    checks = {
        "conditional_picard_profile_image_is_strictly_contained": (
            tube.profile.interior_contains(step.profile_picard_image)
        ),
        "conditional_picard_derivative_image_is_strictly_contained": (
            tube.derivative.interior_contains(step.derivative_picard_image)
        ),
        "endpoint_profile_remains_monotone_decreasing": (
            step.endpoint.derivative.upper < 0
        ),
        "origin_cubic_coefficient_is_positive": cubic.lower > 0,
    }
    return {
        "goal": "Validated Skyrmion Conditional ODE Step Foundation",
        "status": "pass" if all(checks.values()) else "fail",
        "result_type": "conditional_exact_rational_picard_step",
        "central_result": (
            "Given the displayed positive-radius initial box, exact interval "
            "Picard containment proves a unique curved-Skyrmion solution across "
            "the displayed cell and encloses its endpoint."
        ),
        "executable_checks": checks,
        "radius_start": str(step.radius_start),
        "radius_end": str(step.radius_end),
        "origin_cubic_coefficient_interval": {
            "lower": str(cubic.lower),
            "upper": str(cubic.upper),
        },
        "claim_boundary": (
            "The initial box is a conditional rational input near the floating "
            "profile. It is not connected to the certified regular-origin "
            "family box, so this certificate is ODE-checker infrastructure "
            "rather than AU.1 profile existence or shooting evidence."
        ),
        "next_physics_gate": (
            "use the certified uniform origin cutoff box as the first common-"
            "family Taylor-track input"
        ),
    }


def conditional_taylor_foundation_certificate() -> dict[str, object]:
    """Validate a short exact-rational normalized-polynomial track."""
    initial = SkyrmionStateBox(
        RationalInterval(
            Fraction(2983595, 1_000_000),
            Fraction(2983596, 1_000_000),
        ),
        RationalInterval(
            Fraction(-1575269, 1_000_000),
            Fraction(-1575267, 1_000_000),
        ),
    )
    width = Fraction(1, 1_000_000)
    profile_center = Fraction(5967191, 2_000_000)
    derivative_center = Fraction(-1575268, 1_000_000)
    linear = width * derivative_center
    first = SkyrmionTaylorCell(
        radius_start=Fraction(1001, 10_000),
        step=width,
        profile_polynomial=RationalPolynomial((profile_center, linear)),
        profile_radius=Fraction(1, 1_000_000),
        derivative_radius=Fraction(1, 100_000),
    )
    second = SkyrmionTaylorCell(
        radius_start=first.radius_start + width,
        step=width,
        profile_polynomial=RationalPolynomial(
            (profile_center + linear, linear)
        ),
        profile_radius=Fraction(2, 1_000_000),
        derivative_radius=Fraction(2, 100_000),
    )
    track = validate_skyrmion_taylor_track(initial, (first, second))
    checks = {
        "two_cells_chain_exact_checker_endpoints": (
            len(track.cells) == 2
            and track.cells[1].initial == track.cells[0].endpoint
        ),
        "all_componentwise_self_map_inequalities_close": all(
            cell.profile_self_map_bound <= cell.profile_radius
            and cell.derivative_self_map_bound <= cell.derivative_radius
            for cell in track.cells
        ),
        "all_weighted_contraction_bounds_are_below_one": all(
            cell.contraction_bound < 1 for cell in track.cells
        ),
        "track_derivative_remains_strictly_negative": (
            track.endpoint.derivative.upper < 0
        ),
    }
    return {
        "goal": "Validated Skyrmion Conditional Taylor Track Foundation",
        "status": "pass" if all(checks.values()) else "fail",
        "result_type": "conditional_exact_rational_taylor_track",
        "central_result": (
            "Given the displayed positive-radius initial box, independently "
            "recomputed defects and state Jacobians prove a unique solution "
            "inside two chained normalized-polynomial correction tubes."
        ),
        "executable_checks": checks,
        "radius_start": str(track.cells[0].radius_start),
        "radius_end": str(track.cells[-1].radius_end),
        "cell_count": len(track.cells),
        "claim_boundary": (
            "This is a two-microcell conditional track. Its initial box is "
            "not connected to the certified origin-family cutoff box, and it "
            "does not validate a shooting family or wall residual."
        ),
        "next_physics_gate": (
            "generate and validate a common-family track from a uniform "
            "origin box to the hard wall, plus two narrow endpoint tracks"
        ),
    }


def validated_skyrmion_profile_foundation_certificate() -> dict[str, object]:
    """Combine the conditional rectangle and Taylor-track foundations."""
    picard = conditional_picard_foundation_certificate()
    taylor = conditional_taylor_foundation_certificate()
    checks = {
        "conditional_picard_cell_passes": picard["status"] == "pass",
        "conditional_taylor_track_passes": taylor["status"] == "pass",
    }
    return {
        "goal": "Validated Skyrmion Positive-Radius ODE Foundations",
        "status": "pass" if all(checks.values()) else "fail",
        "result_type": "conditional_exact_rational_ode_foundations",
        "executable_checks": checks,
        "picard_foundation": picard,
        "taylor_foundation": taylor,
        "claim_boundary": (
            "Both results are conditional on supplied positive-radius input "
            "boxes and therefore do not constitute AU.1 profile existence."
        ),
    }
