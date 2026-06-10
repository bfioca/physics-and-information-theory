"""Leading rigid-Skyrmion quadrupole stress and its conservation obstruction.

The Skyrme work package uses signature ``(+---)``.  We first derive physical
orthonormal density and pressures with the positive-energy Hilbert convention,
then report the scalar-harmonic amplitudes in the ``(-+++)`` mixed-component
convention used by ``static_patch_l2_response``.

For a fixed hedgehog and a stationary mean-zero collective state, write
``Y=n_a Q_ab n_b``.  The leading ``l=2`` stress is proportional to ``Y/I^2``.
The radial-angular amplitude vanishes, but the remaining amplitudes fail the
static conservation equations generically.  Therefore the fixed-profile rotor
is not an admissible Zerilli source without centrifugal material deformation,
collective-projection corrections, or time dependence.
"""

from __future__ import annotations

from math import cos, isfinite, sin


def _positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def rigid_skyrmion_l2_stress_amplitudes(
    *,
    radius: float,
    metric_factor: float,
    profile: float,
    profile_derivative: float,
    pion_decay_constant: float,
    skyrme_coupling: float,
    moment_of_inertia: float,
) -> dict[str, float | str]:
    """Return coefficients multiplying ``Y=nQn`` in the leading stress."""
    for name, value in (
        ("radius", radius),
        ("metric_factor", metric_factor),
        ("pion_decay_constant", pion_decay_constant),
        ("skyrme_coupling", skyrme_coupling),
        ("moment_of_inertia", moment_of_inertia),
    ):
        _positive(name, value)
    _finite("profile", profile)
    _finite("profile_derivative", profile_derivative)

    sine = sin(profile)
    radial_strain_squared = metric_factor * profile_derivative**2
    tangential_strain_squared = sine**2 / radius**2
    sigma_coefficient = pion_decay_constant**2 * sine**2 / (8.0 * metric_factor)
    skyrme_coefficient = sine**2 / (2.0 * skyrme_coupling**2 * metric_factor)
    inertia_squared = moment_of_inertia**2

    energy_density = (
        -(
            sigma_coefficient
            + skyrme_coefficient * (radial_strain_squared + tangential_strain_squared)
        )
        / inertia_squared
    )
    radial_pressure = (
        -(
            sigma_coefficient
            + skyrme_coefficient * (tangential_strain_squared - radial_strain_squared)
        )
        / inertia_squared
    )
    tangential_pressure = (
        -(sigma_coefficient + skyrme_coefficient * radial_strain_squared)
        / inertia_squared
    )
    angular_tracefree = -(
        skyrme_coefficient * tangential_strain_squared / inertia_squared
    )
    return {
        "radius": radius,
        "radial_strain_squared_a2": radial_strain_squared,
        "tangential_strain_squared_b2": tangential_strain_squared,
        "sigma_coefficient_k2": sigma_coefficient,
        "skyrme_coefficient_k4": skyrme_coefficient,
        "energy_density_coefficient": energy_density,
        "radial_pressure_coefficient": radial_pressure,
        "tangential_pressure_coefficient": tangential_pressure,
        "radial_angular_shear_coefficient": 0.0,
        "angular_tracefree_stress_coefficient": angular_tracefree,
        "common_harmonic": "Y=n_a Q_ab n_b",
        "angular_tensor_harmonic": ("Y_AB=D_A D_B Y+3 gamma_AB Y for ell=2"),
        "state_scope": (
            "stationary symmetric second moment and vanishing mean angular "
            "momentum; coefficients multiply Y and already include I^-2"
        ),
    }


def rigid_skyrmion_l2_conservation_residuals(
    *,
    radius: float,
    metric_factor: float,
    profile: float,
    profile_derivative: float,
    profile_second_derivative: float,
    pion_decay_constant: float,
    skyrme_coupling: float,
    moment_of_inertia: float,
) -> dict[str, float | bool | str]:
    """Return exact coefficients of the radial and angular residuals."""
    amplitudes = rigid_skyrmion_l2_stress_amplitudes(
        radius=radius,
        metric_factor=metric_factor,
        profile=profile,
        profile_derivative=profile_derivative,
        pion_decay_constant=pion_decay_constant,
        skyrme_coupling=skyrme_coupling,
        moment_of_inertia=moment_of_inertia,
    )
    _finite("profile_second_derivative", profile_second_derivative)
    sine = sin(profile)
    if abs(sine) <= 1.0e-14:
        raise ValueError(
            "bulk residual formula requires sin(profile) nonzero; use the "
            "separate hard-wall asymptotic at a profile zero"
        )
    radial_strain_squared = float(amplitudes["radial_strain_squared_a2"])
    tangential_strain_squared = float(amplitudes["tangential_strain_squared_b2"])
    sigma_coefficient = float(amplitudes["sigma_coefficient_k2"])
    skyrme_coefficient = float(amplitudes["skyrme_coefficient_k4"])
    inertia_squared = moment_of_inertia**2
    cotangent = cos(profile) / sine

    angular_residual = (
        -(
            sigma_coefficient
            + skyrme_coefficient
            * (radial_strain_squared - 2.0 * tangential_strain_squared)
        )
        / inertia_squared
    )
    radial_bracket = (
        (
            skyrme_coupling**2 * pion_decay_constant**2 / 4.0
            + 2.0 * tangential_strain_squared
            - radial_strain_squared
        )
        * cotangent
        - metric_factor * profile_second_derivative
        - 2.0 * metric_factor * profile_derivative / radius
    )
    radial_residual = -(
        2.0 * skyrme_coefficient * profile_derivative * radial_bracket / inertia_squared
    )
    return {
        **amplitudes,
        "radial_conservation_residual_coefficient": radial_residual,
        "angular_conservation_residual_coefficient": angular_residual,
        "angular_residual_from_amplitudes": float(
            amplitudes["tangential_pressure_coefficient"]
        )
        - 2.0 * float(amplitudes["angular_tracefree_stress_coefficient"]),
        "fixed_profile_source_is_bulk_conserved": (
            abs(radial_residual) <= 1.0e-12 and abs(angular_residual) <= 1.0e-12
        ),
        "interpretation": (
            "The static hedgehog profile equation does not cancel these "
            "quadratic rotational residuals. Centrifugal deformation or a "
            "time-dependent source is required."
        ),
    }


def hard_wall_angular_residual_asymptotic(
    *,
    wall_metric_factor: float,
    wall_profile_slope: float,
    pion_decay_constant: float,
    skyrme_coupling: float,
    moment_of_inertia: float,
) -> dict[str, float | bool | str]:
    """Return the coefficient of ``(r_w-r)^2`` near a Dirichlet wall.

    For ``F(r_w)=0`` and nonzero slope, the trace-free angular term starts at
    fourth order in the wall distance, while the tangential-pressure term is
    negative at second order.  Static angular conservation therefore fails on
    every sufficiently small interior collar.
    """
    for name, value in (
        ("wall_metric_factor", wall_metric_factor),
        ("pion_decay_constant", pion_decay_constant),
        ("skyrme_coupling", skyrme_coupling),
        ("moment_of_inertia", moment_of_inertia),
    ):
        _positive(name, value)
    _finite("wall_profile_slope", wall_profile_slope)
    slope_squared = wall_profile_slope**2
    leading_coefficient = (
        -(
            pion_decay_constant**2 * slope_squared / (8.0 * wall_metric_factor)
            + slope_squared**2 / (2.0 * skyrme_coupling**2)
        )
        / moment_of_inertia**2
    )
    return {
        "wall_profile_slope": wall_profile_slope,
        "angular_residual_quadratic_coefficient": leading_coefficient,
        "strictly_negative_for_nonzero_slope": (
            wall_profile_slope != 0.0 and leading_coefficient < 0.0
        ),
        "asymptotic": (
            "C_ang(r)=coefficient*(r_w-r)^2+O((r_w-r)^3); "
            "the angular trace-free contribution begins at fourth order"
        ),
        "consequence": (
            "The fixed-profile rigid quadrupole is not a conserved static "
            "bulk source in any collar of a nontrivial hard wall."
        ),
    }


def rigid_skyrmion_stress_conservation_certificate() -> dict[str, object]:
    """Audit the exact amplitudes and a strict hard-wall obstruction."""
    sample = rigid_skyrmion_l2_conservation_residuals(
        radius=1.0,
        metric_factor=1.0,
        profile=1.5707963267948966,
        profile_derivative=0.0,
        profile_second_derivative=0.0,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=1.0,
    )
    wall = hard_wall_angular_residual_asymptotic(
        wall_metric_factor=0.96,
        wall_profile_slope=-1.25,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=2.0,
    )
    claims = {
        "sample_energy_coefficient_matches_rigid_inertia_density": abs(
            sample["energy_density_coefficient"] + 0.625
        )
        < 1.0e-15,
        "angular_residual_matches_conservation_checker": abs(
            sample["angular_conservation_residual_coefficient"]
            - sample["angular_residual_from_amplitudes"]
        )
        < 1.0e-15,
        "sample_fixed_profile_source_is_not_conserved": not sample[
            "fixed_profile_source_is_bulk_conserved"
        ],
        "hard_wall_obstruction_is_strict": wall["strictly_negative_for_nonzero_slope"],
    }
    return {
        "goal": "Conserved Rotating Skyrmion Quadrupole Source",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "fixed_profile_rigid_source_conservation_no_go",
        "sample_bulk_record": sample,
        "hard_wall_asymptotic": wall,
        "certified_claims": claims,
        "required_replacement": (
            "Solve the O(Omega^2) material and wall deformation, or retain the "
            "time-dependent stress and use a dynamical gravitational response."
        ),
        "claim_boundary": (
            "Leading fixed-profile collective ansatz, stationary symmetric "
            "second moments, zero mean angular momentum, and the classical "
            "two-plus-four-derivative Skyrme stress. This does not exclude a "
            "conserved deformed rotating Skyrmion or a dynamical source."
        ),
    }
