"""Conservation gates for a static even-parity stress multipole.

On ``ds^2=-f dt^2+dr^2/f+r^2 dOmega^2``, decompose one scalar harmonic as

    delta T^t_t = -rho Y,
    delta T^r_r = p_r Y,
    delta T^r_A = j D_A Y,
    delta T^A_B = p_perp Y delta^A_B + pi Y^A_B,

where ``Y^A_B=D^A D_B Y+[l(l+1)/2]delta^A_B Y`` is trace free.
The two functions below are the exact radial and angular components of
``nabla_mu T^mu_nu=0`` in the smooth bulk.
"""

from __future__ import annotations

from math import isfinite


def _finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _multipole_number(ell: int) -> int:
    if isinstance(ell, bool) or not isinstance(ell, int) or ell < 2:
        raise ValueError("ell must be an integer at least two")
    return ell * (ell + 1)


def static_even_stress_conservation_residuals(
    *,
    ell: int,
    radius: float,
    metric_factor: float,
    metric_factor_derivative: float,
    energy_density: float,
    radial_pressure: float,
    radial_pressure_derivative: float,
    tangential_pressure: float,
    radial_angular_shear: float,
    radial_angular_shear_derivative: float,
    angular_tracefree_stress: float,
) -> dict[str, float | bool | str]:
    """Return the two exact bulk conservation residuals."""
    angular_eigenvalue = _multipole_number(ell)
    for name, value in (
        ("radius", radius),
        ("metric_factor", metric_factor),
        ("metric_factor_derivative", metric_factor_derivative),
        ("energy_density", energy_density),
        ("radial_pressure", radial_pressure),
        ("radial_pressure_derivative", radial_pressure_derivative),
        ("tangential_pressure", tangential_pressure),
        ("radial_angular_shear", radial_angular_shear),
        ("radial_angular_shear_derivative", radial_angular_shear_derivative),
        ("angular_tracefree_stress", angular_tracefree_stress),
    ):
        _finite(name, value)
    if radius <= 0.0:
        raise ValueError("radius must be positive")
    if metric_factor <= 0.0:
        raise ValueError("metric_factor must be positive")

    radial_residual = (
        radial_pressure_derivative
        + metric_factor_derivative
        * (energy_density + radial_pressure)
        / (2.0 * metric_factor)
        + 2.0 * (radial_pressure - tangential_pressure) / radius
        - angular_eigenvalue * radial_angular_shear / (metric_factor * radius**2)
    )
    angular_residual = (
        radial_angular_shear_derivative
        + 2.0 * radial_angular_shear / radius
        + tangential_pressure
        - (angular_eigenvalue - 2.0) * angular_tracefree_stress / 2.0
    )
    return {
        "ell": ell,
        "angular_eigenvalue": angular_eigenvalue,
        "radial_conservation_residual": radial_residual,
        "angular_conservation_residual": angular_residual,
        "bulk_source_is_conserved": (
            abs(radial_residual) <= 1.0e-12 and abs(angular_residual) <= 1.0e-12
        ),
        "convention": ("mixed stress components on ds^2=-f dt^2+dr^2/f+r^2dOmega^2"),
    }


def zero_momentum_static_relation(
    *,
    ell: int,
    tangential_pressure: float,
    angular_tracefree_stress: float,
) -> dict[str, float | bool | str]:
    """Audit angular conservation when ``j=0`` identically."""
    angular_eigenvalue = _multipole_number(ell)
    _finite("tangential_pressure", tangential_pressure)
    _finite("angular_tracefree_stress", angular_tracefree_stress)
    required_pressure = (angular_eigenvalue - 2.0) * angular_tracefree_stress / 2.0
    residual = tangential_pressure - required_pressure
    return {
        "ell": ell,
        "tangential_pressure": tangential_pressure,
        "angular_tracefree_stress": angular_tracefree_stress,
        "required_tangential_pressure": required_pressure,
        "angular_conservation_residual": residual,
        "zero_momentum_source_is_angularly_conserved": abs(residual) <= 1.0e-12,
        "quadrupole_specialization": (
            "For ell=2 and j=0, conservation requires p_perp=2 pi."
        ),
    }


def hard_wall_traction_jump_record(
    *,
    wall_radius: float,
    interior_radial_pressure: float,
    interior_radial_angular_shear: float,
) -> dict[str, float | bool | str]:
    """Return delta coefficients created by hard truncation at a wall.

    Multiplication by ``Theta(r_w-r)`` sends ``p_r'`` to
    ``p_r' Theta-p_r(r_w)delta`` and similarly for ``j'``.  A membrane source
    or vanishing traction is therefore required.
    """
    _finite("wall_radius", wall_radius)
    _finite("interior_radial_pressure", interior_radial_pressure)
    _finite("interior_radial_angular_shear", interior_radial_angular_shear)
    if wall_radius <= 0.0:
        raise ValueError("wall_radius must be positive")
    radial_delta = -interior_radial_pressure
    angular_delta = -interior_radial_angular_shear
    return {
        "wall_radius": wall_radius,
        "radial_conservation_delta_coefficient": radial_delta,
        "angular_conservation_delta_coefficient": angular_delta,
        "bulk_truncation_is_distributionally_conserved": (
            radial_delta == 0.0 and angular_delta == 0.0
        ),
        "required_completion": (
            "Add membrane stress whose intrinsic divergence and normal traction "
            "cancel these coefficients, or impose vanishing bulk traction."
        ),
    }


def static_even_stress_conservation_certificate() -> dict[str, object]:
    """Audit bulk identities, the l=2 zero-momentum relation, and wall jumps."""
    conserved = static_even_stress_conservation_residuals(
        ell=2,
        radius=1.0,
        metric_factor=1.0,
        metric_factor_derivative=0.0,
        energy_density=3.0,
        radial_pressure=1.0,
        radial_pressure_derivative=0.0,
        tangential_pressure=1.0,
        radial_angular_shear=0.0,
        radial_angular_shear_derivative=0.0,
        angular_tracefree_stress=0.5,
    )
    relation = zero_momentum_static_relation(
        ell=2,
        tangential_pressure=1.0,
        angular_tracefree_stress=0.5,
    )
    wall = hard_wall_traction_jump_record(
        wall_radius=4.0,
        interior_radial_pressure=2.0,
        interior_radial_angular_shear=0.25,
    )
    claims = {
        "manufactured_bulk_source_is_conserved": conserved["bulk_source_is_conserved"],
        "quadrupole_zero_momentum_relation_is_p_perp_equals_two_pi": relation[
            "zero_momentum_source_is_angularly_conserved"
        ],
        "hard_truncation_requires_membrane_traction": not wall[
            "bulk_truncation_is_distributionally_conserved"
        ],
    }
    return {
        "goal": "Conserved Static Even-Parity Matter Source Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_bulk_conservation_and_wall_traction_gate",
        "manufactured_conserved_source": conserved,
        "zero_momentum_quadrupole_relation": relation,
        "hard_wall_jump": wall,
        "certified_claims": claims,
        "claim_boundary": (
            "This is a kinematic conservation checker in the -+++ gravity "
            "convention. It does not derive the amplitudes from the +--- "
            "Skyrme action, convert conventions, or supply the membrane stress."
        ),
    }
