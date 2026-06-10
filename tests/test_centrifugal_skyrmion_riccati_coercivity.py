from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_riccati_coercivity import (
    centrifugal_liouville_coercivity_probe,
    centrifugal_riccati_coercivity_probe,
    exact_riccati_identity_certificate,
    riccati_completion_identity_defect,
)


def test_exact_matrix_riccati_completion_identity() -> None:
    record = exact_riccati_identity_certificate()
    assert record["identity_verified"] is True
    assert record["regular_liouville_identity_verified"] is True
    assert record["identity_defect"] == "0"


def test_completion_rejects_nonsymmetric_principal_or_multiplier() -> None:
    common = dict(
        principal=((Fraction(2), Fraction(0)), (Fraction(0), Fraction(3))),
        mixed=((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0))),
        coordinate=((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))),
        multiplier=((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0))),
        multiplier_derivative=(
            (Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(0)),
        ),
        field=(Fraction(1), Fraction(2)),
        derivative=(Fraction(3), Fraction(4)),
        spectral_target=Fraction(1, 10),
    )
    with pytest.raises(ValueError, match="principal must be symmetric"):
        riccati_completion_identity_defect(
            **{**common, "principal": ((Fraction(2), Fraction(1)), (Fraction(0), Fraction(3)))}
        )
    with pytest.raises(ValueError, match="multiplier must be symmetric"):
        riccati_completion_identity_defect(
            **{**common, "multiplier": ((Fraction(0), Fraction(1)), (Fraction(0), Fraction(0)))}
        )


def test_floating_riccati_candidate_has_large_bulk_and_wall_margins() -> None:
    record = centrifugal_riccati_coercivity_probe()
    assert record["candidate_passes_sampled_preflight"] is True
    assert record["minimum_sampled_riccati_residual_eigenvalue"] > 0.09
    assert record["allowed_wall_trace_margin"] > 0.48
    assert record["maximum_multiplier_symmetry_defect"] < 1e-12
    assert record["shifted_finite_energy_roots"][0] > 0.79
    assert record["shifted_finite_energy_roots"][1] > 2.94
    assert "do not prove" in record["claim_boundary"]


def test_explicit_liouville_candidate_supports_one_twentieth_target() -> None:
    record = centrifugal_liouville_coercivity_probe()
    assert record["candidate_passes_sampled_preflight"] is True
    assert record["minimum_sampled_completed_potential_eigenvalue"] > 0.075
    assert record["sampled_margin_above_target"] > 0.025
    assert record["allowed_wall_trace_margin"] > 0.21
    assert abs(record["minimum_completed_potential_radius"] - 1.9821) < 0.002
    assert "does not certify" in record["claim_boundary"]


def test_probe_rejects_invalid_spectral_ordering() -> None:
    with pytest.raises(ValueError, match="construction_shift"):
        centrifugal_riccati_coercivity_probe(
            target_lower_bound=0.2,
            construction_shift=0.1,
        )
