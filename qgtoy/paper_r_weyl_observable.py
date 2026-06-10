"""Exact annular electric-Weyl normalization for Paper R.

Outside the compact source, the static ``ell=2`` master field is

``Psi(x)=A_ext v_H(x/R)``,  ``v_H(s)=(3-s^2)/(2s^2)``.

The Paper-R curvature normalization removes the action and state tensor, so
its dimensionless radial coefficient is precisely ``Psi``.  This module
integrates ``v_H^2`` exactly on a rational exterior annulus and transfers a
directed amplitude interval to the corresponding RMS Weyl interval.
"""

from __future__ import annotations

from fractions import Fraction

from .validated_interval import RationalInterval, sqrt_fraction_interval


def horizon_regular_mode_squared_annular_average(
    inner_radius: Fraction,
    outer_radius: Fraction,
    *,
    patch_radius: Fraction,
) -> Fraction:
    """Return the exact annular average of ``v_H(x/R)^2``.

    The antiderivative used here is

    ``-3 R^4/(4 x^3) + 3 R^2/(2 x) + x/4``.
    """
    if not 0 < inner_radius < outer_radius < patch_radius:
        raise ValueError(
            "annulus must satisfy 0 < inner_radius < outer_radius < patch_radius"
        )

    def antiderivative(radius: Fraction) -> Fraction:
        return (
            -3 * patch_radius**4 / (4 * radius**3)
            + 3 * patch_radius**2 / (2 * radius)
            + radius / 4
        )

    integral = antiderivative(outer_radius) - antiderivative(inner_radius)
    if integral <= 0:
        raise AssertionError("positive horizon-regular mode has nonpositive norm")
    return integral / (outer_radius - inner_radius)


def horizon_regular_mode_annular_rms(
    inner_radius: Fraction,
    outer_radius: Fraction,
    *,
    patch_radius: Fraction,
    sqrt_bisection_steps: int = 160,
) -> RationalInterval:
    """Enclose the annular RMS of the horizon-regular mode."""
    squared = horizon_regular_mode_squared_annular_average(
        inner_radius,
        outer_radius,
        patch_radius=patch_radius,
    )
    return sqrt_fraction_interval(squared, bisection_steps=sqrt_bisection_steps)


def annular_weyl_rms_interval(
    exterior_amplitude: RationalInterval,
    *,
    inner_radius: Fraction = Fraction(5),
    outer_radius: Fraction = Fraction(10),
    patch_radius: Fraction = Fraction(20),
    sqrt_bisection_steps: int = 160,
) -> RationalInterval:
    """Transfer ``A_ext`` to the Paper-R annular RMS coefficient ``B_W``.

    The returned lower endpoint is positive exactly when the supplied
    amplitude interval excludes zero.
    """
    mode_rms = horizon_regular_mode_annular_rms(
        inner_radius,
        outer_radius,
        patch_radius=patch_radius,
        sqrt_bisection_steps=sqrt_bisection_steps,
    )
    absolute_upper = max(
        abs(exterior_amplitude.lower), abs(exterior_amplitude.upper)
    )
    absolute_lower = (
        Fraction(0)
        if exterior_amplitude.contains_zero()
        else min(abs(exterior_amplitude.lower), abs(exterior_amplitude.upper))
    )
    return RationalInterval(
        absolute_lower * mode_rms.lower,
        absolute_upper * mode_rms.upper,
    )

