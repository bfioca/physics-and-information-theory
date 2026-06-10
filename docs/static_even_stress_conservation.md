# Static Even-Parity Stress Conservation

This note isolates a kinematic gate that every static gravitational-response
calculation in the program must pass. It is independent of the Skyrme model.

## Conventions

On the `(-+++)` static spherical background

```text
ds^2 = -f(r) dt^2 + dr^2/f(r) + r^2 dOmega^2,
```

decompose one scalar harmonic with `L=ell(ell+1)` as

```text
delta T^t_t = -rho Y,
delta T^r_r = p_r Y,
delta T^r_A = j D_A Y,
delta T^A_B = p_perp Y delta^A_B + pi Y^A_B,
Y^A_B = D^A D_B Y + (L/2) delta^A_B Y.
```

The tensor harmonic is trace free. Direct evaluation of
`nabla_mu T^mu_nu=0` gives the two exact bulk equations

```text
p_r' + f'(rho+p_r)/(2f) + 2(p_r-p_perp)/r
     - L j/(f r^2) = 0,

j' + 2j/r + p_perp - (L-2)pi/2 = 0.
```

For a static quadrupole with `ell=2` and `j=0`, angular conservation therefore
requires the algebraic identity

```text
p_perp = 2 pi.
```

This is a useful early rejection test: a proposed collection of source
amplitudes that violates it cannot be inserted consistently into a static
Zerilli equation.

## Hard-Wall Completion

Hard truncation at `r=r_w` creates distributional terms. Multiplication by
`Theta(r_w-r)` gives the conservation delta coefficients

```text
C_r^delta = -p_r(r_w),
C_A^delta = -j(r_w).
```

Thus either the bulk traction must vanish or a membrane stress must cancel
these coefficients through its intrinsic divergence and normal-force balance.
Checking only the smooth interior equations is insufficient.

## Scope

This result is a conservation checker, not a matter model. It neither derives
the amplitudes from the `(+---)` Skyrme action nor constructs a membrane. Its
role is to keep gauge-invariant response calculations tied to a conserved,
same-action source.

## Reproduction

Run

```bash
python experiments/static_even_stress_conservation_audit.py
python -m pytest -q tests/test_static_even_stress_conservation.py \
  tests/test_static_even_stress_conservation_audit.py
```

The exact certificate is
`experiments/static_even_stress_conservation_certificate.json`, with SHA-256
`ffdd21d1ca7e5c33df825bb7f0ba57b0d816916f34f1ea23e383f804c7299856`.
