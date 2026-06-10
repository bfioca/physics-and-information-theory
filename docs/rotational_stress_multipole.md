# Leading Rotational Stress Multipole Theorem

Status: exact angular/state theorem for the quadratic collective hedgehog;
spin-two Einstein response and higher-order rotation open.

## State Tensor

For any rotational reference state define

```text
S_ab=<J_aJ_b+J_bJ_a>/2,
C=Tr(S)=<J^2>,
Q_ab=S_ab-delta_ab C/3.                               (1)
```

`S` is positive semidefinite. Therefore

```text
||Q||_op <= 2C/3,
||Q||_F <= sqrt(2/3) C.                               (2)
```

For a unit radial vector `n`, the exact fourth spherical moment gives

```text
<(nQn)^2>_S2=2||Q||_F^2/15,
RMS(nQn)<=2C/(3sqrt(5)).                              (3)
```

The bounds are asymptotically sharp. For the spin cat
`(|j,j>+|j,-j>)/sqrt(2)`, the quadrupole eigenvalues are

```text
[-j(2j-1)/6,-j(2j-1)/6,j(2j-1)/3],                  (4)
```

and `||Q||_op/C -> 2/3`.

## Hedgehog Stress Decomposition

At quadratic order in collective angular velocity, hedgehog covariance and the
local inertia projector give

```text
dE_rot/(dr dOmega)
 =3 i(r)/(16pi I^2) [C-n_a n_b S_ab]
 =3 i(r)/(16pi I^2) [2C/3-nQn].                     (5)
```

The first term is the spherical monopole already priced by the authenticated
gravity-to-Casimir theorem. The second is the complete leading spin-two energy
source. Since `int i(r)dr=I`, equations (2)-(3) imply

```text
||E_rot,l=2||_(radial L1, angular L1)
 <=3sqrt(2/15)||Q||_F/(4I)
 <= C/(2sqrt(5)I)
 = E_rot/sqrt(5).                                    (6)
```

Thus the nonspherical energy source is uniformly controlled by the same rotor
energy entering the monopole constraint. Converting (6) into a metric bound now
requires the norm of the static-patch `l=2` linearized Einstein response with
the correct pressure sources and boundary conditions.

## Anticoherent Escape

The pure spin-2 state

```text
|T>=(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2)                 (7)
```

has

```text
<J_a>=0,
S_ab=2delta_ab,
Q_ab=0,
F_Q=8 I_3.                                           (8)
```

It is second-order anticoherent: the local rotational QFI is full rank, while
the entire leading spin-two stress in (5) vanishes. Its finite stabilizer still
leaves global orientation ambiguities, so (8) is not by itself an arbitrarily
accurate global frame.

This is a genuine escape route from an overly broad no-go. Accurate rotational
references do not universally require nonzero leading quadrupolar gravity. The
paper must split its theorem:

1. on the `Q=0` branch, the spherical monopole gravity theorem survives through
   quadratic collective order;
2. on the all-state branch, equation (6) supplies the source norm and an `l=2`
   Einstein-response bound is required;
3. neither branch yet controls `Omega^4`, collective projection, the membrane,
   or off-center support.

## Reproduction

```bash
python experiments/rotational_stress_multipole_audit.py
python -m pytest -q tests/test_rotational_stress_multipole.py \
  tests/test_rotational_stress_multipole_audit.py
```

Artifact:

```text
experiments/rotational_stress_multipole_exact_certificate.json
SHA256 13bfaa681377caef32875a03f9a5c313e7fecb4f17cde5c2e191a8f8810fe07e
```

Primary context:

- [Goldberg and James, quantum-limited Euler-angle measurements with
  anticoherent states](https://arxiv.org/abs/1806.02355).
- [Baguette and Martin, anticoherence measures for pure spin
  states](https://arxiv.org/abs/1707.01246).
