"""Tensorial Israel gates for static spherical and perturbed thin shells.

The metric convention in the spherical routines is

``ds^2=-A(r) dt^2+dr^2/B(r)+r^2 dOmega^2``.

The same unit normal, directed from the inner (``-``) region to the outer
(``+``) region, is used on both sides.  With

``[K_i^j]-delta_i^j[K]=-kappa S_i^j``

and a positive-tension Nambu--Goto shell ``S_i^j=-sigma delta_i^j``, every
principal extrinsic-curvature jump is ``-kappa sigma/2``.  This module keeps
that tensorial statement separate from a one-dimensional master-equation
transmission condition.
"""

from __future__ import annotations

from math import isfinite, sqrt


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(name: str, value: float) -> float:
    value = _finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def spherical_mixed_extrinsic_curvature(
    *,
    radius: float,
    lapse: float,
    lapse_derivative: float,
    radial_metric_function: float | None = None,
) -> dict[str, float | str]:
    """Return the two principal mixed extrinsic curvatures of ``r=radius``.

    ``lapse`` is ``A`` and ``radial_metric_function`` is ``B``.  The latter
    defaults to ``A``, as in a vacuum Schwarzschild--de Sitter chart.
    """
    radius = _positive("radius", radius)
    lapse = _positive("lapse", lapse)
    lapse_derivative = _finite("lapse_derivative", lapse_derivative)
    radial = lapse if radial_metric_function is None else _positive(
        "radial_metric_function", radial_metric_function
    )
    root_radial = sqrt(radial)
    temporal = root_radial * lapse_derivative / (2.0 * lapse)
    angular = root_radial / radius
    return {
        "temporal_mixed_extrinsic_curvature": temporal,
        "angular_mixed_extrinsic_curvature": angular,
        "mixed_trace": temporal + 2.0 * angular,
        "normal_convention": "one normal directed from inner to outer region",
    }


def pure_tension_spherical_israel_record(
    *,
    radius: float,
    inner_lapse: float,
    inner_lapse_derivative: float,
    outer_lapse: float,
    outer_lapse_derivative: float,
    surface_tension: float,
    gravitational_coupling: float,
    inner_radial_metric_function: float | None = None,
    outer_radial_metric_function: float | None = None,
) -> dict[str, float | bool | str]:
    """Evaluate both independent Israel equations for a spherical shell."""
    tension = _positive("surface_tension", surface_tension)
    coupling = _positive("gravitational_coupling", gravitational_coupling)
    inner = spherical_mixed_extrinsic_curvature(
        radius=radius,
        lapse=inner_lapse,
        lapse_derivative=inner_lapse_derivative,
        radial_metric_function=inner_radial_metric_function,
    )
    outer = spherical_mixed_extrinsic_curvature(
        radius=radius,
        lapse=outer_lapse,
        lapse_derivative=outer_lapse_derivative,
        radial_metric_function=outer_radial_metric_function,
    )
    jump_t = float(outer["temporal_mixed_extrinsic_curvature"]) - float(
        inner["temporal_mixed_extrinsic_curvature"]
    )
    jump_a = float(outer["angular_mixed_extrinsic_curvature"]) - float(
        inner["angular_mixed_extrinsic_curvature"]
    )
    jump_trace = jump_t + 2.0 * jump_a
    half_coupling_tension = coupling * tension / 2.0

    # Reduced equations: [K_t^t]=[K_theta^theta]=-kappa sigma/2.
    temporal_reduced = jump_t + half_coupling_tension
    angular_reduced = jump_a + half_coupling_tension

    # Unreduced tensor equations provide an independent sign/trace audit.
    temporal_tensor = jump_t - jump_trace - coupling * tension
    angular_tensor = jump_a - jump_trace - coupling * tension
    maximum = max(
        abs(temporal_reduced),
        abs(angular_reduced),
        abs(temporal_tensor),
        abs(angular_tensor),
    )
    return {
        "temporal_extrinsic_curvature_jump": jump_t,
        "angular_extrinsic_curvature_jump": jump_a,
        "trace_jump": jump_trace,
        "required_principal_jump": -half_coupling_tension,
        "temporal_reduced_israel_residual": temporal_reduced,
        "angular_reduced_israel_residual": angular_reduced,
        "temporal_tensor_israel_residual": temporal_tensor,
        "angular_tensor_israel_residual": angular_tensor,
        "maximum_israel_residual": maximum,
        "israel_matching_closes": maximum <= 1.0e-11,
        "identity": (
            "[K_i^j]-delta_i^j[K]=kappa*sigma*delta_i^j iff "
            "[K_t^t]=[K_theta^theta]=-kappa*sigma/2"
        ),
    }


def identical_geometry_pure_tension_no_go_record(
    *,
    radius: float,
    lapse: float,
    lapse_derivative: float,
    surface_tension: float,
    gravitational_coupling: float,
    radial_metric_function: float | None = None,
) -> dict[str, float | bool | str]:
    """Show that a smooth identical geometry cannot carry positive tension."""
    record = pure_tension_spherical_israel_record(
        radius=radius,
        inner_lapse=lapse,
        inner_lapse_derivative=lapse_derivative,
        outer_lapse=lapse,
        outer_lapse_derivative=lapse_derivative,
        surface_tension=surface_tension,
        gravitational_coupling=gravitational_coupling,
        inner_radial_metric_function=radial_metric_function,
        outer_radial_metric_function=radial_metric_function,
    )
    obstruction = _positive("gravitational_coupling", gravitational_coupling) * (
        _positive("surface_tension", surface_tension)
    ) / 2.0
    record.update(
        {
            "exact_reduced_obstruction": obstruction,
            "nonzero_tension_is_obstructed": obstruction > 0.0
            and not bool(record["israel_matching_closes"]),
            "claim": (
                "Identical inner and outer extrinsic curvatures have zero jump, "
                "whereas a positive-tension shell requires -kappa*sigma/2."
            ),
        }
    )
    return record


def de_sitter_kottler_static_shell_benchmark(
    *,
    radius: float,
    compact_radius_ratio_squared: float,
    gravitational_coupling: float = 1.0,
) -> dict[str, float | bool | str | dict[str, float | bool | str]]:
    """Construct an exact static pure-tension de Sitter/Kottler shell.

    The inner region is regular de Sitter and the outer region has the same
    cosmological radius and Kottler mass length ``m=G M``.  Static positive
    tension with both lapses positive requires ``1/3<u<2/3``, where
    ``u=a^2/R^2``.  Solving both Israel equations gives

    ``alpha*a=2(2-3u)/(3 sqrt(1-u))`` and
    ``m/a=2(2-3u)/(9(1-u))``, with ``alpha=kappa*sigma/2``.
    """
    radius = _positive("radius", radius)
    u = _finite("compact_radius_ratio_squared", compact_radius_ratio_squared)
    if not 1.0 / 3.0 < u < 2.0 / 3.0:
        raise ValueError("compact_radius_ratio_squared must lie in (1/3, 2/3)")
    coupling = _positive("gravitational_coupling", gravitational_coupling)
    patch_radius = radius / sqrt(u)
    root_inner = sqrt(1.0 - u)
    alpha_radius = 2.0 * (2.0 - 3.0 * u) / (3.0 * root_inner)
    alpha = alpha_radius / radius
    tension = 2.0 * alpha / coupling
    mass_length = radius * 2.0 * (2.0 - 3.0 * u) / (9.0 * (1.0 - u))
    inner_lapse = 1.0 - u
    outer_lapse = inner_lapse - 2.0 * mass_length / radius
    inner_derivative = -2.0 * radius / patch_radius**2
    outer_derivative = 2.0 * mass_length / radius**2 + inner_derivative
    israel = pure_tension_spherical_israel_record(
        radius=radius,
        inner_lapse=inner_lapse,
        inner_lapse_derivative=inner_derivative,
        outer_lapse=outer_lapse,
        outer_lapse_derivative=outer_derivative,
        surface_tension=tension,
        gravitational_coupling=coupling,
    )
    root_lapse_identity_error = sqrt(outer_lapse) - (root_inner - alpha_radius)
    return {
        "wall_radius": radius,
        "static_patch_radius": patch_radius,
        "u=a^2/R^2": u,
        "surface_tension": tension,
        "alpha=kappa*sigma/2": alpha,
        "kottler_mass_length_GM": mass_length,
        "inner_lapse_at_wall": inner_lapse,
        "outer_lapse_at_wall": outer_lapse,
        "outer_lapse_is_positive": outer_lapse > 0.0,
        "root_lapse_identity_error": root_lapse_identity_error,
        "israel": israel,
        "benchmark_closes": bool(israel["israel_matching_closes"])
        and abs(root_lapse_identity_error) <= 1.0e-12,
        "claim_boundary": (
            "Exact vacuum thin-shell benchmark only; it does not include the "
            "Skyrmion interior or its ell=2 perturbation."
        ),
    }


def linearized_constant_tension_israel_gate(
    *,
    inner_induced_metric_amplitudes: tuple[float, float, float],
    outer_induced_metric_amplitudes: tuple[float, float, float],
    inner_mixed_extrinsic_curvature_amplitudes: tuple[float, float, float],
    outer_mixed_extrinsic_curvature_amplitudes: tuple[float, float, float],
    tolerance: float = 1.0e-11,
) -> dict[str, object]:
    """Evaluate the tensorial ``ell>=2`` gate after background matching.

    Each tuple contains temporal-scalar, angular-trace, and angular-tracefree
    harmonic amplitudes pulled back to the *physical displaced shell*.  For a
    constant-tension shell the mixed surface stress is exactly
    ``S_i^j=-sigma delta_i^j``.  Its nonspherical perturbation therefore
    vanishes, and linearized Israel matching requires continuity of the first
    form and of all three mixed-extrinsic-curvature amplitudes.

    Computing these six geometric amplitudes from a master field is a separate
    reconstruction problem; accepting them explicitly prevents a scalar jump
    test from masquerading as tensorial Israel matching.
    """
    tolerance = _positive("tolerance", tolerance)
    if len(inner_induced_metric_amplitudes) != 3 or len(
        outer_induced_metric_amplitudes
    ) != 3:
        raise ValueError("induced metric tuples must each have length three")
    if len(inner_mixed_extrinsic_curvature_amplitudes) != 3 or len(
        outer_mixed_extrinsic_curvature_amplitudes
    ) != 3:
        raise ValueError("extrinsic-curvature tuples must each have length three")
    inner_q = tuple(_finite("inner induced amplitude", x) for x in inner_induced_metric_amplitudes)
    outer_q = tuple(_finite("outer induced amplitude", x) for x in outer_induced_metric_amplitudes)
    inner_k = tuple(
        _finite("inner extrinsic amplitude", x)
        for x in inner_mixed_extrinsic_curvature_amplitudes
    )
    outer_k = tuple(
        _finite("outer extrinsic amplitude", x)
        for x in outer_mixed_extrinsic_curvature_amplitudes
    )
    first_form = tuple(outer - inner for inner, outer in zip(inner_q, outer_q))
    second_form = tuple(outer - inner for inner, outer in zip(inner_k, outer_k))
    maximum = max(*(abs(x) for x in first_form), *(abs(x) for x in second_form))
    labels = ("temporal_scalar", "angular_trace", "angular_tracefree")
    return {
        "first_form_jump_amplitudes": dict(zip(labels, first_form)),
        "mixed_extrinsic_curvature_jump_amplitudes": dict(zip(labels, second_form)),
        "maximum_tensorial_junction_residual": maximum,
        "tensorial_linearized_israel_matching_closes": maximum <= tolerance,
        "tolerance": tolerance,
        "required_inputs": (
            "physical-shell pullbacks including displacement and gauge terms"
        ),
        "identity": (
            "delta S_i^j=0 for constant tension; hence [delta q_ij]=0 and "
            "[delta K_i^j]=0 after the spherical Israel equations hold"
        ),
    }
