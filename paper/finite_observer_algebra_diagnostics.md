# Screen Shadows Do Not Determine Finite Observer Algebras

## Abstract

We give a finite executable benchmark suite for observer-algebra diagnostics.
In the packaged static-patch regulator model, screen-visible data are identical
between a quantum matrix-algebra regulator and a dephased abelian control, while
intrinsic operator-response diagnostics distinguish the observer algebra. A
finite strong-continuity gate rules out instantaneous dephasing without assuming
off-diagonal response as an axiom. A cofinal full-matrix inclusion scaffold gives
a conditional hyperfinite Type `II_1` candidate path for the quantum sequence,
with an abelian dephased control carrying the same screen shadows. The result is
a finite diagnostic framework and code appendix, not a continuum de Sitter,
dS/CFT, or ER=EPR theorem.

## 1. Scope

This note extracts the publishable core from a larger research-code repository.
The goal is not to introduce a new definition of algebraic ER=EPR or to prove a
new theorem about continuum de Sitter quantum gravity. The goal is narrower:

```text
make an executable finite arena where screen-visible data provably fail to
determine the observer algebra, and record which additional operator-response
and continuity data repair the ambiguity.
```

Standard ingredients include finite matrix algebras, diagonal subalgebras,
Schur channels, stabilizer/QEC-style diagnostics, UHF inclusions, and
operator-algebraic reconstruction language. The contribution is the linked
finite benchmark and obstruction ledger.

## 2. Finite Observer Model

At cutoff `L`, let

```text
A_L = M_N,      S_L = C^N,      D_L = C^N.
```

Here `A_L` is the finite quantum observer algebra, `S_L` is the diagonal screen
algebra, and `D_L` is the dephased abelian control. The screen map is diagonal
restriction/dephasing. The finite static-patch regulators are CPTP/unital Schur
or semigroup channels acting on matrix units.

### Screen-Visible Diagnostics

For the packaged finite benchmark, a screen-visible diagnostic is a declared
functional of:

- the diagonal screen state `E_diag(rho)`;
- diagonal correlators;
- finite horizon-overlap counts;
- low-order screen-restricted transfer records.

Such diagnostics are not allowed to query off-diagonal matrix units,
commutators, or intrinsic operator-response probes. This finite class is a
benchmark definition, not a canonical continuum definition of a gravitational
screen.

### Operator-Visible Diagnostics

Operator-visible diagnostics may query:

- off-diagonal matrix-unit response;
- commutators such as `[e_12,e_21]`;
- relative/operator response under region channels;
- finite generator covariance under cutoff inclusions.

These are the diagnostics that distinguish `M_N` from `C^N` in the package.

## 3. Main Results

### Theorem 1: Screen-Shadow Collision

There are finite benchmark pairs in which the declared screen-visible
diagnostics agree levelwise, while the recoverable observer algebra differs as
`M_N` versus `C^N`.

The statement is implemented by the Goals 24-31 static-patch certificate stack.
It should be read as a formal insufficiency benchmark: diagonal/screen data
alone are not a complete observer-algebra invariant.

### Theorem 2: Strong-Continuity Gate

Let `Lambda_L(delta)=exp(delta G_L)` be an identity-starting finite semigroup
with `||G_L|| <= Gamma_L`. If `delta_L Gamma_L -> 0`, then

```text
||Lambda_L(delta_L)-id|| <= exp(delta_L Gamma_L)-1 -> 0.
```

This condition is anti-tautological: it does not mention `M_N`, `C^N`, bridge
algebra, or off-diagonal response. It excludes stationary modular twirling and
fixed-lapse thermalization as sufficient principles for preserving the finite
bridge diagnostic.

### Proposition 3: Cofinal Type-II Candidate Scaffold

Consecutive spherical cutoffs `N_L=(L+1)^2` do not form exact unital
full-matrix inductive systems because `N_L` does not divide `N_{L+1}` for
`L >= 1`. The cofinal factorial subsequence

```text
L_k=(k+1)!-1,    N_k=((k+1)!)^2
```

does admit trace-preserving full-matrix inclusions. The quantum sequence is a
UHF inductive limit whose tracial GNS closure is the hyperfinite Type `II_1`
factor by the standard trace-closure theorem. The dephased diagonal control
has the same levelwise screen shadows but an abelian von Neumann limit.

This is a conditional operator-algebra scaffold, not a canonical static-patch
cutoff construction.

### Audit 4: Inclusion-Covariant Dynamics

For the chosen rank-ordered block embedding, exact finite generator covariance
fails for raw fuzzy-sphere Hamiltonians. The weaker conditional-expectation
condition

```text
E_k G_{k+1} iota_k(x) ~= G_k(x)
```

has decreasing bounded errors along the audited factorial levels. The dephased
screen dynamics is exactly inclusion-covariant and abelian.

This audit isolates the remaining load-bearing assumption:
`rank_ordered_static_patch_embedding`.

## 4. Why The Benchmark Is Not Trivialized

A fair criticism is that diagonal probes cannot see off-diagonal structure by
construction. The point of the benchmark is to formalize that limitation in a
static-patch-like finite setting and to pair it with:

- a declared screen-shadow class;
- exact operator-response witnesses;
- KMS/detailed-balance counterexamples;
- a strong-continuity gate that is independent of the desired algebra split;
- a large-cutoff inclusion scaffold with an abelian control.

The claim is therefore not that the collision is physically surprising by
itself. The claim is that the benchmark gives a reproducible wind tunnel for
testing proposed screen/observer diagnostics.

## 5. Relation to Prior Art

The broad lesson that operator-algebraic structure matters is standard in
holographic QEC and algebraic ER=EPR discussions. The Type `II_1` static-patch
context is also an active continuum topic. This note does not claim those
conceptual banners. It supplies a finite, executable diagnostic layer under
them.

## 6. Open Problems

The main unresolved physical question is whether the current
`rank_ordered_static_patch_embedding` should be replaced by a more canonical
cutoff map:

- angular-momentum branching;
- coherent-state or Berezin-Toeplitz refinement;
- heat-kernel coarse graining;
- continuum `L^2(S^2)` projections;
- approximate inclusions rather than exact unital matrix inclusions.

A stronger paper would either derive the inclusion-covariant generator family
from such a canonical construction or prove a no-go for the present finite
regulator route.

## 7. Reproducibility

Focused package regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics
```

Compact certificate summary:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

Machine-readable package index:

```bash
python3 -m json.tool docs/static_patch_observer_algebra/audit_index.json
```

