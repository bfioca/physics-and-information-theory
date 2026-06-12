#!/usr/bin/env python3
"""Verify the checked Paper A manuscript and its proof dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zlib
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
MANIFEST = PACKAGE / "artifact_manifest.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_hashes(entries: dict[str, str], *, base: Path) -> list[str]:
    errors: list[str] = []
    for relative, expected in entries.items():
        path = base / relative
        if not path.is_file():
            errors.append(f"missing file: {path}")
            continue
        actual = _sha256(path)
        if actual != expected:
            errors.append(
                f"hash mismatch for {path}: expected {expected}, got {actual}"
            )
    return errors


def _json_payload_sha256(path: Path, excluded_keys: list[str]) -> str:
    payload = json.loads(path.read_text(encoding="ascii"))
    for key in excluded_keys:
        payload.pop(key, None)
    rendered = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")
    return hashlib.sha256(rendered).hexdigest()


def _mathematical_payload_audit(
    manifest: dict[str, object], replay_au2: Path | None
) -> tuple[list[str], str | None]:
    errors: list[str] = []
    replay_digest: str | None = None
    for relative, specification in manifest.get(
        "mathematical_payloads", {}
    ).items():
        path = ROOT / relative
        excluded = specification["excluded_top_level_keys"]
        expected = specification["sha256"]
        if not path.is_file():
            continue
        actual = _json_payload_sha256(path, excluded)
        if actual != expected:
            errors.append(
                f"mathematical payload mismatch for {path}: "
                f"expected {expected}, got {actual}"
            )
        if replay_au2 is not None and relative.endswith(
            "skyrmion_au2_global_tail_exact_certificate.json"
        ):
            if not replay_au2.is_file():
                errors.append(f"missing AU.2 replay: {replay_au2}")
            else:
                replay_digest = _json_payload_sha256(replay_au2, excluded)
                if replay_digest != expected:
                    errors.append(
                        f"AU.2 replay payload mismatch: expected {expected}, "
                        f"got {replay_digest}"
                    )
    return errors, replay_digest


def _source_audit() -> list[str]:
    errors: list[str] = []
    main = (PACKAGE / "main.tex").read_text(encoding="utf-8")
    inputs = re.findall(r"\\input\{([^}]+)\}", main)
    for relative in inputs:
        path = PACKAGE / f"{relative}.tex"
        if not path.is_file():
            errors.append(f"missing TeX input: {path}")

    tex_paths = [PACKAGE / "main.tex", *(PACKAGE / f"{item}.tex" for item in inputs)]
    source = "\n".join(path.read_text(encoding="utf-8") for path in tex_paths)
    source = re.sub(r"(?<!\\)%.*$", "", source, flags=re.MULTILINE)
    cited: set[str] = set()
    for group in re.findall(r"\\cite\{([^}]+)\}", source):
        cited.update(key.strip() for key in group.split(","))
    bibliography = (PACKAGE / "references.bib").read_text(encoding="utf-8")
    defined = set(re.findall(r"@[A-Za-z]+\{([^,]+),", bibliography))
    missing = sorted(cited - defined)
    if missing:
        errors.append(f"undefined bibliography keys: {', '.join(missing)}")

    labels = re.findall(r"\\label\{([^}]+)\}", source)
    duplicates = sorted({label for label in labels if labels.count(label) > 1})
    if duplicates:
        errors.append(f"duplicate labels: {', '.join(duplicates)}")
    referenced: set[str] = set()
    for group in re.findall(
        r"\\(?:ref|eqref|pageref|cref|Cref)\{([^}]+)\}", source
    ):
        referenced.update(key.strip() for key in group.split(","))
    missing_labels = sorted(referenced - set(labels))
    if missing_labels:
        errors.append(f"undefined labels: {', '.join(missing_labels)}")
    return errors


def _proof_source_audit(manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    proof_json = {
        **manifest["proof_certificates"],
        **manifest.get("proof_inputs", {}),
    }
    for relative in proof_json:
        certificate_path = ROOT / relative
        if not certificate_path.is_file():
            continue
        try:
            certificate = json.loads(certificate_path.read_text(encoding="ascii"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid proof JSON {certificate_path}: {exc}")
            continue
        source_hashes = certificate.get("source_sha256")
        if not isinstance(source_hashes, dict):
            errors.append(f"missing source_sha256 ledger: {certificate_path}")
            continue
        errors.extend(_require_hashes(source_hashes, base=ROOT))
    return errors


def _paper_claim_audit(
    manifest: dict[str, object],
) -> tuple[list[str], int]:
    """Link the displayed raw-transform bounds to the exact AU.2 payload."""

    errors: list[str] = []
    checks = manifest.get("claim_checks", {})
    relative = checks.get("au2_certificate")
    claimed = checks.get("numerator_derivative_upper_bounds", [])
    if not isinstance(relative, str) or not isinstance(claimed, list):
        return ["invalid claim_checks configuration"], 0
    path = ROOT / relative
    if not path.is_file():
        return [f"missing claim certificate: {path}"], 0
    try:
        payload = json.loads(path.read_text(encoding="ascii"))
        ledger = payload["exact_outputs"][
            "au2_global_derivative_norms_and_tail"
        ]["spectral_ledger"]
        tail = ledger["tail_envelope"]
        records = tail["numerator_derivative_coefficients"]
        wall_lower = Fraction(
            ledger["endpoint"]["wall_weight_second_derivative"]["lower"]
        )
        tail_start = Fraction(tail["tail_start"])
        bounds = [Fraction(value) for value in claimed]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [f"invalid claim certificate payload: {exc}"], 0
    if len(records) != len(bounds):
        errors.append(
            "raw-transform claim count mismatch: "
            f"certificate {len(records)}, manifest {len(bounds)}"
        )
    for index, (record, bound) in enumerate(zip(records, bounds)):
        try:
            upper = Fraction(record["upper"])
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"invalid raw-transform bound {index}: {exc}")
            continue
        if upper > bound:
            errors.append(
                f"raw-transform derivative {index} exceeds displayed bound: "
                f"{upper} > {bound}"
            )
    if wall_lower <= 0:
        errors.append("certified wall second derivative is not positive")
    if tail_start != 1:
        errors.append(f"raw-transform tail envelope starts at {tail_start}, not 1")
    return errors, len(bounds)


def _pdf_page_count(data: bytes) -> int | None:
    """Count page dictionaries, including those in Flate object streams."""

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


def _pdf_and_log_audit(manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    pdf = PACKAGE / "main.pdf"
    if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
        errors.append("main.pdf is missing or lacks a PDF signature")
    else:
        actual_pages = _pdf_page_count(pdf.read_bytes())
        expected_pages = int(manifest["page_count"])
        if actual_pages is None:
            errors.append("could not determine main.pdf page count")
        elif actual_pages != expected_pages:
            errors.append(
                f"page count mismatch: manifest {expected_pages}, PDF {actual_pages}"
            )

    log = PACKAGE / "main.log"
    if not log.is_file():
        errors.append("checked main.log is missing")
    else:
        text = log.read_text(encoding="utf-8", errors="replace")
        forbidden = (
            "Overfull \\hbox",
            "Underfull \\hbox",
            "undefined references",
            "Citation `",
        )
        for marker in forbidden:
            if marker.lower() in text.lower():
                errors.append(f"build log contains {marker!r}")
        match = re.search(r"Output written on main\.xdv \((\d+) pages", text)
        expected_pages = int(manifest["page_count"])
        if match is None:
            errors.append("checked main.log has no Tectonic page-count record")
        elif int(match.group(1)) != expected_pages:
            errors.append(
                f"page count mismatch: manifest {expected_pages}, log {match.group(1)}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replay-au2",
        type=Path,
        help=(
            "compare a regenerated AU.1/AU.2 JSON after excluding only the "
            "recorded command and dependency-version fields"
        ),
    )
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = _require_hashes(manifest["files"], base=PACKAGE)
    errors.extend(_require_hashes(manifest["proof_certificates"], base=ROOT))
    errors.extend(_require_hashes(manifest.get("proof_inputs", {}), base=ROOT))
    errors.extend(_proof_source_audit(manifest))
    claim_errors, checked_claim_bounds = _paper_claim_audit(manifest)
    errors.extend(claim_errors)
    payload_errors, replay_digest = _mathematical_payload_audit(
        manifest, args.replay_au2
    )
    errors.extend(payload_errors)
    errors.extend(_source_audit())
    errors.extend(_pdf_and_log_audit(manifest))
    report = {
        "artifact": manifest["artifact"],
        "status": "pass" if not errors else "fail",
        "checked_manuscript_files": len(manifest["files"]),
        "checked_proof_certificates": len(manifest["proof_certificates"]),
        "checked_proof_inputs": len(manifest.get("proof_inputs", {})),
        "checked_claim_bounds": checked_claim_bounds,
        "replay_au2_payload_sha256": replay_digest,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
