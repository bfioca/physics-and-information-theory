# Centrifugal Conormal Interface Certificate

Status: exact structural certificate complete

Cellwise strong residual bounds are valid weak residual bounds only after
excluding delta distributions at internal interfaces. For the centrifugal
weak form the conormal is

```text
p=M(x,F,F')^T y+P(x,F,F')y'.
```

The authenticated sharp tube represents restrictions of one global `C1`
Skyrmion profile. The rational primal and adjoint archives are exactly `C1`,
including the regular-origin join. Consequently `(x,F,F',y,y')` has the same
one-sided value at every interface, and so does `p`. Every internal conormal
jump is identically zero.

This is a structural continuity argument. Adjacent interval ranges need not
overlap or be numerically equal because they enclose different whole-cell
ranges. Comparing those boxes would test the wrong statement.

The source-bound artifact replays both trials on the 344-cell eightfold
partition:

```text
python experiments/centrifugal_conormal_interface_audit.py
python -m pytest -q tests/test_centrifugal_conormal_interface_certificate.py \
  tests/test_centrifugal_conormal_interface_audit.py
```

Artifact: `experiments/centrifugal_conormal_interface_certificate.json`.

Claim boundary: this certificate removes internal interface distributions. It
does not reduce the bulk residual enclosure and does not certify the loaded
adjoint wall equation.
