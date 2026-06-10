"""Norm-honest finite-time matter-to-observer recovery transfers.

Two logically different perturbation results are kept separate here.

* A normalized diamond-distance estimate from a physical channel to the
  collective ``SO(3)`` heat channel transfers both any-decoder lower bounds
  and explicit-decoder upper bounds.
* The available ULE theorem controls an ancilla-stable state residual in
  operator norm.  It transfers only through the fixed Choi fidelity witness,
  with the explicit dimension cost already identified in the overlapping-
  sector calculation.  It is not promoted to a diamond-distance estimate.

The distinction is encoded in separate immutable bound types so that the two
proof routes cannot be silently interchanged by callers.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log, pi

from .finite_size_static_patch_observer import (
    energy_constrained_rotor_recovery_bound_record,
)
from .finite_time_rotation_diffusion import finite_time_twirl_distance_record
from .redshifted_rotation_reference_tradeoff import (
    peter_weyl_constructive_diamond_upper_bound,
)
from .static_patch_finite_switching_ule import (
    ancilla_stable_finite_switch_ule_residual_bound,
)


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_unit_interval(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError(f"{name} must lie in the closed unit interval")


def _validate_spin(spin: int) -> None:
    if isinstance(spin, bool) or not isinstance(spin, int) or spin < 1:
        raise ValueError("spin must be a positive integer")


def _validate_provenance(provenance: str) -> None:
    if not isinstance(provenance, str) or not provenance.strip():
        raise ValueError("provenance must be a nonempty string")


@dataclass(frozen=True)
class NormalizedDiamondDistanceBound:
    """Upper bound on one half of a channel diamond distance."""

    value: float
    provenance: str

    def __post_init__(self) -> None:
        _validate_unit_interval("normalized diamond-distance bound", self.value)
        _validate_provenance(self.provenance)


@dataclass(frozen=True)
class AncillaStableOperatorNormResidual:
    """Ancilla-stable operator-norm residual for one evolved state."""

    value: float
    provenance: str

    def __post_init__(self) -> None:
        _validate_nonnegative("operator-norm residual bound", self.value)
        _validate_provenance(self.provenance)


def _require_diamond_bound(
    name: str,
    bound: NormalizedDiamondDistanceBound,
) -> NormalizedDiamondDistanceBound:
    if not isinstance(bound, NormalizedDiamondDistanceBound):
        raise TypeError(f"{name} must be a NormalizedDiamondDistanceBound")
    return bound


def _require_operator_residual(
    residual: AncillaStableOperatorNormResidual,
) -> AncillaStableOperatorNormResidual:
    if not isinstance(residual, AncillaStableOperatorNormResidual):
        raise TypeError(
            "spectral_residual must be an AncillaStableOperatorNormResidual"
        )
    return residual


def _diamond_bound_record(
    bound: NormalizedDiamondDistanceBound,
) -> dict[str, object]:
    return {
        "value": bound.value,
        "norm_kind": "normalized_diamond_distance",
        "provenance": bound.provenance,
    }


def _operator_residual_record(
    residual: AncillaStableOperatorNormResidual,
) -> dict[str, object]:
    return {
        "value": residual.value,
        "norm_kind": "ancilla_stable_state_operator_norm",
        "provenance": residual.provenance,
    }


def recovery_error_transfer_bracket(
    *,
    haar_any_decoder_lower_bound: float,
    haar_constructive_decoder_upper_bound: float,
    heat_to_haar_bound: NormalizedDiamondDistanceBound,
    physical_to_heat_bound: NormalizedDiamondDistanceBound,
) -> dict[str, object]:
    """Transfer lower and upper recovery bounds through diamond perturbations.

    For normalized recovery error

    ``e(N)=inf_D 0.5 ||D N-id||_diamond``, decoder contractivity and the
    triangle inequality make ``e`` one-Lipschitz in normalized diamond
    distance.  The upper bound applies to the declared constructive decoder;
    both Haar bounds must therefore refer to the same reference preparation
    when the returned pair is interpreted as a literal bracket.
    """
    _validate_unit_interval(
        "haar_any_decoder_lower_bound", haar_any_decoder_lower_bound
    )
    _validate_unit_interval(
        "haar_constructive_decoder_upper_bound",
        haar_constructive_decoder_upper_bound,
    )
    if haar_any_decoder_lower_bound > haar_constructive_decoder_upper_bound:
        raise ValueError("the declared Haar lower bound exceeds the upper bound")
    heat = _require_diamond_bound("heat_to_haar_bound", heat_to_haar_bound)
    local = _require_diamond_bound(
        "physical_to_heat_bound",
        physical_to_heat_bound,
    )
    correction = heat.value + local.value
    return {
        "haar_any_decoder_error_lower_bound": haar_any_decoder_lower_bound,
        "haar_constructive_decoder_error_upper_bound": (
            haar_constructive_decoder_upper_bound
        ),
        "heat_to_haar_bound": _diamond_bound_record(heat),
        "physical_to_heat_bound": _diamond_bound_record(local),
        "total_normalized_diamond_correction": correction,
        "physical_any_decoder_error_lower_bound": max(
            0.0, haar_any_decoder_lower_bound - correction
        ),
        "physical_constructive_decoder_error_upper_bound": min(
            1.0, haar_constructive_decoder_upper_bound + correction
        ),
        "lower_transfer_formula": "max(0,e_Haar_lower-eta_heat-eta_local)",
        "upper_transfer_formula": "min(1,e_Haar_upper+eta_heat+eta_local)",
        "norm_requirement": (
            "both perturbations are certified normalized diamond distances"
        ),
    }


def finite_time_peter_weyl_recovery_transfer_record(
    system_spin: int,
    reference_cutoff: int,
    *,
    maximum_mean_casimir: float,
    proper_time: float,
    diffusion_rate: float,
    physical_to_heat_bound: NormalizedDiamondDistanceBound,
) -> dict[str, object]:
    """Report finite-time obstruction and constructive branches.

    The obstruction is uniform over all reference states satisfying the mean-
    Casimir budget.  The constructive branch uses the canonical Peter-Weyl
    token through ``reference_cutoff``.  They are displayed together for a
    resource comparison but are not a single-resource bracket unless that
    canonical token is separately shown to obey the declared mean-Casimir
    budget.
    """
    _validate_spin(system_spin)
    _validate_nonnegative("maximum_mean_casimir", maximum_mean_casimir)
    _validate_nonnegative("proper_time", proper_time)
    _validate_positive("diffusion_rate", diffusion_rate)
    local = _require_diamond_bound(
        "physical_to_heat_bound",
        physical_to_heat_bound,
    )
    heat_record = finite_time_twirl_distance_record(
        proper_time,
        diffusion_rate=diffusion_rate,
    )
    heat = NormalizedDiamondDistanceBound(
        heat_record["normalized_diamond_distance_to_haar_upper_bound"],
        "SO(3) heat-kernel L2-to-diamond estimate",
    )
    correction = heat.value + local.value
    haar_obstruction = energy_constrained_rotor_recovery_bound_record(
        system_spin,
        maximum_mean_casimir=maximum_mean_casimir,
    )
    haar_constructive = peter_weyl_constructive_diamond_upper_bound(
        system_spin,
        reference_cutoff,
    )
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": 2 * system_spin + 1,
        "proper_time_T": proper_time,
        "diffusion_rate_gamma": diffusion_rate,
        "heat_to_haar_bound": _diamond_bound_record(heat),
        "physical_to_heat_bound": _diamond_bound_record(local),
        "total_normalized_diamond_correction": correction,
        "energy_constrained_obstruction_branch": {
            "maximum_mean_left_casimir": maximum_mean_casimir,
            "haar_any_decoder_error_lower_bound": haar_obstruction[
                "normalized_diamond_error_lower_bound"
            ],
            "physical_any_decoder_error_lower_bound": max(
                0.0,
                haar_obstruction["normalized_diamond_error_lower_bound"]
                - correction,
            ),
            "haar_optimizer_record": haar_obstruction["optimizer_record"],
        },
        "canonical_peter_weyl_constructive_branch": {
            "reference_cutoff_J": reference_cutoff,
            "haar_constructive_decoder_error_upper_bound": haar_constructive,
            "physical_constructive_decoder_error_upper_bound": min(
                1.0, haar_constructive + correction
            ),
        },
        "resource_comparison_boundary": (
            "the lower branch is uniform under a mean-Casimir budget; the upper "
            "branch uses a specified canonical Peter-Weyl token, so this is not a "
            "single-resource bracket until a common resource condition is proved"
        ),
    }


def matter_collective_diffusion_rate_lower_bound(
    coupling: float,
    lapse: float,
    zero_frequency_spectrum_lower_bound: float,
) -> float:
    """Return ``pi lambda^2 j(0)_lower/N^2`` in observer proper time."""
    _validate_positive("coupling", coupling)
    _validate_positive("lapse", lapse)
    _validate_positive(
        "zero_frequency_spectrum_lower_bound",
        zero_frequency_spectrum_lower_bound,
    )
    return (
        pi
        * coupling**2
        * zero_frequency_spectrum_lower_bound
        / lapse**2
    )


def fixed_spin_spectral_obstruction_from_residual(
    spin: int,
    *,
    heat_to_haar_bound: NormalizedDiamondDistanceBound,
    spectral_residual: AncillaStableOperatorNormResidual,
) -> dict[str, object]:
    """Transfer a state operator-norm residual through the Choi witness only."""
    _validate_spin(spin)
    heat = _require_diamond_bound("heat_to_haar_bound", heat_to_haar_bound)
    residual = _require_operator_residual(spectral_residual)
    dimension = 2 * spin + 1
    lower_bound = max(
        0.0,
        1.0 - 1.0 / dimension - heat.value - dimension * residual.value,
    )
    return {
        "spin_L": spin,
        "dimension_d": dimension,
        "heat_to_haar_bound": _diamond_bound_record(heat),
        "spectral_residual": _operator_residual_record(residual),
        "decoder_witness_trace_norm": float(dimension),
        "physical_any_decoder_witness_error_lower_bound": lower_bound,
        "transfer_formula": "max(0,1-1/d-eta_heat-d*epsilon_infinity)",
        "norm_boundary": (
            "epsilon_infinity is used only against the fixed pulled-back Choi "
            "witness of trace norm d; no channel diamond bound is inferred"
        ),
    }


def finite_switch_matter_obstruction_record(
    spin: int,
    *,
    lapse: float,
    coupling: float,
    elapsed_time: float,
    burn_in: float,
    switch_effective_lead: float,
    jump_l1_upper_bound: float,
    jump_first_moment_upper_bound: float,
    zero_frequency_spectrum_lower_bound: float,
) -> dict[str, object]:
    """Compose matter rate, finite switching, heat mixing, and witness transfer."""
    _validate_spin(spin)
    diffusion_rate_lower = matter_collective_diffusion_rate_lower_bound(
        coupling,
        lapse,
        zero_frequency_spectrum_lower_bound,
    )
    heat_record = finite_time_twirl_distance_record(
        elapsed_time,
        diffusion_rate=diffusion_rate_lower,
    )
    heat = NormalizedDiamondDistanceBound(
        heat_record["normalized_diamond_distance_to_haar_upper_bound"],
        "SO(3) heat bound evaluated at a certified diffusion-rate lower bound",
    )
    residual_value = ancilla_stable_finite_switch_ule_residual_bound(
        spin,
        lapse,
        coupling,
        elapsed_time,
        burn_in,
        switch_effective_lead,
        jump_l1_upper_bound,
        jump_first_moment_upper_bound,
    )
    residual = AncillaStableOperatorNormResidual(
        residual_value,
        "finite-switch Nathan-Rudner state residual with moment upper bounds",
    )
    obstruction = fixed_spin_spectral_obstruction_from_residual(
        spin,
        heat_to_haar_bound=heat,
        spectral_residual=residual,
    )
    return {
        **obstruction,
        "lapse_N": lapse,
        "coupling_lambda": coupling,
        "elapsed_time_T": elapsed_time,
        "burn_in_B": burn_in,
        "switch_effective_lead_T_chi": switch_effective_lead,
        "zero_frequency_spectrum_lower_bound": (
            zero_frequency_spectrum_lower_bound
        ),
        "diffusion_rate_lower_bound": diffusion_rate_lower,
        "jump_l1_upper_bound": jump_l1_upper_bound,
        "jump_first_moment_upper_bound": jump_first_moment_upper_bound,
        "result_type": "spectral_witness_obstruction_not_diamond_transfer",
    }


def static_patch_matter_observer_channel_certificate() -> dict[str, object]:
    """Audit the norm separation and both finite-time transfer formulas."""
    zero = NormalizedDiamondDistanceBound(0.0, "exact channel identity")
    generic = recovery_error_transfer_bracket(
        haar_any_decoder_lower_bound=0.4,
        haar_constructive_decoder_upper_bound=0.6,
        heat_to_haar_bound=zero,
        physical_to_heat_bound=zero,
    )
    local = NormalizedDiamondDistanceBound(
        0.01,
        "synthetic typed API witness, not a physical local-channel estimate",
    )
    finite_time = finite_time_peter_weyl_recovery_transfer_record(
        8,
        512,
        maximum_mean_casimir=1.0,
        proper_time=2.0,
        diffusion_rate=1.0,
        physical_to_heat_bound=local,
    )

    spin = 8
    lapse = 1.0
    coupling = 1.0e-8
    zero_spectrum = 1.0
    diffusion_rate = matter_collective_diffusion_rate_lower_bound(
        coupling,
        lapse,
        zero_spectrum,
    )
    heat_time = log(float(2 * spin + 1)) / (2.0 * diffusion_rate)
    short_burn = finite_switch_matter_obstruction_record(
        spin,
        lapse=lapse,
        coupling=coupling,
        elapsed_time=heat_time,
        burn_in=1.0,
        switch_effective_lead=1.0,
        jump_l1_upper_bound=3.0,
        jump_first_moment_upper_bound=1.0,
        zero_frequency_spectrum_lower_bound=zero_spectrum,
    )
    long_burn = finite_switch_matter_obstruction_record(
        spin,
        lapse=lapse,
        coupling=coupling,
        elapsed_time=heat_time,
        burn_in=heat_time,
        switch_effective_lead=1.0,
        jump_l1_upper_bound=3.0,
        jump_first_moment_upper_bound=1.0,
        zero_frequency_spectrum_lower_bound=zero_spectrum,
    )
    claims = {
        "zero_diamond_perturbation_preserves_recovery_bounds": (
            generic["physical_any_decoder_error_lower_bound"] == 0.4
            and generic["physical_constructive_decoder_error_upper_bound"] == 0.6
        ),
        "synthetic_finite_time_diamond_transfer_is_nontrivial": finite_time[
            "energy_constrained_obstruction_branch"
        ]["physical_any_decoder_error_lower_bound"]
        > 0.0,
        "finite_time_constructive_branch_is_bounded": 0.0
        <= finite_time["canonical_peter_weyl_constructive_branch"][
            "physical_constructive_decoder_error_upper_bound"
        ]
        <= 1.0,
        "longer_burn_in_improves_spectral_obstruction": long_burn[
            "physical_any_decoder_witness_error_lower_bound"
        ]
        >= short_burn["physical_any_decoder_witness_error_lower_bound"],
        "spectral_matter_witness_is_nontrivial": long_burn[
            "physical_any_decoder_witness_error_lower_bound"
        ]
        > 0.0,
        "operator_residual_is_not_reported_as_diamond_distance": long_burn[
            "spectral_residual"
        ]["norm_kind"]
        == "ancilla_stable_state_operator_norm",
    }
    return {
        "goal": "Finite-Time Matter-To-Observer Recovery Transfer",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "norm_separated_obstruction_and_completeness_transfer",
        "central_result": (
            "Normalized diamond perturbations transfer both any-decoder lower "
            "bounds and explicit-decoder upper bounds. The current finite-switch "
            "ULE residual instead transfers only through the fixed Choi witness, "
            "with an explicit factor d, and is never relabeled a channel bound."
        ),
        "certified_claims": claims,
        "generic_zero_perturbation_record": generic,
        "finite_time_peter_weyl_record": finite_time,
        "short_burn_spectral_record": short_burn,
        "long_burn_spectral_record": long_burn,
        "claim_boundary": (
            "The diamond theorem is conditional on an independently certified "
            "physical-to-heat normalized diamond bound. The spectral theorem uses "
            "only a fixed-spin Choi witness and does not certify constructive "
            "diamond completeness. Applying the matter record to the Skyrmion "
            "requires AU.1 profile closure, interval-certified global jump moments, "
            "a derived switch and collective projection, and a local field-top model."
        ),
        "next_physics_gate": (
            "derive a local matter-to-rotor channel estimate in normalized diamond "
            "distance, or prove a finite-dimensional trace-norm upgrade of the "
            "ULE residual"
        ),
    }
