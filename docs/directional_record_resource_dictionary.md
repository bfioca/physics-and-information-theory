# Directional-Record Resource Dictionary

Status: audit-ready Paper U G2 ledger. Every implication is directional and
status labeled. Natural logarithms are used throughout.

## 1. The chain is a fork

The valid operational structure is

```text
                         /-> required accessible readout information
target Haar risk -------+
                         \-> required SO(3) asymmetry

accessible readout information
  -> finite classical record size       only in a declared classical bottleneck

required asymmetry or Casimir
  -> representation/energy cost         only under named spectral or matter premises
```

It is not valid to write

```text
risk -> A_SO3 -> classical dimension -> energy
```

as an unconditional serial chain. Relative entropy of asymmetry upper-bounds
accessible orientation information; it does not certify that a protocol
actually acquires or stores a classical record.

## 2. Quantities that remain distinct

Let `G~Haar(SO(3))`, let `Y` be the complete readout transcript, and let
`g_hat(Y)` be its estimate.

| Symbol | Exact meaning | Not implied by the definition |
| --- | --- | --- |
| `R_Haar` | `E sin^2[theta(g_hat^-1 G)/2]`, the global Bayes risk | local unbiasedness, absolute orientation, or a QFI regime |
| `S_dir=A_SO3(rho)` | `D(rho || G_SO3[rho])` for the complete accessible encoded state | accessible information equality, a classical memory, thermodynamic entropy, or `S_Ob` |
| `I_out` | classical mutual information `I(G:Y)` for the actual protocol | optimality of the readout |
| `I_acc` | supremum of `I(G:Y)` over the declared allowed measurements on the orbit ensemble | existence of a stable record or equality with `S_dir` |
| `m_C` | support cardinality of a declared finite discrete classical record `C` | quantum Hilbert-space dimension or gravitational observer dimension |
| `d_eff^cl(C)` | `exp[H(C)]` for that declared discrete classical record | a coordinate-invariant notion for continuous outcomes or a quantum effective dimension |
| `C2` | mean Casimir `Tr(rho J^2)=sum_j j(j+1)p_j` | orientation quality |
| `K1` | mean representation label `sum_j j p_j`, not `|<J>|` | polarization or a classical angular-momentum charge |
| `F_Q` | local SLD quantum Fisher information matrix for the orbit, when defined | small global risk or removal of stabilizer ambiguities |
| `S_th` | thermodynamic or von Neumann entropy specified by a separate state/ensemble convention | asymmetry, record capacity, or observer entropy |
| `S_Ob` | the observer-entropy parameter in Harlow's closed-universe observer rule | `A_SO3`, `H(C)`, `log dim H_O`, or a static-patch thermodynamic entropy |

The joint-state convention for `S_dir`, including invariant memories and
pre-correlations, is fixed in `observer_register_model_class.md`.

## 3. Closed operational arrows

Define

```text
c_SO3 = 6/(e pi^(5/3)),
L(epsilon) = [ (3/2) log(c_SO3/epsilon) ]_+.             (3.1)
```

The exact dual lower bound used in the rate-distortion proof is

```text
L_dual(epsilon)
  = sup_(lambda>0) {-lambda epsilon-log Z(lambda)},
Z(lambda)=integral dg exp[-lambda c(g,e)].               (3.2)
```

Equation (3.1) is the analytic lower bound obtained from
`Z(lambda)<=pi^(5/2)/(8 lambda^(3/2))`.

### Arrow R1: risk to actual readout information - PROVED

For every protocol in `C_dir^op`,

```text
R_Haar <= epsilon
  => I_out >= L_dual(epsilon) >= L(epsilon).             (3.3)
```

This is a rate-distortion necessity statement for the actual output, not a
claim that mutual information alone is sufficient for low risk.

### Arrow R2: readout information to asymmetry allocation - PROVED

For the group-orbit ensemble and any `g`-independent physical channel followed
by any POVM,

```text
I_out <= I_acc <= S_dir.                                 (3.4)
```

The last inequality is the Holevo/relative-entropy data-processing bound. It
continues to hold with arbitrary rotation-trivial multiplicity and invariant
ancillas when `S_dir` is evaluated on the full accessible state.

### Arrow R3: risk to asymmetry - PROVED

Combining (3.3) and (3.4),

```text
R_Haar >= c_SO3 exp[-2S_dir/3],
R_Haar <= epsilon => S_dir >= L(epsilon).                (3.5)
```

The converse is false; see Arrow F1.

## 4. Classical-record branch

This branch exists only in `C_dir^cl`. Let `C_T` be a finite discrete classical
state after storage, and require the Markov factorization

```text
G -> C_T -> Y.                                           (4.1)
```

All side information available to `Y` must be part of `C_T`; otherwise (4.1)
is false.

### Arrow C1: risk to classical record capacity - CONDITIONAL

Under (4.1),

```text
I_out <= I(G:C_T) <= H(C_T)
      = log d_eff^cl(C_T) <= log m_C.                   (4.2)
```

Therefore

```text
R_Haar <= epsilon
  => d_eff^cl(C_T) >= exp[L(epsilon)]
  => m_C >= ceil(exp[L(epsilon)]).                       (4.3)
```

This is a proved lemma once the classical bottleneck is declared. It is marked
`CONDITIONAL` because a general quantum register need not factor through
(4.1). For continuous records, differential entropy is coordinate dependent;
neither `m_C` nor `d_eff^cl` is used without a declared discretization.

Postselection does not remove the condition. An abort is another classical
outcome in the unconditional record. For a covariant success event with
probability `p_s`, conditional risk `R_s` instead implies the rate-weighted
allocation

```text
S_dir >= p_s L(R_s).                                    (4.4)
```

The factor `p_s` is essential.

### Arrow C2: asymmetry to classical record size - FALSE in general

`S_dir` bounds how much orientation information a measurement can extract; it
does not lower-bound `I_out`, force a measurement to be performed, or construct
a stable classical bottleneck. A protocol may discard an asymmetric state, and
arbitrarily large invariant memory multiplicity may carry no orientation
information. The identity `S_dir=log D` for the canonical pure Peter-Weyl token
is a property of that construction, not a universal memory-dimension theorem.

## 5. Representation branch

### Arrow J1: risk to mean Casimir - PROVED

The independent fusion/Hardy theorem gives

```text
R_Haar >= 1/(16C2+8),
R_Haar <= epsilon
  => C2 >= C_req(epsilon)=[epsilon^-1-8]_+/16.           (5.1)
```

The lower bound is nontrivial for `epsilon<1/8`. It says that good performance
requires Casimir; it does not say that Casimir provides good performance.

### Arrow J2: asymmetry to mean representation label - PROVED

For `p_j=Tr(P_j rho)`,

```text
S_dir <= H(p)+2 sum_j p_j log(2j+1) <= B(K1),            (5.2)

B(K)=inf_(beta>0) {beta K+log Z_spin(beta)},
Z_spin(beta)=(1+6e^-beta+e^-2beta)/(1-e^-beta)^3.
```

Thus `R_Haar<=epsilon` requires

```text
B(K1) >= L(epsilon),                                    (5.3)
```

or equivalently `K1>=B^{-1}_uparrow(L)` using the increasing generalized
inverse. Jensen separately gives `K1(K1+1)<=C2`.

### Arrow J3: representation moments to performance - FALSE as a converse

A maximally mixed state in a high-spin irrep has large `C2` and rotor energy
but `S_dir=0` and `F_Q=0`. Large `K1` or `C2` is therefore not sufficient.
Mean vector spin is even less suitable: cat and anticoherent states can have
`<J>=0` with nonzero asymmetry or QFI.

## 6. Energy branch

### Arrow E1: asymmetry to energy under sector growth - CONDITIONAL

Let the ground-subtracted invariant directional Hamiltonian `H_dir` act on the
same complete accessible state and representation used to define `S_dir`. Let
`H_dir=direct_sum_j identity_(V_j) tensor H_j`, let
`epsilon_j=inf spectrum(H_j)`, and suppose, for at least one `beta>0`,

```text
Z_H(beta)=sum_j (2j+1)^2 exp(-beta epsilon_j)<infinity.  (6.1)
```

Then every state of mean energy `E_dir=Tr(rho H_dir)` obeys

```text
S_dir <= beta E_dir+log Z_H(beta).                       (6.2)
```

Combining (3.5) and (6.2) gives the model-dependent energy requirement

```text
E_dir >= E_req(epsilon)
       = sup_(beta: Z_H(beta)<infinity)
         [L(epsilon)-log Z_H(beta)]_+/beta.              (6.3)
```

The mathematical implication is proved; its use in Paper U is conditional on
deriving `epsilon_j`, `H_dir`, and the comparison to total Killing energy from
the same action. Charged controllers and invariant physical memories cannot be
removed from `H_dir` while their joint state remains inside `S_dir`.

### Arrow E2: finite energy to finite directional capacity - FALSE without (6.1)

The positive invariant Hamiltonian

```text
H_bad=sum_j (1-exp(-j))P_j < 1                           (6.4)
```

admits Peter-Weyl cutoff tokens whose risk tends to zero at uniformly bounded
energy. Covariance, positivity, and a finite mean energy do not imply a
directional-capacity bound.

### Arrow E3: risk to excitation energy for confined orbital matter - PROVED on `C_dir^orb`

For the proved subclass `C_dir^orb`, with finitely many spinless
nonrelativistic particles, hard support `|x_i|<=a`, total rest mass `M`, and
`H_ex>=sum_i p_i^2/(2m_i)`,

```text
C2 <= 2Ma^2 E_ex,
R_Haar <= epsilon
  => E_ex >= [epsilon^-1-8]_+/(32Ma^2).                  (6.5)
```

This is a theorem on that named domain, not a relativistic-field or intrinsic-
spin result.

### Arrow E4: classical record size to energy - OPEN/model specific

There is no Hamiltonian-independent cost per classical record state. Degenerate
memories, charged representations, preparation work, support stress, and
readout controls can change the cost. Equations (6.2) and (6.5) price the
directional quantum resource, not an abstract number of classical labels.

## 7. QFI, thermodynamic entropy, and observer entropy

### Arrow F1: large asymmetry to small global risk - FALSE as a universal converse

Equation (3.5) is necessary-only. Asymmetry can be inaccessible for the chosen
protocol, and a state with a nontrivial stabilizer cannot resolve the full
group. Explicitly, the pure state `|j,0>` has
`S_dir=log(2j+1)->infinity` but is invariant under every rotation about its
axis; taking a stabilizer half-turn gives `R_Haar>=1/2`. A state should not be
called a good full-frame record from `S_dir` alone.

### Arrow F2: local QFI to small global risk - FALSE

Local QFI measures infinitesimal orbit sensitivity. It does not remove distant
or stabilizer ambiguities. The repository contains two explicit failures:

1. a rare high-spin tail has diverging QFI while the full orbit converges in
   trace distance to an invariant state; and
2. a spin-2 state has `F_Q=8 I_3` but a half-turn stabilizer forces
   `R_Haar>=1/2`.

QFI is not used in the closed G2 chain. A QFI-based route would require a hard
spectral or higher-moment tail condition and a global identifiability lemma.

### Arrow F3: `S_dir` and thermodynamic entropy - FALSE as an identification

A pure asymmetric token has von Neumann entropy zero and positive `S_dir`.
Conversely, the maximally mixed state in a spin irrep has positive von Neumann
entropy and `S_dir=0`. Thermodynamic entropy additionally depends on a
Hamiltonian and ensemble. No universal equality or monotone comparison is used.

### Arrow F4: `S_dir` and Harlow's `S_Ob` - OPEN

No common state space, conditional expectation, or comparison theorem has been
specified that would relate the static-patch quantity (2.2) to the
closed-universe observer parameter `S_Ob`. Paper U neither identifies them nor
assumes an inequality in either direction. The relevant primary sources are
Harlow, Usatyuk, and Zhao, [arXiv:2501.02359](https://arxiv.org/abs/2501.02359),
and Gour, Marvian, and Spekkens,
[arXiv:0901.0943](https://arxiv.org/abs/0901.0943).

## 8. Gravity boundary

The proved compactness substitution for `C_dir^orb`,

```text
2G(M+E_ex)/a <= chi < 1
  => C2 <= chi^2 a^4/(8G^2),                             (8.1)
```

is a declared weak-gravity proxy. It is not a complete metric, lapse, stress,
junction, horizon, or QES bound. Therefore:

| Arrow | Status | Required addition |
| --- | --- | --- |
| `energy + proper support -> compactness proxy (8.1)` | **CONDITIONAL** | the explicit positive-energy orbital assumptions and the declared proxy |
| `energy + support -> physically preferred G_cap` | **OPEN** | select a gauge-invariant functional and derive it from the common action |
| `G_cap -> S_Ob` | **OPEN** | a gravitational observer-algebra or path-integral comparison theorem |
| nonzero `B_W` -> Paper U capacity | **FALSE as a current dependency** | Paper U does not require `B_W`; the completed Paper R interval contains zero |

## 9. Proof notes for newly exposed lemmas

### P1. Rate-distortion dual bound for R1

For each output, rotate its posterior into an error density. Relative-entropy
positivity against `exp(-lambda c)/Z(lambda)` gives
`I(G:Y)>=-lambda R-log Z(lambda)`. Optimize in `lambda`. Applying the stated
upper bound on `Z` yields (3.1). This is the proof in
`docs/global_so3_reference_risk.md`, now exposed as an arrow rather than only a
risk corollary.

### P2. Full-state Holevo bound for R2

The ensemble average is `G_SO3[rho]`, so its Holevo information is
`S(G_SO3[rho])-S(rho)=D(rho||G_SO3[rho])` when the entropy difference is
finite, and the relative-entropy formulation extends beyond that case. Data
processing through every `g`-independent channel and measurement proves (3.4).
Invariant correlated memories are already part of the multiplicity space.

### P3. Classical bottleneck lemma C1

The Markov chain (4.1) gives `I(G:Y)<=I(G:C_T)`. Classical entropy bounds give
`I(G:C_T)<=H(C_T)<=log m_C`. Combining with P1 proves (4.3). This proof does not
apply to a quantum memory or an undeclared continuous outcome.

### P4. Covariant postselection lemma

Let `B` be the success flag. Covariance makes `p(B=1|G=g)=p_s`, hence
`I(G:B)=0` and the success-conditional prior is Haar. The chain rule gives
`I(G:Y,B)>=p_s I(G:Y|B=1)`. P1 applied to the success branch and P2 applied to
the full instrument yield (4.4).

### P5. Spectral energy inversion

Relative-entropy positivity of `p_j` against probabilities proportional to
`(2j+1)^2 exp(-beta epsilon_j)` proves (6.2). Since it holds for every admissible
`beta`, substitute `S_dir>=L(epsilon)`, rearrange, take the positive part, and
optimize to obtain (6.3).

### P6. Bounded-loss stability

With total variation defined as one half of the `l1` distance, expectations of
any `[0,1]` loss differ by at most that distance. The diamond or strategy norm
contracts to output total variation, proving the error rule in
`observer_register_model_class.md`.

## 10. Final closure ledger

| ID | Arrow | Status |
| --- | --- | --- |
| R1 | target Haar risk -> actual readout mutual information | **PROVED** |
| R2 | actual/accessible information <= joint `S_dir` | **PROVED** |
| R3 | target Haar risk -> required joint `S_dir` | **PROVED** |
| C1 | target Haar risk -> finite classical entropy/alphabet | **CONDITIONAL** on a declared finite classical bottleneck |
| C2 | `S_dir` -> classical record dimension | **FALSE** in general |
| J1 | target Haar risk -> required mean Casimir | **PROVED** |
| J2 | required `S_dir` -> required mean representation label | **PROVED** |
| J3 | large Casimir/mean spin -> good reference | **FALSE** |
| E1 | required `S_dir` -> energy cost | **CONDITIONAL** on finite sector partition function |
| E2 | generic finite energy -> bounded directional capacity | **FALSE** |
| E3 | target risk -> orbital excitation cost | **PROVED** within `C_dir^orb`; extension beyond that class is open |
| E4 | classical record size -> energy cost | **OPEN/model specific** |
| F1 | large `S_dir` -> small global risk | **FALSE** as a universal converse |
| F2 | large local QFI -> small global risk | **FALSE** |
| F3 | `S_dir` = thermodynamic entropy | **FALSE** |
| F4 | `S_dir` compared or identified with `S_Ob` | **OPEN** |
| G1 | energy/support -> preferred gravitational budget | **OPEN** beyond declared proxies |
