# Conditional Localized SO(3) Observer Tradeoff

Status: exact elimination theorem inside a declared composite branch; open
windows are necessary-only; one-action Skyrmion realization remains open

## Purpose

This theorem is the first explicit composition of orientation accuracy,
proper localization, a compactness/backreaction margin, optical support, and
coherence in the repository. It combines three exact inputs:

1. the global `SO(3)` chordal-risk theorem;
2. the marked spherical-top compactness capacity; and
3. the equal-shell hard-current optical support bounds.

Reference-only isotropic heat diffusion supplies the coherence condition. The
inputs are exact in their own declared models but do not yet follow from one
microscopic action. Therefore failure is a conditional no-go, while success is
only a compatibility result.

## Accuracy Forces Proper Size

For target risk `0<epsilon<3/4`, the direct global theorem gives the necessary
Casimir capacity

```text
C_req(epsilon)=max{0,[epsilon^-1-8]/16}.       (1)
```

The marked spherical top obeys

```text
Cbar<=A_comp a^4,
A_comp=kappa chi^2 zeta/[2G^2(1+zeta)^2].     (2)
```

Hence every reference in this branch with `R_ref<=epsilon` must satisfy

```text
a>=a_min(epsilon)
  =[C_req(epsilon)/A_comp]^(1/4).              (3)
```

For `epsilon<1/8`, equation (3) is a nonzero lower bound. It applies to
arbitrary rotor states, not only a definite-spin or canonical Peter-Weyl token.

## Optical Support Ceilings

For target spin `L`, the hard-current theorem supplies generic and
dipole-cancelled optical angular-support ceilings, plus equal-worldtube
nonoverlap. The exact static-slice conversion

```text
d_prop(theta)=2R asin[cos(rho/R) sin(theta/2)]
```

turns each into a proper radius ceiling `a_max^(design)(L)`. A design is
immediately excluded when

```text
a_min(epsilon)>a_max^(design)(L).              (4)
```

The generic and dipole-cancelled ceilings are sufficient designs inherited
from the hard-current approximation, not universal bounds over all local
couplings.

## Coherence Ceiling

At a given radius ceiling, insert the largest compactness-compatible Casimir
into both global risk bounds and retain the stronger initial floor `r_0`. Under
reference-only rotational heat diffusion,

```text
R_ref(T)>=3/4[1-exp(-2 gamma T)]+r_0 exp(-2 gamma T).  (5)
```

Maintaining risk at most `epsilon<3/4` therefore requires

```text
gamma T<=1/2 log[(3/4-r_0)/(3/4-epsilon)].    (6)
```

Equations (3), (4), and (6) are evaluated together for each optical design.

## Logical Interpretation

For each design, the certificate reports:

- whether the proper-radius interval is nonempty;
- whether the stronger of the Casimir and mean-spin/asymmetry risk floors fits
  under `epsilon`; and
- whether the requested protocol duration fits below the exact heat coherence
  ceiling.

If any condition fails, that design is excluded inside the declared
spherical-top, hard-current, and reference-heat branch. If every condition
passes, the inequalities are compatible, but a physical observer has not yet
been constructed. Stress support, switching, finite-memory error, and the
diffusion rate must still be derived from the same action.

## Audit Example

The deterministic certificate uses `L=2`, `epsilon=0.1`, `R=1`, `G=10^-12`,
`kappa=2/3`, `chi=1/2`, and `zeta=1/4`. At `gamma T=10^-4`, all three sampled
designs retain necessary windows. At `gamma T=10`, equation (5) puts every
design at risk approximately `0.75`, so all are excluded. The positive case is
only a code-path audit; it is not a phenomenological parameter claim.

## Paper Role

This closes UO.5 for one explicit composite model class. It clarifies the next
physics task: replace the compositional assumptions with quantities derived
from the supported Skyrmion/KMS action. Poor AU.3 or lifetime constants can now
be inserted into a theorem with a definite failure criterion rather than
reported as an isolated numerical disappointment.

## Reproduction

```bash
PYTHONPATH=. python3 -m unittest tests.test_localized_so3_observer_tradeoff
```

Artifacts:

- `qgtoy/localized_so3_observer_tradeoff.py`
- `tests/test_localized_so3_observer_tradeoff.py`
- `docs/global_so3_reference_risk.md`
- `docs/static_patch_hard_current_multipole.md`
- `docs/finite_size_static_patch_observer.md`
