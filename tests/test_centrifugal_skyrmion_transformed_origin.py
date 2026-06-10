from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_transformed_origin import (
    centrifugal_transformed_origin_certificate,
    transformed_quadrupole_reduced_density,
    transformed_quadrupole_reduced_density_from_kernels,
)


def test_transformed_density_has_exact_center_value():
    for v in (Fraction(-3, 2), Fraction(0), Fraction(7, 5)):
        record = transformed_quadrupole_reduced_density_from_kernels(
            t=Fraction(0),
            metric_factor=Fraction(1),
            profile_deficit_over_radius=Fraction(11, 7),
            profile_deficit_time_derivative=Fraction(-2, 5),
            sine_over_radius=Fraction(11, 7),
            cosine_of_profile_deficit=Fraction(1),
            v=v,
            u=Fraction(19, 13),
            v_time_derivative=Fraction(-17, 9),
            u_time_derivative=Fraction(23, 8),
            pion_mass_squared=Fraction(5, 3),
        )
        assert record["reduced_density"] == v * v / 6


def test_transformed_density_matches_direct_full_density():
    record = centrifugal_transformed_origin_certificate()
    assert all(record["exact_fraction_center_checks"])
    assert record["maximum_floating_direct_replay_relative_error"] < 2.0e-15


def test_rotational_source_is_compatible_with_cubic_resonance():
    compatibility = centrifugal_transformed_origin_certificate()[
        "forced_cubic_compatibility"
    ]
    assert all(
        compatibility["cubic_indicial_rows_have_ratio_minus_three_halves"]
    )
    assert compatibility["source_has_same_ratio"]
    assert compatibility["source_is_in_range_of_K3"]
    assert compatibility["particular_cubic_initial_relation_verified"]


def test_floating_evaluator_is_finite_at_the_origin():
    record = transformed_quadrupole_reduced_density(
        t=0.0,
        curvature=0.0025,
        profile_deficit_over_radius=1.58,
        profile_deficit_time_derivative=-0.2,
        v=0.7,
        u=-0.4,
        v_time_derivative=0.2,
        u_time_derivative=-0.1,
        pion_mass=1.0,
    )
    assert record["reduced_density"] == pytest.approx(0.7**2 / 6.0)
    assert record["original_density"] == 0.0


@pytest.mark.parametrize(
    "kwargs",
    (
        {"t": -1.0},
        {"curvature": -1.0},
        {"pion_mass": -1.0},
        {"t": 2.0, "curvature": 1.0},
    ),
)
def test_floating_evaluator_rejects_invalid_inputs(kwargs):
    inputs = {
        "t": 0.1,
        "curvature": 0.0025,
        "profile_deficit_over_radius": 1.58,
        "profile_deficit_time_derivative": -0.2,
        "v": 0.7,
        "u": -0.4,
        "v_time_derivative": 0.2,
        "u_time_derivative": -0.1,
        "pion_mass": 1.0,
    }
    inputs.update(kwargs)
    with pytest.raises(ValueError):
        transformed_quadrupole_reduced_density(**inputs)
