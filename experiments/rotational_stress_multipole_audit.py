#!/usr/bin/env python3
"""Write the exact leading rotational stress-multipole certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.rotational_stress_multipole import (  # noqa: E402
    rotational_stress_multipole_certificate,
)


OUTPUT = ROOT / "experiments/rotational_stress_multipole_exact_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/rotational_stress_multipole_audit.py",
        ROOT / "qgtoy/rotational_stress_multipole.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    record = rotational_stress_multipole_certificate()
    record["source_sha256"] = starting_hashes
    if _source_hashes() != starting_hashes:
        raise ValueError("rotational stress source changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "universal_spin_two_energy_ratio": record[
                    "cat_integrated_spin_two_energy"
                ]["universal_ratio_upper_bound"],
                "anticoherent_spin_two_energy_vanishes": record[
                    "anticoherent_integrated_spin_two_energy"
                ]["leading_spin_two_energy_vanishes"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
