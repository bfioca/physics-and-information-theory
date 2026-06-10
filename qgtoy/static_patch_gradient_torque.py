"""Three-axis gradient-bath covariance for a static-patch rotation reference.

The optical zero-frequency scalar kernel is ``phi_0(y)=y/sinh(y)``.  Coupling
vector charges to local orthonormal gradient components produces a Kossakowski
cross matrix given by the parallel-transported mixed Hessian of this kernel.
In a geodesic frame it has one longitudinal and two transverse eigenvalues,

    c_parallel(y) = -3 phi_0''(y),
    c_perp(y)     = -3 phi_0'(y)/sinh(y).

The coincident auto-covariance is isotropic.  A conditional angular-momentum /
optical-gradient coupling therefore gives a three-component diffusion
surrogate, but at separated centers it is not the common mode required by the
collective ``L_a+J_a`` heat channel.  This is not by itself a mechanical torque
model for a spherical top.
"""

from __future__ import annotations

from math import exp, isfinite, log, pi, sinh, sqrt

from .common_mode_locality_mismatch import (
    axial_common_mode_mismatch_lower_bound,
    maximum_correlation_defect_for_mismatch,
)
from .static_patch_scalar_common_mode import (
    maximum_same_shell_angular_separation,
)


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_dimension(dimension: int) -> None:
    if (
        isinstance(dimension, bool)
        or not isinstance(dimension, int)
        or dimension < 3
    ):
        raise ValueError("dimension must be an integer at least three")


def _validate_correlation(name: str, value: float) -> None:
    if not isfinite(value) or value < -1.0 or value > 1.0:
        raise ValueError(f"{name} must lie in the interval [-1,1]")


def _csch_coth(value: float) -> tuple[float, float]:
    if value < 20.0:
        hyperbolic_sine = sinh(value)
        csch = 1.0 / hyperbolic_sine
        t = exp(-2.0 * value)
        coth = (1.0 + t) / (1.0 - t)
        return csch, coth
    t = exp(-2.0 * value)
    csch = 2.0 * exp(-value) / (1.0 - t)
    coth = (1.0 + t) / (1.0 - t)
    return csch, coth


def zero_mode_kernel_derivatives(
    distance_over_radius: float,
) -> tuple[float, float]:
    """Return first and second derivatives of ``y/sinh(y)``."""
    y = distance_over_radius
    _validate_nonnegative("distance_over_radius", y)
    if y < 5.0e-2:
        y2 = y * y
        first = (
            -y / 3.0
            + 7.0 * y * y2 / 90.0
            - 31.0 * y * y2 * y2 / 2520.0
            + 127.0 * y * y2 * y2 * y2 / 75600.0
        )
        second = (
            -1.0 / 3.0
            + 7.0 * y2 / 30.0
            - 31.0 * y2 * y2 / 504.0
            + 127.0 * y2 * y2 * y2 / 10800.0
        )
        return first, second
    csch, coth = _csch_coth(y)
    first = csch * (1.0 - y * coth)
    second = csch * (y * (1.0 + 2.0 * csch * csch) - 2.0 * coth)
    return first, second


def gradient_zero_frequency_correlations(
    distance_over_radius: float,
) -> tuple[float, float]:
    """Return longitudinal and transverse normalized gradient correlations."""
    y = distance_over_radius
    _validate_nonnegative("distance_over_radius", y)
    if y == 0.0:
        return 1.0, 1.0
    if y < 5.0e-2:
        y2 = y * y
        longitudinal = (
            1.0
            - 7.0 * y2 / 10.0
            + 31.0 * y2 * y2 / 168.0
            - 127.0 * y2 * y2 * y2 / 3600.0
        )
        transverse = 1.0 - 2.0 * y2 / 5.0 + 2.0 * y2 * y2 / 21.0
        return longitudinal, transverse
    first, second = zero_mode_kernel_derivatives(y)
    csch, _ = _csch_coth(y)
    return -3.0 * second, -3.0 * first * csch


def maximum_gradient_distance_for_defect(
    maximum_defect: float,
    *,
    component: str = "longitudinal",
) -> float:
    """Invert the first small-distance crossing of a gradient correlation defect."""
    _validate_nonnegative("maximum_defect", maximum_defect)
    if maximum_defect >= 1.0:
        raise ValueError("maximum_defect must be smaller than one")
    if component not in {"longitudinal", "transverse"}:
        raise ValueError("component must be longitudinal or transverse")
    if maximum_defect == 0.0:
        return 0.0

    index = 0 if component == "longitudinal" else 1

    def defect(distance: float) -> float:
        return 1.0 - gradient_zero_frequency_correlations(distance)[index]

    low = 0.0
    high = 0.25
    while defect(high) <= maximum_defect:
        high *= 2.0
        if high > 64.0:
            raise RuntimeError("gradient defect inversion failed to bracket a crossing")
    for _ in range(96):
        middle = 0.5 * (low + high)
        if defect(middle) <= maximum_defect:
            low = middle
        else:
            high = middle
    return low


def spin_half_singlet_survival_probability(
    dimensionless_time: float,
    *,
    longitudinal_correlation: float,
    transverse_correlation: float,
) -> float:
    """Return exact singlet survival for the anisotropic two-qubit channel.

    The generator convention is

    ``-sum_a([L_a,[L_a,.]]+[J_a,[J_a,.]]+2c_a[L_a,[J_a,.]])``

    with ``L_a=J_a=sigma_a/2`` and correlations
    ``(c_parallel,c_perp,c_perp)``.
    """
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    _validate_correlation(
        "longitudinal_correlation",
        longitudinal_correlation,
    )
    _validate_correlation("transverse_correlation", transverse_correlation)
    if dimensionless_time == 0.0:
        return 1.0
    if longitudinal_correlation == 1.0 and transverse_correlation == 1.0:
        return 1.0

    longitudinal = longitudinal_correlation
    transverse = transverse_correlation
    mean_eigenvalue = -4.0 + longitudinal
    splitting = sqrt(longitudinal**2 + 8.0 * transverse**2)
    exponent_plus = dimensionless_time * (mean_eigenvalue + splitting)
    exponent_minus = dimensionless_time * (mean_eigenvalue - splitting)
    exponential_plus = exp(exponent_plus)
    exponential_minus = exp(exponent_minus)
    hyperbolic_factor = 0.5 * (exponential_plus + exponential_minus)
    if splitting == 0.0:
        split_factor = dimensionless_time * exp(
            dimensionless_time * mean_eigenvalue
        )
    else:
        split_factor = 0.5 * (
            exponential_plus - exponential_minus
        ) / splitting
    longitudinal_bell_coefficient = (
        -hyperbolic_factor
        + split_factor * (longitudinal - 4.0 * transverse)
    )
    transverse_bell_coefficient = (
        -hyperbolic_factor
        + split_factor * (-2.0 * transverse - longitudinal)
    )
    survival = (
        1.0
        - longitudinal_bell_coefficient
        - 2.0 * transverse_bell_coefficient
    ) / 4.0
    return min(1.0, max(0.0, survival))


def spin_half_three_axis_mismatch_lower_bound(
    dimensionless_time: float,
    *,
    center_distance_over_radius: float,
) -> float:
    """Return the exact singlet-output trace-distance channel witness."""
    longitudinal, transverse = gradient_zero_frequency_correlations(
        center_distance_over_radius
    )
    survival = spin_half_singlet_survival_probability(
        dimensionless_time,
        longitudinal_correlation=longitudinal,
        transverse_correlation=transverse,
    )
    return 1.0 - survival


def maximum_gradient_distance_for_spin_half_mismatch(
    target_mismatch: float,
    *,
    dimensionless_time: float,
) -> float | None:
    """Invert the exact spin-half witness on its near-coincidence branch."""
    _validate_nonnegative("target_mismatch", target_mismatch)
    if target_mismatch >= 1.0:
        raise ValueError("target_mismatch must be smaller than one")
    _validate_positive("dimensionless_time", dimensionless_time)
    if target_mismatch == 0.0:
        return 0.0

    def mismatch(distance: float) -> float:
        return spin_half_three_axis_mismatch_lower_bound(
            dimensionless_time,
            center_distance_over_radius=distance,
        )

    low = 0.0
    high = 1.0
    if mismatch(high) < target_mismatch:
        return None
    for _ in range(96):
        middle = 0.5 * (low + high)
        if mismatch(middle) <= target_mismatch:
            low = middle
        else:
            high = middle
    return low


def static_patch_gradient_torque_record(
    dimension: int,
    *,
    center_distance_over_radius: float,
    charge_gap: float = 1.0,
    mismatch_coefficient: float = 1.0,
    stretched_distance: float = 0.05,
    radius: float = 1.0,
) -> dict[str, object]:
    """Audit a local three-axis scalar-gradient bath against common diffusion."""
    _validate_dimension(dimension)
    _validate_nonnegative(
        "center_distance_over_radius",
        center_distance_over_radius,
    )
    _validate_positive("charge_gap", charge_gap)
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    _validate_positive("stretched_distance", stretched_distance)
    _validate_positive("radius", radius)
    if stretched_distance > 0.5 * pi * radius:
        raise ValueError("stretched_distance must be at most pi R/2")
    target_mismatch = mismatch_coefficient / float(dimension)
    if target_mismatch >= 0.5:
        raise ValueError("mismatch_coefficient/dimension must be smaller than one half")

    dimensionless_time = 0.5 * log(float(dimension))
    longitudinal, transverse = gradient_zero_frequency_correlations(
        center_distance_over_radius
    )
    longitudinal_axiswise_mismatch = axial_common_mode_mismatch_lower_bound(
        dimensionless_time,
        correlation=longitudinal,
        charge_gap=charge_gap,
    )
    transverse_axiswise_mismatch = axial_common_mode_mismatch_lower_bound(
        dimensionless_time,
        correlation=transverse,
        charge_gap=charge_gap,
    )
    spin_half_mismatch = spin_half_three_axis_mismatch_lower_bound(
        dimensionless_time,
        center_distance_over_radius=center_distance_over_radius,
    )
    maximum_defect = maximum_correlation_defect_for_mismatch(
        target_mismatch,
        dimensionless_time=dimensionless_time,
        charge_gap=charge_gap,
    )
    if maximum_defect < 1.0 - 1.0e-12:
        maximum_longitudinal_distance = maximum_gradient_distance_for_defect(
            maximum_defect,
            component="longitudinal",
        )
        maximum_transverse_distance = maximum_gradient_distance_for_defect(
            maximum_defect,
            component="transverse",
        )
        maximum_angular_separation = maximum_same_shell_angular_separation(
            stretched_distance,
            maximum_longitudinal_distance,
            radius=radius,
        )
    else:
        maximum_longitudinal_distance = None
        maximum_transverse_distance = None
        maximum_angular_separation = None
    maximum_spin_half_distance = maximum_gradient_distance_for_spin_half_mismatch(
        target_mismatch,
        dimensionless_time=dimensionless_time,
    )
    if maximum_spin_half_distance is None:
        maximum_spin_half_angle = None
    else:
        maximum_spin_half_angle = maximum_same_shell_angular_separation(
            stretched_distance,
            maximum_spin_half_distance,
            radius=radius,
        )
    return {
        "dimension_d": dimension,
        "dimensionless_protocol_time_s": dimensionless_time,
        "center_distance_over_radius_y": center_distance_over_radius,
        "axial_charge_gap_Delta": charge_gap,
        "gradient_cross_matrix_eigenvalues": {
            "longitudinal": longitudinal,
            "transverse_multiplicity_two": transverse,
        },
        "collective_relative_rate_weights": {
            "longitudinal": {
                "collective_1_plus_c": 1.0 + longitudinal,
                "relative_1_minus_c": 1.0 - longitudinal,
            },
            "transverse": {
                "collective_1_plus_c": 1.0 + transverse,
                "relative_1_minus_c": 1.0 - transverse,
            },
        },
        "longitudinal_axiswise_axial_surrogate_mismatch": (
            longitudinal_axiswise_mismatch
        ),
        "transverse_axiswise_axial_surrogate_mismatch": (
            transverse_axiswise_mismatch
        ),
        "spin_half_singlet_three_axis_mismatch_lower_bound": spin_half_mismatch,
        "allocated_mismatch_A_over_d": target_mismatch,
        "passes_imported_axiswise_axial_allocation": (
            max(
                longitudinal_axiswise_mismatch,
                transverse_axiswise_mismatch,
            )
            <= target_mismatch
        ),
        "passes_exact_spin_half_three_axis_allocation": (
            spin_half_mismatch <= target_mismatch
        ),
        "maximum_allowed_correlation_defect": maximum_defect,
        "maximum_longitudinal_center_distance_over_radius": (
            maximum_longitudinal_distance
        ),
        "maximum_transverse_center_distance_over_radius": (
            maximum_transverse_distance
        ),
        "maximum_same_shell_angle_from_longitudinal_component": (
            maximum_angular_separation
        ),
        "maximum_spin_half_center_distance_over_radius": maximum_spin_half_distance,
        "maximum_same_shell_angle_from_spin_half_witness": maximum_spin_half_angle,
        "interaction": (
            "H_I=lambda sum_a[L_a B_a(p)+J_a B_a(q)], "
            "B_a=e_a^i nabla_i Phi_opt"
        ),
        "interaction_interpretation": (
            "conditional proper-SO(3)-covariant gyroscopic coupling; parity odd "
            "for an ordinary scalar and not a derived mechanical top torque"
        ),
        "auto_kossakowski_matrix": "proportional to delta_ab/(3 R^2)",
        "cross_kossakowski_matrix": (
            "diag(c_parallel,c_perp,c_perp) after parallel transport in the "
            "center-separation geodesic frame"
        ),
        "scope": (
            "localized vector charges, optical scalar-gradient zero mode, equal "
            "center redshift and coupling normalization, weak-coupling secular "
            "three-axis diffusion; the finite-time mismatch numbers import the "
            "one-axis witness, while the singlet witness is an exact full "
            "noncommuting three-axis spin-half channel lower bound"
        ),
    }


def static_patch_gradient_torque_certificate(
    *,
    center_distance_over_radius: float = 0.2,
    maximum_dimension: int = 4096,
    charge_gap: float = 1.0,
    mismatch_coefficient: float = 1.0,
    stretched_distance: float = 0.05,
    radius: float = 1.0,
) -> dict[str, object]:
    """Audit the three-axis gradient-bath common-mode obstruction."""
    _validate_dimension(maximum_dimension)
    if maximum_dimension < 32:
        raise ValueError("maximum_dimension must be at least thirty-two")
    dimensions = tuple(
        sorted(
            {
                dimension
                for dimension in (8, 32, 128, 512, maximum_dimension)
                if dimension <= maximum_dimension
            }
            | {maximum_dimension}
        )
    )
    records = tuple(
        static_patch_gradient_torque_record(
            dimension,
            center_distance_over_radius=center_distance_over_radius,
            charge_gap=charge_gap,
            mismatch_coefficient=mismatch_coefficient,
            stretched_distance=stretched_distance,
            radius=radius,
        )
        for dimension in dimensions
    )
    distances = (0.0, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 4.0)
    correlations = tuple(
        gradient_zero_frequency_correlations(distance)
        for distance in distances
    )
    required_longitudinal_distances = tuple(
        record["maximum_longitudinal_center_distance_over_radius"]
        for record in records
        if record["maximum_longitudinal_center_distance_over_radius"] is not None
    )
    required_angles = tuple(
        record["maximum_same_shell_angle_from_longitudinal_component"]
        for record in records
        if record["maximum_same_shell_angle_from_longitudinal_component"] is not None
    )
    required_spin_half_distances = tuple(
        record["maximum_spin_half_center_distance_over_radius"]
        for record in records
        if record["maximum_spin_half_center_distance_over_radius"] is not None
    )
    required_spin_half_angles = tuple(
        record["maximum_same_shell_angle_from_spin_half_witness"]
        for record in records
        if record["maximum_same_shell_angle_from_spin_half_witness"] is not None
    )
    small_distance = 1.0e-3
    small_longitudinal, small_transverse = gradient_zero_frequency_correlations(
        small_distance
    )
    small_time = 0.75
    small_spin_half_mismatch = spin_half_three_axis_mismatch_lower_bound(
        small_time,
        center_distance_over_radius=small_distance,
    )
    certified_claims = {
        "coincident_gradient_auto_covariance_is_isotropic": correlations[0]
        == (1.0, 1.0),
        "two_site_kossakowski_blocks_are_positive_semidefinite": all(
            abs(longitudinal) <= 1.0 + 1.0e-12
            and abs(transverse) <= 1.0 + 1.0e-12
            for longitudinal, transverse in correlations
        ),
        "longitudinal_component_is_the_stricter_nearby_common_mode": all(
            longitudinal <= transverse
            for longitudinal, transverse in correlations[1:6]
        ),
        "small_distance_longitudinal_coefficient_is_seven_tenths": abs(
            (1.0 - small_longitudinal) / small_distance**2 - 0.7
        )
        < 1.0e-6,
        "small_distance_transverse_coefficient_is_two_fifths": abs(
            (1.0 - small_transverse) / small_distance**2 - 0.4
        )
        < 1.0e-6,
        "spin_half_singlet_is_exactly_decoherence_free_at_coincidence": (
            spin_half_three_axis_mismatch_lower_bound(
                1.0,
                center_distance_over_radius=0.0,
            )
            == 0.0
        ),
        "spin_half_small_distance_coefficient_is_three_halves_s": abs(
            small_spin_half_mismatch / (small_time * small_distance**2) - 1.5
        )
        < 1.0e-5,
        "A_over_d_budget_forces_three_axis_colocation": (
            len(required_longitudinal_distances) >= 2
            and all(
                right < left
                for left, right in zip(
                    required_longitudinal_distances,
                    required_longitudinal_distances[1:],
                )
            )
        ),
        "near_horizon_three_axis_angular_window_shrinks": (
            len(required_angles) >= 2
            and all(
                right < left
                for left, right in zip(required_angles, required_angles[1:])
            )
        ),
        "exact_spin_half_distance_budget_shrinks": (
            len(required_spin_half_distances) >= 2
            and all(
                right < left
                for left, right in zip(
                    required_spin_half_distances,
                    required_spin_half_distances[1:],
                )
            )
        ),
        "exact_spin_half_angular_window_shrinks": (
            len(required_spin_half_angles) >= 2
            and all(
                right < left
                for left, right in zip(
                    required_spin_half_angles,
                    required_spin_half_angles[1:],
                )
            )
        ),
        "fixed_separation_fails_imported_axiswise_allocation": (
            not records[-1]["passes_imported_axiswise_axial_allocation"]
        ),
        "fixed_separation_fails_exact_spin_half_allocation": (
            not records[-1]["passes_exact_spin_half_three_axis_allocation"]
        ),
    }
    return {
        "goal": "Static-Patch Gradient-Coupling Common-Mode Test",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "three_axis_bunch_davies_gradient_covariance_obstruction",
        "central_result": (
            "A conditional vector coupling to the optical scalar gradient has "
            "an isotropic auto Kossakowski matrix but a separated cross matrix "
            "diag(c_parallel,c_perp,c_perp), with c_parallel=-3 phi0'' and "
            "c_perp=-3 phi0'/sinh. Axis by axis it contains relative L_a-J_a "
            "noise and is not collective L_a+J_a diffusion at nonzero center "
            "separation. For two spin-half charges, singlet leakage gives an "
            "exact finite-time full three-axis channel witness."
        ),
        "scaling_consequence": (
            "The exact spin-half witness is (3/2)s y^2+O(y^4) near coincidence. "
            "With s=(1/2)log d and an A/d allocation it requires "
            "y=O(1/sqrt(d log d)). The earlier charge-gap-dependent axiswise "
            "criterion remains available for general axial sectors."
        ),
        "claim_boundary": (
            "this derives a three-component local gradient-bath covariance for "
            "localized vector charges. It is not a mechanical torque theorem, "
            "and the exact finite-time witness is limited to two spin-half "
            "charges. It does not identify the global hard "
            "angular target with L_a at one worldtube, derive the physical "
            "conformal vector source and support stresses, control finite memory, "
            "or include gravitational backreaction."
        ),
        "certified_claims": certified_claims,
        "sample_correlations": tuple(
            {
                "distance_over_radius": distance,
                "longitudinal": correlation[0],
                "transverse": correlation[1],
            }
            for distance, correlation in zip(distances, correlations)
        ),
        "records": records,
        "next_physics_gate": (
            "derive the target angular-momentum density and finite-top vector "
            "source from one local action, extend the witness beyond spin half, "
            "then close the stress-energy/lifetime error budget"
        ),
    }
