# Observer Algebra Tomography Beyond One Logical Qubit

This is a finite stabilizer/OA-QEC theorem note, not a continuum gravity claim.
The motivating question is:

```text
Which finite diagnostic data determine an observer's accessible logical algebra?
```

## Setup

For an `[[n,k]]` stabilizer code with stabilizer space `S`, let

```text
L = S^perp / S
```

be the `2k`-dimensional logical Pauli symplectic space. For a physical region
`R`, define `L_R` as the image in `L` of centralizer Paulis supported in `R`.
The finite observer-algebra signature is

```text
tau(R) = (dim L_R, dim Z_R, dim L_R^perp, L_R = L),
Z_R = L_R cap L_R^perp.
```

Here `L_R^perp` is the logical symplectic commutant inside `L`, not the full
physical commutant.

## Result

The Goal 5 certificate gives a strict finite diagnostic hierarchy:

```text
channel shadow
  < channel + center shadow
  < center + logical-commutant shadow
  = observer-algebra signature.
```

The channel shadow is the all-region record of forbidden and qualified regions:
`L_R = 0` and `L_R = L`. It is the finite erasure/survivor fixed-point shadow.

**Negative theorem.** For `k>1`, the channel shadow does not determine
observer-algebra signatures. A bounded-first witness is the `[[3,2,1]]` pair
`<XXI>` versus `<XXX>`. Their all-region channel shadows match, but on
`R={0,1}` the signatures are

```text
(2,0,2,false)  versus  (3,1,1,false).
```

**Stronger negative theorem.** Channel plus center is still insufficient. The
`[[4,2,1]]` pair `<XIIX,XXXI>` versus `<IZXI,ZIXX>` has matching all-region
channel and center shadows, but on `R={1,2}` has

```text
(3,1,1,false)  versus  (1,1,3,false).
```

**Algebraic completion proposition.** Center plus logical commutant dimensions
determine the signature. In any finite symplectic space,

```text
dim L_R + dim L_R^perp = 2k,
```

so

```text
dim L_R = 2k - commutant_dim(R).
```

This recovers `dim L_R`; the center and commutant dimensions are given; and
`L_R=L` is equivalent to `dim L_R=2k`. This final equality is finite symplectic
bookkeeping, not by itself an operational tomography theorem.

## Distance Amplification

The minimal channel-shadow witness has distance `1`. Concatenating each outer
qubit with the five-qubit perfect code gives a certified `[[15,2,3]]` pair.
The separation persists on the block-threshold region corresponding to outer
blocks `{0,1}`, and the optional certificate scans all `32,768` regions of the
amplified pair.

## What Is New Versus Known

Known-derived ingredients include stabilizer cleaning, QSS access structures,
and OA-QEC reconstruction criteria: supported logical subspaces are computable
by symplectic linear algebra, and the `k=1` erasure/survivor completion boundary
is plausibly a repackaging of standard facts.

The potentially useful contribution is the tomography hierarchy: entropy/min-cut
and forbidden/qualified channel shadows are too coarse for `k>1` intermediate
observer algebras; center alone is still too coarse; center plus logical
commutant dimensions are algebraically sufficient for the finite stabilizer
signature. The expert-facing question is whether the strict insufficiency
hierarchy is already standard in OA-QEC/QSS language, and whether direct
logical-commutant input can be replaced by operational entropy, recovery,
relative-entropy, channel-spectrum, or commutator-test data.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 5 hierarchy certificate | `python3 -m qgtoy observer-tomography-kgt1 --max-n 4` |
| Full amplified `[[15,2,3]]` scan | `python3 -m qgtoy observer-tomography-kgt1 --max-n 4 --include-amplified-full-scan` |
| Goal 4 `k=1` boundary certificate | `python3 -m qgtoy observer-tomography --max-m 3 --scan-max-n 4` |
