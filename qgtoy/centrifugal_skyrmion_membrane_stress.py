"""Distributional membrane completion of the centrifugal quadrupole.

The interior stress is supported on ``r<R(n)`` with
``R=a+xi q(n)``.  Expanding the moving support creates a singular layer from
the spherical background stress.  A Nambu--Goto membrane contributes its own
``delta`` and ``delta-prime`` amplitudes.  This module combines those terms and
reduces distributional conservation to the background Young--Laplace equation
and the linearized normal/tangential wall-force conditions.

The calculation is fixed-background and uses the ``(-+++)`` mixed-stress
convention of ``static_even_stress_conservation``.
"""

from __future__ import annotations

from math import cos, isfinite, sin, sqrt

from .centrifugal_skyrmion_bvp import solve_centrifugal_quadrupole_bvp
from .centrifugal_skyrmion_completed_stress import (
    centrifugal_quadrupole_stress_amplitudes,
)
from .centrifugal_skyrmion_deformation import (
    hard_wall_background_pressure_derivative,
)
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile


def _finite(name: str, value: float) -> float:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(name: str, value: float) -> float:
    value = _finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def pure_tension_shell_singular_amplitudes(
    *,
    wall_radius: float,
    wall_metric_factor: float,
    wall_metric_factor_derivative: float,
    membrane_tension: float,
    wall_displacement_coefficient: float,
) -> dict[str, float | str]:
    """Return the moving Nambu--Goto shell's ``delta`` coefficients.

    The returned ``*_delta_prime`` values multiply ``delta'(r-a)``.  The
    perturbation of ``T^t_t`` is ``-rho q`` and that of ``T^r_A`` is
    ``j D_A q``.
    """
    wall_radius = _positive("wall_radius", wall_radius)
    lapse = _positive("wall_metric_factor", wall_metric_factor)
    lapse_derivative = _finite(
        "wall_metric_factor_derivative", wall_metric_factor_derivative
    )
    tension = _positive("membrane_tension", membrane_tension)
    displacement = _finite(
        "wall_displacement_coefficient", wall_displacement_coefficient
    )
    root_lapse = sqrt(lapse)
    lapse_shape = lapse_derivative / (2.0 * root_lapse)
    energy_delta = tension * displacement * lapse_shape
    energy_delta_prime = -tension * displacement * root_lapse
    shear_delta = -tension * displacement * root_lapse
    return {
        "wall_radius": wall_radius,
        "energy_density_delta": energy_delta,
        "energy_density_delta_prime": energy_delta_prime,
        "radial_pressure_delta": 0.0,
        "radial_pressure_delta_prime": 0.0,
        "tangential_pressure_delta": -energy_delta,
        "tangential_pressure_delta_prime": -energy_delta_prime,
        "radial_angular_shear_delta": shear_delta,
        "radial_angular_shear_delta_prime": 0.0,
        "angular_tracefree_stress_delta": 0.0,
        "angular_tracefree_stress_delta_prime": 0.0,
        "convention": (
            "coefficients multiply delta(r-a) or delta'(r-a); "
            "delta T^t_t=-rho q and delta T^r_A=j D_Aq"
        ),
    }


def moving_interface_singular_amplitudes(
    *,
    wall_radius: float,
    wall_metric_factor: float,
    wall_metric_factor_derivative: float,
    membrane_tension: float,
    wall_displacement_coefficient: float,
    background_energy_density: float,
    background_radial_pressure: float,
    background_tangential_pressure: float,
) -> dict[str, float | str]:
    """Add the displaced-background layer to the shell amplitudes."""
    displacement = _finite(
        "wall_displacement_coefficient", wall_displacement_coefficient
    )
    background_energy = _finite("background_energy_density", background_energy_density)
    background_radial = _finite(
        "background_radial_pressure", background_radial_pressure
    )
    background_tangential = _finite(
        "background_tangential_pressure", background_tangential_pressure
    )
    shell = pure_tension_shell_singular_amplitudes(
        wall_radius=wall_radius,
        wall_metric_factor=wall_metric_factor,
        wall_metric_factor_derivative=wall_metric_factor_derivative,
        membrane_tension=membrane_tension,
        wall_displacement_coefficient=displacement,
    )
    return {
        "energy_density_delta": (
            displacement * background_energy + shell["energy_density_delta"]
        ),
        "energy_density_delta_prime": shell["energy_density_delta_prime"],
        "radial_pressure_delta": displacement * background_radial,
        "radial_pressure_delta_prime": 0.0,
        "tangential_pressure_delta": (
            displacement * background_tangential + shell["tangential_pressure_delta"]
        ),
        "tangential_pressure_delta_prime": shell["tangential_pressure_delta_prime"],
        "radial_angular_shear_delta": shell["radial_angular_shear_delta"],
        "radial_angular_shear_delta_prime": 0.0,
        "angular_tracefree_stress_delta": 0.0,
        "angular_tracefree_stress_delta_prime": 0.0,
        "scope": (
            "Eulerian first variation of T0*Theta(a+xi*q-r) plus a moving "
            "constant-tension Nambu--Goto shell"
        ),
    }


def pure_tension_shell_divergence_coefficients(
    *,
    ell: int,
    wall_radius: float,
    wall_metric_factor: float,
    wall_metric_factor_derivative: float,
    wall_metric_factor_second_derivative: float,
    membrane_tension: float,
    wall_displacement_coefficient: float,
) -> dict[str, float | int | str]:
    """Reduce the shell divergence to its curvature-force coefficients."""
    if isinstance(ell, bool) or not isinstance(ell, int) or ell < 2:
        raise ValueError("ell must be an integer at least two")
    radius = _positive("wall_radius", wall_radius)
    lapse = _positive("wall_metric_factor", wall_metric_factor)
    lapse_derivative = _finite(
        "wall_metric_factor_derivative", wall_metric_factor_derivative
    )
    lapse_second_derivative = _finite(
        "wall_metric_factor_second_derivative",
        wall_metric_factor_second_derivative,
    )
    tension = _positive("membrane_tension", membrane_tension)
    displacement = _finite(
        "wall_displacement_coefficient", wall_displacement_coefficient
    )
    angular_eigenvalue = ell * (ell + 1)
    shell = pure_tension_shell_singular_amplitudes(
        wall_radius=radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_derivative,
        membrane_tension=tension,
        wall_displacement_coefficient=displacement,
    )
    connection = lapse_derivative / (2.0 * lapse)
    connection_derivative = lapse_second_derivative / (
        2.0 * lapse
    ) - lapse_derivative**2 / (2.0 * lapse**2)
    rho_delta = float(shell["energy_density_delta"])
    rho_delta_prime = float(shell["energy_density_delta_prime"])
    tangential_delta = float(shell["tangential_pressure_delta"])
    tangential_delta_prime = float(shell["tangential_pressure_delta_prime"])
    shear_delta = float(shell["radial_angular_shear_delta"])
    raw_radial_delta_prime = (
        connection * rho_delta_prime - 2.0 * tangential_delta_prime / radius
    )
    raw_radial_delta = (
        connection * rho_delta
        - connection_derivative * rho_delta_prime
        - 2.0 * tangential_delta / radius
        - 2.0 * tangential_delta_prime / radius**2
        - angular_eigenvalue * shear_delta / (lapse * radius**2)
    )
    raw_angular_delta_prime = shear_delta + tangential_delta_prime
    raw_angular_delta = 2.0 * shear_delta / radius + tangential_delta

    root_lapse = sqrt(lapse)
    mean_curvature = 2.0 * root_lapse / radius + lapse_derivative / (2.0 * root_lapse)
    mean_curvature_derivative = (
        lapse_derivative / (root_lapse * radius)
        - 2.0 * root_lapse / radius**2
        + lapse_second_derivative / (2.0 * root_lapse)
        - lapse_derivative**2 / (4.0 * lapse**1.5)
    )
    shape_curvature = mean_curvature_derivative + angular_eigenvalue / (
        radius**2 * root_lapse
    )
    expected_radial_delta_prime = -tension * displacement * mean_curvature
    expected_radial_delta = tension * displacement * shape_curvature
    expected_angular_delta_prime = 0.0
    expected_angular_delta = -tension * displacement * mean_curvature
    factorization_error = max(
        abs(raw_radial_delta_prime - expected_radial_delta_prime),
        abs(raw_radial_delta - expected_radial_delta),
        abs(raw_angular_delta_prime - expected_angular_delta_prime),
        abs(raw_angular_delta - expected_angular_delta),
    )
    return {
        "ell": ell,
        "mean_curvature": mean_curvature,
        "shape_curvature_coefficient": shape_curvature,
        "radial_delta_prime_coefficient": raw_radial_delta_prime,
        "radial_delta_coefficient": raw_radial_delta,
        "angular_delta_prime_coefficient": raw_angular_delta_prime,
        "angular_delta_coefficient": raw_angular_delta,
        "expected_radial_delta_prime_coefficient": expected_radial_delta_prime,
        "expected_radial_delta_coefficient": expected_radial_delta,
        "expected_angular_delta_prime_coefficient": expected_angular_delta_prime,
        "expected_angular_delta_coefficient": expected_angular_delta,
        "curvature_factorization_maximum_error": factorization_error,
        "identity": ("nabla_mu T^mu_nu(shell)=sigma K_shell n_nu delta_shell"),
    }


def distributional_wall_conservation_coefficients(
    *,
    ell: int,
    wall_radius: float,
    wall_metric_factor: float,
    wall_metric_factor_derivative: float,
    wall_metric_factor_second_derivative: float,
    membrane_tension: float,
    wall_displacement_coefficient: float,
    background_energy_density: float,
    background_radial_pressure: float,
    background_radial_pressure_derivative: float,
    background_tangential_pressure: float,
    intrinsic_radial_pressure_multipole: float,
    intrinsic_radial_angular_shear_multipole: float,
) -> dict[str, float | int | bool | str]:
    """Return all ``delta`` and ``delta-prime`` conservation coefficients."""
    if isinstance(ell, bool) or not isinstance(ell, int) or ell < 2:
        raise ValueError("ell must be an integer at least two")
    radius = _positive("wall_radius", wall_radius)
    lapse = _positive("wall_metric_factor", wall_metric_factor)
    lapse_derivative = _finite(
        "wall_metric_factor_derivative", wall_metric_factor_derivative
    )
    lapse_second_derivative = _finite(
        "wall_metric_factor_second_derivative",
        wall_metric_factor_second_derivative,
    )
    tension = _positive("membrane_tension", membrane_tension)
    displacement = _finite(
        "wall_displacement_coefficient", wall_displacement_coefficient
    )
    background_energy = _finite("background_energy_density", background_energy_density)
    background_radial = _finite(
        "background_radial_pressure", background_radial_pressure
    )
    background_radial_derivative = _finite(
        "background_radial_pressure_derivative",
        background_radial_pressure_derivative,
    )
    background_tangential = _finite(
        "background_tangential_pressure", background_tangential_pressure
    )
    intrinsic_radial = _finite(
        "intrinsic_radial_pressure_multipole",
        intrinsic_radial_pressure_multipole,
    )
    intrinsic_shear = _finite(
        "intrinsic_radial_angular_shear_multipole",
        intrinsic_radial_angular_shear_multipole,
    )
    angular_eigenvalue = ell * (ell + 1)
    singular = moving_interface_singular_amplitudes(
        wall_radius=radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_derivative,
        membrane_tension=tension,
        wall_displacement_coefficient=displacement,
        background_energy_density=background_energy,
        background_radial_pressure=background_radial,
        background_tangential_pressure=background_tangential,
    )
    connection = lapse_derivative / (2.0 * lapse)
    connection_derivative = lapse_second_derivative / (
        2.0 * lapse
    ) - lapse_derivative**2 / (2.0 * lapse**2)
    rho_delta = float(singular["energy_density_delta"])
    rho_delta_prime = float(singular["energy_density_delta_prime"])
    radial_delta = float(singular["radial_pressure_delta"])
    tangential_delta = float(singular["tangential_pressure_delta"])
    tangential_delta_prime = float(singular["tangential_pressure_delta_prime"])
    shear_delta = float(singular["radial_angular_shear_delta"])

    raw_radial_delta_prime = (
        radial_delta
        + connection * rho_delta_prime
        - 2.0 * tangential_delta_prime / radius
    )
    raw_radial_delta = (
        -intrinsic_radial
        + connection * (rho_delta + radial_delta)
        - connection_derivative * rho_delta_prime
        + 2.0 * (radial_delta - tangential_delta) / radius
        - 2.0 * tangential_delta_prime / radius**2
        - angular_eigenvalue * shear_delta / (lapse * radius**2)
    )
    raw_angular_delta_prime = shear_delta + tangential_delta_prime
    raw_angular_delta = -intrinsic_shear + 2.0 * shear_delta / radius + tangential_delta

    root_lapse = sqrt(lapse)
    mean_curvature = 2.0 * root_lapse / radius + lapse_derivative / (2.0 * root_lapse)
    mean_curvature_derivative = (
        lapse_derivative / (root_lapse * radius)
        - 2.0 * root_lapse / radius**2
        + lapse_second_derivative / (2.0 * root_lapse)
        - lapse_derivative**2 / (4.0 * lapse**1.5)
    )
    shape_curvature = mean_curvature_derivative + angular_eigenvalue / (
        radius**2 * root_lapse
    )
    background_conservation = (
        background_radial_derivative
        + connection * (background_energy + background_radial)
        + 2.0 * (background_radial - background_tangential) / radius
    )
    equilibrium = background_radial - tension * mean_curvature
    normal_force = (
        intrinsic_radial
        + displacement * background_radial_derivative
        - tension * shape_curvature * displacement
    )
    tangential_force = intrinsic_shear - displacement * (
        background_tangential - background_radial
    )
    factorized_radial_delta_prime = displacement * equilibrium
    factorized_radial_delta = -normal_force + displacement * background_conservation
    factorized_angular_delta_prime = 0.0
    factorized_angular_delta = -tangential_force + displacement * equilibrium
    factorization_error = max(
        abs(raw_radial_delta_prime - factorized_radial_delta_prime),
        abs(raw_radial_delta - factorized_radial_delta),
        abs(raw_angular_delta_prime - factorized_angular_delta_prime),
        abs(raw_angular_delta - factorized_angular_delta),
    )
    maximum_raw_coefficient = max(
        abs(raw_radial_delta_prime),
        abs(raw_radial_delta),
        abs(raw_angular_delta_prime),
        abs(raw_angular_delta),
    )
    return {
        "ell": ell,
        "angular_eigenvalue": angular_eigenvalue,
        "mean_curvature": mean_curvature,
        "shape_curvature_coefficient": shape_curvature,
        "background_young_laplace_residual": equilibrium,
        "background_bulk_conservation_residual": background_conservation,
        "linearized_normal_force_residual": normal_force,
        "linearized_tangential_force_residual": tangential_force,
        "radial_conservation_delta_prime_coefficient": raw_radial_delta_prime,
        "radial_conservation_delta_coefficient": raw_radial_delta,
        "angular_conservation_delta_prime_coefficient": raw_angular_delta_prime,
        "angular_conservation_delta_coefficient": raw_angular_delta,
        "factorized_radial_delta_prime_coefficient": (factorized_radial_delta_prime),
        "factorized_radial_delta_coefficient": factorized_radial_delta,
        "factorized_angular_delta_prime_coefficient": (factorized_angular_delta_prime),
        "factorized_angular_delta_coefficient": factorized_angular_delta,
        "factorization_maximum_error": factorization_error,
        "maximum_distributional_conservation_coefficient": maximum_raw_coefficient,
        "distributional_conservation_closes": maximum_raw_coefficient <= 1.0e-9,
        "claim_boundary": (
            "Fixed-background first-order distributional conservation for a "
            "constant-tension ideal shell; no Israel matching or surface "
            "elasticity"
        ),
    }


def default_membrane_distributional_conservation_record(
    *,
    node_count: int = 401,
    profile_step: float = 0.002,
) -> dict[str, object]:
    """Evaluate the distributional wall identities on the default BVP."""
    solution = solve_centrifugal_quadrupole_bvp(
        node_count=node_count,
        profile_step=profile_step,
    )
    parameters = solution["parameters"]
    pion_mass = float(parameters["pion_mass_mu"])
    curvature = float(parameters["curvature_lambda"])
    radius = float(parameters["wall_radius"])
    tension = float(parameters["membrane_tension"])
    _, points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=radius,
        step=profile_step,
    )
    _, profile, profile_derivative = points[-1]
    lapse = 1.0 - curvature * radius**2
    lapse_derivative = -2.0 * curvature * radius
    lapse_second_derivative = -2.0 * curvature
    sine = sin(profile)
    radial_strain = lapse * profile_derivative**2
    tangential_strain = sine**2 / radius**2
    potential = pion_mass**2 * (1.0 - cos(profile)) / 4.0
    background_energy = (
        radial_strain / 8.0
        + tangential_strain / 4.0
        + radial_strain * tangential_strain
        + tangential_strain**2 / 2.0
        + potential
    )
    background_radial = (
        radial_strain / 8.0
        - tangential_strain / 4.0
        + radial_strain * tangential_strain
        - tangential_strain**2 / 2.0
        - potential
    )
    background_tangential = (
        -radial_strain / 8.0 + tangential_strain**2 / 2.0 - potential
    )
    pressure_derivative = hard_wall_background_pressure_derivative(
        wall_radius=radius,
        curvature=curvature,
        wall_profile_derivative=profile_derivative,
    )["background_pressure_radial_derivative"]
    stress = centrifugal_quadrupole_stress_amplitudes(
        radius=radius,
        metric_factor=lapse,
        profile=profile,
        profile_derivative=profile_derivative,
        radial_field=float(solution["wall_radial_field"]),
        radial_field_derivative=float(solution["wall_radial_field_derivative"]),
        tangential_field=float(solution["wall_tangential_field"]),
        tangential_field_derivative=0.0,
        pion_mass=pion_mass,
    )
    conservation = distributional_wall_conservation_coefficients(
        ell=2,
        wall_radius=radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_derivative,
        wall_metric_factor_second_derivative=lapse_second_derivative,
        membrane_tension=tension,
        wall_displacement_coefficient=float(solution["wall_shape_coefficient"]),
        background_energy_density=background_energy,
        background_radial_pressure=background_radial,
        background_radial_pressure_derivative=float(pressure_derivative),
        background_tangential_pressure=background_tangential,
        intrinsic_radial_pressure_multipole=float(stress["total_radial_pressure"]),
        intrinsic_radial_angular_shear_multipole=float(
            stress["total_radial_angular_shear"]
        ),
    )
    claims = {
        "distributional_factorization_is_exact_numerically": (
            conservation["factorization_maximum_error"] < 1.0e-14
        ),
        "background_young_laplace_balance_closes": (
            abs(conservation["background_young_laplace_residual"]) < 1.0e-10
        ),
        "linearized_normal_force_balance_closes": (
            abs(conservation["linearized_normal_force_residual"]) < 1.0e-9
        ),
        "linearized_tangential_force_balance_closes": (
            abs(conservation["linearized_tangential_force_residual"]) < 1.0e-9
        ),
        "bulk_plus_shell_distribution_is_conserved": conservation[
            "distributional_conservation_closes"
        ],
    }
    return {
        "goal": "Distributional Centrifugal Skyrmion Membrane Completion",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "floating_bulk_plus_nambu_goto_wall_conservation",
        "parameters": parameters,
        "wall_profile": profile,
        "wall_profile_derivative": profile_derivative,
        "wall_displacement_coefficient": solution["wall_shape_coefficient"],
        "wall_stress": {
            "intrinsic_radial_pressure_multipole": stress["total_radial_pressure"],
            "intrinsic_radial_angular_shear_multipole": stress[
                "total_radial_angular_shear"
            ],
        },
        "distributional_conservation": conservation,
        "certified_claims": claims,
        "claim_boundary": (
            "Floating fixed-background first-order wall completion at the "
            "default point. The exact distributional factorization is "
            "analytic, but the profile/BVP inputs are not interval enclosed. "
            "No Israel matching, surface elasticity, or master-source "
            "projection is included."
        ),
    }
