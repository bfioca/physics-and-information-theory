# Collective-Band Feshbach Gate

Status: exact operator transfer theorem and insufficiency witness; spherical
profile-membrane radial channels are certified, while anchor/nonspherical gaps
and off-band couplings remain unproved

## Sector Decomposition

In a fixed rotational sector, let `P` project onto the proposed collective band
and `Q=1-P`. Write the full self-adjoint Hamiltonian as

```text
H = [ A   B^* ]
    [ B    D  ].
```

Suppose the quadratic forms obey

```text
A>=a,
D>=d,
||B||<=v.                                               (1)
```

For a normalized vector with component norms `p=||P psi||` and `q=||Q psi||`,

```text
<H> >= a p^2+d q^2-2v p q.
```

Minimizing over `p^2+q^2=1` gives the exact scalar comparison

```text
epsilon_full >= lambda_-(a,d,v)
 = [a+d-sqrt((d-a)^2+4v^2)]/2.                         (2)
```

This does not require finite-dimensional bands. It is a quadratic-form theorem
provided the off-diagonal block is bounded in the stated norm.

## Fractional Transfer

If `d>=a+Delta` with `Delta>0`, the Schur estimate gives

```text
epsilon_full >= a-v^2/Delta.                           (3)
```

Therefore the sector floor transfers at a uniform fraction whenever

```text
v^2 <= eta Delta a,   0<=eta<1:
epsilon_full >= (1-eta)a.                              (4)
```

Applied to the supported Skyrmion collective theorem,

```text
a_j=sqrt[3N_w j(j+1)/2]/a_support,
```

equation (4) preserves the linear high-spin growth and hence the finite
rotational partition function. This is the precise band-completeness condition
needed by UO.2Q.

An equivalent scale-uniform form is often more natural. If

```text
d_j>=gamma a_j,  v_j<=rho a_j,  rho^2<gamma,
```

then

```text
epsilon_j^full>=kappa(gamma,rho)a_j,
kappa=[1+gamma-sqrt((1-gamma)^2+4rho^2)]/2>0.           (4a)
```

The threshold `rho^2=gamma` collapses the transferred fraction exactly.

## Projection Leakage

For a normalized eigenstate with eigenvalue `E<d`, the `Q` block equation gives

```text
||Q psi|| <= [v/(d-E)] ||P psi||,
||Q psi||^2 <= r^2/(1+r^2),  r=v/(d-E).                (5)
```

The same gap and coupling data thus control both energy-floor transfer and the
collective-band projection error required by the current/current and readout
lemmas.

## Why Current Static Certificates Are Insufficient

Knowing `A>=a` alone does not control the full floor. For any `0<delta<=1`, the
positive two-band Hamiltonian

```text
H_delta = [ a              (1-delta)a ]
          [ (1-delta)a      a           ]              (6)
```

has exactly the same collective block `PHP=aP`, but eigenvalues

```text
delta a,  (2-delta)a.
```

Thus the full floor can be an arbitrarily small fraction of the collective
floor without changing any fixed-profile collective mass or inertia datum.

Even growing diagonal blocks are insufficient without a coupling estimate.
For `A_j>Delta>0`, choose

```text
H_j = [ A_j    b_j ],  b_j^2=(A_j-Delta)(2A_j-Delta).
      [ b_j   2A_j ]
```

Both diagonal floors grow with `A_j`, but the exact eigenvalues are `Delta` and
`3A_j-Delta`. The full rotational partition function therefore still diverges
if `Delta` is fixed.

The analogous classical one-mode completion is

```text
L=-M-Delta q^2/2+(I_0+bq)Omega^2/2.
```

Eliminating `q` produces

```text
J_4=b^2/(2Delta).
```

As `Delta->0`, quartic control fails while the static point `q=0`, its mass,
and its leading inertia remain unchanged. This is why a static radial BVP
certificate cannot be silently reused as a dynamical collective-band gap.

## Repository Evidence Audit

The repository currently proves:

- the profile-uniform supported hedgehog collective floor;
- exact fixed-profile projective representation kinematics;
- static radial BVP existence and uniqueness, plus authenticated exact-solution
  full-domain `l=0` floors `omega_hat_rad>=1/5` for the fixed wall and
  `omega_hat_rad>=1/50` for the spherical moving membrane;
- an exact branch-coordinate comparison that could sharpen the conservative
  moving-membrane floor; and
- conditional centered radial wall curvature evidence.

It does not currently prove:

- a quantum collective projector `P_j` and compression inequality
  `P_jH_jP_j>=a_jP_j`; the existing nonlinear hedgehog-family infimum is not
  by itself a linear-subspace compression theorem;
- the anchor and nonspherical sectors of the coupled time-dependent Hessian;
- a positive complement gap after removing rotational zero modes in every
  grand-spin channel;
- a norm bound on `QHP_j` uniform in spin;
- a Feshbach remainder or collective-band spectral projector;
- survival of spin-isospin locking and the right multiplicity register after
  projection; or
- a renormalized quantum Hamiltonian/domain statement for the full field
  theory.

The existing AU.2/AU.3 “spectral” certificates concern the bath form factor and
its frequency derivatives. They are not fluctuation-spectrum bounds for the
Skyrmion Hamiltonian.

## Required Physical Certificate

A full-band Skyrmion certificate should provide, sector by sector,

```text
a quantum projector P_j, a_j, Delta_j, v_j,
v_j^2/(Delta_j a_j) <= eta < 1,                         (7)
```

with directed errors and a common spin range. The spherical membrane radial
mode is now certified; the full result must add anchor and nonspherical modes,
remove exact rotational zero modes, and state the norm/domain in which `v_j` is
controlled. Equations (2), (4), and (5) then automatically
produce the full sector floor, partition bound, and projection-error budget.

Until (7) is supplied, the collective theorem is a rigorous enabling lemma and
the counterexample (6) blocks promotion to a full-field observer theorem.

## Reproduction

```bash
PYTHONPATH=. python -m qgtoy collective-band-feshbach
python -m pytest -q tests/test_collective_band_feshbach.py
```

Artifacts:

- `qgtoy/collective_band_feshbach.py`
- `tests/test_collective_band_feshbach.py`
