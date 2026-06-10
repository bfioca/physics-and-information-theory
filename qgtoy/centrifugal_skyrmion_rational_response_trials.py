"""Exact rational trial archives for the centrifugal response problem.

The floating primal-adjoint feasibility calculation produces nodal Galerkin
solutions.  This module converts those samples into exact, globally ``C1``
cubic-Hermite trials on an arbitrary rational partition.  Shared endpoint
values and derivatives are rounded once, so conformity is an exact algebraic
property rather than a floating tolerance check.

The interval touching the center is represented separately in the regular
variables ``t=x^2``, ``g=x v(t)``, and ``f=x[-v(t)+t u(t)]``.  The positive-
radius cells therefore start at the authenticated origin cutoff and can be
passed directly to :mod:`qgtoy.validated_centrifugal_response_residual`.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb, isfinite
from typing import Mapping, Sequence

import numpy as np

from .centrifugal_skyrmion_master_adjoint import (
    _ExteriorAmplitudeFunctional,
    _fields_from_vector,
)
from .centrifugal_skyrmion_variational import (
    assemble_centrifugal_quadrupole_variational_system,
)
from .validated_centrifugal_response_residual import (
    RationalC1TrialCell,
    ValidatedStrongResidualCell,
    profile_jet_cell_from_sharp_replay,
    validate_rational_c1_trial_cells,
    validated_conormal_strong_cell_from_profile,
    validated_strong_residual_cell,
)
from .validated_interval import RationalInterval, RationalPolynomial
from .validated_skyrmion_au3 import exact_fraction_from_text
from .validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpProfileTube,
)


def _positive_integer(name: str, value: int, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer at least {minimum}")
    return value


def _rounded_fraction(value: float, denominator: int) -> Fraction:
    if not isfinite(value):
        raise ValueError("trial samples must be finite")
    return Fraction(round(value * denominator), denominator)


def _hermite_coefficients(
    left_value: Fraction,
    right_value: Fraction,
    left_derivative: Fraction,
    right_derivative: Fraction,
    width: Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    difference = right_value - left_value
    return (
        left_value,
        width * left_derivative,
        3 * difference - width * (2 * left_derivative + right_derivative),
        -2 * difference + width * (left_derivative + right_derivative),
    )


def _cubic_hermite_sample(
    radii: np.ndarray,
    values: np.ndarray,
    derivatives: np.ndarray,
    radius: float,
) -> tuple[float, float]:
    if radius < float(radii[0]) or radius > float(radii[-1]):
        raise ValueError("trial target radius lies outside floating sample domain")
    if radius == float(radii[-1]):
        index = len(radii) - 2
        u = 1.0
    else:
        index = int(np.searchsorted(radii, radius, side="right") - 1)
        index = max(0, min(index, len(radii) - 2))
        width = float(radii[index + 1] - radii[index])
        u = (radius - float(radii[index])) / width
    width = float(radii[index + 1] - radii[index])
    left = float(values[index])
    right = float(values[index + 1])
    left_slope = float(derivatives[index])
    right_slope = float(derivatives[index + 1])
    coefficients = (
        left,
        width * left_slope,
        3.0 * (right - left) - width * (2.0 * left_slope + right_slope),
        -2.0 * (right - left) + width * (left_slope + right_slope),
    )
    value = sum(coefficient * u**power for power, coefficient in enumerate(coefficients))
    derivative_u = sum(
        power * coefficient * u ** (power - 1)
        for power, coefficient in enumerate(coefficients)
        if power > 0
    )
    return value, derivative_u / width


@dataclass(frozen=True)
class RegularOriginTrial:
    """Exact regular trial on ``0 <= t=x^2 <= cutoff^2``."""

    cutoff: Fraction
    u_polynomial: RationalPolynomial
    v_polynomial: RationalPolynomial

    def physical_endpoint_jet(
        self,
    ) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
        """Return ``((f,g),(f',g'))`` at the positive cutoff."""
        x = self.cutoff
        t = x**2
        u = self.u_polynomial.evaluate(t).lower
        u_t = self.u_polynomial.derivative().evaluate(t).lower
        v = self.v_polynomial.evaluate(t).lower
        v_t = self.v_polynomial.derivative().evaluate(t).lower
        f = x * (-v + t * u)
        g = x * v
        f_derivative = -v - 2 * t * v_t + 3 * t * u + 2 * t**2 * u_t
        g_derivative = v + 2 * t * v_t
        return (f, g), (f_derivative, g_derivative)


@dataclass(frozen=True)
class RationalResponseTrial:
    """One exact primal or adjoint trial over the full radial domain."""

    name: str
    origin: RegularOriginTrial
    positive_radius_cells: tuple[RationalC1TrialCell, ...]

    def validate(self) -> None:
        validate_rational_c1_trial_cells(self.positive_radius_cells)
        first = self.positive_radius_cells[0]
        if first.radius.lower != self.origin.cutoff:
            raise ValueError("origin trial and positive-radius cells do not meet")
        if self.origin.physical_endpoint_jet() != first.endpoint_jet(right=False):
            raise ValueError("origin trial does not join the positive-radius trial")


@dataclass(frozen=True)
class RationalResponseTrialPair:
    """Exact primal and adjoint trials generated from one floating solve."""

    primal: RationalResponseTrial
    adjoint: RationalResponseTrial
    node_count: int
    quadrature_order: int
    profile_step: float
    rounding_denominator: int

    def validate(self) -> None:
        self.primal.validate()
        self.adjoint.validate()
        if tuple(cell.radius for cell in self.primal.positive_radius_cells) != tuple(
            cell.radius for cell in self.adjoint.positive_radius_cells
        ):
            raise ValueError("primal and adjoint trial partitions differ")


def _restrict_polynomial_to_equal_subcell(
    polynomial: RationalPolynomial,
    *,
    subdivision: int,
    subdivisions: int,
) -> RationalPolynomial:
    """Compose ``p(u)`` with ``u=(subdivision+v)/subdivisions`` exactly."""
    subdivisions = _positive_integer("subdivisions", subdivisions)
    if (
        isinstance(subdivision, bool)
        or not isinstance(subdivision, int)
        or not 0 <= subdivision < subdivisions
    ):
        raise ValueError("subdivision index is outside the equal partition")
    offset = Fraction(subdivision, subdivisions)
    scale = Fraction(1, subdivisions)
    coefficients = [Fraction(0) for _ in polynomial.coefficients]
    for power, coefficient in enumerate(polynomial.coefficients):
        for local_power in range(power + 1):
            coefficients[local_power] += (
                coefficient
                * comb(power, local_power)
                * offset ** (power - local_power)
                * scale**local_power
            )
    return RationalPolynomial(tuple(coefficients))


def refine_rational_response_trial(
    trial: RationalResponseTrial,
    *,
    subdivisions_per_cell: int,
) -> RationalResponseTrial:
    """Restrict an exact trial to equal subcells without changing its field."""
    subdivisions = _positive_integer(
        "subdivisions_per_cell", subdivisions_per_cell
    )
    refined = []
    for cell in trial.positive_radius_cells:
        width = cell.radius.width / subdivisions
        for subdivision in range(subdivisions):
            radius = RationalInterval(
                cell.radius.lower + width * subdivision,
                cell.radius.lower + width * (subdivision + 1),
            )
            refined.append(
                RationalC1TrialCell(
                    radius=radius,
                    radial_field=_restrict_polynomial_to_equal_subcell(
                        cell.radial_field,
                        subdivision=subdivision,
                        subdivisions=subdivisions,
                    ),
                    tangential_field=_restrict_polynomial_to_equal_subcell(
                        cell.tangential_field,
                        subdivision=subdivision,
                        subdivisions=subdivisions,
                    ),
                )
            )
    result = RationalResponseTrial(trial.name, trial.origin, tuple(refined))
    result.validate()
    return result


def _regular_origin_trial(
    cutoff: Fraction,
    endpoint_jet: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
) -> RegularOriginTrial:
    (f, g), (f_derivative, g_derivative) = endpoint_jet
    t = cutoff**2
    v = g / cutoff
    v_t = (g_derivative - v) / (2 * t)
    u = (f / cutoff + v) / t
    u_t = (f_derivative + v + 2 * t * v_t - 3 * t * u) / (2 * t**2)
    return RegularOriginTrial(
        cutoff=cutoff,
        u_polynomial=RationalPolynomial((u - u_t * t, u_t)),
        v_polynomial=RationalPolynomial((v - v_t * t, v_t)),
    )


def _trial_from_floating_fields(
    *,
    name: str,
    sample_radii: np.ndarray,
    fields: np.ndarray,
    target_cells: tuple[RationalInterval, ...],
    rounding_denominator: int,
) -> RationalResponseTrial:
    if not target_cells or target_cells[0].lower <= 0:
        raise ValueError("target cells must start at a positive radius")
    for left, right in zip(target_cells, target_cells[1:]):
        if left.upper != right.lower:
            raise ValueError("target cells must be contiguous")
    derivatives = np.column_stack(
        tuple(
            np.gradient(fields[:, component], sample_radii, edge_order=2)
            for component in range(2)
        )
    )
    endpoints = (target_cells[0].lower,) + tuple(cell.upper for cell in target_cells)
    rational_jets: list[
        tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]
    ] = []
    for endpoint in endpoints:
        values = []
        slopes = []
        for component in range(2):
            value, slope = _cubic_hermite_sample(
                sample_radii,
                fields[:, component],
                derivatives[:, component],
                float(endpoint),
            )
            values.append(_rounded_fraction(value, rounding_denominator))
            slopes.append(_rounded_fraction(slope, rounding_denominator))
        rational_jets.append(
            ((values[0], values[1]), (slopes[0], slopes[1]))
        )
    cells = []
    for radius, left, right in zip(
        target_cells, rational_jets[:-1], rational_jets[1:], strict=True
    ):
        fields_polynomials = []
        for component in range(2):
            fields_polynomials.append(
                RationalPolynomial(
                    _hermite_coefficients(
                        left[0][component],
                        right[0][component],
                        left[1][component],
                        right[1][component],
                        radius.width,
                    )
                )
            )
        cells.append(
            RationalC1TrialCell(
                radius=radius,
                radial_field=fields_polynomials[0],
                tangential_field=fields_polynomials[1],
            )
        )
    # The Galerkin essential trace is exactly zero. Preserve that exact datum
    # even if a platform's interpolation returns a signed rounding residue.
    last = cells[-1]
    wall_values, wall_slopes = last.endpoint_jet(right=True)
    if wall_values[1] != 0:
        corrected = RationalPolynomial(
            _hermite_coefficients(
                cells[-1].endpoint_jet(right=False)[0][1],
                Fraction(0),
                cells[-1].endpoint_jet(right=False)[1][1],
                wall_slopes[1],
                last.radius.width,
            )
        )
        cells[-1] = RationalC1TrialCell(
            radius=last.radius,
            radial_field=last.radial_field,
            tangential_field=corrected,
        )
    origin = _regular_origin_trial(target_cells[0].lower, cells[0].endpoint_jet(right=False))
    trial = RationalResponseTrial(name, origin, tuple(cells))
    trial.validate()
    return trial


def build_rational_response_trial_pair(
    target_cells: Sequence[RationalInterval],
    *,
    node_count: int = 81,
    quadrature_order: int = 5,
    profile_step: float = 0.001,
    rounding_denominator: int = 10**12,
) -> RationalResponseTrialPair:
    """Solve the floating systems and fit exact trials on ``target_cells``."""
    node_count = _positive_integer("node_count", node_count, 5)
    quadrature_order = _positive_integer("quadrature_order", quadrature_order, 2)
    rounding_denominator = _positive_integer(
        "rounding_denominator", rounding_denominator
    )
    if not isfinite(profile_step) or profile_step <= 0:
        raise ValueError("profile_step must be finite and positive")
    partition = tuple(target_cells)
    assembled = assemble_centrifugal_quadrupole_variational_system(
        node_count=node_count,
        quadrature_order=quadrature_order,
        profile_step=profile_step,
    )
    stiffness = np.asarray(assembled["stiffness_matrix"], dtype=float)
    load = np.asarray(assembled["load_vector"], dtype=float)
    functional = _ExteriorAmplitudeFunctional(assembled)
    _, output, _ = functional.affine_data()
    primal_vector = np.linalg.solve(stiffness, load)
    adjoint_vector = np.linalg.solve(stiffness, output)
    dof_map = np.asarray(assembled["degree_of_freedom_map"], dtype=int)
    radii = np.asarray(assembled["radii"], dtype=float)
    pair = RationalResponseTrialPair(
        primal=_trial_from_floating_fields(
            name="primal",
            sample_radii=radii,
            fields=_fields_from_vector(primal_vector, dof_map),
            target_cells=partition,
            rounding_denominator=rounding_denominator,
        ),
        adjoint=_trial_from_floating_fields(
            name="adjoint",
            sample_radii=radii,
            fields=_fields_from_vector(adjoint_vector, dof_map),
            target_cells=partition,
            rounding_denominator=rounding_denominator,
        ),
        node_count=node_count,
        quadrature_order=quadrature_order,
        profile_step=profile_step,
        rounding_denominator=rounding_denominator,
    )
    pair.validate()
    return pair


def validated_positive_radius_primal_residuals(
    profile: ValidatedSkyrmionSharpProfileTube,
    trial: RationalResponseTrial,
    *,
    trigonometric_terms: int = 12,
) -> tuple[ValidatedStrongResidualCell, ...]:
    """Evaluate the physical primal strong residual on all sharp cells."""
    trial.validate()
    if len(profile.cells) != len(trial.positive_radius_cells):
        raise ValueError("profile and trial cell counts differ")
    residuals = []
    for profile_cell, trial_cell in zip(
        profile.cells, trial.positive_radius_cells, strict=True
    ):
        if profile_cell.radius != trial_cell.radius:
            raise ValueError("profile and trial partitions differ")
        coefficients = validated_conormal_strong_cell_from_profile(
            profile_jet_cell_from_sharp_replay(profile_cell),
            curvature=profile.curvature,
            pion_mass_squared=profile.pion_mass_squared,
            trigonometric_terms=trigonometric_terms,
        )
        residuals.append(validated_strong_residual_cell(coefficients, trial_cell))
    return tuple(residuals)


def _fraction_record(value: Fraction) -> str:
    return str(value)


def _polynomial_record(polynomial: RationalPolynomial) -> list[str]:
    return [_fraction_record(value) for value in polynomial.coefficients]


def rational_response_trial_pair_to_record(
    pair: RationalResponseTrialPair,
) -> dict[str, object]:
    """Serialize a trial pair without losing rational data."""
    pair.validate()

    def trial_record(trial: RationalResponseTrial) -> dict[str, object]:
        return {
            "name": trial.name,
            "origin": {
                "cutoff": str(trial.origin.cutoff),
                "u_coefficients_in_t": _polynomial_record(
                    trial.origin.u_polynomial
                ),
                "v_coefficients_in_t": _polynomial_record(
                    trial.origin.v_polynomial
                ),
            },
            "positive_radius_cells": [
                {
                    "radius": {
                        "lower": str(cell.radius.lower),
                        "upper": str(cell.radius.upper),
                    },
                    "radial_coefficients_in_u": _polynomial_record(
                        cell.radial_field
                    ),
                    "tangential_coefficients_in_u": _polynomial_record(
                        cell.tangential_field
                    ),
                }
                for cell in trial.positive_radius_cells
            ],
        }

    return {
        "parameters": {
            "node_count": pair.node_count,
            "quadrature_order": pair.quadrature_order,
            "profile_step": pair.profile_step,
            "rounding_denominator": pair.rounding_denominator,
        },
        "primal": trial_record(pair.primal),
        "adjoint": trial_record(pair.adjoint),
    }


def rational_response_trial_pair_from_record(
    record: Mapping[str, object],
) -> RationalResponseTrialPair:
    """Load and exactly validate a serialized trial pair."""
    parameters = record.get("parameters")
    if not isinstance(parameters, Mapping):
        raise TypeError("trial-pair parameters are missing")

    def polynomial(values: object) -> RationalPolynomial:
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise TypeError("polynomial coefficients must be a sequence")
        if not all(isinstance(value, str) for value in values):
            raise TypeError("polynomial coefficients must be rational strings")
        return RationalPolynomial(tuple(exact_fraction_from_text(value) for value in values))

    def trial(value: object) -> RationalResponseTrial:
        if not isinstance(value, Mapping):
            raise TypeError("trial record must be a mapping")
        name = value.get("name")
        origin_record = value.get("origin")
        archived_cells = value.get("positive_radius_cells")
        if not isinstance(name, str) or not isinstance(origin_record, Mapping):
            raise TypeError("trial name or origin record is invalid")
        if not isinstance(archived_cells, Sequence) or isinstance(
            archived_cells, (str, bytes)
        ):
            raise TypeError("trial cells must be a sequence")
        origin = RegularOriginTrial(
            cutoff=exact_fraction_from_text(str(origin_record.get("cutoff"))),
            u_polynomial=polynomial(origin_record.get("u_coefficients_in_t")),
            v_polynomial=polynomial(origin_record.get("v_coefficients_in_t")),
        )
        cells = []
        for item in archived_cells:
            if not isinstance(item, Mapping):
                raise TypeError("trial cell must be a mapping")
            radius = item.get("radius")
            if not isinstance(radius, Mapping):
                raise TypeError("trial cell radius must be a mapping")
            cells.append(
                RationalC1TrialCell(
                    radius=RationalInterval(
                        exact_fraction_from_text(str(radius.get("lower"))),
                        exact_fraction_from_text(str(radius.get("upper"))),
                    ),
                    radial_field=polynomial(item.get("radial_coefficients_in_u")),
                    tangential_field=polynomial(
                        item.get("tangential_coefficients_in_u")
                    ),
                )
            )
        result = RationalResponseTrial(name, origin, tuple(cells))
        result.validate()
        return result

    pair = RationalResponseTrialPair(
        primal=trial(record.get("primal")),
        adjoint=trial(record.get("adjoint")),
        node_count=int(parameters.get("node_count", 0)),
        quadrature_order=int(parameters.get("quadrature_order", 0)),
        profile_step=float(parameters.get("profile_step", 0.0)),
        rounding_denominator=int(parameters.get("rounding_denominator", 0)),
    )
    pair.validate()
    return pair
