"""Emit finite controls for the algebra-type certification sprint.

The exact cylinder surrogate and entropy floor are analytic controls.  The
finite-prefix frontier is an exact finite-spectrum optimization up to ordinary
floating-point evaluation of elementary functions.  Its apparent asymptotic
rate is recorded only as a diagnostic, not as a proved theorem.
"""

from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path
from typing import Any

from qgtoy.finite_type_certification_control import (
    FiniteCertificationBudget,
    cylinder_type_i_surrogate_record,
    embezzlement_dimension_lower_bound,
    embezzlement_log_dimension_lower_bound,
    embezzlement_site_lower_bound,
    optimal_prefix_embezzlement_record,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "experiments" / "finite_type_certification_control_certificate.json"
)
SITE_COUNTS = (2, 4, 8, 16, 32, 64, 128, 256)
TARGET_DIMENSIONS = (2, 4, 8)
ERROR_TARGETS = (0.1, 0.05, 0.02)


def build_record() -> dict[str, Any]:
    budget = FiniteCertificationBudget(
        probe_dimension=4,
        channel_calls=8,
        energy_cap=16.0,
        duration=8.0,
        accessible_site_count=max(SITE_COUNTS),
        adaptive=True,
        output_metric="half_trace_distance",
    )
    frontiers: dict[str, list[dict[str, Any]]] = {}
    for target in TARGET_DIMENSIONS:
        records = []
        for sites in SITE_COUNTS:
            record = optimal_prefix_embezzlement_record(
                site_count=sites,
                target_dimension=target,
            )
            record["sqrt_site_scaled_error"] = (
                sqrt(sites) * record["optimal_half_trace_distance"]
            )
            records.append(record)
        frontiers[str(target)] = records

    dimension_floors = []
    for target in TARGET_DIMENSIONS:
        for error in ERROR_TARGETS:
            dimension_floors.append(
                {
                    "target_dimension": target,
                    "half_trace_distance": error,
                    "local_dimension_lower_bound": (
                        embezzlement_dimension_lower_bound(
                            target_dimension=target,
                            half_trace_distance=error,
                        )
                    ),
                    "log_local_dimension_lower_bound": (
                        embezzlement_log_dimension_lower_bound(
                            target_dimension=target,
                            half_trace_distance=error,
                        )
                    ),
                    "qubit_site_lower_bound": embezzlement_site_lower_bound(
                        target_dimension=target,
                        half_trace_distance=error,
                    ),
                }
            )

    return {
        "goal": "finite-resource operational certification of algebra type",
        "status": "control_pass_research_stop",
        "decision": "STOP_GENERIC_FINITE_CERTIFICATION_THEOREM",
        "protocol_budget_example": budget.as_record(),
        "exact_cylinder_surrogate": cylinder_type_i_surrogate_record(
            site_count=budget.accessible_site_count
        ),
        "entropy_continuity_dimension_floors": dimension_floors,
        "finite_prefix_embezzlement_frontiers": frontiers,
        "finite_checks": {
            "all_frontiers_improve_on_doubling_support": all(
                all(
                    left["optimal_half_trace_distance"]
                    > right["optimal_half_trace_distance"]
                    for left, right in zip(records, records[1:])
                )
                for records in frontiers.values()
            ),
            "larger_targets_are_harder_at_each_support": all(
                frontiers["2"][index]["optimal_half_trace_distance"]
                < frontiers["4"][index]["optimal_half_trace_distance"]
                < frontiers["8"][index]["optimal_half_trace_distance"]
                for index in range(len(SITE_COUNTS))
            ),
        },
        "observed_rate_diagnostic": (
            "for the checked prefixes, sqrt(n) times the optimal half trace "
            "distance approaches a target-dependent constant; no asymptotic "
            "rate theorem is claimed"
        ),
        "claim_boundary": (
            "the computation allows arbitrary local unitaries and prices no "
            "Hamiltonian energy, circuit complexity, spacetime support, or "
            "gravitational backreaction"
        ),
        "research_residual": (
            "derive a physical lower or upper bound on the resources needed "
            "to implement algebra-type witnesses in one named local model"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    record = build_record()
    args.output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(record["finite_checks"], sort_keys=True))
    print(record["decision"])


if __name__ == "__main__":
    main()
