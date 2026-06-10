"""Representation-safe weak wall terms for the Paper-R response.

The signed estimator and the correlation-preserving adjoint certificate keep
their bulk residuals in weak form.  Their wall completion therefore contains
only the explicit form and load traces.  A conormal residual belongs instead
to an all-strong bulk representation and must not be mixed into these terms.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .centrifugal_skyrmion_rational_response_trials import RationalResponseTrial
from .validated_centrifugal_response_residual import (
    ValidatedWallConormalCoefficients,
)
from .validated_centrifugal_wall_master_load import ValidatedWallMasterLoad
from .validated_interval import RationalInterval


@dataclass(frozen=True)
class PaperRWeakWallContribution:
    """Explicit wall terms compatible with weak bulk residuals."""

    primal_radial_value: Fraction
    adjoint_radial_value: Fraction
    master_wall_contribution: RationalInterval
    primal_residual_wall_contribution: RationalInterval
    corrected_estimator_wall_contribution: RationalInterval
    adjoint_weak_wall_residual: RationalInterval
    conormal_residual_included: bool


def certify_paper_r_weak_wall_contribution(
    *,
    primal_trial: RationalResponseTrial,
    adjoint_trial: RationalResponseTrial,
    coefficients: ValidatedWallConormalCoefficients,
    master_load: ValidatedWallMasterLoad,
    primal_wall_load: RationalInterval = RationalInterval.point(0),
) -> PaperRWeakWallContribution:
    """Return the weak wall completion of the corrected estimator.

    If ``k`` is the radial Robin form coefficient, the retained weak bulk
    representation gives

    ``B_wall(y_h) = gamma_B y_f(a)``

    and

    ``R_y(z_h)_wall = (ell_wall-k y_f(a)) z_f(a)``.

    Hence the corrected wall term is
    ``gamma_B*y_f + (ell_wall-k*y_f)*z_f``.  The loaded weak adjoint wall
    coefficient is ``gamma_B-k*z_f``.  Neither expression contains the trial
    conormal.
    """
    if not isinstance(primal_wall_load, RationalInterval):
        raise TypeError("primal_wall_load must be a RationalInterval")
    primal_trial.validate()
    adjoint_trial.validate()
    if (
        coefficients.wall_radius
        != primal_trial.positive_radius_cells[-1].radius.upper
    ):
        raise ValueError("primal trial does not end at the certified wall")
    if (
        coefficients.wall_radius
        != adjoint_trial.positive_radius_cells[-1].radius.upper
    ):
        raise ValueError("adjoint trial does not end at the certified wall")

    primal_value, _ = primal_trial.positive_radius_cells[-1].endpoint_jet(
        right=True
    )
    adjoint_value, _ = adjoint_trial.positive_radius_cells[-1].endpoint_jet(
        right=True
    )
    y_f = primal_value[0]
    z_f = adjoint_value[0]
    master = master_load.gamma_b.scale(y_f)
    residual = (
        primal_wall_load
        - coefficients.wall_form_coefficient.scale(y_f)
    ).scale(z_f)
    adjoint_wall = (
        master_load.gamma_b
        - coefficients.wall_form_coefficient.scale(z_f)
    )
    corrected = master + residual
    if primal_wall_load == RationalInterval.point(0):
        factored = adjoint_wall.scale(y_f)
        if corrected != factored:
            raise AssertionError("weak wall factorizations disagree")
    return PaperRWeakWallContribution(
        primal_radial_value=y_f,
        adjoint_radial_value=z_f,
        master_wall_contribution=master,
        primal_residual_wall_contribution=residual,
        corrected_estimator_wall_contribution=corrected,
        adjoint_weak_wall_residual=adjoint_wall,
        conormal_residual_included=False,
    )
