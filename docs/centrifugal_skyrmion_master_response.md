# Completed Skyrmion Quadrupole Master Response

This note composes the regular centrifugal branch, same-action bulk stress,
moving Nambu-Goto membrane, exact Zerilli-Moncrief source map, and fixed-de
Sitter Green kernel. It produces the first nonzero gauge-invariant master
response of the completed source in the repository's frozen convention.

## Normalization

All values below are dimensionless coefficients `psi0(x)` per

```text
kappa_hat=1
```

and per dimensionless quadratic angular-velocity harmonic

```text
q(n)=Q_ab n_a n_b.
```

They use the dimensionless Skyrme radius `x=e f_pi r` and dimensionless stress.
Here the dimensionless Einstein coupling is
`kappa_hat=8 pi G f_pi^2`. The older executable field name
`total_master_response_over_kappa` means `psi0`; it is not division by the
dimensionful `8 pi G`. Physical collective normalization is supplied in
`centrifugal_skyrmion_physical_response.md`.

For the default parameters

```text
mu=1,
lambda=0.0025,
R=20,
a=4,
sigma=0.001931779647,
```

the literal thin-shell master source at 401 nodes contains

```text
D_2 delta'' =-0.0013923102731 delta'',
D_1 delta'  = 0.0024220397459 delta',
D_0 delta   =-0.0018179198616 delta.
```

The corresponding contact in the metric-defined master is removed for
off-wall evaluation. The equivalent source has

```text
D_1^off= 0.0024510462099,
D_0^off=-0.0023617910621,
```

with no `delta''` term. This subtraction does not change the response away from
the membrane.

## Response

The 401-node result is

| Radius | Bulk `psi0` | Wall `psi0` | Total `psi0` |
|---:|---:|---:|---:|
| 1 | -0.22087479 | -1.3839e-5 | -0.22088863 |
| 2 | -0.33010058 | -1.1143e-4 | -0.33021201 |
| 3 | -0.17580950 | -3.8019e-4 | -0.17618969 |
| 5 | -0.06401031 | -2.2029e-3 | -0.06621317 |
| 10 | -0.01498114 | -5.1556e-4 | -0.01549670 |

The response is finite, nonzero, and has a stable sign at these off-wall
sample points. The membrane contribution is small in the interior but is kept
because it is required for exact conservation and becomes a few percent just
outside the wall.

## Refinement

The `401`- to `801`-node maximum relative response change is
`1.0631e-4`. Changing the origin cutoff from `0.02` to `0.01` changes the
response by `2.9872e-5`, and refining the background profile step from `0.002`
to `0.001` changes it by `2.8720e-7`.

This is the positive-construction branch anticipated by the universal observer
program: the invalid rigid source is replaced by a regular same-action
matter-wall deformation, its full distribution is conserved, and its
gauge-invariant master response is nonzero.

## Claim Boundary

This is still not a physical prediction in SI or de Sitter units. It remains a
floating fixed-background coefficient because it lacks:

1. interval validation of the coupled nonspherical BVP and response integral;
2. Israel matching and response on the spherically deformed background;
3. higher-order rotation and collective-band projection control;
4. reconstruction of an off-wall Weyl scalar or operational worldtube
   observable;
5. an independent sourced Kodama-Ishibashi convention cross-check.

The result therefore upgrades the Skyrmion from an existence candidate to an
explicit conserved gravitational-response construction, but it does not yet
complete the universal localization-reference-backreaction theorem.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_master_response_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_master_response.py \
  tests/test_centrifugal_skyrmion_master_response_audit.py
```

The source-hashed artifact is
`experiments/centrifugal_skyrmion_master_response_certificate.json`, SHA-256
`07c66bb0731588a268db1398f9714746dd43b1e666867d004ee472e525873437`.
