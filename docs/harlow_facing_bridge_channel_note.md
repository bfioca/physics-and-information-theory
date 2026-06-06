# Finite Bridge-Channel Benchmarks For Algebraic ER=EPR Diagnostics

## One-line pitch

Engelhardt and Liu propose that ER=EPR connectivity should be associated with
operator-algebraic structure, not merely with the amount of entanglement. This
repository supplies a finite stabilizer/QEC benchmark layer for that idea:
exact bridge-channel certificates where entropy and min-cut shadows can be
blind to the named channel, while algebraic decoding and coupling data predict
the operational transfer.

## Claim boundary

This is not a new definition of algebraic ER=EPR, not a continuum-gravity
theorem, and not a de Sitter construction. It is a finite research-code
laboratory for asking which diagnostics determine observer reconstruction and
bridge-channel behavior.

The safe technical claim is:

```text
finite entropy/min-cut shadows can be incomplete;
operator-algebraic data can be necessary to predict reconstruction or channel behavior.
```

## Result spine

The benchmark arc now has a theorem target above the finite bridge-screen stack.

| Layer | Finite statement | Main diagnostic split |
| --- | --- | --- |
| Observer-algebra tomography | Finite stabilizer/OA-QEC shadows form a strict hierarchy; weak entropy/channel data do not determine observer algebras, while richer response/commutator data can recover the finite algebraic signature. | entropy/channel-visible vs reconstruction-visible |
| Encoded mouths | Right mouths are encoded in independent `[[5,1,3]]` blocks; low-order physical entropy through the code distance is blind to the logical mouth pairing. | low-order entropy-visible vs decoder/channel-visible |
| Bridge controls | Algebra-aware Clifford and `T`-dressed activations transfer to the algebraically correct mouth; wrong-mouth and mouth-blind Pauli-twirled controls fail. | generic resource-visible vs coupling/channel-visible |
| State-derived dynamics | The mouth map is inferred from the encoded resource state, and the north/south recovery transition is inferred from induced screen channels. | low-order entropy-visible vs state/channel-visible |
| Interacting bridge theorem | Logical-`CZ` dressing makes the bridge resource non-product; the state determines observer algebra and mouth map, while a static-state no-go isolates the need for screen dynamics. | interacting-state-visible vs static-transition-visible |
| Interacting bridge code theorem | For arbitrary right-mouth graph-`CZ` interactions, pairwise inter-bridge MI fails as a graph reader, but state-derived Pauli-correlation tomography recovers the graph, observer algebra, and exact transfer. | weak correlation-visible vs Pauli-correlation/algebra-visible |
| Inseparable bridge-screen dynamics | The graph-`CZ` bridge and north/south screen router are one declared finite dynamics family; the same record derives the bridge algebra, bridge channel, screen channels, and recovery/area-analogue transition. | static-state-visible vs unified-dynamics-visible |
| Intrinsic local bridge-screen dynamics | The declared screen router is replaced by a star-local tensor network; screen channels and the recovery/area transition are derived by partial trace from local transfer tensors. | declared-router-visible vs local-channel-visible |
| Relative-entropy observer-bridge theorem | Exact finite-dimensional observer-bridge reconstruction is formulated through relative-entropy preservation, not labeled logical probes or supplied product tables. | static entropy-visible vs distinguishability/recovery-visible |
| Algebraic connectivity order parameter | Noisy finite bridge channels are classified by approximate recoverable observer algebra: relative-entropy response plus product/commutator closure separates quantum, classical, and null phases. | static entropy-visible vs algebraic-connectivity-visible |
| General finite-dimensional stability no-go | In arbitrary finite dimension, response-plus-closure on a proper probe algebra certifies that subalgebra but does not determine the maximal recoverable observer algebra. | certified-subalgebra-visible vs maximal-algebra-visible |
| Finite dS/CFT-ER=EPR compatibility benchmark | Two static-patch screen realizations can share screen entropy, horizon overlap, diagonal correlator, and screen-transfer shadows while differing in algebraic bridge connectivity. | screen/CFT-visible vs bridge-algebra-visible |
| Finite dS/CFT-ER=EPR single-dynamics benchmark | One finite screen operator-transfer family derives both screen shadows and bridge channels; screen-restricted dynamics can still collide while full operator response recovers the bridge algebra. | screen-restricted-dynamics-visible vs full-operator-dynamics-visible |
| Regulated static-patch dS/CFT testbed | Cutoff spherical screen modes and one geometric transfer kernel replace the abstract switch; low-order screen data still collide, while full operator response determines the bridge with explicit cutoff errors. | low-order-cutoff-visible vs intrinsic-operator-response-visible |
| Conditional dS ER=EPR theorem ledger | The regulated static-patch benchmark is organized as a conditional finite-to-continuum theorem ledger: screen-shadow sequences still fail, full response has vanishing model error, and the missing dS ER=EPR promotion assumptions are explicit. | finite-regulated-visible vs continuum-promotion-visible |
| Physical static-patch kernel search | A fuzzy-sphere/static-patch Hamiltonian Lindblad-dephasing kernel replaces the hand-built Schur distance kernel and preserves the screen-shadow no-go plus `M_N` versus `C^N` bridge distinction. | physically-motivated-kernel-visible vs actual-dS-dynamics-visible |
| Static-patch bilayer substrate | A coherent two-screen erasure model gives explicit north/south recovery channels and an exact symmetric recovery/quantum-area-analogue crossing, plus a no-go for independent area bias. | recovery-visible vs inserted-geometry-visible |

The strongest finite bridge-screen certificate currently packaged is Goal 18.
The more ambitious theorem target above it is the relative-entropy
observer-bridge statement: in exact finite dimension, the observer algebra is
the algebra whose state-space distinguishability is preserved by the region
channel, and the transferred bridge algebra is the largest algebra preserved by
the composed observer-to-observer channel. Goal 19 turns that statement into a
finite noisy order parameter for Pauli-diagonal bridges. Goal 20 then removes
the hidden Pauli-completeness assumption: response and closure certify the
algebra that was actually probed, but maximal observer-algebra recovery needs
an informationally complete probe atlas or an explicit maximality test.

## What is standard vs new here

Standard ingredients include stabilizer codes, logical Bell pairs, stabilizer
distance, Pauli transfer matrices, Choi/Kraus checks, teleportation through Bell
resources, OA-QEC language, and the known lesson that algebraic reconstruction
is the right language for holographic QEC.

The nonstandard contribution is the exact finite benchmark package: a linked
set of certificates comparing entropy shadows, low-order physical entropy,
logical mouth maps, explicit bridge activations, wrong-mouth controls,
non-Clifford channel signatures, and scrambling controls under the same finite
QEC bookkeeping. The goal is not to replace the Engelhardt-Liu conceptual
proposal, but to make a small operational testbed under it.

## Why this may be useful

The finite examples isolate a sharp operational question:

```text
What data available to an observer determine the observer's accessible algebra
and the bridge channel it can activate?
```

Entropy alone is too coarse in these benchmarks. Labeled logical access is too
privileged for a gravity-like observer. The useful middle ground is intrinsic
physical response plus commutator/channel tomography: enough operational data
to recover a finite observer algebra without pretending that a full continuum
geometry has been derived.

## Static-patch bilayer next step

The bilayer program is the current route back toward an ER=EPR-in-dS question.
It introduces two finite observer screens, north and south, and asks whether a
bulk algebra is reconstructible from the north screen, the south screen, both,
or neither. The implemented coherent routing model derives complementary
screen erasure channels from one isometry and verifies an exact symmetric match
between:

- the recovery-fidelity transition; and
- a state-derived quantum-area analogue using reduced screen entropies.

It also records a no-go: adding an independent bare-area bias shifts the
quantum-area crossing without shifting the recovery crossing. A real de
Sitter-like theorem must derive both the recovery channel and the area
competition from one controlled static-patch construction.

## Goal 15-16 update

Goal 15 adds the first non-product interacting bridge theorem in this sequence.
The right encoded mouths are dressed by a logical `CZ` interaction graph. The
resulting stabilizer state is not a tensor product of independent bridges:
full-block mutual information infers the mouth map, and the dressed observer
algebra is computed by conjugating the right logical algebra through the
inferred graph.

The positive theorem says that the state-derived decoder, which removes the
inferred interaction and routes by the inferred mouth map, restores exact
transfer while wrong-mouth and mouth-blind controls fail. The no-go theorem says
the same static state does not determine a north/south recovery transition:
opposite screen-channel completions have the same static state signature. The
minimal missing ingredient is an explicit screen dynamics/isometry.

Goal 16 fixes the arbitrary-graph diagnostic layer. Pairwise inter-bridge
mutual information is certified insufficient: for `m=3`, a path/star graph can
look like a triangle to pairwise MI. The theorem-family reader is instead a
state-derived Pauli-correlation protocol: for each paired bridge, solve for the
unique product of right logical `Zbar` operators that turns `X_L Xbar` into a
state stabilizer. That unique dressing recovers the right-mouth graph `G`, and
therefore the dressed observer algebra and inverse-interaction channel decoder.

Goal 16 still left the screen dynamics as a separate completion. Goal 17 below
packages the bridge and screen in one declared dynamics family. Goal 18 then
removes the declared screen-router layer by deriving the screen channels from a
star-local tensor network.

## Goal 17 update

Goal 17 implements that next target in the finite benchmark setting. The
declared dynamics record has one shared `dynamics_id` for:

- encoded bridge preparation;
- right-mouth graph-`CZ` interaction;
- inferred inverse interaction plus inferred mouth routing;
- coherent north/south qutrit-erasure screen routing.

The certificate verifies that full-block MI recovers `pi`, Pauli-correlation
tomography recovers `G`, the dressed observer algebra is reconstructed, and the
state-derived bridge decoder restores exact transfer. It then traces the same
declared screen router to obtain north/south channels; their Kraus operators
give the keep probabilities, recovery fidelities, and finite quantum-area
analogue. The transition is therefore derived from the unified channel data,
not appended to a static bridge state.

Controls still matter. If the screen layer is dropped, the static-state-only
no-go returns: opposite screen-channel completions share the same bridge
signature. If an external bare-area bias is appended after the channel is
fixed, the area crossing shifts while the recovery crossing does not.

## Goal 18 update

Goal 18 replaces the explicit screen router with local tensor factors. A coin
source and independent north/south transfer tensors define a star-local
isometry for one recovered logical payload qubit. There is no direct
north/south tensor, no separately declared screen recovery isometry, and no
external area bias. The north and south screen channels are obtained by partial
trace and are verified to be exact qutrit erasure channels.

The representative witness keeps the three-mouth path graph, twisted pairing
`(1,0,2)`, and `[[5,1,3]]` right blocks. It recovers `pi`, `G`, the dressed
observer algebra, and exact bridge transfer as before. The new screen theorem
checks that local branch probability is recovered from the reduced channels,
that recovery fidelity and the finite quantum-area analogue transition together
at `p=1/2`, and that entropy-only data cannot orient the transition: at
`p=0.75`, north and south screen entropies tie while channel recovery favors
north.

The useful claim is therefore finite and operational: local channel structure,
not entropy alone and not a static bridge state alone, determines the oriented
screen recovery in this benchmark.

## Major theorem target

The next theorem layer replaces stabilizer-specific Pauli response with
relative-entropy response. For a finite-dimensional region channel `N_R`,
relative-entropy preservation on an algebra's full-rank state pairs is
equivalent, by Petz/OAQEC recovery, to exact reconstructability of that algebra
on `R`. For bridge dynamics, the composed channel selects the transferred
observer algebra by the same criterion.

This is not advertised as a new Petz theorem. The contribution is the
observer-bridge diagnostic packaging: entropy/static shadows can agree while
relative-entropy response separates quantum, classical, and null observer
bridges. It is also the cleanest route from the finite stabilizer certificates
toward the Harlow-adjacent question: what operational data specify an
observer's effective algebra and channel?

## Goal 19 update

Goal 19 defines a finite noisy order parameter:

```text
algebraic connectivity = approximate recoverable observer algebra.
```

For one-qubit Pauli-diagonal bridge channels, it probes full-rank antipodal
states along `X`, `Y`, and `Z`, records relative-entropy defects, and checks
product/commutator closure. With `r=0.5` and `epsilon=0.25`, the stability
bound gives an axis-shrink lower bound `0.839956192704`, an average-gate-fidelity
lower bound `0.919978096352`, and a product/commutator-defect upper bound
`0.294473594339`.

The certificate separates finite noisy phases:

- clean and stable noisy quantum bridges;
- classical `Z` bridge;
- null depolarizing bridge.

All have the same maximally mixed static entropy shadow `(1,1)`. The certificate
also records a response-only no-go: at a coarser tolerance, a physical Pauli
channel can preserve two noncommuting probes while missing their commutator
axis, so response data must include product/commutator closure to define an
algebra.

This is still finite and Pauli-diagonal. The next true lift is a general
finite-dimensional OA-QEC stability theorem beyond Pauli channels, with
dimension/error constants and a many-body simulation signature.

## Goal 20 update

Goal 20 gives the first general finite-dimensional obstruction. For every
`d >= 2`, compare two CPTP observer channels on `M_d`:

- identity on `M_d`;
- complete dephasing onto the diagonal algebra `C^d`.

If the intrinsic probe algebra is only the diagonal `C^d`, then every diagonal
state-pair relative entropy is preserved by both channels, product closure is
pointwise exact, commutators vanish for both, and the maximally mixed entropy
shadow agrees. But the maximal recoverable observer algebras differ:

```text
identity:  M_d
dephasing: C^d
```

An off-diagonal matrix-unit coherence probe separates them immediately. The
finite lesson is therefore not that algebraic connectivity fails; it is that
the order parameter must report both the certified recoverable algebra and the
maximality evidence behind that certification.

The revised principle is:

```text
algebraic connectivity = certified recoverable algebra + maximality evidence.
```

This recovers Goal 19 as the Pauli special case where the chosen `X,Y,Z` probes
are informationally complete for `M_2`, and it marks the next serious frontier:
approximate finite-dimensional OA-QEC stability with explicit net size and
dimension-dependent error constants.

## Goal 21 update

Goal 21 routes the program back toward the dS/CFT-with-ER=EPR question without
claiming a continuum dual. The finite setup has two observer primitives,
north/south static patches, and a shared finite horizon/screen algebra `C^d`.
The screen/CFT-like layer records screen entropies, diagonal correlator shadows,
horizon-overlap data, and transfer spectra restricted to the screen algebra.

For every `d >= 2`, the same screen layer is compatible with two bridge
realizations:

```text
quantum bridge:           identity on M_d
classical horizon bridge: complete dephasing onto C^d
```

All declared screen-visible data match, but the maximal recoverable bridge
algebras differ. An off-diagonal coherence response probe separates the two
immediately. The useful interpretation is:

```text
dS/CFT-like screen shadows are not enough;
ER=EPR-style bridge connectivity needs intrinsic observer-algebra response.
```

This is a finite compatibility benchmark, not a dS/CFT theorem. It is meant to
pin down what a future controlled dS/CFT or static-patch model would need to
derive: not just screen entropy or horizon overlap, but the observer algebraic
channel connecting patches.

## Goal 22 update

Goal 22 removes one more loophole in the finite benchmark. Instead of comparing
a screen shadow to a separately attached bridge channel, it uses one finite
operator-transfer family. Diagonal matrix units are fixed for both realizations,
while off-diagonal matrix units are either fixed or projected to zero:

```text
offdiag_coupling = 1: identity bridge on M_d
offdiag_coupling = 0: dephasing bridge onto C^d
```

The same transfer process derives the screen-restricted data and the bridge
channel. Entropy, diagonal correlators, horizon overlap, low-order screen
correlators, and screen-restricted transfer spectra match. The maximal bridge
algebras differ.

The completion is not another entropy: it is full intrinsic operator dynamics,
including off-diagonal relative-entropy response and commutator/OTOC-style
growth. Inside this finite family, that data recovers the bridge algebra.

This is still not dS/CFT, but it states the next finite lesson cleanly:

```text
boundary-like screen dynamics must carry operator-algebraic response data,
not only screen-restricted correlators, to determine ER=EPR-style connectivity.
```

## Goal 23 update

Goal 23 is the first regulated static-patch version of the finite benchmark.
Instead of an abstract transfer switch, the screen is a finite set of spherical
modes `(ell,m)` with angular cutoff `L`, so the screen algebra has
`N=(L+1)^2` modes. One geometric kernel derives both the screen data and the
bridge channel:

```text
E_ii -> E_ii
E_ij -> exp(-distance(i,j)/(L+1)^2) E_ij   quantum bridge
E_ij -> 0                                  classical horizon bridge
```

The cutoff error is recorded explicitly:

```text
epsilon_L = 1 - min_offdiag_shrink.
```

For `1 <= L <= 4`, entropy shadows, low-order diagonal correlators,
horizon-overlap data, and screen-restricted transfer data collide. The induced
epsilon-recoverable bridge algebras differ: `M_N` versus `C^N`. Full intrinsic
operator response, off-diagonal relative entropy, modular response, and
commutator/OTOC-style growth recover the bridge phase inside this regulated
family.

The continuum gate remains closed. The next real physics step is to derive the
kernel from a static-patch Hamiltonian or path integral, identify a boundary
operator dictionary, prove cutoff-error control, and replace the finite Type-I
algebra with the appropriate Type-II/Type-III observer-algebra limit.

## Goal 24 update

Goal 24 turns the Goal 23 continuum gate into a theorem ledger. For each cutoff
`L`, it formalizes the finite screen/static-patch system:

```text
A_L = C^N,  O_N,L = M_N,  O_S,L = M_N,  H_L = C^N,
K_L(alpha): E_ij -> alpha exp(-distance(i,j)/(L+1)^2) E_ij.
```

It then proves two finite-regulated statements. First, the Goal 23 theorem is
recovered as the finite cutoff layer. Second, screen-visible data remain
insufficient at the sequence level: the quantum and classical/dephased kernels
agree term-by-term on screen entropy, finite-order diagonal correlators,
horizon-overlap data, and screen-restricted transfer data, while the bridge
algebras remain `M_N` versus `C^N`.

The positive theorem is explicitly conditional. Inside the regulated model, the
operator-response error obeys

```text
epsilon_L <= 2L/(L+1)^2 -> 0.
```

If a physical static-patch/dS-CFT continuum limit also supplies the required
operator dictionary, positivity/unitarity control, observer-algebra limit,
relative-entropy/OA-QEC recovery stability, horizon/QES data, and algebraic
ER=EPR interpretation, then limiting algebraic connectivity is equivalent to a
nontrivial recoverable observer bridge channel.

The finite kernel itself now has a CP preflight. The Schur coefficient matrix is
proved positive semidefinite because it is a finite restriction of a product
positive-definite kernel on `(ell,m)`, then mixed with the identity:

```text
C_alpha,s = (1-alpha)I + alpha G_s.
```

Unit diagonal gives trace preservation and unitality, and bounded numeric
Cholesky checks backstop the analytic proof. Composition is closed in the
broadened damping family `C_alpha,s o C_beta,r = C_{alpha beta,s+r}`, while the
fixed single-step subfamily is not generically closed.

The first obstruction is not hidden: `K_L` is still a regulated benchmark
kernel, not one derived from an actual static-patch Hamiltonian, path integral,
or controlled dS/CFT regulator. Goal 24 therefore does not claim de Sitter
ER=EPR. It says exactly what has been proved finitely and exactly what must be
proved before that phrase becomes honest.

## Goal 25 update

Goal 25 replaces the hand-built distance kernel with a physically motivated
finite candidate. The screen modes still use the spherical cutoff, but the
operator dynamics is now generated by a finite Hamiltonian spectrum

```text
E_L(ell,m) = [ell(ell+1) + delta_L m]/(L+1)^2.
```

The `ell(ell+1)` term is the fuzzy-sphere/spherical-harmonic Laplacian
spectrum; the small `m` split is an axisymmetric finite regulator that makes
the port labels distinguishable. The channel is the Lindblad pure-dephasing
semigroup

```text
L(rho)=-(1/2)[H_L,[H_L,rho]],
E_ij -> exp[-t_L(E_i-E_j)^2/2] E_ij.
```

It is CP, trace preserving, and unital by construction. For `1 <= L <= 5`, the
physical candidate and the classical dephased control agree on screen entropy,
low-order diagonal correlators, horizon-overlap data, and screen-restricted
transfer data, but differ in recoverable bridge algebra: `M_N` versus `C^N`.
The double-scaled time `t_L=O((L+1)^-2)` gives a vanishing cutoff-error bound.

This is progress over Goal 24 because the kernel is now tied to fuzzy-sphere
Hamiltonian/Lindblad structure. It is still not a derivation from actual de
Sitter static-patch quantum gravity. The next obstruction is deriving this, or
a better replacement, from a controlled static-patch Hamiltonian, path integral,
or dS/CFT screen dictionary.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 11 encoded-mouth entropy blindness | `PYTHONPATH=. python3 -m qgtoy er-epr-encoded --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 12 coupling-activated transfer | `PYTHONPATH=. python3 -m qgtoy er-epr-traversable --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 13 non-Clifford/scrambling controls | `PYTHONPATH=. python3 -m qgtoy bridge-channel-controls --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 14 state-derived bridge dynamics | `PYTHONPATH=. python3 -m qgtoy state-bridge-dynamics --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 15 interacting bridge theorem | `PYTHONPATH=. python3 -m qgtoy interacting-bridge-theorem --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 16 interacting bridge code theorem | `PYTHONPATH=. python3 -m qgtoy interacting-bridge-code-theorem --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Goal 17 inseparable bridge-screen dynamics | `PYTHONPATH=. python3 -m qgtoy bridge-screen-dynamics --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Goal 18 intrinsic local bridge-screen dynamics | `PYTHONPATH=. python3 -m qgtoy local-bridge-screen-dynamics --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Relative-entropy observer-bridge theorem | `PYTHONPATH=. python3 -m qgtoy relative-entropy-bridge-theorem` |
| Goal 19 algebraic connectivity order parameter | `PYTHONPATH=. python3 -m qgtoy algebraic-connectivity-order` |
| Goal 20 general finite-dimensional no-go | `PYTHONPATH=. python3 -m qgtoy general-algebraic-connectivity --max-dim 5` |
| Goal 21 finite dS/CFT-ER=EPR compatibility benchmark | `PYTHONPATH=. python3 -m qgtoy ds-cft-er-epr --max-dim 5 --screen-probability 0.75` |
| Goal 22 finite dS/CFT-ER=EPR single-dynamics benchmark | `PYTHONPATH=. python3 -m qgtoy ds-cft-er-epr-dynamics --max-dim 5 --screen-probability 0.75 --low-order 2` |
| Goal 23 regulated static-patch dS/CFT testbed | `PYTHONPATH=. python3 -m qgtoy regulated-static-patch --max-cutoff 4 --screen-probability 0.75 --low-order 2` |
| Goal 24 conditional dS ER=EPR theorem ledger | `PYTHONPATH=. python3 -m qgtoy conditional-ds-er-epr --max-cutoff 5 --screen-probability 0.75 --low-order 2` |
| Goal 24.1 static-patch kernel CP preflight | `PYTHONPATH=. python3 -m qgtoy static-patch-kernel-audit --max-cutoff 6` |
| Goal 25 physical static-patch kernel search | `PYTHONPATH=. python3 -m qgtoy physical-static-patch-kernel --max-cutoff 5 --noise-strength 1.0 --screen-probability 0.75 --low-order 2` |
| Static-patch bilayer certificate | `PYTHONPATH=. python3 -m qgtoy bilayer-program` |
| Focused merged regression slice | `PYTHONPATH=. python3 -m unittest tests.test_bilayer tests.test_state_bridge tests.test_interacting_bridge tests.test_interacting_bridge_code_theorem tests.test_bridge_screen_dynamics tests.test_local_bridge_screen tests.test_relative_entropy_bridge tests.test_algebraic_connectivity tests.test_general_algebraic_connectivity tests.test_ds_cft_er_epr tests.test_ds_cft_dynamics tests.test_static_patch_testbed tests.test_conditional_ds_er_epr tests.test_physical_static_patch_kernel tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal11_encoded_mouth_bridge_channel_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal12_finite_bridge_channel_dynamics_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal13_non_clifford_scrambling_bridge_controls_certificate` |
