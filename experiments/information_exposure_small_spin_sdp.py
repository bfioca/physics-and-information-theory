"""Smallest full-SO(3) information--disturbance frontier.

The source is an ordered pair of noncollinear spin-1/2 markers,
``|z+>_O |x+>_D``.  The joint representation is the physical integer-spin
``j=0 direct_sum j=1`` representation, so the orbit has a trivial SO(3)
stabilizer and encodes a full frame.

The SDP optimizes over every covariant instrument whose continuous outcome is
the frame estimate and whose quantum output is the recovered complete ``OD``
source.  It is an unrestricted finite-dimensional control calculation, not a
local-action or resource-cost theorem.

Install the optional solver dependencies with
``python -m pip install -e '.[research-sdp]'``.
"""

from __future__ import annotations

import argparse
import json
from math import pi, sqrt
from pathlib import Path
from typing import Any

try:
    import cvxpy as cp
    import numpy as np
    from numpy.polynomial.legendre import leggauss
except ImportError as exc:  # pragma: no cover - exercised only without extras
    raise SystemExit(
        "information_exposure_small_spin_sdp requires the research-sdp extra"
    ) from exc

from qgtoy.information_exposure_control import (
    SO3_HAAR_RANDOM_RISK,
    marvian_spekkens_pure_orbit_recovery_floor,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "experiments" / "information_exposure_small_spin_sdp.json"
SOURCE_DIMENSION = 4
CHOI_DIMENSION = SOURCE_DIMENSION**2
FRONTIER_RISKS = (0.54, 0.56, 0.60, 0.65, 0.70, 0.74)


def _z_rotation(angle: float) -> np.ndarray:
    return np.diag((np.exp(-0.5j * angle), np.exp(0.5j * angle)))


def _y_rotation(angle: float) -> np.ndarray:
    return np.array(
        (
            (np.cos(0.5 * angle), -np.sin(0.5 * angle)),
            (np.sin(0.5 * angle), np.cos(0.5 * angle)),
        ),
        dtype=complex,
    )


def _haar_samples(order: int) -> tuple[tuple[np.ndarray, float, float], ...]:
    """Product quadrature for normalized ZYZ Haar measure."""
    nodes, weights = leggauss(order)
    fourier_order = 2 * order + 1
    out = []
    for alpha_index in range(fourier_order):
        alpha = 2.0 * pi * alpha_index / fourier_order
        for gamma_index in range(fourier_order):
            gamma = 2.0 * pi * gamma_index / fourier_order
            for node, weight in zip(nodes, weights):
                beta = np.arccos(node)
                spinor = (
                    _z_rotation(alpha) @ _y_rotation(beta) @ _z_rotation(gamma)
                )
                representation = np.kron(spinor, spinor)
                normalized_weight = float(weight) / (2.0 * fourier_order**2)
                chordal_cost = 1.0 - abs(np.trace(spinor)) ** 2 / 4.0
                out.append((representation, normalized_weight, chordal_cost))
    return tuple(out)


def _fiducial() -> tuple[np.ndarray, np.ndarray]:
    z_plus = np.array((1.0, 0.0), dtype=complex)
    x_plus = np.array((1.0, 1.0), dtype=complex) / sqrt(2.0)
    vector = np.kron(z_plus, x_plus)
    return vector, np.outer(vector, vector.conjugate())


def _quadrature_operators(
    order: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    _, state = _fiducial()
    identity = np.eye(SOURCE_DIMENSION)
    probability_operator = np.kron(state.T, identity)
    fidelity_operator = np.kron(state.T, state)
    twirl = np.zeros((CHOI_DIMENSION**2, CHOI_DIMENSION**2), dtype=complex)
    risk_operator = np.zeros((CHOI_DIMENSION, CHOI_DIMENSION), dtype=complex)
    twirled_fidelity = np.zeros_like(risk_operator)
    state_twirl = np.zeros((SOURCE_DIMENSION, SOURCE_DIMENSION), dtype=complex)
    weight_sum = 0.0
    cost_average = 0.0

    for representation, weight, cost in _haar_samples(order):
        choi_representation = np.kron(
            representation.conjugate(), representation
        )
        twirl += weight * np.kron(
            choi_representation.conjugate(), choi_representation
        )
        risk_operator += weight * cost * (
            choi_representation.conjugate().T
            @ probability_operator
            @ choi_representation
        )
        twirled_fidelity += weight * (
            choi_representation.conjugate().T
            @ fidelity_operator
            @ choi_representation
        )
        state_twirl += weight * (
            representation @ state @ representation.conjugate().T
        )
        weight_sum += weight
        cost_average += weight * cost

    diagnostics = {
        "weight_sum_error": abs(weight_sum - 1.0),
        "haar_cost_average_error": abs(cost_average - SO3_HAAR_RANDOM_RISK),
        "fiducial_twirl_max_error": float(
            np.max(abs(state_twirl - np.eye(SOURCE_DIMENSION) / SOURCE_DIMENSION))
        ),
    }
    return twirl, risk_operator, twirled_fidelity, diagnostics


def _apply_twirl(twirl: np.ndarray, choi: np.ndarray) -> np.ndarray:
    vector = choi.reshape(-1, order="F")
    return (twirl @ vector).reshape((CHOI_DIMENSION, CHOI_DIMENSION), order="F")


def _partial_trace_output(choi: np.ndarray) -> np.ndarray:
    reshaped = choi.reshape(
        (
            SOURCE_DIMENSION,
            SOURCE_DIMENSION,
            SOURCE_DIMENSION,
            SOURCE_DIMENSION,
        )
    )
    return np.einsum("iaja->ij", reshaped)


def _generic_cloner_orbit_disturbance(
    risk: float,
    minimum_risk: float,
) -> float:
    record_shrinkage = (SO3_HAAR_RANDOM_RISK - risk) / (
        SO3_HAAR_RANDOM_RISK - minimum_risk
    )
    alpha_squared = max(0.0, min(1.0, 1.0 - record_shrinkage))
    alpha = sqrt(alpha_squared)
    beta = -alpha / SOURCE_DIMENSION + sqrt(
        1.0
        - alpha_squared
        + alpha_squared / SOURCE_DIMENSION**2
    )
    return beta * beta * (1.0 - 1.0 / SOURCE_DIMENSION)


def _solution_record(
    *,
    status: str,
    choi: np.ndarray,
    twirl: np.ndarray,
    risk_operator: np.ndarray,
    fidelity_operator: np.ndarray,
    minimum_risk: float,
) -> dict[str, float | str]:
    twirled = _apply_twirl(twirl, choi)
    risk = float(np.trace(risk_operator @ choi).real)
    fidelity = float(np.trace(fidelity_operator @ choi).real)
    return {
        "status": status,
        "risk": risk,
        "optimal_orbit_fidelity": fidelity,
        "optimal_orbit_recovery_infidelity": 1.0 - fidelity,
        "generic_u4_cloner_infidelity": _generic_cloner_orbit_disturbance(
            risk, minimum_risk
        ),
        "marvian_spekkens_control_floor": (
            marvian_spekkens_pure_orbit_recovery_floor(
                record_risk=risk,
                minimum_source_orbit_fidelity=0.0,
            )
        ),
        "minimum_seed_eigenvalue": float(np.min(np.linalg.eigvalsh(choi))),
        "trace_preserving_max_error": float(
            np.max(abs(_partial_trace_output(twirled) - np.eye(SOURCE_DIMENSION)))
        ),
    }


def build_record(*, solver: str = "CLARABEL") -> dict[str, Any]:
    twirl, risk_operator, fidelity_operator, diagnostics = _quadrature_operators(3)
    twirl_check, risk_check, fidelity_check, diagnostics_check = (
        _quadrature_operators(4)
    )
    diagnostics.update(
        {
            "order_3_vs_4_twirl_max_error": float(np.max(abs(twirl - twirl_check))),
            "order_3_vs_4_risk_operator_max_error": float(
                np.max(abs(risk_operator - risk_check))
            ),
            "order_3_vs_4_fidelity_operator_max_error": float(
                np.max(abs(fidelity_operator - fidelity_check))
            ),
            "order_4_weight_sum_error": diagnostics_check["weight_sum_error"],
        }
    )

    seed = cp.Variable((CHOI_DIMENSION, CHOI_DIMENSION), hermitian=True)
    vectorized_seed = cp.vec(seed, order="F")
    twirled_seed = cp.reshape(
        twirl @ vectorized_seed,
        (CHOI_DIMENSION, CHOI_DIMENSION),
        order="F",
    )
    risk_expression = cp.real(cp.trace(risk_operator @ seed))
    fidelity_expression = cp.real(cp.trace(fidelity_operator @ seed))
    base_constraints = (
        seed >> 0,
        cp.partial_trace(
            twirled_seed,
            (SOURCE_DIMENSION, SOURCE_DIMENSION),
            axis=1,
        )
        == np.eye(SOURCE_DIMENSION),
    )
    solve_options: dict[str, Any] = {"solver": solver, "warm_start": True}
    if solver == "CLARABEL":
        solve_options.update(
            {
                "tol_gap_abs": 2e-8,
                "tol_gap_rel": 2e-8,
                "tol_feas": 2e-8,
                "max_iter": 500,
            }
        )
    elif solver == "SCS":
        solve_options.update({"eps": 2e-7, "max_iters": 200_000})

    minimum_problem = cp.Problem(cp.Minimize(risk_expression), base_constraints)
    minimum_risk = float(minimum_problem.solve(**solve_options))
    minimum_record = _solution_record(
        status=minimum_problem.status,
        choi=seed.value,
        twirl=twirl,
        risk_operator=risk_operator,
        fidelity_operator=fidelity_operator,
        minimum_risk=minimum_risk,
    )

    maximum_problem = cp.Problem(cp.Maximize(fidelity_expression), base_constraints)
    maximum_problem.solve(**solve_options)
    identity_record = _solution_record(
        status=maximum_problem.status,
        choi=seed.value,
        twirl=twirl,
        risk_operator=risk_operator,
        fidelity_operator=fidelity_operator,
        minimum_risk=minimum_risk,
    )

    risk_limit = cp.Parameter(nonneg=True)
    frontier_problem = cp.Problem(
        cp.Maximize(fidelity_expression),
        base_constraints + (risk_expression <= risk_limit,),
    )
    frontier = []
    for requested_risk in FRONTIER_RISKS:
        risk_limit.value = requested_risk
        frontier_problem.solve(**solve_options)
        point = _solution_record(
            status=frontier_problem.status,
            choi=seed.value,
            twirl=twirl,
            risk_operator=risk_operator,
            fidelity_operator=fidelity_operator,
            minimum_risk=minimum_risk,
        )
        point["requested_risk_ceiling"] = requested_risk
        point["risk_ceiling_violation"] = max(0.0, point["risk"] - requested_risk)
        frontier.append(point)

    return {
        "schema": "information-exposure-small-spin-sdp-v1",
        "model": {
            "group": "SO(3)",
            "source": "ordered noncollinear spin-1/2 pair |z+>_O |x+>_D",
            "representation": "j=0 direct_sum j=1",
            "source_dimension": SOURCE_DIMENSION,
            "orbit_stabilizer": "trivial",
            "loss": "sin^2(theta_error/2)",
            "minimum_source_orbit_fidelity": 0.0,
            "koashi_imoto_nondisturbing_information_nats": 0.0,
        },
        "optimization": {
            "type": "covariant-instrument Choi SDP",
            "seed_dimension": CHOI_DIMENSION,
            "solver": solver,
            "cvxpy_version": cp.__version__,
            "numpy_version": np.__version__,
            "haar_quadrature": "ZYZ Fourier x Gauss-Legendre, order 3",
            "disturbance": "one minus complete-OD pure-orbit recovery fidelity",
            "not_controlled": (
                "diamond recovery, finite record dimension, local action, work, "
                "support, duration, KMS exposure, and gravity"
            ),
        },
        "quadrature_diagnostics": diagnostics,
        "endpoints": {
            "minimum_record_risk": minimum_record,
            "identity_source_channel": identity_record,
            "single_marker_full_frame_risk": 2.0 / 3.0,
        },
        "frontier": frontier,
        "counterexamples": {
            "redundant_transfer": (
                "With n retained and k transferred copies, universal n->n+k "
                "cloning gives error 1-d[n]/d[n+k]; n=J^2,k=J makes both "
                "record risk and recovery error vanish."
            ),
            "postselection": (
                "Success-only transfer has arbitrarily small conditional risk "
                "and O(p_s) unconditional disturbance; use the flagged channel."
            ),
        },
        "novelty_audit": {
            "generic_framework": "Sacchi, arXiv:quant-ph/0702033",
            "directly_adjacent_result": "Sacchi, arXiv:2606.18040",
            "directly_adjacent_scope": (
                "optimal full-state information-disturbance frontier for "
                "antiparallel spin pairs in the same j=0 direct_sum j=1 carrier"
            ),
            "difference_here": (
                "noncollinear ordered pair, full SO(3) frame loss, and complete "
                "OD wording"
            ),
            "verdict": (
                "KNOWN-FRAMEWORK SPECIALIZATION: useful control calculation, "
                "not a residual Paper U theorem"
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--solver", choices=("CLARABEL", "SCS"), default="CLARABEL")
    args = parser.parse_args()
    record = build_record(solver=args.solver)
    args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(
        "information-exposure SDP: "
        f"R_min={record['endpoints']['minimum_record_risk']['risk']:.12f}, "
        f"points={len(record['frontier'])}, "
        f"verdict={record['novelty_audit']['verdict']}"
    )


if __name__ == "__main__":
    main()
