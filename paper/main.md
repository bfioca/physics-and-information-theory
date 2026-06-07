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
cofinal matrix inclusions, and a consecutive-cutoff embedding audit comparing
a trace-filled UCP baseline with harmonic, heat-kernel, and
Berezin-Toeplitz-inspired finite refinements. Finally, we formulate a
conditional continuum-lift obstruction: any proposed static-patch or dS/CFT
dictionary that factors only through convergent screen shadows is incomplete
whenever an operator-response witness persists.

This is a finite benchmark note with reproducible code. It is not a continuum
de Sitter theorem, not a dS/CFT construction, and not a proof of ER=EPR in de
Sitter.

## 1. Introduction and Claim Boundary

Observer algebras are finer objects than entropy vectors, diagonal correlators,
or screen-restricted channel summaries. In holographic and observer-centered
settings this distinction matters: an entropy-like screen can carry the right
size scale while still failing to specify which noncommutative observables are
available to the observer. This paper isolates that failure mode in finite,
exactly executable models.

The construction is deliberately modest. At each cutoff we compare a quantum
matrix observer algebra with a dephased abelian control that has the same
declared screen-visible data. The two models agree on the finite diagnostics
that are allowed to factor through the screen, but differ on intrinsic
operator-response probes such as commutators and off-diagonal matrix-unit
response. The result is not that diagonal blindness is surprising; the result
is a reproducible finite benchmark that names precisely which data are being
used and which algebraic structure they miss.

The main theorem ladder has four roles. First, a screen-shadow collision shows
that the declared screen diagnostics do not determine the observer algebra.
Second, operator-response witnesses separate the quantum algebra from the
abelian control. Third, a cutoff-compatible strong-continuity gate rules out
instantaneous dephasing without assuming the desired algebraic response as an
axiom. Fourth, finite cutoff embeddings and a conditional lift obstruction
explain how this benchmark constrains any proposed continuum dictionary that
would factor only through screen-shadow data.

The paper is positioned as a finite diagnostic benchmark rather than a
competing formulation of holographic QEC, algebraic ER=EPR, or de Sitter
static-patch algebras. Its purpose is to provide a small arena in which
screen-only observer dictionaries can be tested and, under explicit lift
assumptions, shown incomplete.

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

## 2. Known, Standard, New, and Open

This note uses standard finite-dimensional ingredients: matrix algebras,
diagonal conditional expectations, Schur multipliers, UCP maps, UHF inductive
limits, and operator-algebra/QEC language for reconstructable observables.
The fact that a diagonal screen map forgets off-diagonal matrix units is also
standard and elementary.

The benchmark contribution is narrower. It packages that elementary
forgetfulness into a reproducible finite diagnostic obstruction, adds a
strong-continuity gate that excludes instantaneous dephasing without assuming
the desired response, and audits consecutive cutoff maps that are more
structured than a bare factorial inclusion. In particular, the embedding audit
now compares:

- a trace-filled UCP baseline;
- harmonic mode-label refinement across consecutive cutoffs;
- heat-kernel Schur coarse graining after harmonic refinement;
- a Berezin-Toeplitz-inspired CP smoothing surrogate.

The open physics question is whether any of these finite cutoff maps, or a
different one, is the right approximation to a static-patch observer algebra.
The sharp expert-feedback question is:

```text
Are the continuum-lift obstruction and cutoff embedding/coarse-graining problem
meaningful ways to formalize the limitation of diagonal/screen-shadow data?
```

## 3. Finite Observer Model

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

### Definition 3.1: Screen-Shadow Functor `Sh_N`

For this benchmark, let `Scr_N` be the class of declared finite
screen-visible diagnostics. An element `F in Scr_N` is any functional that
factors through diagonal screen data:

- the diagonal state `E_diag(rho)`;
- diagonal correlators;
- finite horizon-overlap counts;
- low-order screen-restricted transfer records.

The screen-shadow functor is the tuple of all such benchmark diagnostics:

```text
Sh_N(A,rho,channel) = (F(A,rho,channel))_{F in Scr_N}.
```

Equivalently, if two finite models have the same diagonal expectation data and
the same declared low-order screen-transfer records, then their `Sh_N` values
agree. This is a finite benchmark definition, not a canonical continuum
definition of a gravitational screen.

### Definition 3.2: Operator-Response Functor `Resp_N`

Let `Resp_N` be the finite operator-response diagnostic tuple. Unlike `Sh_N`,
it may query non-diagonal algebraic structure:

- off-diagonal matrix units `e_ij`;
- commutators such as `[e_12,e_21]`;
- relative/operator response under a channel;
- generator covariance under cutoff refinement maps.

The basic commutator subdiagnostic is:

```text
[e_12,e_21] = e_11 - e_22.
```

Its operator norm is `1` inside `M_N`, while every commutator vanishes inside
the abelian control `C^N`.

## 4. Main Results

### Theorem 1: Screen-Shadow Collision

For every `N >= 2`, the quantum observer algebra `M_N` and the dephased abelian
control `C^N` have identical `Sh_N` values for all diagnostics in `Scr_N`, but
their observer algebras are not isomorphic and are separated by `Resp_N`.

**Proof sketch.** The screen algebra in both cases is the same diagonal algebra
`C^N`. Any screen-shadow diagnostic is, by definition, a function only of the
diagonal state, diagonal correlators, and declared screen-restricted transfer
records. Those data are matched by construction after applying `E_diag`.
However, `M_N` is noncommutative for `N >= 2`, while `C^N` is abelian. In
`M_N`, the matrix units satisfy `[e_12,e_21]=e_11-e_22`, whose operator norm is
`1`. In `C^N`, all commutators are zero. Thus `Sh_N` agrees while `Resp_N`,
the observer algebra, and intrinsic operator response differ. QED.

The finite certificates extend this elementary collision across the packaged
static-patch regulator stack: screen entropy, diagonal correlator,
horizon-overlap, and screen-restricted transfer data are held fixed while
off-diagonal response distinguishes `M_N` from `C^N`.

### Proposition 2: Finite Schur and Derived Dynamics Preserve the Split

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

### Theorem 3: Strong-Continuity Gate

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

### Proposition 4: Cofinal Type-`II_1` Scaffold

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

### Proposition 5: Consecutive Cutoff Refinement Audit

Exact full-matrix inclusions are too rigid for consecutive cutoffs. The
finite audit therefore compares consecutive UCP or controlled-positive
refinements that preserve or converge on the declared screen-shadow data while
retaining an operator-response witness.

The baseline trace-filled refinement is as follows. For `n <= m`, choose an
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

The audit then adds three more structured finite refinements. Harmonic
projection preserves spherical-harmonic labels with `ell <= L` inside the
`ell <= L+1` cutoff and uses the same trace-filled complement, so low-harmonic
diagonal observables are preserved exactly and the `1/n` multiplicativity
witness remains. Heat-kernel coarse graining composes harmonic refinement with
a positive-definite Schur heat channel; diagonal screen data are fixed exactly,
while off-diagonal response is retained by a positive heat-kernel factor that
tends to one under the chosen cutoff scaling. The Berezin-Toeplitz-inspired
smoothing surrogate is a convex mixture of harmonic trace-filled refinement
with a trace-to-uniform channel at `O(1/N)` weight; it is UCP and trace
preserving, has vanishing screen-shadow perturbation, and retains commutator
response with retention tending to one.

None of these maps is claimed as the canonical static-patch embedding. The
point is that the finite obstruction survives a small family of more
physically motivated cutoff/coarse-graining audits rather than only the
factorial inclusion scaffold.

### Theorem 6: Conditional Continuum Lift Obstruction

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

This is a conditional theorem. Its assumptions are the lift data; it is not a
construction of the continuum theory.

The continuum-lift theorem sprint formalizes the two finite diagnostics used
in this proof. The declared screen-shadow functor `Sh_L` is the tuple of all
screen-visible functionals that factor through diagonal/screen data, and the
operator-response witness is the operator-norm noncommutativity functional

```text
nu(A_L)=sup { ||[a,b]|| : ||a||<=1, ||b||<=1 }.
```

For the finite benchmark, `Sh_L(M_N)=Sh_L(C^N)` by screen factorization, while
`nu(M_N)>=1` using `a=e_12,b=e_21` and `nu(C^N)=0`. The response topology is
operator norm; the rank-one trace-`L^2` matrix-unit witness is explicitly not
used as the persistence topology because it can vanish with `N`.

The branch decision ledger selects the theorem-candidate endpoint: the
obstruction theorem is proof-ready under explicit lift hypotheses, while a
canonical static-patch realization of those hypotheses remains conditional
operator-algebra input.

One way to visualize the obstruction is:

```text
finite quantum regulators      ----response persists---->  quantum limit A
        | Sh_N                                             | screen dictionary
        v                                                  v
finite dephased controls      ----same screen shadow---->  same screen output
        | Resp_N gap
        v
abelian response/control data  ------------------------->  abelian limit D
```

If the right-hand dictionary only sees the middle screen output, it cannot
separate the noncommutative and abelian limiting candidates.

A physical static-patch construction would instantiate the lift assumptions by
choosing a canonical cutoff/coarse-graining map, a convergent state or trace
family, and a compatible local or modular generator. Harmonic projection,
heat-kernel coarse graining, or Berezin-Toeplitz refinement are plausible
candidate mechanisms; the trace-filled UCP map in Proposition 5 is only a
finite benchmark replacement for the exact divisibility obstruction.

## 5. Why This Is Not Trivialized By Diagonal Blindness

The finite collision is intentionally sharp: screen shadows are diagonal or
screen-restricted, while the response witness is noncommutative. A skeptical
reader may say that diagonal probes cannot see off-diagonal structure. That is
true, and it is the point of the benchmark.

The nontrivial part is the package surrounding that elementary observation:

- the screen-shadow class is declared explicitly;
- the response witness is algebraic and exact;
- KMS/detailed-balance-looking conditions are separated from strong continuity;
- finite derived dynamics and regulator-class certificates preserve the split;
- exact cofinal inclusions, approximate consecutive UCP refinements, harmonic
  mode refinement, heat-kernel coarse graining, and Berezin-inspired smoothing
  are audited;
- the continuum-lift obstruction states what any screen-only dictionary would
  fail to see under explicit lift assumptions.

The result is best read as a calibration rig for proposed observer/screen
dictionaries.

## 6. Related Work and Positioning

Operator-algebra quantum error correction is the natural finite language for
reconstructable observable algebras; see Beny, Kempf, and Kribs,
*Quantum Error Correction of Observables* (arXiv:0705.1574). Holographic QEC
and subalgebra reconstruction enter through Almheiri, Dong, and Harlow,
*Bulk Locality and Quantum Error Correction in AdS/CFT* (arXiv:1411.7041), and
Harlow, *The Ryu-Takayanagi Formula from Quantum Error Correction*
(arXiv:1607.03901).

HaPPY-style holographic tensor-network codes supply another finite arena where
entropy/min-cut diagnostics are useful but do not exhaust reconstruction
questions; see Pastawski, Yoshida, Harlow, and Preskill, *Holographic quantum
error-correcting codes: toy models for the bulk/boundary correspondence*
(arXiv:1503.06237). The present benchmark is not a competing tensor-network or
AdS/CFT construction. It isolates a finite static-patch-style screen/observer
diagnostic failure mode and makes the certificate layer executable.

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

## 7. Limitations

The note does not prove:

- a continuum de Sitter observer-algebra theorem;
- a dS/CFT dictionary;
- literal ER=EPR in de Sitter;
- that the factorial subsequence is physically canonical;
- that the trace-filled, harmonic, heat-kernel, or Berezin-inspired cutoff maps
  are the correct fuzzy-sphere/static-patch refinement;
- approximate QEC stability in a Type-II or Type-III limit.

The next mathematical target is to replace the finite surrogate map family with
a canonical construction, for example a proven Berezin-Toeplitz or
static-patch modular conditional expectation, and rerun the screen-shadow,
response, continuity, and covariance tests.

## Appendix A: What the Tests Prove and Do Not Prove

The tests and certificates prove reproducibility of the finite benchmark
implementation: the declared certificate fields are regenerated, the lead
JSON indexes parse, the compact package script reports all five certificate
families as passing, and the focused regression tests exercise the finite
strong-continuity, Type-II scaffold, inclusion-covariance, UCP embedding, and
continuum-lift modules. The `tests.test_lift_diagnostics` suite additionally
checks the formal `Sh_L` equality, operator-norm response separation, response
lower bounds under implemented lift maps, and theorem-candidate decision
record.

The tests do not replace the human proofs above. They also do not prove a
canonical continuum static-patch embedding, a dS/CFT dictionary, approximate
QEC stability, or literal ER=EPR in de Sitter. Their purpose is to make the
finite theorem package auditable and regression-safe.

## Appendix B: Reproducibility

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
