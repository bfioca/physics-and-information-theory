# U8a Finite-Switch Storage Channel

Status: **INCONCLUSIVE STOP FOR U8a.** The finite-switch estimate is proved in
the Nathan-Rudner regular Gaussian-bath framework, and its correctly dimensioned
conditional `WT-R1/D1` box has positive width and nonzero coupling. Applying
that estimate to the named Bunch-Davies quasifree field still requires a
regulator-uniform KMS GNS/Pauli-Fierz channel bridge. Independently, the exact
factorized rigid-current density fails microcausality under disjoint spacelike
smearings. That rigorous locality obstruction stops this exact route; it is not
a no-go for different local completions. Paper U U8a and U8b remain open as
mathematical interfaces, but the later information-exposure stop did not
activate them as a research continuation.

## 1. Fixed register, target, and action

The register is the cutoff-one Peter-Weyl space

```text
R_1=(V_0 tensor V_0*) direct_sum (V_1 tensor V_1*),
dim R_1=1+9=10.                                         (1.1)
```

The unknown relative rotation acts on the left factors. The canonical token is

```text
|eta_1>=(|Phi_0>+3|Phi_1>)/sqrt(10),                   (1.2)
```

with exact initial Haar chordal risk `3/8` and mean left Casimir `9/5`. The
target `D=V_1` is a distinguishable inert relational anchor. Because both
compared storage maps act as the identity on `D`, it is an inert stabilizing
system and is not included in the ten-dimensional channel conversion.

The target realization places the register on the central static worldline of
a unit-radius de Sitter patch, so proper and Killing time agree. Let `phi` be a
conformally coupled pseudoscalar in the Bunch-Davies KMS state and

```text
B_a=e_a^mu(nabla_mu phi+a_mu phi).                     (1.3)
```

Choose the radial `C-infinity` seed

```text
h(x)=exp[1-1/(1-x^2)] for 0<=x<1, and h(x)=0 for x>=1,
```

supported in optical radius `a/2`. Normalize its spherical transform in the
zero spectral channel, not by ordinary spatial volume, and let
`h_A=f_A^vee*f_A` be its radial convolution square. Then `h_A` is supported in
optical radius `a=R/5`, has field-amplitude multiplier `F_A(p)^2`, and produces
the exact spectrum `j_A(w)=j_0(w)F_A(Rw)^4`. Parallel-transport the axial
gradient to the central tetrad and define

```text
Phi_a(h_A)=integral_(H3_R) dmu_opt(y)
             h_A(y) P_a^b(y->0) B_b(tau,y).             (1.4)
```

Next define

```text
q(u)=0                    for u<=0,
q(u)=exp(-1/u)            for u>0,
S(u)=q(u)/[q(u)+q(1-u)],
chi_(B,T)(tau)=S(tau)S(B+T+2-tau).                     (1.5)
```

Thus `chi_(B,T)` is in `C_c^infinity`, ramps on during `0<tau<1`, is
identically one through the burn-in and storage interval, and ramps off after
storage during `B+T+1<tau<B+T+2`. The interaction is

```text
H_int(tau)=lambda chi_(B,T)(tau)
             sum_a J_left^a tensor Phi_a(h_A).          (1.6)
```

Equation (1.6) is the binding spatially smeared rigid-detector EFT. It has
compact worldtube support, but the same noncommuting global `J_left^a` is spread
over that support. It is therefore not claimed to be a microcausal local matter
current or a relativistic matter-field completion. Within this declared EFT,
the factorization in (1.6) is exact and no center-value multipole replacement
is made.

There is also a sharp reason not to relabel this as local matter. If one tried
to define an operator-valued distribution `ell_a(x)=h_A(x)J_left^a`, choose
real smooth test functions `f,g` with disjoint equal-time spatial supports in
an open set where `h_A` is nonzero. Write
`alpha_f=int f h_A dmu` and `alpha_g=int g h_A dmu`, choosing the functions so
both coefficients are nonzero. Then, for distinct components `a=1,b=2`,

```text
[ell_1(f),ell_2(g)]
 =i alpha_f alpha_g J_left^3 !=0 on the V_1 block.      (1.7)
```

The test-function supports are spacelike separated, so (1.7) violates
microcausality. It blocks promotion of this exact factorized density into Paper
U's local-matter class while retaining the exact-zero error ledger, but it does
not obstruct a different local completion with additional degrees of freedom
and nonzero multipole, band, or Lamb terms.

The free register Hamiltonian is `C_left/(2I)`. Hence
`[C_left,J_left^a]=0`, every coupled charge is zero Bohr, and the hard
`j<=1` subspace is exactly invariant. Radial smearing at the patch center gives
an isotropic Kossakowski tensor. The Lamb shift is a known function of
`C_left`; it is retained as a covariant unitary rather than discarded.
In any well-defined joint realization of (1.6), the same commutator shows that
the switched dynamics preserves `C_left`; its reduced burn map therefore
preserves the token's mean Casimir `9/5`.

## 2. Conditional channel target and common input time

The named quasifree QFT bath is not a trace-class reservoir with a bounded bath
operator. A complete application must construct the compactly switched
propagator in the KMS GNS/Araki-Woods representation, rerun the Gaussian ULE
bounds uniformly for regulated smeared fields, prove convergence of the
finite-register reduced maps, and pass the norm inequality to the limit. That
bridge is open here.

Conditional on this bridge, let the reduced map be defined by the KMS-state
slice rather than an informal bath partial trace. Let `t_0` be before switch-on,
when every admissible register-memory input is factorized from the fixed KMS
state, and let `t_b` be the end of the ramp and burn-in. Define

```text
P_B       = exact reduced channel from t_0 to t_b,
F_(B,T)   = exact reduced channel from t_0 to t_b+T,
G_(B,T)   = U_cov(T) o H_s(T) o P_B,
U_cov(T)  = U_free(T) o U_LS(T).                        (2.1)
```

`U_free` is the known free Casimir evolution, `U_LS` is the known Casimir Lamb
unitary, and `H_s` is the zero-Bohr isotropic `SO(3)` heat semigroup. Thus the
comparison is in the Schrodinger picture and retains the relative free phase
between the `j=0` and `j=1` sectors. Its rate is

```text
s=kappa T,
kappa=pi lambda^2 j_f(0),
j_f(0)=1/(24 pi^3).                                    (2.2)
```

Once the bridge hypotheses hold, `F_(B,T)` and `G_(B,T)` are linear CPTP maps
from the same pre-switch input. No channel from an arbitrary reduced state at
`t_b` is inferred: register-bath correlations generally exist after the ramp
and burn-in.

Let `V_g` be the left `SO(3)` action on the register and `W_g` the spatial
rotation on the bath. The radial optical profile and parallel transport make
`sum_a J_left^a tensor Phi_a` invariant under `V_g tensor W_g`, and the KMS bath
state is `W_g`-invariant. Conjugating the joint propagator and applying the KMS
slice therefore gives

```text
P_B(V_g rho V_g^dagger)=V_g P_B(rho)V_g^dagger,
F_(B,T)(V_g rho V_g^dagger)=V_g F_(B,T)(rho)V_g^dagger. (2.3)
```

The heat channel is isotropic, and `U_free,U_LS` are functions of `C_left`, so
they commute with the encoding. Thus the post-burn family remains an `SO(3)`
orbit, the known unitary does not change its optimal relational risk, and U7
applies to `H_s o P_B` once mean-Casimir preservation is established.

## 3. Uniform ULE residual and diamond conversion

Write

```text
c=144 lambda^2 L^2/N^2,   L=1,   N=1,
G=int |g(t)|dt,            M1=int |t g(t)|dt.           (3.1)
```

Within the Nathan-Rudner regular Gaussian-bath hypotheses, the finite-switch
estimate is uniform for every register state entangled with an arbitrary inert
memory that is initially factorized from the bath. It gives

```text
epsilon_infinity
 <= 2c Gbar Mbar
    +2c^2 Gbar^3 Mbar T
    +c Gbar Mbar log[1+T/(B+T_chi)].                   (3.2)
```

The exact analytic profile enclosure supplies

```text
Gbar = 16863.898481372697,
Mbar = 76435.38103914078.                              (3.3)
```

These intentionally loose values enclose the continuum integrals and their
infinite-frequency tails. They are not extrapolated Simpson quadratures.

The passage from (3.2) to a channel norm must pay its dimension cost. For a
Hermiticity-preserving trace-annihilating channel difference `Delta`, stabilize
with an input-dimensional ancilla. If the input and output dimensions are
`D_in,D_out`, the resulting Hermitian output `X` has dimension
`n=D_in D_out` and trace zero. Therefore

```text
||X||_1=2 Tr X_+
       <=2 min(rank X_+,rank X_-) ||X||_infinity
       <=2 floor(n/2)||X||_infinity.                   (3.4)
```

Consequently, for every regulated or regular-bath realization satisfying those
hypotheses,

```text
(1/2)||F_(B,T)-G_(B,T)||_diamond
 <= floor(D_in D_out/2) epsilon_infinity.              (3.5)
```

For `R_1`, `D_in=D_out=10`, so the factor is exactly `50`. This conversion does
not use a bound for one selected state. Uniformity over the stabilized input and
the common pre-switch domain in (2.1) are essential. Equation (3.5) becomes a
statement about the named Bunch-Davies channel only after the open QFT bridge.

## 4. Complete error ledger

For the declared model,

| contribution | normalized diamond bound | reason |
| --- | ---: | --- |
| stationary ULE initialization | `50(2c Gbar Mbar)` | equation (3.2) |
| stationary ULE growth | `50(2c^2 Gbar^3 Mbar T)` | equation (3.2) |
| finite switching history | `50c Gbar Mbar log[1+T/(B+T_chi)]` | finite ramp/burn theorem |
| multipoles | `0` | (1.6) is the exact binding smeared-detector coupling; no center-value replacement occurs |
| band leakage | `0` | `J_left^a` preserves every Peter-Weyl `j` block |
| free evolution | `0` | the exact known free Casimir unitary is included in `G_(B,T)` |
| Lamb shift | `0` | the exact known Casimir Lamb unitary is included in `G_(B,T)` |

The zeros are model statements, not generic claims about extended matter.
Changing the rigid current, hard compression, or tracked Lamb unitary reopens
the corresponding error term.

## 5. Conditional open parameter box

Take `beta=10`, require the heat exposure to lie strictly inside the declared
envelope `0.7<s<1`, and reserve the strict normalized channel bound
`eta_U8a<0.039`. The executable evaluates the displayed decimal endpoints with
80-digit outward-rounded `Decimal` arithmetic, the exact rational Sobolev
enclosures, and the guard `3.14159<pi<3.14160`. Its cross-corner exposure range is enclosed
between `0.710898...` and `0.989893...`, while its normalized diamond bound is
`0.037992465`. The conditional open box is

```text
1.278e-14 < lambda < 1.460e-14,
1.497e18 < B/R < 1.645e18,
1.031e30 < T/R < 1.100e30.
                                                               (5.1)
```

The smooth switch-on and switch-off each have duration `R`. Every protocol in
the box therefore has total duration `tau_protocol/R=2+B/R+T/R`, also bounded
between finite positive endpoints. The coupling interval excludes zero, and
every independently varied interval has positive width.

This is a finite protocol-duration statement, not an independently derived
hardware-lifetime theorem. The detector EFT is assumed to persist through the
protocol. If it cannot, the proposed storage protocol is unavailable even
earlier; the present calculation does not diagnose that failure mechanism.

The enormous times are scientifically important. They are produced by the
conservative exact Sobolev enclosures, the finite-switch estimate, and the
factor `50` in (3.5). Thus (5.1) is a controlled formal parameter regime under
the regular-bath hypotheses, not yet a theorem about the named QFT detector and
not a practical detector design.

## 6. Conditional operational record failure

For every state with mean Casimir at most `9/5`, U7 gives

```text
R_heat(s) >= 3/4-(3/4-1/36.8)exp(-2s).                 (6.1)
```

Because the interaction preserves `C_left` in every bridged realization, the
state after `P_B` still has mean Casimir `C2=9/5`. With the declared channel
error `eta<0.039`, solving
`R_heat(s)-0.039>1/2` gives the sufficient failure threshold

```text
s > s_fail = 0.6156552580594193.                       (6.2)
```

The whole box lies above `s=0.7>s_fail`. Evaluating U7 at the weaker declared
lower exposure `0.7` and subtracting the larger declared error `0.039` gives the
directed guard

```text
R_physical >= 0.5717532814987301-0.039
           >= 0.5327532814987301 > 1/2.                (6.3)
```

The token begins with risk `3/8<1/2`, so `1/2` is a genuine operational record
threshold rather than an impossible initial target. Conditional on the QFT
bridge, (6.3) excludes high-fidelity retention for `WT-R1/D1` on the declared
degradation box only. It does not
exclude shorter exposure, a different detector or local action, active error
correction with all resources priced, or a larger register.

## 7. Claim boundary

The unconditional reusable results are narrower:

- the switched missing-history and ancilla-stable comparison theorem is proved
  under the Nathan-Rudner regular Gaussian-bath hypotheses;
- the operator-to-diamond factor `50`, profile moments, and strict parameter-box
  arithmetic are verified;
- the exact factorized density has a nonzero commutator under disjoint spacelike
  smearings and therefore cannot itself be microcausal local matter.

The named Bunch-Davies reduced channel still requires the regulator-uniform KMS
GNS/Pauli-Fierz bridge. The nonzero finite box and operational record-failure
implication become physical only after that bridge. The complete error ledger
specifies what that future bridge must preserve.

It does not derive a microcausal local matter current. That remains the local-
matter part of U8a. It also does not derive preparation of (1.2) or a final
detector/readout action; those are U8b. It does not select a gravitational
functional, compare `S_dir` with `S_Ob`, revive Paper R, or close full U8.
It also does not derive an independent apparatus lifetime; persistence of the
declared EFT through each finite protocol is a premise.

The terminal research disposition is therefore:

```text
finite-switch regular-bath channel box: CONDITIONAL PASS,
named Bunch-Davies QFT channel bridge: OPEN,
unchanged promotion of the exact factorized density: INCONCLUSIVE STOP,
Paper U U8a: OPEN BUT NOT ACTIVATED,
U8b and full U8: OPEN BUT NOT ACTIVATED.
```

Reproduce with:

```bash
PYTHONPATH=. python -m pytest -q tests/test_u8a_finite_storage_channel.py
```
