"""Obstructions to an energy-density-only Einstein response bound.

Two independent facts constrain any proposed nonspherical backreaction norm.

* On an Einstein background, a compactly supported pure-gauge perturbation
  ``h=L_xi g`` has zero linearized Einstein source but arbitrarily large
  coordinate-component norm.
* In the local flat limit, a compact scalar potential ``chi`` generates the
  conserved static stress

      T_00=0,
      T_ij=A(delta_ij Delta-partial_i partial_j)chi.

  Its energy density vanishes, but its trace and gauge-invariant linearized
  scalar curvature are generally nonzero and scale freely with ``A``.

Thus a valid response theorem must fix/quotient gauge and control a norm of the
full conserved stress tensor, not only its energy-density multipole.
"""

from __future__ import annotations

from math import isfinite, pi


def _validate_finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _validate_positive(name: str, value: float) -> None:
    _validate_finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


def pure_gauge_metric_norm_no_go_record(
    gauge_amplitude: float,
) -> dict[str, float | bool | str]:
    """Record the exact zero-source scaling of a pure-gauge perturbation."""
    _validate_finite("gauge_amplitude", gauge_amplitude)
    amplitude = abs(gauge_amplitude)
    return {
        "compact_vector_field_amplitude": amplitude,
        "linearized_einstein_source_norm": 0.0,
        "coordinate_metric_component_scale": amplitude,
        "arbitrarily_scalable_at_zero_source": amplitude > 0.0,
        "identity": (
            "On an Einstein background, h=L_xi g lies in the kernel of the "
            "linearized Einstein operator by diffeomorphism covariance."
        ),
        "consequence": (
            "No coordinate-component metric norm can satisfy a source-response "
            "bound before a gauge is fixed or pure gauges are quotiented."
        ),
    }


def density_only_curvature_counterexample_record(
    *,
    stress_amplitude: float,
    potential_laplacian: float,
    newton_constant: float,
) -> dict[str, float | bool | str]:
    """Evaluate the compact-potential stress counterexample at one point.

    For any smooth compactly supported ``chi`` in the flat local limit, set
    ``T_ij=A(delta_ij Delta-partial_i partial_j)chi`` and all time components
    to zero. Commuting derivatives proves conservation. The trace is
    ``T=2 A Delta chi`` and the traced linearized Einstein equation gives
    ``R^(1)=-8 pi G T``.
    """
    _validate_finite("stress_amplitude", stress_amplitude)
    _validate_finite("potential_laplacian", potential_laplacian)
    _validate_positive("newton_constant", newton_constant)
    stress_trace = 2.0 * stress_amplitude * potential_laplacian
    scalar_curvature = -8.0 * pi * newton_constant * stress_trace
    return {
        "stress_amplitude": stress_amplitude,
        "potential_laplacian": potential_laplacian,
        "energy_density_T00": 0.0,
        "energy_density_norm": 0.0,
        "spatial_stress_trace": stress_trace,
        "linearized_scalar_curvature": scalar_curvature,
        "four_divergence_vanishes": True,
        "divergence_identity": (
            "partial_i[(delta_ij Delta-partial_i partial_j)chi]="
            "partial_j Delta chi-Delta partial_j chi=0"
        ),
        "nonzero_curvature_at_zero_energy_density": (
            stress_trace != 0.0 and scalar_curvature != 0.0
        ),
        "quadrupole_choice": (
            "Choosing chi=f(r)Y_2m with a smooth compact radial bump makes "
            "the trace and curvature response purely l=2."
        ),
    }


def density_only_einstein_response_no_go_certificate() -> dict[str, object]:
    """Audit the gauge and stress-completeness obstructions."""
    gauge = pure_gauge_metric_norm_no_go_record(10.0)
    stress = density_only_curvature_counterexample_record(
        stress_amplitude=3.0,
        potential_laplacian=2.0,
        newton_constant=1.0,
    )
    doubled = density_only_curvature_counterexample_record(
        stress_amplitude=6.0,
        potential_laplacian=2.0,
        newton_constant=1.0,
    )
    claims = {
        "gauge_dependent_metric_norm_has_zero_source_counterexample": gauge[
            "arbitrarily_scalable_at_zero_source"
        ],
        "density_only_bound_has_conserved_stress_counterexample": stress[
            "nonzero_curvature_at_zero_energy_density"
        ],
        "curvature_response_scales_independently_of_density": abs(
            doubled["linearized_scalar_curvature"]
            - 2.0 * stress["linearized_scalar_curvature"]
        )
        < 1.0e-12,
    }
    return {
        "goal": "Well-Posed Nonspherical Einstein Response Inputs",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "gauge_and_density_only_response_no_go",
        "pure_gauge_counterexample": gauge,
        "density_only_counterexample": stress,
        "certified_claims": claims,
        "required_replacement": (
            "Choose a gauge-invariant output or a fully fixed gauge, impose "
            "linearized stress conservation, and bound density, radial and "
            "tangential pressure, momentum, and shear in a response-compatible "
            "source norm."
        ),
        "claim_boundary": (
            "The density-only counterexample is exact in the local Minkowski "
            "limit and therefore rules out a bound claimed uniformly as the "
            "worldtube size over de Sitter radius tends to zero. It is not the "
            "static-patch l=2 Green function and does not prove that the full "
            "Skyrmion stress lacks a finite response bound."
        ),
    }
