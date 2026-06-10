# Global Orientation Risk From State Stabilizers

Status: exact all-measurement theorem; explicit `Q=0` branch audited

## Theorem

Let the unknown orientation `g in SO(3)` have normalized Haar prior and let

```text
rho_g=U(g)rho U(g)^*.
```

Suppose a rotation `h` of principal angle `alpha in [0,pi]` stabilizes the
reference density operator:

```text
U(h)rho U(h)^*=rho.
```

Then every measurement and estimator, for the chordal frame cost

```text
c(x)=sin^2(theta(x)/2)=(3-Tr R(x))/4,
```

obeys

```text
R_ref >= sin^2(alpha/4).                         (1)
```

The statement is global. It does not use local unbiasedness, quantum Fisher
information, a spin cutoff, or a particular POVM.

## Proof

The stabilizer identity gives `rho_g=rho_(gh)`, hence the same conditional
measurement law for the paired hypotheses `g` and `gh`. Right invariance of
Haar measure therefore gives

```text
R_ref
 = (1/2) integral dg dy p(y|g)
     [c(g_hat(y)^-1 g)+c(g_hat(y)^-1 g h)]
 >= (1/2) min_(x in SO(3)) [c(x)+c(xh)].          (2)
```

If `H=R(h)`, then

```text
c(X)+c(XH)=[6-Tr X(I+H)]/4.
```

The singular values of `I+H` are

```text
2, 2 cos(alpha/2), 2 cos(alpha/2).
```

The orientation-preserving Procrustes maximum is consequently
`2+4cos(alpha/2)`. Substitution into (2) gives

```text
(1/2) min_x[c(x)+c(xh)]
 = (1/2)[1-cos(alpha/2)]
 = sin^2(alpha/4),
```

which proves (1).

## Anticoherent Example

The pure spin-2 state used in the leading stress-multipole theorem is

```text
|psi>=(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2).
```

It occupies only `m=-2,0,2`. A rotation by `pi` around the quantization axis
therefore acts with phase `exp(-i m pi)=1` on every occupied component. Equation
(1) gives the exact global floor

```text
R_ref >= sin^2(pi/4)=1/2.                        (3)
```

This state simultaneously has

```text
<J>=0,
Q=0,
F_Q=8 I_3,
R_ref>=1/2.
```

Thus full-rank local QFI and vanishing leading spin-two stress do not make this
state a globally accurate orientation reference. The earlier `Q=0` result is a
local gravitational escape branch, not yet an operational escape from the
universal observer tradeoff.

## Claim Boundary

Equation (1) only uses an exact stabilizer. It does not exclude:

- `Q=0` states with trivial stabilizer;
- families whose largest stabilizer angle tends to zero;
- cross-spin superpositions whose global orbit becomes asymptotically free; or
- a different operational task defined on the quotient `SO(3)/H`.

The correct next test for the isotropic branch is therefore constructive:
determine whether a sequence with `Q=0`, vanishing global `SO(3)` risk, bounded
support, and controlled higher-order stress exists. The explicit spin-2 state
cannot serve as that sequence.

## Reproduction

```bash
python experiments/orientation_stabilizer_risk_audit.py
python -m pytest -q tests/test_orientation_stabilizer_risk.py \
  tests/test_orientation_stabilizer_risk_audit.py
```

Artifact:

```text
experiments/orientation_stabilizer_risk_exact_certificate.json
SHA256 5043d84e063051e8b730612a096b57dcafda2b30b7614facb0ac95003ff5f54b
```
