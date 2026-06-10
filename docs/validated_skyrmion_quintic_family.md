# Validated Uniform Quintic Skyrmion Origin Family

The authenticated AU.3b shooting interval is not a single profile. Any finite
origin transfer used in the continuum proof must therefore control the full
profile family, uniformly in the shooting slope. The earlier uniform origin
theorem used a cubic center and a comparatively large remainder ball. This
certificate upgrades that input to the quintic form required by the
post-indicial field germ.

On each of 16 exact rational slope cells, set `t=x^2` and write

```text
p(t)=b-3c(b)t-5d(b)t^2+t^3 r_p(t),   |r_p| <= 13/10,
u(t)=b-c(b)t-d(b)t^2+t^3 r_u(t),     |r_u| <= 13/70,
F(x)=pi-x u(x^2),                    F'(x)=-p(x^2).
```

Here `c(b)` and `d(b)` are interval enclosures of the exact cubic and quintic
regular-origin coefficients. Degree-two Taylor models retain these
coefficients while bounding all higher powers by exact rational interval
arithmetic. The Volterra map is then proved contractive on every slope cell.

For `x <= 1/16`, the source-hashed audit proves

```text
maximum contraction bound       < 0.584076 < 3/5,
maximum residual bound          < 0.135432,
maximum radii left side         < 0.894730 < 9/10,
chosen remainder radius          = 1.3,
minimum Volterra denominator    > 20.7559.
```

The 16 cells cover the authenticated slope interval without gaps. At the
cutoff the whole family also satisfies

```text
3.0425506 < F(1/16) < 3.0432169,
-1.583443 < F'(1/16) < -1.572800.
```

The strict negative derivative fixes the common orientation of the profile
branch. More importantly for the centrifugal response, the `t^3` remainder
matches the exact field germs through physical power `x^5`; no derivative of
the profile remainder is needed in the conormal formulation.

## Reproduce

```bash
PYTHONPATH=. python experiments/validated_skyrmion_quintic_family_audit.py
python -m pytest -q tests/test_validated_skyrmion_quintic_family.py tests/test_validated_skyrmion_quintic_family_audit.py
```

## Claim Boundary

This is a uniform finite-origin profile theorem. It does not prove the
centrifugal field transfer, Friedrichs-domain equivalence, the global
continuum inverse, or a nonzero tidal response. It supplies the sharp profile
input needed for those steps.
