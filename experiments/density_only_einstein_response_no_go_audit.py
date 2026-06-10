#!/usr/bin/env python3
"""Write the exact Einstein-response input obstruction certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.density_only_einstein_response_no_go import (  # noqa: E402
    density_only_einstein_response_no_go_certificate,
)


OUTPUT = ROOT / "experiments/density_only_einstein_response_no_go_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/density_only_einstein_response_no_go_audit.py",
        ROOT / "qgtoy/density_only_einstein_response_no_go.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    record = density_only_einstein_response_no_go_certificate()
    record["source_sha256"] = starting_hashes
    if _source_hashes() != starting_hashes:
        raise ValueError("Einstein response no-go sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "result_type": record["result_type"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
