from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_friedrichs_trace import (
    centrifugal_friedrichs_origin_trace_certificate,
    certify_friedrichs_physical_endpoint_trace,
    local_power_energy_integral,
    power_branch_has_finite_local_energy,
)
from qgtoy.validated_centrifugal_conormal_remainder import (
    validate_centrifugal_conormal_remainder,
)
from qgtoy.validated_centrifugal_physical_origin_transfer import (
    validate_centrifugal_physical_origin_transfer,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_quintic_family import (
    validate_skyrmion_origin_quintic_family,
)


AUTHENTICATED_SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
)


def test_exact_power_integrability_threshold() -> None:
    assert power_branch_has_finite_local_energy(Fraction(-1, 2) + Fraction(1, 100))
    assert not power_branch_has_finite_local_energy(Fraction(-1, 2))
    assert not power_branch_has_finite_local_energy(-4)
    assert local_power_energy_integral(1, Fraction(1, 16)) == Fraction(1, 12_288)
    assert local_power_energy_integral(-2, Fraction(1, 16)) is None


def test_all_indicial_branches_have_positive_exact_leading_energy() -> None:
    certificate = centrifugal_friedrichs_origin_trace_certificate()
    assert certificate["indicial_powers"] == (1, 3, -2, -4)
    assert certificate["leading_principal_block_positive_for_every_real_slope"]
    checks = certificate["branch_checks"]
    assert isinstance(checks, dict)
    for exponent in (1, 3, -2, -4):
        assert checks[exponent]["indicial_residual_vanishes"]
        assert checks[exponent]["leading_energy_positive_for_every_real_slope"]
    assert checks[1]["finite_local_energy"]
    assert checks[3]["finite_local_energy"]
    assert not checks[-2]["finite_local_energy"]
    assert not checks[-4]["finite_local_energy"]


def test_certificate_excludes_distinct_singular_power_cancellation() -> None:
    certificate = centrifugal_friedrichs_origin_trace_certificate()
    assert certificate["homogeneous_solution_trace_dimension"] == 2
    assert certificate["finite_energy_homogeneous_powers"] == (1, 3)
    assert certificate["forced_affine_column_power"] == 3
    assert "x^-8" in certificate["singular_cancellation_rule"]
    assert "x^-4" in certificate["singular_cancellation_rule"]
    assert "does not classify the entire form domain" in certificate["scope"]


def test_admissible_germs_map_to_certified_physical_endpoint_columns() -> None:
    profile = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )
    remainder = validate_centrifugal_conormal_remainder(profile)
    transfer = validate_centrifugal_physical_origin_transfer(profile, remainder)
    trace = certify_friedrichs_physical_endpoint_trace(transfer)
    assert trace.cutoff == Fraction(1, 16)
    assert trace.homogeneous_dimension == 2
    assert trace.homogeneous_branch_order == (
        "linear_homogeneous",
        "cubic_homogeneous",
    )
    assert trace.forced_branch == "forced_particular"
    assert len(trace.cells) == 2
    assert trace.cells[0].homogeneous_fields == (
        transfer.cells[0].branches[0].field,
        transfer.cells[0].branches[1].field,
    )
    assert trace.cells[0].forced_field == transfer.cells[0].branches[2].field
    assert "not a classification" in trace.scope


def test_input_validation() -> None:
    with pytest.raises(TypeError, match="exponent"):
        power_branch_has_finite_local_energy(1.0)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="positive Fraction"):
        local_power_energy_integral(1, Fraction(0))
    with pytest.raises(ValueError, match="integral"):
        local_power_energy_integral(Fraction(1, 4), Fraction(1, 16))
    with pytest.raises(TypeError, match="transfer"):
        certify_friedrichs_physical_endpoint_trace(object())  # type: ignore[arg-type]
