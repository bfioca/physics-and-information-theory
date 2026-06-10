# Exact Conormal Origin-Transfer Scaffold

The centrifugal quadrupole equations are regular singular at the Skyrmion
origin. Directly differentiating the strong equations would require
derivatives of the validated profile remainder. The conormal formulation
avoids that loss.

Write the weak-form density in coordinate, mixed, and principal blocks
`C`, `M`, and `P`, with source coefficients `s0` and `s1`. Define

```text
a=y/x,
p=P y' + M^T y - s1,
z=p/x^2,
t=x^2,
X=(a,z).
```

For `C=Cbar(t)`, `M=x Mbar(t)`, `P=x^2 Pbar(t)`,
`s0=x shat0(t)`, and `s1=x^2 shat1(t)`, exact algebra gives

```text
2t X_t=A(t)X+q(t),

A11=-Pbar^-1(Pbar+Mbar^T),   A12=Pbar^-1,
A21=Cbar-Mbar Pbar^-1 Mbar^T,
A22=Mbar Pbar^-1-2I,

q1=Pbar^-1 shat1,
q2=Mbar Pbar^-1 shat1-shat0.
```

The physical rotational source is more regular than the generic scaling:
`s0=O(x^3)` and `s1=O(x^4)`. This is the conormal statement behind the
log-free forced cubic branch.

## Leading Theorem

At `t=0`, exact rational-function algebra in the origin slope proves the four
distinct eigenvalues

```text
spec A(0)={0,2,-3,-5}.
```

They correspond to the physical powers `{1,3,-2,-4}` after `a=y/x`. The
constant-Fuchs Green operator for a remainder beginning at degree three is

```text
G H(t)=(1/2) sum_lambda Pi_lambda
        integral_0^1 s^((6-lambda)/2-1) H(st) ds,
```

where each `Pi_lambda` is the exact Lagrange polynomial in `A(0)`. In the
declared weighted infinity norm

```text
weights=(36/25,73/50,13/20,73/100),
||X||_w=max_i |X_i|/weights_i,
```

a 128-cell exact rational enclosure of the authenticated slope interval gives

```text
||G||_w < 0.44950 < 9/20.
```

The exact field recurrence through `x^5` is exported as two homogeneous
endpoint columns plus one forced affine column. The correlation is preserved;
no interval Robin inversion is formed.

## Next Certificate

For `X=X_c+t^3R`, the desired fixed-point estimate is

```text
R=G[(A-A0)R-e],
gamma delta < 1,
gamma epsilon + gamma delta Rmax <= Rmax,
```

with `delta=sup||A-A0||_w` and `epsilon=sup||e||_w`. The repository now has
the validated quintic profile family needed to compute these two quantities,
but it does not yet have their Taylor-model enclosures. In particular, the
current scaffold does not claim that the conormal residual is divisible by
`t^3` on the full profile tube.

## Reproduce

```bash
PYTHONPATH=. python experiments/validated_centrifugal_origin_transfer_audit.py
python -m pytest -q tests/test_validated_centrifugal_origin_transfer.py tests/test_validated_centrifugal_origin_transfer_audit.py
```

## Claim Boundary

This is an exact conormal identity, leading spectral decomposition, Green
majorant, and formal affine endpoint-germ theorem. It is not yet a finite-cell
field transfer, Friedrichs-domain equivalence, global continuum inverse, or
validated nonzero response.
