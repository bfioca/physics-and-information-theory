# Why Energy Density Alone Cannot Bound Einstein Response

Status: exact gauge obstruction plus local-flat conserved-stress no-go

## Two Necessary Inputs

A nonspherical backreaction theorem needs both:

1. a gauge-invariant output, or a gauge condition with a proved reconstruction
   estimate; and
2. a response-compatible norm of the full conserved stress tensor.

The existing rotational theorem bounds the leading `l=2` energy-density
source. That is useful, but it supplies neither item by itself.

## Gauge Obstruction

Let `g` be any Einstein background and let `xi` be a compactly supported vector
field. Diffeomorphism covariance gives

```text
h_ab=L_xi g_ab
  => delta(G_ab+Lambda g_ab)[h]=0.
```

Scaling `xi` scales every coordinate-component norm of `h` while its source
remains zero. Therefore no inequality of the form

```text
||h||_coordinates <= C ||delta T||
```

can hold before gauge is fixed or pure gauges are quotiented. Suitable outputs
include a master variable, linearized Weyl curvature, induced worldtube
geometry, or a horizon curvature multipole.

## Density-Only Obstruction

The second failure persists for gauge-invariant curvature. In the local
Minkowski limit, choose any smooth compactly supported scalar `chi` and define

```text
T_00=0,
T_0i=0,
T_ij=A(delta_ij Delta-partial_i partial_j)chi.      (1)
```

Commuting derivatives gives exact conservation:

```text
partial_i T_ij
 =A(partial_j Delta-Delta partial_j)chi=0.          (2)
```

But

```text
T=2A Delta chi,
R^(1)=-8 pi G T=-16 pi G A Delta chi.              (3)
```

Thus the energy-density norm is identically zero while a gauge-invariant
curvature response is nonzero and can be scaled arbitrarily. Taking
`chi=f(r)Y_2m` with a compact radial bump makes the trace and curvature in (3)
quadrupolar.

This rules out every density-only response inequality claimed uniformly in
the small-worldtube limit `a/R -> 0`. It does not rule out a finite response
bound for the complete conserved Skyrmion stress.

## Replacement Gate

For a static even-parity source, the response input must control the amplitudes

```text
rho, p_r, p_perp, j, pi,
```

representing density, radial and tangential pressure, radial-angular shear,
and trace-free angular stress. They must satisfy the two background
conservation equations and include the membrane traction distribution. A hard
bulk truncation without that wall term is not an admissible Einstein source.

Only after this ledger is derived from the same rotating Skyrme-worldtube
action may it be projected onto the static-patch Zerilli source.

## Reproduction

```bash
python experiments/density_only_einstein_response_no_go_audit.py
python -m pytest -q tests/test_density_only_einstein_response_no_go.py \
  tests/test_density_only_einstein_response_no_go_audit.py
```

Artifact:

```text
experiments/density_only_einstein_response_no_go_certificate.json
SHA256 54d4d33642198274f656fc1e87ea631a5b7dead8ec18da4dbfdd58f2d57f7b7c
```
