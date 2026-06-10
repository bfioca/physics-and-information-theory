"""Validated moving-wall master load for the centrifugal adjoint problem.

At the physical wall ``a/R=1/5`` the static ``l=2`` Green weight is an exact
rational expression in ``atanh(1/5)``.  The wall displacement and background
stress contain the same authenticated profile slope, so they must be ranged
correlatively.  This module uses a centered Taylor model in that one slope
variable and returns an exact rational enclosure of the response trace
``gamma_B``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .centrifugal_skyrmion_affine_master_kernel import (
    centrifugal_moving_wall_master_affine_kernel,
)
from .validated_centrifugal_liouville_taylor import _CenteredTaylorModel
from .validated_centrifugal_response_residual import (
    RationalC1TrialCell,
    ValidatedWallConormalCoefficients,
    wall_endpoint_conormal_residual,
)
from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    atanh_fraction_interval,
    sqrt_fraction_interval,
)


DEFAULT_WALL_SLOPE = RationalInterval(
    Fraction(-94644972770042989, 10**18),
    Fraction(-43733242881735721, 5 * 10**17),
)


@dataclass(frozen=True)
class ValidatedWallMasterLoad:
    """Exact-rational inputs and output of the correlated wall calculation."""

    wall_ratio: Fraction
    center_regular_solution: RationalInterval
    center_regular_solution_derivative: RationalInterval
    wall_green_weight: RationalInterval
    wall_green_weight_derivative: RationalInterval
    wall_profile_derivative: RationalInterval
    wall_displacement_per_radial_field: RationalInterval
    gamma_b: RationalInterval


def _l2_center_regular_wall_intervals(
    wall_ratio: Fraction,
    *,
    atanh_terms: int,
) -> tuple[RationalInterval, RationalInterval]:
    """Enclose ``u`` and ``du/dx`` from their exact closed forms."""
    x = Fraction(wall_ratio)
    if not 0 < x < 1:
        raise ValueError("wall ratio must lie strictly between zero and one")
    atanh_x = atanh_fraction_interval(x, terms=atanh_terms)
    point = RationalInterval.point
    center = atanh_x.scale(15 * (3 - x**2) / (4 * x**2)) - 45 / (4 * x)
    center_derivative = (
        atanh_x.scale(-6 / x**3)
        + point(3 / x**2 - 1) / point(1 - x**2)
    ).scale(Fraction(15, 4)) + 45 / (4 * x**2)
    return center, center_derivative


def validated_wall_master_load(
    wall_profile_derivative: RationalInterval = DEFAULT_WALL_SLOPE,
    *,
    wall_radius: Fraction = Fraction(4),
    inverse_patch_radius_squared: Fraction = Fraction(1, 400),
    membrane_tension: Fraction = Fraction(1931779647, 10**12),
    gravitational_coupling: Fraction = Fraction(1),
    atanh_terms: int = 80,
    square_root_steps: int = 160,
    model_degree: int = 20,
    rounding_denominator: int = 10**30,
) -> ValidatedWallMasterLoad:
    """Certify the physical moving-wall trace coefficient ``gamma_B``.

    The slope is represented as ``midpoint + radius*z`` for ``-1<=z<=1``.
    Its reciprocal is formed inside the same Taylor model, retaining the
    dependence between the background wall stress and wall displacement.
    """
    if not isinstance(wall_profile_derivative, RationalInterval):
        raise TypeError("wall_profile_derivative must be a RationalInterval")
    if wall_profile_derivative.upper >= 0:
        raise ValueError("wall profile derivative must be strictly negative")
    if inverse_patch_radius_squared <= 0:
        raise ValueError("inverse patch radius squared must be positive")
    patch_radius_squared = 1 / inverse_patch_radius_squared
    patch_radius = sqrt_fraction_interval(
        patch_radius_squared,
        bisection_steps=square_root_steps,
    )
    if patch_radius.lower != patch_radius.upper:
        raise ValueError("the declared patch radius must be exactly rational")
    patch_radius_value = patch_radius.lower
    ratio = wall_radius / patch_radius_value
    center, center_derivative = _l2_center_regular_wall_intervals(
        ratio,
        atanh_terms=atanh_terms,
    )
    green_weight = center.scale(2 * patch_radius_value / 15)
    green_weight_derivative = center_derivative.scale(Fraction(2, 15))
    lapse = 1 - inverse_patch_radius_squared * wall_radius**2
    if lapse <= 0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")

    options = {
        "degree_limit": model_degree,
        "rounding_denominator": rounding_denominator,
    }
    slope_model = _CenteredTaylorModel.from_polynomial(
        RationalPolynomial(
            (
                wall_profile_derivative.midpoint,
                wall_profile_derivative.width / 2,
            )
        ),
        **options,
    )
    constant = lambda value: _CenteredTaylorModel.constant(  # noqa: E731
        value,
        **options,
    )
    displacement_model = -constant(1) / slope_model
    kernel = centrifugal_moving_wall_master_affine_kernel(
        wall_radius=constant(wall_radius),
        wall_metric_factor=constant(lapse),
        wall_metric_factor_derivative=constant(
            -2 * inverse_patch_radius_squared * wall_radius
        ),
        sqrt_wall_metric_factor=constant(
            sqrt_fraction_interval(lapse, bisection_steps=square_root_steps)
        ),
        inverse_patch_radius_squared=constant(inverse_patch_radius_squared),
        sine_profile=constant(0),
        cosine_profile=constant(1),
        profile_derivative=slope_model,
        pion_mass_squared=constant(1),
        membrane_tension=constant(membrane_tension),
        wall_displacement_per_radial_field=displacement_model,
        wall_green_weight=constant(green_weight),
        wall_green_weight_derivative=constant(green_weight_derivative),
        gravitational_coupling=constant(gravitational_coupling),
    )
    return ValidatedWallMasterLoad(
        wall_ratio=ratio,
        center_regular_solution=center,
        center_regular_solution_derivative=center_derivative,
        wall_green_weight=green_weight,
        wall_green_weight_derivative=green_weight_derivative,
        wall_profile_derivative=wall_profile_derivative,
        wall_displacement_per_radial_field=displacement_model.range(),
        gamma_b=kernel.response_wall_trace_gamma_b.range(),
    )


def loaded_adjoint_wall_residual(
    *,
    trial: RationalC1TrialCell,
    coefficients: ValidatedWallConormalCoefficients,
    master_load: ValidatedWallMasterLoad,
) -> RationalInterval:
    """Enclose the adjoint wall equation loaded by certified ``gamma_B``."""
    if coefficients.wall_radius != trial.radius.upper:
        raise ValueError("adjoint trial does not terminate at the certified wall")
    return wall_endpoint_conormal_residual(
        coefficients=coefficients,
        trial=trial,
        wall_load=master_load.gamma_b,
    )
