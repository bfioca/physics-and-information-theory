# Centrifugal master primal-adjoint feasibility

This floating audit asks whether the certified matter inverse could plausibly
be extended to a validated nonzero exterior Zerilli--Moncrief amplitude.

On the symmetric piecewise-linear matter space it writes

```text
K y = ell,
K z = b,
J(y) = J_rigid + B(y) = J_rigid + b^T y.
```

`J_rigid` is the exterior horizon-regular amplitude of the undeformed rotating
stress. The deformation functional `B` is assembled by passing every Galerkin
basis field through the existing completed-stress, moving-membrane, canonical
master-source, and de Sitter Green-response maps. The wall displacement is
`xi = gamma_xi f(a)` with `gamma_xi = -1/F'(a)`. This displacement coefficient
is distinct from the much smaller effective master-response wall trace
coefficient used in the analytic reduction.

A coarse primal and adjoint are interpolated into a nested fine space. With
fine residuals `r_y` and `r_z`, the corrected estimator is

```text
J_hat = J_rigid,fine + B_fine(y_coarse) + r_y^T z_coarse,
|J_fine - J_hat| <= ||r_y||_{K^-1} ||r_z||_{K^-1}.
```

The audit reports whether this floating residual product excludes zero. This
is a feasibility test, not a continuum or interval certificate. In particular,
the fine discretization is only a reference problem, the first radial element
is omitted from the master-source integral, and profile interpolation,
quadrature, stress-to-master conversion, and residual norms are not enclosed.

For the source-hashed default `41 -> 81` run,

```text
J_hat                              = -0.002818947812,
delta_y delta_z                    =  0.0000450997164,
product/|J_hat|                    =  0.0159988,
distance from zero after the bound =  0.002773848096.
```

The saved artifact is
`experiments/centrifugal_skyrmion_master_adjoint_feasibility.json`, SHA256
`584a22ea3ae9807dcc9da8cd6cc20274c943c52bb23c38923cbe8e6dcf986bf7`.
