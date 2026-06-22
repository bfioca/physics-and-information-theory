import hashlib
import json
from math import asinh, atanh, exp, log, pi, sinh, sqrt, tanh
from pathlib import Path

import pytest

from qgtoy.local_scalar_observer_cost import (
    all_angular_cost_extension_record,
    bekenstein_dephasing_comparison_record,
    causal_output_support_record,
    de_sitter_areal_radius_from_optical,
    de_sitter_optical_radius,
    dephasing_exponent_from_observer_error,
    fractional_inverse_schur_constant,
    flux_free_constraint_measure_record,
    linear_momentum_profile_window,
    local_scalar_observer_cost_certificate,
    logarithmic_kernel_row_integral,
    minimum_scalar_killing_energy,
    observer_backreaction_lower_bound,
    observer_cost_coefficient_from_optical_support,
    observer_cost_optimality_bracket_from_optical_support,
    scalar_pointer_action_record,
    second_inverse_norm_constant,
    sharp_observer_cost_characterization,
    sharp_thermal_half_line_momentum_cost,
    smooth_source_density_record,
    spherical_wall_constraint_ratio,
    thermal_momentum_kernel_value,
    thermal_momentum_maximum_row_integral,
    thermal_momentum_row_maximizer,
    weak_gravity_observer_error_floor,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "experiments/local_scalar_observer_cost_certificate.json"


def test_areal_and_optical_radii_are_exact_inverses() -> None:
    optical = de_sitter_optical_radius(0.2, static_patch_radius=1.0)
    assert optical == pytest.approx(atanh(0.2))
    assert de_sitter_areal_radius_from_optical(
        optical,
        static_patch_radius=1.0,
    ) == pytest.approx(0.2)


def test_finite_propagation_adds_duration_in_optical_distance() -> None:
    record = causal_output_support_record(
        source_areal_radius=0.2,
        switching_duration=0.1,
        static_patch_radius=1.0,
    )
    expected_optical = atanh(0.2) + 0.1
    assert record["output_optical_radius_L"] == pytest.approx(expected_optical)
    assert record["output_areal_radius_b"] == pytest.approx(tanh(expected_optical))


def test_compressed_inverse_constants_match_kernel_proofs() -> None:
    maximum_location = 1.0 / sqrt(2.0)
    assert fractional_inverse_schur_constant() == pytest.approx(
        2.0 * asinh(1.0) / pi
    )
    assert logarithmic_kernel_row_integral(
        maximum_location
    ) == pytest.approx(fractional_inverse_schur_constant())
    assert second_inverse_norm_constant() == pytest.approx(4.0 / pi**2)
    nearby = (0.2, 0.5, 0.8, 0.99)
    assert all(
        logarithmic_kernel_row_integral(value)
        <= fractional_inverse_schur_constant()
        for value in nearby
    )
    assert 1.0 / pi < fractional_inverse_schur_constant()
    assert 1.0 / pi**2 < second_inverse_norm_constant()


def test_exact_thermal_kernel_has_the_vacuum_limit_and_kms_enhancement() -> None:
    x = 0.2
    y = 0.7
    vacuum = log((x + y) / abs(x - y)) / pi
    cold = thermal_momentum_kernel_value(
        x,
        y,
        inverse_temperature=1.0e8,
    )
    thermal = thermal_momentum_kernel_value(
        x,
        y,
        inverse_temperature=2.0 * pi,
    )
    assert cold == pytest.approx(vacuum, rel=1.0e-12)
    assert thermal > vacuum
    assert thermal_momentum_kernel_value(
        y,
        x,
        inverse_temperature=2.0 * pi,
    ) == pytest.approx(thermal)


def test_exact_thermal_kernel_matches_the_matsubara_product() -> None:
    x = 0.2
    y = 0.7
    beta = 2.0 * pi
    vacuum = log((x + y) / abs(x - y)) / pi
    partial_sum = sum(
        log(
            ((index * beta) ** 2 + (x + y) ** 2)
            / ((index * beta) ** 2 + (x - y) ** 2)
        )
        for index in range(1, 10001)
    ) / pi
    exact = thermal_momentum_kernel_value(
        x,
        y,
        inverse_temperature=beta,
    )
    assert exact == pytest.approx(vacuum + partial_sum, abs=5.0e-7)


def test_exact_kms_row_maximizer_satisfies_the_stationarity_identity() -> None:
    tau = 0.7
    u_star = thermal_momentum_row_maximizer(tau)
    assert 0.0 < u_star < 1.0
    assert sinh(tau * (1.0 + u_star)) * sinh(
        tau * (1.0 - u_star)
    ) == pytest.approx(sinh(tau * u_star) ** 2)
    row = thermal_momentum_maximum_row_integral(
        1.4,
        inverse_temperature=2.0 * pi,
    )
    assert row["maximizing_position_ratio_u"] == pytest.approx(u_star)


@pytest.mark.parametrize(
    ("support_length", "inverse_temperature"),
    ((0.1, 0.7), (1.0, 2.0 * pi), (7.0, 0.4), (30.0, 100.0)),
)
def test_general_thermal_half_line_cost_has_rigorous_global_brackets(
    support_length: float,
    inverse_temperature: float,
) -> None:
    record = sharp_thermal_half_line_momentum_cost(
        support_length,
        inverse_temperature=inverse_temperature,
    )
    assert record["rigorous_lower_coefficient"] <= record[
        "rigorous_explicit_upper_coefficient"
    ]
    assert record["rigorous_explicit_upper_coefficient"] <= record[
        "closed_form_upper_coefficient"
    ]
    assert record["exact_optimal_coefficient_formula"] == (
        "C_beta(L)=2*L*Lambda(pi*L/beta)"
    )


def test_general_thermal_half_line_cost_has_the_correct_scaling() -> None:
    base = sharp_thermal_half_line_momentum_cost(
        0.8,
        inverse_temperature=3.0,
    )
    scale = 7.5
    scaled = sharp_thermal_half_line_momentum_cost(
        scale * 0.8,
        inverse_temperature=scale * 3.0,
    )
    assert scaled["thermal_support_ratio_tau"] == pytest.approx(
        base["thermal_support_ratio_tau"]
    )
    for key in (
        "vacuum_profile_lower_coefficient",
        "thermal_green_lower_coefficient",
        "closed_form_upper_coefficient",
        "exact_row_schur_upper_coefficient",
        "small_support_upper_coefficient",
        "large_support_upper_coefficient",
        "rigorous_explicit_upper_coefficient",
    ):
        assert scaled[key] == pytest.approx(scale * base[key])


@pytest.mark.parametrize("support_ratio", (1.0e-6, 0.3, 1.0, 10.0, 100.0))
def test_sharp_cost_characterization_has_rigorous_global_brackets(
    support_ratio: float,
) -> None:
    record = sharp_observer_cost_characterization(
        support_ratio,
        static_patch_radius=1.0,
    )
    lower = record["rigorous_lower_coefficient"]
    upper = record["rigorous_explicit_upper_coefficient"]
    assert lower <= upper
    assert upper <= record["legacy_F_upper_coefficient"]
    assert record["exact_optimal_coefficient_formula"] == (
        "C_opt(y)=2*y*Lambda(y/2)"
    )
    half_line = record["general_thermal_half_line_specialization"]
    assert half_line["thermal_support_ratio_tau"] == pytest.approx(
        record["thermal_support_ratio_tau"]
    )
    assert half_line["rigorous_lower_coefficient"] == pytest.approx(
        record["rigorous_lower_coefficient"]
    )


def test_momentum_lower_bounds_dominate_the_coordinate_sector_for_all_y() -> None:
    for exponent in range(-8, 9):
        y = 10.0 ** (exponent / 2.0)
        coordinate_upper = 2.0 * y / pi + 2.0 * y**2 / pi**3
        momentum_lower = max(3.0 * y / pi, 8.0 * y**2 / pi**3)
        assert momentum_lower >= coordinate_upper


def test_dimensionless_cost_coefficient_has_vacuum_and_thermal_terms() -> None:
    record = observer_cost_coefficient_from_optical_support(
        0.3,
        static_patch_radius=1.0,
    )
    expected = 4.0 * asinh(1.0) * 0.3 / pi + 8.0 * 0.3**2 / pi**3
    assert record["dimensionless_cost_coefficient_F"] == pytest.approx(expected)
    assert record["vacuum_localization_term"] > record[
        "thermal_static_patch_term"
    ]


def test_s_wave_constants_extend_to_every_angular_sector() -> None:
    record = all_angular_cost_extension_record()
    assert "A_l>=A_0" in record["operator_order"]
    assert "arbitrary angular source data" in record["conclusion"]
    assert "exclude coordinate-sector and l>0 ties" in record["conclusion"]


def test_harlow_pointer_target_and_detector_scope_are_not_conflated() -> None:
    record = scalar_pointer_action_record()
    assert "Harlow-Usatyuk-Zhao" in record["harlow_pointer_target_relation"]
    assert "not identified with exp(-S_Ob)" in record[
        "harlow_pointer_target_relation"
    ]
    assert "not an autonomous relativistic pointer field" in record[
        "pointer_locality_scope"
    ]
    assert "commute at spacelike separation" in record["pointer_locality_scope"]


def test_ideal_profile_has_a_rigorous_smooth_source_closure() -> None:
    record = smooth_source_density_record()
    assert "continuous under L2 convergence" in record["covariance_continuity"]
    assert "converge uniformly" in record["mass_continuity"]
    assert "worldtube-supported" in record["source_realization"]


def test_bekenstein_entropy_and_dephasing_are_not_the_same_form() -> None:
    record = bekenstein_dephasing_comparison_record()
    assert "Gamma_0/S_B diverges" in record["boundary_sequence"]
    assert "S_B/Gamma_0 diverges" in record["center_sequence"]
    assert "neither uniformly bounds the other" in record["conclusion"]


def test_small_support_scaling_has_close_two_sided_constants() -> None:
    record = observer_cost_optimality_bracket_from_optical_support(
        1.0e-8,
        static_patch_radius=1.0,
    )
    assert record["constructive_lower_coefficient"] == pytest.approx(
        3.0e-8 / pi
    )
    assert record["small_support_limiting_ratio"] == pytest.approx(
        4.0 * asinh(1.0) / 3.0
    )
    assert record["upper_to_lower_ratio"] == pytest.approx(
        record["small_support_limiting_ratio"],
        rel=1.0e-8,
    )


def test_longer_switching_weakens_the_energy_lower_bound() -> None:
    short = minimum_scalar_killing_energy(
        1.0e-3,
        source_areal_radius=0.2,
        switching_duration=0.1,
        static_patch_radius=1.0,
    )
    long = minimum_scalar_killing_energy(
        1.0e-3,
        source_areal_radius=0.2,
        switching_duration=0.5,
        static_patch_radius=1.0,
    )
    assert short["dephasing_exponent_Gamma"] == pytest.approx(log(500.0))
    assert short["minimum_scalar_killing_energy"] > long[
        "minimum_scalar_killing_energy"
    ]


def test_wall_constraint_composes_with_channel_energy_bound() -> None:
    record = observer_backreaction_lower_bound(
        1.0e-3,
        source_areal_radius=0.2,
        switching_duration=0.1,
        static_patch_radius=1.0,
        newton_constant=1.0e-3,
    )
    direct = spherical_wall_constraint_ratio(
        record["minimum_scalar_killing_energy"],
        output_areal_radius=record["output_areal_radius_b"],
        static_patch_radius=1.0,
        newton_constant=1.0e-3,
    )
    assert record["minimum_wall_constraint_ratio_q"] == pytest.approx(direct)
    assert direct > 0.0


@pytest.mark.parametrize("radius", (0.01, 0.2, 0.8))
def test_flux_free_optical_energy_is_exact_constraint_mass(radius: float) -> None:
    record = flux_free_constraint_measure_record(
        radius,
        static_patch_radius=1.0,
    )
    assert record["mass_measure_per_radial_momentum_squared_dx"] == (
        pytest.approx(0.5)
    )


def test_weak_gravity_floor_saturates_the_necessary_wall_bound() -> None:
    floor = weak_gravity_observer_error_floor(
        maximum_constraint_ratio=0.2,
        source_areal_radius=0.2,
        switching_duration=0.1,
        static_patch_radius=1.0,
        newton_constant=0.1,
    )
    epsilon = floor["minimum_observer_error_epsilon"]
    assert epsilon == pytest.approx(
        0.5 * exp(-floor["maximum_dephasing_exponent_Gamma"])
    )
    composed = observer_backreaction_lower_bound(
        epsilon,
        source_areal_radius=0.2,
        switching_duration=0.1,
        static_patch_radius=1.0,
        newton_constant=0.1,
    )
    assert composed["minimum_wall_constraint_ratio_q"] == pytest.approx(0.2)


def test_explicit_linear_profile_has_a_nonempty_weak_gravity_window() -> None:
    record = linear_momentum_profile_window(
        1.0e-6,
        support_areal_radius=0.2,
        static_patch_radius=1.0,
        newton_constant=1.0e-6,
        maximum_constraint_ratio=0.25,
    )
    assert record["thermal_covariance_lower_bound_Q"] == pytest.approx(
        3.0 * atanh(0.2) / (2.0 * pi)
    )
    assert record["target_has_certified_weak_gravity_window"]
    assert record["sufficient_local_constraint_ratio_upper_bound"] < 0.01


def test_linear_profile_constraint_ratio_is_monotone() -> None:
    radii = tuple(index / 100.0 for index in range(1, 100))
    values = tuple(
        atanh(radius) ** 3 / (radius * (1.0 - radius**2))
        for radius in radii
    )
    assert all(left < right for left, right in zip(values, values[1:]))


def test_default_certificate_passes_the_theorem_but_keeps_paper_gate_open() -> None:
    certificate = local_scalar_observer_cost_certificate()
    assert certificate["status"] == (
        "strengthened_final_support_theorem_pass_external_review_open"
    )
    assert all(certificate["certified_claims"].values())
    assert "actuator" in certificate["paper_gate"]
    assert "not modeled" in certificate["claim_boundary"]
    assert certificate["certified_claims"][
        "all_angular_conformal_scalar_extension"
    ]
    assert certificate["certified_claims"][
        "harlow_pointer_target_identified_without_entropy_dictionary"
    ]
    assert "not time-reflection symmetric" in certificate[
        "observer_cost_bound"
    ]["gravity_hypothesis"]


def test_frozen_certificate_is_source_bound() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    assert record["status"] == (
        "strengthened_final_support_theorem_pass_external_review_open"
    )
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


@pytest.mark.parametrize(
    ("function", "kwargs"),
    [
        (
            de_sitter_optical_radius,
            {"areal_radius": 1.0, "static_patch_radius": 1.0},
        ),
        (
            dephasing_exponent_from_observer_error,
            {"observer_error": 0.6},
        ),
        (
            observer_cost_coefficient_from_optical_support,
            {"output_optical_radius": 0.0, "static_patch_radius": 1.0},
        ),
        (
            spherical_wall_constraint_ratio,
            {
                "killing_energy": 1.0,
                "output_areal_radius": 1.0,
                "static_patch_radius": 1.0,
                "newton_constant": 1.0,
            },
        ),
    ],
)
def test_invalid_cost_inputs_are_rejected(function, kwargs) -> None:
    with pytest.raises(ValueError):
        function(**kwargs)
