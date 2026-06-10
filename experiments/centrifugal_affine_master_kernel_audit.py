"""Write the source-hashed affine and origin-regular master-kernel audit."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import cos, sin, sqrt
from pathlib import Path

from qgtoy.centrifugal_skyrmion_affine_master_kernel import (
    centrifugal_completed_master_source_affine_kernel,
    centrifugal_completed_master_source_generic,
    centrifugal_moving_wall_master_affine_kernel,
)
from qgtoy.centrifugal_skyrmion_origin_master_kernel import (
    centrifugal_completed_master_source_origin_affine_kernel,
    centrifugal_completed_master_source_origin_generic,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/centrifugal_affine_master_kernel_certificate.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_affine_master_kernel.py",
    "qgtoy/centrifugal_skyrmion_origin_master_kernel.py",
    "experiments/centrifugal_affine_master_kernel_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fraction_strings(values: tuple[Fraction, ...]) -> list[str]:
    return [str(value) for value in values]


def build_record() -> dict[str, object]:
    bulk_background = {
        "radius": Fraction(7, 5),
        "metric_factor": Fraction(19, 20),
        "metric_factor_derivative": Fraction(-7, 1000),
        "inverse_patch_radius_squared": Fraction(1, 400),
        "sine_profile": Fraction(3, 5),
        "cosine_profile": Fraction(4, 5),
        "profile_derivative": Fraction(-2, 5),
        "profile_second_derivative": Fraction(1, 7),
        "pion_mass_squared": Fraction(6, 5),
        "gravitational_coupling": Fraction(3, 2),
    }
    bulk_fields = {
        "radial_field": Fraction(2, 13),
        "radial_field_derivative": Fraction(-3, 17),
        "radial_field_second_derivative": Fraction(11, 29),
        "tangential_field": Fraction(5, 19),
        "tangential_field_derivative": Fraction(7, 23),
    }
    bulk_kernel = centrifugal_completed_master_source_affine_kernel(
        **bulk_background
    )
    bulk_direct = centrifugal_completed_master_source_generic(
        **bulk_background, **bulk_fields
    )
    bulk_affine = bulk_kernel.evaluate(**bulk_fields)

    origin_background = {
        "t": Fraction(0),
        "metric_factor": Fraction(1),
        "metric_factor_time_derivative": Fraction(-1, 400),
        "inverse_patch_radius_squared": Fraction(1, 400),
        "profile_deficit_over_radius": Fraction(3, 2),
        "profile_deficit_time_derivative": Fraction(1, 7),
        "profile_deficit_second_time_derivative": Fraction(-1, 11),
        "sine_over_radius": Fraction(3, 2),
        # s_t(0)=w_t(0)-w(0)^3/6 for s=sin(sqrt(t)w)/sqrt(t).
        "sine_over_radius_time_derivative": Fraction(-47, 112),
        "cosine_of_profile_deficit": Fraction(1),
        "pion_mass_squared": Fraction(1),
        "gravitational_coupling": Fraction(3, 2),
    }
    origin_fields = {
        "u": Fraction(2, 5),
        "u_time_derivative": Fraction(-1, 9),
        "u_second_time_derivative": Fraction(1, 13),
        "v": Fraction(-3, 7),
        "v_time_derivative": Fraction(2, 11),
        "v_second_time_derivative": Fraction(-1, 17),
    }
    origin_kernel = centrifugal_completed_master_source_origin_affine_kernel(
        **origin_background
    )
    origin_direct = centrifugal_completed_master_source_origin_generic(
        **origin_background, **origin_fields
    )
    origin_affine = origin_kernel.evaluate(**origin_fields)

    wall_kernel = centrifugal_moving_wall_master_affine_kernel(
        wall_radius=Fraction(3),
        wall_metric_factor=Fraction(16, 25),
        wall_metric_factor_derivative=Fraction(-6, 25),
        sqrt_wall_metric_factor=Fraction(4, 5),
        inverse_patch_radius_squared=Fraction(1, 25),
        sine_profile=Fraction(3, 5),
        cosine_profile=Fraction(4, 5),
        profile_derivative=Fraction(-2, 5),
        pion_mass_squared=Fraction(6, 5),
        membrane_tension=Fraction(7, 13),
        wall_displacement_per_radial_field=Fraction(5, 2),
        wall_green_weight=Fraction(11, 17),
        wall_green_weight_derivative=Fraction(-7, 19),
        gravitational_coupling=Fraction(3, 2),
    )

    t = 0.4
    x = sqrt(t)
    curvature = 1.0 / 400.0
    w = 1.3 + 0.2 * t - 0.07 * t**2
    w_t = 0.2 - 0.14 * t
    w_tt = -0.14
    p = w + 2.0 * t * w_t
    p_t = 3.0 * w_t + 2.0 * t * w_tt
    argument = x * w
    s = sin(argument) / x
    s_t = (cos(argument) * p - s) / (2.0 * t)
    u, u_t, u_tt = 0.31, -0.08, 0.04
    v, v_t, v_tt = -0.27, 0.06, -0.03
    a = -v + t * u
    a_t = -v_t + u + t * u_t
    fp = a + 2.0 * t * a_t
    fp_t = 3.0 * u - 3.0 * v_t + 7.0 * t * u_t - 2.0 * t * v_tt + 2.0 * t**2 * u_tt
    gp = v + 2.0 * t * v_t
    positive_direct = centrifugal_completed_master_source_generic(
        radius=x,
        metric_factor=1.0 - curvature * t,
        metric_factor_derivative=-2.0 * curvature * x,
        inverse_patch_radius_squared=curvature,
        sine_profile=x * s,
        cosine_profile=-cos(argument),
        profile_derivative=-p,
        profile_second_derivative=-2.0 * x * p_t,
        radial_field=x * a,
        radial_field_derivative=fp,
        radial_field_second_derivative=2.0 * x * fp_t,
        tangential_field=x * v,
        tangential_field_derivative=gp,
        pion_mass_squared=1.0,
        gravitational_coupling=1.7,
    )
    positive_regular = centrifugal_completed_master_source_origin_generic(
        t=t,
        metric_factor=1.0 - curvature * t,
        metric_factor_time_derivative=-curvature,
        inverse_patch_radius_squared=curvature,
        profile_deficit_over_radius=w,
        profile_deficit_time_derivative=w_t,
        profile_deficit_second_time_derivative=w_tt,
        sine_over_radius=s,
        sine_over_radius_time_derivative=s_t,
        cosine_of_profile_deficit=cos(argument),
        u=u,
        u_time_derivative=u_t,
        u_second_time_derivative=u_tt,
        v=v,
        v_time_derivative=v_t,
        v_second_time_derivative=v_tt,
        pion_mass_squared=1.0,
        gravitational_coupling=1.7,
    )
    factorization_error = abs(positive_direct - x * positive_regular)
    claims = {
        "bulk_affine_reconstruction_is_exact_rational": bulk_affine == bulk_direct,
        "origin_affine_reconstruction_is_exact_rational": origin_affine
        == origin_direct,
        "origin_center_evaluation_is_exact_fraction": isinstance(
            origin_direct, Fraction
        ),
        "effective_wall_endpoint_cancellation_is_exact": all(
            value == 0
            for value in (
                wall_kernel.rigid.effective_wall_amplitude,
                wall_kernel.radial_field_derivative.effective_wall_amplitude,
                wall_kernel.tangential_field.effective_wall_amplitude,
                wall_kernel.tangential_field_derivative.effective_wall_amplitude,
            )
        ),
        "wall_displacement_and_response_traces_are_distinct": (
            wall_kernel.response_wall_trace_gamma_b
            != wall_kernel.wall_displacement_per_radial_field
        ),
        "positive_radius_origin_factorization_closes": factorization_error
        < 1.0e-12,
    }
    return {
        "goal": "Affine Completed-Stress And Origin-Regular Master Kernel",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_affine_local_algebra_and_origin_factorization",
        "certified_claims": claims,
        "bulk_master_coefficients": _fraction_strings(
            (
                bulk_kernel.rigid,
                bulk_kernel.radial_field,
                bulk_kernel.radial_field_derivative,
                bulk_kernel.radial_field_second_derivative,
                bulk_kernel.tangential_field,
                bulk_kernel.tangential_field_derivative,
            )
        ),
        "origin_center_master_coefficients": _fraction_strings(
            (
                origin_kernel.rigid,
                origin_kernel.u,
                origin_kernel.u_time_derivative,
                origin_kernel.u_second_time_derivative,
                origin_kernel.v,
                origin_kernel.v_time_derivative,
                origin_kernel.v_second_time_derivative,
            )
        ),
        "wall_displacement_per_radial_field": str(
            wall_kernel.wall_displacement_per_radial_field
        ),
        "response_wall_trace_gamma_b": str(
            wall_kernel.response_wall_trace_gamma_b
        ),
        "positive_radius_factorization_error": factorization_error,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies local affine algebra and center regularity only. "
            "It does not enclose continuum primal/adjoint fields, wall terms, "
            "integrals, residual norms, or a nonzero exterior amplitude."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
