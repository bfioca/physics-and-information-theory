"""Profile-resolving directed frequency bounds for the certified Skyrmion.

The AU.3a theorem uses only positivity of the normalized inertia measure.  This
module consumes the authenticated cellwise inertia snapshot and retains the
radial distribution inside the same identity

``H(p)=3(1+p^2)^-1 int K(p,y)/tanh(y)^2 dmu``.

Every finite-band integral is an exact rational upper sum.  Transcendental
point values use rational Taylor remainders and all intermediate intervals are
rounded outwards to a declared rational grid.  The result remains conditional
until a caller authenticates both the AU.2 archive and its companion tube
snapshot.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from multiprocessing import get_context
from typing import Mapping

from .validated_interval import (
    RationalInterval,
    atanh_fraction_interval,
    cos_center_lipschitz_interval,
    pi_machin_interval,
    sin_center_lipschitz_interval,
)
from .validated_skyrmion_au3 import (
    _fraction_text,
    _sqrt_upper,
    _upper_float,
    exact_fraction_from_text,
    reconstruct_au2_spectral_ledger,
)
from .validated_skyrmion_spectral_ledger import (
    build_validated_skyrmion_spectral_ledger,
)
from .validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpMeasure,
    validate_validated_skyrmion_sharp_measure,
)


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _positive_fraction(name: str, value: int | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    result = Fraction(value)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _digest(name: str, value: str | None) -> str | None:
    if value is None:
        return None
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"{name} must be a lowercase SHA256")
    return value


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


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def _ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _round_interval(
    value: RationalInterval,
    denominator: int,
) -> RationalInterval:
    scale = _positive_integer("rounding_denominator", denominator)
    return RationalInterval(
        Fraction(_floor_fraction(value.lower * scale), scale),
        Fraction(_ceil_fraction(value.upper * scale), scale),
    )


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _symmetric(radius: Fraction) -> RationalInterval:
    if radius < 0:
        raise ValueError("symmetric radius must be nonnegative")
    return RationalInterval(-radius, radius)


def _perfect_rational_square_root(value: Fraction) -> Fraction:
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator**2 != value.numerator or denominator**2 != value.denominator:
        raise ValueError("AU.3b currently requires point-square curvature")
    return Fraction(numerator, denominator)


@dataclass(frozen=True)
class ValidatedSkyrmionInertiaDensityCell:
    source_cell_index: int
    radius: RationalInterval
    density: RationalInterval
    integral: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionAU3BProfile:
    certificate_id: str
    canonical_au2_sha256: str
    curvature: Fraction
    origin_cutoff: Fraction
    wall_radius: Fraction
    inertia: RationalInterval
    origin_inertia_upper_bound: Fraction
    cells: tuple[ValidatedSkyrmionInertiaDensityCell, ...]


def reconstruct_au3b_profile(
    snapshot: Mapping[str, object],
) -> ValidatedSkyrmionAU3BProfile:
    """Validate the algebraic consistency of one serialized tube snapshot."""

    certificate_id = snapshot.get("certificate_id")
    canonical_sha = snapshot.get("canonical_au2_sha256")
    physical = snapshot.get("physical_observables")
    if not isinstance(certificate_id, str) or not certificate_id:
        raise ValueError("tube snapshot certificate id is missing")
    if not isinstance(canonical_sha, str):
        raise TypeError("canonical AU.2 digest must be a string")
    canonical_digest = _digest("canonical_au2_sha256", canonical_sha)
    if canonical_digest is None:
        raise ValueError("canonical AU.2 digest is required")
    if not isinstance(physical, Mapping):
        raise TypeError("tube snapshot physical observables are missing")
    if not all(
        physical.get(name) is True
        for name in (
            "strict_monotonicity_verified",
            "negative_wall_slope_verified",
            "positive_finite_inertia_verified",
        )
    ):
        raise ValueError("tube snapshot does not carry all AU.1 physical checks")
    curvature = exact_fraction_from_text(str(physical["curvature"]))
    origin_cutoff = exact_fraction_from_text(str(physical["origin_cutoff"]))
    wall_radius = exact_fraction_from_text(str(physical["wall_radius"]))
    inertia = _archive_interval(physical["inertia_enclosure"])
    origin_upper = exact_fraction_from_text(
        str(physical["origin_inertia_upper_bound"])
    )
    if curvature <= 0 or origin_cutoff <= 0 or wall_radius <= origin_cutoff:
        raise ValueError("invalid physical domain in tube snapshot")
    if inertia.lower <= 0 or origin_upper < 0:
        raise ValueError("tube snapshot inertia data must be nonnegative")
    cell_records = physical.get("inertia_cells")
    if not isinstance(cell_records, (list, tuple)) or not cell_records:
        raise ValueError("tube snapshot must contain inertia cells")
    cells = []
    for position, record in enumerate(cell_records):
        if not isinstance(record, Mapping):
            raise TypeError("inertia cell must be a mapping")
        source_index = record.get("source_cell_index")
        if source_index != position:
            raise ValueError("inertia cells must retain source order")
        radius = _archive_interval(record["radius"])
        density = _archive_interval(record["density_enclosure"])
        integral = _archive_interval(record["integral_enclosure"])
        if density.lower < 0:
            raise ValueError("certified inertia density must be nonnegative")
        if integral != density.scale(radius.width):
            raise ValueError("inertia cell integral does not match its density")
        cells.append(
            ValidatedSkyrmionInertiaDensityCell(
                source_cell_index=position,
                radius=radius,
                density=density,
                integral=integral,
            )
        )
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("inertia cells must form a contiguous cover")
    if cells[0].radius.lower != origin_cutoff:
        raise ValueError("inertia cells do not start at the origin cutoff")
    if cells[-1].radius.upper != wall_radius:
        raise ValueError("inertia cells do not reach the wall")
    positive_sum = RationalInterval.point(0)
    for cell in cells:
        positive_sum += cell.integral
    expected_inertia = RationalInterval(
        positive_sum.lower,
        positive_sum.upper + origin_upper,
    )
    if inertia != expected_inertia:
        raise ValueError("snapshot inertia does not match its certified cells")
    return ValidatedSkyrmionAU3BProfile(
        certificate_id=certificate_id,
        canonical_au2_sha256=canonical_digest,
        curvature=curvature,
        origin_cutoff=origin_cutoff,
        wall_radius=wall_radius,
        inertia=inertia,
        origin_inertia_upper_bound=origin_upper,
        cells=tuple(cells),
    )


def _periodic_trigonometric_intervals(
    argument: RationalInterval,
    *,
    pi_interval: RationalInterval,
    terms: int,
    rounding_denominator: int,
) -> tuple[RationalInterval, RationalInterval]:
    """Enclose sine and cosine after exact interval range reduction."""

    midpoint = argument.midpoint
    period_midpoint = 2 * pi_interval.midpoint
    turns = _floor_fraction(midpoint / period_midpoint + Fraction(1, 2))
    reduced = argument - pi_interval.scale(2 * turns)
    sine = sin_center_lipschitz_interval(reduced, terms=terms)
    cosine = cos_center_lipschitz_interval(reduced, terms=terms)
    return (
        _round_interval(sine, rounding_denominator),
        _round_interval(cosine, rounding_denominator),
    )


def _sinc_derivative_interval(
    argument: RationalInterval,
    order: int,
    *,
    pi_interval: RationalInterval,
    terms: int,
    rounding_denominator: int,
) -> RationalInterval:
    if order not in (0, 1, 2):
        raise ValueError("sinc derivative order must be zero, one, or two")
    center = argument.midpoint
    if center == 0:
        point = (
            RationalInterval.point(1),
            RationalInterval.point(0),
            RationalInterval.point(Fraction(-1, 3)),
        )[order]
    else:
        sine, cosine = _periodic_trigonometric_intervals(
            RationalInterval.point(center),
            pi_interval=pi_interval,
            terms=terms,
            rounding_denominator=rounding_denominator,
        )
        center_interval = RationalInterval.point(center)
        if order == 0:
            point = sine / center_interval
        elif order == 1:
            point = (
                center_interval * cosine - sine
            ) / center_interval.power(2)
        else:
            point = (
                (RationalInterval.point(2) - center_interval.power(2)) * sine
                - (center_interval * cosine).scale(2)
            ) / center_interval.power(3)
    radius = argument.width / (2 * (order + 2))
    expanded = point + _symmetric(radius)
    global_bound = Fraction(1, order + 1)
    return _round_interval(
        RationalInterval(
            max(-global_bound, expanded.lower),
            min(global_bound, expanded.upper),
        ),
        rounding_denominator,
    )


@dataclass(frozen=True)
class _RadialIntegrationCell:
    radius: RationalInterval
    optical_radius: RationalInterval
    y_over_tanh: RationalInterval
    inverse_tanh_squared: RationalInterval
    density: RationalInterval


def _radial_integration_cells(
    profile: ValidatedSkyrmionAU3BProfile,
    *,
    subdivisions: int,
    atanh_terms: int,
    rounding_denominator: int,
) -> tuple[_RadialIntegrationCell, ...]:
    root_curvature = _perfect_rational_square_root(profile.curvature)
    result = []
    for parent in profile.cells:
        spacing = parent.radius.width / subdivisions
        for subdivision in range(subdivisions):
            left = parent.radius.lower + subdivision * spacing
            right = left + spacing
            left_z = root_curvature * left
            right_z = root_curvature * right
            if left_z <= 0 or right_z >= 1:
                raise ValueError("radial integration cell leaves the static patch")
            y = _round_interval(
                RationalInterval(
                    atanh_fraction_interval(left_z, terms=atanh_terms).lower,
                    atanh_fraction_interval(right_z, terms=atanh_terms).upper,
                ),
                rounding_denominator,
            )
            z = RationalInterval(left_z, right_z)
            tanh_squared = RationalInterval.point(profile.curvature) * (
                RationalInterval(left, right).power(2)
            )
            result.append(
                _RadialIntegrationCell(
                    radius=RationalInterval(left, right),
                    optical_radius=y,
                    y_over_tanh=_round_interval(
                        y / z,
                        rounding_denominator,
                    ),
                    inverse_tanh_squared=_round_interval(
                        RationalInterval.point(1) / tanh_squared,
                        rounding_denominator,
                    ),
                    density=parent.density,
                )
            )
    return tuple(result)


def _kernel_derivative_intervals(
    momentum: RationalInterval,
    radial: _RadialIntegrationCell,
    *,
    pi_interval: RationalInterval,
    trigonometric_terms: int,
    rounding_denominator: int,
) -> tuple[RationalInterval, RationalInterval, RationalInterval]:
    y = radial.optical_radius
    y_squared = y.power(2)
    phase = momentum * y
    sine, cosine = _periodic_trigonometric_intervals(
        phase,
        pi_interval=pi_interval,
        terms=trigonometric_terms,
        rounding_denominator=rounding_denominator,
    )
    sinc = tuple(
        _sinc_derivative_interval(
            phase,
            order,
            pi_interval=pi_interval,
            terms=trigonometric_terms,
            rounding_denominator=rounding_denominator,
        )
        for order in range(3)
    )
    kernels = (
        radial.y_over_tanh * sinc[0] - cosine,
        (y * radial.y_over_tanh) * sinc[1] + y * sine,
        (y_squared * radial.y_over_tanh) * sinc[2] + y_squared * cosine,
    )
    return tuple(
        _round_interval(
            kernel * radial.inverse_tanh_squared,
            rounding_denominator,
        )
        for kernel in kernels
    )  # type: ignore[return-value]


def _profile_resolved_form_factor_derivative_bounds(
    momentum: RationalInterval,
    profile: ValidatedSkyrmionAU3BProfile,
    radial_cells: tuple[_RadialIntegrationCell, ...],
    *,
    pi_interval: RationalInterval,
    trigonometric_terms: int,
    rounding_denominator: int,
) -> tuple[Fraction, Fraction, Fraction]:
    numerator = [RationalInterval.point(0) for _ in range(3)]
    for radial in radial_cells:
        kernels = _kernel_derivative_intervals(
            momentum,
            radial,
            pi_interval=pi_interval,
            trigonometric_terms=trigonometric_terms,
            rounding_denominator=rounding_denominator,
        )
        for order in range(3):
            numerator[order] += (
                radial.density * kernels[order]
            ).scale(radial.radius.width)
    root_curvature = _perfect_rational_square_root(profile.curvature)
    origin_y = atanh_fraction_interval(
        root_curvature * profile.origin_cutoff,
        terms=80,
    ).upper
    origin_c = 1 / (1 - profile.curvature * profile.origin_cutoff**2)
    origin_d = Fraction(4, 3) + origin_y**2 / 3
    origin_bounds = (
        origin_c * (1 + Fraction(2, 3) * momentum.upper**2),
        origin_c * origin_d * momentum.upper,
        origin_c * origin_d,
    )
    for order in range(3):
        numerator[order] += _symmetric(
            profile.origin_inertia_upper_bound * origin_bounds[order]
        )
        numerator[order] = _round_interval(
            numerator[order] / profile.inertia,
            rounding_denominator,
        ).scale(3)

    denominator = RationalInterval.point(1) + momentum.power(2)
    first = (
        numerator[1] / denominator
        - (momentum * numerator[0]).scale(2) / denominator.power(2)
    )
    second = (
        numerator[2] / denominator
        - (momentum * numerator[1]).scale(4) / denominator.power(2)
        + (
            (momentum.power(2).scale(6) - RationalInterval.point(2))
            * numerator[0]
        )
        / denominator.power(3)
    )
    form = (
        numerator[0] / denominator,
        first,
        second,
    )
    return tuple(_absolute_upper(value) for value in form)  # type: ignore[return-value]


@dataclass(frozen=True)
class ValidatedSkyrmionAU3BCertificate:
    certificate_id: str
    authenticated_au2_sha256: str | None
    authenticated_snapshot_sha256: str | None
    band_split: Fraction
    frequency_step: Fraction
    radial_subdivisions: int
    finite_band_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    tail_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    global_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    q_norm_upper_bounds: tuple[Fraction, Fraction, Fraction]
    jump_l1_upper_bound: Fraction
    jump_first_moment_upper_bound: Fraction

    def to_record(self) -> dict[str, object]:
        authenticated = (
            self.authenticated_au2_sha256 is not None
            and self.authenticated_snapshot_sha256 is not None
        )

        def exact(values: tuple[Fraction, Fraction, Fraction]) -> tuple[str, ...]:
            return tuple(_fraction_text(value) for value in values)

        return {
            "goal": "Validated Skyrmion AU.3b Profile-Resolved Certificate",
            "result_type": "directed_cellwise_inertia_frequency_upper_bounds",
            "au3b_status": (
                "complete_authenticated_profile_resolved_upper_certificate"
                if authenticated
                else "conditional_profile_resolved_upper_certificate"
            ),
            "certificate_id": self.certificate_id,
            "authenticated_au2_sha256": self.authenticated_au2_sha256,
            "authenticated_snapshot_sha256": self.authenticated_snapshot_sha256,
            "band_split": _fraction_text(self.band_split),
            "frequency_step": _fraction_text(self.frequency_step),
            "radial_subdivisions": self.radial_subdivisions,
            "finite_band_squared_h2_bounds_exact": exact(
                self.finite_band_squared_h2_bounds
            ),
            "tail_squared_h2_bounds_exact": exact(self.tail_squared_h2_bounds),
            "global_squared_h2_bounds_exact": exact(
                self.global_squared_h2_bounds
            ),
            "q_norm_upper_bounds_exact": exact(self.q_norm_upper_bounds),
            "q_norm_upper_bounds": tuple(
                _upper_float(value) for value in self.q_norm_upper_bounds
            ),
            "jump_l1_upper_bound_exact": _fraction_text(
                self.jump_l1_upper_bound
            ),
            "jump_l1_upper_bound": _upper_float(self.jump_l1_upper_bound),
            "jump_first_moment_upper_bound_exact": _fraction_text(
                self.jump_first_moment_upper_bound
            ),
            "jump_first_moment_upper_bound": _upper_float(
                self.jump_first_moment_upper_bound
            ),
            "claim_boundary": (
                "The finite band uses certified cellwise inertia-density "
                "ranges and directed kernel upper sums. It still discards "
                "within-cell profile correlations and does not prove a "
                "finite-coupling reduced-dynamics, switching, access, stress, "
                "lifetime, or gravitational theorem."
            ),
        }


def build_validated_skyrmion_au3b_certificate(
    au2_record: Mapping[str, object],
    snapshot_record: Mapping[str, object],
    *,
    band_split: int | Fraction = 400,
    frequency_step: int | Fraction = 1,
    radial_subdivisions: int = 4,
    trigonometric_terms: int = 24,
    atanh_terms: int = 80,
    rounding_denominator: int = 10**18,
    square_root_decimal_places: int = 12,
    authenticated_au2_sha256: str | None = None,
    authenticated_snapshot_sha256: str | None = None,
) -> ValidatedSkyrmionAU3BCertificate:
    """Build a profile-resolving finite-band/tail certificate."""

    split = _positive_fraction("band_split", band_split)
    step = _positive_fraction("frequency_step", frequency_step)
    subdivisions = _positive_integer("radial_subdivisions", radial_subdivisions)
    trig_terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    atanh_count = _positive_integer("atanh_terms", atanh_terms)
    rounding = _positive_integer("rounding_denominator", rounding_denominator)
    sqrt_places = _positive_integer(
        "square_root_decimal_places", square_root_decimal_places
    )
    if split < 1 or split % step != 0 or Fraction(1) % step != 0:
        raise ValueError("frequency step must divide one and a split at least one")
    au2_digest = _digest("authenticated_au2_sha256", authenticated_au2_sha256)
    snapshot_digest = _digest(
        "authenticated_snapshot_sha256", authenticated_snapshot_sha256
    )
    ledger = reconstruct_au2_spectral_ledger(au2_record)
    if ledger.tail_envelope is None:
        raise ValueError("AU.2 archive must contain a completed tail envelope")
    profile = reconstruct_au3b_profile(snapshot_record)
    if profile.certificate_id != ledger.endpoint.certificate_id:
        raise ValueError("AU.2 ledger and AU.3b profile identities differ")
    if au2_digest is not None and profile.canonical_au2_sha256 != au2_digest:
        raise ValueError("snapshot does not reference the authenticated AU.2 archive")
    radial_cells = _radial_integration_cells(
        profile,
        subdivisions=subdivisions,
        atanh_terms=atanh_count,
        rounding_denominator=rounding,
    )
    pi_interval = pi_machin_interval(terms=80)
    finite = [Fraction(0), Fraction(0), Fraction(0)]
    low_bare = (Fraction(2, 9), Fraction(13, 18), Fraction(25, 2))
    cell_count = int(split / step)
    for index in range(cell_count):
        momentum = RationalInterval(index * step, (index + 1) * step)
        form = _profile_resolved_form_factor_derivative_bounds(
            momentum,
            profile,
            radial_cells,
            pi_interval=pi_interval,
            trigonometric_terms=trig_terms,
            rounding_denominator=rounding,
        )
        if momentum.upper <= 1:
            bare = low_bare
        else:
            root_right = _sqrt_upper(
                momentum.upper,
                decimal_places=sqrt_places,
            )
            inverse_root_left = _sqrt_upper(
                Fraction(1, momentum.lower),
                decimal_places=sqrt_places,
            )
            bare = (
                momentum.upper * root_right / 6,
                Fraction(81, 480) * root_right,
                Fraction(21, 48) * inverse_root_left,
            )
        positive = (
            bare[0] * form[0],
            bare[1] * form[0] + bare[0] * form[1],
            bare[2] * form[0] + 2 * bare[1] * form[1] + bare[0] * form[2],
        )
        pi_upper = Fraction(22, 7)
        negative = (
            positive[0],
            pi_upper * positive[0] + positive[1],
            positive[2]
            + 2 * pi_upper * positive[1]
            + pi_upper**2 * positive[0],
        )
        for order in range(3):
            finite[order] += step * (
                positive[order] ** 2 + negative[order] ** 2
            )
    joined = build_validated_skyrmion_spectral_ledger(
        ledger.endpoint,
        a_third_derivative_l1=ledger.a_third_derivative_l1,
        w_third_derivative_l1=ledger.w_third_derivative_l1,
        tail_start=split,
        physical_radius=ledger.tail_envelope.physical_radius,
    )
    if joined.tail_envelope is None:
        raise AssertionError("completed AU.2 ledger did not generate a tail")
    radius = joined.tail_envelope.physical_radius.enclosure.lower
    finite_physical = tuple(
        finite[order] * radius ** (2 * order - 4) for order in range(3)
    )
    tail = tuple(
        value.upper
        for value in joined.tail_envelope.squared_physical_h2_tail_bounds
    )
    global_squared = tuple(
        finite_physical[order] + tail[order] for order in range(3)
    )
    q_norms = tuple(
        _sqrt_upper(value, decimal_places=sqrt_places)
        for value in global_squared
    )
    pi_upper = Fraction(22, 7)
    jump_l1 = _sqrt_upper(
        2 * pi_upper * q_norms[0] * q_norms[1],
        decimal_places=sqrt_places,
    )
    jump_first = _sqrt_upper(
        2 * pi_upper * q_norms[1] * q_norms[2],
        decimal_places=sqrt_places,
    )
    return ValidatedSkyrmionAU3BCertificate(
        certificate_id=profile.certificate_id,
        authenticated_au2_sha256=au2_digest,
        authenticated_snapshot_sha256=snapshot_digest,
        band_split=split,
        frequency_step=step,
        radial_subdivisions=subdivisions,
        finite_band_squared_h2_bounds=finite_physical,  # type: ignore[arg-type]
        tail_squared_h2_bounds=tail,  # type: ignore[arg-type]
        global_squared_h2_bounds=global_squared,  # type: ignore[arg-type]
        q_norm_upper_bounds=q_norms,  # type: ignore[arg-type]
        jump_l1_upper_bound=jump_l1,
        jump_first_moment_upper_bound=jump_first,
    )


@dataclass(frozen=True)
class ValidatedSkyrmionAU3BSharpCertificate:
    certificate_id: str
    authenticated_au2_sha256: str | None
    authenticated_snapshot_sha256: str | None
    band_split: Fraction
    frequency_step: Fraction
    radial_cell_count: int
    physical_radius_lower_bound: Fraction
    physical_radius_upper_bound: Fraction
    physical_radius_provenance: str
    finite_band_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    tail_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    global_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    q_norm_upper_bounds: tuple[Fraction, Fraction, Fraction]
    jump_l1_upper_bound: Fraction
    jump_first_moment_upper_bound: Fraction
    parallel_frequency_workers: int = 1

    def to_record(self) -> dict[str, object]:
        external_digest_claims = (
            self.authenticated_au2_sha256 is not None
            and self.authenticated_snapshot_sha256 is not None
        )

        def exact(values: tuple[Fraction, Fraction, Fraction]) -> tuple[str, ...]:
            return tuple(_fraction_text(value) for value in values)

        return {
            "goal": "Validated Skyrmion AU.3b Sharp Radial Certificate",
            "result_type": "sharp_newton_profile_directed_frequency_upper_bounds",
            "au3b_status": (
                "conditional_sharp_radial_upper_certificate_with_external_digests"
                if external_digest_claims
                else "conditional_sharp_radial_upper_certificate"
            ),
            "certificate_id": self.certificate_id,
            "authenticated_au2_sha256": self.authenticated_au2_sha256,
            "authenticated_snapshot_sha256": self.authenticated_snapshot_sha256,
            "band_split": _fraction_text(self.band_split),
            "frequency_step": _fraction_text(self.frequency_step),
            "radial_cell_count": self.radial_cell_count,
            "parallel_frequency_workers": self.parallel_frequency_workers,
            "physical_radius_interval_exact": {
                "lower": _fraction_text(self.physical_radius_lower_bound),
                "upper": _fraction_text(self.physical_radius_upper_bound),
            },
            "physical_radius_provenance": self.physical_radius_provenance,
            "zero_mode_form_factor_lower_bound_exact": "1",
            "moment_convention": (
                "signed scalar factor q_Sky=sqrt(j_0) H_Sky in Killing frequency"
            ),
            "finite_band_squared_h2_bounds_exact": exact(
                self.finite_band_squared_h2_bounds
            ),
            "tail_squared_h2_bounds_exact": exact(self.tail_squared_h2_bounds),
            "global_squared_h2_bounds_exact": exact(self.global_squared_h2_bounds),
            "q_norm_upper_bounds_exact": exact(self.q_norm_upper_bounds),
            "q_norm_upper_bounds": tuple(
                _upper_float(value) for value in self.q_norm_upper_bounds
            ),
            "jump_l1_upper_bound_exact": _fraction_text(self.jump_l1_upper_bound),
            "jump_l1_upper_bound": _upper_float(self.jump_l1_upper_bound),
            "jump_first_moment_upper_bound_exact": _fraction_text(
                self.jump_first_moment_upper_bound
            ),
            "jump_first_moment_upper_bound": _upper_float(
                self.jump_first_moment_upper_bound
            ),
            "claim_boundary": (
                "When the supplied measure is produced by the authenticated "
                "sharp replay, the finite band retains its endpoint-corrected "
                "spline, local Newton radii, and origin-regular inertia data in "
                "an anchored normalized-measure identity. The reusable builder "
                "itself proves only structural measure consistency. The joined "
                "tail still uses the conservative AU.2 derivative ledger, and "
                "the bare spectral jet still uses absolute-value product bounds."
                " Digest strings are caller-supplied claims; only an entry-point "
                "audit that rehashes the inputs may label the result authenticated."
            ),
        }


def _sharp_radial_integration_cells(
    measure: ValidatedSkyrmionSharpMeasure,
    *,
    atanh_terms: int,
    rounding_denominator: int,
) -> tuple[_RadialIntegrationCell, ...]:
    root_curvature = _perfect_rational_square_root(measure.curvature)
    result = []
    for cell in measure.positive_radius_cells:
        left_z = root_curvature * cell.radius.lower
        right_z = root_curvature * cell.radius.upper
        if left_z <= 0 or right_z >= 1:
            raise ValueError("sharp radial cell leaves the static patch")
        y = _round_interval(
            RationalInterval(
                atanh_fraction_interval(left_z, terms=atanh_terms).lower,
                atanh_fraction_interval(right_z, terms=atanh_terms).upper,
            ),
            rounding_denominator,
        )
        z = RationalInterval(left_z, right_z)
        tanh_squared = RationalInterval.point(measure.curvature) * (
            cell.radius.power(2)
        )
        result.append(
            _RadialIntegrationCell(
                radius=cell.radius,
                optical_radius=y,
                y_over_tanh=_round_interval(y / z, rounding_denominator),
                inverse_tanh_squared=_round_interval(
                    RationalInterval.point(1) / tanh_squared,
                    rounding_denominator,
                ),
                density=cell.density,
            )
        )
    return tuple(result)


def _sharp_form_factor_derivative_bounds(
    momentum: RationalInterval,
    measure: ValidatedSkyrmionSharpMeasure,
    radial_cells: tuple[_RadialIntegrationCell, ...],
    *,
    origin_cutoff: Fraction,
    pi_interval: RationalInterval,
    trigonometric_terms: int,
    rounding_denominator: int,
) -> tuple[Fraction, Fraction, Fraction]:
    kernel_cells = tuple(
        _kernel_derivative_intervals(
            momentum,
            radial,
            pi_interval=pi_interval,
            trigonometric_terms=trigonometric_terms,
            rounding_denominator=rounding_denominator,
        )
        for radial in radial_cells
    )
    root_curvature = _perfect_rational_square_root(measure.curvature)
    origin_y = atanh_fraction_interval(
        root_curvature * origin_cutoff,
        terms=80,
    ).upper
    origin_c = 1 / (1 - measure.curvature * origin_cutoff**2)
    origin_d = Fraction(4, 3) + origin_y**2 / 3
    origin_bounds = (
        origin_c * (1 + Fraction(2, 3) * momentum.upper**2),
        origin_c * origin_d * momentum.upper,
        origin_c * origin_d,
    )
    direct = [RationalInterval.point(0) for _ in range(3)]
    for radial, kernels in zip(radial_cells, kernel_cells):
        for order in range(3):
            direct[order] += (radial.density * kernels[order]).scale(
                radial.radius.width
            )
    for origin in measure.origin_cells:
        for order in range(3):
            direct[order] += (
                origin.density * _symmetric(origin_bounds[order])
            ).scale(origin.radius.width)

    expectation = []
    for order in range(3):
        anchor = direct[order].midpoint / measure.inertia.midpoint
        residual = RationalInterval.point(0)
        anchor_interval = RationalInterval.point(anchor)
        for radial, kernels in zip(radial_cells, kernel_cells):
            residual += (
                radial.density * (kernels[order] - anchor_interval)
            ).scale(radial.radius.width)
        for origin in measure.origin_cells:
            residual += (
                origin.density
                * (_symmetric(origin_bounds[order]) - anchor_interval)
            ).scale(origin.radius.width)
        expectation.append(
            _round_interval(
                anchor_interval + residual / measure.inertia,
                rounding_denominator,
            ).scale(3)
        )

    denominator = RationalInterval.point(1) + momentum.power(2)
    form = (
        expectation[0] / denominator,
        expectation[1] / denominator
        - (momentum * expectation[0]).scale(2) / denominator.power(2),
        expectation[2] / denominator
        - (momentum * expectation[1]).scale(4) / denominator.power(2)
        + (
            (momentum.power(2).scale(6) - RationalInterval.point(2))
            * expectation[0]
        )
        / denominator.power(3),
    )
    return tuple(_absolute_upper(value) for value in form)  # type: ignore[return-value]


_SHARP_FREQUENCY_WORKER_STATE: tuple[object, ...] | None = None


def _sharp_frequency_cell_contribution(
    index: int,
    *,
    step: Fraction,
    measure: ValidatedSkyrmionSharpMeasure,
    radial_cells: tuple[_RadialIntegrationCell, ...],
    pi_interval: RationalInterval,
    trigonometric_terms: int,
    rounding_denominator: int,
    square_root_decimal_places: int,
) -> tuple[Fraction, Fraction, Fraction]:
    momentum = RationalInterval(index * step, (index + 1) * step)
    form = _sharp_form_factor_derivative_bounds(
        momentum,
        measure,
        radial_cells,
        origin_cutoff=measure.origin_cutoff,
        pi_interval=pi_interval,
        trigonometric_terms=trigonometric_terms,
        rounding_denominator=rounding_denominator,
    )
    if momentum.upper <= 1:
        bare = (Fraction(2, 9), Fraction(13, 18), Fraction(25, 2))
    else:
        root_right = _sqrt_upper(
            momentum.upper,
            decimal_places=square_root_decimal_places,
        )
        inverse_root_left = _sqrt_upper(
            Fraction(1, momentum.lower),
            decimal_places=square_root_decimal_places,
        )
        bare = (
            momentum.upper * root_right / 6,
            Fraction(81, 480) * root_right,
            Fraction(21, 48) * inverse_root_left,
        )
    positive = (
        bare[0] * form[0],
        bare[1] * form[0] + bare[0] * form[1],
        bare[2] * form[0] + 2 * bare[1] * form[1] + bare[0] * form[2],
    )
    pi_upper = Fraction(22, 7)
    negative = (
        positive[0],
        pi_upper * positive[0] + positive[1],
        positive[2]
        + 2 * pi_upper * positive[1]
        + pi_upper**2 * positive[0],
    )
    return tuple(
        step * (positive[order] ** 2 + negative[order] ** 2)
        for order in range(3)
    )  # type: ignore[return-value]


def _initialize_sharp_frequency_worker(*state: object) -> None:
    global _SHARP_FREQUENCY_WORKER_STATE
    _SHARP_FREQUENCY_WORKER_STATE = state


def _sharp_frequency_worker(index: int) -> tuple[Fraction, Fraction, Fraction]:
    if _SHARP_FREQUENCY_WORKER_STATE is None:
        raise RuntimeError("sharp frequency worker was not initialized")
    (
        step,
        measure,
        radial_cells,
        pi_interval,
        trigonometric_terms,
        rounding_denominator,
        square_root_decimal_places,
    ) = _SHARP_FREQUENCY_WORKER_STATE
    return _sharp_frequency_cell_contribution(
        index,
        step=step,  # type: ignore[arg-type]
        measure=measure,  # type: ignore[arg-type]
        radial_cells=radial_cells,  # type: ignore[arg-type]
        pi_interval=pi_interval,  # type: ignore[arg-type]
        trigonometric_terms=trigonometric_terms,  # type: ignore[arg-type]
        rounding_denominator=rounding_denominator,  # type: ignore[arg-type]
        square_root_decimal_places=square_root_decimal_places,  # type: ignore[arg-type]
    )


def build_validated_skyrmion_au3b_sharp_certificate(
    au2_record: Mapping[str, object],
    measure: ValidatedSkyrmionSharpMeasure,
    *,
    band_split: int | Fraction = 128,
    frequency_step: int | Fraction = 1,
    trigonometric_terms: int = 24,
    atanh_terms: int = 80,
    rounding_denominator: int = 10**18,
    square_root_decimal_places: int = 12,
    parallel_frequency_workers: int = 1,
    authenticated_au2_sha256: str | None = None,
    authenticated_snapshot_sha256: str | None = None,
) -> ValidatedSkyrmionAU3BSharpCertificate:
    """Join a sharp Newton-profile finite band to the authenticated AU.2 tail."""

    split = _positive_fraction("band_split", band_split)
    step = _positive_fraction("frequency_step", frequency_step)
    trig_terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    atanh_count = _positive_integer("atanh_terms", atanh_terms)
    rounding = _positive_integer("rounding_denominator", rounding_denominator)
    sqrt_places = _positive_integer(
        "square_root_decimal_places", square_root_decimal_places
    )
    workers = _positive_integer(
        "parallel_frequency_workers", parallel_frequency_workers
    )
    if split < 1 or split % step != 0 or Fraction(1) % step != 0:
        raise ValueError("frequency step must divide one and a split at least one")
    au2_digest = _digest("authenticated_au2_sha256", authenticated_au2_sha256)
    snapshot_digest = _digest(
        "authenticated_snapshot_sha256", authenticated_snapshot_sha256
    )
    if (au2_digest is None) != (snapshot_digest is None):
        raise ValueError("AU.2 and snapshot digest claims must be supplied together")
    validate_validated_skyrmion_sharp_measure(measure)
    ledger = reconstruct_au2_spectral_ledger(au2_record)
    if ledger.tail_envelope is None:
        raise ValueError("AU.2 archive must contain a completed tail envelope")
    if measure.certificate_id != ledger.endpoint.certificate_id:
        raise ValueError("AU.2 ledger and sharp measure identities differ")
    if ledger.endpoint.origin_cutoff is None:
        raise ValueError("AU.2 endpoint does not declare an origin cutoff")
    if (
        measure.curvature != ledger.endpoint.curvature
        or measure.origin_cutoff != ledger.endpoint.origin_cutoff
        or measure.wall_radius != ledger.endpoint.wall_radius
    ):
        raise ValueError("AU.2 ledger and sharp measure geometries differ")
    radial_cells = _sharp_radial_integration_cells(
        measure,
        atanh_terms=atanh_count,
        rounding_denominator=rounding,
    )
    pi_interval = pi_machin_interval(terms=80)
    finite = [Fraction(0), Fraction(0), Fraction(0)]
    cell_count = int(split / step)
    worker_state = (
        step,
        measure,
        radial_cells,
        pi_interval,
        trig_terms,
        rounding,
        sqrt_places,
    )
    if workers == 1:
        contributions = (
            _sharp_frequency_cell_contribution(
                index,
                step=step,
                measure=measure,
                radial_cells=radial_cells,
                pi_interval=pi_interval,
                trigonometric_terms=trig_terms,
                rounding_denominator=rounding,
                square_root_decimal_places=sqrt_places,
            )
            for index in range(cell_count)
        )
        for contribution in contributions:
            for order in range(3):
                finite[order] += contribution[order]
    else:
        with ProcessPoolExecutor(
            max_workers=workers,
            mp_context=get_context("spawn"),
            initializer=_initialize_sharp_frequency_worker,
            initargs=worker_state,
        ) as executor:
            for contribution in executor.map(
                _sharp_frequency_worker,
                range(cell_count),
            ):
                for order in range(3):
                    finite[order] += contribution[order]
    joined = build_validated_skyrmion_spectral_ledger(
        ledger.endpoint,
        a_third_derivative_l1=ledger.a_third_derivative_l1,
        w_third_derivative_l1=ledger.w_third_derivative_l1,
        tail_start=split,
        physical_radius=ledger.tail_envelope.physical_radius,
    )
    if joined.tail_envelope is None:
        raise AssertionError("completed AU.2 ledger did not generate a tail")
    radius = joined.tail_envelope.physical_radius.enclosure.lower
    radius_upper = joined.tail_envelope.physical_radius.enclosure.upper
    finite_physical = tuple(
        finite[order] * radius ** (2 * order - 4) for order in range(3)
    )
    tail = tuple(
        value.upper
        for value in joined.tail_envelope.squared_physical_h2_tail_bounds
    )
    global_squared = tuple(
        finite_physical[order] + tail[order] for order in range(3)
    )
    q_norms = tuple(
        _sqrt_upper(value, decimal_places=sqrt_places)
        for value in global_squared
    )
    pi_upper = Fraction(22, 7)
    jump_l1 = _sqrt_upper(
        2 * pi_upper * q_norms[0] * q_norms[1],
        decimal_places=sqrt_places,
    )
    jump_first = _sqrt_upper(
        2 * pi_upper * q_norms[1] * q_norms[2],
        decimal_places=sqrt_places,
    )
    return ValidatedSkyrmionAU3BSharpCertificate(
        certificate_id=measure.certificate_id,
        authenticated_au2_sha256=au2_digest,
        authenticated_snapshot_sha256=snapshot_digest,
        band_split=split,
        frequency_step=step,
        radial_cell_count=(
            len(measure.origin_cells) + len(measure.positive_radius_cells)
        ),
        physical_radius_lower_bound=radius,
        physical_radius_upper_bound=radius_upper,
        physical_radius_provenance=(
            joined.tail_envelope.physical_radius.provenance
        ),
        finite_band_squared_h2_bounds=finite_physical,  # type: ignore[arg-type]
        tail_squared_h2_bounds=tail,  # type: ignore[arg-type]
        global_squared_h2_bounds=global_squared,  # type: ignore[arg-type]
        q_norm_upper_bounds=q_norms,  # type: ignore[arg-type]
        jump_l1_upper_bound=jump_l1,
        jump_first_moment_upper_bound=jump_first,
        parallel_frequency_workers=workers,
    )
