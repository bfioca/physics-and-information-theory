"""Local pseudoscalar gyroscope candidate and lapse-scaling obstruction.

For a conformally coupled pseudoscalar, the acceleration-improved physical
gradient is exactly the optical gradient times ``N^-2``.  A parity-even rotor
phase-space action can therefore realize the gradient Kossakowski tensor for
two localized spin systems.  The same identity fixes the proper-time spectral
scaling and exposes a nonuniform fixed-coupling Davies limit near the horizon.
"""

from __future__ import annotations

from math import isfinite, log, sin, sqrt

from .static_patch_scalar_common_mode import maximum_same_shell_angular_separation


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def static_lapse_from_horizon_distance(
    horizon_distance: float,
    *,
    radius: float = 1.0,
) -> float:
    """Return the exact static lapse ``N=sin(rho/R)``."""
    _validate_positive("horizon_distance", horizon_distance)
    _validate_positive("radius", radius)
    if horizon_distance > 0.5 * 3.141592653589793 * radius:
        raise ValueError("horizon_distance must be at most pi R/2")
    return sin(horizon_distance / radius)


def optical_gradient_from_improved_physical_components(
    lapse: float,
    *,
    physical_gradient_component: float,
    acceleration_component: float,
    physical_field_value: float,
) -> float:
    """Return ``N^2(nabla_hat chi+a_hat chi)=D_hat^opt chi_opt``."""
    _validate_positive("lapse", lapse)
    if lapse > 1.0:
        raise ValueError("lapse must be at most one")
    for name, value in (
        ("physical_gradient_component", physical_gradient_component),
        ("acceleration_component", acceleration_component),
        ("physical_field_value", physical_field_value),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    return lapse**2 * (
        physical_gradient_component
        + acceleration_component * physical_field_value
    )


def proper_time_zero_frequency_spectrum(
    lapse: float,
    *,
    optical_zero_frequency_spectrum: float,
) -> float:
    """Return ``S_tau(0)=N^-3 S_opt(0)`` for the improved gradient."""
    _validate_positive("lapse", lapse)
    if lapse > 1.0:
        raise ValueError("lapse must be at most one")
    _validate_positive(
        "optical_zero_frequency_spectrum",
        optical_zero_frequency_spectrum,
    )
    return optical_zero_frequency_spectrum / lapse**3


def proper_time_bath_correlation_time(
    lapse: float,
    *,
    optical_correlation_time: float,
) -> float:
    """Return the redshifted bath time ``tau_B=N tau_B,opt``."""
    _validate_positive("lapse", lapse)
    if lapse > 1.0:
        raise ValueError("lapse must be at most one")
    _validate_positive("optical_correlation_time", optical_correlation_time)
    return lapse * optical_correlation_time


def pseudoscalar_markov_parameter(
    lapse: float,
    *,
    coupling: float,
    optical_zero_frequency_spectrum: float = 1.0,
    optical_correlation_time: float = 1.0,
    system_casimir_load: float = 1.0,
) -> float:
    """Return the loaded weak-coupling parameter for a declared sector."""
    _validate_positive("coupling", coupling)
    _validate_positive("system_casimir_load", system_casimir_load)
    spectrum = proper_time_zero_frequency_spectrum(
        lapse,
        optical_zero_frequency_spectrum=optical_zero_frequency_spectrum,
    )
    correlation_time = proper_time_bath_correlation_time(
        lapse,
        optical_correlation_time=optical_correlation_time,
    )
    return (
        system_casimir_load
        * coupling**2
        * spectrum
        * correlation_time
    )


def pseudoscalar_gyroscope_record(
    spin: int,
    *,
    horizon_distance: float,
    radius: float = 1.0,
    fixed_coupling: float = 0.01,
    optical_zero_frequency_spectrum: float = 1.0,
    optical_correlation_time: float = 1.0,
    optical_smeared_gradient_rms: float = 1.0,
    maximum_interaction_rms: float = 1.0,
    mismatch_coefficient: float = 1.0,
) -> dict[str, object]:
    """Audit rate, Markov, localization, and reference-state RMS scalings."""
    _validate_positive_integer("spin", spin)
    for name, value in (
        ("fixed_coupling", fixed_coupling),
        ("optical_zero_frequency_spectrum", optical_zero_frequency_spectrum),
        ("optical_correlation_time", optical_correlation_time),
        ("optical_smeared_gradient_rms", optical_smeared_gradient_rms),
        ("maximum_interaction_rms", maximum_interaction_rms),
        ("mismatch_coefficient", mismatch_coefficient),
    ):
        _validate_positive(name, value)
    lapse = static_lapse_from_horizon_distance(
        horizon_distance,
        radius=radius,
    )
    dimension = 2 * spin + 1
    dimensionless_time = 0.5 * log(float(dimension))
    spectrum = proper_time_zero_frequency_spectrum(
        lapse,
        optical_zero_frequency_spectrum=optical_zero_frequency_spectrum,
    )
    bath_time = proper_time_bath_correlation_time(
        lapse,
        optical_correlation_time=optical_correlation_time,
    )
    casimir_load = float(spin * (spin + 1))
    fixed_markov = pseudoscalar_markov_parameter(
        lapse,
        coupling=fixed_coupling,
        optical_zero_frequency_spectrum=optical_zero_frequency_spectrum,
        optical_correlation_time=optical_correlation_time,
        system_casimir_load=casimir_load,
    )
    rms_budget_coupling = (
        maximum_interaction_rms
        * lapse**2
        / (sqrt(casimir_load) * optical_smeared_gradient_rms)
    )
    rms_budget_rate = rms_budget_coupling**2 * spectrum
    rms_budget_markov = rms_budget_rate * bath_time * casimir_load
    scheduled_protocol_time = dimensionless_time / rms_budget_rate
    leading_distance = sqrt(
        mismatch_coefficient
        / (
            dimension
            * spin
            * (spin + 1)
            * log(float(dimension))
        )
    )
    leading_angle = maximum_same_shell_angular_separation(
        horizon_distance,
        leading_distance,
        radius=radius,
    )
    return {
        "spin_L": spin,
        "sector_dimension_d": dimension,
        "horizon_distance_rho": horizon_distance,
        "static_lapse_N": lapse,
        "dimensionless_protocol_time_s": dimensionless_time,
        "proper_zero_frequency_spectrum": spectrum,
        "proper_bath_correlation_time": bath_time,
        "system_casimir_load_L_L_plus_1": casimir_load,
        "fixed_physical_coupling": fixed_coupling,
        "fixed_coupling_loaded_markov_parameter": fixed_markov,
        "coupling_at_reference_state_interaction_rms_budget": (
            rms_budget_coupling
        ),
        "diffusion_rate_at_reference_state_rms_budget": rms_budget_rate,
        "loaded_markov_parameter_at_reference_state_rms_budget": (
            rms_budget_markov
        ),
        "proper_time_for_chosen_logarithmic_schedule_at_rms_budget": (
            scheduled_protocol_time
        ),
        "leading_higher_spin_center_distance_over_radius": leading_distance,
        "leading_same_shell_angular_separation": leading_angle,
        "scaled_scheduled_time_T_over_d_cubed_log_d": (
            scheduled_protocol_time
            / (dimension**3 * log(float(dimension)))
        ),
        "scaled_angle_theta_d_to_5_over_2_sqrt_log_d": (
            leading_angle
            * dimension**2.5
            * sqrt(log(float(dimension)))
        ),
        "top_action": (
            "S_top=int d tau[-m+(I/2)|varpi-g B|^2], "
            "B_a=e_a^mu(nabla_mu chi+a_mu chi), chi pseudoscalar"
        ),
        "canonical_interaction": "H_int=g J_a^left B_a up to sign convention",
        "parity": (
            "even because angular velocity/angular momentum and the improved "
            "gradient of a pseudoscalar are axial vectors"
        ),
        "hard_target_boundary": (
            "a localized spin multiplet has the same zero-Bohr coupling, but a "
            "distributed hard field target requires a local angular-current "
            "density and uncontrolled multipole/nonzero-Bohr corrections"
        ),
        "rms_budget_boundary": (
            "state-dependent second-moment budget on the declared spin sector "
            "and smearing state; not an operator-norm bound or all-state Davies "
            "estimate"
        ),
    }


def static_patch_pseudoscalar_gyroscope_certificate(
    *,
    maximum_spin: int = 4096,
    fixed_coupling: float = 0.01,
) -> dict[str, object]:
    """Certify the local action and its near-horizon lapse tradeoff."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 64:
        raise ValueError("maximum_spin must be at least sixty-four")
    _validate_positive("fixed_coupling", fixed_coupling)
    spins = tuple(
        sorted(
            {
                spin
                for spin in (16, 64, 256, 1024, maximum_spin)
                if spin <= maximum_spin
            }
            | {maximum_spin}
        )
    )
    records = tuple(
        pseudoscalar_gyroscope_record(
            spin,
            horizon_distance=1.0 / float(2 * spin + 1),
            fixed_coupling=fixed_coupling,
        )
        for spin in spins
    )
    certified_claims = {
        "fixed_coupling_loaded_markov_parameter_grows_on_samples": all(
            right["fixed_coupling_loaded_markov_parameter"]
            > left["fixed_coupling_loaded_markov_parameter"]
            for left, right in zip(records, records[1:])
        ),
        "rms_budget_coupling_includes_lapse_and_casimir_load": all(
            abs(
                record["coupling_at_reference_state_interaction_rms_budget"]
                * sqrt(record["system_casimir_load_L_L_plus_1"])
                / record["static_lapse_N"] ** 2
                - 1.0
            )
            < 1.0e-12
            for record in records
        ),
        "rms_budget_rate_has_N_over_casimir_scaling": all(
            abs(
                record["diffusion_rate_at_reference_state_rms_budget"]
                * record["system_casimir_load_L_L_plus_1"]
                / record["static_lapse_N"]
                - 1.0
            )
            < 1.0e-12
            for record in records
        ),
        "chosen_schedule_time_has_d_cubed_log_d_scaling": abs(
            records[-1]["scaled_scheduled_time_T_over_d_cubed_log_d"] - 0.125
        )
        < 5.0e-4,
        "geometry_translates_imported_distance_to_d_minus_five_halves_angle": abs(
            records[-1]["scaled_angle_theta_d_to_5_over_2_sqrt_log_d"]
            - 2.0
        )
        < 5.0e-4,
        "rms_budget_loaded_markov_parameter_decreases_on_samples": all(
            right["loaded_markov_parameter_at_reference_state_rms_budget"]
            < left["loaded_markov_parameter_at_reference_state_rms_budget"]
            for left, right in zip(records, records[1:])
        ),
    }
    return {
        "goal": "Local Pseudoscalar Gyroscope Static-Patch Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "local_action_lapse_and_davies_tradeoff",
        "central_result": (
            "A parity-even local rotor action with an acceleration-improved "
            "conformal pseudoscalar gradient realizes the optical-gradient "
            "covariance for localized spins. Its proper zero-frequency spectrum "
            "scales as N^-3 and its bath time as N."
        ),
        "scaling_consequence": (
            "For spin L, fixed physical coupling gives a loaded Markov parameter "
            "growing as L(L+1)N^-2. Under a declared reference-state interaction "
            "RMS budget, g scales as N^2/sqrt(L(L+1)) and the diffusion coefficient "
            "as N/[L(L+1)]. Running the chosen s=(1/2)log d schedule then takes "
            "Theta(L(L+1)log d/N), or Theta(d^3 log d) along N~1/d. The imported "
            "higher-spin distance law maps geometrically to an "
            "O(d^(-5/2)/sqrt(log d)) angle."
        ),
        "claim_boundary": (
            "the action derives the top-side and a lumped-spin zero-Bohr "
            "coupling. It selects the static congruence, breaks pseudoscalar "
            "shift symmetry through the acceleration term, assumes controlled "
            "derivative smearing and a state-specific RMS budget rather than an "
            "operator bound, and does not reduce a distributed hard angular "
            "current to one global L_a operator. The logarithmic time is a chosen "
            "sufficient schedule, not a necessary mixing time."
        ),
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "bound the multipole and nonzero-Bohr errors of the distributed hard "
            "angular current at the d^-5/2 same-shell angular scale, then include "
            "support stress and gravitational backreaction"
        ),
    }
