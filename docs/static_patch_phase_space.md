# Static-Patch S-Wave Phase-Space KMS Regulator

Status: fixed-UV quasifree phase-space/KMS theorem; UV removal, locality, and
all-angular Bunch-Davies identification open

## Canonical Data

For the conformally coupled massless s-wave, use the rescaled radial field on
the half-line in tortoise coordinate. A real equal-time phase-space datum is

```text
F=(f,g),  A_F=phi(f)+pi(g),
```

with canonical symplectic form

```text
sigma(F,G)=int_0^infinity [f g_G-g f_G] dx.
```

The executable theorem uses compactly supported `C^2` polynomial bumps. At
fixed momentum cutoff they can be replaced by any compact tests whose sine
transforms give continuous integrands. Smooth compact tests are required for
the later UV-removal theorem.

## Finite Stretched Patch

At stretched-horizon tortoise length `X`, impose Dirichlet conditions and set

```text
k_n=n pi/X,
e_n(x)=sqrt(2/X) sin(k_n x),
N=floor(KX/pi).
```

For mode coefficients `f_n=<e_n,f>` and `g_n=<e_n,g>`, the projected phase
space has

```text
sigma_XK(F,G)=sum_{n<=N} [f_n g_G,n-g_n f_G,n]
```

and thermal covariance at `beta=2 pi R`

```text
mu_XK(F,G)=1/2 sum_{n<=N} coth(beta k_n/2)
 [f_n f_G,n/k_n+k_n g_n g_G,n].
```

This is a finite-dimensional quasifree state on the quotient by the kernel of
the first `N` sine coefficients. Mode by mode,

```text
det covariance_n = coth(beta k_n/2)^2/4 >= 1/4,
```

so

```text
mu(F,F)mu(G,G) >= sigma(F,G)^2/4.
```

## Fixed-Band Continuum Limit

With the unitary sine transform

```text
fhat(k)=sqrt(2/pi) int_0^infinity sin(kx)f(x) dx,
```

the exact identity

```text
f_n=sqrt(Delta k) fhat(k_n),  Delta k=pi/X,
```

turns both finite forms into right Riemann sums. Hence, for fixed `K`,

```text
sigma_XK -> int_0^K [fhat ghat_G-ghat fhat_G] dk,
```

and

```text
mu_XK -> 1/2 int_0^K coth(beta k/2)
 [fhat fhat_G/k+k ghat ghat_G] dk.
```

The apparent thermal infrared singularity is removable because the sine
transform of a compact test is `O(k)` at the origin. The code uses the exact
zero-momentum limit and audits the Riemann convergence numerically.

## Unequal-Time KMS Identity

Define

```text
c_F(k)=fhat(k)/sqrt(2k)-i sqrt(k/2) ghat(k),
n_beta(k)=1/(exp(beta k)-1).
```

The fixed-band two-point function is

```text
G_FG(z)=int_0^K [(1+n_beta)c_F conjugate(c_G) exp(ikz)
                 +n_beta conjugate(c_F)c_G exp(-ikz)] dk.
```

It is analytic in the open strip `0<Im z<beta`, continuous on the closed
strip, and obeys

```text
G_FG(t+i beta)=omega(alpha_t(A_G) A_F).
```

The finite-box formula is the same Riemann sum. The implementation evaluates
the closed strip with exponentially decaying weights, avoiding artificial
overflow at high cutoff. At equal time it independently verifies

```text
G_FG(0)=mu(F,G)+i sigma(F,G)/2.
```

## What Is Proved

At fixed UV bandlimit and for each finite family of declared compact Cauchy
data:

- projected finite symplectic forms converge to the half-line forms;
- quasifree covariances converge;
- unequal-time two-point functions converge on the sampled KMS strip;
- finite and continuum fixed-band states satisfy the KMS boundary identity;
- the uncertainty condition holds.

The analytic convergence statement is the ordinary Riemann-sum theorem; the
certificate supplies reproducible numerical audits, not a replacement proof.

## Remaining Gate

A hard bandlimit is spatially nonlocal. This theorem therefore does not yet
construct a local Weyl net. The next proof must:

1. use smooth compact Cauchy data and remove `K` distributionally;
2. add every angular operator
   `h_ell=-d^2/dx^2+ell(ell+1)/(R^2 sinh^2(x/R))`;
3. control the low-frequency s-wave uniformly as the horizon wall is removed;
4. identify the limit directly with the Bunch-Davies two-point distribution;
5. then invoke the applicable Hadamard/AQFT theorem for the local Type-`III_1`
   algebra and form its continuous core.

No Bunch-Davies GNS identification, Hadamard theorem, Type `III_1`, Type-II
core, gravitational constraint, or generalized-entropy statement is claimed
here.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-phase-space
PYTHONPATH=. python3 -m unittest tests.test_static_patch_phase_space
```
