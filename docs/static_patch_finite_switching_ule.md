# Finite Switch-On And Burn-In For The ULE Route

Status: proved within the Nathan-Rudner regular Gaussian-bath framework: a
finite-preparation correction for a prescribed interaction-amplitude ramp, with
an ancilla-stable state bound and unchanged large-spin coupling exponents. A
regulator-uniform extension to the named algebraic KMS QFT bath is not proved.

## Amplitude Switch

Let

```text
H_int(t)=chi(t)H_int,    0<=chi<=1,                  (1)
```

with `chi=0` before `t_0`, `chi=1` from `t_s` through readout, and a factorized
system-memory/bath state before switch-on. Because (1) switches the amplitude,
the second-order Born-Redfield kernel contains `chi(t)chi(s)`. On the plateau,
`chi(t)=1`, so the missing stationary history is controlled only by
`1-chi(s)`.

Define

```text
delta_chi(z)=1-chi(t_s-z),
T_chi=inf_{delta_chi(z)>0} z/delta_chi(z).            (2)
```

Then

```text
delta_chi(z)<=min(1,z/T_chi).                         (3)
```

An abrupt switch has `T_chi=0`. If `||dot chi||_infinity<=L_chi`, then
`T_chi>=1/L_chi`; a linear ramp of duration `T_sw` saturates this relation.
Thus a finite ramp contributes directly to the effective preparation age.

## Plateau Decomposition And Missing-History Rate

This section gives the proof adaptation rather than only quoting its result.
Work in the interaction picture and absorb the scalar amplitude into the system
operators, `X_alpha^chi(t)=chi(t)X_alpha(t)`. Their norms remain at most one, so
the Nathan-Rudner Born, Markov, and speed-limit estimates apply with unchanged
bath constants. In particular,

```text
||xi(t)||_infinity <= Gamma^2 tau,
||dot(rho)(t)||_infinity <= Gamma/2.                  (4)
```

For `t>=t_s`, write the exact reduced equation, after the same exact
Gaussian-bath expansion used in that proof, as

```text
dot(rho)=(R+D_chi(t))rho+xi,
D_chi(t)=-int_{-infinity}^{t_s} ds
             [1-chi(s)] Delta(t,s).                  (5)
```

Here `R` is the stationary plateau Bloch-Redfield generator and the kernel
obeys the induced spectral-norm estimate

```text
||Delta(t,s)||_(infinity->infinity)
 <=4 gamma ||J(t-s)||_1.                             (6)
```

This formula includes both the absent pre-switch history and the incomplete
ramp history; no factorization is reimposed at the plateau. At
`t=t_s+B+r`, set `a=B+r` and `z=t_s-s`. Equations (3), (5), and (6) give

```text
||D_chi(t)||_(infinity->infinity)
 <=4 gamma int_0^infinity dz delta_chi(z)||J(a+z)||_1
 <=[4 gamma int_0^infinity du u||J(u)||_1]/(a+T_chi)
 <=Gamma tau/(B+r+T_chi).                            (7)
```

The middle inequality uses
`delta_chi(z)/(a+z)<=1/(a+T_chi)`: for `z<=T_chi`, use
`delta<=z/T_chi`; for `z>=T_chi`, use `delta<=1`. The final inequality is the
Nathan-Rudner moment relation `Gamma_0 tau_0<=Gamma tau`.

## Ancilla-Stable Dressing Proof

Let `M_t` be the stationary plateau dressing superoperator and `L` the
stationary ULE generator. The Appendix-C kernel integrals establish, for every
operator `A`,

```text
dot(M_t)+R=L,
||M_t(A)||_infinity <=Gamma tau ||A||_infinity,
||L(A)||_infinity <=(Gamma/2)||A||_infinity.          (8)
```

Define `rho'=(1+M_t)rho`. Using (5) and the first identity in (8), with no
reset or factorization at the plateau,

```text
dot(rho')
 =L rho+D_chi rho+xi+M_t dot(rho)
 =L rho'+eta,
eta=D_chi rho+xi+M_t dot(rho)+L(rho-rho').            (9)
```

The four terms in (9) are bounded respectively by (7), `Gamma^2 tau`,
`Gamma^2 tau/2`, and `Gamma^2 tau/2`. Thus

```text
||eta(t_s+B+r)||_infinity
 <=2 Gamma^2 tau+Gamma tau/(B+r+T_chi).              (10)
```

At both endpoints `||rho'-rho||_infinity<=Gamma tau`. The zero-Bohr ULE is
unital, so its Schrodinger semigroup contracts the operator norm on Hermitian
inputs. Duhamel's formula and integration of (10) therefore give

```text
||rho_exact(t_s+B+T)-E_T(rho_exact(t_s+B))||_infinity
 <= 2 Gamma tau+2 Gamma^2 tau T
    +Gamma tau log(1+T/(B+T_chi)).                   (11)
```

For an arbitrary inert memory `M`, rerun the termwise proof with every
`X_alpha` replaced by `X_alpha tensor I_M`. All operator norms, kernel bounds,
and bath constants in (4)-(10) are unchanged. Hence (11) holds uniformly for every system-memory
density input that is factorized from the fixed bath before switch-on. The
post-burn system-memory state may be correlated with the bath: (11) is derived
from the common pre-switch initial time and does not restart the proof after
burn-in. Equation (11) is a uniform spectral/operator-norm state estimate, not
yet a trace- or diamond-norm theorem.

The fixed finite `WT-R1/D1` application in
`u8a_finite_storage_channel.md` defines the exact and comparison maps from that
same pre-switch input and then pays the explicit
`floor(D_in D_out/2)` conversion factor. A freely initialized channel on an
arbitrary correlated post-burn state remains unjustified.

For a target switch contribution `epsilon_sw`, (11) gives the explicit burn-in

```text
B >= max{0,
 T/[exp(epsilon_sw/(Gamma tau))-1]-T_chi}.            (12)
```

If the effective preparation age satisfies

```text
B+T_chi >= beta/Gamma,                              (13)
```

then `log(1+x)<=x` reduces (11) to

```text
epsilon_infinity(T)
 <=2 Gamma tau+(2+1/beta)Gamma^2 tau T.              (14)
```

When only an upper bound `G<=G_bar` is used, the executable does not claim to
verify (13) for an unspecified experiment. Instead it reports the sufficient
bound-level requirement

```text
B+T_chi >= beta/Gamma_bar,
Gamma_bar=144 lambda^2 L^2 G_bar^2/N^2.             (14a)
```

This is enough for the numerical upper bound because
`(Gamma tau)_bar Gamma_bar=(Gamma^2 tau)_bar`.
The certificate sets `B=beta/Gamma_bar`, `T_chi=0` as a mathematical witness
and evaluates the original logarithmic bound directly. This proves that the
conditional schedule is nonempty; it does not provide a physically practical
preparation mechanism.

## Heat-Time Schedule

For the three-channel collective model,

```text
Gamma tau=144 lambda^2 L^2 G M_1/N^2.                (15)
```

At heat time

```text
T=N^2 log(d)/[2pi lambda^2 j(0)],                     (16)
```

condition (13) changes the previous long-time coefficient from `20736` to

```text
20736[1+1/(2beta)].                                  (17)
```

Therefore the sufficient schedules remain

```text
lambda=O[d^(-7/2)/sqrt(log d)]
```

for an `O(1/d)` spectral budget, and

```text
lambda=O[d^-4/sqrt(log d)]
```

when the decoder-amplified correction must match the heat `O(1/d)` term.
For `beta=10`, the asymptotic coupling-cap penalty is only
`1/sqrt(1.05)=0.975900...`.

The preparation resource is not unchanged. At the two cap schedules the
required bound-level ages scale respectively as

```text
B+T_chi=Theta(d^3 log d),
B+T_chi=Theta(d^4 log d),                             (18)
```

while their ratio to heat time is
`Theta(1/[d^2 log d])` in both cases. The executable audits these scalings for
both budgets. The absolute ages are nevertheless extremely large at the
illustrative caps.

Using the step-converged signed-Skyrmion moments, the executable also reports
finite-switch versions of the two candidate matter caps. They remain
non-rigorous numbers until the continuum moment constants are interval
certified.

## Compact Time Support

A separately smooth switch-on, flat at the stationary plateau, may be paired
with a smooth switch-off after readout. The latter cannot affect earlier
reduced dynamics, so this smooth-on/smooth-off choice gives
`chi in C_c^infinity` while maintaining a plateau containing the burn-in and
observation interval. A linear ramp is only Lipschitz and does not itself have
this smooth compact-support property. The theorem does not compare ramp-time
dynamics to a stationary semigroup; a time-dependent ULE is the correct target
there.

## Claim Boundary

This is a direct proof adaptation of the finite-initialization and modified-
state arguments, not a theorem stated verbatim in the source. It assumes a
regular stationary zero-mean Gaussian reservoir for which the Nathan-Rudner
exact reduced equation and norm estimates are defined, finite `G,M_1`,
factorization before switch-on, a prescribed scalar amplitude `chi`, a
zero-Bohr unital ULE, and an inert memory. The existence of a compactly switched
unbounded-field propagator in a KMS GNS representation and regulator-uniform
passage to a quasifree QFT channel require a separate bridge lemma. This result
also does not derive `chi` from the worldtube action, show that the required
preparation age is experimentally available, cover a non-Gaussian bath, or
control stress, lifetime, gravity, or ramp-time dynamics.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-finite-switching-ule
```

Primary source: F. Nathan and M. S. Rudner,
[Universal Lindblad equation for open quantum systems](https://doi.org/10.1103/PhysRevB.102.115109),
Phys. Rev. B 102, 115109 (2020), with the
[2021 erratum](https://doi.org/10.1103/PhysRevB.104.119901). The imported speed
and Born--Markov bounds use Eq. (13) and Appendices A.3--A.5; the
finite-initialization tail uses Appendix A.6; the moment comparison uses
Appendix B Eq. (B2); and the dressing, generator, and residual bounds use
Appendix C.1--C.3. The erratum does not change the independently evaluated
`G`, `M_1`, `Gamma`, or `tau` used here.
