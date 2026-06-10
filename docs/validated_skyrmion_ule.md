# Validated Normalized Centered Skyrmion ULE Bridge

Status: exact conditional consequence of the authenticated AU.3b baseline;
physical unit map, positive coupling lower bound, and one-action derivation open

## Purpose

This bridge answers a narrow question: once an AU.3b certificate supplies
directed jump-factor moments, what finite-switch ULE residual follows without
introducing a second tunable coupling or silently taking an infinite
preparation time?

It does not yet answer whether a supported Skyrmion is a complete physical
observer. The AU.2 radius is in dimensionless `R=1` normalization. The result
therefore remains a normalized calculation until the Skyrmion length and
coupling units are derived and authenticated from the declared action.

## Inputs

Let

```text
Gbar = ||q||_1 upper bound,
Mbar = ||u q(u)||_1 upper bound,
L    = integer or half-integer collective spin,
g^2  = one declared coupling parameter,
T    = normalized elapsed time,
B    = normalized burn-in time,
Tchi = normalized switch-lead time.
```

The consumer checks the three finite-band, tail, and global squared Sobolev
bounds, the three `Q`-norm enclosures, both Sobolev-derived jump moments, radius
provenance, and paired digest claims. Digest strings remain external claims;
the global audit is responsible for rehashing their source archives.

## Residual

With

```text
a = 144 g^2 L^2,
```

the exact finite-switch state operator-norm residual is bounded by

```text
2 a Gbar Mbar
+ 2 a^2 Gbar^3 Mbar T
+ a Gbar Mbar log(1 + T/(B+Tchi)).
```

The norm is ancilla-stable for the stated state operator-norm estimate. It is
not a normalized diamond-distance bound for a physical matter channel.

For heat time `T=log(d)/(2 g^2 K0)` with `d=2L+1`, burn-in measured by
`beta=144 g^2 L^2 Gbar^2(B+Tchi)`, and normalized zero-mode lower bound

```text
K0 >= 1/(24 pi_upper^2 R_upper^3),
```

the sufficient residual coefficient is

```text
C_beta = 288 L^2 Gbar Mbar
       + 20736 (1 + 1/(2 beta))
         L^4 Gbar^3 Mbar log(d)/K0.
```

Thus a residual budget `epsilon` gives the exact sufficient cap

```text
g^2 <= epsilon/C_beta.
```

Optional observation-deadline and preparation-age constraints give lower
bounds on `g^2`; the executable reports whether the resulting interval is
nonempty.

The authenticated baseline does not supply either optional lower bound. Its
reported lower endpoint is therefore zero, so `coupling_window_nonempty=true`
is automatic. The two recorded coupling upper diagnostics are approximately
`2.273e-21` and `8.553e-23`; they are normalized caps, not physical windows.

## Claim Boundary

The result assumes:

- a prescribed amplitude switch;
- exact zero-Bohr rigid collective projection;
- a stationary quasifree bath;
- replacement of remote-past preparation by the displayed burn-in estimate;
- Casimir Lamb-shift control; and
- reuse of one caller-declared coupling parameter in both formulas.

It does not certify autonomous switching, a same-action coupling derivation,
collective-band leakage, local access, off-center lapse deformation, wall
stress, lifetime, junction conditions, metric response, gravitational
backreaction, or the physical length/coupling unit map.

## Reproduction

```bash
pytest -q tests/test_validated_skyrmion_ule.py
python -m ruff check qgtoy/validated_skyrmion_ule.py tests/test_validated_skyrmion_ule.py
```

Primary implementation:

- `qgtoy/validated_skyrmion_ule.py`
- `tests/test_validated_skyrmion_ule.py`
- `experiments/skyrmion_au3b_sharp_global_audit.py`
