"""Kinematic and wall gates for centrifugal Skyrmion deformation.

The leading equivariant coordinate deformation of a spinning hedgehog has
three radial functions.  In the body frame, with angular velocity ``Omega``,

    delta y = A (Omega cross x)^2 x - 2 B r^2 Omega^2 x
              + C r^2 Omega cross (Omega cross x).

This is the Hata--Kikuchi basis, written so that ``A``, ``B``, and ``C`` are
the coefficients appearing in their coordinate-transformed static soliton.
The module isolates its exact monopole/quadrupole content and the boundary
conditions imposed by an ideal Dirichlet mirror.  It does not solve the three
coupled deformation equations.
"""

from __future__ import annotations

from math import cos, isfinite, sin, sqrt


def _finite(name: str, value: float) -> float:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(name: str, value: float) -> float:
    value = _finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def equivariant_deformation_multipoles(
    *,
    radius: float,
    function_a: float,
    function_b: float,
    function_c: float,
) -> dict[str, float | int | str]:
    """Return the exact ``ell=0`` and ``ell=2`` deformation coefficients.

    Write ``u=Omega dot n`` and ``P2=u^2-Omega^2/3``.  To quadratic order,

    ``delta r = d0 Omega^2 + d2 P2``

    and the tangential displacement is

    ``delta y_perp = t2 u (Omega-u n)``.

    The two quadrupole coefficients are independent.  A radial-profile-only
    ansatz sets ``t2=0`` and therefore does not span the general response.
    """
    radius = _positive("radius", radius)
    function_a = _finite("function_a", function_a)
    function_b = _finite("function_b", function_b)
    function_c = _finite("function_c", function_c)
    difference = function_a - function_c
    radial_scale = radius**3
    return {
        "radius": radius,
        "function_a_minus_c": difference,
        "radial_monopole_coefficient": radial_scale
        * (2.0 * difference / 3.0 - 2.0 * function_b),
        "radial_quadrupole_coefficient": -radial_scale * difference,
        "tangential_quadrupole_coefficient": radial_scale * function_c,
        "quadrupole_coefficient_map_determinant": -1.0,
        "quadrupole_response_rank": 2,
        "quadrupole_basis": (
            "delta r=d0 Omega^2+d2[(Omega.n)^2-Omega^2/3]; "
            "delta y_perp=t2 (Omega.n)[Omega-(Omega.n)n]"
        ),
        "scope": "kinematic decomposition through O(Omega^2)",
    }


def direct_vector_deformation_invariants(
    *,
    radius: float,
    omega_squared: float,
    omega_dot_direction: float,
    function_a: float,
    function_b: float,
    function_c: float,
) -> dict[str, float | str]:
    """Evaluate radial and tangential invariants of the deformation."""
    radius = _positive("radius", radius)
    omega_squared = _finite("omega_squared", omega_squared)
    omega_dot_direction = _finite("omega_dot_direction", omega_dot_direction)
    if omega_squared < 0.0:
        raise ValueError("omega_squared must be nonnegative")
    if omega_dot_direction**2 > omega_squared + 1.0e-14:
        raise ValueError("omega_dot_direction is incompatible with omega_squared")
    function_a = _finite("function_a", function_a)
    function_b = _finite("function_b", function_b)
    function_c = _finite("function_c", function_c)
    transverse_squared = max(0.0, omega_squared - omega_dot_direction**2)
    radial_displacement = radius**3 * (
        (function_a - function_c) * transverse_squared
        - 2.0 * function_b * omega_squared
    )
    tangential_prefactor = radius**3 * function_c * omega_dot_direction
    return {
        "radial_displacement": radial_displacement,
        "tangential_vector_prefactor": tangential_prefactor,
        "tangential_vector": (
            "prefactor times [Omega-(Omega.n)n]; its squared bracket norm is "
            "Omega^2-(Omega.n)^2"
        ),
    }


def ideal_mirror_pullback_residuals(
    *,
    wall_radius: float,
    function_a_at_wall: float,
    function_b_at_wall: float,
    function_c_at_wall: float,
    wall_monopole_displacement_coefficient: float = 0.0,
    wall_quadrupole_displacement_coefficient: float = 0.0,
) -> dict[str, float | bool | str]:
    """Return the two ideal-mirror pullback residuals at a deformed wall.

    The wall displacement is ``xi=xi0 Omega^2+xi2 P2``.  For a nonzero static
    wall slope, ``U=1`` requires the sum of wall and coordinate radial
    displacements to vanish independently in the monopole and quadrupole
    sectors.
    """
    multipoles = equivariant_deformation_multipoles(
        radius=wall_radius,
        function_a=function_a_at_wall,
        function_b=function_b_at_wall,
        function_c=function_c_at_wall,
    )
    wall_monopole_displacement_coefficient = _finite(
        "wall_monopole_displacement_coefficient",
        wall_monopole_displacement_coefficient,
    )
    wall_quadrupole_displacement_coefficient = _finite(
        "wall_quadrupole_displacement_coefficient",
        wall_quadrupole_displacement_coefficient,
    )
    monopole_residual = wall_monopole_displacement_coefficient + float(
        multipoles["radial_monopole_coefficient"]
    )
    quadrupole_residual = wall_quadrupole_displacement_coefficient + float(
        multipoles["radial_quadrupole_coefficient"]
    )
    return {
        **multipoles,
        "wall_monopole_displacement_coefficient": (
            wall_monopole_displacement_coefficient
        ),
        "wall_quadrupole_displacement_coefficient": (
            wall_quadrupole_displacement_coefficient
        ),
        "monopole_pullback_residual": monopole_residual,
        "quadrupole_pullback_residual": quadrupole_residual,
        "ideal_mirror_pullback_is_satisfied": (
            abs(monopole_residual) <= 1.0e-12 and abs(quadrupole_residual) <= 1.0e-12
        ),
        "fixed_wall_condition": "A(r_w)=C(r_w) and B(r_w)=0",
        "tangential_note": (
            "C(r_w) is not fixed by U=1 because the internal direction is "
            "degenerate where sin(F)=0."
        ),
    }


def required_comoving_wall_displacement(
    *,
    wall_radius: float,
    function_a_at_wall: float,
    function_b_at_wall: float,
    function_c_at_wall: float,
) -> dict[str, float | bool]:
    """Return wall coefficients that cancel the field-coordinate displacement."""
    multipoles = equivariant_deformation_multipoles(
        radius=wall_radius,
        function_a=function_a_at_wall,
        function_b=function_b_at_wall,
        function_c=function_c_at_wall,
    )
    monopole = -float(multipoles["radial_monopole_coefficient"])
    quadrupole = -float(multipoles["radial_quadrupole_coefficient"])
    check = ideal_mirror_pullback_residuals(
        wall_radius=wall_radius,
        function_a_at_wall=function_a_at_wall,
        function_b_at_wall=function_b_at_wall,
        function_c_at_wall=function_c_at_wall,
        wall_monopole_displacement_coefficient=monopole,
        wall_quadrupole_displacement_coefficient=quadrupole,
    )
    return {
        "required_wall_monopole_displacement_coefficient": monopole,
        "required_wall_quadrupole_displacement_coefficient": quadrupole,
        "pullback_check_passes": check["ideal_mirror_pullback_is_satisfied"],
    }


def fixed_spherical_wall_quadrupole_traction(
    *,
    wall_radius: float,
    wall_metric_factor: float,
    wall_profile_derivative: float,
    derivative_of_a_minus_c_at_wall: float,
) -> dict[str, float | bool | str]:
    """Return the induced ``ell=2`` radial-pressure coefficient at a fixed wall.

    Fixed-wall Dirichlet data require ``A-C=0`` at the wall.  Then
    ``delta F'_2=-r_w^3 F'_w (A-C)' P2``.  In the repository's dimensionless
    pressure normalization, ``p_w=N_w F_w'^2/8``, so the linear pressure
    coefficient is the value returned below.  A spherical pure-tension wall
    has no ``ell=2`` curvature response; absent an anchor, this coefficient
    must vanish as well.
    """
    wall_radius = _positive("wall_radius", wall_radius)
    wall_metric_factor = _positive("wall_metric_factor", wall_metric_factor)
    wall_profile_derivative = _finite(
        "wall_profile_derivative", wall_profile_derivative
    )
    derivative = _finite(
        "derivative_of_a_minus_c_at_wall",
        derivative_of_a_minus_c_at_wall,
    )
    pressure_coefficient = -(
        wall_metric_factor
        * wall_profile_derivative**2
        * wall_radius**3
        * derivative
        / 4.0
    )
    return {
        "quadrupole_radial_pressure_coefficient": pressure_coefficient,
        "unanchored_fixed_spherical_wall_is_force_balanced": (
            abs(pressure_coefficient) <= 1.0e-12
        ),
        "additional_fixed_wall_condition": (
            "(A-C)'(r_w)=0 unless an ell=2 anchor or wall deformation supplies "
            "the reaction"
        ),
    }


def static_patch_shell_shape_curvature_coefficient(
    *,
    wall_radius: float,
    curvature: float,
    ell: int,
) -> dict[str, float | int | str]:
    """Return ``delta K/xi`` for a static shell-shape harmonic.

    For ``N=1-lambda r^2`` and coordinate displacement ``xi Y_ellm``, direct
    expansion of the unit-normal divergence gives

    ``delta K=[K'(a)+ell(ell+1)/(a^2 sqrt(N_a))] xi Y_ellm``.

    The constant-mode term agrees with direct differentiation of the centered
    shell curvature.  In flat space the coefficients for ``ell=0,1,2`` are
    ``-2/a^2, 0, 4/a^2``, respectively.
    """
    wall_radius = _positive("wall_radius", wall_radius)
    curvature = _finite("curvature", curvature)
    if curvature < 0.0:
        raise ValueError("curvature must be nonnegative")
    if isinstance(ell, bool) or not isinstance(ell, int) or ell < 0:
        raise ValueError("ell must be a nonnegative integer")
    lapse = 1.0 - curvature * wall_radius**2
    if lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    root_lapse = sqrt(lapse)
    centered_derivative = (
        -2.0 * root_lapse / wall_radius**2
        - 3.0 * curvature / root_lapse
        - curvature**2 * wall_radius**2 / lapse**1.5
    )
    angular_contribution = ell * (ell + 1.0) / (wall_radius**2 * root_lapse)
    return {
        "ell": ell,
        "wall_metric_factor": lapse,
        "centered_curvature_derivative": centered_derivative,
        "angular_laplacian_contribution": angular_contribution,
        "shape_curvature_coefficient": (centered_derivative + angular_contribution),
        "convention": (
            "delta K=coefficient*xi*Y for outward coordinate displacement xi"
        ),
    }


def hard_wall_background_pressure_derivative(
    *,
    wall_radius: float,
    curvature: float,
    wall_profile_derivative: float,
) -> dict[str, float | str]:
    """Return the local radial derivative of the static pressure at ``F=0``.

    In the repository normalization ``p=N F'^2/8`` at the hard wall.  The
    static profile equation gives ``F''=-(N'/N+2/r)F'`` there, and hence

    ``p'=-N' F'^2/8-N F'^2/(2r)``.

    This is a spatial derivative of the background solution.  It is not the
    derivative of pressure along the family of re-solved spherical cavities.
    """
    wall_radius = _positive("wall_radius", wall_radius)
    curvature = _finite("curvature", curvature)
    if curvature < 0.0:
        raise ValueError("curvature must be nonnegative")
    derivative = _finite("wall_profile_derivative", wall_profile_derivative)
    lapse = 1.0 - curvature * wall_radius**2
    if lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    lapse_derivative = -2.0 * curvature * wall_radius
    pressure_derivative = -(
        lapse_derivative * derivative**2 / 8.0
        + lapse * derivative**2 / (2.0 * wall_radius)
    )
    return {
        "wall_metric_factor": lapse,
        "wall_metric_factor_derivative": lapse_derivative,
        "wall_profile_derivative": derivative,
        "background_pressure_radial_derivative": pressure_derivative,
        "scope": "local derivative on the fixed static hard-wall profile",
    }


def scalar_quadrupole_restricted_equation(
    *,
    radius: float,
    metric_factor: float,
    metric_factor_derivative: float,
    profile: float,
    profile_derivative: float,
    profile_second_derivative: float,
    pion_mass: float,
) -> dict[str, float | str]:
    """Return the profile-only ``ell=2`` Jacobi equation and rigid forcing.

    This is the exact restriction ``delta F=f(r) q(n)`` with the hedgehog
    direction held fixed.  The equation is

    ``[-(P f')'+Q2 f]=-4 E_H``.

    Its source is tied exactly to the radial conservation defect of the rigid
    stress.  The independent tangential field equation is absent, so this
    restricted equation is a diagnostic rather than a consistent truncation.
    """
    radius = _positive("radius", radius)
    metric_factor = _positive("metric_factor", metric_factor)
    metric_factor_derivative = _finite(
        "metric_factor_derivative", metric_factor_derivative
    )
    profile = _finite("profile", profile)
    profile_derivative = _finite("profile_derivative", profile_derivative)
    profile_second_derivative = _finite(
        "profile_second_derivative", profile_second_derivative
    )
    pion_mass = _finite("pion_mass", pion_mass)
    if pion_mass < 0.0:
        raise ValueError("pion_mass must be nonnegative")

    sine = sin(profile)
    cosine = cos(profile)
    sine_twice = sin(2.0 * profile)
    cosine_twice = cos(2.0 * profile)
    radius_squared = radius**2
    sine_squared = sine**2
    profile_factor = radius_squared + 8.0 * sine_squared
    principal = metric_factor * profile_factor
    radial_potential = (
        4.0 * sine_twice**2 / radius_squared
        + 2.0 * (1.0 + 4.0 * sine_squared / radius_squared) * cosine_twice
        - 8.0 * metric_factor * cosine_twice * profile_derivative**2
        + pion_mass**2 * radius_squared * cosine
        - 8.0 * metric_factor_derivative * sine_twice * profile_derivative
        - 8.0 * metric_factor * sine_twice * profile_second_derivative
    )
    angular_potential = 6.0 * (1.0 + 4.0 * sine_squared / radius_squared)
    quadrupole_potential = radial_potential + angular_potential
    routhian_density = (
        radius_squared * sine_squared / (8.0 * metric_factor)
        + radius_squared * sine_squared * profile_derivative**2 / 2.0
        + sine_squared**2 / (2.0 * metric_factor)
    )
    routhian_euler_derivative = (
        radius_squared
        / metric_factor
        * (
            sine
            * cosine
            * (
                0.25
                + 2.0 * sine_squared / radius_squared
                - metric_factor * profile_derivative**2
            )
            - sine_squared
            * (
                metric_factor * profile_second_derivative
                + 2.0 * metric_factor * profile_derivative / radius
            )
        )
    )
    rigid_radial_residual = -(
        profile_derivative * routhian_euler_derivative / radius_squared
    )
    sigma_coefficient = sine_squared / (8.0 * metric_factor)
    skyrme_coefficient = sine_squared / (2.0 * metric_factor)
    radial_strain_squared = metric_factor * profile_derivative**2
    tangential_strain_squared = sine_squared / radius_squared
    rigid_angular_residual = -(
        sigma_coefficient
        + skyrme_coefficient * (radial_strain_squared - 2.0 * tangential_strain_squared)
    )
    return {
        "jacobi_principal_coefficient": principal,
        "radial_jacobi_potential": radial_potential,
        "ell2_angular_potential": angular_potential,
        "ell2_jacobi_potential": quadrupole_potential,
        "rigid_rotational_routhian_density": routhian_density,
        "routhian_euler_derivative": routhian_euler_derivative,
        "ell2_equation_source": -4.0 * routhian_euler_derivative,
        "rigid_radial_conservation_residual_coefficient": rigid_radial_residual,
        "radial_hilbert_identity_residual": (
            rigid_radial_residual
            + profile_derivative * routhian_euler_derivative / radius_squared
        ),
        "rigid_angular_conservation_residual_coefficient": (rigid_angular_residual),
        "operator": "L2 f=-(P f')'+Q2 f=-4 E_H",
        "boundary_conditions": (
            "scalar-only regularity f=O(r^3); fixed mirror f(a)=0; moving "
            "mirror f(a)+F'(a)xi2=0"
        ),
        "claim_boundary": (
            "The scalar equation enforces only the radial projection. The "
            "tangential quadrupole field and its Euler-Lagrange equation are "
            "required for full stress conservation."
        ),
    }


def hata_quadrupole_physical_fields(
    *,
    radius: float,
    profile: float,
    profile_derivative: float,
    function_a_minus_c: float,
    function_c: float,
) -> dict[str, float | str]:
    """Map Hata coordinate functions to regular physical ``ell=2`` fields."""
    radius = _positive("radius", radius)
    profile = _finite("profile", profile)
    profile_derivative = _finite("profile_derivative", profile_derivative)
    difference = _finite("function_a_minus_c", function_a_minus_c)
    function_c = _finite("function_c", function_c)
    radial_field = -(radius**3) * profile_derivative * difference
    tangential_field = sin(profile) * radius**2 * function_c
    return {
        "radial_profile_field_f": radial_field,
        "tangential_orientation_field_g": tangential_field,
        "field_basis": ("delta Y=f q e_F+g[Qn-qn], with q=Q_ab n_a n_b"),
        "origin_regular_subspace": (
            "g=g1 r+O(r^3), f=-g1 r+O(r^3), and f+g=O(r^3); "
            "raw A,C need not remain finite"
        ),
    }


def quadrupole_static_hessian_density(
    *,
    radius: float,
    metric_factor: float,
    profile: float,
    profile_derivative: float,
    radial_field: float,
    tangential_field: float,
    radial_field_derivative: float,
    tangential_field_derivative: float,
    pion_mass: float,
) -> float:
    """Return the angular-averaged static Hessian for the physical ``K=2`` pair.

    The quadrupole tensor is normalized to
    ``Q=Omega Omega-delta Omega^2/3`` with ``Omega^2=1``.  Thus
    ``<q^2>=4/45`` and ``<|Qn-qn|^2>=2/15``.  The result is the exact second
    variation density, not yet integrated over ``4 pi r^2 dr`` and not
    integrated by parts in ``r``.
    """
    radius = _positive("radius", radius)
    metric_factor = _positive("metric_factor", metric_factor)
    profile = _finite("profile", profile)
    profile_derivative = _finite("profile_derivative", profile_derivative)
    radial_field = _finite("radial_field", radial_field)
    tangential_field = _finite("tangential_field", tangential_field)
    radial_field_derivative = _finite(
        "radial_field_derivative", radial_field_derivative
    )
    tangential_field_derivative = _finite(
        "tangential_field_derivative", tangential_field_derivative
    )
    pion_mass = _finite("pion_mass", pion_mass)
    if pion_mass < 0.0:
        raise ValueError("pion_mass must be nonnegative")

    sine = sin(profile)
    cosine = cos(profile)
    radius_squared = radius**2
    q_squared_average = 4.0 / 45.0
    tangent_squared_average = 2.0 / 15.0
    tangent_derivative_squared_average = 4.0 / 5.0
    angular_tensor_squared_average = 2.0 / 3.0

    perturbation_squared = (
        radial_field**2 * q_squared_average
        + tangential_field**2 * tangent_squared_average
    )
    radial_b = (
        2.0 * radial_field_derivative**2 * q_squared_average
        + 2.0 * tangential_field_derivative**2 * tangent_squared_average
        - 2.0 * tangential_field**2 * tangent_squared_average * profile_derivative**2
    )
    angular_gradient_squared = (
        4.0 * radial_field**2 * tangent_squared_average
        + 2.0 * radial_field**2 * q_squared_average * cosine**2
        + tangential_field**2 * tangent_derivative_squared_average
        - 4.0 * radial_field * tangential_field * cosine * tangent_squared_average
        - 6.0 * radial_field * tangential_field * cosine * q_squared_average
    )
    angular_b_trace = (
        2.0 * angular_gradient_squared - 4.0 * perturbation_squared * sine**2
    )
    hessian_b_trace = metric_factor * radial_b + angular_b_trace / radius_squared

    a_trace_coefficient = (
        2.0 * metric_factor * profile_derivative * radial_field_derivative
        + 2.0
        * sine
        / radius_squared
        * (2.0 * radial_field * cosine - 3.0 * tangential_field)
    )
    a_trace_squared = q_squared_average * a_trace_coefficient**2
    radial_angular_a_coefficient = (
        sine * tangential_field_derivative
        + profile_derivative * (2.0 * radial_field - cosine * tangential_field)
    )
    angular_a_squared = (
        4.0
        * sine**2
        * (
            2.0 * radial_field**2 * cosine**2 * q_squared_average
            - 6.0 * radial_field * cosine * tangential_field * q_squared_average
            + tangential_field**2 * angular_tensor_squared_average
        )
    )
    a_squared_trace = (
        4.0
        * metric_factor**2
        * profile_derivative**2
        * radial_field_derivative**2
        * q_squared_average
        + 2.0
        * metric_factor
        / radius_squared
        * radial_angular_a_coefficient**2
        * tangent_squared_average
        + angular_a_squared / radius_squared**2
    )
    background_strain_trace = (
        metric_factor * profile_derivative**2 + 2.0 * sine**2 / radius_squared
    )
    g_times_b_trace = (
        metric_factor**2 * profile_derivative**2 * radial_b
        + sine**2 * angular_b_trace / radius_squared**2
    )
    return (
        radius_squared * hessian_b_trace / 8.0
        + radius_squared
        / 2.0
        * (
            a_trace_squared
            + background_strain_trace * hessian_b_trace
            - a_squared_trace
            - g_times_b_trace
        )
        + pion_mass**2 * radius_squared * cosine * perturbation_squared / 4.0
    )


def quadrupole_static_hessian_matrix(
    *,
    radius: float,
    metric_factor: float,
    profile: float,
    profile_derivative: float,
    pion_mass: float,
) -> dict[str, object]:
    """Polarize the local Hessian into the variables ``(f,g,f',g')``."""
    labels = ("f", "g", "f_prime", "g_prime")

    def evaluate(vector: tuple[float, float, float, float]) -> float:
        return quadrupole_static_hessian_density(
            radius=radius,
            metric_factor=metric_factor,
            profile=profile,
            profile_derivative=profile_derivative,
            radial_field=vector[0],
            tangential_field=vector[1],
            radial_field_derivative=vector[2],
            tangential_field_derivative=vector[3],
            pion_mass=pion_mass,
        )

    basis = tuple(
        tuple(1.0 if row == column else 0.0 for row in range(4)) for column in range(4)
    )
    diagonal = tuple(evaluate(vector) for vector in basis)
    matrix_rows: list[tuple[float, ...]] = []
    for row in range(4):
        entries: list[float] = []
        for column in range(4):
            if row == column:
                entries.append(diagonal[row])
                continue
            combined = tuple(
                basis[row][index] + basis[column][index] for index in range(4)
            )
            entries.append(
                (evaluate(combined) - diagonal[row] - diagonal[column]) / 2.0
            )
        matrix_rows.append(tuple(entries))
    matrix = tuple(matrix_rows)
    return {
        "variable_order": labels,
        "symmetric_hessian_matrix": matrix,
        "radial_field_principal_coefficient": matrix[2][2],
        "tangential_field_principal_coefficient": matrix[3][3],
        "normalization": (
            "angular average for Q=Omega Omega-delta/3 and Omega^2=1; "
            "multiply by 4pi for the sphere integral"
        ),
    }


def rotational_quadrupole_source_covector(
    *,
    radius: float,
    metric_factor: float,
    profile: float,
    profile_derivative: float,
) -> dict[str, float | str]:
    """Return the angular-averaged first variation of the rotational Routhian.

    Coefficients multiply ``(f,g,f',g')`` in the regular physical-field basis.
    The scalar entries equal ``-<q^2>(H_F,H_F')`` and therefore reproduce the
    source in :func:`scalar_quadrupole_restricted_equation` after radial
    integration by parts.  The nonzero ``g`` entry is the missing tangential
    forcing that makes the profile-only restriction inconsistent.
    """
    radius = _positive("radius", radius)
    metric_factor = _positive("metric_factor", metric_factor)
    profile = _finite("profile", profile)
    profile_derivative = _finite("profile_derivative", profile_derivative)
    sine = sin(profile)
    cosine = cos(profile)
    radius_squared = radius**2
    q_squared_average = 4.0 / 45.0
    tangent_weight = 2.0 / 15.0
    radial_prefactor = (
        radius_squared * sine * (1.0 / (4.0 * metric_factor) + profile_derivative**2)
    )
    routhian_f_derivative = (
        radial_prefactor * cosine + 2.0 * sine**3 * cosine / metric_factor
    )
    routhian_f_prime_derivative = radius_squared * sine**2 * profile_derivative
    radial_field_coefficient = -q_squared_average * routhian_f_derivative
    radial_derivative_coefficient = -(q_squared_average * routhian_f_prime_derivative)
    tangential_field_coefficient = (
        -tangent_weight * radial_prefactor
        + 3.0 * q_squared_average * sine**3 / metric_factor
    )
    return {
        "radial_field_coefficient": radial_field_coefficient,
        "tangential_field_coefficient": tangential_field_coefficient,
        "radial_field_derivative_coefficient": radial_derivative_coefficient,
        "tangential_field_derivative_coefficient": 0.0,
        "variable_order": "(f,g,f',g')",
        "source_density": (
            "s_f f+s_g g+s_fprime f'; multiply by 4pi for the sphere integral"
        ),
        "normalization": ("Q=Omega Omega-delta/3, Omega^2=1, <q^2>=4/45"),
    }


def pure_tension_wall_shape_balance(
    *,
    wall_radius: float,
    curvature: float,
    ell: int,
    membrane_tension: float,
    background_pressure_radial_derivative: float,
    intrinsic_pressure_multipole: float,
    wall_displacement_coefficient: float,
) -> dict[str, float | bool | str]:
    """Audit the linearized Young--Laplace equation for one shape harmonic.

    The pressure evaluated on the displaced shell is

    ``delta p=p_intrinsic+p_0' xi``.

    A constant-tension membrane supplies ``sigma delta K``.  This is only the
    fixed-background normal-force equation; gravitational junction terms and
    any independent surface elastic stresses are outside its scope.
    """
    membrane_tension = _positive("membrane_tension", membrane_tension)
    pressure_derivative = _finite(
        "background_pressure_radial_derivative",
        background_pressure_radial_derivative,
    )
    intrinsic_pressure = _finite(
        "intrinsic_pressure_multipole", intrinsic_pressure_multipole
    )
    displacement = _finite(
        "wall_displacement_coefficient", wall_displacement_coefficient
    )
    curvature_record = static_patch_shell_shape_curvature_coefficient(
        wall_radius=wall_radius,
        curvature=curvature,
        ell=ell,
    )
    shape_coefficient = float(curvature_record["shape_curvature_coefficient"])
    balance_denominator = pressure_derivative - membrane_tension * shape_coefficient
    residual = intrinsic_pressure + balance_denominator * displacement
    required_displacement = (
        -intrinsic_pressure / balance_denominator
        if balance_denominator != 0.0
        else None
    )
    return {
        **curvature_record,
        "membrane_tension": membrane_tension,
        "background_pressure_radial_derivative": pressure_derivative,
        "intrinsic_pressure_multipole": intrinsic_pressure,
        "wall_displacement_coefficient": displacement,
        "shape_balance_denominator": balance_denominator,
        "normal_force_residual": residual,
        "normal_force_is_balanced": abs(residual) <= 1.0e-12,
        "required_wall_displacement_coefficient": required_displacement,
        "scope": (
            "linear fixed-background pure-tension Young-Laplace equation; "
            "no Israel junction or surface elasticity"
        ),
    }


def comoving_pure_tension_quadrupole_boundary(
    *,
    wall_radius: float,
    curvature: float,
    membrane_tension: float,
    wall_profile_derivative: float,
    function_a_minus_c_at_wall: float,
    derivative_of_a_minus_c_at_wall: float,
) -> dict[str, float | bool | str]:
    """Return the coupled ideal-mirror and pure-tension ``ell=2`` wall gate.

    Let ``D=A-C``.  The mirror pullback fixes the shape coefficient
    ``xi2=a^3 D``.  Evaluating the matter traction on that displaced surface
    cancels all ``F''`` terms and gives an exact Robin condition for ``D``.
    """
    wall_radius = _positive("wall_radius", wall_radius)
    curvature = _finite("curvature", curvature)
    if curvature < 0.0:
        raise ValueError("curvature must be nonnegative")
    membrane_tension = _positive("membrane_tension", membrane_tension)
    wall_profile_derivative = _finite(
        "wall_profile_derivative", wall_profile_derivative
    )
    if wall_profile_derivative == 0.0:
        raise ValueError("wall_profile_derivative must be nonzero")
    difference = _finite("function_a_minus_c_at_wall", function_a_minus_c_at_wall)
    difference_derivative = _finite(
        "derivative_of_a_minus_c_at_wall",
        derivative_of_a_minus_c_at_wall,
    )
    lapse = 1.0 - curvature * wall_radius**2
    if lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    lapse_derivative = -2.0 * curvature * wall_radius
    curvature_record = static_patch_shell_shape_curvature_coefficient(
        wall_radius=wall_radius,
        curvature=curvature,
        ell=2,
    )
    shape_coefficient = float(curvature_record["shape_curvature_coefficient"])
    displacement = wall_radius**3 * difference
    profile_slope_squared = wall_profile_derivative**2
    matter_pressure = (
        -lapse * profile_slope_squared * wall_radius**3 * difference_derivative / 4.0
        + profile_slope_squared
        * (lapse_derivative / 8.0 - 3.0 * lapse / (4.0 * wall_radius))
        * displacement
    )
    membrane_pressure = membrane_tension * shape_coefficient * displacement
    residual = matter_pressure - membrane_pressure
    robin_multiplier = (
        lapse_derivative / (2.0 * lapse)
        - 3.0 / wall_radius
        - 4.0 * membrane_tension * shape_coefficient / (lapse * profile_slope_squared)
    )
    required_difference_derivative = robin_multiplier * difference
    return {
        **curvature_record,
        "function_a_minus_c_at_wall": difference,
        "derivative_of_a_minus_c_at_wall": difference_derivative,
        "mirror_required_wall_quadrupole_displacement": displacement,
        "matter_quadrupole_pressure_on_moving_wall": matter_pressure,
        "membrane_quadrupole_curvature_pressure": membrane_pressure,
        "normal_force_residual": residual,
        "normal_force_is_balanced": abs(residual) <= 1.0e-12,
        "robin_multiplier": robin_multiplier,
        "required_derivative_of_a_minus_c_at_wall": (required_difference_derivative),
        "robin_condition": ("D'(a)=[N'/(2N)-3/a-4 sigma k2/(N F_w'^2)]D(a)"),
        "tangential_boundary_condition": (
            "The physical tangential field g must vanish at the ideal mirror; "
            "this is automatic for finite C because g=sin(F)a^2 C."
        ),
        "scope": (
            "linear fixed-background ideal mirror plus pure tension; no "
            "surface elasticity, exterior pressure, or Israel junction"
        ),
    }


def centrifugal_deformation_kinematics_certificate() -> dict[str, object]:
    """Audit multipole rank, mirror pullback, and fixed-wall traction."""
    sample = equivariant_deformation_multipoles(
        radius=2.0,
        function_a=3.0,
        function_b=0.5,
        function_c=1.0,
    )
    direct_axis = direct_vector_deformation_invariants(
        radius=2.0,
        omega_squared=4.0,
        omega_dot_direction=2.0,
        function_a=3.0,
        function_b=0.5,
        function_c=1.0,
    )
    fixed_wall = ideal_mirror_pullback_residuals(
        wall_radius=4.0,
        function_a_at_wall=0.0125,
        function_b_at_wall=0.0,
        function_c_at_wall=0.0125,
    )
    comoving = required_comoving_wall_displacement(
        wall_radius=4.0,
        function_a_at_wall=0.015,
        function_b_at_wall=0.005,
        function_c_at_wall=0.005,
    )
    traction = fixed_spherical_wall_quadrupole_traction(
        wall_radius=4.0,
        wall_metric_factor=0.96,
        wall_profile_derivative=-0.0878757998,
        derivative_of_a_minus_c_at_wall=0.2,
    )
    pressure_derivative = hard_wall_background_pressure_derivative(
        wall_radius=4.0,
        curvature=0.0025,
        wall_profile_derivative=-0.0878757998,
    )
    trial_wall_balance = pure_tension_wall_shape_balance(
        wall_radius=4.0,
        curvature=0.0025,
        ell=2,
        membrane_tension=0.001931779647,
        background_pressure_radial_derivative=float(
            pressure_derivative["background_pressure_radial_derivative"]
        ),
        intrinsic_pressure_multipole=0.0001,
        wall_displacement_coefficient=0.0,
    )
    balanced_wall = pure_tension_wall_shape_balance(
        wall_radius=4.0,
        curvature=0.0025,
        ell=2,
        membrane_tension=0.001931779647,
        background_pressure_radial_derivative=float(
            pressure_derivative["background_pressure_radial_derivative"]
        ),
        intrinsic_pressure_multipole=0.0001,
        wall_displacement_coefficient=float(
            trial_wall_balance["required_wall_displacement_coefficient"]
        ),
    )
    coupled_trial = comoving_pure_tension_quadrupole_boundary(
        wall_radius=4.0,
        curvature=0.0025,
        membrane_tension=0.001931779647,
        wall_profile_derivative=-0.0878757998,
        function_a_minus_c_at_wall=0.01,
        derivative_of_a_minus_c_at_wall=0.0,
    )
    coupled_balanced = comoving_pure_tension_quadrupole_boundary(
        wall_radius=4.0,
        curvature=0.0025,
        membrane_tension=0.001931779647,
        wall_profile_derivative=-0.0878757998,
        function_a_minus_c_at_wall=0.01,
        derivative_of_a_minus_c_at_wall=float(
            coupled_trial["required_derivative_of_a_minus_c_at_wall"]
        ),
    )
    scalar_diagnostic = scalar_quadrupole_restricted_equation(
        radius=1.0,
        metric_factor=0.96,
        metric_factor_derivative=-0.005,
        profile=1.0,
        profile_derivative=-0.4,
        profile_second_derivative=0.2,
        pion_mass=1.0,
    )
    coupled_hessian = quadrupole_static_hessian_matrix(
        radius=1.0,
        metric_factor=0.96,
        profile=1.0,
        profile_derivative=-0.4,
        pion_mass=1.0,
    )
    rotational_source = rotational_quadrupole_source_covector(
        radius=1.0,
        metric_factor=0.96,
        profile=1.0,
        profile_derivative=-0.4,
    )
    expected_scalar_principal = 4.0 / 45.0 * 0.96 * (1.0 + 8.0 * sin(1.0) ** 2) / 4.0
    claims = {
        "equivariant_quadrupole_deformation_has_rank_two": (
            sample["quadrupole_response_rank"] == 2
            and sample["quadrupole_coefficient_map_determinant"] != 0.0
        ),
        "axis_radial_displacement_matches_direct_basis": abs(
            float(direct_axis["radial_displacement"]) + 32.0
        )
        <= 1.0e-12,
        "fixed_wall_pullback_conditions_are_sufficient": fixed_wall[
            "ideal_mirror_pullback_is_satisfied"
        ],
        "comoving_wall_cancels_both_pullback_sectors": comoving[
            "pullback_check_passes"
        ],
        "generic_fixed_wall_deformation_needs_quadrupole_reaction": not traction[
            "unanchored_fixed_spherical_wall_is_force_balanced"
        ],
        "pure_tension_shape_has_nonzero_quadrupole_response": (
            trial_wall_balance["shape_curvature_coefficient"] > 0.0
        ),
        "movable_pure_tension_wall_can_balance_sample_traction": balanced_wall[
            "normal_force_is_balanced"
        ],
        "coupled_mirror_tension_robin_condition_balances_sample": (
            coupled_balanced["normal_force_is_balanced"]
        ),
        "scalar_source_matches_rigid_radial_hilbert_defect": abs(
            float(scalar_diagnostic["radial_hilbert_identity_residual"])
        )
        <= 1.0e-12,
        "scalar_restriction_leaves_an_independent_angular_gate": abs(
            float(scalar_diagnostic["rigid_angular_conservation_residual_coefficient"])
        )
        > 1.0e-12,
        "coupled_hessian_is_symmetric": all(
            abs(
                coupled_hessian["symmetric_hessian_matrix"][row][column]
                - coupled_hessian["symmetric_hessian_matrix"][column][row]
            )
            <= 1.0e-12
            for row in range(4)
            for column in range(4)
        ),
        "coupled_hessian_reproduces_scalar_principal_coefficient": abs(
            float(coupled_hessian["radial_field_principal_coefficient"])
            - expected_scalar_principal
        )
        <= 1.0e-12,
        "rotational_source_forces_tangential_channel": abs(
            float(rotational_source["tangential_field_coefficient"])
        )
        > 1.0e-12,
    }
    return {
        "goal": "Centrifugal Skyrmion Deformation And Wall Kinematic Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "rank_two_quadrupole_deformation_and_wall_gate",
        "sample_multipoles": sample,
        "fixed_wall_pullback": fixed_wall,
        "required_comoving_wall": comoving,
        "fixed_wall_traction": traction,
        "hard_wall_background_pressure_derivative": pressure_derivative,
        "pure_tension_wall_shape_balance": balanced_wall,
        "coupled_mirror_tension_boundary": coupled_balanced,
        "scalar_quadrupole_diagnostic": scalar_diagnostic,
        "coupled_static_hessian": coupled_hessian,
        "rotational_source_covector": rotational_source,
        "certified_claims": claims,
        "required_next_step": (
            "Derive and solve the coupled two-channel static-patch ell=2 "
            "deformation equations in regular physical variables (f,g), with "
            "the dynamical wall Robin condition or a declared quadrupole "
            "anchor, then audit full stress conservation."
        ),
        "claim_boundary": (
            "Exact O(Omega^2) equivariant kinematics, scalar radial diagnostic, "
            "and fixed-background ideal-mirror/pure-tension boundary algebra. "
            "No coupled two-channel bulk operator, existence theorem, Israel "
            "junction, or Zerilli source is supplied."
        ),
    }
