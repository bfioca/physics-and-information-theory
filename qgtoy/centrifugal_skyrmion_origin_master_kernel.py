"""Origin-regular affine bulk master-source kernel.

For the regular variables

``t=x^2``, ``F=pi-x w(t)``, ``g=x v(t)``, and
``f=x[-v(t)+t u(t)]``, the completed stress-to-master map factorizes as

``F_master(x)=x F_hat(t)``.

This module evaluates ``F_hat`` without dividing by ``x`` or ``t``.  The
caller supplies the entire profile kernel ``s(t)=sin(x w(t))/x`` and its time
derivative.  Consequently the same formulas remain meaningful at ``t=0`` and
under exact rational, interval, or Taylor-model arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .centrifugal_skyrmion_affine_master_kernel import (
    _AffineScalar,
    _FirstRadialJet,
)


Scalar = TypeVar("Scalar")


@dataclass(frozen=True)
class OriginRegularStress(Generic[Scalar]):
    """Stress data needed by ``F_master/x`` in regular origin variables."""

    energy_density: Scalar
    radial_pressure: Scalar
    tangential_pressure: Scalar
    radial_angular_shear_over_radius: Scalar
    angular_tracefree_stress: Scalar


def _origin_regular_completed_stress(
    *,
    t: Scalar,
    metric_factor: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
    profile_deficit_radial_derivative: Scalar,
    radial_field_over_radius: Scalar,
    radial_field_derivative: Scalar,
    tangential_field_over_radius: Scalar,
    tangential_field_derivative: Scalar,
    pion_mass_squared: Scalar,
) -> OriginRegularStress[Scalar]:
    """Evaluate the completed stress after all origin cancellations."""
    sine_squared = sine_over_radius * sine_over_radius  # type: ignore[operator]
    profile_derivative_squared = (  # type: ignore[operator]
        profile_deficit_radial_derivative * profile_deficit_radial_derivative
    )
    radial_strain = metric_factor * profile_derivative_squared  # type: ignore[operator]
    tangential_strain = sine_squared
    sigma_rotation = t * sine_squared / (metric_factor * 8)  # type: ignore[operator]
    skyrme_rotation = t * sine_squared / (metric_factor * 2)  # type: ignore[operator]
    zero = t - t  # type: ignore[operator]
    quarter = (zero + 1) / 4  # type: ignore[operator]

    rigid_energy = -(  # type: ignore[operator]
        sigma_rotation
        + skyrme_rotation * (radial_strain + tangential_strain)
    )
    rigid_radial = -(  # type: ignore[operator]
        sigma_rotation
        + skyrme_rotation * (tangential_strain - radial_strain)
    )
    rigid_tangential = -(  # type: ignore[operator]
        sigma_rotation + skyrme_rotation * radial_strain
    )
    rigid_tracefree = -(skyrme_rotation * tangential_strain)  # type: ignore[operator]

    a = radial_field_over_radius
    v = tangential_field_over_radius
    c = cosine_of_profile_deficit
    p = profile_deficit_radial_derivative
    fp = radial_field_derivative
    gp = tangential_field_derivative
    radial_strain_variation = -(metric_factor * p * fp * 2)  # type: ignore[operator]
    angular_isotropic_variation = sine_over_radius * (  # type: ignore[operator]
        -(a * c * 2) - v * 3
    )
    angular_trace_variation = angular_isotropic_variation * 2  # type: ignore[operator]
    total_trace_variation = (  # type: ignore[operator]
        radial_strain_variation + angular_trace_variation
    )
    deformation_energy = (  # type: ignore[operator]
        total_trace_variation / 8
        + tangential_strain * radial_strain_variation
        + (radial_strain + tangential_strain) * angular_trace_variation / 2
        + pion_mass_squared * t * a * sine_over_radius / 4
    )
    deformation_radial = (  # type: ignore[operator]
        radial_strain_variation
        * (quarter - radial_strain + tangential_strain * 2)
        + radial_strain * total_trace_variation
        - deformation_energy
    )
    deformation_tangential = (  # type: ignore[operator]
        (quarter + radial_strain) * angular_isotropic_variation
        + tangential_strain * total_trace_variation
        - deformation_energy
    )
    deformation_tracefree = (  # type: ignore[operator]
        (quarter + radial_strain) * sine_over_radius * v
    )
    shear_regular = (  # type: ignore[operator]
        metric_factor
        * (
            sine_over_radius * gp
            - p * (a * 2 + c * v)  # type: ignore[operator]
        )
        * (quarter + tangential_strain)
        / 2
    )
    return OriginRegularStress(
        rigid_energy + deformation_energy,  # type: ignore[operator]
        rigid_radial + deformation_radial,  # type: ignore[operator]
        rigid_tangential + deformation_tangential,  # type: ignore[operator]
        shear_regular,
        rigid_tracefree + deformation_tracefree,  # type: ignore[operator]
    )


def centrifugal_completed_master_source_origin_generic(
    *,
    t: Scalar,
    metric_factor: Scalar,
    metric_factor_time_derivative: Scalar,
    inverse_patch_radius_squared: Scalar,
    profile_deficit_over_radius: Scalar,
    profile_deficit_time_derivative: Scalar,
    profile_deficit_second_time_derivative: Scalar,
    sine_over_radius: Scalar,
    sine_over_radius_time_derivative: Scalar,
    cosine_of_profile_deficit: Scalar,
    u: Scalar,
    u_time_derivative: Scalar,
    u_second_time_derivative: Scalar,
    v: Scalar,
    v_time_derivative: Scalar,
    v_second_time_derivative: Scalar,
    pion_mass_squared: Scalar,
    gravitational_coupling: Scalar,
) -> Scalar:
    """Return the regular factor ``F_hat=F_master/x`` at ``t>=0``.

    No ordering checks are performed so validated scalar types can use the
    same algebra.  ``metric_factor_time_derivative`` is normally ``-1/R^2``.
    """
    zero = t - t  # type: ignore[operator]
    one = zero + 1  # type: ignore[operator]
    w = profile_deficit_over_radius
    w_t = profile_deficit_time_derivative
    w_tt = profile_deficit_second_time_derivative
    u_t = u_time_derivative
    u_tt = u_second_time_derivative
    v_t = v_time_derivative
    v_tt = v_second_time_derivative
    p = w + t * w_t * 2  # type: ignore[operator]
    p_t = w_t * 3 + t * w_tt * 2  # type: ignore[operator]
    a = -v + t * u  # type: ignore[operator]
    a_t = -v_t + u + t * u_t  # type: ignore[operator]
    fp = a + t * a_t * 2  # type: ignore[operator]
    fp_t = (  # type: ignore[operator]
        u * 3
        - v_t * 3
        + t * u_t * 7
        - t * v_tt * 2
        + t * t * u_tt * 2
    )
    gp = v + t * v_t * 2  # type: ignore[operator]
    gp_t = v_t * 3 + t * v_tt * 2  # type: ignore[operator]
    c_t = -(sine_over_radius * p) / 2  # type: ignore[operator]

    stress = _origin_regular_completed_stress(
        t=_FirstRadialJet(t, one),
        metric_factor=_FirstRadialJet(
            metric_factor, metric_factor_time_derivative
        ),
        sine_over_radius=_FirstRadialJet(
            sine_over_radius, sine_over_radius_time_derivative
        ),
        cosine_of_profile_deficit=_FirstRadialJet(
            cosine_of_profile_deficit, c_t
        ),
        profile_deficit_radial_derivative=_FirstRadialJet(p, p_t),
        radial_field_over_radius=_FirstRadialJet(a, a_t),
        radial_field_derivative=_FirstRadialJet(fp, fp_t),
        tangential_field_over_radius=_FirstRadialJet(v, v_t),
        tangential_field_derivative=_FirstRadialJet(gp, gp_t),
        pion_mass_squared=_FirstRadialJet.constant(pion_mass_squared),
    )
    energy = stress.energy_density
    return gravitational_coupling * (  # type: ignore[operator, return-value]
        -(t * metric_factor * energy.derivative) / 3
        + (one + t * inverse_patch_radius_squared * 4) * energy.value / 6
        - stress.radial_pressure.value / 2
        - stress.radial_angular_shear_over_radius.value
        + stress.angular_tracefree_stress.value * 2
    )


@dataclass(frozen=True)
class AffineOriginMasterSourceKernel(Generic[Scalar]):
    """Affine coefficients of the regular factor in ``(u,u_t,u_tt,v,v_t,v_tt)``."""

    rigid: Scalar
    u: Scalar
    u_time_derivative: Scalar
    u_second_time_derivative: Scalar
    v: Scalar
    v_time_derivative: Scalar
    v_second_time_derivative: Scalar

    def evaluate(
        self,
        *,
        u: Scalar,
        u_time_derivative: Scalar,
        u_second_time_derivative: Scalar,
        v: Scalar,
        v_time_derivative: Scalar,
        v_second_time_derivative: Scalar,
    ) -> Scalar:
        return (  # type: ignore[return-value]
            self.rigid
            + self.u * u  # type: ignore[operator]
            + self.u_time_derivative * u_time_derivative
            + self.u_second_time_derivative * u_second_time_derivative
            + self.v * v
            + self.v_time_derivative * v_time_derivative
            + self.v_second_time_derivative * v_second_time_derivative
        )


def centrifugal_completed_master_source_origin_affine_kernel(
    *,
    t: Scalar,
    metric_factor: Scalar,
    metric_factor_time_derivative: Scalar,
    inverse_patch_radius_squared: Scalar,
    profile_deficit_over_radius: Scalar,
    profile_deficit_time_derivative: Scalar,
    profile_deficit_second_time_derivative: Scalar,
    sine_over_radius: Scalar,
    sine_over_radius_time_derivative: Scalar,
    cosine_of_profile_deficit: Scalar,
    pion_mass_squared: Scalar,
    gravitational_coupling: Scalar,
) -> AffineOriginMasterSourceKernel[Scalar]:
    """Extract the six-field affine origin kernel without basis differencing."""
    dimension = 6
    lift = lambda value: _AffineScalar.lifted(value, dimension)  # noqa: E731
    fields = tuple(_AffineScalar.basis(t, dimension, index) for index in range(6))
    result = centrifugal_completed_master_source_origin_generic(
        t=lift(t),
        metric_factor=lift(metric_factor),
        metric_factor_time_derivative=lift(metric_factor_time_derivative),
        inverse_patch_radius_squared=lift(inverse_patch_radius_squared),
        profile_deficit_over_radius=lift(profile_deficit_over_radius),
        profile_deficit_time_derivative=lift(profile_deficit_time_derivative),
        profile_deficit_second_time_derivative=lift(
            profile_deficit_second_time_derivative
        ),
        sine_over_radius=lift(sine_over_radius),
        sine_over_radius_time_derivative=lift(
            sine_over_radius_time_derivative
        ),
        cosine_of_profile_deficit=lift(cosine_of_profile_deficit),
        u=fields[0],
        u_time_derivative=fields[1],
        u_second_time_derivative=fields[2],
        v=fields[3],
        v_time_derivative=fields[4],
        v_second_time_derivative=fields[5],
        pion_mass_squared=lift(pion_mass_squared),
        gravitational_coupling=lift(gravitational_coupling),
    )
    return AffineOriginMasterSourceKernel(result.constant, *result.coefficients)
