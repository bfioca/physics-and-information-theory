# Conditional Class-Uniform Observer Tradeoff

Status: exact composition theorem; physical capacity, localization, and noise
premises must be proved for each declared observer class.

## Composition Theorem

Let the exposure-input ensemble be the covariant orbit
`sigma_g=U(g)sigma U(g)^*` of the complete accessible encoded state, in an
integer-spin rotational representation with arbitrary rotation-trivial
multiplicities. Every `G`-dependent system that transforms nontrivially and can
re-enter at readout is included in `U`; any unheated side system is
`G`-independent and rotation-trivial. The isotropic heat channel is convolution
by the same representation,
`H_Gamma(rho)=integral dh k_Gamma(h)U(h)rho U(h)^*`. Let `C2=<J^2>` on
`sigma`, and let `R(T)` be the Haar-prior chordal full-frame Bayes risk after
this convolution and before an arbitrary final readout. Suppose a declared
observer class proves

```text
C2 <= C_max(a,beta),
a  <= A(s_opt,rho_h,beta),
Gamma(T)=integral_0^T gamma(tau)d tau,
```

where the last line is the exposure of an isotropic `SO(3)` heat channel.  No
monotonicity of `C_max` is implicit.  Define the finite support envelope

```text
C_hat(A,beta)=sup_(0<=a<=A) C_max(a,beta)<infinity.      (0)
```

If `C_max` is proved nondecreasing in `a`, then
`C_hat(A,beta)=C_max(A,beta)`.  In general the envelope in (0) is required.
The all-state fusion theorem and exact spin-1 heat attenuation give

```text
R(T) >= 3/4[1-exp(-2 Gamma)]
        +exp(-2 Gamma)/[16 C_hat(A,beta)+8].             (1)
```

More generally, the elementary last term in (1) may be replaced by any proved
nonincreasing initial-risk floor evaluated at `C_hat`, including Hayashi's
known exact mean-Casimir optimum.  Equation (1) is retained as a transparent
executable corollary, not as a claim of a new sharp estimation constant.

For target `R(T)<=epsilon<3/4`, define

```text
delta_epsilon(Gamma)
  =3/4-(3/4-epsilon)exp(2 Gamma).                        (2)
```

Necessary conditions are

```text
delta_epsilon(Gamma)>0,
C_hat(A,beta)>=[delta_epsilon(Gamma)^-1-8]_+/16.         (3)
```

In particular,

```text
Gamma < (1/2)log[(3/4)/(3/4-epsilon)].                  (4)
```

Equation (4) is an exposure ceiling, not a universal coherence-time ceiling.
Without a physical lower bound on `gamma` from preparation and readout, an
isolated or decoupled reference can make elapsed time irrelevant.

The composition is implemented in `qgtoy/universal_observer_tradeoff.py`.
The source-hashed audit is
`experiments/universal_observer_tradeoff_certificate.json`, SHA256
`2bd73ea29cc649ed8dbc99f266d0fafa07c6b294a7a3d4cb87d88cd791168487`.

## Proved Orbital Corollary

For confined spinless nonrelativistic orbital matter with a nonnegative energy
budget `H_ex>=T`, proper support radius `a`, total rest mass `M`, and mean
energy `E_ex`,

```text
C2<=2 M a^2 E_ex.                                       (5)
```

The energy zero is part of this premise.  `H_ex` is not an arbitrary
ground-subtracted Dirichlet Hamiltonian.  If a model instead supplies `H_gs`,
it must exhibit `Delta>=0` with `H_gs+Delta>=T` as quadratic forms, and replace
`E_ex` by `E_gs+Delta`.  If `H_phys>=T` and
`H_gs=H_phys-E_phys,0`, then `Delta=E_phys,0` suffices.  A gravitational budget
must count the physical energy and support costs consistently, without
double-counting the offset.

Under the separately declared compactness admissibility condition

```text
2G(M+E_ex)/a<=chi<1,
```

one obtains

```text
C2<=chi^2 a^4/(8G^2),
R(T)>=3/4[1-exp(-2 Gamma)]
      +exp(-2 Gamma)/[8+2chi^2 a^4/G^2].                (6)
```

For `0<delta_epsilon<1/8`, a necessary size condition is

```text
chi a^2/G >= sqrt[(delta_epsilon^-1-8)/2].              (7)
```

This is an exact conditional composition and named orbital implication under
the declared heat-channel and compactness premises. Within that domain it
covers arbitrary states, zero-mean states, rare high-spin tails, arbitrary
particle number, and arbitrary rotation-trivial multiplicity. It does not
cover intrinsic spin, relativistic fields, or negative interaction energy.

The compactness parameter `chi` is not yet a complete gravitational
backreaction measure: it does not by itself control the lapse, local stress,
junction data, nonspherical metric response, or trapped surfaces throughout
the support.

## Optical Substitution

On a de Sitter static slice, `h=N^2 h_opt`. If a body lies in an optical ball
of radius `s_opt` and `N_+` is the maximum lapse on that ball, then

```text
a<=N_+ s_opt.
```

For center proper horizon distance `rho_h`, exact static-patch geometry gives

```text
N_+=sech([log cot(rho_h/(2R))-s_opt/R]_+).               (8)
```

Substitution in (6) gives a conditional optical form of (1). This step is
mathematically exact, but the repository has not yet proved that the same
curved-space matter model realizes the orbital capacity, optical support, and
heat channel jointly.

## Physics Boundary

The theorem is class-uniform only after the three premise maps are named. It
is not an unrestricted theorem about every observer. The shortest route to a
paper-worthy physics result is:

1. derive a nonzero lower exposure from the same local interaction that reads
   the orientation;
2. replace compactness admissibility by a metric/stress/junction margin for one
   relativistic matter family;
3. prove that the readout's optical support controls that same family's proper
   support;
4. exhibit either an excluded open scaling family or a certified open
   parameter box.

The supported Einstein-Skyrme collective band is the repository's strongest
candidate realization. The optical common-mode theorem is the faster fallback
if the one-action bridge does not close.
