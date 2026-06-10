from fractions import Fraction

import pytest

from qgtoy.spherical_rotational_backreaction import (
    collective_constraint_casimir_capacity,
    collective_constraint_lower_bound,
    collective_constraint_orientation_risk_floor,
    collective_rotational_backreaction_record,
    spherical_rotational_backreaction_certificate,
)


PARAMETERS = {
    "metric_budget": Fraction(1, 2),
    "wall_radius": Fraction(4),
    "curvature": Fraction(1, 400),
    "static_patch_radius_squared_over_newton": Fraction(10**6),
    "static_mass_lower": Fraction(34),
    "inertia_upper": Fraction(49),
}


def test_exact_casimir_capacity_saturates_am_gm_bound() -> None:
    capacity = collective_constraint_casimir_capacity(**PARAMETERS)
    lower = collective_constraint_lower_bound(
        float(capacity),
        metric_budget=0.5,
        wall_radius=4.0,
        curvature=1.0 / 400.0,
        static_patch_radius_squared_over_newton=1.0e6,
        static_mass=34.0,
        inertia=49.0,
    )
    assert lower == pytest.approx(0.5)
    assert collective_constraint_orientation_risk_floor(capacity) > 0


def test_capacity_has_expected_monotonicity() -> None:
    baseline = collective_constraint_casimir_capacity(**PARAMETERS)
    stronger_gravity = collective_constraint_casimir_capacity(
        **{**PARAMETERS, "static_patch_radius_squared_over_newton": Fraction(5 * 10**5)}
    )
    tighter_metric = collective_constraint_casimir_capacity(
        **{**PARAMETERS, "metric_budget": Fraction(1, 4)}
    )
    assert stronger_gravity < baseline
    assert tighter_metric < baseline


def test_record_exposes_global_risk_chain() -> None:
    record = collective_rotational_backreaction_record(**PARAMETERS)
    assert record["maximum_mean_casimir_float"] > 0.0
    assert record["global_orientation_risk_lower_bound_float"] > 0.0
    assert "AM-GM" in record["coupling_elimination"]


def test_certificate_passes() -> None:
    certificate = spherical_rotational_backreaction_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("metric_budget", Fraction(1)),
        ("wall_radius", Fraction(0)),
        ("curvature", Fraction(0)),
        ("static_mass_lower", Fraction(0)),
        ("inertia_upper", Fraction(0)),
    ],
)
def test_invalid_exact_inputs_are_rejected(name, value) -> None:
    with pytest.raises(ValueError):
        collective_constraint_casimir_capacity(**{**PARAMETERS, name: value})
