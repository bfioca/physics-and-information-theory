# Global Centrifugal Friedrichs Form

Status: certified conditional theorem for the declared fixed-background
matter-plus-moving-membrane action.

## Statement

Let `a=4`, `y=(f,g)`, and let the static quadrupole form have the coefficient
scaling

```text
P=x^2 Pbar,   M=x Mbar,   K=x Kbar.
```

The authenticated origin and outer profile families prove that the completed
Liouville potential obeys `W_K >= (1/100)I` on all of `[0,a]`. The wall
certificate proves that the allowed `f(a)` trace remainder is positive.

On

```text
H = L2((0,a);R^2),
V = {y in H : y in AC_loc((0,a]), x y' in H, g(a)=0},
```

the closure of the smooth core `C-infinity([0,a];R^2)` with `g(a)=0`
defines a dense, symmetric, closed form satisfying

```text
q[y] >= (1/100) ||y||_H^2.
```

Consequently the first representation theorem gives a positive
self-adjoint operator `A`; zero lies in its resolvent and

```text
||A^-1||_(H -> H) <= 100.
```

The wall operator condition is `g(a)=0` together with the natural `f`
conormal law, which is equivalent to `f'(a)=beta f(a)` in the declared
moving-membrane model.

## Endpoint And Join

The graph norm of `V` is `||y||_H^2+||x y'||_H^2`. Under

```text
s=log(a/x),   (Uy)(s)=sqrt(x)y(x),
```

`U` identifies `V` with the half-line `H1` space satisfying `(Uy)_g(0)=0`.
An origin cutoff therefore has vanishing graph-norm cost, so smooth functions
which vanish near `x=0` are already dense. No center trace is imposed.
Moreover `sqrt(x)y(x)` tends to zero, and hence the completion boundary term
`y^T K y` vanishes because `K=x Kbar`. The Friedrichs operator domain, rather
than an added form trace, selects the finite-energy origin germs.

The split at `x=3/16` is only a certificate partition. Elements of `V` are
locally `H1` there and the coefficient formulas are common on both sides, so
no interface trace term or matching condition is introduced.

Uniform upper coefficient bounds make the form continuous on `V`. Uniform
positivity of `Pbar`, boundedness of the completed first-order multiplier,
and the `W_K` lower bound make the completed-square norm equivalent to the
graph norm. This supplies closedness as well as semiboundedness.

## Evidence And Boundary

The source-hashed artifact is
`experiments/centrifugal_skyrmion_friedrichs_form_certificate.json`, SHA256
`4a4e3ecd48a205860de3aa045c94d2b825c0afce1c0f12f4b96254db355b85bb`.
It composes the authenticated origin artifact SHA256
`daa220e68ceef034a1b23ea955033dc08c0e776ee49628eb07acb0834b57c065`
and outer artifact SHA256
`c8744dd4136b607595a42de1ada271644c8408b0fff6b4a2629bf749ea136b91`.

This result certifies the operator and its `L2` inverse bound only for the
declared fixed-de Sitter weak form. The logarithmic half-line representation
does not imply compact resolvent. The static Hessian bound is not a kinetic
mode-frequency gap. A derivative-coupled physical source may lie in `V*`, so
the `L2` inverse constant alone does not certify its response. Tensorial Israel
matching and a backreacted Einstein-matter solution also remain open.

The next certificate must enclose `A^-1 s` tightly enough that a physical
response functional excludes zero despite the honest inverse constant `100`.
