"""Sharp radial replay of the certified endpoint-corrected Skyrmion tube.

The AU.1 physical-observable audit stores whole-cell ranges.  Those boxes are
enough for existence and positivity, but merely bisecting them cannot recover
the profile correlation needed by AU.3b.  This module instead replays the exact
endpoint-corrected spline on every requested radial subcell and adds the local
Newton error radius that generated the authenticated parent tube.

The replay is exact rational arithmetic.  Authentication of the input archive
and companion snapshot remains the responsibility of the audit entry point.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    cos_center_lipschitz_interval,
    pi_machin_interval,
    sin_center_lipschitz_interval,
)
from .validated_rational_text import exact_fraction_from_text
from .validated_skyrmion_bvp import (
    SkyrmionJetBox,
    SkyrmionPolynomialCell,
    _affine_restrict_polynomial,
    _polynomial_subcell_jet,
    _rational_polynomial_add,
    _rational_polynomial_bernstein_range,
    _rational_polynomial_scale,
)
from .validated_skyrmion_origin import (
    ValidatedSkyrmionOriginFamily,
    _entire_even_kernel_interval,
    validate_skyrmion_origin_family,
    validate_skyrmion_origin_quintic_patch,
)


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _ceil_fraction(value: Fraction, denominator: int) -> Fraction:
    scaled = value * denominator
    numerator = -((-scaled.numerator) // scaled.denominator)
    return Fraction(numerator, denominator)


def _archive_interval(value: object) -> RationalInterval:
    if not isinstance(value, Mapping):
        raise TypeError("archived interval must be a mapping")
    lower = value.get("lower")
    upper = value.get("upper")
    if not isinstance(lower, str) or not isinstance(upper, str):
        raise TypeError("archived interval endpoints must be strings")
    return RationalInterval(
        exact_fraction_from_text(lower),
        exact_fraction_from_text(upper),
    )


def _fraction_field(record: Mapping[str, object], name: str) -> Fraction:
    value = record.get(name)
    if not isinstance(value, str):
        raise TypeError(f"{name} must be an exact rational string")
    return exact_fraction_from_text(value)


def _profile_cells(record: Mapping[str, object]) -> tuple[SkyrmionPolynomialCell, ...]:
    archived = record.get("profile_cells")
    if not isinstance(archived, Sequence) or isinstance(archived, (str, bytes)):
        raise TypeError("AU.2 profile_cells must be a sequence")
    cells = []
    for item in archived:
        if not isinstance(item, Mapping):
            raise TypeError("AU.2 profile cell must be a mapping")
        coefficients = item.get("coefficients")
        if not isinstance(coefficients, Sequence) or isinstance(
            coefficients, (str, bytes)
        ):
            raise TypeError("profile coefficients must be a sequence")
        if not coefficients or not all(isinstance(value, str) for value in coefficients):
            raise TypeError("profile coefficients must be rational strings")
        cells.append(
            SkyrmionPolynomialCell(
                radius=_archive_interval(item.get("radius")),
                profile_polynomial=RationalPolynomial(
                    tuple(exact_fraction_from_text(value) for value in coefficients)
                ),
            )
        )
    if not cells:
        raise ValueError("AU.2 archive has no profile cells")
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("AU.2 profile cells are not contiguous")
    return tuple(cells)


@dataclass(frozen=True)
class ValidatedSkyrmionSharpParentCell:
    source_cell_index: int
    radius: RationalInterval
    archived_tube_jet: SkyrmionJetBox
    endpoint_family_jet: SkyrmionJetBox
    profile_error_radius: Fraction
    derivative_error_radius: Fraction
    second_derivative_error_radius: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionSharpRadialCell:
    source_cell_index: int
    parent_cell_index: int
    radius: RationalInterval
    endpoint_family_jet: SkyrmionJetBox
    solution_profile: RationalInterval
    solution_derivative: RationalInterval
    solution_second_derivative: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionSharpProfileTube:
    certificate_id: str
    curvature: Fraction
    pion_mass_squared: Fraction
    origin_cutoff: Fraction
    wall_radius: Fraction
    shooting_slope_interval: RationalInterval
    origin_remainder_radius: Fraction
    profile_cells: tuple[SkyrmionPolynomialCell, ...]
    left_value_correction: RationalInterval
    right_value_correction: Fraction
    parents: tuple[ValidatedSkyrmionSharpParentCell, ...]
    cells: tuple[ValidatedSkyrmionSharpRadialCell, ...]
    subdivisions_per_parent: int
    claim_boundary: str


@dataclass(frozen=True)
class ValidatedSkyrmionSharpInertiaCell:
    region: str
    source_cell_index: int
    radius: RationalInterval
    density: RationalInterval
    integral: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionSharpMeasure:
    certificate_id: str
    curvature: Fraction
    origin_cutoff: Fraction
    wall_radius: Fraction
    origin_cells: tuple[ValidatedSkyrmionSharpInertiaCell, ...]
    positive_radius_cells: tuple[ValidatedSkyrmionSharpInertiaCell, ...]
    inertia: RationalInterval
    claim_boundary: str


def validate_validated_skyrmion_sharp_measure(
    measure: ValidatedSkyrmionSharpMeasure,
) -> None:
    """Reject internally inconsistent serialized or synthetic sharp measures."""

    if not isinstance(measure, ValidatedSkyrmionSharpMeasure):
        raise TypeError("measure must be a ValidatedSkyrmionSharpMeasure")
    if (
        measure.curvature <= 0
        or measure.origin_cutoff <= 0
        or measure.wall_radius <= measure.origin_cutoff
    ):
        raise ValueError("sharp measure geometry is invalid")
    if not measure.origin_cells or not measure.positive_radius_cells:
        raise ValueError("sharp measure requires origin and positive-radius cells")
    if (
        measure.origin_cells[0].radius.lower != 0
        or measure.origin_cells[-1].radius.upper != measure.origin_cutoff
        or measure.positive_radius_cells[0].radius.lower != measure.origin_cutoff
        or measure.positive_radius_cells[-1].radius.upper != measure.wall_radius
    ):
        raise ValueError("sharp measure cells do not cover the declared geometry")
    all_cells = (*measure.origin_cells, *measure.positive_radius_cells)
    for left, right in zip(all_cells, all_cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("sharp measure cells are not contiguous")
    recomputed_inertia = RationalInterval.point(0)
    for expected_region, cells in (
        ("origin", measure.origin_cells),
        ("positive_radius", measure.positive_radius_cells),
    ):
        for cell in cells:
            if cell.region != expected_region or cell.radius.width <= 0:
                raise ValueError("sharp measure cell label or radius is invalid")
            if cell.density.lower < 0 or cell.integral != cell.density.scale(
                cell.radius.width
            ):
                raise ValueError("sharp measure cell integral is inconsistent")
            recomputed_inertia += cell.integral
    if measure.inertia != recomputed_inertia or measure.inertia.lower <= 0:
        raise ValueError("sharp measure inertia does not match its cells")


@dataclass(frozen=True)
class ValidatedSkyrmionSharpWorldtubeConstants:
    certificate_id: str
    pion_mass_squared: Fraction
    curvature: Fraction
    wall_radius: Fraction
    interior_mass: RationalInterval
    shell_mass: RationalInterval
    total_mass: RationalInterval
    inertia: RationalInterval
    claim_boundary: str


def _endpoint_family_jet(
    profile_cell: SkyrmionPolynomialCell,
    normalized_left: Fraction,
    normalized_right: Fraction,
    *,
    domain_left: Fraction,
    domain_right: Fraction,
    left_value_correction: RationalInterval,
    right_value_correction: Fraction,
) -> SkyrmionJetBox:
    domain_length = domain_right - domain_left
    left_center = (
        Fraction(0)
        if left_value_correction.lower <= 0 <= left_value_correction.upper
        else left_value_correction.midpoint
    )
    left_deviation = left_value_correction - left_center
    if normalized_left != normalized_right:
        center = (normalized_left + normalized_right) / 2
        half_width = (normalized_right - normalized_left) / 2
        width = profile_cell.radius.width
        physical_center = profile_cell.radius.lower + width * center
        physical_half_width = width * half_width
        polynomial = profile_cell.profile_polynomial
        restricted = _affine_restrict_polynomial(polynomial, center, half_width)
        radius_polynomial = RationalPolynomial((physical_center, physical_half_width))
        chi_left_polynomial = RationalPolynomial(
            (
                (domain_right - physical_center) / domain_length,
                -physical_half_width / domain_length,
            )
        )
        chi_right_polynomial = RationalPolynomial(
            (
                (physical_center - domain_left) / domain_length,
                physical_half_width / domain_length,
            )
        )
        midpoint_polynomial = _rational_polynomial_add(
            restricted,
            _rational_polynomial_scale(chi_left_polynomial, left_center),
            _rational_polynomial_scale(
                chi_right_polynomial,
                right_value_correction,
            ),
        )
        chi_left_range = _rational_polynomial_bernstein_range(
            chi_left_polynomial
        )
        return SkyrmionJetBox(
            radius=_rational_polynomial_bernstein_range(radius_polynomial),
            profile=(
                _rational_polynomial_bernstein_range(midpoint_polynomial)
                + left_deviation * chi_left_range
            ),
            derivative=(
                _rational_polynomial_bernstein_range(
                    _rational_polynomial_scale(
                        midpoint_polynomial.derivative(),
                        1 / physical_half_width,
                    )
                )
                + left_deviation.scale(-1 / domain_length)
            ),
            second_derivative=_rational_polynomial_bernstein_range(
                _rational_polynomial_scale(
                    midpoint_polynomial.derivative().derivative(),
                    1 / physical_half_width**2,
                )
            ),
        )
    else:
        base = _polynomial_subcell_jet(
            profile_cell,
            normalized_left,
            normalized_right,
        )
    chi_left = (
        RationalInterval.point(domain_right) - base.radius
    ).scale(1 / domain_length)
    chi_right = (
        base.radius - RationalInterval.point(domain_left)
    ).scale(1 / domain_length)
    profile = (
        base.profile
        + chi_left.scale(left_center)
        + chi_right.scale(right_value_correction)
        + left_deviation * chi_left
    )
    derivative = (
        base.derivative
        + RationalInterval.point(
            (right_value_correction - left_center) / domain_length
        )
        + left_deviation.scale(-1 / domain_length)
    )
    return SkyrmionJetBox(
        radius=base.radius,
        profile=profile,
        derivative=derivative,
        second_derivative=base.second_derivative,
    )


def reconstruct_validated_skyrmion_sharp_profile(
    au2_record: Mapping[str, object],
    snapshot_record: Mapping[str, object],
    *,
    subdivisions_per_parent: int = 4,
) -> ValidatedSkyrmionSharpProfileTube:
    """Replay the exact spline family and local Newton tube on refined cells."""

    subdivisions = _positive_integer(
        "subdivisions_per_parent", subdivisions_per_parent
    )
    parameters = au2_record.get("parameters")
    physical = snapshot_record.get("sharp_profile_recipe")
    certificate_id = snapshot_record.get("certificate_id")
    if not isinstance(parameters, Mapping):
        raise TypeError("AU.2 parameters are missing")
    if not isinstance(physical, Mapping):
        raise TypeError("AU.3b sharp profile recipe is missing")
    if not isinstance(certificate_id, str) or not certificate_id:
        raise ValueError("AU.3b certificate id is missing")
    cells = _profile_cells(au2_record)
    curvature = _fraction_field(parameters, "curvature")
    mass_squared = _fraction_field(parameters, "pion_mass_squared")
    cutoff = _fraction_field(parameters, "origin_cutoff")
    wall = _fraction_field(parameters, "wall_radius")
    slope = _fraction_field(parameters, "shooting_slope")
    if cells[0].radius.lower != cutoff or cells[-1].radius.upper != wall:
        raise ValueError("AU.2 profile domain does not match its parameters")
    for name, expected in (
        ("curvature", curvature),
        ("pion_mass_squared", mass_squared),
        ("origin_cutoff", cutoff),
        ("wall_radius", wall),
    ):
        if _fraction_field(physical, name) != expected:
            raise ValueError(f"snapshot {name} does not match AU.2")

    origin = validate_skyrmion_origin_quintic_patch(
        slope,
        cutoff=cutoff,
        pion_mass_squared=mass_squared,
        curvature=curvature,
    )
    left_value = cells[0].profile_polynomial.evaluate(Fraction(0))
    right_value = cells[-1].profile_polynomial.evaluate(Fraction(1))
    left_correction = origin.profile_at_cutoff - left_value
    right_correction = -right_value.lower
    if _archive_interval(physical.get("left_value_correction")) != left_correction:
        raise ValueError("snapshot left endpoint correction does not replay")
    if _fraction_field(physical, "right_value_correction") != right_correction:
        raise ValueError("snapshot right endpoint correction does not replay")
    archived_cells = physical.get("cells")
    if not isinstance(archived_cells, Sequence) or isinstance(
        archived_cells, (str, bytes)
    ):
        raise TypeError("snapshot tube_cells must be a sequence")
    if len(archived_cells) != len(cells):
        raise ValueError("canonical sharp replay requires one tube cell per spline cell")

    omega = _fraction_field(physical, "omega")
    newton_radius = _fraction_field(physical, "newton_radius")
    rounding = int(_fraction_field(physical, "rounding_denominator"))
    if Fraction(rounding) != _fraction_field(physical, "rounding_denominator"):
        raise ValueError("snapshot rounding denominator must be an integer")
    _positive_integer("rounding_denominator", rounding)
    profile_second_sensitivity = _fraction_field(
        physical,
        "profile_second_sensitivity_upper_bound",
    )
    shooting_slopes = _archive_interval(physical.get("shooting_slope_interval"))
    origin_remainder = _fraction_field(physical, "origin_remainder_radius")
    if omega <= 0 or newton_radius <= 0 or profile_second_sensitivity < 0:
        raise ValueError("snapshot Newton replay parameters are invalid")
    expected_shooting_slopes = RationalInterval(
        slope - newton_radius / omega,
        slope + newton_radius / omega,
    )
    if shooting_slopes != expected_shooting_slopes:
        raise ValueError("snapshot shooting interval does not match AU.2 Newton tube")
    domain_length = wall - cutoff

    parents = []
    refined = []
    for parent_index, (profile_cell, item) in enumerate(zip(cells, archived_cells)):
        if not isinstance(item, Mapping):
            raise TypeError("snapshot tube cell must be a mapping")
        if item.get("source_cell_index") != parent_index:
            raise ValueError("snapshot tube source-cell ordering changed")
        archived_radius = _archive_interval(item.get("radius"))
        if archived_radius != profile_cell.radius:
            raise ValueError("snapshot tube radius does not match AU.2 spline")
        archived = SkyrmionJetBox(
            radius=archived_radius,
            profile=_archive_interval(item.get("archived_tube_profile")),
            derivative=_archive_interval(item.get("archived_tube_derivative")),
            second_derivative=_archive_interval(
                item.get("archived_tube_second_derivative")
            ),
        )
        family = _endpoint_family_jet(
            profile_cell,
            Fraction(0),
            Fraction(1),
            domain_left=cutoff,
            domain_right=wall,
            left_value_correction=left_correction,
            right_value_correction=right_correction,
        )
        if _archive_interval(item.get("endpoint_family_profile")) != family.profile:
            raise ValueError("snapshot endpoint profile family does not replay")
        if (
            _archive_interval(item.get("endpoint_family_derivative"))
            != family.derivative
        ):
            raise ValueError("snapshot endpoint derivative family does not replay")
        if (
            _archive_interval(item.get("endpoint_family_second_derivative"))
            != family.second_derivative
        ):
            raise ValueError("snapshot endpoint C2 family does not replay")
        base_c0 = _fraction_field(item, "local_graph_c0_upper_bound") + (
            _fraction_field(item, "local_auxiliary_c0_upper_bound") / omega
        )
        base_c1 = _fraction_field(item, "local_graph_c1_upper_bound") + (
            _fraction_field(item, "local_auxiliary_c1_upper_bound") / omega
        )
        base_c2 = _fraction_field(item, "local_graph_c2_upper_bound") + (
            _fraction_field(item, "local_auxiliary_c2_upper_bound") / omega
        )
        profile_radius = _ceil_fraction(
            base_c0 * newton_radius
            + profile_second_sensitivity * newton_radius**2 / (2 * omega**2),
            rounding,
        )
        derivative_radius = _ceil_fraction(
            base_c1 * newton_radius
            + profile_second_sensitivity
            * newton_radius**2
            / (2 * domain_length * omega**2),
            rounding,
        )
        second_radius = _ceil_fraction(
            base_c2 * newton_radius,
            rounding,
        )
        for name, recomputed in (
            ("profile_error_radius", profile_radius),
            ("derivative_error_radius", derivative_radius),
            ("second_derivative_error_radius", second_radius),
        ):
            if _fraction_field(item, name) != recomputed:
                raise ValueError(f"snapshot {name} does not replay")
        parents.append(
            ValidatedSkyrmionSharpParentCell(
                source_cell_index=parent_index,
                radius=archived_radius,
                archived_tube_jet=archived,
                endpoint_family_jet=family,
                profile_error_radius=profile_radius,
                derivative_error_radius=derivative_radius,
                second_derivative_error_radius=second_radius,
            )
        )
        for subdivision in range(subdivisions):
            normalized_left = Fraction(subdivision, subdivisions)
            normalized_right = Fraction(subdivision + 1, subdivisions)
            subfamily = _endpoint_family_jet(
                profile_cell,
                normalized_left,
                normalized_right,
                domain_left=cutoff,
                domain_right=wall,
                left_value_correction=left_correction,
                right_value_correction=right_correction,
            )
            solution_profile = subfamily.profile + RationalInterval(
                -profile_radius,
                profile_radius,
            )
            solution_derivative = subfamily.derivative + RationalInterval(
                -derivative_radius,
                derivative_radius,
            )
            solution_second = subfamily.second_derivative + RationalInterval(
                -second_radius,
                second_radius,
            )
            if not solution_profile.is_subset_of(archived.profile):
                raise ValueError("refined profile replay escaped its parent tube")
            if not solution_derivative.is_subset_of(archived.derivative):
                raise ValueError("refined derivative replay escaped its parent tube")
            if not solution_second.is_subset_of(archived.second_derivative):
                raise ValueError("refined C2 replay escaped its parent tube")
            refined.append(
                ValidatedSkyrmionSharpRadialCell(
                    source_cell_index=parent_index,
                    parent_cell_index=parent_index,
                    radius=subfamily.radius,
                    endpoint_family_jet=subfamily,
                    solution_profile=solution_profile,
                    solution_derivative=solution_derivative,
                    solution_second_derivative=solution_second,
                )
            )

    for left, right in zip(refined, refined[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("sharp radial replay is not contiguous")
    return ValidatedSkyrmionSharpProfileTube(
        certificate_id=certificate_id,
        curvature=curvature,
        pion_mass_squared=mass_squared,
        origin_cutoff=cutoff,
        wall_radius=wall,
        shooting_slope_interval=shooting_slopes,
        origin_remainder_radius=origin_remainder,
        profile_cells=cells,
        left_value_correction=left_correction,
        right_value_correction=right_correction,
        parents=tuple(parents),
        cells=tuple(refined),
        subdivisions_per_parent=subdivisions,
        claim_boundary=(
            "Exact replay of the authenticated endpoint-corrected spline plus "
            "the generating local Newton radii; this object is not itself an "
            "archive-authentication or frequency-integral theorem."
        ),
    )


def reconstruct_validated_skyrmion_sharp_origin_family(
    snapshot_record: Mapping[str, object],
) -> ValidatedSkyrmionOriginFamily:
    """Recompute and exactly match the sharp snapshot's origin-family proof."""

    recipe = snapshot_record.get("sharp_profile_recipe")
    if not isinstance(recipe, Mapping):
        raise TypeError("AU.3b sharp profile recipe is missing")
    archived = recipe.get("origin_family")
    if not isinstance(archived, Mapping):
        raise TypeError("AU.3b sharp origin family is missing")
    result = validate_skyrmion_origin_family(
        _archive_interval(archived.get("shooting_slopes")),
        cutoff=_fraction_field(archived, "cutoff"),
        remainder_radius=_fraction_field(archived, "remainder_radius"),
        pion_mass_squared=_fraction_field(archived, "pion_mass_squared"),
        curvature=_fraction_field(archived, "curvature"),
    )
    exact_fields = {
        "shooting_slopes": result.shooting_slopes,
        "cutoff": result.cutoff,
        "pion_mass_squared": result.pion_mass_squared,
        "curvature": result.curvature,
        "cubic_coefficient": result.cubic_coefficient,
        "remainder_radius": result.remainder_radius,
        "residual_bound": result.residual_bound,
        "contraction_bound": result.contraction_bound,
        "volterra_denominator_lower_bound": (
            result.volterra_denominator_lower_bound
        ),
        "profile_at_cutoff": result.profile_at_cutoff,
        "derivative_at_cutoff": result.derivative_at_cutoff,
    }
    for name, expected in exact_fields.items():
        actual = (
            _archive_interval(archived.get(name))
            if isinstance(expected, RationalInterval)
            else _fraction_field(archived, name)
        )
        if actual != expected:
            raise ValueError(f"snapshot origin-family field {name} does not replay")
    return result


def build_validated_skyrmion_sharp_measure(
    profile: ValidatedSkyrmionSharpProfileTube,
    origin_family: ValidatedSkyrmionOriginFamily,
    *,
    origin_subdivisions: int = 8,
    trigonometric_terms: int = 24,
    origin_kernel_terms: int = 20,
    pi_terms: int = 80,
) -> ValidatedSkyrmionSharpMeasure:
    """Recompute a directed inertia measure on the sharp radial replay."""

    origin_parts = _positive_integer("origin_subdivisions", origin_subdivisions)
    trig_terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    kernel_terms = _positive_integer("origin_kernel_terms", origin_kernel_terms)
    pi_count = _positive_integer("pi_terms", pi_terms)
    if origin_family.cutoff != profile.origin_cutoff:
        raise ValueError("origin family cutoff does not match sharp profile")
    if (
        origin_family.curvature != profile.curvature
        or origin_family.pion_mass_squared != profile.pion_mass_squared
    ):
        raise ValueError("origin family parameters do not match sharp profile")
    if origin_family.shooting_slopes != profile.shooting_slope_interval:
        raise ValueError("origin family shooting branch does not match sharp profile")
    if origin_family.remainder_radius != profile.origin_remainder_radius:
        raise ValueError("origin family remainder ball does not match sharp profile")
    factor = pi_machin_interval(terms=pi_count).scale(Fraction(2, 3))

    positive_cells = []
    for cell in profile.cells:
        radius_squared = cell.radius.power(2)
        lapse = RationalInterval.point(1) - radius_squared.scale(profile.curvature)
        if lapse.lower <= 0:
            raise ValueError("sharp inertia cell reaches the horizon")
        sine_squared = sin_center_lipschitz_interval(
            cell.solution_profile,
            terms=trig_terms,
        ).power(2)
        derivative_squared = cell.solution_derivative.power(2)
        density = factor * (
            radius_squared * sine_squared / lapse
            + (radius_squared * sine_squared * derivative_squared).scale(4)
            + sine_squared.power(2).scale(4) / lapse
        )
        if density.lower < 0:
            raise AssertionError("positive-radius inertia density became negative")
        positive_cells.append(
            ValidatedSkyrmionSharpInertiaCell(
                region="positive_radius",
                source_cell_index=cell.source_cell_index,
                radius=cell.radius,
                density=density,
                integral=density.scale(cell.radius.width),
            )
        )

    origin_cells = []
    origin_step = profile.origin_cutoff / origin_parts
    remainder = origin_family.remainder_radius
    remainder_box = RationalInterval(-remainder, remainder)
    for index in range(origin_parts):
        radius = RationalInterval(index * origin_step, (index + 1) * origin_step)
        time = radius.power(2)
        time_squared = time.power(2)
        u = (
            origin_family.shooting_slopes
            - origin_family.cubic_coefficient * time
            + (remainder_box * time_squared).scale(Fraction(1, 5))
        )
        momentum = (
            origin_family.shooting_slopes
            - (origin_family.cubic_coefficient * time).scale(3)
            + remainder_box * time_squared
        )
        argument_squared = time * u.power(2)
        sinc = _entire_even_kernel_interval(
            argument_squared,
            scale_squared=1,
            derivative_order=0,
            terms=kernel_terms,
        )
        sine_over_radius = u * sinc
        sine_over_radius_squared = sine_over_radius.power(2)
        lapse = RationalInterval.point(1) - time.scale(profile.curvature)
        density = (
            factor
            * time_squared
            / lapse
            * (
                sine_over_radius_squared
                * (
                    RationalInterval.point(1)
                    + (lapse * momentum.power(2)).scale(4)
                )
                + sine_over_radius_squared.power(2).scale(4)
            )
        )
        if density.lower < 0:
            raise AssertionError("origin inertia density became negative")
        origin_cells.append(
            ValidatedSkyrmionSharpInertiaCell(
                region="origin",
                source_cell_index=index,
                radius=radius,
                density=density,
                integral=density.scale(radius.width),
            )
        )

    inertia = RationalInterval.point(0)
    for cell in (*origin_cells, *positive_cells):
        inertia += cell.integral
    if inertia.lower <= 0:
        raise ValueError("sharp inertia replay did not prove positive inertia")
    return ValidatedSkyrmionSharpMeasure(
        certificate_id=profile.certificate_id,
        curvature=profile.curvature,
        origin_cutoff=profile.origin_cutoff,
        wall_radius=profile.wall_radius,
        origin_cells=tuple(origin_cells),
        positive_radius_cells=tuple(positive_cells),
        inertia=inertia,
        claim_boundary=(
            "Directed box integral of the certified Newton solution's inertia "
            "density; it is not a quadrature-error estimate or a spectral norm."
        ),
    )


def build_validated_skyrmion_sharp_worldtube_constants(
    profile: ValidatedSkyrmionSharpProfileTube,
    origin_family: ValidatedSkyrmionOriginFamily,
    *,
    measure: ValidatedSkyrmionSharpMeasure | None = None,
    origin_subdivisions: int = 8,
    trigonometric_terms: int = 24,
    origin_kernel_terms: int = 20,
    pi_terms: int = 80,
) -> ValidatedSkyrmionSharpWorldtubeConstants:
    """Certify inertia and centered Young-Laplace worldtube mass constants."""

    if measure is None:
        measure = build_validated_skyrmion_sharp_measure(
            profile,
            origin_family,
            origin_subdivisions=origin_subdivisions,
            trigonometric_terms=trigonometric_terms,
            origin_kernel_terms=origin_kernel_terms,
            pi_terms=pi_terms,
        )
    else:
        validate_validated_skyrmion_sharp_measure(measure)
    if (
        measure.certificate_id != profile.certificate_id
        or measure.curvature != profile.curvature
        or measure.origin_cutoff != profile.origin_cutoff
        or measure.wall_radius != profile.wall_radius
    ):
        raise ValueError("sharp measure provenance does not match profile")
    if len(measure.positive_radius_cells) != len(profile.cells):
        raise ValueError("sharp measure positive-radius cover does not match profile")
    if any(
        measure_cell.radius != profile_cell.radius
        for measure_cell, profile_cell in zip(
            measure.positive_radius_cells,
            profile.cells,
        )
    ):
        raise ValueError("sharp measure positive-radius cells do not match profile")
    origin_parts = _positive_integer("origin_subdivisions", origin_subdivisions)
    if len(measure.origin_cells) != origin_parts:
        raise ValueError("sharp measure origin subdivision count does not match")
    pi_interval = pi_machin_interval(terms=pi_terms)
    energy_integral = RationalInterval.point(0)
    for cell in profile.cells:
        radius_squared = cell.radius.power(2)
        lapse = RationalInterval.point(1) - radius_squared.scale(profile.curvature)
        sine = sin_center_lipschitz_interval(
            cell.solution_profile,
            terms=trigonometric_terms,
        )
        cosine = cos_center_lipschitz_interval(
            cell.solution_profile,
            terms=trigonometric_terms,
        )
        sine_squared = sine.power(2)
        derivative_squared = cell.solution_derivative.power(2)
        density = (
            lapse
            * (radius_squared + sine_squared.scale(8))
            * derivative_squared
        ).scale(Fraction(1, 8))
        density += sine_squared.scale(Fraction(1, 4))
        density += sine_squared.power(2) / radius_squared.scale(2)
        density += (
            radius_squared
            * (RationalInterval.point(1) - cosine)
        ).scale(profile.pion_mass_squared / 4)
        if density.lower < 0:
            raise AssertionError("positive-radius energy density became negative")
        energy_integral += density.scale(cell.radius.width)

    origin_step = profile.origin_cutoff / origin_parts
    remainder_box = RationalInterval(
        -origin_family.remainder_radius,
        origin_family.remainder_radius,
    )
    for index in range(origin_parts):
        radius = RationalInterval(index * origin_step, (index + 1) * origin_step)
        time = radius.power(2)
        time_squared = time.power(2)
        u = (
            origin_family.shooting_slopes
            - origin_family.cubic_coefficient * time
            + (remainder_box * time_squared).scale(Fraction(1, 5))
        )
        momentum = (
            origin_family.shooting_slopes
            - (origin_family.cubic_coefficient * time).scale(3)
            + remainder_box * time_squared
        )
        argument = radius * u
        argument_squared = time * u.power(2)
        sinc = _entire_even_kernel_interval(
            argument_squared,
            scale_squared=1,
            derivative_order=0,
            terms=origin_kernel_terms,
        )
        cosine = cos_center_lipschitz_interval(
            argument,
            terms=trigonometric_terms,
        )
        sine_over_radius_squared = (u * sinc).power(2)
        lapse = RationalInterval.point(1) - time.scale(profile.curvature)
        density = (
            lapse
            * time
            * (RationalInterval.point(1) + sine_over_radius_squared.scale(8))
            * momentum.power(2)
        ).scale(Fraction(1, 8))
        density += (time * sine_over_radius_squared).scale(Fraction(1, 4))
        density += (time * sine_over_radius_squared.power(2)).scale(Fraction(1, 2))
        density += (
            time * (RationalInterval.point(1) + cosine)
        ).scale(profile.pion_mass_squared / 4)
        if density.lower < 0:
            raise AssertionError("origin energy density became negative")
        energy_integral += density.scale(radius.width)

    interior_mass = pi_interval.scale(4) * energy_integral
    wall_derivative = profile.cells[-1].solution_derivative
    wall_squared = profile.wall_radius**2
    wall_lapse = 1 - profile.curvature * wall_squared
    wall_denominator = 2 - 3 * profile.curvature * wall_squared
    if wall_lapse <= 0 or wall_denominator <= 0:
        raise ValueError("centered positive-tension wall condition is not satisfied")
    shell_mass = (
        pi_interval
        * wall_derivative.power(2)
    ).scale(
        profile.wall_radius**3
        * wall_lapse**2
        / (2 * wall_denominator)
    )
    total_mass = interior_mass + shell_mass
    return ValidatedSkyrmionSharpWorldtubeConstants(
        certificate_id=profile.certificate_id,
        pion_mass_squared=profile.pion_mass_squared,
        curvature=profile.curvature,
        wall_radius=profile.wall_radius,
        interior_mass=interior_mass,
        shell_mass=shell_mass,
        total_mass=total_mass,
        inertia=measure.inertia,
        claim_boundary=(
            "Directed fixed-background interior energy plus the centered "
            "Young-Laplace Nambu-Goto shell mass. This is not an "
            "Einstein-Skyrme junction or nonspherical stability theorem."
        ),
    )
