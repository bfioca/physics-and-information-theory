from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_affine_master_kernel import (
    _FirstRadialJet,
    centrifugal_completed_master_source_generic,
    centrifugal_completed_stress_generic,
)
from qgtoy.static_patch_l2_response import (
    l2_center_regular_solution,
    l2_center_regular_solution_derivative,
)
from qgtoy.validated_centrifugal_adjoint_bulk_load import (
    ValidatedWeakMasterLoadCell,
    _center_regular_green_intervals,
    centrifugal_weak_master_load_affine_kernel,
    validated_bulk_load_on_trial_cell,
    validated_weak_adjoint_residual_cell,
)
from qgtoy.validated_centrifugal_response_residual import (
    RationalC1TrialCell,
    ValidatedConormalStrongCell,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial


def test_exact_weak_kernel_matches_strong_source_plus_boundary_derivative() -> None:
    values = {
        "radius": Fraction(7, 5),
        "metric_factor": Fraction(19, 20),
        "metric_factor_derivative": Fraction(-7, 1000),
        "inverse_patch_radius_squared": Fraction(1, 400),
        "sine_profile": Fraction(3, 5),
        "cosine_profile": Fraction(4, 5),
        "profile_derivative": Fraction(-2, 5),
        "profile_second_derivative": Fraction(1, 7),
        "pion_mass_squared": Fraction(6, 5),
        "gravitational_coupling": Fraction(3, 2),
    }
    fields = {
        "radial_field": Fraction(2, 13),
        "radial_field_derivative": Fraction(-3, 17),
        "radial_field_second_derivative": Fraction(11, 29),
        "tangential_field": Fraction(5, 19),
        "tangential_field_derivative": Fraction(7, 23),
    }
    weight = Fraction(13, 17)
    weight_derivative = Fraction(-5, 11)
    weak = centrifugal_weak_master_load_affine_kernel(
        **{key: value for key, value in values.items() if key != "profile_second_derivative"},
        green_weight=weight,
        green_weight_derivative=weight_derivative,
    ).evaluate(
        radial_field=fields["radial_field"],
        radial_field_derivative=fields["radial_field_derivative"],
        tangential_field=fields["tangential_field"],
        tangential_field_derivative=fields["tangential_field_derivative"],
    )
    source = centrifugal_completed_master_source_generic(**values, **fields)

    zero = Fraction(0)
    one = Fraction(1)
    radius_jet = _FirstRadialJet(values["radius"], one)
    metric_jet = _FirstRadialJet(
        values["metric_factor"], values["metric_factor_derivative"]
    )
    sine_jet = _FirstRadialJet(
        values["sine_profile"],
        values["cosine_profile"] * values["profile_derivative"],
    )
    cosine_jet = _FirstRadialJet(
        values["cosine_profile"],
        -values["sine_profile"] * values["profile_derivative"],
    )
    stress = centrifugal_completed_stress_generic(
        radius=radius_jet,
        metric_factor=metric_jet,
        sine_profile=sine_jet,
        cosine_profile=cosine_jet,
        profile_derivative=_FirstRadialJet(
            values["profile_derivative"], values["profile_second_derivative"]
        ),
        radial_field=_FirstRadialJet(
            fields["radial_field"], fields["radial_field_derivative"]
        ),
        radial_field_derivative=_FirstRadialJet(
            fields["radial_field_derivative"],
            fields["radial_field_second_derivative"],
        ),
        tangential_field=_FirstRadialJet(
            fields["tangential_field"], fields["tangential_field_derivative"]
        ),
        tangential_field_derivative=_FirstRadialJet(
            fields["tangential_field_derivative"], zero
        ),
        pion_mass_squared=_FirstRadialJet.constant(values["pion_mass_squared"]),
    ).total
    radius = values["radius"]
    metric = values["metric_factor"]
    coefficient_a = radius**2 * metric / 6
    coefficient_a_derivative = (
        radius * metric / 3
        + radius**2 * values["metric_factor_derivative"] / 6
    )
    boundary_derivative = (
        (weight_derivative * coefficient_a + weight * coefficient_a_derivative)
        * stress.energy_density.value
        + weight * coefficient_a * stress.energy_density.derivative
    ) * values["gravitational_coupling"]
    assert weak == weight * source + boundary_derivative


@pytest.mark.parametrize("left,right", [(Fraction(1, 100), Fraction(1, 10)), (Fraction(1), Fraction(4))])
def test_positive_green_series_encloses_endpoint_float_values(
    left: Fraction, right: Fraction
) -> None:
    green, derivative = _center_regular_green_intervals(
        RationalInterval(left, right), patch_radius=Fraction(20), terms=10
    )
    for radius in (left, right):
        ratio = float(radius / 20)
        exact_green = 40.0 / 15.0 * l2_center_regular_solution(ratio)
        exact_derivative = 2.0 / 15.0 * l2_center_regular_solution_derivative(ratio)
        assert float(green.lower) <= exact_green * (1 + 1.0e-14)
        assert exact_green <= float(green.upper) * (1 + 1.0e-14)
        assert float(derivative.lower) <= exact_derivative * (1 + 1.0e-14)
        assert exact_derivative <= float(derivative.upper) * (1 + 1.0e-14)


def test_trial_load_and_weak_residual_keep_derivative_test_coefficient() -> None:
    point = RationalInterval.point
    zero = point(0)
    one = point(1)
    radius = RationalInterval(1, 2)
    load = ValidatedWeakMasterLoadCell(
        radius=radius,
        green_weight=one,
        green_weight_derivative=zero,
        rigid=zero,
        b0=(point(2), point(-3)),
        b1=(point(5), point(7)),
    )
    trial = RationalC1TrialCell(
        radius=radius,
        radial_field=RationalPolynomial((1, 2)),
        tangential_field=RationalPolynomial((-1, 1)),
    )
    integral = validated_bulk_load_on_trial_cell(load, trial)
    # Range-times-width is deliberately an enclosure, not exact quadrature.
    assert integral.lower <= Fraction(79, 4) <= integral.upper

    zero_matrix = ((zero, zero), (zero, zero))
    coefficients = ValidatedConormalStrongCell(
        radius=radius,
        coordinate=zero_matrix,
        mixed=zero_matrix,
        principal=zero_matrix,
        mixed_derivative=zero_matrix,
        principal_derivative=zero_matrix,
        strong_source=(zero, zero),
    )
    residual = validated_weak_adjoint_residual_cell(coefficients, load, trial)
    assert residual.test_value_coefficient == load.b0
    assert residual.test_derivative_coefficient == load.b1


def test_green_series_rejects_domain_beyond_physical_wall() -> None:
    with pytest.raises(ValueError, match="radius/patch_radius"):
        _center_regular_green_intervals(
            RationalInterval(1, 5), patch_radius=Fraction(20), terms=8
        )
