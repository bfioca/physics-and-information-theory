# Higher-Spin Static-Patch Gradient Obstruction

## Result

The polarization-resolved gradient channel admits an exact singlet witness for
every integer spin `L`, not only spin one half. Let

```text
delta_parallel=1-c_parallel,
delta_perp=1-c_perp,
Delta=delta_parallel+2 delta_perp,
```

and let `P_L` be the unique total-spin-zero state in `V_L tensor V_L`. The ideal
collective generator fixes `P_L`. For the separated gradient generator,

```text
(1/2)||E_s-E_s^collective||_diamond
 >= 1-Tr[P_L E_s(P_L)].
```

This is a channel-comparison witness. The singlet is an allowed diamond-norm
probe, but it is not a product-prepared target/reference input.

## Exact Tensor-Rank Reduction

The operator representation decomposes as

```text
End(V_L)=direct_sum_(ell=0)^(2L) V_ell.
```

The singlet projector has one scalar component in each equal-rank block
`V_ell tensor V_ell`. Axial gradient anisotropy preserves total magnetic number
zero. Consequently, its survival probability is exactly

```text
p_L(s)=sum_(ell=0)^(2L) (2ell+1)/d^2
        <s_ell|exp(s B_ell)|s_ell>,
d=2L+1,
```

where `s_ell,m=(-1)^(ell-m)/sqrt(2ell+1)` and `B_ell` is the real symmetric
tridiagonal matrix

```text
(B_ell)_(m,m)=-2ell(ell+1)+2 c_parallel m^2,

(B_ell)_(m+1,m)
=-c_perp(ell-m)(ell+m+1).
```

The largest block has size only `4L+1`, rather than the `d^4` dimension of the
full Liouvillian. The repository evaluates these blocks with a dependency-free
symmetric Jacobi diagonalization and checks the independent-bath and perfect-
common-mode limits.

## Uniform Local Theorem

Write the generator in collective and relative charges,

```text
Q_a=L_a+J_a,    D_a=L_a-J_a.
```

Expanding at perfect common mode gives the exact finite-time first variation

```text
1-p_L(s)
=(4/3)L(L+1)s Delta + remainder.                       (1)
```

This is not merely an initial-time derivative. The ideal semigroup is self-
adjoint and fixes the singlet, so collective evolution before and after the
single perturbation insertion drops out.

The Hilbert-Schmidt superoperator estimate

```text
||G_delta-G_0||_(2->2)<=8 L^2 Delta
```

gives the uniform remainder bound

```text
|remainder|<=32 s^2 L^4 Delta^2.                       (2)
```

In particular, if

```text
Delta<=(L+1)/(48 s L^3),
```

then the exact mismatch is at least one half of the linear term.

## Growing-Sector Scaling

For the optical Bunch-Davies gradient kernel,

```text
Delta=(3/2)y^2+O(y^4),    y=d_H/R.
```

Equations (1)-(2) therefore give

```text
1-p_L(s)=2L(L+1)s y^2+O(sL^2y^4+s^2L^4y^4).           (3)
```

Take the protected sector dimension itself to be `d=2L+1`, use the sufficient
schedule `s=(1/2)log d`, and allocate mismatch `A/d`. Then the leading necessary
co-location law is

```text
y<=sqrt[A/(d L(L+1) log d)]
 =O[d^(-3/2)/sqrt(log d)].                             (4)
```

At the scaling (4), `sL^2Delta=O(1/d)`, so the explicit remainder is lower
order. This is parametrically stronger than the fixed-spin witness
`O[d^(-1/2)/sqrt(log d)]`.

For equal-shell supports near the horizon, the earlier optical geometry turns
(4) into the corresponding angular co-location bound after multiplication by
`rho/R` at leading order.

## Scope

This closes the growing integer-spin calculation inside the declared
Markovian gradient GKSL model. It does not yet establish:

- a smooth local hard-target/finite-top matter action producing the coupling;
- a Davies approximation uniform as `L` grows;
- derivative-field smearing and renormalization uniform in `L`;
- admissibility of the entangled singlet witness in a product-prepared
  reference protocol;
- a joint localization, lifetime, support-stress, and gravitational
  backreaction window.

The tensor-rank decomposition and Casimir identities are standard. The
candidate contribution is the collision between their exact channel witness,
the finite-reference `A/d` recovery budget, and the near-horizon optical
geometry.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-higher-spin-gradient
PYTHONPATH=. python3 -m unittest tests.test_static_patch_higher_spin_gradient
```

Implementation: `qgtoy/static_patch_higher_spin_gradient.py`.
