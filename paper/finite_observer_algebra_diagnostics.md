# Screen Shadows Do Not Determine Finite Observer Algebras

## Abstract

This note extracts a focused result from the accompanying executable
certificate suite. We study finite static-patch-inspired observer models with a
matrix observer algebra `M_N`, a diagonal screen algebra `C^N`, and a dephased
abelian control. For a declared class of screen-visible diagnostics, the
quantum model and the abelian control have identical screen shadows, while
intrinsic operator response distinguishes their observer algebras. We then
record three stabilizing structures: a cutoff-compatible strong-continuity gate
that excludes instantaneous dephasing, a finite-to-Type-`II_1` scaffold via
cofinal matrix inclusions, and a consecutive-cutoff UCP refinement with
multiplicativity error `1/N`. Finally, we formulate a conditional
continuum-lift obstruction: any proposed static-patch or dS/CFT dictionary that
factors only through convergent screen shadows is incomplete whenever an
operator-response witness persists.

This is a finite benchmark note with reproducible code. It is not a continuum
de Sitter theorem, not a dS/CFT construction, and not a proof of ER=EPR in de
Sitter.

## 1. Scope and Claim Boundary

The central claim is deliberately finite:

```text
screen-visible finite diagnostics do not determine the observer algebra;
operator-response, continuity, and embedding data are needed.
```

The standard background includes finite matrix algebras, diagonal subalgebras,
Schur channels, finite stabilizer/OA-QEC-style diagnostics, UHF inclusions, and
operator-algebraic reconstruction language. The contribution is not a new
definition of holography or algebraic ER=EPR. It is a linked finite benchmark
and obstruction ledger designed to make a common pitfall executable: a
screen-only diagnostic can miss the noncommutative observer algebra.

The results below are separated into four claim categories:

- **Exact finite theorem:** a statement about the finite objects defined here.
- **Bounded certificate:** a checked finite family or implementation-backed
  audit.
- **Conditional lift theorem schema:** a theorem form that becomes
  continuum-relevant only if stated lift conditions are supplied.
- **Continuum speculation:** motivation only; not claimed as proved here.

## 2. Finite Observer Model

Fix a cutoff `L` and let `N=N_L`. The finite benchmark compares:

```text
A_L = M_N,        S_L = C^N,        D_L = C^N.
```

Here `A_L` is the quantum observer algebra, `S_L` is the diagonal screen
algebra, and `D_L` is the dephased abelian control. Let

```text
E_diag : M_N -> C^N
```

be the diagonal conditional expectation in a chosen screen basis.

### Definition 2.1: Screen Shadows

For this benchmark, a screen-visible diagnostic is any declared finite
functional that factors through diagonal screen data:

- the diagonal state `E_diag(rho)`;
- diagonal correlators;
- finite horizon-overlap counts;
- low-order screen-restricted transfer records.

Equivalently, if two finite models have the same diagonal expectation data and
the same declared low-order screen-transfer records, every diagnostic in the
screen-shadow class gives the same value on them. This is a finite benchmark
definition, not a canonical continuum definition of a gravitational screen.

### Definition 2.2: Operator-Response Witnesses

An operator-response diagnostic may query non-diagonal algebraic structure, for
example:

- off-diagonal matrix units `e_ij`;
- commutators such as `[e_12,e_21]`;
- relative/operator response under a channel;
- generator covariance under cutoff refinement maps.

The basic response witness used below is:

```text
[e_12,e_21] = e_11 - e_22.
```

Its operator norm is `1` inside `M_N`, while every commutator vanishes inside
the abelian control `C^N`.

## 3. Main Results

### Theorem 3.1: Screen-Shadow Collision

For every `N >= 2`, the quantum observer algebra `M_N` and the dephased abelian
control `C^N` have identical screen shadows for all diagnostics that factor
through `E_diag`, but their observer algebras are not isomorphic and are
separated by the commutator witness `[e_12,e_21]`.

**Proof sketch.** The screen algebra in both cases is the same diagonal algebra
`C^N`. Any screen-shadow diagnostic is, by definition, a function only of the
diagonal state, diagonal correlators, and declared screen-restricted transfer
records. Those data are matched by construction after applying `E_diag`.
However, `M_N` is noncommutative for `N >= 2`, while `C^N` is abelian. In
`M_N`, the matrix units satisfy `[e_12,e_21]=e_11-e_22`, whose operator norm is
`1`. In `C^N`, all commutators are zero. Thus the screen shadow agrees while
the observer algebra and intrinsic operator response differ. QED.

The finite certificates extend this elementary collision across the packaged
static-patch regulator stack: screen entropy, diagonal correlator,
horizon-overlap, and screen-restricted transfer data are held fixed while
off-diagonal response distinguishes `M_N` from `C^N`.

### Proposition 3.2: Finite Schur and Derived Dynamics Preserve the Split

The finite static-patch regulator channels used in the package are CPTP/unital
Schur or random-unitary channels that preserve the diagonal screen shadow and
act nontrivially on off-diagonal matrix units. Within the audited finite
regulator class, the screen-shadow collision and operator-response separation
persist.

**Proof sketch.** A Schur multiplier with positive semidefinite kernel and unit
diagonal is completely positive and unital; because it fixes diagonal matrix
units, it preserves the declared diagonal screen data. Finite phase-kick
dilations give random-unitary Schur channels by averaging phases over a finite
environment, so they are CPTP. The dephased control erases off-diagonal matrix
units, while the quantum regulator retains a controlled off-diagonal response
inside the declared finite family. The code certificates check the corresponding
positivity, trace-preservation, diagonal-shadow, and response fields for the
bounded regulator stack. QED.

This proposition is a finite benchmark claim. It does not derive a continuum
static-patch Hamiltonian or path integral.

### Theorem 3.3: Strong-Continuity Gate

Let `Lambda_L(delta)=exp(delta G_L)` be an identity-starting finite semigroup
and suppose `||G_L|| <= Gamma_L`. If `delta_L Gamma_L -> 0`, then

```text
||Lambda_L(delta_L)-I|| <= exp(delta_L Gamma_L)-1 -> 0.
```

Thus cutoff-compatible strong continuity rules out abrupt dephasing routes
without naming `M_N`, `C^N`, or off-diagonal response as an axiom.

**Proof.** Use the exponential series:

```text
exp(delta G)-I = sum_{r>=1} (delta G)^r/r!.
```

Taking operator norm and using submultiplicativity gives

```text
||exp(delta G)-I||
 <= sum_{r>=1} (delta ||G||)^r/r!
 <= exp(delta Gamma)-1.
```

If `delta_L Gamma_L -> 0`, the right-hand side tends to zero. Stationary
twirling or complete dephasing fails this gate because it jumps by norm one on
an off-diagonal matrix unit, for example `e_12`. Fixed-lapse thermalization is
not enough by itself unless the product `delta_L Gamma_L` vanishes. QED.

### Proposition 3.4: Cofinal Type-`II_1` Scaffold

Consecutive spherical cutoffs

```text
N_L=(L+1)^2
```

do not generally admit unital full-matrix `*-homomorphisms`
`M_{N_L} -> M_{N_{L+1}}`, because such a map exists only when
`N_L` divides `N_{L+1}`. The cofinal factorial subsequence

```text
L_k=(k+1)!-1,        N_k=((k+1)!)^2
```

does admit trace-preserving full-matrix inclusions by amplification. The
resulting quantum inductive limit is a UHF algebra whose tracial GNS closure is
the hyperfinite Type `II_1` factor by the standard UHF trace-closure theorem.
The dephased diagonal sequence has the same levelwise screen shadows and an
abelian von Neumann limit.

**Proof sketch.** A unital `*-homomorphism` `M_n -> M_m` exists exactly when
`m=nr`; it is then conjugate to `A -> A tensor I_r`. For consecutive cutoffs,
`(L+1)^2` does not divide `(L+2)^2` for `L>=1`, so exact full-matrix inclusions
fail. On the factorial subsequence, `N_{k+1}/N_k=(k+2)^2`, so the amplification
map exists and preserves the normalized trace. The diagonal control splits each
screen atom into equal subatoms, preserving diagonal trace data. The UHF/trace
closure statement is standard operator-algebra input; the finite certificate
does not claim it is the canonical de Sitter static-patch algebra. QED.

### Proposition 3.5: Consecutive UCP Cutoff Refinement

Exact full-matrix inclusions are too rigid for consecutive cutoffs, but
consecutive cutoffs admit a unital completely positive trace-preserving
refinement with controlled multiplicativity error. For `n <= m`, choose an
isometry `V:C^n -> C^m`, let `P=VV^*`, let `Q=I_m-P`, and define

```text
Phi(A)=V A V^* + tau_n(A) Q.
```

Then `Phi` is unital, completely positive, and normalized-trace preserving.
For `A=e_12` and `B=e_21`,

```text
||Phi(AB)-Phi(A)Phi(B)|| = 1/n.
```

For static-patch dimensions `n=N_L=(L+1)^2`, the error tends to zero.

**Proof.** Unitality follows from

```text
Phi(I_n)=P+Q=I_m.
```

Complete positivity follows because `A -> VAV^*` is completely positive and
`A -> tau_n(A)Q` is the tensor product of a positive functional with a positive
operator. For normalized traces,

```text
tau_m(Phi(A))
 = (Tr_n(A) + tau_n(A)(m-n))/m
 = Tr_n(A)/n
 = tau_n(A).
```

For `A=e_12`, `B=e_21`, one has `AB=e_11`, `tau_n(A)=tau_n(B)=0`, and
`tau_n(e_11)=1/n`. Therefore

```text
Phi(AB)-Phi(A)Phi(B) = (1/n)Q,
```

whose operator norm is `1/n` when `m>n`. The off-diagonal matrix units remain
visible in the embedded corner, so the commutator witness persists there while
the dephased control remains abelian. QED.

This is not a canonical fuzzy-sphere embedding. It is a finite replacement for
the divisibility obstruction and a test harness for more physical approximate
embeddings, such as harmonic projection or Berezin-Toeplitz refinement.

### Theorem Schema 3.6: Continuum Lift Obstruction

Suppose two finite regulator sequences satisfy the following lift conditions:

1. embedding or coarse-graining maps between cutoffs;
2. trace/state convergence;
3. screen-shadow convergence;
4. strong-continuity or generator control;
5. persistence of an operator-response witness;
6. compatibility with the proposed limiting observer algebra.

If their limiting screen shadows agree but their limiting response witnesses
differ, then no dictionary that factors only through the limiting screen shadow
can determine the observer algebra.

**Proof sketch.** Let `D` be a dictionary that factors through the screen
shadow. If two sequences have identical limiting screen shadows, `D` assigns
them the same output. If an operator-response witness has a nonzero limiting
gap, the two limiting observer-algebra candidates are distinguishable by
operator response. Therefore `D` cannot be a complete invariant of the
observer algebra. QED.

This is a proof-ready conditional obstruction theorem under explicit lift
hypotheses. It is the continuum-facing lesson of the finite benchmark, not a
construction of the continuum theory.

## 4. Why This Is Not Trivialized By Diagonal Blindness

The finite collision is intentionally sharp: screen shadows are diagonal or
screen-restricted, while the response witness is noncommutative. A skeptical
reader may say that diagonal probes cannot see off-diagonal structure. That is
true, and it is the point of the benchmark.

The nontrivial part is the package surrounding that elementary observation:

- the screen-shadow class is declared explicitly;
- the response witness is algebraic and exact;
- KMS/detailed-balance-looking conditions are separated from strong continuity;
- finite derived dynamics and regulator-class certificates preserve the split;
- exact cofinal inclusions and approximate consecutive UCP refinements are both
  audited;
- the continuum-lift obstruction states what any screen-only dictionary would
  fail to see under explicit lift assumptions.

The result is best read as a calibration rig for proposed observer/screen
dictionaries.

## 5. Related Work and Positioning

Operator-algebra quantum error correction is the natural finite language for
reconstructable observable algebras; see Beny, Kempf, and Kribs,
*Quantum Error Correction of Observables* (arXiv:0705.1574). Holographic QEC
and subalgebra reconstruction enter through Almheiri, Dong, and Harlow,
*Bulk Locality and Quantum Error Correction in AdS/CFT* (arXiv:1411.7041), and
Harlow, *The Ryu-Takayanagi Formula from Quantum Error Correction*
(arXiv:1607.03901).

The algebraic ER=EPR motivation is due to Engelhardt and Liu,
*Algebraic ER=EPR and Complexity Transfer* (arXiv:2311.04281). This note does
not claim that slogan; it supplies finite operational benchmarks under the same
lesson that algebraic structure matters beyond entanglement amount.

The static-patch Type-II motivation is anchored by Chandrasekaran, Longo,
Penington, and Witten, *An Algebra of Observables for de Sitter Space*
(arXiv:2206.10780). Approximate matrix-algebra/fuzzy-sphere convergence is
motivated by Rieffel's work on matrix algebras converging to the sphere in
quantum Gromov-Hausdorff distance (arXiv:math/0108005). The present UCP
refinement is only a finite benchmark gadget; it is not asserted to be the
canonical Berezin-Toeplitz or static-patch refinement.

## 6. Limitations

The note does not prove:

- a continuum de Sitter observer-algebra theorem;
- a dS/CFT dictionary;
- literal ER=EPR in de Sitter;
- that the factorial subsequence is physically canonical;
- that the trace-filled UCP map is the correct fuzzy-sphere refinement;
- approximate QEC stability in a Type-II or Type-III limit.

The next mathematical target is to replace the trace-filled UCP refinement with
a more physical harmonic, heat-kernel, or Berezin-Toeplitz cutoff map and rerun
the screen-shadow, response, continuity, and covariance tests.

## Appendix A: Reproducibility

Run the focused package regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics tests.test_embedding_channels tests.test_continuum_lift_obstruction tests.test_lift_diagnostics
```

Run the compact certificate summary:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

Emit the lead certificates:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy static-patch-embedding-channels --max-cutoff 5
PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5
```

Validate machine-readable indexes:

```bash
python3 -m json.tool docs/static_patch_observer_algebra/audit_index.json
python3 -m json.tool docs/static_patch_embedding_channels_certificate_index.json
python3 -m json.tool docs/continuum_lift_obstruction_certificate_index.json
```
