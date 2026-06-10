# Distributional Centrifugal Membrane Stress

This note completes the fixed-background `O(Omega^2)`, `ell=2` conservation
audit for the supported Skyrmion by including the moving Nambu-Goto membrane.
The result is an exact distributional factorization plus source-hashed floating
closure on the default BVP. It is not an Israel-matched self-gravitating shell.

## Moving Shell

Let the membrane be

```text
r=a+xi q(n),
```

with outward normal from the interior. Its covariant delta distribution is

```text
delta_Sigma=sqrt(N(r))[delta(r-a)-xi q delta'(r-a)]+O(xi^2),
```

and its mixed stress is

```text
T^mu_nu=-sigma(delta^mu_nu-n^mu n_nu)delta_Sigma.
```

In the repository's static even-parity convention, the shape multipole is

```text
rho_Sigma=sigma xi[N'/(2sqrt(N)) delta-sqrt(N) delta'],
p_r,Sigma=0,
j_Sigma=-sigma xi sqrt(N) delta,
p_perp,Sigma=-rho_Sigma,
pi_Sigma=0.
```

The `delta'` term is not an independent dipole layer. It is the fixed-coordinate
expansion of an ordinary delta layer displaced to the nonspherical membrane.

## Curvature Identity

Define

```text
K=N'/(2sqrt(N))+2sqrt(N)/r,
k_l=K'(a)+l(l+1)/(a^2sqrt(N_a)).
```

Applying the exact static conservation operator distributionally gives

```text
C_r,Sigma=-sigma xi K delta'+sigma xi k_l delta,
C_A,Sigma=-sigma xi K D_Aq delta.
```

The executable derives these coefficients directly from the shell amplitudes
and checks their equality to the curvature form. This is the component identity

```text
nabla_mu T^mu_nu,Sigma=sigma K_Sigma n_nu delta_Sigma.
```

## Moving Bulk Layer

The interior stress is multiplied by `Theta(a+xi q-r)`. Its Eulerian first
variation therefore contains the singular background layer

```text
xi q T0^mu_nu(a) delta(r-a).
```

Combining this layer, the intrinsic bulk quadrupole, and the membrane reduces
all distributional coefficients to four physical residuals:

```text
C_r^(delta')=xi[p_0-sigma K],
C_r^(delta) =-[p_r,2+xi p_0'-sigma k_2 xi]
              +xi C_r,background,
C_A^(delta')=0,
C_A^(delta) =-[j_2-xi(p_perp,0-p_0)]+xi[p_0-sigma K].
```

Thus conservation is equivalent to centered Young-Laplace balance, smooth
background conservation, and the linearized normal and tangential traction
conditions

```text
p_0=sigma K,
p_r,2+xi p_0'=sigma k_2 xi,
j_2+xi(p_0-p_perp,0)=0.
```

For the hard-wall hedgehog, `p_perp,0=-p_0`, the ideal mirror gives
`f(a)=-F'_w xi` and `g(a)=0`, and the completed stress gives

```text
j_2(a)=N F'_w f(a)/4=-N F_w'^2 xi/4.
```

The tangential condition then vanishes identically. The normal condition is
exactly the moving-wall Robin law already used by the global BVP, so this audit
is an independent distributional interpretation of that boundary condition.

## Default Closure

Across `101`, `201`, `401`, and `801` BVP nodes, the largest absolute
distributional conservation coefficient lies between `1.16e-12` and
`1.19e-12`. The tangential-force residual is zero at floating precision, the
Young-Laplace residual is `4.71e-14`, and the algebraic factorization error is
below `6e-20`.

This closes the fixed-background bulk-plus-shell conservation gate for the
default branch. It does not provide:

1. an interval proof of the profile or coupled BVP;
2. Israel junction conditions or a self-consistent metric;
3. surface elasticity, an exterior medium, or a mirror-sector UV completion;
4. collective projection or a conserved Zerilli master-source map.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_membrane_stress_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_membrane_stress.py \
  tests/test_centrifugal_skyrmion_membrane_stress_audit.py
```

The source-hashed artifact is
`experiments/centrifugal_skyrmion_membrane_stress_certificate.json`, SHA-256
`1ef92b3579f60fe52d2849d3da3202dc55be33be538b401117218f81cdea53aa`.
