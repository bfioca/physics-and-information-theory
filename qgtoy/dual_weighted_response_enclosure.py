"""Exact dual-weighted residual enclosure for symmetric coercive forms."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class DualWeightedResponseInterval:
    corrected_estimate: Fraction
    primal_energy_dual_residual_upper: Fraction
    adjoint_energy_dual_residual_upper: Fraction
    error_upper: Fraction
    response_lower: Fraction
    response_upper: Fraction
    excludes_zero: bool
    sign: int


def certify_dual_weighted_response_interval(
    *,
    corrected_estimate: Fraction,
    primal_energy_dual_residual_upper: Fraction,
    adjoint_energy_dual_residual_upper: Fraction,
) -> DualWeightedResponseInterval:
    """Enclose ``J0+B(y)`` using primal and adjoint energy-dual residuals.

    For a symmetric positive form ``q``, let ``q(y,v)=ell(v)`` and
    ``q(v,z)=B(v)``. For conforming trials ``y_h,z_h`` define

    ``Jhat=J0+B(y_h)+R_y(z_h)``.

    If the energy-dual residual norms are bounded by ``delta_y,delta_z``, then
    the exact Galerkin identity and Cauchy--Schwarz give

    ``|J-Jhat| <= delta_y*delta_z``.
    """
    values = (
        corrected_estimate,
        primal_energy_dual_residual_upper,
        adjoint_energy_dual_residual_upper,
    )
    if not all(isinstance(value, Fraction) for value in values):
        raise TypeError("all enclosure inputs must be exact Fractions")
    if primal_energy_dual_residual_upper < 0:
        raise ValueError("primal residual upper bound must be nonnegative")
    if adjoint_energy_dual_residual_upper < 0:
        raise ValueError("adjoint residual upper bound must be nonnegative")
    error = (
        primal_energy_dual_residual_upper * adjoint_energy_dual_residual_upper
    )
    lower = corrected_estimate - error
    upper = corrected_estimate + error
    excludes_zero = lower > 0 or upper < 0
    sign = 1 if lower > 0 else -1 if upper < 0 else 0
    return DualWeightedResponseInterval(
        corrected_estimate=corrected_estimate,
        primal_energy_dual_residual_upper=primal_energy_dual_residual_upper,
        adjoint_energy_dual_residual_upper=adjoint_energy_dual_residual_upper,
        error_upper=error,
        response_lower=lower,
        response_upper=upper,
        excludes_zero=excludes_zero,
        sign=sign,
    )


def l2_residual_product_upper(
    *,
    primal_l2_residual_upper: Fraction,
    adjoint_l2_residual_upper: Fraction,
    operator_lower_bound: Fraction,
) -> Fraction:
    """Return the product error bound for endpoint-exact ``L2`` residuals."""
    values = (
        primal_l2_residual_upper,
        adjoint_l2_residual_upper,
        operator_lower_bound,
    )
    if not all(isinstance(value, Fraction) for value in values):
        raise TypeError("all residual inputs must be exact Fractions")
    if primal_l2_residual_upper < 0 or adjoint_l2_residual_upper < 0:
        raise ValueError("residual upper bounds must be nonnegative")
    if operator_lower_bound <= 0:
        raise ValueError("operator lower bound must be positive")
    return (
        primal_l2_residual_upper
        * adjoint_l2_residual_upper
        / operator_lower_bound
    )
