import hashlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
BUILDER = (
    ROOT
    / "paper"
    / "local_scalar_observer_cost"
    / "build_review_packets.py"
)
SPEC = importlib.util.spec_from_file_location("observer_review_packets", BUILDER)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_revision_metadata_refuses_dirty_checkout(monkeypatch) -> None:
    monkeypatch.setattr(
        MODULE,
        "_run_git",
        lambda *args: " M main.pdf" if args[0] == "status" else "",
    )
    with pytest.raises(RuntimeError, match="dirty checkout"):
        MODULE._revision_metadata(allow_dirty=False)


def test_review_packets_are_minimal_pinned_and_reproducible(tmp_path: Path) -> None:
    revision = "0123456789abcdef0123456789abcdef01234567"
    commit_epoch = 1_767_225_600
    first = MODULE.build_all(
        tmp_path / "first",
        revision=revision,
        commit_epoch=commit_epoch,
    )
    second = MODULE.build_all(
        tmp_path / "second",
        revision=revision,
        commit_epoch=commit_epoch,
    )

    assert [path.name for path in first] == [path.name for path in second]
    assert [_sha256(path) for path in first] == [_sha256(path) for path in second]

    expected_briefs = {
        "detector-qft": "QFT_NOVELTY_REVIEW.md",
        "operator-theory": "OPERATOR_NOVELTY_REVIEW.md",
        "observer-code": "OBSERVER_CODE_REVIEW.md",
    }
    for archive_path in first:
        domain = next(
            key for key in expected_briefs if archive_path.name.startswith(key)
        )
        brief = expected_briefs[domain]
        expected_names = {
            "main.pdf",
            brief,
            "REVIEW_RESPONSE_FORM.md",
            "PACKET_README.txt",
            "REVIEW_PACKET_MANIFEST.json",
        }
        with zipfile.ZipFile(archive_path) as archive:
            assert set(archive.namelist()) == expected_names
            assert archive.read("main.pdf").startswith(b"%PDF-")
            assert b"NOT REVIEWED is not interpreted" in archive.read(
                "PACKET_README.txt"
            )
            assert b"Submission Acceptance Rule" in archive.read(
                "REVIEW_RESPONSE_FORM.md"
            )
            assert "PRIORITY_AUDIT.md" not in archive.namelist()
            assert "REVIEWER_SHORTLIST.md" not in archive.namelist()
            manifest = json.loads(archive.read("REVIEW_PACKET_MANIFEST.json"))
            assert manifest["domain"] == domain
            assert manifest["artifact"] == (
                "finite_pointer_observer_entropy_review_packet"
            )
            assert manifest["manuscript_revision"] == revision
            assert manifest["endorsement_requested"] is False
            for name, expected_hash in manifest["files_sha256"].items():
                assert hashlib.sha256(archive.read(name)).hexdigest() == expected_hash
            assert len({entry.date_time for entry in archive.infolist()}) == 1
