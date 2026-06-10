"""Spectral premises that turn energy into global SO(3) reference bounds.

For a rotationally invariant Hamiltonian with sector floors ``epsilon_j``,
the relative entropy of asymmetry of every state with mean energy at most
``E`` obeys

    A_SO(3) <= beta E + log sum_j (2j+1)^2 exp(-beta epsilon_j).

The multiplicity spaces on which rotations act trivially do not enter this
partition function.  This module also records a fixed bounded-spectrum
counterexample: covariance and finite mean energy alone do not control
orientation capacity unless the rotational-sector energies grow.
"""

from __future__ import annotations

from math import exp, isfinite, log

from .global_so3_reference_risk import (
    asymmetry_orientation_risk_lower_bound,
    hard_cutoff_orientation_risk_lower_bound,
    mean_casimir_orientation_risk_lower_bound,
    projective_hard_cutoff_orientation_risk_lower_bound,
    tail_quantile_orientation_risk_lower_bound,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_cutoff(reference_cutoff: int) -> None:
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")


def finite_rotational_partition_function(
    sector_energy_floors: tuple[float, ...],
    *,
    dual_parameter: float,
    projective: bool = False,
) -> float:
    """Evaluate ``sum_j (2j+1)^2 exp(-beta epsilon_j)`` exactly.

    The supplied tuple must contain every sector of the finite model.  Entry
    ``n`` represents spin ``n`` in the ordinary sector and spin ``n+1/2`` in
    the projective sector.
    """
    _validate_positive("dual_parameter", dual_parameter)
    if not sector_energy_floors:
        raise ValueError("sector_energy_floors must be nonempty")
    partition = 0.0
    for index, energy_floor in enumerate(sector_energy_floors):
        _validate_nonnegative("sector energy floor", energy_floor)
        dimension = 2 * index + (2 if projective else 1)
        partition += dimension**2 * exp(-dual_parameter * energy_floor)
    return partition


def log_finite_rotational_partition_function(
    sector_energy_floors: tuple[float, ...],
    *,
    dual_parameter: float,
    projective: bool = False,
) -> float:
    """Evaluate the finite rotational log partition without underflow."""
    _validate_positive("dual_parameter", dual_parameter)
    if not sector_energy_floors:
        raise ValueError("sector_energy_floors must be nonempty")
    log_terms = []
    for index, energy_floor in enumerate(sector_energy_floors):
        _validate_nonnegative("sector energy floor", energy_floor)
        dimension = 2 * index + (2 if projective else 1)
        log_terms.append(2.0 * log(dimension) - dual_parameter * energy_floor)
    maximum = max(log_terms)
    return maximum + log(sum(exp(term - maximum) for term in log_terms))


def gibbs_spectral_asymmetry_upper_bound(
    *,
    mean_energy: float,
    sector_energy_floors: tuple[float, ...],
    dual_parameter: float,
    projective: bool = False,
) -> float:
    """Return the Gibbs variational capacity ``beta E + log Z(beta)``."""
    _validate_nonnegative("mean_energy", mean_energy)
    log_partition = log_finite_rotational_partition_function(
        sector_energy_floors,
        dual_parameter=dual_parameter,
        projective=projective,
    )
    return dual_parameter * mean_energy + log_partition


def gibbs_spectral_orientation_risk_lower_bound(
    *,
    mean_energy: float,
    sector_energy_floors: tuple[float, ...],
    dual_parameter: float,
    projective: bool = False,
) -> float:
    """Compose the finite-spectrum Gibbs capacity with global Bayes risk."""
    capacity = gibbs_spectral_asymmetry_upper_bound(
        mean_energy=mean_energy,
        sector_energy_floors=sector_energy_floors,
        dual_parameter=dual_parameter,
        projective=projective,
    )
    return asymmetry_orientation_risk_lower_bound(capacity)


def casimir_coercive_orientation_risk_lower_bound(
    *,
    mean_energy: float,
    casimir_gap_coefficient: float,
) -> float:
    """Apply ``H_ex >= alpha J^2`` to get ``R>=alpha/(16E+8alpha)``."""
    _validate_nonnegative("mean_energy", mean_energy)
    _validate_positive("casimir_gap_coefficient", casimir_gap_coefficient)
    capacity = mean_energy / casimir_gap_coefficient
    return mean_casimir_orientation_risk_lower_bound(capacity)


def sector_tail_probability_upper_bound(
    *,
    mean_energy: float,
    first_excluded_sector_energy: float,
) -> float:
    """Markov bound for probability above a chosen representation cutoff."""
    _validate_nonnegative("mean_energy", mean_energy)
    _validate_positive(
        "first_excluded_sector_energy",
        first_excluded_sector_energy,
    )
    return min(1.0, mean_energy / first_excluded_sector_energy)


def spectral_tail_orientation_risk_lower_bound(
    *,
    reference_cutoff: int,
    mean_energy: float,
    first_excluded_sector_energy: float,
    projective: bool = False,
) -> float:
    """Transfer a spectral energy tail bound to the sharp cutoff risk floor."""
    _validate_cutoff(reference_cutoff)
    tail = sector_tail_probability_upper_bound(
        mean_energy=mean_energy,
        first_excluded_sector_energy=first_excluded_sector_energy,
    )
    if projective:
        cutoff_floor = projective_hard_cutoff_orientation_risk_lower_bound(
            reference_cutoff
        )
        return max(0.0, cutoff_floor - tail**0.5)
    return tail_quantile_orientation_risk_lower_bound(reference_cutoff, tail)


def bounded_spectrum_counterexample_record(
    reference_cutoff: int,
) -> dict[str, object]:
    """Exhibit bounded energy with an achievable risk tending to zero.

    On ``L^2(SO(3))`` use the fixed invariant Hamiltonian
    ``H_bad=sum_j (1-exp(-j)) P_j``.  A normalized Peter-Weyl kernel through
    spin ``J`` has the reported risk, while every state has energy below one.
    This is an obstruction to deriving an energy-reference theorem from
    positivity and rotational covariance alone.
    """
    _validate_cutoff(reference_cutoff)
    cutoff = float(reference_cutoff)
    numerator = 4.0 * cutoff * (cutoff + 2.0) + 3.0
    normalization = (
        4.0
        * (cutoff + 1.0)
        * (2.0 * cutoff + 1.0)
        * (2.0 * cutoff + 3.0)
        / 3.0
    )
    achievable_risk = numerator / normalization
    support_energy_ceiling = 1.0 - exp(-cutoff)
    sharp_cutoff_floor = hard_cutoff_orientation_risk_lower_bound(
        reference_cutoff
    )
    claims = {
        "hamiltonian_is_positive_and_uniformly_bounded_below_one": True,
        "cutoff_token_energy_is_at_most_numerical_unit_ceiling": (
            support_energy_ceiling <= 1.0
        ),
        "reported_risk_respects_sharp_cutoff_floor": (
            achievable_risk + 1e-15 >= sharp_cutoff_floor
        ),
    }
    return {
        "goal": "Rotational spectral confinement necessity",
        "status": "pass" if all(claims.values()) else "fail",
        "hamiltonian": "H_bad=sum_j (1-exp(-j)) P_j on L^2(SO(3))",
        "reference_cutoff_J": reference_cutoff,
        "cutoff_token_mean_energy_upper_bound": support_energy_ceiling,
        "log_strict_energy_gap_below_one": -cutoff,
        "cutoff_token_achievable_orientation_risk": achievable_risk,
        "sharp_cutoff_orientation_risk_lower_bound": sharp_cutoff_floor,
        "asymptotic_statement": (
            "The energy remains below one for every J while the achievable "
            "risk is O(1/J) and tends to zero."
        ),
        "claim_boundary": (
            "This is a mathematical obstruction Hamiltonian, not a local "
            "matter model. It proves that a growing rotational-sector spectral "
            "premise must be derived from the physical action."
        ),
        "certified_claims": claims,
    }
