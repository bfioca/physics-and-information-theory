import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "local_scalar_observer_cost"
MAIN = PAPER / "main.tex"
BIBLIOGRAPHY = PAPER / "references.bib"
SECTIONS = tuple(sorted((PAPER / "sections").glob("*.tex")))
REVIEW_DOCUMENTS = (
    ROOT / "REVIEWER_README.md",
    ROOT / "README.md",
    ROOT / "REPRODUCIBILITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "THEOREMS.md",
    ROOT / "paper" / "README.md",
    ROOT / "docs" / "README.md",
    PAPER / "README.md",
    PAPER / "REFEREE_GUIDE.md",
    PAPER / "QFT_NOVELTY_REVIEW.md",
    PAPER / "OPERATOR_NOVELTY_REVIEW.md",
    PAPER / "EXTERNAL_REVIEW_LAUNCH.md",
    PAPER / "REVIEW_RESPONSE_FORM.md",
    PAPER / "PRIORITY_AUDIT.md",
    PAPER / "REVIEWER_SHORTLIST.md",
    ROOT / "docs" / "local_scalar_observer_cost.md",
    ROOT / "docs" / "local_scalar_observer_proof_audit.md",
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


def _markdown_link_targets(text: str) -> list[str]:
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    return re.findall(r"\[[^]]+\]\(([^)]+)\)", prose)


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
    assert "ER=EPR" not in text
    assert "does not include the stress" in text
    assert "F(y)" in text
    assert "Sharp Final-Support Field--Energy Bounds" in text
    assert "\\mathcal C_\\beta(L)=2L\\Lambda(\\pi L/\\beta)" in text
    assert "Sharpness refers to the optimization over final Cauchy data" in text
    assert "Causal source-cylinder envelope" in text
    assert text.index("\\appendix") < text.index(
        "\\section{Final-slice Einstein--scalar application}"
    )
    assert "HarlowUsatyukZhao2025" in citation_keys
    assert {
        "AnoopJohnson2025",
        "AsplingLawler2023",
        "JohnsonVerma2026",
        "Kozlowski2008",
        "Polosin2022",
        "Widom2006",
    } <= citation_keys
    assert "Wiener--Hopf term minus" in text
    assert "finite-interval logarithmic convolution" in text
    assert "geodesic compression of the hyperbolic logarithmic Green" in text
    assert "\\norm{r_\\tau}\\leq(\\pi\\tau)^{-1}" in text
    assert "\\leq\\frac\\beta3" in text
    assert "\\leq\\frac{2\\pi}{3}" in text
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
        for target in _markdown_link_targets(text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (document.parent / target.split("#", 1)[0]).resolve()
            assert resolved.exists(), f"broken link in {document}: {target}"

    reviewer_text = REVIEW_DOCUMENTS[0].read_text(encoding="ascii")
    assert "C_beta(L)=2 L Lambda(pi L/beta)" in reviewer_text
    assert "SUBMIT" in reviewer_text
    assert "STRENGTHEN" in reviewer_text
    assert "NO-GO" in reviewer_text
    assert "not endorsement or approval" in reviewer_text
    assert "one manuscript" in reviewer_text

    root_readme = (ROOT / "README.md").read_text(encoding="ascii")
    assert "GO to external review; HOLD submission" in root_readme
    assert "Earlier Paper A" not in root_readme
    assert "Current Branch Result" not in root_readme
    assert "Historical Repository Context" not in root_readme

    launch_text = (PAPER / "EXTERNAL_REVIEW_LAUNCH.md").read_text(
        encoding="ascii"
    )
    assert "does not substitute" in launch_text
    assert "Harlow Framing Email Draft" in launch_text
    assert "build_review_packets.py" in launch_text
    assert "byte-for-byte deterministic" in launch_text
    assert "Silence or a polite general reaction does not close a gate" in launch_text

    response_text = (PAPER / "REVIEW_RESPONSE_FORM.md").read_text(
        encoding="ascii"
    )
    assert "KNOWN COROLLARY" in response_text
    assert "TECHNICALLY NEW BUT INSUFFICIENT" in response_text
    assert "Submission Acceptance Rule" in response_text
    assert "every central claim" in response_text
    assert "marked `NOT REVIEWED` by every" in response_text
    assert "Neither answer grants permission to imply endorsement" in response_text

    priority_text = (PAPER / "PRIORITY_AUDIT.md").read_text(encoding="ascii")
    assert "The vacuum parent problem is established prior art" in priority_text
    assert "Finite temperature: odd log-sinh convolution sector" in priority_text
    assert "STRENGTHEN, external gate open" in priority_text

    shortlist_text = (PAPER / "REVIEWER_SHORTLIST.md").read_text(
        encoding="ascii"
    )
    assert "First route: Andre G. S. Landulfo" in shortlist_text
    assert "First route: A. A. Polosin" in shortlist_text
    assert "does not replace either domain review" in shortlist_text

    proof_audit = (ROOT / "docs" / "local_scalar_observer_proof_audit.md").read_text(
        encoding="ascii"
    )
    assert "Adversarial Follow-Up: 2026-06-23" in proof_audit
    assert "Checks Requiring External Sign-Off" in proof_audit
    assert "Remaining Independent Checks" not in proof_audit
    assert "No missing factor" in proof_audit
    assert "of two was found" in proof_audit
    assert "||r_tau||<=pi/(6 tau)" in proof_audit
    assert "does not replace either external specialist disposition" in proof_audit
