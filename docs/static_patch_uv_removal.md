# Static-Patch S-Wave Ultraviolet Removal

Status: rigorous s-wave quasifree UV-removal theorem; the successor
`static_patch_all_angular.md` closes equal-time angular wall removal, while
Lorentzian Hadamard and Type-III classification remain open

## Theorem

Let `F=(f,g)` and `G=(u,v)` be compactly supported real Cauchy data on the
static-patch tortoise half-line. Suppose their zero extensions have finite
`n`-th distributional derivative measures, with `n>=2`. Integration by parts
gives

```text
|fhat(k)| <= A_f,n/k^n,
A_f,n=sqrt(2/pi) ||D^n f||_TV.
```

For ordinary `W_0^{n,1}` data, total variation is replaced by
`||f^(n)||_1`. For `C_c^infinity` data this estimate holds at every order.

At inverse temperature `beta=2 pi R`, the full s-wave thermal covariance is

```text
mu(F,G)=1/2 int_0^infinity coth(beta k/2)
 [fhat uhat/k+k ghat vhat] dk.
```

Its omitted ultraviolet tail obeys

```text
|mu-mu_K| <= 1/2 coth(beta K/2)
 [A_f A_u/(2n K^(2n))
  +A_g A_v/((2n-2)K^(2n-2))].
```

The symplectic tail satisfies

```text
|sigma-sigma_K| <=
 [A_f A_v+A_g A_u]/[(2n-1)K^(2n-1)].
```

For the unequal-time two-point function, uniformly on the closed KMS strip
`0<=Im z<=beta`,

```text
|W(z)-W_K(z)| <= 1/2 coth(beta K/2)
 [A_f A_u/(2n K^(2n))
  +(A_f A_v+A_g A_u)/((2n-1)K^(2n-1))
  +A_g A_v/((2n-2)K^(2n-2))].
```

Uniform closed-strip convergence preserves analyticity in the open strip and
the KMS boundary identity. The diagonal covariance estimate also gives

```text
|exp[-mu(F,F)/2]-exp[-mu_K(F,F)/2]|
 <= |mu(F,F)-mu_K(F,F)|/2,
```

so the quasifree Weyl characteristic function has a well-defined UV limit.

## Infrared Lemma

Compact support gives the independent bound

```text
|hhat(k)| <= sqrt(2/pi) k int x|h(x)| dx.
```

This removes the apparent zero-frequency thermal singularity. In particular,
the field-field covariance integrand has the finite limit

```text
2 m_1(f)m_1(u)/(pi beta),
m_1(f)=int x f(x) dx.
```

Thus the UV estimates and the infrared lemma together establish absolute
convergence of the full s-wave covariance and KMS distributions.

## Executable Test Class

The implementation uses normalized compact bumps

```text
b(x)=N(x-a)^p(b-x)^p 1_(a,b)(x),  p=3.
```

Their zero extensions are `C^2`. The fourth distributional derivative is a
finite measure containing an interior polynomial density and endpoint atoms.
Consequently `|bhat(k)|=O(k^-4)`, and the worst momentum covariance and
closed-strip KMS tail is `O(K^-6)`. The symplectic tail is `O(K^-7)`.

## Locality Consequence

The unbandlimited equal-time symplectic form is the local canonical form

```text
sigma(F,G)=int(fv-gu) dx.
```

For disjoint compact supports it vanishes. A hard bandlimit produces a nonzero
tail, but the theorem bounds that leakage by `O(K^-(2n-1))`. Equal-time
canonical locality is therefore restored as `K` tends to infinity.

This is not yet spacetime microcausality or a four-dimensional local AQFT net.

## Order Of Limits

Together with the fixed-band stretched-wall Riemann theorem, the result proves

```text
lim_(K->infinity) lim_(delta->0)
```

for the s-wave symplectic, covariance, Weyl, and KMS data. A standard diagonal
argument selects a joint refinement sequence. Arbitrary joint paths
`K(delta)->infinity` are not claimed without a uniform finite-grid tail and
Riemann-error theorem.

## Successor And Remaining Gate

The successor theorem in `static_patch_all_angular.md` now supplies the exact
angular operators, wall-uniform angular covariance tails, all-angular
equal-time wall convergence, and the Euclidean conformal Bunch-Davies kernel
identity. Completion still requires:

1. all-angular ultraviolet estimates on compact spacetime tests;
2. unequal-time Lorentzian distributional convergence;
3. direct Hadamard boundary-value and wavefront-set control;
4. local-GNS identification and the Type-`III_1` theorem.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-uv-removal
PYTHONPATH=. python3 -m unittest tests.test_static_patch_uv_removal
```
