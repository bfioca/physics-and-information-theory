# Validated Sharp Skyrmion AU.3b Program

Status: authenticated baseline certificate complete; tail sharpening remains

## Question

AU.3a proves that the signed Skyrmion jump factor has the global Sobolev
moments required by the conditional ULE theorem, but it discards the radial
profile and all finite-frequency cancellation. AU.3b asks whether retaining the
certified Newton tube makes those upper constants useful.

This is a computational theorem gate, not the universal observer theorem and
not a physical-window test by itself.

## Authenticated Inputs

The sharp replay binds two archives:

- AU.2 global derivative/tail archive SHA256
  `1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9`;
- sharp Newton-tube snapshot SHA256
  `1781a2ff357f3b165d23e290eb403552d77d099a72b9e90920735e6a80b30431`.

The snapshot was produced by an exact replay of the canonical AU.2 audit. It
stores the endpoint-corrected spline family, origin contraction data, local
Newton radii, rounding denominator, and source hashes. The global entrypoint
rehashes both archives, the snapshot dependencies, and its own source set
before writing a result.

## Directed Profile Layer

The replay reconstructs cellwise enclosures for the exact profile and its first
two derivatives. It then certifies:

- a nonnegative cellwise rotor-inertia measure, including the regular origin;
- fixed-background interior Skyrmion mass;
- the ideal Young-Laplace shell mass; and
- total fixed-background mass.

The capacity substitution uses total mass including the shell and interior
Skyrmion rotor inertia. Wall inertia is not included. These are worldtube proxy
constants, not an Einstein-Skyrme mass or a backreaction theorem.

## Sharp Frequency Layer

For the normalized inertia measure `dmu`, the anchored identity

```text
H(p)=3/(1+p^2) int K(p,y)/tanh(y)^2 dmu
```

is evaluated by exact rational interval quadrature on each requested frequency
cell. Subtracting a cellwise anchor retains some signed radial cancellation
while remaining valid for the full Newton tube. The finite band is joined to
the AU.2 continuum tail recomputed at the same split.

The output gives directed upper bounds for

```text
Q0, Q1, Q2, Gbar=||q||_1, Mbar=||u q(u)||_1.
```

The AU.2 tail is deliberately conservative, and the bare spectral product
still uses absolute-value bounds. A weak AU.3b constant therefore diagnoses
the proof route; it is not automatically a physical no-go.

## Authenticated Baseline Result

The canonical baseline uses `P=64`, unit frequency cells, one radial
subdivision per positive-radius parent cell, two regular-origin cells, and 16
parallel frequency workers with deterministic ordered reduction. The artifact

```text
experiments/skyrmion_au3b_sharp_global_exact_certificate.json
```

has SHA256
`bc6cf2ea21f44c122001fcc3f7fa6cffb9983d4ec4e35591323aa2d29b25c529`.
It rehashes the authenticated AU.2 archive, sharp snapshot, and snapshot source
dependencies before emitting the result.

The directed global norms are

```text
Q0 <= 17526.908442
Q1 <= 53893.636849
Q2 <= 242992.970718.
```

These are rigorous but weaker than the AU.3a bounds. The squared finite-band
and joined-tail contributions are, respectively,

```text
k=0: 4.990764e5       and 3.066934e8
k=1: 5.333905e6       and 2.899190e9
k=2: 4.264636e8       and 5.861912e10.
```

Thus the conservative AU.2 tail dominates the finite-band contribution by
about `614`, `543`, and `137` for `k=0,1,2`. This baseline authenticates the
profile-resolved pipeline and locates its present overestimation; it does not
show that the physical ULE construction fails.

The same replay gives the fixed-background directed intervals

```text
interior rotor inertia   [21.149280505678, 48.390985007421]
interior mass            [33.833816379433, 64.832878884109]
ideal shell mass         [0.377022981349, 0.441448015749]
total mass               [34.210839360783, 65.274326899858].
```

Using the total-mass lower endpoint and interior-inertia upper endpoint in the
existing compactness/slow-rotation proxy gives continuous capacity at most
`353.623193055092`, odd cutoff `J<=352`, physical spin `K<=705/2`, and the
conditional projective risk floor
`R_ref>=1.9689304688982673e-5`. This is an exactly hard-supported,
fixed-profile proxy-budget result. It is not a dynamically generated cutoff.

The attached centered, prescribed-switch ULE records only normalized coupling
upper caps. Its lower coupling bound is zero because no positive observation
deadline or preparation-age requirement was supplied. Consequently its
formally nonempty coupling interval is automatic and is not a physical
observer window.

## Claim Boundary

AU.3b can certify profile-resolved spectral upper constants and directed
fixed-background capacity inputs. It does not supply:

- physical length or coupling units;
- a nonzero coupling lower bound from observation deadlines;
- autonomous switching or collective-projection leakage;
- local access or a normalized diamond-distance channel estimate;
- wall dynamics, stability lifetime, or all angular modes;
- junction, metric-response, or gravitational backreaction bounds.

Those gates must close before any nonempty coupling cap is called a physical
observer window, or before poor constants are called a universal obstruction.

## Reproduction

```bash
python experiments/skyrmion_au3b_sharp_snapshot_audit.py
python experiments/skyrmion_au3b_sharp_global_audit.py
pytest -q tests/test_validated_skyrmion_sharp_profile.py \
  tests/test_validated_skyrmion_au3b.py \
  tests/test_validated_skyrmion_ule.py
```

Primary implementation:

- `qgtoy/validated_skyrmion_sharp_profile.py`
- `qgtoy/validated_skyrmion_au3b.py`
- `experiments/skyrmion_au3b_sharp_snapshot_audit.py`
- `experiments/skyrmion_au3b_sharp_global_audit.py`
