"""Exact-rational global Sobolev bounds for the signed Skyrmion bath.

AU.2 supplies endpoint jets, six third-derivative ``L1`` bounds, and a
boundary-aware tail envelope for the exact continuum form factor.  This module
closes the remaining *finiteness* part of AU.3 without pretending that the
result is numerically sharp.  Positivity of the normalized inertia measure
gives profile-uniform kernel bounds on a rational finite-frequency mesh; the
AU.2 ``p^-5`` theorem encloses the complement.  The joined certificate gives
rigorous global upper bounds for ``Q0,Q1,Q2,G,M1``.

The low-band estimate deliberately discards Fourier cancellation.  It is a
proof-quality fallback and a conditioning diagnostic, not a substitute for
the sharper directed finite-frequency quadrature still needed for a useful
physical coupling window.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from math import inf, isqrt, nextafter
from typing import Mapping

from .validated_interval import RationalInterval
from .validated_skyrmion_spectral_ledger import (
    ValidatedSkyrmionDerivativeNormUpperBound,
    ValidatedSkyrmionSpectralInput,
    ValidatedSkyrmionSpectralLedger,
    build_validated_skyrmion_spectral_ledger,
    validate_skyrmion_spectral_endpoint_ledger,
)


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _authentication_digest(value: str | None) -> str | None:
    if value is None:
        return None
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("authenticated_input_sha256 must be a lowercase SHA256")
    return value


def _sqrt_upper(value: Fraction, *, decimal_places: int = 12) -> Fraction:
    """Return a terminating decimal rational no smaller than ``sqrt(value)``."""

    if value < 0:
        raise ValueError("square-root input must be nonnegative")
    places = _positive_integer("decimal_places", decimal_places)
    scale = 10**places
    scaled_numerator = value.numerator * scale**2
    root = isqrt(scaled_numerator // value.denominator)
    if root * root * value.denominator < scaled_numerator:
        root += 1
    return Fraction(root, scale)


def _upper_float(value: Fraction) -> float:
    rendered = float(value)
    if Fraction.from_float(rendered) < value:
        rendered = nextafter(rendered, inf)
    return rendered


def _integer_text_unbounded(value: int) -> str:
    """Render an integer without depending on the interpreter digit ceiling."""

    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    remaining = abs(value)
    width = 1_000
    base = 10**width
    chunks: list[int] = []
    while remaining:
        remaining, chunk = divmod(remaining, base)
        chunks.append(chunk)
    head = str(chunks[-1])
    tail = "".join(str(chunk).zfill(width) for chunk in reversed(chunks[:-1]))
    return sign + head + tail


def _fraction_text(value: Fraction) -> str:
    numerator = _integer_text_unbounded(value.numerator)
    if value.denominator == 1:
        return numerator
    return numerator + "/" + _integer_text_unbounded(value.denominator)


def _interval_record(value: RationalInterval) -> dict[str, str]:
    return {
        "lower": _fraction_text(value.lower),
        "upper": _fraction_text(value.upper),
        "width": _fraction_text(value.width),
    }


def _parse_unbounded_integer(value: str) -> int:
    """Parse a decimal integer without Python's long-string safety ceiling."""

    if not isinstance(value, str) or not value:
        raise ValueError("integer text must be nonempty")
    sign = -1 if value.startswith("-") else 1
    digits = value[1:] if value[:1] in {"-", "+"} else value
    if not digits or not digits.isdecimal():
        raise ValueError("invalid integer text")
    result = 0
    width = 1_000
    for start in range(0, len(digits), width):
        chunk = digits[start : start + width]
        result = result * 10 ** len(chunk) + int(chunk)
    return sign * result


def exact_fraction_from_text(value: str) -> Fraction:
    """Parse an archived exact rational, including endpoints with many digits."""

    if not isinstance(value, str) or not value:
        raise ValueError("fraction text must be nonempty")
    pieces = value.split("/")
    if len(pieces) == 1:
        return Fraction(_parse_unbounded_integer(pieces[0]))
    if len(pieces) != 2:
        raise ValueError("invalid fraction text")
    numerator = _parse_unbounded_integer(pieces[0])
    denominator = _parse_unbounded_integer(pieces[1])
    if denominator == 0:
        raise ZeroDivisionError("fraction denominator cannot vanish")
    return Fraction(numerator, denominator)


def _archived_interval(value: object) -> RationalInterval:
    if not isinstance(value, Mapping):
        raise TypeError("archived interval must be a mapping")
    lower = value.get("lower")
    upper = value.get("upper")
    if not isinstance(lower, str) or not isinstance(upper, str):
        raise TypeError("archived interval endpoints must be strings")
    interval = RationalInterval(
        exact_fraction_from_text(lower),
        exact_fraction_from_text(upper),
    )
    width = value.get("width")
    if isinstance(width, str) and exact_fraction_from_text(width) != interval.width:
        raise ValueError("archived interval width is inconsistent")
    return interval


def _optional_fraction(value: object) -> Fraction | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("optional archived fraction must be a string or null")
    return exact_fraction_from_text(value)


def reconstruct_au2_spectral_ledger(
    record: Mapping[str, object],
) -> ValidatedSkyrmionSpectralLedger:
    """Recompute and verify an AU.2 ledger serialized in an exact archive.

    The endpoint and tail formulas are recomputed rather than trusted from the
    JSON payload.  Equality with the archived exact strings is then required.
    """

    endpoint_record = record.get("endpoint")
    derivative_record = record.get("derivative_norm_bounds")
    tail_record = record.get("tail_envelope")
    if not isinstance(endpoint_record, Mapping):
        raise TypeError("AU.2 record is missing its endpoint mapping")
    if not isinstance(derivative_record, Mapping):
        raise TypeError("AU.2 record is missing derivative norm mappings")
    if not isinstance(tail_record, Mapping):
        raise ValueError("AU.2 record must contain a completed tail envelope")

    certificate_id = endpoint_record.get("certificate_id")
    conclusion_scope = endpoint_record.get("conclusion_scope")
    if not isinstance(certificate_id, str) or not certificate_id:
        raise ValueError("AU.2 endpoint certificate id is missing")
    if not isinstance(conclusion_scope, str) or not conclusion_scope:
        raise ValueError("AU.2 endpoint conclusion scope is missing")
    inertia_provenance = endpoint_record.get("inertia_provenance")
    wall_provenance = endpoint_record.get("wall_slope_provenance")
    if not isinstance(inertia_provenance, str) or not inertia_provenance:
        raise ValueError("AU.2 inertia provenance is missing")
    if not isinstance(wall_provenance, str) or not wall_provenance:
        raise ValueError("AU.2 wall-slope provenance is missing")

    endpoint = validate_skyrmion_spectral_endpoint_ledger(
        curvature=exact_fraction_from_text(str(endpoint_record["curvature"])),
        wall_radius=exact_fraction_from_text(str(endpoint_record["wall_radius"])),
        inertia=ValidatedSkyrmionSpectralInput(
            _archived_interval(endpoint_record["inertia"]),
            inertia_provenance,
            certificate_id,
        ),
        wall_slope=ValidatedSkyrmionSpectralInput(
            _archived_interval(endpoint_record["wall_slope"]),
            wall_provenance,
            certificate_id,
        ),
    )
    endpoint = replace(
        endpoint,
        conclusion_scope=conclusion_scope,
        newton_radius=_optional_fraction(endpoint_record.get("newton_radius")),
        omega=_optional_fraction(endpoint_record.get("omega")),
        origin_cutoff=_optional_fraction(endpoint_record.get("origin_cutoff")),
    )

    families: dict[str, tuple[ValidatedSkyrmionDerivativeNormUpperBound, ...]] = {}
    for family in ("A", "W"):
        parsed = []
        for order in range(3):
            item = derivative_record.get(f"M_{order}^{family}")
            if not isinstance(item, Mapping):
                raise ValueError("AU.2 record must contain all six derivative bounds")
            provenance = item.get("provenance")
            item_certificate = item.get("certificate_id")
            upper = item.get("upper_bound")
            if not isinstance(provenance, str) or not provenance:
                raise ValueError("derivative-bound provenance is missing")
            if item_certificate != certificate_id:
                raise ValueError("derivative bound does not match the endpoint")
            if not isinstance(upper, str):
                raise TypeError("derivative upper bound must be an exact string")
            parsed.append(
                ValidatedSkyrmionDerivativeNormUpperBound(
                    exact_fraction_from_text(upper),
                    provenance,
                    certificate_id,
                )
            )
        families[family] = tuple(parsed)

    radius_record = tail_record.get("physical_radius")
    radius_provenance = tail_record.get("physical_radius_provenance")
    tail_start = tail_record.get("tail_start")
    if not isinstance(radius_provenance, str) or not radius_provenance:
        raise ValueError("physical-radius provenance is missing")
    if not isinstance(tail_start, str):
        raise TypeError("tail start must be an exact string")
    ledger = build_validated_skyrmion_spectral_ledger(
        endpoint,
        a_third_derivative_l1=families["A"],  # type: ignore[arg-type]
        w_third_derivative_l1=families["W"],  # type: ignore[arg-type]
        tail_start=exact_fraction_from_text(tail_start),
        physical_radius=ValidatedSkyrmionSpectralInput(
            _archived_interval(radius_record),
            radius_provenance,
            "physical-scale:" + certificate_id,
        ),
    )
    for name in (
        "root_curvature",
        "radial_horizon_ratio",
        "horizon_margin",
        "optical_wall",
        "wall_slope_magnitude",
        "form_factor_prefactor",
        "wall_weight_second_derivative",
        "wall_a_second_derivative",
        "leading_form_factor_tail_amplitude",
    ):
        if getattr(endpoint, name) != _archived_interval(endpoint_record[name]):
            raise ValueError(f"archived AU.2 endpoint mismatch in {name}")
    generated_tail = ledger.tail_envelope
    if generated_tail is None:
        raise AssertionError("completed AU.2 inputs did not generate a tail")

    def archived_intervals(name: str) -> tuple[RationalInterval, ...]:
        values = tail_record.get(name)
        if not isinstance(values, (list, tuple)):
            raise TypeError(f"archived tail field {name} must be a sequence")
        return tuple(_archived_interval(value) for value in values)

    tail_checks = {
        "b_transform_bounds": generated_tail.b_transform_bounds,
        "d_transform_bounds": generated_tail.d_transform_bounds,
        "numerator_derivative_coefficients": (
            generated_tail.numerator_derivative_coefficients
        ),
        "form_factor_derivative_coefficients": (
            generated_tail.form_factor_derivative_coefficients
        ),
        "positive_signed_factor_coefficients": (
            generated_tail.positive_signed_factor_coefficients
        ),
        "negative_signed_factor_coefficients": (
            generated_tail.negative_signed_factor_coefficients
        ),
        "squared_dimensionless_h2_tail_bounds": (
            generated_tail.squared_dimensionless_h2_tail_bounds
        ),
        "squared_physical_h2_tail_bounds": (
            generated_tail.squared_physical_h2_tail_bounds
        ),
    }
    for name, generated_values in tail_checks.items():
        if generated_values != archived_intervals(name):
            raise ValueError(f"archived AU.2 tail mismatch in {name}")
    physical_tail_start = tail_record.get("physical_tail_start")
    if not isinstance(physical_tail_start, str) or generated_tail.physical_tail_start != exact_fraction_from_text(physical_tail_start):
        raise ValueError("archived AU.2 physical tail start is inconsistent")
    return ledger


@dataclass(frozen=True)
class ValidatedSkyrmionAU3Certificate:
    """Conservative exact-rational global ``H2`` and time-moment certificate."""

    certificate_id: str
    authenticated_input_sha256: str | None
    physical_radius: Fraction
    band_split: Fraction
    frequency_step: Fraction
    frequency_cell_count: int
    optical_probability_constant: Fraction
    kernel_derivative_constant: Fraction
    positive_factor_derivative_bounds: tuple[Fraction, Fraction, Fraction]
    negative_factor_derivative_bounds: tuple[Fraction, Fraction, Fraction]
    finite_band_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    tail_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    global_squared_h2_bounds: tuple[Fraction, Fraction, Fraction]
    q_norm_upper_bounds: tuple[Fraction, Fraction, Fraction]
    jump_l1_upper_bound: Fraction
    jump_first_moment_upper_bound: Fraction
    stationary_residual_quadratic_coefficient: Fraction
    stationary_residual_quartic_time_coefficient: Fraction

    def to_record(self) -> dict[str, object]:
        def exact(values: tuple[Fraction, Fraction, Fraction]) -> tuple[str, ...]:
            return tuple(_fraction_text(value) for value in values)

        def decimal(values: tuple[Fraction, Fraction, Fraction]) -> tuple[float, ...]:
            return tuple(_upper_float(value) for value in values)

        authenticated = self.authenticated_input_sha256 is not None
        return {
            "goal": "Validated Skyrmion AU.3 Global Sobolev Certificate",
            "result_type": "exact_rational_conservative_global_sobolev_bounds",
            "au3_status": (
                "complete_directed_global_upper_certificate"
                if authenticated
                else "conditional_directed_global_upper_certificate"
            ),
            "sharp_finite_frequency_status": "open_directed_quadrature_for_useful_constants",
            "certificate_id": self.certificate_id,
            "authenticated_input_sha256": self.authenticated_input_sha256,
            "physical_radius": _fraction_text(self.physical_radius),
            "band_split": _fraction_text(self.band_split),
            "frequency_step": _fraction_text(self.frequency_step),
            "frequency_cell_count": self.frequency_cell_count,
            "optical_probability_constant_exact": _fraction_text(
                self.optical_probability_constant
            ),
            "kernel_derivative_constant_exact": _fraction_text(
                self.kernel_derivative_constant
            ),
            "positive_factor_derivative_bounds_exact": exact(
                self.positive_factor_derivative_bounds
            ),
            "negative_factor_derivative_bounds_exact": exact(
                self.negative_factor_derivative_bounds
            ),
            "finite_band_squared_h2_bounds_exact": exact(
                self.finite_band_squared_h2_bounds
            ),
            "tail_squared_h2_bounds_exact": exact(
                self.tail_squared_h2_bounds
            ),
            "global_squared_h2_bounds_exact": exact(
                self.global_squared_h2_bounds
            ),
            "q_norm_upper_bounds_exact": exact(self.q_norm_upper_bounds),
            "q_norm_upper_bounds": decimal(self.q_norm_upper_bounds),
            "jump_l1_upper_bound_exact": _fraction_text(self.jump_l1_upper_bound),
            "jump_l1_upper_bound": _upper_float(self.jump_l1_upper_bound),
            "jump_first_moment_upper_bound_exact": _fraction_text(
                self.jump_first_moment_upper_bound
            ),
            "jump_first_moment_upper_bound": _upper_float(
                self.jump_first_moment_upper_bound
            ),
            "stationary_residual_quadratic_coefficient_exact": _fraction_text(
                self.stationary_residual_quadratic_coefficient
            ),
            "stationary_residual_quartic_time_coefficient_exact": _fraction_text(
                self.stationary_residual_quartic_time_coefficient
            ),
            "proof_scope": (
                ("Authenticated " if authenticated else "Conditional ")
                + "positivity of the exact normalized inertia measure and exact "
                "endpoint geometry give uniform kernel bounds on every "
                "rational finite-frequency cell. Exact upper sums bound that "
                "band, and the AU.2 p^-5 envelope recomputed at the same join "
                "bounds the complement. The joined values rigorously "
                "upper-bound global Q0,Q1,Q2 and the Sobolev G,M1 constants."
            ),
            "claim_boundary": (
                "The finite-band proof discards profile-specific oscillatory "
                "cancellation and is not a sharp interval evaluation of the "
                "certified profile. It certifies finite ULE inputs, but not a "
                "useful coupling window, the exact reduced dynamics, switching "
                "from one action, band projection, stress, lifetime, or "
                "backreaction."
            ),
        }


def build_validated_skyrmion_au3_certificate(
    ledger: ValidatedSkyrmionSpectralLedger,
    *,
    band_split: int | Fraction = 128,
    frequency_step: int | Fraction = Fraction(1, 4),
    square_root_decimal_places: int = 12,
    authenticated_input_sha256: str | None = None,
) -> ValidatedSkyrmionAU3Certificate:
    """Join an exact low-band enclosure to a completed AU.2 tail certificate."""

    if not isinstance(ledger, ValidatedSkyrmionSpectralLedger):
        raise TypeError("ledger must be a ValidatedSkyrmionSpectralLedger")
    places = _positive_integer(
        "square_root_decimal_places", square_root_decimal_places
    )
    authentication = _authentication_digest(authenticated_input_sha256)
    tail = ledger.tail_envelope
    if tail is None or ledger.missing_derivative_norms:
        raise ValueError("AU.3 requires a completed six-norm AU.2 tail ledger")
    split = Fraction(band_split)
    step = Fraction(frequency_step)
    if split < 1:
        raise ValueError("band_split must be at least one")
    if step <= 0 or step > 1:
        raise ValueError("frequency_step must lie in (0,1]")
    if split % step != 0 or Fraction(1) % step != 0:
        raise ValueError("frequency_step must divide both one and band_split")
    radius_interval = tail.physical_radius.enclosure
    if radius_interval.width != 0 or radius_interval.lower <= 0:
        raise ValueError("physical radius must be a strictly positive point interval")
    radius = radius_interval.lower
    endpoint = ledger.endpoint
    optical_probability = 1 / endpoint.horizon_margin.lower
    wall = endpoint.optical_wall.upper
    kernel_derivative = Fraction(4, 3) + wall**2 / 3
    pi_upper = Fraction(22, 7)
    low_bare = (Fraction(2, 9), Fraction(13, 18), Fraction(25, 2))
    finite_dimensionless = [Fraction(0), Fraction(0), Fraction(0)]
    positive_maxima = [Fraction(0), Fraction(0), Fraction(0)]
    negative_maxima = [Fraction(0), Fraction(0), Fraction(0)]
    cell_count = int(split / step)
    for index in range(cell_count):
        left = index * step
        right = left + step
        denominator = 1 + left**2
        b0 = optical_probability * (1 + Fraction(2, 3) * right**2)
        b1 = optical_probability * kernel_derivative * right
        b2 = optical_probability * kernel_derivative
        h0 = 3 * b0 / denominator
        h1 = 3 * (
            b1 / denominator + 2 * right * b0 / denominator**2
        )
        h2 = 3 * (
            b2 / denominator
            + 4 * right * b1 / denominator**2
            + (6 * right**2 + 2) * b0 / denominator**3
        )
        if right <= 1:
            bare = low_bare
        else:
            root_right = _sqrt_upper(right, decimal_places=places)
            inverse_root_left = _sqrt_upper(
                Fraction(1, left), decimal_places=places
            )
            bare = (
                right * root_right / 6,
                Fraction(81, 480) * root_right,
                Fraction(21, 48) * inverse_root_left,
            )
        positive = (
            bare[0] * h0,
            bare[1] * h0 + bare[0] * h1,
            bare[2] * h0 + 2 * bare[1] * h1 + bare[0] * h2,
        )
        negative = (
            positive[0],
            pi_upper * positive[0] + positive[1],
            positive[2]
            + 2 * pi_upper * positive[1]
            + pi_upper**2 * positive[0],
        )
        for order in range(3):
            finite_dimensionless[order] += step * (
                positive[order] ** 2 + negative[order] ** 2
            )
            positive_maxima[order] = max(positive_maxima[order], positive[order])
            negative_maxima[order] = max(negative_maxima[order], negative[order])
    finite_physical = tuple(
        finite_dimensionless[order] * radius ** (2 * order - 4)
        for order in range(3)
    )
    joined_ledger = build_validated_skyrmion_spectral_ledger(
        endpoint,
        a_third_derivative_l1=ledger.a_third_derivative_l1,
        w_third_derivative_l1=ledger.w_third_derivative_l1,
        tail_start=split,
        physical_radius=tail.physical_radius,
    )
    joined_tail = joined_ledger.tail_envelope
    if joined_tail is None:
        raise AssertionError("completed derivative inputs did not generate a tail")
    tail_physical = tuple(
        value.upper for value in joined_tail.squared_physical_h2_tail_bounds
    )
    global_squared = tuple(
        finite_physical[order] + tail_physical[order] for order in range(3)
    )
    q_norms = tuple(
        _sqrt_upper(value, decimal_places=places) for value in global_squared
    )
    jump_l1 = _sqrt_upper(
        2 * pi_upper * q_norms[0] * q_norms[1],
        decimal_places=places,
    )
    jump_first = _sqrt_upper(
        2 * pi_upper * q_norms[1] * q_norms[2],
        decimal_places=places,
    )
    quadratic = 288 * jump_l1 * jump_first
    quartic = 2 * 144**2 * jump_l1**3 * jump_first
    return ValidatedSkyrmionAU3Certificate(
        certificate_id=endpoint.certificate_id,
        authenticated_input_sha256=authentication,
        physical_radius=radius,
        band_split=split,
        frequency_step=step,
        frequency_cell_count=cell_count,
        optical_probability_constant=optical_probability,
        kernel_derivative_constant=kernel_derivative,
        positive_factor_derivative_bounds=tuple(positive_maxima),  # type: ignore[arg-type]
        negative_factor_derivative_bounds=tuple(negative_maxima),  # type: ignore[arg-type]
        finite_band_squared_h2_bounds=finite_physical,  # type: ignore[arg-type]
        tail_squared_h2_bounds=tail_physical,  # type: ignore[arg-type]
        global_squared_h2_bounds=global_squared,  # type: ignore[arg-type]
        q_norm_upper_bounds=q_norms,  # type: ignore[arg-type]
        jump_l1_upper_bound=jump_l1,
        jump_first_moment_upper_bound=jump_first,
        stationary_residual_quadratic_coefficient=quadratic,
        stationary_residual_quartic_time_coefficient=quartic,
    )


def build_validated_skyrmion_au3_from_au2_record(
    record: Mapping[str, object],
    *,
    square_root_decimal_places: int = 12,
    authenticated_input_sha256: str | None = None,
) -> ValidatedSkyrmionAU3Certificate:
    """Verify AU.2 algebra and derive a conditional or authenticated result.

    Record consistency alone does not prove that the supplied inertia density
    is positive or that its norm bounds came from an AU.1 proof. Callers may
    provide ``authenticated_input_sha256`` only after verifying a trusted AU.2
    proof archive, as the repository audit script does.
    """

    return build_validated_skyrmion_au3_certificate(
        reconstruct_au2_spectral_ledger(record),
        square_root_decimal_places=square_root_decimal_places,
        authenticated_input_sha256=authenticated_input_sha256,
    )
