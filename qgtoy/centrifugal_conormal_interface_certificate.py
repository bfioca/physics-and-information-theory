"""Exact internal-conormal cancellation for the centrifugal response trials.

The strong residual is evaluated cell by cell, so a weak residual could also
contain delta distributions at internal cell boundaries.  Those terms vanish
identically when the authenticated profile is one global ``C1`` solution and
the rational trial is globally ``C1``: the conormal

``p=M(x,F,F')^T y+P(x,F,F')y'``

has the same one-sided value at every interface.  Interval boxes on adjacent
cells need not coincide; continuity of the represented functions, rather than
overlap of independently ranged boxes, is the relevant statement.
"""

from __future__ import annotations

from dataclasses import dataclass

from .centrifugal_skyrmion_rational_response_trials import RationalResponseTrial
from .validated_skyrmion_sharp_profile import ValidatedSkyrmionSharpProfileTube


@dataclass(frozen=True)
class ConormalInterfaceCertificate:
    """Structural certificate excluding all internal conormal distributions."""

    profile_certificate_id: str
    interface_count: int
    origin_join_is_c1: bool
    positive_radius_trial_is_c1: bool
    profile_is_one_global_c1_solution: bool
    coefficient_map_uses_only_profile_value_and_first_derivative: bool
    internal_conormal_jump_is_exactly_zero: bool


def certify_internal_conormal_cancellation(
    profile: ValidatedSkyrmionSharpProfileTube,
    trial: RationalResponseTrial,
) -> ConormalInterfaceCertificate:
    """Certify that cellwise strong residuals have no internal delta terms.

    The sharp tube is a replay of one authenticated Newton solution, not a
    collection of unrelated cellwise solutions.  Its cells therefore restrict
    one global ``C1`` profile.  ``trial.validate`` proves exact equality of the
    trial value and derivative across the regular-origin join and every
    positive-radius interface.  The regular conormal kernels depend only on
    ``x,F,F'`` and the trial jet ``y,y'``; no ranged second derivative enters
    the conormal itself.
    """
    if not isinstance(profile, ValidatedSkyrmionSharpProfileTube):
        raise TypeError("profile must be a ValidatedSkyrmionSharpProfileTube")
    if not isinstance(trial, RationalResponseTrial):
        raise TypeError("trial must be a RationalResponseTrial")
    trial.validate()
    cells = profile.cells
    if not cells:
        raise ValueError("profile tube has no positive-radius cells")
    if cells[0].radius.lower != profile.origin_cutoff:
        raise ValueError("profile tube does not start at its origin cutoff")
    if cells[-1].radius.upper != profile.wall_radius:
        raise ValueError("profile tube does not end at its wall")
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("profile tube cells are not contiguous")
    trial_radii = tuple(cell.radius for cell in trial.positive_radius_cells)
    profile_radii = tuple(cell.radius for cell in cells)
    if trial_radii != profile_radii:
        raise ValueError("profile and trial partitions differ")

    origin_join = (
        trial.origin.physical_endpoint_jet()
        == trial.positive_radius_cells[0].endpoint_jet(right=False)
    )
    positive_c1 = all(
        left.endpoint_jet(right=True) == right.endpoint_jet(right=False)
        for left, right in zip(
            trial.positive_radius_cells,
            trial.positive_radius_cells[1:],
        )
    )
    cancellation = origin_join and positive_c1
    return ConormalInterfaceCertificate(
        profile_certificate_id=profile.certificate_id,
        interface_count=len(cells),
        origin_join_is_c1=origin_join,
        positive_radius_trial_is_c1=positive_c1,
        profile_is_one_global_c1_solution=True,
        coefficient_map_uses_only_profile_value_and_first_derivative=True,
        internal_conormal_jump_is_exactly_zero=cancellation,
    )
