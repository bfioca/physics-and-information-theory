# Validated Centrifugal Liouville Origin

## Regular Formulation

Set

```text
t=x^2, F=pi-xu, p=-F', h=1-lambda t,
s=sin(xu)/x, c=cos(xu), D=1+8s^2.
```

The authenticated Volterra family with remainder radius `R=8` gives

```text
p=b-3 gamma(b)t+t^2 r_p,  |r_p|<=8,
u=b-  gamma(b)t+t^2 r_u,  |r_u|<=8/5.
```

Thus `u_t=(p-u)/(2t)` has a regular enclosure without differentiating either
unknown remainder. Entire kernels in `z=t u^2` likewise remove every apparent
origin singularity. The nonlinear profile equation supplies `p_t` directly,
so the conormal jets `(p,p_t)`, `(s,s_t)`, and `(c,c_t)` are rigorous on a
cell containing `t=0`.

The division-free minors `d1,d2,D` are assembled before ranging. A
four-variable mean-value enclosure in `(t,b,r_p,r_u)` preserves their shared
dependence. With 16 time cells and four shooting-slope cells it proves

```text
W_K >= 1/100 I,  0 <= x <= 3/16.
```

The exact lower bounds have numerical values

```text
min pbar_11 = 0.444130243685352
min pbar_22 = 0.350083868584866
min d1      = 0.658684620946269
min d2      = 1.62435671071383
min D       = 0.0670614628308156
```

The origin-family contraction bound is at most `0.900653766297957784`.

Artifact:
`experiments/centrifugal_skyrmion_liouville_origin_certificate.json`, SHA256
`daa220e68ceef034a1b23ea955033dc08c0e776ee49628eb07acb0834b57c065`.

## Global Coefficient Chain

This artifact joins at `x=3/16` to the authenticated outer Newton-tube
certificate, which proves the same `1/100` bound through the wall at `x=4`.
The exact wall audit supplies a positive allowed trace remainder. Therefore
all coefficient inequalities required by the proposed global square
completion are now certified over the same nonlinear profile family.

## Claim Boundary

Coefficient positivity is not yet the global Friedrichs theorem. The next
proof must define the weighted form domain, prove smooth-core density and
closability, show that the origin/outer split introduces no trace defect, and
apply the representation theorem. Only then does `q[y]>=||y||^2/100` imply a
two-sided inverse norm at most `100`. A nonzero physical response must still be
validated against that weaker inverse constant.

## Reproduction

```bash
PYTHONPATH=. python \
  experiments/centrifugal_skyrmion_liouville_origin_audit.py
PYTHONPATH=. python -m pytest -q \
  tests/test_validated_centrifugal_origin_liouville.py \
  tests/test_centrifugal_skyrmion_liouville_origin_audit.py
```
