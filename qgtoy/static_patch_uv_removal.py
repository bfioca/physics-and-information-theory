"""Ultraviolet removal for the conformal static-patch s-wave.

Compact Cauchy data for which the ``n``-th distributional derivative of the
zero extension is a finite measure, with ``n>=2``, have unitary sine transforms
bounded by

    |fhat(k)| <= sqrt(2/pi) ||D^n f||_TV / k^n.

These bounds make the full half-line symplectic form, thermal covariance, and
unequal-time KMS two-point distribution absolutely convergent.  The explicit
tail estimates below prove removal of the hard momentum bandlimit.  The
executable cubic polynomial bumps are a concrete C2 subclass with ``n=4``;
the same formulas apply at every order to smooth compact data.
"""

from __future__ import annotations

from math import comb, exp, expm1, factorial, isfinite, pi, sqrt

from .static_patch_phase_space import (
    CompactPolynomialBump,
    PhaseSpaceTest,
    continuum_phase_space_covariance,
    continuum_phase_space_symplectic_form,
    continuum_unequal_time_wightman,
    polynomial_bump_moment,
    polynomial_bump_normalization,
)
from .static_patch_weyl_regulator import de_sitter_inverse_temperature


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def polynomial_bump_derivative_l1_bound(
    bump: CompactPolynomialBump,
    derivative_order: int,
) -> float:
    """Coefficientwise upper bound for ``||bump^(n)||_1``.

    With ``t=(x-a)/(b-a)``, the unnormalized bump is
    ``(b-a)^(2p) t^p(1-t)^p``.  Expanding the derivative polynomial and using
    the triangle inequality gives a closed, dependency-free seminorm bound.
    Boundary traces vanish through order ``p-1``, so integration by parts is
    valid for every ``n<=p``.
    """
    if (
        isinstance(derivative_order, bool)
        or not isinstance(derivative_order, int)
        or derivative_order < 1
        or derivative_order > bump.power
    ):
        raise ValueError("derivative_order must lie from one through bump.power")
    power = bump.power
    width = bump.support_end - bump.support_start
    coefficient_integral_bound = 0.0
    for index in range(power + 1):
        exponent = power + index
        if exponent < derivative_order:
            continue
        derivative_coefficient = (
            comb(power, index)
            * factorial(exponent)
            / factorial(exponent - derivative_order)
        )
        coefficient_integral_bound += derivative_coefficient / (
            exponent - derivative_order + 1
        )
    return (
        polynomial_bump_normalization(bump)
        * width ** (2 * power - derivative_order + 1)
        * coefficient_integral_bound
    )


def polynomial_bump_distributional_derivative_tv_bound(
    bump: CompactPolynomialBump,
) -> float:
    """Bound the total variation of the zero extension's ``D^(p+1)``.

    The zero extension is ``C^(p-1)`` and its ``p``-th derivative has endpoint
    jumps.  Thus ``D^(p+1)`` is a finite signed measure consisting of an
    interior polynomial density plus two endpoint atoms.
    """
    power = bump.power
    width = bump.support_end - bump.support_start
    pth_coefficients = tuple(
        ((-1) ** index)
        * comb(power, index)
        * factorial(power + index)
        / factorial(index)
        for index in range(power + 1)
    )
    left_jump = abs(pth_coefficients[0])
    right_jump = abs(sum(pth_coefficients))
    interior_variation_bound = sum(
        abs(index * coefficient) / index
        for index, coefficient in enumerate(pth_coefficients)
        if index >= 1
    )
    return (
        polynomial_bump_normalization(bump)
        * width**power
        * (left_jump + right_jump + interior_variation_bound)
    )


def sine_transform_decay_constant(
    bump: CompactPolynomialBump,
    derivative_order: int,
) -> float:
    """Return ``A_n`` such that ``|bump_hat(k)|<=A_n/k^n``."""
    if derivative_order == bump.power + 1:
        derivative_bound = polynomial_bump_distributional_derivative_tv_bound(bump)
    else:
        derivative_bound = polynomial_bump_derivative_l1_bound(
            bump,
            derivative_order,
        )
    return sqrt(2.0 / pi) * derivative_bound


def sine_transform_ir_constant(bump: CompactPolynomialBump) -> float:
    """Return ``I`` such that ``|bump_hat(k)|<=I k`` near zero and globally."""
    return sqrt(2.0 / pi) * polynomial_bump_moment(bump, 1)


def phase_space_ir_constants(test: PhaseSpaceTest) -> tuple[float, float]:
    """Field and momentum constants in the linear infrared sine bound."""
    field_constant = 0.0
    momentum_constant = 0.0
    if test.field_bump is not None:
        field_constant = abs(test.field_scale) * sine_transform_ir_constant(
            test.field_bump
        )
    if test.momentum_bump is not None:
        momentum_constant = abs(test.momentum_scale) * sine_transform_ir_constant(
            test.momentum_bump
        )
    return field_constant, momentum_constant


def covariance_zero_momentum_limit(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    radius: float,
) -> float:
    """Exact removable ``k=0`` limit of the thermal covariance integrand."""
    _validate_positive("radius", radius)
    if first.field_bump is None or second.field_bump is None:
        return 0.0
    first_moment = first.field_scale * polynomial_bump_moment(
        first.field_bump, 1
    )
    second_moment = second.field_scale * polynomial_bump_moment(
        second.field_bump, 1
    )
    beta = de_sitter_inverse_temperature(radius)
    return 2.0 * first_moment * second_moment / (pi * beta)


def phase_space_decay_constants(
    test: PhaseSpaceTest,
    derivative_order: int,
) -> tuple[float, float]:
    """Field and momentum sine-transform decay constants."""
    field_constant = 0.0
    momentum_constant = 0.0
    if test.field_bump is not None:
        field_constant = abs(test.field_scale) * sine_transform_decay_constant(
            test.field_bump,
            derivative_order,
        )
    if test.momentum_bump is not None:
        momentum_constant = abs(
            test.momentum_scale
        ) * sine_transform_decay_constant(
            test.momentum_bump,
            derivative_order,
        )
    return field_constant, momentum_constant


def _thermal_coth(beta_times_cutoff: float) -> float:
    """Stable ``coth(beta*K/2)``."""
    if beta_times_cutoff > 50.0:
        return 1.0
    return 1.0 + 2.0 / expm1(beta_times_cutoff)


def symplectic_uv_tail_bound(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    momentum_cutoff: float,
    derivative_order: int = 4,
) -> float:
    """Bound the omitted ``k>K`` symplectic integral."""
    _validate_positive("momentum_cutoff", momentum_cutoff)
    if derivative_order < 1:
        raise ValueError("derivative_order must be positive")
    first_field, first_momentum = phase_space_decay_constants(
        first, derivative_order
    )
    second_field, second_momentum = phase_space_decay_constants(
        second, derivative_order
    )
    numerator = (
        first_field * second_momentum + first_momentum * second_field
    )
    return numerator / (
        (2 * derivative_order - 1)
        * momentum_cutoff ** (2 * derivative_order - 1)
    )


def covariance_uv_tail_bound(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    radius: float,
    momentum_cutoff: float,
    derivative_order: int = 4,
) -> float:
    """Bound the omitted thermal covariance integral above ``K``."""
    _validate_positive("radius", radius)
    _validate_positive("momentum_cutoff", momentum_cutoff)
    if derivative_order < 2:
        raise ValueError("derivative_order must be at least two")
    first_field, first_momentum = phase_space_decay_constants(
        first, derivative_order
    )
    second_field, second_momentum = phase_space_decay_constants(
        second, derivative_order
    )
    beta = de_sitter_inverse_temperature(radius)
    thermal_factor = _thermal_coth(beta * momentum_cutoff)
    field_tail = first_field * second_field / (
        2 * derivative_order * momentum_cutoff ** (2 * derivative_order)
    )
    momentum_tail = first_momentum * second_momentum / (
        (2 * derivative_order - 2)
        * momentum_cutoff ** (2 * derivative_order - 2)
    )
    return 0.5 * thermal_factor * (field_tail + momentum_tail)


def wightman_uv_tail_bound(
    first: PhaseSpaceTest,
    second: PhaseSpaceTest,
    *,
    radius: float,
    momentum_cutoff: float,
    derivative_order: int = 4,
) -> float:
    """Uniform closed-KMS-strip bound for the omitted two-point tail."""
    _validate_positive("radius", radius)
    _validate_positive("momentum_cutoff", momentum_cutoff)
    if derivative_order < 2:
        raise ValueError("derivative_order must be at least two")
    first_field, first_momentum = phase_space_decay_constants(
        first, derivative_order
    )
    second_field, second_momentum = phase_space_decay_constants(
        second, derivative_order
    )
    beta = de_sitter_inverse_temperature(radius)
    thermal_factor = 0.5 * _thermal_coth(beta * momentum_cutoff)
    field_tail = first_field * second_field / (
        2 * derivative_order * momentum_cutoff ** (2 * derivative_order)
    )
    mixed_tail = (
        first_field * second_momentum + first_momentum * second_field
    ) / (
        (2 * derivative_order - 1)
        * momentum_cutoff ** (2 * derivative_order - 1)
    )
    momentum_tail = first_momentum * second_momentum / (
        (2 * derivative_order - 2)
        * momentum_cutoff ** (2 * derivative_order - 2)
    )
    return thermal_factor * (field_tail + mixed_tail + momentum_tail)


def weyl_characteristic_uv_tail_bound(
    test: PhaseSpaceTest,
    *,
    radius: float,
    momentum_cutoff: float,
    derivative_order: int = 4,
) -> float:
    """Bound the cutoff error in ``exp[-mu(F,F)/2]``."""
    return 0.5 * covariance_uv_tail_bound(
        test,
        test,
        radius=radius,
        momentum_cutoff=momentum_cutoff,
        derivative_order=derivative_order,
    )


def static_patch_uv_removal_certificate(
    *,
    radius: float = 1.0,
    minimum_cutoff: float = 8.0,
    steps: int = 4,
    derivative_order: int = 4,
) -> dict[str, object]:
    """Audit quantitative removal of the s-wave UV bandlimit."""
    _validate_positive("radius", radius)
    _validate_positive("minimum_cutoff", minimum_cutoff)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 3 or steps > 6:
        raise ValueError("steps must be an integer from three through six")
    if derivative_order != 4:
        raise ValueError("the executable certificate currently uses derivative_order=4")

    left = CompactPolynomialBump(0.25 * radius, 0.75 * radius, 3)
    right = CompactPolynomialBump(1.0 * radius, 1.5 * radius, 3)
    first = PhaseSpaceTest(field_bump=left, momentum_bump=right)
    second = PhaseSpaceTest(
        field_bump=right,
        momentum_bump=left,
        field_scale=0.7,
        momentum_scale=-0.4,
    )
    locality_first = PhaseSpaceTest(field_bump=left)
    locality_second = PhaseSpaceTest(momentum_bump=right)
    beta = de_sitter_inverse_temperature(radius)
    real_time = 0.31 * radius
    strip_fractions = (0.0, 0.37, 1.0)
    cutoffs = tuple(minimum_cutoff * 2**index for index in range(steps))

    records = []
    for cutoff in cutoffs:
        symplectic_value = continuum_phase_space_symplectic_form(
            first,
            second,
            momentum_cutoff=cutoff,
            integration_steps=1600,
        )
        covariance_value = continuum_phase_space_covariance(
            first,
            second,
            radius=radius,
            momentum_cutoff=cutoff,
            integration_steps=1600,
        )
        wightman_values = tuple(
            continuum_unequal_time_wightman(
                first,
                second,
                real_time + 1j * fraction * beta,
                radius=radius,
                momentum_cutoff=cutoff,
                integration_steps=1600,
            )
            for fraction in strip_fractions
        )
        locality_leakage = abs(
            continuum_phase_space_symplectic_form(
                locality_first,
                locality_second,
                momentum_cutoff=cutoff,
                integration_steps=1600,
            )
        )
        records.append(
            {
                "momentum_cutoff_K": cutoff,
                "truncated_symplectic_form": symplectic_value,
                "symplectic_uv_tail_bound": symplectic_uv_tail_bound(
                    first,
                    second,
                    momentum_cutoff=cutoff,
                    derivative_order=derivative_order,
                ),
                "truncated_covariance": covariance_value,
                "covariance_uv_tail_bound": covariance_uv_tail_bound(
                    first,
                    second,
                    radius=radius,
                    momentum_cutoff=cutoff,
                    derivative_order=derivative_order,
                ),
                "truncated_wightman_closed_strip_samples": tuple(
                    {
                        "imaginary_time_fraction_of_beta": fraction,
                        "real": value.real,
                        "imag": value.imag,
                    }
                    for fraction, value in zip(strip_fractions, wightman_values)
                ),
                "wightman_uv_tail_bound_uniform_on_closed_kms_strip": (
                    wightman_uv_tail_bound(
                        first,
                        second,
                        radius=radius,
                        momentum_cutoff=cutoff,
                        derivative_order=derivative_order,
                    )
                ),
                "equal_time_disjoint_support_symplectic_leakage": locality_leakage,
                "locality_uv_tail_bound": symplectic_uv_tail_bound(
                    locality_first,
                    locality_second,
                    momentum_cutoff=cutoff,
                    derivative_order=derivative_order,
                ),
                "weyl_characteristic_uv_tail_bound": (
                    weyl_characteristic_uv_tail_bound(
                        first,
                        radius=radius,
                        momentum_cutoff=cutoff,
                        derivative_order=derivative_order,
                    )
                ),
            }
        )

    def decreasing(key: str) -> bool:
        values = tuple(record[key] for record in records)
        return all(right < left for left, right in zip(values, values[1:]))

    successive_bounds_hold = True
    for left_record, right_record in zip(records, records[1:]):
        successive_bounds_hold = successive_bounds_hold and (
            abs(
                right_record["truncated_symplectic_form"]
                - left_record["truncated_symplectic_form"]
            )
            <= left_record["symplectic_uv_tail_bound"] * 1.01
        )
        successive_bounds_hold = successive_bounds_hold and (
            abs(
                right_record["truncated_covariance"]
                - left_record["truncated_covariance"]
            )
            <= left_record["covariance_uv_tail_bound"] * 1.01
        )
        wightman_difference = max(
            sqrt(
                (right_sample["real"] - left_sample["real"]) ** 2
                + (right_sample["imag"] - left_sample["imag"]) ** 2
            )
            for left_sample, right_sample in zip(
                left_record["truncated_wightman_closed_strip_samples"],
                right_record["truncated_wightman_closed_strip_samples"],
            )
        )
        successive_bounds_hold = successive_bounds_hold and (
            wightman_difference
            <= left_record[
                "wightman_uv_tail_bound_uniform_on_closed_kms_strip"
            ]
            * 1.01
        )

    certified_claims = {
        "explicit_symplectic_uv_tail_bound_vanishes": decreasing(
            "symplectic_uv_tail_bound"
        ),
        "explicit_covariance_uv_tail_bound_vanishes": decreasing(
            "covariance_uv_tail_bound"
        ),
        "uniform_closed_strip_wightman_uv_tail_bound_vanishes": decreasing(
            "wightman_uv_tail_bound_uniform_on_closed_kms_strip"
        ),
        "weyl_characteristic_functions_are_uv_cauchy": decreasing(
            "weyl_characteristic_uv_tail_bound"
        ),
        "observed_successive_cutoff_differences_obey_analytic_bounds": (
            successive_bounds_hold
        ),
        "equal_time_locality_leakage_is_bounded_and_vanishes": all(
            record["equal_time_disjoint_support_symplectic_leakage"]
            <= record["locality_uv_tail_bound"] * 1.01
            for record in records
        )
        and decreasing("locality_uv_tail_bound"),
    }
    return {
        "goal": "Static-Patch S-Wave Ultraviolet Removal",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "quantitative_s_wave_quasifree_uv_tail_theorem",
        "central_result": (
            "For compact Cauchy data whose n-th distributional derivative is a "
            "finite measure, integration by parts gives k^-n sine-transform decay. "
            "The s-wave symplectic, thermal covariance, Weyl characteristic, and "
            "unequal-time KMS tails therefore vanish explicitly as K tends to "
            "infinity; for the C2 cubic bumps n=4 and the worst thermal tail is "
            "O(K^-6)."
        ),
        "locality_result": (
            "The unbandlimited equal-time symplectic form is the local canonical "
            "form; nonzero bandlimited symplectic response between disjoint compact "
            "supports is bounded by the same vanishing UV tail."
        ),
        "smooth_test_extension": (
            "For C_c^infinity data the estimate holds at every derivative order, "
            "so the ultraviolet tails decrease faster than any inverse power."
        ),
        "infrared_result": (
            "The sine transform obeys |hhat(k)|<=sqrt(2/pi) k int x|h(x)|dx. "
            "Therefore the thermal covariance and KMS integrands have removable "
            "zero-frequency limits; the field-field covariance limit is "
            "2 m1(f)m1(u)/(pi beta)."
        ),
        "claim_boundary": (
            "free conformal s-wave on the half-line; the executable audit uses C2 "
            "piecewise-polynomial Cauchy data while the analytic theorem requires "
            "n>=2 for momentum covariance and covers compact data with finite "
            "n-th derivative measure, including C_c^infinity. The wall/UV result "
            "is an iterated limit, with selected diagonal refinements available; "
            "arbitrary joint cutoff paths are not claimed. No all-angular potential, "
            "direct Bunch-Davies identification, Hadamard/type-III classification, "
            "continuous core, gravity, or generalized entropy is claimed"
        ),
        "certified_claims": certified_claims,
        "records": tuple(records),
        "next_physics_gate": (
            "prove the all-angular finite-wall spectral limit and match the "
            "resulting full two-point distribution directly to Bunch-Davies"
        ),
    }
