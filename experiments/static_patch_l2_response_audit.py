#!/usr/bin/env python3
"""Write the fixed-de Sitter static quadrupole response certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.static_patch_l2_response import (  # noqa: E402
    static_patch_l2_response_certificate,
)


OUTPUT = ROOT / "experiments/static_patch_l2_response_exact_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/static_patch_l2_response_audit.py",
        ROOT / "qgtoy/static_patch_l2_response.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    record = static_patch_l2_response_certificate()
    record["source_sha256"] = starting_hashes
    if _source_hashes() != starting_hashes:
        raise ValueError("static-patch l=2 response sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "inverse_operator_norm": record["coercive_response"][
                    "inverse_operator_norm_upper_bound"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
