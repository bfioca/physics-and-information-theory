# Local Worldtube Filter And Stabilized ULE Theorem

Status: exact stationary filter derivation, exact compact-support replacement,
and conditional ancilla-stable operator-norm ULE theorem. A profile-specific
interval certificate and matter-current derivation remain open. The finite
amplitude-ramp and burn-in theorem is supplied separately.

## Result

The Gaussian spectral regulator in the overlapping-sector model is not an
arbitrary frequency cutoff. On the optical spatial slice `H^3_R`, apply

```text
exp[(sigma^2/2)(Delta_H+R^-2)]                         (1)
```

to the field before taking the local orthonormal gradient. A mode with optical
spectral parameter `p=R|omega|` acquires amplitude

```text
H_sigma(omega)=exp(-sigma^2 omega^2/2).                (2)
```

The two-point spectrum therefore acquires exactly the factor
`exp(-sigma^2 omega^2)` used in the earlier executable ansatz.

The radial kernel is

```text
h_sigma(r)=(2pi sigma^2)^(-3/2)
           [(r/R)/sinh(r/R)] exp[-r^2/(2sigma^2)].     (3)
```

It is stationary and rotationally covariant, but positive at every finite
`r`. Thus it is quasilocal rather than supported in a bounded worldtube.

This distinction is unavoidable. The spherical transform of a compact radial
profile is entire of exponential type. The continuation of (2) to `p=i eta`
grows as `exp[sigma^2 eta^2/(2R^2)]`, faster than every fixed exponential type.
No compact stationary spatial smearing reproduces the exact Gaussian.

## Explicit Compact Replacement

Let `A=a/R` and use a normalized indicator of the optical ball of radius `a`.
Its spherical multiplier, normalized at zero spectral parameter, is

```text
q_A(p)=[cosh(A)sin(Ap)-p sinh(A)cos(Ap)]
       /[p(1+p^2)(A cosh(A)-sinh(A))],
q_A(0)=1.                                               (4)
```

Convolve two copies of the radial profile. The field smearing is supported in
optical radius `2a`, its amplitude multiplier is `q_A(p)^2`, and the regulated
gradient spectrum is

```text
j_A(omega)=j_0(omega) q_A(Romega)^4.                   (5)
```

This preserves exactly

```text
j_A(-omega)=exp(-2pi R omega)j_A(omega),
j_A(0)=1/(24pi^3R^3).                                  (6)
```

For `p>=1`,

```text
|q_A(p)| <= C_A/p^2,
C_A=[cosh(A)+sinh(A)]/[A cosh(A)-sinh(A)].             (7)
```

Consequently `j_A(+omega)=O(omega^-5)`. The equal-time gradient
variance and zero-Bohr Lamb integral are finite. In the standard Davies
convention,

```text
s_A=-(12pi^2R^3)^(-1)
    int_0^infinity (1+p^2)q_A(p)^4 dp.                 (8)
```

The executable evaluates (8) and separately reports the analytic omitted-tail
bound `(2/5)C_A^4 p_max^-5/(12pi^2R^3)`.

The ball indicator is an idealized finite-regularity source, analogous to a
hard wall. For a smooth compact spatial profile, choose a real radial
`f in C_c^infinity(H^3_R)` supported in `B_(a/2)` and smear with
`h=f^vee*f`. Its multiplier is `|F(p)|^2>=0`, its support lies in `B_a`, and
the spectrum is `j_0|F|^4`. The principal square root is smooth at zeros and
rapidly decreasing. All jump-correlator moments are finite. The elementary
closed formula (4) is then replaced by a one-dimensional spherical transform.
A genuine compact spacetime AQFT test function additionally needs a switching
function and therefore belongs to the finite-preparation/transient analysis.

## Bath Moments

Use the Nathan--Rudner convention

```text
g(t)=(2pi)^(-1/2) int sqrt[j(omega)]e^(-i omega t)domega,
G=int |g(t)|dt,
M_1=int |t g(t)|dt,
tau=M_1/G.                                              (9)
```

Let `q=sqrt(j)` and choose any positive time scale `T`. Weighted
Cauchy--Schwarz and Plancherel give the rigorous bounds

```text
G <= sqrt(pi T) sqrt(||q||_2^2+T^-2||q'||_2^2),
M_1 <= sqrt(pi T) sqrt(||q'||_2^2+T^-2||q''||_2^2).    (10)
```

Equation (7), thermal suppression at negative frequency, and smoothness at
zero imply the norms in (10) are finite for the double-ball filter. A smooth
compact convolution-square profile is Schwartz in spectral parameter and is
stronger still.

The code exposes (10) as the bridge from a profile-specific interval
quadrature to rigorous open-system constants. The default certificate uses
illustrative finite moment inputs only to verify dimension scaling; its output
labels the resulting schedules as illustrative and separately reports that
profile-specific ULE constants are not yet certified.
Independent upper bounds `G<=G_bar` and `M_1<=M_bar` do not imply
`tau<=M_bar/G_bar`. The rigorous residual instead substitutes them directly in
the monotone products `G M_1` and `G^3 M_1` appearing below.

## Ancilla-Stable ULE Bound

Normalize

```text
X_a=Q_a/(2L),
sqrt(gamma_NR)=2L lambda/N.                             (11)
```

The executable certificate uses the repository's integer-spin convention
`L in N`, `d=2L+1`. The analytic formulas extend to half-integer `L`, but that
API/test extension is not claimed here.

For three identical diagonal bath channels,
`||g(t)I_3||_(2,1)=3|g(t)|`. Nathan and Rudner's exact constants are therefore

```text
Gamma=144 lambda^2 L^2 G^2/N^2,
tau=M_1/G.                                              (12)
```

Their Appendix C modified state obeys

```text
||rho'-rho_exact||_infinity<=Gamma tau,
dot(rho')=L_ULE(rho')+xi',
||xi'||_infinity<=2Gamma^2 tau.                         (13)
```

Adjoin an arbitrary inert memory `A` and replace `X_a` by `X_a tensor I_A`.
All operator norms and bath constants are unchanged. At zero Bohr frequency
the jumps are Hermitian and the Lamb shift is Hamiltonian, so the ULE
Schrodinger semigroup is unital and contracts the operator norm on Hermitian
inputs. Duhamel's formula then gives, when the ULE is initialized at the
physical state,

```text
||rho_exact^(SA)(t)-(E_t tensor id_A)(rho_0^(SA))||_infinity
 <= 2Gamma tau+2Gamma^2 tau t.                         (14)
```

This is genuinely stable under an arbitrary spectator dimension. It is not a
diamond-norm theorem. It is exactly the norm needed by the Choi recovery
witness already derived in the overlapping-sector work package; the final
decoder transfer still costs `d epsilon_infinity`.

For one fixed finite compression, `u8a_finite_storage_channel.md` adds the
missing uniform-map quantifiers in the regular Gaussian-bath framework,
defines both channels from the common factorized pre-switch input, and converts
(14) with the explicit bound `floor(D_in D_out/2) epsilon_infinity`. Applying
that result to the named Bunch-Davies QFT is conditional on the open KMS
GNS/Araki-Woods bridge. The conversion is separate from (14) and does not make
the raw spectral estimate dimension free.

The collective heat rate is

```text
kappa=pi lambda^2 j(0)/N^2.                             (15)
```

At `kappa t=(1/2)log d`, (14) becomes

```text
epsilon_infinity <=
 288 G M_1 lambda^2L^2/N^2
 +[20736 G^3M_1/(pi j(0))]
   lambda^2L^4N^-2 log d.                              (16)
```

Thus an `A/d` spectral budget, with a fixed small prefactor `A`, has the exact
sufficient cap

```text
lambda <= N sqrt{
 (A/d)/[288L^2GM_1
       +20736L^4G^3M_1 log(d)/(pi j(0))]}.             (17)
```

For fixed regulator moments, `N~d^-1`, and `L~d`, this proves

```text
lambda=O[d^(-7/2)/sqrt(log d)]                         (18)
```

and guarantees the asymptotic recovery lower bound `1-A-o(1)`. Requiring the
ULE contribution to match the heat `O(1/d)` recovery correction is guaranteed
by imposing `epsilon_infinity=O(d^-2)`, which gives the sufficient schedule

```text
lambda=O[d^-4/sqrt(log d)].                            (19)
```

These are now conditional theorems with explicit constants, not dimensional
guesses.

## Hypotheses And Remaining Gates

The bound requires all of the following:

- a stationary, zero-mean Gaussian or quasifree bath;
- factorization of the entire system-memory state from the bath in the remote
  past;
- finite `G` and `M_1`;
- inclusion or controlled counterrotation of the collective Casimir Lamb
  shift;
- an inert memory and the zero-Bohr fixed-sector system Hamiltonian.

The finite-initialization rate correction `Gamma tau/(t-t_0)` is now integrated
in `static_patch_finite_switching_ule.md`. For an amplitude ramp with effective
lead `T_chi` and plateau burn-in `B`, it adds
`Gamma tau log(1+t/(B+T_chi))` to (14). This closes the prescribed finite-
preparation gate without changing the large-`d` schedules. It does not derive
the switch from the worldtube action. Merkli's all-time Davies theorem is not
directly applicable because the collective model is highly degenerate and has
dark sectors rather than a unique mixing stationary state.

The remaining physical gate is not the Markov scaling. It is to derive a
specific smooth compact optical profile and the collective coupling from a
finite matter worldtube action, then certify its Sobolev constants, switch-on,
direct target-reference interactions, support stress, lifetime, and gravity.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-worldtube-ule
PYTHONPATH=. python3 -m unittest tests.test_static_patch_worldtube_ule
```

Primary references:

- [Nathan and Rudner, Universal Lindblad equation, Appendices A--C](https://doi.org/10.1103/PhysRevB.102.115109), with the [2021 erratum](https://doi.org/10.1103/PhysRevB.104.119901)
- [Merkli, Dynamics of open quantum systems II](https://arxiv.org/abs/2105.00023)
- [Perche and Zambianco, derivative-coupled detectors](https://arxiv.org/abs/2305.11949)
- [Olafsson and Wolf, Paley--Wiener theorem for symmetric spaces](https://arxiv.org/abs/1101.4419)
