# Rigid Skyrmion Stress Conservation No-Go

The leading fixed-profile rotating hedgehog does not furnish a conserved
static `ell=2` Einstein source at quadratic order in angular velocity. This
closes an invalid shortcut in the gravitational-discriminator program: the
exact static response kernel cannot be applied until the centrifugal matter
and wall response has been solved.

## Stress Convention

The Skyrme work package uses signature `(+---)` and the positive-energy Hilbert
convention

```text
T_mu_nu = +2/sqrt(-g) delta S_m/delta g^(mu nu).
```

The gravitational perturbation package uses `(-+++)` mixed components. The
formulas below first compute physical orthonormal density and pressure, then
translate them into that response convention.

Set

```text
N = 1-r^2/R^2,  s=sin F,  a^2=N F'^2,  b^2=s^2/r^2,
k_2=f_pi^2 s^2/(8N),  k_4=s^2/(2e^2 N).
```

For `w_A=(Omega cross n)_A` and
`w^2=Omega^2-(n dot Omega)^2`, the complete fixed-profile rotational stress is

```text
delta rho  = [k_2+k_4(a^2+b^2)] w^2,
delta p_r  = [k_2+k_4(b^2-a^2)] w^2,
delta T_AB = [k_2+k_4(a^2-b^2)] w^2 gamma_AB
             + 2k_4 b^2 w_A w_B,
delta T_rA = delta T_0r = 0,
delta T^t_A = -2[k_2+k_4(a^2+b^2)] w_A.
```

The last term is an odd `ell=1` component at first order in `Omega`. Its sign
depends on the angular-velocity convention. The radial integral of the energy
coefficient reproduces the moment-of-inertia density already used by the
collective Hamiltonian.

## Quadrupole Amplitudes

For a stationary mean-zero collective state, define

```text
S_ab = <{J_a,J_b}>/2,
C = Tr S,
Q_ab = S_ab-(C/3)delta_ab,
q(n) = Q_ab n^a n^b.
```

In the static-response convention, the coefficients multiplying `q/I^2` are

```text
rho    = -[k_2+k_4(a^2+b^2)] q/I^2,
p_r    = -[k_2+k_4(b^2-a^2)] q/I^2,
p_perp = -[k_2+k_4 a^2] q/I^2,
pi     = -k_4 b^2 q/I^2,
j      = 0.
```

## Conservation Obstruction

Because `j=0`, quadrupole conservation requires `p_perp=2pi`. Instead the
angular residual is

```text
C_A = -[k_2+k_4(a^2-2b^2)] q/I^2,
```

which is generically nonzero. The radial residual is

```text
C_r = -(2k_4 F' q/I^2)
      [(e^2 f_pi^2/4+2b^2-a^2)cot F-NF''-2NF'/r].
```

The static profile equation does not cancel these residuals. This is the
expected Hilbert-identity diagnosis: a time-dependent collective rotation of
an undeformed static profile does not solve the full matter equation at
`O(Omega^2)`.

The hard-wall limit makes the obstruction strict. If
`F=sigma(r_w-r)+O((r_w-r)^2)` with nonzero `sigma`, then

```text
C_A = -[sigma^2/(N_w I^2)]
      [f_pi^2/8+N_w sigma^2/(2e^2)]
      q (r_w-r)^2 + O((r_w-r)^3).
```

The coefficient is strictly negative. Since every fixed-profile rotational
traction also vanishes at the ideal Dirichlet wall, no omitted wall delta term
can repair this bulk failure.

## Required Replacement

The next admissible source calculation must do one of the following:

1. Solve the `O(Omega^2)` centrifugal profile response together with the
   nonspherical membrane displacement and stress, then verify bulk and shell
   conservation before projecting into the static master equation.
2. Retain the time-dependent matter stress and use a dynamical gravitational
   response.
3. Restrict to a state with `Q=0`, in which case this leading quadrupole source
   vanishes; this does not by itself supply an orientation reference because
   stabilizer risk can remain order one.

The result does not exclude a conserved deformed rotating Skyrmion. It says
that the rigid fixed-profile approximation cannot be used as the claimed
gauge-invariant gravitational discriminator.

## Reproduction

Run

```bash
python experiments/rigid_skyrmion_stress_conservation_audit.py
python -m pytest -q tests/test_rigid_skyrmion_stress_conservation.py \
  tests/test_rigid_skyrmion_stress_conservation_audit.py
```

The exact certificate is
`experiments/rigid_skyrmion_stress_conservation_certificate.json`, with
SHA-256
`a91577f62a2992f3aca8c7ffe9af171c6c5759a0dcff80550c3dff5240286bfe`.
