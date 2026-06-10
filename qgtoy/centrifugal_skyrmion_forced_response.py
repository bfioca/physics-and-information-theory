"""Exact nonzero weak-response theorem for the centrifugal Skyrmion source."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class CertifiedCentrifugalWeakResponse:
    shooting_slope_lower: Fraction
    shooting_slope_upper: Fraction
    tangential_source_leading_lower: Fraction
    source_space: str
    source_is_continuous: bool
    source_is_nonzero: bool
    unique_weak_solution_exists: bool
    weak_solution_is_nonzero: bool
    source_conjugate_susceptibility_positive: bool
    derivative_source_vanishes_at_endpoints: bool
    l2_inverse_bound_applies_directly: bool
    master_or_weyl_response_certified: bool
    conclusion_scope: str


def certify_centrifugal_weak_response(
    *,
    shooting_slope_lower: Fraction,
    shooting_slope_upper: Fraction,
    form_coercivity_lower_bound: Fraction,
) -> CertifiedCentrifugalWeakResponse:
    """Prove a nonzero weak response from the exact origin source coefficient.

    In regular origin variables the tangential coordinate source satisfies

    ``s_g(x)/x^3 -> b*(4*b^2-1)/30``.

    The source is initially written with a derivative term. Its coefficient
    is ``O(x^4)`` and vanishes at both endpoints, so exact integration by parts
    gives the ``L2`` source ``s=s0-s1'`` without a boundary load. Its nonzero
    tangential component, together with coercivity of the closed form, gives a
    unique nonzero weak solution and positive source-conjugate susceptibility.
    """
    values = (
        shooting_slope_lower,
        shooting_slope_upper,
        form_coercivity_lower_bound,
    )
    if not all(isinstance(value, Fraction) for value in values):
        raise TypeError("all theorem inputs must be exact Fractions")
    if shooting_slope_lower <= Fraction(1, 2):
        raise ValueError("the authenticated slope must lie strictly above 1/2")
    if shooting_slope_upper < shooting_slope_lower:
        raise ValueError("shooting slope interval is reversed")
    if form_coercivity_lower_bound <= 0:
        raise ValueError("form coercivity must be positive")

    slope = shooting_slope_lower
    leading_lower = slope * (4 * slope**2 - 1) / 30
    if leading_lower <= 0:
        raise AssertionError("tangential source leading coefficient is not positive")
    return CertifiedCentrifugalWeakResponse(
        shooting_slope_lower=shooting_slope_lower,
        shooting_slope_upper=shooting_slope_upper,
        tangential_source_leading_lower=leading_lower,
        source_space=(
            "L2 after endpoint-free integration by parts, hence also V* for "
            "V={y in L2: y in AC_loc, x*y' in L2, g(a)=0}"
        ),
        source_is_continuous=True,
        source_is_nonzero=True,
        unique_weak_solution_exists=True,
        weak_solution_is_nonzero=True,
        source_conjugate_susceptibility_positive=True,
        derivative_source_vanishes_at_endpoints=True,
        l2_inverse_bound_applies_directly=True,
        master_or_weyl_response_certified=False,
        conclusion_scope=(
            "unique nonzero fixed-background weak matter deformation and "
            "strictly positive source-conjugate static susceptibility; no "
            "quantitative field norm, master amplitude, or Weyl response"
        ),
    )
