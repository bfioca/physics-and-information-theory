#!/usr/bin/env python3
"""Build deterministic, revision-pinned external specialist review packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / "local_scalar_observer_review"
SOURCE_URL = (
    "https://github.com/bfioca/physics-and-information-theory/commit/{revision}"
)


@dataclass(frozen=True)
class Packet:
    slug: str
    label: str
    brief: str

    @property
    def files(self) -> tuple[str, ...]:
        return ("main.pdf", self.brief, "REVIEW_RESPONSE_FORM.md")


PACKETS = (
    Packet("detector-qft", "Relativistic detector/QFT", "QFT_NOVELTY_REVIEW.md"),
    Packet(
        "operator-theory",
        "Integral-operator/fractional-Sobolev",
        "OPERATOR_NOVELTY_REVIEW.md",
    ),
)


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _run_git(*args: str) -> str:
    result = subprocess.run(
        ("git", *args),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _revision_metadata(*, allow_dirty: bool) -> tuple[str, int]:
    dirty = _run_git("status", "--porcelain", "--untracked-files=no")
    if dirty and not allow_dirty:
        raise RuntimeError(
            "refusing to build a revision-pinned packet from a dirty checkout"
        )
    revision = _run_git("rev-parse", "--verify", "HEAD")
    commit_epoch = int(_run_git("show", "-s", "--format=%ct", revision))
    return revision, commit_epoch


def _zip_datetime(commit_epoch: int) -> tuple[int, int, int, int, int, int]:
    # ZIP timestamps begin in 1980 and store seconds at two-second precision.
    fields = list(time.gmtime(max(commit_epoch, 315532800))[:6])
    fields[-1] -= fields[-1] % 2
    return tuple(fields)  # type: ignore[return-value]


def _write_entry(
    archive: zipfile.ZipFile,
    name: str,
    payload: bytes,
    timestamp: tuple[int, int, int, int, int, int],
) -> None:
    info = zipfile.ZipInfo(name, date_time=timestamp)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    archive.writestr(info, payload)


def _read_verified_files(packet: Packet) -> dict[str, bytes]:
    manifest = json.loads((PACKAGE / "artifact_manifest.json").read_text("ascii"))
    frozen_hashes = manifest["files"]
    payloads: dict[str, bytes] = {}
    for relative in packet.files:
        payload = (PACKAGE / relative).read_bytes()
        expected = frozen_hashes.get(relative)
        if expected != _sha256(payload):
            raise RuntimeError(
                f"{relative} does not match its frozen artifact-manifest hash"
            )
        payloads[relative] = payload
    if not payloads["main.pdf"].startswith(b"%PDF-"):
        raise RuntimeError("main.pdf is not a valid PDF payload")
    return payloads


def _packet_readme(packet: Packet, revision: str) -> bytes:
    source_url = SOURCE_URL.format(revision=revision)
    text = f"""Independent Technical Novelty Review Packet

Domain: {packet.label}
Manuscript revision: {revision}
Frozen source: {source_url}

Please read main.pdf and {packet.brief}, then record a concise disposition in
REVIEW_RESPONSE_FORM.md. If the central result is known, please give a source
or equation-level reduction. If it is insufficient, please identify the
smallest bounded addition needed for a publishable short paper.

This is a request for critical technical review, not endorsement or approval.
Internal planning notes and repository history are intentionally excluded.
"""
    return text.encode("ascii")


def build_packet(
    packet: Packet,
    output_dir: Path,
    *,
    revision: str,
    commit_epoch: int,
) -> Path:
    """Build one deterministic review archive and return its path."""
    payloads = _read_verified_files(packet)
    readme = _packet_readme(packet, revision)
    file_hashes = {name: _sha256(payload) for name, payload in payloads.items()}
    file_hashes["PACKET_README.txt"] = _sha256(readme)
    commit_time = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime(commit_epoch),
    )
    manifest = {
        "schema_version": 1,
        "artifact": "final_support_thermal_dephasing_review_packet",
        "domain": packet.slug,
        "manuscript_revision": revision,
        "commit_time_utc": commit_time,
        "source_url": SOURCE_URL.format(revision=revision),
        "files_sha256": file_hashes,
        "disposition_required": [
            "KNOWN COROLLARY",
            "TECHNICALLY NEW BUT INSUFFICIENT",
            "SUITABLE SHORT-PAPER RESULT",
        ],
        "endorsement_requested": False,
    }
    manifest_payload = (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode("ascii")

    output_dir.mkdir(parents=True, exist_ok=True)
    short_revision = revision[:12]
    destination = output_dir / f"{packet.slug}-review-{short_revision}.zip"
    timestamp = _zip_datetime(commit_epoch)
    entries = {
        **payloads,
        "PACKET_README.txt": readme,
        "REVIEW_PACKET_MANIFEST.json": manifest_payload,
    }
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for name in sorted(entries):
            _write_entry(archive, name, entries[name], timestamp)
    return destination


def build_all(
    output_dir: Path,
    *,
    revision: str,
    commit_epoch: int,
) -> tuple[Path, ...]:
    return tuple(
        build_packet(
            packet,
            output_dir,
            revision=revision,
            commit_epoch=commit_epoch,
        )
        for packet in PACKETS
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="permit development builds whose Git revision does not freeze edits",
    )
    args = parser.parse_args()
    try:
        revision, commit_epoch = _revision_metadata(allow_dirty=args.allow_dirty)
    except RuntimeError as exc:
        parser.error(str(exc))
    built = build_all(
        args.output_dir,
        revision=revision,
        commit_epoch=commit_epoch,
    )
    result = {
        "status": "pass",
        "revision": revision,
        "packets": [
            {
                "path": str(path),
                "sha256": _sha256(path.read_bytes()),
            }
            for path in built
        ],
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
