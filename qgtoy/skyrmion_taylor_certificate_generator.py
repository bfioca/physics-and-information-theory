"""Untrusted generation of exact-rational Skyrmion Taylor tracks.

Nothing in this module is part of the trusted proof kernel.  Floating RK4
samples select polynomial centers, and heuristic radius iteration proposes
Taylor cells.  The result is useful only because every accepted cell, and the
complete returned track, are passed through the exact-rational validators in
``validated_skyrmion_profile``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .massive_skyrmion_worldtube import _rk4_hard_wall_profile
from .validated_interval import RationalInterval, RationalPolynomial
from .validated_skyrmion_origin import validate_skyrmion_origin_quintic_patch
from .validated_skyrmion_profile import (
    SkyrmionStateBox,
    SkyrmionTaylorCell,
    ValidatedSkyrmionTaylorCell,
    ValidatedSkyrmionTaylorTrack,
    curved_skyrmion_acceleration_jacobian_box,
    validate_skyrmion_taylor_cell,
    validate_skyrmion_taylor_track,
)


@dataclass(frozen=True)
class SkyrmionTaylorTrackGeneration:
    """Outcome of an untrusted generation attempt.

    ``status == "pass"`` means ``reached_radius == requested_radius``.  A
    partial result still contains only cells accepted by the trusted checker.
    ``validated_track`` is absent only when the first minimum-width cell could
    not be closed.
    """

    status: str
    shooting_slope: Fraction
    requested_radius: Fraction
    reached_radius: Fraction
    cells: tuple[SkyrmionTaylorCell, ...]
    validated_track: ValidatedSkyrmionTaylorTrack | None
    obstruction: str | None


def _fraction(
    name: str,
    value: int | Fraction,
    *,
    positive: bool = False,
) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    result = Fraction(value)
    if positive and result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _float_center(value: float, denominator: int) -> Fraction:
    if isinstance(denominator, bool) or not isinstance(denominator, int):
        raise TypeError("center_denominator must be an integer")
    if denominator < 1:
        raise ValueError("center_denominator must be positive")
    return Fraction(value).limit_denominator(denominator)


def _round_up(value: Fraction, denominator: int) -> Fraction:
    scaled = value * denominator
    numerator = -(-scaled.numerator // scaled.denominator)
    return Fraction(numerator, denominator)


def _power_of_two_stride(name: str, ratio: Fraction) -> int:
    if ratio.denominator != 1:
        raise ValueError(f"{name} must be an integer multiple of minimum_step")
    stride = ratio.numerator
    if stride < 1 or stride & (stride - 1):
        raise ValueError(f"{name}/minimum_step must be a power of two")
    return stride


def _cubic_hermite_polynomial(
    profile_start: Fraction,
    derivative_start: Fraction,
    profile_end: Fraction,
    derivative_end: Fraction,
    step: Fraction,
) -> RationalPolynomial:
    difference = profile_end - profile_start
    quadratic = 3 * difference - step * (
        2 * derivative_start + derivative_end
    )
    cubic = -2 * difference + step * (
        derivative_start + derivative_end
    )
    return RationalPolynomial(
        (
            profile_start,
            step * derivative_start,
            quadratic,
            cubic,
        )
    )


def _propose_checked_cell(
    initial: SkyrmionStateBox,
    *,
    radius_start: Fraction,
    step: Fraction,
    polynomial: RationalPolynomial,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    radius_denominator: int,
    radius_safety_factor: Fraction,
    maximum_radius_iterations: int,
) -> tuple[SkyrmionTaylorCell, ValidatedSkyrmionTaylorCell]:
    """Iterate untrusted radii, then ask the trusted cell checker."""
    unit = RationalInterval(Fraction(0), Fraction(1))
    radius = RationalInterval(radius_start, radius_start + step)
    derivative_polynomial = polynomial.derivative()
    profile_center = polynomial.evaluate(unit)
    derivative_center = derivative_polynomial.evaluate(unit).scale(1 / step)
    initial_profile_center = polynomial.evaluate(Fraction(0))
    initial_derivative_center = derivative_polynomial.evaluate(
        Fraction(0)
    ).scale(1 / step)
    initial_profile_error = _absolute_upper(
        initial.profile - initial_profile_center
    )
    initial_derivative_error = _absolute_upper(
        initial.derivative - initial_derivative_center
    )
    center_field = curved_skyrmion_acceleration_jacobian_box(
        radius,
        profile_center,
        derivative_center,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    normalized_second_derivative = (
        derivative_polynomial.derivative().evaluate(unit).scale(1 / step**2)
    )
    defect_bound = _absolute_upper(
        normalized_second_derivative - center_field.acceleration
    )

    quantum = Fraction(1, radius_denominator)
    profile_radius = _round_up(
        initial_profile_error + quantum,
        radius_denominator,
    )
    derivative_radius = _round_up(
        initial_derivative_error + quantum, radius_denominator
    )
    for _ in range(maximum_radius_iterations):
        solution_profile = profile_center + RationalInterval(
            -profile_radius, profile_radius
        )
        solution_derivative = derivative_center + RationalInterval(
            -derivative_radius, derivative_radius
        )
        tube_field = curved_skyrmion_acceleration_jacobian_box(
            radius,
            solution_profile,
            solution_derivative,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
            trigonometric_terms=trigonometric_terms,
        )
        profile_jacobian_bound = _absolute_upper(
            tube_field.profile_derivative
        )
        derivative_jacobian_bound = _absolute_upper(
            tube_field.derivative_derivative
        )
        profile_target = initial_profile_error + step * derivative_radius
        derivative_target = initial_derivative_error + step * (
            defect_bound
            + profile_jacobian_bound * profile_radius
            + derivative_jacobian_bound * derivative_radius
        )
        if (
            profile_target <= profile_radius
            and derivative_target <= derivative_radius
        ):
            cell = SkyrmionTaylorCell(
                radius_start=radius_start,
                step=step,
                profile_polynomial=polynomial,
                profile_radius=profile_radius,
                derivative_radius=derivative_radius,
            )
            checked = validate_skyrmion_taylor_cell(
                initial,
                cell,
                pion_mass_squared=pion_mass_squared,
                curvature=curvature,
                trigonometric_terms=trigonometric_terms,
            )
            return cell, checked
        profile_radius = max(
            profile_radius,
            _round_up(
                radius_safety_factor * (profile_target + quantum),
                radius_denominator,
            ),
        )
        derivative_radius = max(
            derivative_radius,
            _round_up(
                radius_safety_factor * (derivative_target + quantum),
                radius_denominator,
            ),
        )
    raise ValueError(
        "Taylor radius iteration did not close after "
        f"{maximum_radius_iterations} iterations"
    )


def generate_skyrmion_taylor_track(
    shooting_slope: Fraction,
    *,
    requested_radius: Fraction,
    initial: SkyrmionStateBox | None = None,
    radius_start: Fraction = Fraction(1, 16),
    minimum_step: Fraction = Fraction(1, 1024),
    maximum_step: Fraction | None = None,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 12,
    center_denominator: int = 10**12,
    radius_denominator: int = 10**12,
    radius_safety_factor: Fraction = Fraction(1001, 1000),
    maximum_radius_iterations: int = 20,
) -> SkyrmionTaylorTrackGeneration:
    """Generate, adaptively subdivide, and rigorously check a Taylor track.

    The existing floating hard-wall RK4 solver is sampled at ``minimum_step``.
    Candidate cells use cubic Hermite centers through selected RK4 endpoint
    data.  A failed candidate is retried at half its rational width until the
    minimum step is reached.  All accepted cells are finally checked together
    by :func:`validate_skyrmion_taylor_track`.
    """
    slope = _fraction("shooting_slope", shooting_slope, positive=True)
    start = _fraction("radius_start", radius_start, positive=True)
    target = _fraction("requested_radius", requested_radius, positive=True)
    minimum = _fraction("minimum_step", minimum_step, positive=True)
    maximum = minimum if maximum_step is None else _fraction(
        "maximum_step", maximum_step, positive=True
    )
    mass_squared = _fraction("pion_mass_squared", pion_mass_squared)
    curvature_value = _fraction("curvature", curvature)
    safety = _fraction(
        "radius_safety_factor", radius_safety_factor, positive=True
    )
    if target <= start:
        raise ValueError("requested_radius must exceed radius_start")
    if mass_squared < 0 or curvature_value < 0:
        raise ValueError("mass squared and curvature must be nonnegative")
    if safety <= 1:
        raise ValueError("radius_safety_factor must exceed one")
    if (
        isinstance(maximum_radius_iterations, bool)
        or not isinstance(maximum_radius_iterations, int)
        or maximum_radius_iterations < 1
    ):
        raise ValueError("maximum_radius_iterations must be positive")
    if (
        isinstance(radius_denominator, bool)
        or not isinstance(radius_denominator, int)
        or radius_denominator < 1
    ):
        raise ValueError("radius_denominator must be a positive integer")
    maximum_stride = _power_of_two_stride(
        "maximum_step", maximum / minimum
    )
    span = (target - start) / minimum
    if span.denominator != 1:
        raise ValueError(
            "requested radius must lie on the minimum-step grid"
        )
    fine_cell_count = span.numerator
    if initial is None:
        origin = validate_skyrmion_origin_quintic_patch(
            slope,
            cutoff=start,
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
        )
        current = SkyrmionStateBox(
            origin.profile_at_cutoff,
            origin.derivative_at_cutoff,
        )
    else:
        if not isinstance(initial, SkyrmionStateBox):
            raise TypeError("initial must be a SkyrmionStateBox")
        current = initial
    initial_state = current

    floating_points = _rk4_hard_wall_profile(
        float(slope),
        pion_mass=float(mass_squared) ** 0.5,
        curvature=float(curvature_value),
        wall_radius=float(target),
        step=float(minimum),
        origin_cutoff=float(start),
    )
    if len(floating_points) != fine_cell_count + 1:
        raise RuntimeError(
            "floating RK4 grid did not match the exact rational grid"
        )
    profile_center = _float_center(
        floating_points[0][1], center_denominator
    )
    derivative_center = _float_center(
        floating_points[0][2], center_denominator
    )

    cells: list[SkyrmionTaylorCell] = []
    fine_index = 0
    obstruction: str | None = None
    while fine_index < fine_cell_count:
        remaining = fine_cell_count - fine_index
        stride = maximum_stride
        while stride > remaining:
            stride //= 2
        last_error: Exception | None = None
        accepted = False
        while stride >= 1:
            endpoint_index = fine_index + stride
            candidate_step = minimum * stride
            next_profile = _float_center(
                floating_points[endpoint_index][1], center_denominator
            )
            next_derivative = _float_center(
                floating_points[endpoint_index][2], center_denominator
            )
            polynomial = _cubic_hermite_polynomial(
                profile_center,
                derivative_center,
                next_profile,
                next_derivative,
                candidate_step,
            )
            try:
                cell, checked = _propose_checked_cell(
                    current,
                    radius_start=start + minimum * fine_index,
                    step=candidate_step,
                    polynomial=polynomial,
                    pion_mass_squared=mass_squared,
                    curvature=curvature_value,
                    trigonometric_terms=trigonometric_terms,
                    radius_denominator=radius_denominator,
                    radius_safety_factor=safety,
                    maximum_radius_iterations=maximum_radius_iterations,
                )
            except (ValueError, ZeroDivisionError) as error:
                last_error = error
                stride //= 2
                continue
            cells.append(cell)
            current = checked.endpoint
            fine_index = endpoint_index
            profile_center = next_profile
            derivative_center = next_derivative
            accepted = True
            break
        if not accepted:
            obstruction = (
                f"minimum-step cell at radius {start + minimum * fine_index} "
                f"did not validate: {last_error}"
            )
            break

    validated: ValidatedSkyrmionTaylorTrack | None = None
    if cells:
        validated = validate_skyrmion_taylor_track(
            initial_state,
            tuple(cells),
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
            trigonometric_terms=trigonometric_terms,
        )
    reached = start + minimum * fine_index
    return SkyrmionTaylorTrackGeneration(
        status="pass" if reached == target else "partial",
        shooting_slope=slope,
        requested_radius=target,
        reached_radius=reached,
        cells=tuple(cells),
        validated_track=validated,
        obstruction=obstruction,
    )
