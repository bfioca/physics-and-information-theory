import json
import math
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_au3 import reconstruct_au2_spectral_ledger
from qgtoy.validated_skyrmion_au3b import (
    _RadialIntegrationCell,
    _kernel_derivative_intervals,
    _sinc_derivative_interval,
    build_validated_skyrmion_au3b_sharp_certificate,
)
from qgtoy.validated_interval import pi_machin_interval
from qgtoy.validated_skyrmion_spectral_ledger import (
    build_validated_skyrmion_spectral_ledger,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpInertiaCell,
    ValidatedSkyrmionSharpMeasure,
)


ROOT = Path(__file__).resolve().parents[1]
AU2_PATH = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"


def _cell(region: str, left: Fraction, right: Fraction) -> ValidatedSkyrmionSharpInertiaCell:
    radius = RationalInterval(left, right)
    density = RationalInterval(Fraction(1), Fraction(11, 10))
    return ValidatedSkyrmionSharpInertiaCell(
        region=region,
        source_cell_index=0,
        radius=radius,
        density=density,
        integral=density.scale(radius.width),
    )


def test_sharp_au3b_builder_returns_directed_conditional_certificate() -> None:
    au2 = json.loads(AU2_PATH.read_text(encoding="ascii"))
    au2_record = au2["exact_outputs"]["au2_global_derivative_norms_and_tail"][
        "spectral_ledger"
    ]
    ledger = reconstruct_au2_spectral_ledger(au2_record)
    origin = _cell("origin", Fraction(0), Fraction(1, 16))
    positive = _cell("positive_radius", Fraction(1, 16), Fraction(4))
    inertia = origin.integral + positive.integral
    measure = ValidatedSkyrmionSharpMeasure(
        certificate_id=ledger.endpoint.certificate_id,
        curvature=Fraction(1, 400),
        origin_cutoff=Fraction(1, 16),
        wall_radius=Fraction(4),
        origin_cells=(origin,),
        positive_radius_cells=(positive,),
        inertia=inertia,
        claim_boundary="synthetic algebra fixture",
    )

    certificate = build_validated_skyrmion_au3b_sharp_certificate(
        au2_record,
        measure,
        band_split=1,
        frequency_step=1,
        trigonometric_terms=12,
        atanh_terms=24,
        rounding_denominator=10**9,
        square_root_decimal_places=8,
    )
    record = certificate.to_record()

    assert record["au3b_status"] == "conditional_sharp_radial_upper_certificate"
    assert certificate.radial_cell_count == 2
    assert all(value > 0 for value in certificate.q_norm_upper_bounds)
    assert all(
        global_value == finite_value + tail_value
        for global_value, finite_value, tail_value in zip(
            certificate.global_squared_h2_bounds,
            certificate.finite_band_squared_h2_bounds,
            certificate.tail_squared_h2_bounds,
        )
    )
    parallel = build_validated_skyrmion_au3b_sharp_certificate(
        au2_record,
        measure,
        band_split=1,
        frequency_step=1,
        trigonometric_terms=12,
        atanh_terms=24,
        rounding_denominator=10**9,
        square_root_decimal_places=8,
        parallel_frequency_workers=2,
    )
    assert parallel.parallel_frequency_workers == 2
    assert parallel.finite_band_squared_h2_bounds == (
        certificate.finite_band_squared_h2_bounds
    )
    assert parallel.global_squared_h2_bounds == certificate.global_squared_h2_bounds
    assert parallel.q_norm_upper_bounds == certificate.q_norm_upper_bounds


def test_sharp_au3b_builder_rejects_inconsistent_measure_normalization() -> None:
    au2 = json.loads(AU2_PATH.read_text(encoding="ascii"))
    au2_record = au2["exact_outputs"]["au2_global_derivative_norms_and_tail"][
        "spectral_ledger"
    ]
    ledger = reconstruct_au2_spectral_ledger(au2_record)
    origin = _cell("origin", Fraction(0), Fraction(1, 16))
    positive = _cell("positive_radius", Fraction(1, 16), Fraction(4))
    measure = ValidatedSkyrmionSharpMeasure(
        certificate_id=ledger.endpoint.certificate_id,
        curvature=Fraction(1, 400),
        origin_cutoff=Fraction(1, 16),
        wall_radius=Fraction(4),
        origin_cells=(origin,),
        positive_radius_cells=(positive,),
        inertia=origin.integral + positive.integral,
        claim_boundary="synthetic algebra fixture",
    )

    try:
        build_validated_skyrmion_au3b_sharp_certificate(
            au2_record,
            replace(measure, inertia=RationalInterval.point(1000)),
            band_split=1,
        )
    except ValueError as error:
        assert "inertia does not match" in str(error)
    else:
        raise AssertionError("inconsistent sharp measure was accepted")


def test_sharp_au3b_builder_binds_measure_geometry_to_au2() -> None:
    au2 = json.loads(AU2_PATH.read_text(encoding="ascii"))
    au2_record = au2["exact_outputs"]["au2_global_derivative_norms_and_tail"][
        "spectral_ledger"
    ]
    ledger = reconstruct_au2_spectral_ledger(au2_record)
    origin = _cell("origin", Fraction(0), Fraction(1, 16))
    positive = _cell("positive_radius", Fraction(1, 16), Fraction(4))
    base_measure = ValidatedSkyrmionSharpMeasure(
        certificate_id=ledger.endpoint.certificate_id,
        curvature=Fraction(1, 400),
        origin_cutoff=Fraction(1, 16),
        wall_radius=Fraction(4),
        origin_cells=(origin,),
        positive_radius_cells=(positive,),
        inertia=origin.integral + positive.integral,
        claim_boundary="synthetic mismatched geometry",
    )
    alternate_origin = _cell("origin", Fraction(0), Fraction(1, 32))
    alternate_cutoff_positive = _cell(
        "positive_radius", Fraction(1, 32), Fraction(4)
    )
    alternate_wall_positive = _cell(
        "positive_radius", Fraction(1, 16), Fraction(3)
    )
    mismatched = (
        replace(base_measure, curvature=Fraction(1, 401)),
        replace(
            base_measure,
            origin_cutoff=Fraction(1, 32),
            origin_cells=(alternate_origin,),
            positive_radius_cells=(alternate_cutoff_positive,),
            inertia=alternate_origin.integral + alternate_cutoff_positive.integral,
        ),
        replace(
            base_measure,
            wall_radius=Fraction(3),
            positive_radius_cells=(alternate_wall_positive,),
            inertia=origin.integral + alternate_wall_positive.integral,
        ),
    )

    for measure in mismatched:
        try:
            build_validated_skyrmion_au3b_sharp_certificate(
                au2_record,
                measure,
                band_split=1,
            )
        except ValueError as error:
            assert "geometries differ" in str(error)
        else:
            raise AssertionError("mismatched sharp measure geometry was accepted")


def test_sharp_au3b_recomputes_tail_at_nontrivial_join() -> None:
    au2 = json.loads(AU2_PATH.read_text(encoding="ascii"))
    au2_record = au2["exact_outputs"]["au2_global_derivative_norms_and_tail"][
        "spectral_ledger"
    ]
    ledger = reconstruct_au2_spectral_ledger(au2_record)
    origin = _cell("origin", Fraction(0), Fraction(1, 16))
    positive = _cell("positive_radius", Fraction(1, 16), Fraction(4))
    measure = ValidatedSkyrmionSharpMeasure(
        certificate_id=ledger.endpoint.certificate_id,
        curvature=ledger.endpoint.curvature,
        origin_cutoff=ledger.endpoint.origin_cutoff,
        wall_radius=ledger.endpoint.wall_radius,
        origin_cells=(origin,),
        positive_radius_cells=(positive,),
        inertia=origin.integral + positive.integral,
        claim_boundary="synthetic tail-join fixture",
    )
    certificate = build_validated_skyrmion_au3b_sharp_certificate(
        au2_record,
        measure,
        band_split=2,
        trigonometric_terms=12,
        atanh_terms=24,
        rounding_denominator=10**9,
        square_root_decimal_places=8,
    )
    joined = build_validated_skyrmion_spectral_ledger(
        ledger.endpoint,
        a_third_derivative_l1=ledger.a_third_derivative_l1,
        w_third_derivative_l1=ledger.w_third_derivative_l1,
        tail_start=Fraction(2),
        physical_radius=ledger.tail_envelope.physical_radius,
    )
    expected = tuple(
        value.upper for value in joined.tail_envelope.squared_physical_h2_tail_bounds
    )
    archived = tuple(
        value.upper for value in ledger.tail_envelope.squared_physical_h2_tail_bounds
    )
    assert certificate.tail_squared_h2_bounds == expected
    assert certificate.tail_squared_h2_bounds != archived


def test_sharp_au3b_rejects_one_sided_digest_claim() -> None:
    au2 = json.loads(AU2_PATH.read_text(encoding="ascii"))
    au2_record = au2["exact_outputs"]["au2_global_derivative_norms_and_tail"][
        "spectral_ledger"
    ]
    ledger = reconstruct_au2_spectral_ledger(au2_record)
    origin = _cell("origin", Fraction(0), Fraction(1, 16))
    positive = _cell("positive_radius", Fraction(1, 16), Fraction(4))
    measure = ValidatedSkyrmionSharpMeasure(
        certificate_id=ledger.endpoint.certificate_id,
        curvature=ledger.endpoint.curvature,
        origin_cutoff=ledger.endpoint.origin_cutoff,
        wall_radius=ledger.endpoint.wall_radius,
        origin_cells=(origin,),
        positive_radius_cells=(positive,),
        inertia=origin.integral + positive.integral,
        claim_boundary="synthetic digest fixture",
    )
    try:
        build_validated_skyrmion_au3b_sharp_certificate(
            au2_record,
            measure,
            band_split=1,
            authenticated_au2_sha256="0" * 64,
        )
    except ValueError as error:
        assert "supplied together" in str(error)
    else:
        raise AssertionError("one-sided digest claim was accepted")


def _sinc_derivative(value: float, order: int) -> float:
    if value == 0.0:
        return (1.0, 0.0, -1.0 / 3.0)[order]
    if order == 0:
        return math.sin(value) / value
    if order == 1:
        return (value * math.cos(value) - math.sin(value)) / value**2
    return (
        (2.0 - value**2) * math.sin(value)
        - 2.0 * value * math.cos(value)
    ) / value**3


def test_sinc_derivative_intervals_contain_period_crossing_samples() -> None:
    pi_interval = pi_machin_interval(terms=80)
    arguments = (
        RationalInterval(Fraction(0), Fraction(1)),
        RationalInterval(Fraction(6), Fraction(13, 2)),
        RationalInterval(Fraction(3141), Fraction(3142)),
    )
    for argument in arguments:
        samples = (
            float(argument.lower),
            float(argument.midpoint),
            float(argument.upper),
        )
        for order in range(3):
            enclosure = _sinc_derivative_interval(
                argument,
                order,
                pi_interval=pi_interval,
                terms=24,
                rounding_denominator=10**15,
            )
            for sample in samples:
                value = _sinc_derivative(sample, order)
                assert float(enclosure.lower) <= value <= float(enclosure.upper)


def test_optical_kernel_derivative_intervals_contain_samples() -> None:
    momentum = RationalInterval(Fraction(31), Fraction(32))
    y = Fraction(1, 5)
    y_over_tanh = Fraction(6, 5)
    inverse_tanh_squared = Fraction(25)
    radial = _RadialIntegrationCell(
        radius=RationalInterval(Fraction(1), Fraction(1)),
        optical_radius=RationalInterval.point(y),
        y_over_tanh=RationalInterval.point(y_over_tanh),
        inverse_tanh_squared=RationalInterval.point(inverse_tanh_squared),
        density=RationalInterval.point(1),
    )
    enclosures = _kernel_derivative_intervals(
        momentum,
        radial,
        pi_interval=pi_machin_interval(terms=80),
        trigonometric_terms=24,
        rounding_denominator=10**15,
    )
    for p in map(float, (momentum.lower, momentum.midpoint, momentum.upper)):
        phase = p * float(y)
        sinc = tuple(_sinc_derivative(phase, order) for order in range(3))
        expected = (
            (float(y_over_tanh) * sinc[0] - math.cos(phase))
            * float(inverse_tanh_squared),
            (
                float(y * y_over_tanh) * sinc[1]
                + float(y) * math.sin(phase)
            )
            * float(inverse_tanh_squared),
            (
                float(y**2 * y_over_tanh) * sinc[2]
                + float(y**2) * math.cos(phase)
            )
            * float(inverse_tanh_squared),
        )
        for enclosure, value in zip(enclosures, expected):
            assert float(enclosure.lower) <= value <= float(enclosure.upper)
