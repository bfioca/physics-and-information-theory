# Skyrmion Radial Dynamical Gap Gate

Status: authenticated full regular-origin-to-fixed-wall `l=0` gap proved; the
spherical moving membrane is proved separately, while anchor and nonspherical
complement channels remain open

## Radial Quadratic Action

Set `x=e f_pi r` and `tau=e f_pi t`. For a time-dependent spherically
symmetric hedgehog `F(tau,x)`, the declared two- and four-derivative Skyrme
action reduces to

```text
S_radial = (4 pi/e^2) integral d tau dx
           [u(F,x) dot(F)^2/(8N)-N u(F,x) F'^2/8-V(F,x)],
u=x^2+8sin^2(F),  N=1-lambda x^2.                       (1)
```

The dot is a `tau` derivative. There is no separate `dot(F)^2 F'^2` term:
the temporal and radial currents are parallel in isospace, while the
angular-time Skyrme commutators supply the `8sin^2(F)` contribution to `u`.

Linearize about a static profile `F_0`. The coefficient variation of the
kinetic term is cubic because the background has `dot(F_0)=0`. The quadratic
normal-mode equation is therefore

```text
L_Jacobi eta = omega_hat^2 W eta,
W(x)=[x^2+8sin^2(F_0)]/N(x),                            (2)
```

where `L_Jacobi=-(P eta')'+Q eta` is the same static Jacobi differential
expression used by the BVP analysis, with `P=N(x^2+8sin^2F_0)`.
The corresponding static-patch Killing frequency is
`omega_K=e f_pi omega_hat`.

## Hard-Support Conversion

For `0<=x<=x_w` and `N_w=1-lambda x_w^2>0`,

```text
0<=W(x)<=(x_w^2+8)/N_w=:W_max.                         (3)
```

Hence, if the Jacobi quadratic form satisfies

```text
<eta,L_Jacobi eta> >= alpha ||eta||_2^2                (4)
```

on the complete physical radial fluctuation domain, the generalized Rayleigh
quotient gives

```text
omega_hat_0^2 >= alpha/W_max
              = alpha N_w/(x_w^2+8).                   (5)
```

This closes the kinetic-weight conversion exactly. A static form gap alone
would not suffice without (3): `L=alpha I`, `W=C I` has the same static gap for
every `C`, while `omega^2=alpha/C->0`.

## What AU.1 Does And Does Not Prove

AU.1 certifies a Barta lower bound greater than

```text
alpha_AU1=1.0235900944571767
```

for the exact rational approximate-profile Jacobi operator on `[1/16,4]` with
Dirichlet conditions at both endpoints. It separately treats the singular
origin family and an augmented endpoint/Schur system to prove existence and
local uniqueness of an exact static hard-wall profile in a Newton tube.

By itself, that original evidence does not establish equation (4) on the
physical origin-to-wall fluctuation form domain:

- the Barta mesh begins at the positive cutoff `x=1/16`, where it imposes an
  artificial Dirichlet condition;
- the physical regular radial fluctuation has an origin condition inherited
  from `F(t,0)=pi`, namely `eta(0)=0` and `eta=O(x)`, and generally has
  `eta(1/16)!=0`;
- the augmented origin machinery is an inverse-function/BVP construction, not
  a Rayleigh-form gluing theorem; and
- the positive Barta quotient must be propagated from the rational center
  profile through every exact-solution jet in the Newton tube; and
- the wall is fixed in the profile BVP, whereas the supported observer has a
  dynamical membrane and ultimately an anchor.

Eliminating the physical origin interval would produce a spectral-parameter
dependent Dirichlet-to-Neumann condition at `x=1/16`. The static shooting
tangent and Schur complement supply only its zero-parameter analogue.

For the default `x_w=4`, `lambda=0.0025`, one has `N_w=0.96` and `W_max=25`.
Equation (5) does give a rigorous corollary for AU.1's artificially truncated,
approximate-profile Dirichlet operator:

```text
omega_hat_D^2 >= 0.04094360377828707,
omega_hat_D   >= 0.202345258845....                     (6)
```

Using only AU.1's declared target `alpha>=1` gives the memorable truncated
result `omega_hat_D>=1/5`. The successor certificate below proves the same
clean bound on the physical fixed-wall domain.

## Exact-Solution Full-Domain Closure

The authenticated successor consumes the pinned AU.2 archive and sharp Newton
recipe without modifying either. On `[1/16,4]` it restricts the exact center
polynomials adaptively, reapplies the endpoint correction, adds the local
Newton `C0,C1,C2` radii, and evaluates the same positive Barta witness. It
closes on 109 leaves at maximum binary depth 5, with

```text
inf_[1/16,4] (L_Jacobi v)/v > 1.0386099769.             (7)
```

On `[0,1/16]`, it writes `pi-F=xu(x^2)` and eliminates `F''` with the exact
profile equation. This cancellation-preserving representation contains no
inverse powers of `x` and gives

```text
inf_[0,1/16] (L_Jacobi v)/v > 36.8298881657.            (8)
```

For physical regular modes, `eta=O(x)` and `P=O(x^2)`, so the origin boundary
term in the ground-state transform is `O(x^4)` and vanishes. The wall term
vanishes because `eta(4)=0`. Equations (7)-(8) therefore prove

```text
<eta,L_Jacobi eta> >= ||eta||_2^2,
omega_hat_rad^2 >= 1/25,
omega_hat_rad >= 1/5,
omega_K >= e f_pi/5.                                   (9)
```

The exact certificate SHA256 is
`695310609d070f6dba2c678982ffc87472ed7c341813137fb90ad9dd9e1e6096`.

## Remaining Closure

Equation (9) closes only the fixed-wall `l=0` profile mode. The coupled membrane
radial degree of freedom requires a matrix Sturm-Liouville/boundary-mass
problem, and nonspherical/anchor modes remain separate inputs to the full-band
Feshbach theorem.

## Reproduction

```bash
PYTHONPATH=. python -m qgtoy skyrmion-radial-dynamical-gap
PYTHONPATH=. python experiments/skyrmion_full_radial_gap_audit.py
python -m pytest -q tests/test_skyrmion_radial_dynamical_gap.py
python -m pytest -q tests/test_validated_skyrmion_radial_gap.py
```

Artifacts:

- `qgtoy/skyrmion_radial_dynamical_gap.py`
- `qgtoy/validated_skyrmion_radial_gap.py`
- `tests/test_skyrmion_radial_dynamical_gap.py`
- `tests/test_validated_skyrmion_radial_gap.py`
- `experiments/skyrmion_full_radial_gap_exact_certificate.json`
