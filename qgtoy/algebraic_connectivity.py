"""Goal 19 algebraic connectivity order-parameter certificates."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, log
from typing import Sequence

from .relative_entropy_bridge import (
    AXES,
    _qubit_antipodal_relative_entropy_bits,
    _rounded,
)


def _axis_relative_entropy_after_bits(
    *,
    bloch_radius: float,
    shrink: float,
) -> float:
    if not 0.0 < bloch_radius < 1.0:
        raise ValueError("bloch_radius must lie in (0,1)")
    output_radius = abs(shrink) * bloch_radius
    if output_radius == 0.0:
        return 0.0
    return output_radius * log(
        (1.0 + output_radius) / (1.0 - output_radius),
        2,
    )


def _axis_defect_bits(*, bloch_radius: float, shrink: float) -> float:
    before = _qubit_antipodal_relative_entropy_bits(bloch_radius)
    after = _axis_relative_entropy_after_bits(
        bloch_radius=bloch_radius,
        shrink=shrink,
    )
    return before - after


def _axis_response_ratio(*, bloch_radius: float, shrink: float) -> float:
    before = _qubit_antipodal_relative_entropy_bits(bloch_radius)
    after = _axis_relative_entropy_after_bits(
        bloch_radius=bloch_radius,
        shrink=shrink,
    )
    return after / before if before else 0.0


def _shrink_lower_bound_from_defect(
    *,
    bloch_radius: float,
    defect_bits: float,
) -> float:
    before = _qubit_antipodal_relative_entropy_bits(bloch_radius)
    if defect_bits <= 0.0:
        return 1.0
    target = before - defect_bits
    if target <= 0.0:
        return 0.0

    low = 0.0
    high = 1.0
    for _ in range(80):
        mid = (low + high) / 2.0
        after = _axis_relative_entropy_after_bits(
            bloch_radius=bloch_radius,
            shrink=mid,
        )
        if after < target:
            low = mid
        else:
            high = mid
    return high


def _pauli_probabilities(
    x_shrink: float,
    y_shrink: float,
    z_shrink: float,
) -> tuple[float, float, float, float]:
    return (
        (1.0 + x_shrink + y_shrink + z_shrink) / 4.0,
        (1.0 + x_shrink - y_shrink - z_shrink) / 4.0,
        (1.0 - x_shrink + y_shrink - z_shrink) / 4.0,
        (1.0 - x_shrink - y_shrink + z_shrink) / 4.0,
    )


def _is_pauli_diagonal_cptp(
    x_shrink: float,
    y_shrink: float,
    z_shrink: float,
) -> bool:
    return all(
        probability >= -1e-12
        for probability in _pauli_probabilities(x_shrink, y_shrink, z_shrink)
    )


def _phase_from_preserved_axes(preserved_axes: tuple[str, ...]) -> str:
    if len(preserved_axes) == 3:
        return "quantum_bridge"
    if len(preserved_axes) == 1:
        return "classical_bridge"
    if len(preserved_axes) == 0:
        return "null_bridge"
    return "incomplete_noncommuting_response_shadow"


def _missing_commutator_axes(preserved_axes: tuple[str, ...]) -> tuple[str, ...]:
    preserved = set(preserved_axes)
    missing = set()
    if {"X", "Y"} <= preserved and "Z" not in preserved:
        missing.add("Z")
    if {"Y", "Z"} <= preserved and "X" not in preserved:
        missing.add("X")
    if {"Z", "X"} <= preserved and "Y" not in preserved:
        missing.add("Y")
    return tuple(sorted(missing))


@dataclass(frozen=True)
class NoisyPauliBridge:
    """Unital one-qubit Pauli-diagonal bridge channel."""

    name: str
    shrinks: tuple[float, float, float]

    def __post_init__(self) -> None:
        if len(self.shrinks) != 3:
            raise ValueError("shrinks must have X,Y,Z entries")
        if any(abs(value) > 1.0 for value in self.shrinks):
            raise ValueError("Pauli shrink factors must lie in [-1,1]")
        if not _is_pauli_diagonal_cptp(*self.shrinks):
            raise ValueError("shrinks must define a CPTP Pauli-diagonal channel")

    @property
    def pauli_probabilities(self) -> tuple[float, float, float, float]:
        return _pauli_probabilities(*self.shrinks)

    def static_entropy_shadow(self) -> dict[str, object]:
        return {
            "channel": self.name,
            "maximally_mixed_input_entropy_bits": 1.0,
            "maximally_mixed_output_entropy_bits": 1.0,
            "named_static_entropy_shadow": (1.0, 1.0),
            "unital_channel_static_shadow_blind": True,
        }

    def response_rows(self, *, bloch_radius: float) -> tuple[dict[str, object], ...]:
        before = _qubit_antipodal_relative_entropy_bits(bloch_radius)
        rows = []
        for axis, shrink in zip(AXES, self.shrinks, strict=True):
            after = _axis_relative_entropy_after_bits(
                bloch_radius=bloch_radius,
                shrink=shrink,
            )
            rows.append(
                {
                    "axis": axis,
                    "shrink": shrink,
                    "relative_entropy_before_bits": _rounded(before),
                    "relative_entropy_after_bits": _rounded(after),
                    "defect_bits": _rounded(before - after),
                    "response_ratio": _rounded(after / before),
                }
            )
        return tuple(rows)

    def product_commutator_defects(self) -> dict[str, object]:
        x_shrink, y_shrink, z_shrink = self.shrinks
        defects = {
            "XY_to_Z": abs(x_shrink * y_shrink - z_shrink),
            "YZ_to_X": abs(y_shrink * z_shrink - x_shrink),
            "ZX_to_Y": abs(z_shrink * x_shrink - y_shrink),
        }
        return {
            "defects": {key: _rounded(value) for key, value in defects.items()},
            "max_product_commutator_defect": _rounded(max(defects.values())),
        }

    def order_parameter_record(
        self,
        *,
        bloch_radius: float,
        epsilon_bits: float,
    ) -> dict[str, object]:
        rows = self.response_rows(bloch_radius=bloch_radius)
        preserved_axes = tuple(
            row["axis"] for row in rows if row["defect_bits"] <= epsilon_bits
        )
        ratios = tuple(float(row["response_ratio"]) for row in rows)
        phase = _phase_from_preserved_axes(preserved_axes)
        missing_commutators = _missing_commutator_axes(preserved_axes)
        product = self.product_commutator_defects()
        min_defect = min(float(row["defect_bits"]) for row in rows)
        max_defect = max(float(row["defect_bits"]) for row in rows)
        return {
            "channel": self.name,
            "shrinks": self.shrinks,
            "pauli_probabilities": tuple(_rounded(value) for value in self.pauli_probabilities),
            "bloch_radius": bloch_radius,
            "epsilon_bits": epsilon_bits,
            "response_rows": rows,
            "preserved_axes_at_epsilon": preserved_axes,
            "response_only_phase": phase,
            "missing_commutator_axes": missing_commutators,
            "algebraic_phase": (
                "not_a_stable_algebra"
                if missing_commutators
                else phase
            ),
            "quantum_connectivity_strength": _rounded(min(ratios)),
            "classical_connectivity_strength": _rounded(max(ratios)),
            "relative_entropy_defect_range_bits": (
                _rounded(min_defect),
                _rounded(max_defect),
            ),
            "worst_axis_recovery_fidelity_lower_bound": _rounded(
                2 ** (-max_defect / 2.0)
            ),
            "product_commutator_stability": product,
            "static_entropy_shadow": self.static_entropy_shadow(),
        }


def _pauli_stability_theorem_record(
    *,
    bloch_radius: float,
    epsilon_bits: float,
) -> dict[str, object]:
    mu = _shrink_lower_bound_from_defect(
        bloch_radius=bloch_radius,
        defect_bits=epsilon_bits,
    )
    product_bound = 1.0 - mu * mu
    average_fidelity_bound = (1.0 + mu) / 2.0
    return {
        "theorem": "Pauli-diagonal noisy bridge stability bound",
        "scope": (
            "unital one-qubit Pauli-diagonal observer-bridge channels with "
            "nonnegative shrink factors"
        ),
        "hypothesis": (
            "All three Pauli-axis relative-entropy defects for full-rank "
            "antipodal probes of radius r are at most epsilon."
        ),
        "mu_lower_bound_on_each_axis_shrink": _rounded(mu),
        "average_gate_fidelity_to_identity_lower_bound": _rounded(
            average_fidelity_bound
        ),
        "product_commutator_defect_upper_bound": _rounded(product_bound),
        "proof_sketch": (
            "The antipodal qubit relative entropy D_r(a)=a r log((1+a r)/(1-a r)) "
            "is monotone in the absolute shrink a.  Defect <= epsilon implies "
            "each shrink is at least mu=D_r^{-1}(D_r(1)-epsilon)/r.  For a "
            "Pauli channel, entanglement fidelity is (1+lambda_X+lambda_Y+lambda_Z)/4, "
            "so the average gate fidelity is at least (1+mu)/2.  Multiplicative "
            "Pauli closure defects obey |lambda_i lambda_j-lambda_k| <= 1-mu^2."
        ),
    }


def _finite_bridge_examples() -> tuple[NoisyPauliBridge, ...]:
    return (
        NoisyPauliBridge("clean_quantum_bridge", (1.0, 1.0, 1.0)),
        NoisyPauliBridge("stable_noisy_quantum_bridge", (0.9, 0.9, 0.85)),
        NoisyPauliBridge("classical_z_bridge", (0.0, 0.0, 1.0)),
        NoisyPauliBridge("null_depolarizing_bridge", (0.0, 0.0, 0.0)),
        NoisyPauliBridge("two_axis_response_control", (0.75, 0.75, 0.5)),
    )


def _bounded_pauli_grid_record(
    *,
    bloch_radius: float,
    epsilon_bits: float,
    response_only_epsilon_bits: float,
) -> dict[str, object]:
    values = (0.0, 0.25, 0.5, 0.75, 1.0)
    records = []
    for x_shrink in values:
        for y_shrink in values:
            for z_shrink in values:
                if not _is_pauli_diagonal_cptp(x_shrink, y_shrink, z_shrink):
                    continue
                bridge = NoisyPauliBridge(
                    name=f"grid_{x_shrink}_{y_shrink}_{z_shrink}",
                    shrinks=(x_shrink, y_shrink, z_shrink),
                )
                records.append(
                    bridge.order_parameter_record(
                        bloch_radius=bloch_radius,
                        epsilon_bits=epsilon_bits,
                    )
                )
    phase_counts: dict[str, int] = {}
    for record in records:
        phase = str(record["algebraic_phase"])
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

    response_only_incomplete = []
    for x_shrink in values:
        for y_shrink in values:
            for z_shrink in values:
                if not _is_pauli_diagonal_cptp(x_shrink, y_shrink, z_shrink):
                    continue
                bridge = NoisyPauliBridge(
                    name=f"coarse_grid_{x_shrink}_{y_shrink}_{z_shrink}",
                    shrinks=(x_shrink, y_shrink, z_shrink),
                )
                record = bridge.order_parameter_record(
                    bloch_radius=bloch_radius,
                    epsilon_bits=response_only_epsilon_bits,
                )
                if record["missing_commutator_axes"]:
                    response_only_incomplete.append(record)

    return {
        "grid_values": values,
        "cptp_channels_checked": len(records),
        "epsilon_bits": epsilon_bits,
        "phase_counts": phase_counts,
        "all_static_entropy_shadows_match": all(
            record["static_entropy_shadow"]["named_static_entropy_shadow"]
            == (1.0, 1.0)
            for record in records
        ),
        "response_only_epsilon_bits": response_only_epsilon_bits,
        "response_only_incomplete_shadow_count": len(response_only_incomplete),
        "first_response_only_incomplete_shadow": (
            response_only_incomplete[0] if response_only_incomplete else None
        ),
    }


def goal19_algebraic_connectivity_order_parameter_certificate(
    *,
    bloch_radius: float = 0.5,
    epsilon_bits: float = 0.25,
    response_only_epsilon_bits: float = 0.4,
) -> dict[str, object]:
    if not 0.0 < bloch_radius < 1.0:
        raise ValueError("bloch_radius must lie in (0,1)")
    if epsilon_bits < 0.0 or response_only_epsilon_bits < 0.0:
        raise ValueError("epsilon values must be nonnegative")

    theorem = _pauli_stability_theorem_record(
        bloch_radius=bloch_radius,
        epsilon_bits=epsilon_bits,
    )
    examples = tuple(
        bridge.order_parameter_record(
            bloch_radius=bloch_radius,
            epsilon_bits=epsilon_bits,
        )
        for bridge in _finite_bridge_examples()
    )
    example_by_name = {record["channel"]: record for record in examples}
    coarse_control = NoisyPauliBridge(
        "two_axis_response_control",
        (0.75, 0.75, 0.5),
    ).order_parameter_record(
        bloch_radius=bloch_radius,
        epsilon_bits=response_only_epsilon_bits,
    )
    grid = _bounded_pauli_grid_record(
        bloch_radius=bloch_radius,
        epsilon_bits=epsilon_bits,
        response_only_epsilon_bits=response_only_epsilon_bits,
    )
    certified_claims = {
        "order_parameter_declared": True,
        "pauli_diagonal_stability_bound_computed": theorem[
            "mu_lower_bound_on_each_axis_shrink"
        ]
        > 0.0,
        "clean_bridge_quantum": example_by_name["clean_quantum_bridge"][
            "algebraic_phase"
        ]
        == "quantum_bridge",
        "stable_noisy_bridge_quantum_at_epsilon": example_by_name[
            "stable_noisy_quantum_bridge"
        ]["algebraic_phase"]
        == "quantum_bridge",
        "classical_bridge_identified": example_by_name["classical_z_bridge"][
            "algebraic_phase"
        ]
        == "classical_bridge",
        "null_bridge_identified": example_by_name["null_depolarizing_bridge"][
            "algebraic_phase"
        ]
        == "null_bridge",
        "static_entropy_shadow_blind_to_phase": all(
            record["static_entropy_shadow"]["named_static_entropy_shadow"]
            == (1.0, 1.0)
            for record in examples
        ),
        "response_only_shadow_has_product_closure_no_go": bool(
            coarse_control["missing_commutator_axes"]
        )
        and coarse_control["algebraic_phase"] == "not_a_stable_algebra",
        "bounded_grid_checked": grid["cptp_channels_checked"] > 0,
        "bounded_grid_static_entropy_blind": grid["all_static_entropy_shadows_match"],
        "goal18_exact_limit_recorded": True,
        "no_continuum_er_epr_or_de_sitter_claim": True,
    }
    certified_claims[
        "goal19_algebraic_connectivity_order_parameter_certificate"
    ] = all(certified_claims.values())

    return {
        "goal": "Goal 19: Algebraic Connectivity Order Parameter",
        "status": (
            "pass"
            if certified_claims[
                "goal19_algebraic_connectivity_order_parameter_certificate"
            ]
            else "fail"
        ),
        "order_parameter": {
            "name": "approximate recoverable observer algebra",
            "ingredients": (
                "relative-entropy response defects",
                "universal recovery fidelity lower bounds",
                "Pauli product/commutator closure defects",
                "static entropy shadow controls",
            ),
            "phase_rule": (
                "three stable noncommuting Pauli axes define quantum bridge; "
                "one stable commuting axis defines classical bridge; no stable "
                "axis defines null bridge; noncommuting response without the "
                "commutator axis is marked not a stable algebra."
            ),
        },
        "stability_theorem": theorem,
        "representative_noisy_bridges": examples,
        "response_only_no_go": {
            "statement": (
                "Axis-wise response alone is not an algebra.  At a coarse "
                "epsilon, a physical Pauli channel can preserve two noncommuting "
                "probe axes while failing to preserve their commutator axis; "
                "product/commutator closure is therefore part of the order parameter."
            ),
            "coarse_epsilon_bits": response_only_epsilon_bits,
            "witness": coarse_control,
        },
        "bounded_pauli_grid": grid,
        "simulation_signature": {
            "proposal": (
                "In a random-circuit, tensor-network, or quantum-simulator bridge, "
                "prepare full-rank antipodal probe pairs for noncommuting observer "
                "operators. Estimate relative-entropy response and product/commutator "
                "closure after the bridge channel. A quantum-to-classical-to-null "
                "connectivity transition is visible in algebraic response even when "
                "the maximally mixed/static entropy shadow is unchanged."
            ),
            "falsifiable_signal": (
                "Find two dynamics with the same coarse entropy/static shadow but "
                "different algebraic phases under the response-plus-closure order "
                "parameter."
            ),
        },
        "relationship_to_goal18": {
            "exact_limit": (
                "Goal 18 is the exact stabilizer local-screen case: all relevant "
                "logical Pauli response defects vanish and product/commutator "
                "closure is exact."
            ),
            "extension": (
                "Goal 19 lets response defects be nonzero and tracks whether the "
                "recoverable observer algebra remains quantum, collapses to a "
                "classical subalgebra, or becomes null."
            ),
        },
        "claim_boundary": (
            "This is a finite noisy Pauli-channel order-parameter theorem and "
            "certificate. It is not continuum ER=EPR, not de Sitter physics, and "
            "not a type-III algebra theorem. The next lift is a general "
            "finite-dimensional OA-QEC stability theorem beyond Pauli-diagonal "
            "bridges."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy algebraic-connectivity-order"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_algebraic_connectivity"
            ),
        },
        "certified_claims": certified_claims,
    }
