import math
from dataclasses import replace
from fractions import Fraction

import pytest

from qgtoy.validated_interval import pi_machin_interval
from qgtoy.validated_skyrmion_au3b import ValidatedSkyrmionAU3BSharpCertificate
from qgtoy.validated_skyrmion_ule import (
    centered_pi_times_normalized_zero_spectrum_lower_bound,
    rational_log_interval,
    validated_centered_skyrmion_ule_heat_window,
    validated_centered_skyrmion_ule_residual,
)


def _certificate() -> ValidatedSkyrmionAU3BSharpCertificate:
    return ValidatedSkyrmionAU3BSharpCertificate(
        certificate_id="synthetic-sharp-au3b",
        authenticated_au2_sha256=None,
        authenticated_snapshot_sha256=None,
        band_split=Fraction(2),
        frequency_step=Fraction(1),
        radial_cell_count=2,
        physical_radius_lower_bound=Fraction(1),
        physical_radius_upper_bound=Fraction(1),
        physical_radius_provenance="synthetic dimensionless normalization",
        finite_band_squared_h2_bounds=(Fraction(1), Fraction(1), Fraction(1)),
        tail_squared_h2_bounds=(Fraction(1), Fraction(1), Fraction(1)),
        global_squared_h2_bounds=(Fraction(2), Fraction(2), Fraction(2)),
        q_norm_upper_bounds=(Fraction(2), Fraction(2), Fraction(2)),
        jump_l1_upper_bound=Fraction(6),
        jump_first_moment_upper_bound=Fraction(6),
    )


@pytest.mark.parametrize("dimension", [2, 3, 348, 8193])
def test_rational_log_interval_contains_library_value(dimension: int) -> None:
    enclosure = rational_log_interval(Fraction(dimension))
    value = math.log(dimension)
    assert float(enclosure.lower) <= value <= float(enclosure.upper)


def test_centered_zero_mode_bound_uses_upper_pi_and_radius() -> None:
    certificate = _certificate()
    expected = Fraction(1, 24) / pi_machin_interval(terms=80).upper**2
    assert (
        centered_pi_times_normalized_zero_spectrum_lower_bound(certificate)
        == expected
    )
    larger = replace(
        certificate,
        physical_radius_lower_bound=Fraction(2),
        physical_radius_upper_bound=Fraction(2),
    )
    assert (
        centered_pi_times_normalized_zero_spectrum_lower_bound(larger)
        == expected / 8
    )


def test_half_integer_heat_window_saturates_exact_budget() -> None:
    record = validated_centered_skyrmion_ule_heat_window(
        _certificate(),
        spin=Fraction(7, 2),
        residual_budget=Fraction(1, 1000),
        burnin_rate_multiples=Fraction(10),
    )
    assert record["dimension_d"] == 8
    assert record["residual_at_coupling_cap_exact"] == "1/1000"
    assert record["coupling_window_nonempty"] is True
    assert record["norm_kind"] == "ancilla_stable_state_operator_norm"
    assert "diamond" in record["claim_boundary"]
    assert "half_integer_kinematics_only" in record[
        "projective_spin_recovery_composition_status"
    ]
    assert record["certificate_authentication_status"] == (
        "conditional_unauthenticated_certificate"
    )
    assert "physical_length_map_required" in record["units_status"]


def test_moment_bounds_and_zero_mode_move_cap_in_safe_directions() -> None:
    certificate = _certificate()
    base = validated_centered_skyrmion_ule_heat_window(
        certificate,
        spin=Fraction(2),
        residual_budget=Fraction(1, 100),
        burnin_rate_multiples=Fraction(10),
    )
    worse_moments = validated_centered_skyrmion_ule_heat_window(
        replace(
            certificate,
            jump_l1_upper_bound=Fraction(8),
            jump_first_moment_upper_bound=Fraction(9),
        ),
        spin=Fraction(2),
        residual_budget=Fraction(1, 100),
        burnin_rate_multiples=Fraction(10),
    )
    stronger_zero_mode = validated_centered_skyrmion_ule_heat_window(
        replace(
            certificate,
            physical_radius_lower_bound=Fraction(1, 2),
            physical_radius_upper_bound=Fraction(1, 2),
        ),
        spin=Fraction(2),
        residual_budget=Fraction(1, 100),
        burnin_rate_multiples=Fraction(10),
    )
    assert Fraction(
        worse_moments["coupling_squared_upper_bound_exact"]
    ) < Fraction(base["coupling_squared_upper_bound_exact"])
    assert Fraction(
        stronger_zero_mode["coupling_squared_upper_bound_exact"]
    ) > Fraction(base["coupling_squared_upper_bound_exact"])


def test_deadline_and_preparation_age_can_close_window() -> None:
    record = validated_centered_skyrmion_ule_heat_window(
        _certificate(),
        spin=Fraction(1, 2),
        residual_budget=Fraction(1, 10**12),
        burnin_rate_multiples=Fraction(10),
        maximum_normalized_observation_time=Fraction(1),
        maximum_normalized_preparation_age=Fraction(1),
    )
    assert record["coupling_window_nonempty"] is False
    assert Fraction(record["coupling_squared_lower_bound_exact"]) > Fraction(
        record["coupling_squared_upper_bound_exact"]
    )


def test_general_residual_is_exact_and_reuses_one_declared_coupling() -> None:
    record = validated_centered_skyrmion_ule_residual(
        _certificate(),
        spin=Fraction(3, 2),
        declared_action_coupling_squared=Fraction(1, 10**6),
        elapsed_normalized_time=Fraction(5),
        burn_in_normalized_time=Fraction(2),
        switch_lead_normalized_time=Fraction(1),
    )
    components = sum(
        Fraction(record[name])
        for name in (
            "initialization_residual_upper_exact",
            "long_time_residual_upper_exact",
            "finite_history_residual_upper_exact",
        )
    )
    assert components == Fraction(record["total_residual_upper_exact"])
    assert record["single_declared_coupling_reused_by_construction"] is True


def test_invalid_spin_denominator_is_rejected() -> None:
    with pytest.raises(ValueError, match="integer or half-integer"):
        validated_centered_skyrmion_ule_heat_window(
            _certificate(),
            spin=Fraction(1, 3),
            residual_budget=Fraction(1, 100),
            burnin_rate_multiples=Fraction(10),
        )


@pytest.mark.parametrize(
    "value",
    [Fraction(1), Fraction(2), Fraction(4), Fraction(1023, 512), Fraction(1025, 512)],
)
def test_rational_log_interval_handles_binary_boundaries(value: Fraction) -> None:
    enclosure = rational_log_interval(value)
    assert float(enclosure.lower) <= math.log(float(value)) <= float(enclosure.upper)


def test_invalid_logarithm_terms_are_rejected() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        rational_log_interval(Fraction(2), terms=0)


def test_digest_claims_and_radius_provenance_are_propagated() -> None:
    certificate = replace(
        _certificate(),
        authenticated_au2_sha256="a" * 64,
        authenticated_snapshot_sha256="b" * 64,
        physical_radius_provenance="dimensionless R=1 canonical archive",
    )
    record = validated_centered_skyrmion_ule_heat_window(
        certificate,
        spin=Fraction(1, 2),
        residual_budget=Fraction(1, 100),
        burnin_rate_multiples=Fraction(10),
    )
    assert record["certificate_authentication_status"] == (
        "conditional_with_external_digest_claims"
    )
    assert record["authenticated_au2_sha256"] == "a" * 64
    assert record["authenticated_snapshot_sha256"] == "b" * 64
    assert record["radius_provenance"] == certificate.physical_radius_provenance


def test_inconsistent_spectral_certificate_is_rejected() -> None:
    certificate = replace(
        _certificate(),
        global_squared_h2_bounds=(Fraction(3), Fraction(2), Fraction(2)),
    )
    with pytest.raises(ValueError, match="global spectral bound"):
        centered_pi_times_normalized_zero_spectrum_lower_bound(certificate)

    inconsistent_moment = replace(
        _certificate(),
        jump_l1_upper_bound=Fraction(1),
    )
    with pytest.raises(ValueError, match="jump L1 bound"):
        centered_pi_times_normalized_zero_spectrum_lower_bound(
            inconsistent_moment
        )


def test_exact_api_survives_float_diagnostic_overflow() -> None:
    residual = validated_centered_skyrmion_ule_residual(
        _certificate(),
        spin=Fraction(1, 2),
        declared_action_coupling_squared=Fraction(10**1000),
        elapsed_normalized_time=Fraction(1),
        burn_in_normalized_time=Fraction(1),
        switch_lead_normalized_time=Fraction(0),
    )
    assert residual["total_residual_upper"] is None
    assert Fraction(residual["total_residual_upper_exact"]) > 0
    window = validated_centered_skyrmion_ule_heat_window(
        _certificate(),
        spin=Fraction(1, 2),
        residual_budget=Fraction(10**1000),
        burnin_rate_multiples=Fraction(10),
    )
    assert window["coupling_upper_diagnostic"] is None
    assert Fraction(window["coupling_squared_upper_bound_exact"]) > 0


def test_exact_api_survives_tiny_values_without_zero_diagnostics() -> None:
    tiny = Fraction(1, 10**5000)
    residual = validated_centered_skyrmion_ule_residual(
        _certificate(),
        spin=Fraction(1, 2),
        declared_action_coupling_squared=tiny,
        elapsed_normalized_time=Fraction(1),
        burn_in_normalized_time=Fraction(1),
        switch_lead_normalized_time=Fraction(0),
    )
    assert residual["total_residual_upper"] is None
    assert "/" in residual["total_residual_upper_exact"]
    window = validated_centered_skyrmion_ule_heat_window(
        _certificate(),
        spin=Fraction(1, 2),
        residual_budget=tiny,
        burnin_rate_multiples=Fraction(10),
    )
    assert window["coupling_upper_diagnostic"] is None
    assert "/" in window["coupling_squared_upper_bound_exact"]


def test_observation_deadline_can_saturate_window_exactly() -> None:
    base = validated_centered_skyrmion_ule_heat_window(
        _certificate(),
        spin=Fraction(1, 2),
        residual_budget=Fraction(1, 100),
        burnin_rate_multiples=Fraction(10),
    )
    coupling_cap = Fraction(base["coupling_squared_upper_bound_exact"])
    log_upper = Fraction(base["log_dimension_upper_exact"])
    zero_mode = Fraction(
        base["pi_times_normalized_zero_spectrum_lower_bound_exact"]
    )
    deadline = log_upper / (2 * zero_mode * coupling_cap)
    saturated = validated_centered_skyrmion_ule_heat_window(
        _certificate(),
        spin=Fraction(1, 2),
        residual_budget=Fraction(1, 100),
        burnin_rate_multiples=Fraction(10),
        maximum_normalized_observation_time=deadline,
    )
    assert saturated["coupling_window_nonempty"] is True
    assert saturated["coupling_squared_lower_bound_exact"] == (
        saturated["coupling_squared_upper_bound_exact"]
    )
