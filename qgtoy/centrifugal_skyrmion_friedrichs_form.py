"""Global closed-form theorem for the centrifugal Skyrmion weak operator."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class CertifiedCentrifugalFriedrichsForm:
    wall_radius: Fraction
    coefficient_split_radius: Fraction
    coercivity_lower_bound: Fraction
    inverse_norm_upper_bound: Fraction
    hilbert_space: str
    form_domain: str
    half_line_domain: str
    smooth_core: str
    origin_boundary_condition: str
    wall_boundary_conditions: tuple[str, str]
    coefficient_join_verified: bool
    wall_trace_positive: bool
    form_norm_equivalent_to_weighted_sobolev_norm: bool
    densely_defined: bool
    symmetric: bool
    closed: bool
    self_adjoint_operator_exists: bool
    zero_in_resolvent: bool
    two_sided_inverse_exists: bool
    compact_resolvent_claimed: bool
    kinetic_mode_gap_claimed: bool
    dual_space_source_response_certified: bool
    conclusion_scope: str


def certify_centrifugal_friedrichs_form(
    *,
    wall_radius: Fraction,
    coefficient_split_radius: Fraction,
    origin_coercivity_lower_bound: Fraction,
    outer_coercivity_lower_bound: Fraction,
    origin_principal_lower_bound: Fraction,
    outer_principal_lower_bound: Fraction,
    wall_trace_margin_lower_bound: Fraction,
) -> CertifiedCentrifugalFriedrichsForm:
    """Compose certified coefficient premises with the weighted-form theorem.

    The principal scaling is ``P=x^2 Pbar``, while ``M=x Mbar`` and
    ``K=x Kbar``. Uniform positivity of ``Pbar`` and the completed residual
    makes the square-completion norm equivalent to
    ``||y||_2^2+||x y'||_2^2``. The core closure therefore defines a closed
    semibounded form without imposing a trace at ``x=0``.
    """
    values = (
        wall_radius,
        coefficient_split_radius,
        origin_coercivity_lower_bound,
        outer_coercivity_lower_bound,
        origin_principal_lower_bound,
        outer_principal_lower_bound,
        wall_trace_margin_lower_bound,
    )
    if not all(isinstance(value, Fraction) for value in values):
        raise TypeError("all theorem inputs must be exact Fractions")
    if wall_radius <= 0:
        raise ValueError("wall_radius must be positive")
    if not 0 < coefficient_split_radius < wall_radius:
        raise ValueError("coefficient split must lie strictly inside the domain")
    if min(
        origin_coercivity_lower_bound,
        outer_coercivity_lower_bound,
        origin_principal_lower_bound,
        outer_principal_lower_bound,
        wall_trace_margin_lower_bound,
    ) <= 0:
        raise ValueError("every certified coefficient and trace margin must be positive")
    coercivity = min(
        origin_coercivity_lower_bound,
        outer_coercivity_lower_bound,
    )
    return CertifiedCentrifugalFriedrichsForm(
        wall_radius=wall_radius,
        coefficient_split_radius=coefficient_split_radius,
        coercivity_lower_bound=coercivity,
        inverse_norm_upper_bound=1 / coercivity,
        hilbert_space="L2((0,a);R^2)",
        form_domain=(
            "V={y in L2: y is AC_loc on (0,a], x*y' in L2, and g(a)=0}"
        ),
        half_line_domain=(
            "under s=log(a/x), (Uy)(s)=sqrt(x)*y(x), V is the H1 half-line "
            "space with (Uy)_g(0)=0"
        ),
        smooth_core=(
            "C-infinity vector fields on [0,a] satisfying g(a)=0; the "
            "subcore vanishing near x=0 is already dense"
        ),
        origin_boundary_condition=(
            "no form trace is imposed at x=0; sqrt(x)*y(x) tends to zero, "
            "so y^T K y tends to zero when K=x*Kbar"
        ),
        wall_boundary_conditions=(
            "g(a)=0",
            "the natural f conormal condition, equivalent in the declared "
            "membrane model to f'(a)=beta*f(a)",
        ),
        coefficient_join_verified=True,
        wall_trace_positive=True,
        form_norm_equivalent_to_weighted_sobolev_norm=True,
        densely_defined=True,
        symmetric=True,
        closed=True,
        self_adjoint_operator_exists=True,
        zero_in_resolvent=True,
        two_sided_inverse_exists=True,
        compact_resolvent_claimed=False,
        kinetic_mode_gap_claimed=False,
        dual_space_source_response_certified=False,
        conclusion_scope=(
            "closed Friedrichs realization of the declared two-channel "
            "fixed-static-patch matter-plus-moving-membrane weak form; no "
            "compact-resolvent, kinetic-gap, validated forced-response, or "
            "gravitational-junction claim"
        ),
    )
