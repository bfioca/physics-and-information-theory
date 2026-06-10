from math import exp

import pytest

from qgtoy.finite_time_tidal_detector import (
    constant_rate_rank_two_jacobi_kernel,
    finite_time_tidal_readout_record,
    rank_two_heat_attenuation,
)


def test_rank_two_multiplier_has_casimir_six() -> None:
    assert rank_two_heat_attenuation(0.3) == pytest.approx(exp(-1.8))


def test_jacobi_kernel_has_zero_rate_limit() -> None:
    assert constant_rate_rank_two_jacobi_kernel(2.0, 0.0) == pytest.approx(2.0)
    tiny = constant_rate_rank_two_jacobi_kernel(2.0, 1.0e-10)
    assert tiny == pytest.approx(2.0, rel=1.0e-9)


def test_short_exposure_series_has_correct_linear_coefficient() -> None:
    argument = 6.0e-5
    rate = argument / 6.0
    expected = 0.5 - argument / 6.0 + argument**2 / 24.0
    assert constant_rate_rank_two_jacobi_kernel(1.0, rate) == pytest.approx(
        expected, abs=1.0e-14
    )


@pytest.mark.parametrize("time,rate", [(0.2, 0.1), (1.0, 0.7), (3.0, 2.0)])
def test_closed_kernel_matches_direct_formula(time: float, rate: float) -> None:
    decay = 6.0 * rate
    expected = time / decay - (1.0 - exp(-decay * time)) / decay**2
    assert constant_rate_rank_two_jacobi_kernel(time, rate) == pytest.approx(
        expected
    )


def test_tidal_readout_composes_rank_two_decay_and_gaussian_error() -> None:
    record = finite_time_tidal_readout_record(
        initial_fractional_acceleration_contrast=-0.02,
        physical_proof_mass_separation=0.4,
        interrogation_time=3.0,
        diffusion_rate=0.1,
        displacement_readout_standard_deviation=0.002,
    )
    assert record["kernel_bounds_hold"] is True
    assert record["rank_two_equals_rank_one_cubed_error"] == pytest.approx(0.0)
    assert record["mean_displacement_contrast"] < 0.0
    assert record["displacement_signal_to_noise_ratio"] > 0.0
    assert 0.0 < record["equal_prior_optimal_gaussian_error_probability"] < 0.5


def test_zero_signal_has_coin_flip_error() -> None:
    record = finite_time_tidal_readout_record(
        initial_fractional_acceleration_contrast=0.0,
        physical_proof_mass_separation=1.0,
        interrogation_time=1.0,
        diffusion_rate=0.2,
        displacement_readout_standard_deviation=0.1,
    )
    assert record["equal_prior_optimal_gaussian_error_probability"] == 0.5


@pytest.mark.parametrize(
    "keyword",
    [
        "physical_proof_mass_separation",
        "displacement_readout_standard_deviation",
    ],
)
def test_positive_detector_inputs_are_enforced(keyword: str) -> None:
    arguments = {
        "initial_fractional_acceleration_contrast": 0.1,
        "physical_proof_mass_separation": 1.0,
        "interrogation_time": 1.0,
        "diffusion_rate": 0.2,
        "displacement_readout_standard_deviation": 0.1,
    }
    arguments[keyword] = 0.0
    with pytest.raises(ValueError, match="must be positive"):
        finite_time_tidal_readout_record(**arguments)
