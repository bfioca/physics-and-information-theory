import pytest

from qgtoy.skyrmion_tidal_reference_discriminator import (
    radial_tidal_gradiometer_record,
    spin_two_tidal_reference_discriminator_record,
)


def test_gradiometer_contracts_radial_tidal_tensor():
    record = radial_tidal_gradiometer_record(
        radial_electric_weyl_tensor=((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 2.0)),
        observation_direction=(0.0, 0.0, 1.0),
        physical_proof_mass_separation=0.25,
    )
    assert record["radial_electric_weyl_contraction"] == pytest.approx(2.0)
    assert record["fractional_relative_acceleration"] == pytest.approx(-2.0)
    assert record["linearized_relative_acceleration"] == pytest.approx(-0.5)


def test_signal_is_linear_in_proof_mass_separation():
    common = {
        "radial_electric_weyl_tensor": (
            (-1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
            (0.0, 0.0, 2.0),
        ),
        "observation_direction": (1.0, 0.0, 0.0),
    }
    first = radial_tidal_gradiometer_record(
        **common, physical_proof_mass_separation=0.2
    )
    second = radial_tidal_gradiometer_record(
        **common, physical_proof_mass_separation=0.6
    )
    assert second["linearized_relative_acceleration"] == pytest.approx(
        3.0 * first["linearized_relative_acceleration"]
    )


def test_equal_casimir_states_have_distinct_tidal_signals():
    record = spin_two_tidal_reference_discriminator_record(
        skyrme_coupling=1.0,
        pion_decay_constant=1.0,
        newton_constant=1.0e-6,
        physical_proof_mass_separation=1.0,
        node_count=101,
        maximum_slow_rotation=0.1,
    )
    assert record["same_casimir_check"]
    assert record["same_inertia_and_energy_check"]
    assert record["shared_casimir_expectation"] == pytest.approx(6.0)
    assert record["spin_cat_gradiometer"]["linearized_relative_acceleration"] != 0.0
    assert (
        record["anticoherent_gradiometer"]["linearized_relative_acceleration"]
        == 0.0
    )
    assert record["linearized_relative_acceleration_contrast"] != 0.0


@pytest.mark.parametrize(
    "kwargs",
    (
        {"observation_direction": (0.0, 0.0, 2.0)},
        {"physical_proof_mass_separation": 0.0},
        {
            "radial_electric_weyl_tensor": (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        },
    ),
)
def test_gradiometer_rejects_invalid_inputs(kwargs):
    values = {
        "radial_electric_weyl_tensor": (
            (-1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
            (0.0, 0.0, 2.0),
        ),
        "observation_direction": (0.0, 0.0, 1.0),
        "physical_proof_mass_separation": 1.0,
    }
    values.update(kwargs)
    with pytest.raises(ValueError):
        radial_tidal_gradiometer_record(**values)
