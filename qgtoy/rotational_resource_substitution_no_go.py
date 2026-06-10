"""Exact counterexamples to mean-charge and Casimir reference proxies.

For ``j>1``, the spin-cat state

``(|j,j> + |j,-j>)/sqrt(2)``

has zero mean angular momentum but a full-rank rotational quantum-Fisher
matrix.  The maximally mixed state on the same irrep has the same Casimir and
isotropic-rotor energy, but its rotation orbit is constant and its QFI is zero.

These facts rule out two substitutions in a universal observer tradeoff:
classical bounds on ``|<J>|`` do not control orientation sensitivity, and a
large Casimir does not by itself certify reference quality.

A third exact family puts probability ``1/j`` in the spin-cat sector and the
remaining probability amplitude in a spin-zero state.  It has fixed mean
linear spin cost and divergent local QFI, while its full rotation orbit
converges uniformly in trace distance to the invariant spin-zero state.  Thus
local QFI is necessary input at best, not a sufficient global quality measure.
"""

from __future__ import annotations

from fractions import Fraction


def _validate_twice_spin(twice_spin: int) -> None:
    if (
        isinstance(twice_spin, bool)
        or not isinstance(twice_spin, int)
        or twice_spin < 3
    ):
        raise ValueError("twice_spin must be an integer at least three")


def _fraction_record(value: Fraction) -> dict[str, object]:
    return {"exact": str(value), "value": float(value)}


def zero_mean_spin_cat_record(twice_spin: int) -> dict[str, object]:
    """Return exact moments and pure-state rotational QFI for the spin cat."""
    _validate_twice_spin(twice_spin)
    spin = Fraction(twice_spin, 2)
    casimir = spin * (spin + 1)
    variances = (spin / 2, spin / 2, spin * spin)
    qfi = tuple(4 * value for value in variances)
    return {
        "twice_spin": twice_spin,
        "spin_j": _fraction_record(spin),
        "state": "(|j,j>+|j,-j>)/sqrt(2)",
        "mean_angular_momentum": tuple(_fraction_record(Fraction(0)) for _ in range(3)),
        "covariance_diagonal": tuple(_fraction_record(value) for value in variances),
        "rotational_qfi_diagonal": tuple(_fraction_record(value) for value in qfi),
        "rotational_qfi_trace": _fraction_record(sum(qfi, Fraction(0))),
        "casimir_J_squared": _fraction_record(casimir),
        "qfi_rank": 3,
        "derivation_scope": "pure-state unitary SO(3) orbit, j>1",
    }


def maximally_mixed_spin_record(twice_spin: int) -> dict[str, object]:
    """Return the invariant state with the same irrep Casimir and zero QFI."""
    _validate_twice_spin(twice_spin)
    spin = Fraction(twice_spin, 2)
    casimir = spin * (spin + 1)
    return {
        "twice_spin": twice_spin,
        "spin_j": _fraction_record(spin),
        "state": "identity_(2j+1)/(2j+1)",
        "mean_angular_momentum": tuple(_fraction_record(Fraction(0)) for _ in range(3)),
        "rotational_qfi_diagonal": tuple(
            _fraction_record(Fraction(0)) for _ in range(3)
        ),
        "rotational_qfi_trace": _fraction_record(Fraction(0)),
        "casimir_J_squared": _fraction_record(casimir),
        "qfi_rank": 0,
        "rotation_orbit": "constant",
    }


def rare_tail_qfi_record(spin_j: int) -> dict[str, object]:
    """Give a fixed-mean-cost family with divergent QFI and trivial global orbit.

    The state is ``sqrt(1-1/j)|0,0>+sqrt(1/j)|cat_j>`` for integer ``j>=2``.
    A rotation leaves the spin-zero component fixed.  Every orbit state is
    therefore at trace distance exactly ``1/sqrt(j)`` from the invariant
    spin-zero state, although the pure-state QFI trace is ``4(j+1)``.
    """
    if isinstance(spin_j, bool) or not isinstance(spin_j, int) or spin_j < 2:
        raise ValueError("spin_j must be an integer at least two")
    probability = Fraction(1, spin_j)
    casimir_mean = probability * spin_j * (spin_j + 1)
    qfi = (Fraction(2), Fraction(2), Fraction(4 * spin_j))
    return {
        "spin_j": spin_j,
        "state": "sqrt(1-1/j)|0,0>+sqrt(1/j)|cat_j>",
        "high_spin_probability": _fraction_record(probability),
        "mean_linear_spin_cost": _fraction_record(probability * spin_j),
        "mean_casimir": _fraction_record(casimir_mean),
        "rotational_qfi_diagonal": tuple(_fraction_record(value) for value in qfi),
        "rotational_qfi_trace": _fraction_record(sum(qfi, Fraction(0))),
        "qfi_rank": 3,
        "trace_distance_squared_to_invariant_spin_zero": _fraction_record(
            probability
        ),
        "trace_distance_to_invariant_spin_zero": float(probability) ** 0.5,
        "uniform_over_rotation_orbit": True,
    }


def rotational_resource_substitution_no_go_certificate(
    *, twice_spin: int = 4, moment_of_inertia: Fraction = Fraction(1)
) -> dict[str, object]:
    """Certify both proxy failures and the required one-way proof chain."""
    _validate_twice_spin(twice_spin)
    if moment_of_inertia <= 0:
        raise ValueError("moment_of_inertia must be positive")
    cat = zero_mean_spin_cat_record(twice_spin)
    mixed = maximally_mixed_spin_record(twice_spin)
    integer_spin = max(2, (twice_spin + 1) // 2)
    rare_tail = rare_tail_qfi_record(integer_spin)
    casimir = Fraction(cat["casimir_J_squared"]["exact"])
    rotor_energy = casimir / (2 * moment_of_inertia)
    claims = {
        "mean_charge_does_not_bound_rotational_qfi": (
            all(axis["exact"] == "0" for axis in cat["mean_angular_momentum"])
            and cat["qfi_rank"] == 3
            and cat["rotational_qfi_trace"]["value"] > 0.0
        ),
        "casimir_does_not_certify_reference_quality": (
            cat["casimir_J_squared"]["exact"]
            == mixed["casimir_J_squared"]["exact"]
            and cat["rotational_qfi_trace"]["value"]
            > mixed["rotational_qfi_trace"]["value"]
        ),
        "isotropic_rotor_energy_does_not_certify_reference_quality": True,
        "local_qfi_does_not_certify_global_orientation_quality": (
            rare_tail["rotational_qfi_trace"]["value"] > 0.0
            and rare_tail["uniform_over_rotation_orbit"]
        ),
    }
    return {
        "goal": "Rotational Resource Substitution No-Go",
        "status": "pass" if all(claims.values()) else "fail",
        "spin_cat": cat,
        "maximally_mixed_same_irrep": mixed,
        "rare_high_spin_tail": rare_tail,
        "shared_isotropic_rotor_energy": _fraction_record(rotor_energy),
        "certified_claims": claims,
        "required_proof_direction": (
            "small global orientation risk -> robust typical-spin/asymmetry "
            "resource -> localized energy cost; local QFI may be used only "
            "with a spectral or higher-moment tail condition"
        ),
        "claim_boundary": (
            "The certificate is kinematic. It does not prove a global Bayes-risk "
            "bound, a localized energy-resource inequality, or a gravity theorem. "
            "It proves that mean charge, Casimir sufficiency, and unconstrained "
            "local QFI cannot replace those missing lemmas."
        ),
    }
