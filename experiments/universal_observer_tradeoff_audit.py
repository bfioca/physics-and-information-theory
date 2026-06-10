"""Write the source-hashed conditional universal observer-tradeoff audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qgtoy.localized_orbital_reference import (
    confined_orbital_observer_tradeoff_record,
)
from qgtoy.universal_observer_tradeoff import (
    conditional_observer_tradeoff_record,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/universal_observer_tradeoff_certificate.json"
SOURCES = (
    "qgtoy/universal_observer_tradeoff.py",
    "qgtoy/localized_orbital_reference.py",
    "qgtoy/global_so3_reference_risk.py",
    "experiments/universal_observer_tradeoff_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    compatible = conditional_observer_tradeoff_record(
        mean_casimir_capacity=2.0,
        risk_budget=0.2,
        rotational_noise_exposure=0.1,
        capacity_model="abstract proved C2 capacity",
        localization_model="abstract proved proper-support ceiling",
    )
    capacity_excluded = conditional_observer_tradeoff_record(
        mean_casimir_capacity=0.0,
        risk_budget=0.1,
        rotational_noise_exposure=0.0,
        capacity_model="zero-capacity diagnostic",
        localization_model="irrelevant for zero capacity",
    )
    orbital_excluded = confined_orbital_observer_tradeoff_record(
        maximum_proper_support_radius=0.1,
        risk_budget=0.2,
        newton_constant=0.01,
        compactness_margin=0.2,
        rotational_noise_exposure=0.1,
    )
    claims = {
        "generic_composition_has_compatible_example": compatible[
            "necessary_conditions_compatible"
        ],
        "zero_capacity_target_is_excluded": capacity_excluded[
            "declared_class_excluded"
        ],
        "confined_orbital_support_ceiling_is_excluded": orbital_excluded[
            "declared_class_excluded"
        ],
        "orbital_radius_floor_exceeds_ceiling": (
            orbital_excluded["minimum_required_proper_support_radius"]
            > orbital_excluded["maximum_proper_support_radius"]
        ),
    }
    return {
        "goal": "Conditional Class-Uniform Observer Tradeoff",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "orientation_capacity_localization_heat_composition",
        "certified_claims": claims,
        "generic_compatible_case": compatible,
        "generic_capacity_excluded_case": capacity_excluded,
        "confined_orbital_excluded_case": orbital_excluded,
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "claim_boundary": (
            "The composition and confined-orbital corollary are proved. The "
            "audit does not derive a relativistic capacity, optical support "
            "map, nonzero physical noise exposure, or metric-backreaction "
            "margin from one action."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
