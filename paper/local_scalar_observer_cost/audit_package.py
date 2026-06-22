#!/usr/bin/env python3
"""Verify the checked local scalar manuscript and theorem certificate."""

from __future__ import annotations

import hashlib
import json
import re
import zlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
MANIFEST = PACKAGE / "artifact_manifest.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_hashes(entries: dict[str, str], *, base: Path) -> list[str]:
    errors: list[str] = []
    for relative, expected in entries.items():
        path = base / relative
        if not path.is_file():
            errors.append(f"missing file: {path}")
        elif (actual := _sha256(path)) != expected:
            errors.append(
                f"hash mismatch for {path}: expected {expected}, got {actual}"
            )
    return errors


def _source_audit() -> list[str]:
    errors: list[str] = []
    main = (PACKAGE / "main.tex").read_text(encoding="ascii")
    inputs = re.findall(r"\\input\{([^}]+)\}", main)
    paths = [PACKAGE / "main.tex"]
    for item in inputs:
        path = PACKAGE / f"{item}.tex"
        if not path.is_file():
            errors.append(f"missing TeX input: {path}")
        else:
            paths.append(path)
    text = "\n".join(path.read_text(encoding="ascii") for path in paths)
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    if len(labels) != len(set(labels)):
        errors.append("duplicate TeX labels")
    references = {
        key.strip()
        for group in re.findall(r"\\(?:c|C)?ref\{([^}]+)\}", text)
        for key in group.split(",")
    }
    missing_labels = sorted(references - set(labels))
    if missing_labels:
        errors.append(f"undefined labels: {', '.join(missing_labels)}")
    citations = {
        key.strip()
        for group in re.findall(r"\\cite\{([^}]+)\}", text)
        for key in group.split(",")
    }
    bibliography = (PACKAGE / "references.bib").read_text(encoding="ascii")
    bibliography_keys = set(re.findall(r"@[A-Za-z]+\{([^,]+),", bibliography))
    missing_citations = sorted(citations - bibliography_keys)
    if missing_citations:
        errors.append(f"undefined citations: {', '.join(missing_citations)}")
    return errors


def _pdf_page_count(data: bytes) -> int | None:
    expanded = bytearray(data)
    for marker in re.finditer(rb"stream\r?\n", data):
        header = data[max(0, marker.start() - 512) : marker.start()]
        if b"/FlateDecode" not in header:
            continue
        end = data.find(b"endstream", marker.end())
        if end < 0:
            continue
        payload = data[marker.end() : end].rstrip(b"\r\n")
        try:
            expanded.extend(zlib.decompress(payload))
        except zlib.error:
            continue
    count = len(re.findall(rb"/Type\s*/Page(?!s)\b", bytes(expanded)))
    return count or None


def _build_audit(manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    pdf = PACKAGE / "main.pdf"
    if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
        errors.append("main.pdf is missing or invalid")
    elif _pdf_page_count(pdf.read_bytes()) != manifest["page_count"]:
        errors.append("PDF page count does not match manifest")
    log = PACKAGE / "main.log"
    if not log.is_file():
        errors.append("main.log is missing")
    else:
        text = log.read_text(encoding="utf-8", errors="replace")
        forbidden = (
            "Overfull \\hbox",
            "Underfull \\hbox",
            "undefined references",
            "Citation `",
        )
        errors.extend(
            f"build log contains {marker!r}"
            for marker in forbidden
            if marker.lower() in text.lower()
        )
        expected = int(manifest["page_count"])
        if f"Output written on main.xdv ({expected} pages" not in text:
            errors.append("build log page count does not match manifest")
    return errors


def _certificate_audit(manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    path = ROOT / str(manifest["certificate"])
    try:
        record = json.loads(path.read_text(encoding="ascii"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"invalid theorem certificate: {exc}"]
    if record.get("status") != "sharp_theorem_pass_paper_novelty_open":
        errors.append("theorem certificate does not have the expected status")
    if not all(record.get("certified_claims", {}).values()):
        errors.append("one or more theorem certificate claims failed")
    source_hashes = record.get("source_sha256")
    if not isinstance(source_hashes, dict):
        errors.append("certificate has no source_sha256 ledger")
    else:
        errors.extend(_check_hashes(source_hashes, base=ROOT))
    return errors


def _numerical_audit() -> list[str]:
    errors: list[str] = []
    path = PACKAGE / "data/observer_cost_spectrum.json"
    try:
        record = json.loads(path.read_text(encoding="ascii"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"invalid numerical spectrum record: {exc}"]
    if record.get("status") != "numerical_convergence_pass_nonrigorous":
        errors.append("numerical spectrum does not have the expected status")
    checks = record.get("checks")
    if not isinstance(checks, dict):
        errors.append("numerical spectrum has no checks")
    else:
        boolean_checks = (
            "all_curve_estimates_inside_rigorous_bracket",
            "all_profile_components_positive",
            "nested_resolution_estimates_monotone",
        )
        errors.extend(
            f"numerical spectrum check failed: {key}"
            for key in boolean_checks
            if checks.get(key) is not True
        )
    source_hashes = record.get("source_sha256")
    if not isinstance(source_hashes, dict):
        errors.append("numerical spectrum has no source_sha256 ledger")
    else:
        errors.extend(_check_hashes(source_hashes, base=ROOT))
    figure = record.get("figure")
    if not isinstance(figure, dict):
        errors.append("numerical spectrum has no figure ledger")
    else:
        relative = figure.get("path")
        expected = figure.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected, str):
            errors.append("numerical spectrum figure ledger is invalid")
        else:
            errors.extend(_check_hashes({relative: expected}, base=ROOT))
        preview_relative = figure.get("preview_path")
        preview_expected = figure.get("preview_sha256")
        if not isinstance(preview_relative, str) or not isinstance(
            preview_expected,
            str,
        ):
            errors.append("numerical spectrum preview ledger is invalid")
        else:
            errors.extend(
                _check_hashes({preview_relative: preview_expected}, base=ROOT)
            )
    return errors


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
    errors = _check_hashes(manifest["files"], base=PACKAGE)
    errors.extend(
        _check_hashes(
            {str(manifest["certificate"]): str(manifest["certificate_sha256"])},
            base=ROOT,
        )
    )
    errors.extend(_source_audit())
    errors.extend(_build_audit(manifest))
    errors.extend(_certificate_audit(manifest))
    errors.extend(_numerical_audit())
    result = {
        "artifact": manifest["artifact"],
        "status": "pass" if not errors else "fail",
        "page_count": manifest["page_count"],
        "checked_files": len(manifest["files"]),
        "errors": errors,
        "novelty_boundary": (
            "This package audit verifies provenance and internal closure; "
            "standalone novelty remains an external specialist-review gate."
        ),
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
