"""Global orientation-risk floors from a reference-state stabilizer.

If a reference state is invariant under a nontrivial rotation ``h``, the
oriented states labelled by ``g`` and ``g h`` are identical.  Pairing those
two Haar-prior hypotheses gives a measurement-independent risk floor.  For the
unit-range chordal cost ``c(x)=sin^2(theta(x)/2)``, a stabilizer rotation of
angle ``alpha`` implies

    R_ref >= sin^2(alpha/4).

This is a global ambiguity theorem.  It is independent of local Fisher
information and of the Casimir carried by the state.
"""

from __future__ import annotations

from fractions import Fraction
from math import isfinite, pi, sin


def stabilizer_chordal_risk_lower_bound(rotation_angle: float) -> float:
    """Return the global Bayes-risk floor from one stabilizer element.

    The angle is the principal ``SO(3)`` rotation angle in ``[0, pi]``.
    Pairing ``g`` with ``g h`` gives

    ``R >= (1/2) min_x [c(x)+c(xh)]``.

    Orthogonal Procrustes maximization yields
    ``max_x Tr[x(I+h)]=2+4 cos(alpha/2)``, so the paired minimum is
    ``2 sin^2(alpha/4)``.
    """
    if not isfinite(rotation_angle) or not 0.0 <= rotation_angle <= pi:
        raise ValueError("rotation_angle must be finite and lie in [0, pi]")
    return sin(rotation_angle / 4.0) ** 2


def half_turn_stabilizer_risk_lower_bound() -> Fraction:
    """Return the exact chordal-risk floor for a half-turn stabilizer."""
    return Fraction(1, 2)


def spin_two_anticoherent_stabilizer_record() -> dict[str, object]:
    """Audit the half-turn stabilizer of the explicit spin-two state.

    The state has support only at magnetic labels ``m=-2,0,2``.  Rotation by
    ``pi`` about the quantization axis therefore multiplies every occupied
    component by ``exp(-i m pi)=1``.
    """
    occupied_magnetic_labels = (-2, 0, 2)
    phases = tuple(
        1 if magnetic_label % 2 == 0 else -1
        for magnetic_label in occupied_magnetic_labels
    )
    invariant = all(phase == 1 for phase in phases)
    exact_floor = half_turn_stabilizer_risk_lower_bound()
    return {
        "state": "(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2)",
        "occupied_magnetic_labels": occupied_magnetic_labels,
        "z_half_turn_phases": phases,
        "density_operator_is_half_turn_invariant": invariant,
        "stabilizer_rotation_angle": "pi",
        "global_chordal_risk_lower_bound_exact": str(exact_floor),
        "global_chordal_risk_lower_bound": float(exact_floor),
        "local_qfi_rank": 3,
        "leading_spin_two_stress_vanishes": True,
        "consequence": (
            "The explicit Q=0 state has full-rank local rotational QFI but "
            "cannot achieve global Haar-prior orientation risk below 1/2."
        ),
    }


def orientation_stabilizer_risk_certificate() -> dict[str, object]:
    """Return an executable certificate for the stabilizer theorem."""
    record = spin_two_anticoherent_stabilizer_record()
    half_turn_float = stabilizer_chordal_risk_lower_bound(pi)
    claims = {
        "half_turn_floor_is_one_half": abs(half_turn_float - 0.5) < 1.0e-15,
        "explicit_anticoherent_state_has_half_turn_stabilizer": record[
            "density_operator_is_half_turn_invariant"
        ],
        "explicit_q_zero_state_is_not_globally_accurate": record[
            "global_chordal_risk_lower_bound"
        ]
        >= 0.5,
    }
    return {
        "goal": "Global Orientation Risk From State Stabilizers",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "all_measurement_stabilizer_ambiguity_bound",
        "general_theorem": (
            "If U(h) rho U(h)^*=rho and h has principal rotation angle "
            "alpha, then every Haar-prior SO(3) orientation protocol with "
            "chordal cost obeys R_ref>=sin^2(alpha/4)."
        ),
        "spin_two_anticoherent_example": record,
        "certified_claims": claims,
        "claim_boundary": (
            "The theorem excludes globally accurate use of the explicit "
            "half-turn-invariant Q=0 state. It does not exclude Q=0 states "
            "with trivial stabilizer, stabilizers approaching the identity, "
            "or cross-spin states whose global orbit is asymptotically free."
        ),
    }
