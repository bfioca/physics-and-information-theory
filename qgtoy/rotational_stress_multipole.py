"""State-dependent spin-two stress in a leading rotating hedgehog.

For any state, define the real symmetric second moment

``S_ab = <{J_a,J_b}>/2`` and ``Q=S-<J^2>I/3``.

At quadratic order in collective angular velocity, spherical hedgehog
covariance restricts every scalar stress source to a radial scalar plus a term
``b(r) n_a n_b S_ab``.  Its entire nonspherical part is therefore
``b(r)n_a n_b Q_ab``.  Positivity of ``S`` gives sharp state-independent bounds,
while second-order anticoherent states have ``Q=0`` exactly.
"""

from __future__ import annotations

from fractions import Fraction
from math import isfinite, sqrt


def _validate_twice_spin(twice_spin: int) -> None:
    if (
        isinstance(twice_spin, bool)
        or not isinstance(twice_spin, int)
        or twice_spin < 3
    ):
        raise ValueError("twice_spin must be an integer at least three")


def _fraction_record(value: Fraction) -> dict[str, object]:
    return {"exact": str(value), "value": float(value)}


def universal_quadrupole_norm_bounds(mean_casimir: float) -> dict[str, float | str]:
    """Bound the traceless second moment using only ``Tr(S)=<J^2>``."""
    if not isfinite(mean_casimir) or mean_casimir < 0.0:
        raise ValueError("mean_casimir must be finite and nonnegative")
    return {
        "mean_casimir": mean_casimir,
        "quadrupole_operator_norm_upper_bound": 2.0 * mean_casimir / 3.0,
        "quadrupole_frobenius_norm_upper_bound": sqrt(2.0 / 3.0)
        * mean_casimir,
        "pointwise_nQn_absolute_upper_bound": 2.0 * mean_casimir / 3.0,
        "angular_rms_nQn_upper_bound": 2.0 * mean_casimir / (3.0 * sqrt(5.0)),
        "proof": (
            "S is positive semidefinite with trace C. Thus Tr(S^2)<=C^2, "
            "Tr(Q^2)=Tr(S^2)-C^2/3<=2C^2/3, and ||Q||op<=2C/3. "
            "The sphere identity <(nQn)^2>=2 Tr(Q^2)/15 gives the RMS bound."
        ),
    }


def spin_cat_quadrupole_record(twice_spin: int) -> dict[str, object]:
    """Return exact spin-two moments of ``(|j,j>+|j,-j>)/sqrt(2)``."""
    _validate_twice_spin(twice_spin)
    spin = Fraction(twice_spin, 2)
    casimir = spin * (spin + 1)
    transverse = spin / 2
    longitudinal = spin**2
    q_transverse = transverse - casimir / 3
    q_longitudinal = longitudinal - casimir / 3
    frobenius_squared = 2 * q_transverse**2 + q_longitudinal**2
    return {
        "state": "(|j,j>+|j,-j>)/sqrt(2)",
        "spin_j": _fraction_record(spin),
        "mean_casimir": _fraction_record(casimir),
        "symmetric_second_moment_eigenvalues": tuple(
            _fraction_record(value)
            for value in (transverse, transverse, longitudinal)
        ),
        "quadrupole_eigenvalues": tuple(
            _fraction_record(value)
            for value in (q_transverse, q_transverse, q_longitudinal)
        ),
        "quadrupole_trace": _fraction_record(
            2 * q_transverse + q_longitudinal
        ),
        "quadrupole_frobenius_norm_squared": _fraction_record(
            frobenius_squared
        ),
        "quadrupole_operator_norm": _fraction_record(abs(q_longitudinal)),
        "operator_norm_to_casimir_ratio": _fraction_record(
            abs(q_longitudinal) / casimir
        ),
        "asymptotic_operator_norm_to_casimir_ratio": "2/3",
    }


def spin_two_tetrahedral_anticoherent_record() -> dict[str, object]:
    """Return an explicit pure spin-2 second-order anticoherent state.

    The state is
    ``(|2,2>+|2,-2>)/2 + i|2,0>/sqrt(2)``.
    Direct ladder-operator evaluation gives zero first moment and ``S=2I``.
    """
    zero = Fraction(0)
    two = Fraction(2)
    eight = Fraction(8)
    return {
        "spin_j": 2,
        "state": "(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2)",
        "normalization_squared": _fraction_record(Fraction(1)),
        "mean_angular_momentum": tuple(_fraction_record(zero) for _ in range(3)),
        "mean_casimir": _fraction_record(Fraction(6)),
        "symmetric_second_moment_eigenvalues": tuple(
            _fraction_record(two) for _ in range(3)
        ),
        "quadrupole_eigenvalues": tuple(_fraction_record(zero) for _ in range(3)),
        "quadrupole_frobenius_norm_squared": _fraction_record(zero),
        "pure_state_rotational_qfi_eigenvalues": tuple(
            _fraction_record(eight) for _ in range(3)
        ),
        "rotational_qfi_rank": 3,
        "interpretation": (
            "The leading spin-two stress vanishes although the local rotational "
            "orbit is sensitive in all three directions. The finite tetrahedral "
            "stabilizer can still create global orientation ambiguities."
        ),
    }


def hedgehog_rotational_stress_multipole_record(
    *,
    mean_casimir: float,
    radial_quadrupole_coefficient: float,
    quadrupole_frobenius_norm: float,
) -> dict[str, float | bool | str]:
    """Bound the ``l=2`` part of ``b(r)n_a n_b S_ab`` at one radius."""
    bounds = universal_quadrupole_norm_bounds(mean_casimir)
    if not isfinite(radial_quadrupole_coefficient):
        raise ValueError("radial_quadrupole_coefficient must be finite")
    if (
        not isfinite(quadrupole_frobenius_norm)
        or quadrupole_frobenius_norm < 0.0
    ):
        raise ValueError(
            "quadrupole_frobenius_norm must be finite and nonnegative"
        )
    maximum_frobenius = float(bounds["quadrupole_frobenius_norm_upper_bound"])
    if quadrupole_frobenius_norm > maximum_frobenius * (1.0 + 1.0e-12):
        raise ValueError("quadrupole norm exceeds the universal Casimir bound")
    coefficient = abs(radial_quadrupole_coefficient)
    return {
        "mean_casimir": mean_casimir,
        "radial_quadrupole_coefficient": radial_quadrupole_coefficient,
        "quadrupole_frobenius_norm": quadrupole_frobenius_norm,
        "pointwise_l2_source_upper_bound": coefficient
        * min(2.0 * mean_casimir / 3.0, quadrupole_frobenius_norm),
        "angular_rms_l2_source": coefficient
        * sqrt(2.0 / 15.0)
        * quadrupole_frobenius_norm,
        "leading_l2_source_vanishes": quadrupole_frobenius_norm == 0.0,
        "decomposition": (
            "n_a n_b S_ab=C/3+n_a n_b Q_ab; the first term is monopole and "
            "the second is the complete leading spin-two source"
        ),
    }


def integrated_hedgehog_quadrupole_energy_record(
    *,
    mean_casimir: float,
    moment_of_inertia: float,
    quadrupole_frobenius_norm: float,
) -> dict[str, float | bool | str]:
    """Bound the radially integrated leading spin-two rotational energy.

    For local inertia density ``i(r)``, the quadratic hedgehog energy is
    ``3 i(r)[C-nSn]/(16 pi I^2)``. Integrating ``i(r)`` gives ``I``.
    Cauchy-Schwarz on the sphere and the exact fourth angular moment then give
    ``E_l2,L1 <= 3 sqrt(2/15)||Q||_F/(4I) <= E_rot/sqrt(5)``.
    """
    bounds = universal_quadrupole_norm_bounds(mean_casimir)
    if not isfinite(moment_of_inertia) or moment_of_inertia <= 0.0:
        raise ValueError("moment_of_inertia must be finite and positive")
    if (
        not isfinite(quadrupole_frobenius_norm)
        or quadrupole_frobenius_norm < 0.0
    ):
        raise ValueError(
            "quadrupole_frobenius_norm must be finite and nonnegative"
        )
    if quadrupole_frobenius_norm > float(
        bounds["quadrupole_frobenius_norm_upper_bound"]
    ) * (1.0 + 1.0e-12):
        raise ValueError("quadrupole norm exceeds the universal Casimir bound")
    total_rotor_energy = mean_casimir / (2.0 * moment_of_inertia)
    l1_quadrupole_energy = (
        3.0
        * sqrt(2.0 / 15.0)
        * quadrupole_frobenius_norm
        / (4.0 * moment_of_inertia)
    )
    universal_l1_upper = total_rotor_energy / sqrt(5.0)
    return {
        "mean_casimir": mean_casimir,
        "moment_of_inertia": moment_of_inertia,
        "total_leading_rotor_energy": total_rotor_energy,
        "radially_integrated_l1_spin_two_energy_upper_bound": (
            l1_quadrupole_energy
        ),
        "universal_l1_spin_two_energy_upper_bound": universal_l1_upper,
        "spin_two_to_total_energy_ratio_upper_bound": (
            l1_quadrupole_energy / total_rotor_energy
            if total_rotor_energy > 0.0
            else 0.0
        ),
        "universal_ratio_upper_bound": 1.0 / sqrt(5.0),
        "leading_spin_two_energy_vanishes": quadrupole_frobenius_norm == 0.0,
        "local_energy_form": (
            "dE_rot/drdOmega=3 i(r)[2C/3-nQn]/(16 pi I^2)"
        ),
        "claim_boundary": (
            "Uses the leading fixed-profile hedgehog inertia projector. It is an "
            "energy-source norm, not yet a metric perturbation bound."
        ),
    }


def rotational_stress_multipole_certificate() -> dict[str, object]:
    """Certify the universal bound and the anisotropic/isotropic state fork."""
    cat = spin_cat_quadrupole_record(20)
    tetrahedral = spin_two_tetrahedral_anticoherent_record()
    cat_casimir = float(Fraction(cat["mean_casimir"]["exact"]))
    cat_frobenius = sqrt(
        float(Fraction(cat["quadrupole_frobenius_norm_squared"]["exact"]))
    )
    cat_source = hedgehog_rotational_stress_multipole_record(
        mean_casimir=cat_casimir,
        radial_quadrupole_coefficient=1.0,
        quadrupole_frobenius_norm=cat_frobenius,
    )
    anticoherent_source = hedgehog_rotational_stress_multipole_record(
        mean_casimir=6.0,
        radial_quadrupole_coefficient=1.0,
        quadrupole_frobenius_norm=0.0,
    )
    cat_energy = integrated_hedgehog_quadrupole_energy_record(
        mean_casimir=cat_casimir,
        moment_of_inertia=1.0,
        quadrupole_frobenius_norm=cat_frobenius,
    )
    anticoherent_energy = integrated_hedgehog_quadrupole_energy_record(
        mean_casimir=6.0,
        moment_of_inertia=1.0,
        quadrupole_frobenius_norm=0.0,
    )
    claims = {
        "cat_quadrupole_is_traceless": cat["quadrupole_trace"]["exact"] == "0",
        "cat_approaches_sharp_operator_bound": (
            cat["operator_norm_to_casimir_ratio"]["value"] > 0.5
        ),
        "anticoherent_pure_state_has_zero_quadrupole": tetrahedral[
            "quadrupole_frobenius_norm_squared"
        ]["exact"]
        == "0",
        "anticoherent_state_has_full_rank_local_qfi": tetrahedral[
            "rotational_qfi_rank"
        ]
        == 3,
        "leading_stress_fork_is_nontrivial": (
            cat_source["angular_rms_l2_source"] > 0.0
            and anticoherent_source["leading_l2_source_vanishes"]
        ),
        "spin_two_energy_is_uniformly_bounded_by_rotor_energy": (
            cat_energy["spin_two_to_total_energy_ratio_upper_bound"]
            <= cat_energy["universal_ratio_upper_bound"]
        ),
        "anticoherent_spin_two_energy_vanishes": anticoherent_energy[
            "leading_spin_two_energy_vanishes"
        ],
    }
    return {
        "goal": "Leading Rotational Stress Multipole Theorem",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "casimir_bounded_spin_two_stress_with_anticoherent_escape",
        "universal_bounds": universal_quadrupole_norm_bounds(cat_casimir),
        "spin_cat": cat,
        "spin_two_tetrahedral_anticoherent": tetrahedral,
        "cat_stress_source": cat_source,
        "anticoherent_stress_source": anticoherent_source,
        "cat_integrated_spin_two_energy": cat_energy,
        "anticoherent_integrated_spin_two_energy": anticoherent_energy,
        "certified_claims": claims,
        "paper_consequence": (
            "A universal observer no-go cannot assume that accurate rotational "
            "references necessarily source a leading quadrupolar metric response. "
            "The all-state branch needs a Casimir-controlled l=2 response bound; "
            "the Q=0 branch retains the spherical theorem at quadratic order."
        ),
        "claim_boundary": (
            "The angular theorem uses only quadratic collective rotation and "
            "hedgehog covariance. It does not derive the radial stress coefficient, "
            "solve the spin-two Einstein equations, remove discrete stabilizer "
            "ambiguities, or control Omega^4 and collective-projection errors."
        ),
    }
