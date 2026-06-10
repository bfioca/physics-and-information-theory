# Static-Patch Scalar Common-Mode Test

Status: named local Bunch-Davies scalar-bath obstruction in an equal-redshift
axial Davies surrogate; the actual hard-angular-target/top torque channel,
finite-memory control, and backreaction remain open

## Local Interaction Surrogate

Place two localized axial charges `q_T,q_R` at static-patch points `x_T,x_R`
on the same static shell and couple their zero-Bohr secular components locally
and stationarily to the conformally coupled Bunch-Davies scalar:

```text
H_I(t)=lambda
 [q_T(0) phi(t,x_T)+q_R(0) phi(t,x_R)].                  (1)
```

The charges are assumed to have exchanged-charge gap `Delta>0`, identical
coupling strengths, charge normalization, and spatial profiles. Equivalently,
the coupled operators commute with their free Hamiltonians or are replaced by
their Davies zero-frequency components. The equal-shell condition gives a
common redshift, so one Killing-time weak-coupling/Davies limit can be compared
with the proper-time diffusion model after a single rescaling.

Equation (1) is the stationary, long-time weak-coupling surrogate. Finite
switching replaces the exact zero-frequency coefficient below by a
`|chi_hat(omega)|^2`-weighted spectral average. A point coupling in four
dimensions is distributional, so a microscopic theorem also needs spatial
smearing or a renormalized detector construction.

This is not yet the desired field-top interaction. It replaces the hard angular
target and finite spherical top by localized axial charges so that the bath
covariance can be calculated exactly.

## Exact Zero-Frequency Correlation

The optical Bunch-Davies Wightman kernel already established in
`static_patch_lorentzian_hadamard.md` has spectral representation

```text
G_opt^+(t;d_H)
 =int_0^infinity dk
  sin(k d_H)/[4 pi^2 R sinh(d_H/R)]
  [e^(-ikt)+e^(-2 pi R k)e^(ikt)]/[1-e^(-2 pi R k)].     (2)
```

At coincidence, the spatial factor is `k/(4 pi^2)`. For pointlike profiles, the
normalized cross spectrum at positive frequency `k` has spatial ratio

```text
c_k(d_H)=sin(k d_H)/[k R sinh(d_H/R)].                   (3)
```

The zero-Bohr-frequency Davies sector uses the exact limit

```text
c_0(y)=lim_(k->0)c_k=y/sinh(y),
y=d_H/R.                                                  (4)
```

This conclusion does not depend on the thermal occupation factor, which cancels
in the normalized ratio. For every fixed `y>0`,

```text
0<c_0(y)<1.
```

Thus the Bunch-Davies scalar supplies correlated noise, but not the rank-one
common mode at separated supports.

For general finite profiles, (4) is replaced by a double-smeared spectral ratio.
However, `static_patch_radial_smearing.md` proves an exact improvement: for any
nonnegative stationary profiles radial in the optical `H^3_R` measure, the
profile amplitudes factor and cancel, so the normalized zero-frequency
coefficient remains exactly (4), independently of profile size and radial
shape. The profiles need not be equal.

The relevant geometric width is optical rather than proper. Near the horizon,
a body of proper size `a` at proper horizon distance `rho` has

```text
optical width/R=O(a/rho).
```

A collar-following apparatus with `a=alpha rho` therefore has order-`alpha`
optical width rather than a profile that becomes pointlike automatically.
Radial width nevertheless cannot rescue the common mode because of the exact
spherical-function factorization. Nonradial profile components remain open.

The spectral form (2) follows from the exact static-patch kernel and the
de Sitter analytic/KMS results of
[Bros, Epstein, and Moschella](https://arxiv.org/abs/gr-qc/9801099). The use of
spatial bath correlations as the criterion for collective dephasing follows the
standard mechanism in
[Palma, Suominen, and Ekert](https://arxiv.org/abs/quant-ph/9702001).
Static-patch two-atom GKSL dynamics driven by a massless scalar, including
Wightman-derived Kossakowski coefficients and entanglement diagnostics, was
already studied by
[Akhtar et al.](https://arxiv.org/abs/1908.09929). Therefore the bath spectrum
or separated-detector open-system setup is not a novelty claim here.

## Channel Obstruction

Insert (4) into Research Theorem Z. At dimensionless protocol time
`s=gamma T`, the localized relational coherence gives

```text
eta_scalar(y,s)
 >= [1-exp(-2s Delta^2[1-y/sinh(y)])]/2.                 (5)
```

At fixed nonzero `y`, (5) tends to `1/2` as `s` grows. Therefore a fixed
separation cannot remain an accurate realization of the ideal common-mode
channel along the sufficient heat schedule `s=(1/2)log d`.

For an allocated mismatch `A/d`, the correlation-defect condition is

```text
1-y/sinh(y)
 <= D_d:=-log(1-2A/d)/(Delta^2 log d).                  (6)
```

Since

```text
sinh(y)>=y+y^3/6,
1-y/sinh(y)>=y^2/(6+y^2),                               (7)
```

(6) necessarily implies the rigorous bound

```text
y<=sqrt[6D_d/(1-D_d)]
 =O(1/[Delta sqrt(d log d)]).                           (8)
```

The implementation also inverts `y/sinh(y)` numerically, yielding a slightly
sharper exact maximum separation.

## Near-Horizon Angular Co-Location

Let both supports lie on a static shell at proper distance `rho` from the
horizon and angular separation `theta`. On the optical `H^3_R` slice,

```text
cosh(y)
 =1+2 cot^2(rho/R) sin^2(theta/2).                       (9)
```

For a maximum allowed optical distance `y_max`, the exact angular window is

```text
theta_max
 =2 asin[sinh(y_max/2) tan(rho/R)],                      (10)
```

capped at `pi`. In the joint small-`rho`, small-`y_max` regime,

```text
theta_max
 =O[(rho/R)/(Delta sqrt(d log d))].                     (11)
```

If the hard-energy collar dimension obeys `d=Theta(sqrt(R/rho))`, then

```text
theta_max
 =O[(rho/R)^(5/4)/sqrt(log(R/rho))]                     (12)
```

for fixed `Delta`. The scalar bath can approximate the ideal common mode only
for increasingly co-located same-shell supports. A fixed angular separation
fails the `A/d` allocation.

## Meaning For Paper C

This is the first calculation in the program that starts from a named local
static-patch KMS field rather than stipulating a common stochastic rotation. It
does not validate the proposed heat-twirl bridge. It rules out one natural
realization of that bridge at fixed support separation and turns Paper C toward
a sharper fork:

1. find a global/long-range mode, gauge constraint, or co-located coupling that
   makes the relevant torque covariance approach rank one fast enough; or
2. publish a no-go showing that a declared class of local finite observers
   cannot realize the append-and-twirl surrogate on the growing collar sector.

The current result supports the second direction only for the axial localized
scalar-bath surrogate.

The candidate new contribution is narrower than the scalar open-system
calculation: combine its exact spatial coefficient with the all-state finite
reference recovery obstruction, the sufficient heat schedule, and the
geometry-derived growing hard sector to obtain the optical/angular co-location
scalings (8), (11), and (12). That combination still needs a dedicated
prior-art search and external expert review.

## Claim Boundary

Established:

1. the exact normalized zero-frequency correlation `c_0(y)=y/sinh(y)` from the
   Bunch-Davies optical spectral kernel;
2. the fixed-separation channel-mismatch floor in the axial Davies model;
3. the exact correlation-defect inversion and rigorous optical bound (8);
4. the same-shell static-patch geometry (9)-(10);
5. the near-horizon angular co-location scaling (11), and (12) after inserting
   the declared hard-sector dimension law;
6. persistence of the normalized coefficient for arbitrary nonnegative optical-
   radial finite smearings, by the separate spherical-function theorem.

Not established:

1. that the hard angular Bunch-Davies target is a localized axial charge;
2. a local rotationally invariant coupling to a finite spherical top;
3. the full three-axis torque spectral matrix or noncommuting `SO(3)` Davies
   generator;
4. finite switching, optical-smearing, Lamb-shift, and Markov approximation
   errors;
5. the diffusion rate and hierarchy
   `max(a,tau_B)<<T<<min(tau_life,tau_recurrence)`;
6. observer stress-energy, horizon displacement, or gravitational backreaction;
7. a no-go for massless, critical, gauge, or explicitly global bath modes in
   general.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-scalar-common-mode
PYTHONPATH=. python3 -m unittest tests.test_static_patch_scalar_common_mode
```
