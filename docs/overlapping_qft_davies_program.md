# Overlapping-Sector QFT Markov Work Package

Status: selected complementary spectral model; stationary optical regulator,
compact replacement, bath-moment theorem, and ancilla-stable spectral ULE bound
completed under explicit Gaussian-bath hypotheses. Matter derivation,
profile-specific interval constants, derivation of the prescribed switch from
the matter action, and joint stress remain pending. The generic finite-
preparation correction is completed separately.

## Purpose

The compactness-localization obstruction assumes distinct nonoverlapping target
and reference worldtubes. A physically different branch places two
operationally distinguishable spin sectors in one worldtube and couples both to
the same regulated Bunch-Davies gradient bath.

This genuinely removes the nonoverlap premise. It does not remove the need to
derive the sectors, their direct interactions, stress tensor, lifetime, or
gravitational backreaction.

## Zero-Bohr Collective Model

On `V_L tensor V_L`, take

```text
H_S=h_T(L_T^2)+h_R(L_R^2),
Q_a=L_T,a+L_R,a,
V_L=(lambda_L/N_L) sum_a Q_a tensor B_a^(sigma).         (1)
```

The Hamiltonian is scalar on the fixed irreducible sectors, so every `Q_a` is
exactly zero Bohr frequency. The regulator width `sigma` is fixed in optical
units while `L` grows.

For the declared Gaussian spectral UV form factor, the candidate coincident
gradient spectrum is

```text
j_sigma(omega)=
 omega(1+R^2 omega^2) exp(-sigma^2 omega^2)
 /[12 pi^2 R^2(1-exp(-2pi R omega))],
j_sigma(0)=1/(24 pi^3 R^3).                              (2)
```

The Gaussian factor in (2) is now derived exactly from the shifted heat
semigroup `exp[(sigma^2/2)(Delta_H+R^-2)]` on optical `H^3_R`. Its kernel is
stationary and covariant but has noncompact Gaussian tails. A Paley--Wiener
growth comparison proves that no compact stationary profile can reproduce the
exact Gaussian. The companion theorem constructs an explicit compact
double-ball replacement with spectrum `j_A=j_0 q_A^4`, the same zero mode and
KMS relation, and sufficient UV decay for finite bath moments. See
`static_patch_worldtube_ule.md`.

Because all system frequencies vanish, the universal-Lindblad jump and the
Davies jump should coincide:

```text
A_a=(lambda_L/N_L)sqrt(2pi j_sigma(0)) Q_a.              (3)
```

The target/reference Kossakowski block is rank one,

```text
K_L=[2pi lambda_L^2 j_sigma(0)/N_L^2]
    [[I,I],[I,I]],                                       (4)
```

and, in the standard Davies Hilbert-transform convention, the candidate Lamb
shift is a collective Casimir with signed coefficient

```text
H_LS=(lambda_L^2/N_L^2)s_sigma sum_a Q_a^2.              (5)
s_sigma=-[1/(24 pi^(3/2)R^2 sigma)
          +1/(48 pi^(3/2)sigma^3)].
```

It annihilates the singlet and commutes with the collective dissipator. A
full-channel theorem must include it exactly or justify a physical counterterm,
not simply drop it.

Primary open-system references:

- [Nathan and Rudner, universal Lindblad
  equation](https://arxiv.org/abs/2004.01469)
- [Merkli, all-time Davies-Lindblad
  approximation](https://arxiv.org/abs/2105.00023)
- [Bros, Epstein, and Moschella, de Sitter analyticity and
  thermality](https://arxiv.org/abs/gr-qc/9801099)
- [Perche and Zambianco, derivative-coupled
  detectors](https://arxiv.org/abs/2305.11949)
- [Olafsson and Wolf, Paley--Wiener theorem for symmetric
  spaces](https://arxiv.org/abs/1101.4419)

More strongly, every `Q_a` annihilates the total-spin singlet. The singlet is
therefore dark under the full collective system-bath Hamiltonian for arbitrary
coupling and bath memory. Its survival probability cannot diagnose the accuracy
of a Markov approximation.

## Non-Dark Witness And Norm Boundary

Let `d=2L+1`, prepare a pure reference `|r><r|`, and use a maximally
entangled target-memory input `Phi_AT`. The return projector

```text
P_ret=Phi_AT tensor |r><r|_R.                            (6)
```

has rank and trace norm one. It is non-dark: its initial expectation is one.
More directly, for the generator `-sum_a[Q_a,[Q_a,rho]]`,

```text
-p'_ret(0)=2 sum_a Var(Q_a)
            =2[2L(L+1)-|<L_R>|^2]
            >=2L(L+2)>0.                                (7)
```

The target marginal of `Phi_AT` is maximally mixed and is uncorrelated with the
reference, which gives the equality. Thus the interaction changes this state at
first order; initial probability one alone is not being used as the criterion.
Because the Haar append-and-twirl channel on `V_L tensor V_L` is
entanglement-breaking, its return probability is at most `1/d`. At heat time
`s=(1/2)log d`,

```text
p_s<=1/d+eta_heat(s)
   <=1/d+3/[2d(1-d^-2)^(3/2)]=O(1/d).                   (8)
```

This is a valid fixed-task Markov diagnostic and uses the same Choi input as the
recovery obstruction.

It is not an all-decoder theorem. For a deterministic decoder `D`, the pulled-
back entanglement-fidelity witness is

```text
W_D=(id tensor D^*)(Phi),  ||W_D||_1=d.                  (9)
```

Therefore an ancilla-stable Choi-state spectral estimate
`||rho_exact-rho_heat||_infinity<=epsilon_infinity` transfers as

```text
epsilon_rec_exact >=
1-1/d-eta_heat(s)-d epsilon_infinity.                   (10)
```

The word `ancilla-stable` is essential. A system-only ULE spectral estimate does
not automatically control the Choi output.

## Ancilla-Stable ULE Error Theorem

Normalize `X_a=Q_a/(2L)` and define bath filter moments

```text
G_sigma=int |g_sigma(t)|dt,
tau_sigma=int |t g_sigma(t)|dt/G_sigma,
```

where `g_sigma` is the Fourier transform of the square root of the spectral
density. For three identical diagonal gradient channels, the multichannel
universal-Lindblad constants are exactly

```text
Gamma_L=144 lambda_L^2 L^2 N_L^-2 G_sigma^2,
tau_sigma=M_1/G_sigma.                                  (11)
```

Nathan and Rudner bound the modified-state distance by `Gamma tau` and its
residual derivative by `2Gamma^2tau`. Apply their proof to the system tensored
with an arbitrary inert memory. The coupling norms and bath constants are
unchanged. Because the zero-Bohr ULE is unital, Duhamel's formula gives

```text
epsilon_infinity(t)<=2Gamma_L tau_sigma
                     +2Gamma_L^2 tau_sigma t.           (12)
```

At collective heat time `s=(1/2)log d`, this becomes

```text
epsilon_infinity <=
 288G_sigma M_1 lambda_L^2L^2/N_L^2
 +[20736G_sigma^3M_1/(pi j(0))]
   lambda_L^2L^4N_L^-2log d.                            (13)
```

Thus `epsilon_infinity<=A/d` with fixed `0<A<1` gives the asymptotic
all-decoder obstruction `1-A-o(1)` by (10), and the exact sufficient cap has
asymptotic form

```text
lambda_L <= c_sigma N_L/[L^2 sqrt(d log d)].            (14)
```

On `N_L~d^-1`, `L~d`, this is

```text
lambda_L=O[d^(-7/2)/sqrt(log d)].                       (15)
```

If the ULE correction is required to be no larger than the heat-to-Haar
`O(1/d)` correction in the recovery error itself, then (10) needs
`epsilon_infinity=O(d^-2)` and the stronger law

```text
lambda_L=O[d^-4/sqrt(log d)].                           (16)
```

Equations (15)-(16) are stronger than the current state-RMS `d^-3` coupling
schedule. The ancilla-stable spectral-state theorem is now supplied. It is not
a trace- or diamond-norm theorem; all-decoder transfer still costs the exact
factor `d` in (10).

The stabilization proof assumes a stationary zero-mean Gaussian bath. The
finite-preparation extension in `static_patch_finite_switching_ule.md` replaces
remote-past factorization by factorization before a prescribed amplitude ramp,
a stationary plateau, and an explicit burn-in. Its additional error is
`Gamma tau log(1+T/(B+T_chi))`. A two-point spectrum alone would not imply the
theorem for a non-Gaussian bath.

## Work Packages

### WP-B1: Spectrum And Lamb Shift

- completed: derive (2) from stationary optical heat smearing;
- completed: evaluate `j_sigma(0)` and the principal-value Lamb shift;
- completed: prove finite `G_sigma` and `tau_sigma` by frequency Sobolev norms;
- completed: verify positivity and exact KMS detailed balance;
- completed: prove the exact Gaussian is not compactly supported and construct
  a finite-worldtube replacement;
- completed: choose a named compact smooth convolution-square profile, compute
  profile-specific step-converged Sobolev constants, and derive the additional
  candidate small-support sufficient-cap penalty
  `lambda_cap=Theta(a^(5/2)[log(R/a)]^-1/8)`;
- pending: replace the numerical margin by interval enclosures and derive the
  smooth profile from a local matter current.

### WP-B2: ULE/Davies Identification

- completed: show fixed-sector scalar `H_S` leaves only zero Bohr frequency;
- completed: derive (3)-(5) with Fourier and lapse conventions fixed;
- completed: use the rank-one return projector as the non-dark diagnostic;
- completed: prove the ancilla-stable Choi spectral estimate with explicit
  three-channel constants and derive (13)-(16);
- completed: replace remote-past preparation by a prescribed amplitude ramp,
  stationary plateau, and explicit burn-in correction;
- pending: derive the switching function from the finite matter action;
- optional stronger route: prove a dimension-aware trace/diamond channel bound.

### WP-B3: Operational Distinguishability

- realize target and reference as different internal species, topological
  sectors, or protected subspaces in one worldtube;
- bound their direct Hamiltonian and exchange interactions;
- show that the relational decoder can address them without an external frame.

### WP-B4: Gravity And Lifetime

- combine both sectors and their trap/support source in one stress tensor;
- compare the common support radius with the massive-Skyrmion work package;
- prove that the protocol duration is shorter than radiation, mixing, and
  support-failure times;
- decide whether overlap opens a genuine joint parameter window.

## Kill Criteria

Reject this branch if:

- the bath moments diverge or force `sigma` to shrink with `d` fast enough to
  erase (14);
- the ULE constants grow with system dimension beyond the explicit spin norms;
- the non-dark return experiment is accurate but cannot be promoted to a
  decoder-independent recovery statement;
- only a dimension-costly trace/diamond conversion connects the theorem to the
  recovery task;
- direct target/reference interactions destroy the collective zero-Bohr sector;
- operational distinguishability imports a hidden external frame; or
- the joint support stress closes the same compactness window even without
  nonoverlap.

## Relation To Track A

Track A, the massive-Skyrmion work package, derives a named compact source and
its current/stress moments. Track B derives a controlled QFT reduced channel for
overlapping sectors. The paper needs their intersection: one source model that
realizes the overlapping algebra and one open-system estimate whose error stays
below the recovery witness over the physical lifetime.

## Reproduction

The executable stage verifies the original spectral identities, the exact
optical heat-kernel realization, the compact replacement and its UV/Lamb
properties, the named smooth compact profile and localization penalty, the
stabilized ULE constants, the rank-one return bound, the exact decoder
trace-norm cost, and both residual scalings:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-overlapping-ule
PYTHONPATH=. python3 -m qgtoy static-patch-worldtube-ule
PYTHONPATH=. python3 -m qgtoy static-patch-smooth-worldtube-ule
PYTHONPATH=. python3 -m unittest tests.test_static_patch_overlapping_ule
PYTHONPATH=. python3 -m unittest tests.test_static_patch_worldtube_ule
PYTHONPATH=. python3 -m unittest tests.test_static_patch_smooth_worldtube_ule
```
