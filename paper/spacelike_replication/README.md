# Spacelike-Replication Manuscript

This directory contains the frozen Track 2 methods-note source. The proposed
central theorem failed its priority gate because it follows directly from an
established UCP/joint-measurement noise inequality. The mathematics remains
useful internally, but this directory is not a submission package.

Files:

- `main.tex` - frozen methods-note source;
- `references.bib` - primary-source bibliography.

For internal rendering, the intended build is:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Run it from this directory. A TeX toolchain is not bundled with the repository,
so source and theorem verification can pass even when PDF compilation is not
available locally. Do not call this note attachment-ready or present it as a
new theorem paper.

The authoritative scientific gates are in
`../../docs/spacelike_replication_manuscript_goal.md` and
`../../docs/spacelike_replication_qec_reduction_audit.md`.
