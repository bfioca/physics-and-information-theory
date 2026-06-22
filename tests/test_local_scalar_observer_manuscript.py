import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "local_scalar_observer_cost"
MAIN = PAPER / "main.tex"
BIBLIOGRAPHY = PAPER / "references.bib"
SECTIONS = tuple(sorted((PAPER / "sections").glob("*.tex")))
REVIEW_DOCUMENTS = (
    ROOT / "REVIEWER_README.md",
    PAPER / "README.md",
    PAPER / "REFEREE_GUIDE.md",
)
ALLOWED_CONTROL_BYTES = {9, 10, 13}


def _assert_plain_ascii(path: Path) -> None:
    payload = path.read_bytes()
    payload.decode("ascii")
    assert not {
        byte for byte in payload if byte < 32 and byte not in ALLOWED_CONTROL_BYTES
    }


def _comma_separated_keys(matches):
    return {
        key.strip()
        for match in matches
        for key in match.split(",")
        if key.strip()
    }


def test_local_scalar_observer_manuscript_is_structurally_closed() -> None:
    sources = (MAIN, *SECTIONS)
    text = "\n".join(path.read_text(encoding="ascii") for path in sources)
    bibliography = BIBLIOGRAPHY.read_text(encoding="ascii")

    labels = re.findall(r"\\label\{([^}]+)\}", text)
    assert len(labels) == len(set(labels))

    referenced_labels = _comma_separated_keys(
        re.findall(r"\\(?:c|C)?ref\{([^}]+)\}", text)
    )
    assert referenced_labels <= set(labels)

    citation_keys = _comma_separated_keys(
        re.findall(r"\\cite\{([^}]+)\}", text)
    )
    bibliography_keys = set(
        re.findall(r"@[A-Za-z]+\{([^,]+),", bibliography)
    )
    assert citation_keys <= bibliography_keys

    for source in (*sources, BIBLIOGRAPHY):
        _assert_plain_ascii(source)

    assert "TODO" not in text
    assert "ER=EPR" in text
    assert "not include the material" in text
    assert "F(y)" in text
    assert "HarlowUsatyukZhao2025" in citation_keys
    assert "not their closed-universe encoding error" in text
    assert "strictly positive quadratic form" in text
    assert "observer_cost_spectrum.pdf" in text
    assert "numerical evidence rather than an additional rigorous lower bound" in text
    assert "time-symmetric Einstein--scalar" not in text
    assert "y=L/R,quad" not in text
    assert "THEOREM CANDIDATE PASS" not in text
    assert "\\begin{document}" in text
    assert "\\end{document}" in text

    for source in sources:
        environment_tokens = re.findall(
            r"\\(begin|end)\{([^}]+)\}",
            source.read_text(encoding="ascii"),
        )
        environment_stack = []
        for action, environment in environment_tokens:
            if action == "begin":
                environment_stack.append(environment)
            else:
                assert environment_stack
                assert environment_stack.pop() == environment
        assert not environment_stack


def test_local_scalar_observer_review_packet_is_navigable() -> None:
    for document in REVIEW_DOCUMENTS:
        text = document.read_text(encoding="ascii")
        _assert_plain_ascii(document)
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (document.parent / target.split("#", 1)[0]).resolve()
            assert resolved.exists(), f"broken link in {document}: {target}"

    reviewer_text = REVIEW_DOCUMENTS[0].read_text(encoding="ascii")
    assert "NARROW PAPER GO" in reviewer_text
    assert "STRENGTHEN" in reviewer_text
    assert "NO-GO" in reviewer_text
    assert "not endorsement or approval" in reviewer_text
    assert "not part of this review packet" in reviewer_text
