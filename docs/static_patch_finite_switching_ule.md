# Finite Switch-On And Burn-In For The ULE Route

Status: proved a finite-preparation correction for a prescribed interaction-
amplitude ramp, with an ancilla-stable state bound and unchanged large-spin
coupling exponents.

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

## Missing-History Rate

Nathan and Rudner bound the finite-initialization Born-Redfield correction by

```text
||D_T(t)|| <= 4 gamma int_T^infinity ||J(u)||_1 du
            <= Gamma tau/T.                          (4)
```

For a ramp followed by burn-in `B`, the same kernel argument and (3) give, at
time `t=t_s+B+r`,

```text
||D_chi(t)|| <= Gamma tau/(B+r+T_chi).                (5)
```

The key point is the elementary inequality

```text
delta_chi(z)/(a+z) <= 1/(a+T_chi),    a=B+r.          (6)
```

For `z<=T_chi`, use `delta<=z/T_chi`; for `z>=T_chi`, use `delta<=1`.

## Ancilla-Stable State Bound

Apply the Nathan-Rudner modified-state construction after the plateau begins.
Writing the exact equation as
`dot(rho)=D_R rho+D_chi rho+xi`, its chain rule is
`dot(rho')=dot(rho)+dot(M_t)rho+M_t dot(rho)`. The finite-history term occurs
once in `dot(rho)`. The product `M_t dot(rho)` is bounded wholesale using the
unchanged switched-dynamics speed limit: `|chi|<=1` does not enlarge that
Appendix-C estimate. There is therefore no second multiplicative
finite-history term. ULE contraction on Hermitian inputs gives

```text
||rho_exact(t_s+B+T)-E_T(rho_exact(t_s+B))||_infinity
 <= 2 Gamma tau+2 Gamma^2 tau T
    +Gamma tau log(1+T/(B+T_chi)).                    (7)
```

The same proof holds after adjoining an arbitrary inert memory. Equation (7)
is a spectral/operator-norm state estimate, not a trace- or diamond-norm
theorem.

For a target switch contribution `epsilon_sw`, (7) gives the explicit burn-in

```text
B >= max{0,
 T/[exp(epsilon_sw/(Gamma tau))-1]-T_chi}.            (8)
```

If the effective preparation age satisfies

```text
B+T_chi >= beta/Gamma,                               (9)
```

then `log(1+x)<=x` reduces (7) to

```text
epsilon_infinity(T)
 <=2 Gamma tau+(2+1/beta)Gamma^2 tau T.              (10)
```

When only an upper bound `G<=G_bar` is used, the executable does not claim to
verify (9) for an unspecified experiment. Instead it reports the sufficient
bound-level requirement

```text
B+T_chi >= beta/Gamma_bar,
Gamma_bar=144 lambda^2 L^2 G_bar^2/N^2.              (10a)
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
Gamma tau=144 lambda^2 L^2 G M_1/N^2.                (11)
```

At heat time

```text
T=N^2 log(d)/[2pi lambda^2 j(0)],                     (12)
```

condition (9) changes the previous long-time coefficient from `20736` to

```text
20736[1+1/(2beta)].                                  (13)
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
B+T_chi=Theta(d^4 log d),                             (14)
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
stationary zero-mean Gaussian or quasifree bath, finite `G,M_1`, factorization
before switch-on, a prescribed scalar amplitude `chi`, a zero-Bohr unital ULE,
and an inert memory. It does not derive `chi` from the worldtube action, show
that the required preparation age is experimentally available, cover a
non-Gaussian bath, or control stress, lifetime, gravity, or ramp-time dynamics.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-finite-switching-ule
```

Primary source: Nathan and Rudner,
[Universal Lindblad equation for open quantum systems](https://arxiv.org/abs/2004.01469),
Appendix A.6 and Appendix C.
