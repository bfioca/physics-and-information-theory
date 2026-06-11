import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper" / "spacelike_replication" / "main.tex"
BIBLIOGRAPHY = ROOT / "paper" / "spacelike_replication" / "references.bib"


def _comma_separated_keys(matches):
    return {
        key.strip()
        for match in matches
        for key in match.split(",")
        if key.strip()
    }


def test_spacelike_replication_manuscript_references_are_closed():
    source = MANUSCRIPT.read_text(encoding="ascii")
    bibliography = BIBLIOGRAPHY.read_text(encoding="ascii")

    labels = re.findall(r"\\label\{([^}]+)\}", source)
    assert len(labels) == len(set(labels))

    referenced_labels = _comma_separated_keys(
        re.findall(r"\\(?:c|C)?ref\{([^}]+)\}", source)
    )
    assert referenced_labels <= set(labels)

    citation_keys = _comma_separated_keys(
        re.findall(r"\\cite\{([^}]+)\}", source)
    )
    bibliography_keys = set(
        re.findall(r"@[A-Za-z]+\{([^,]+),", bibliography)
    )
    assert citation_keys <= bibliography_keys

    assert "Paper U" not in source
    assert "TODO" not in source
    assert "\\begin{document}" in source
    assert "\\end{document}" in source

    environment_tokens = re.findall(r"\\(begin|end)\{([^}]+)\}", source)
    environment_stack = []
    for action, environment in environment_tokens:
        if action == "begin":
            environment_stack.append(environment)
        else:
            assert environment_stack
            assert environment_stack.pop() == environment
    assert not environment_stack

    assert "NOVELTY STOP" in source
    assert "Janssens' Lemma~1" in source
