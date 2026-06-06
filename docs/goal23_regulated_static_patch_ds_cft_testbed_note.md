# Goal 23: Regulated Static-Patch dS/CFT Algebraic ER=EPR Testbed

Goal 23 replaces the abstract finite transfer switch with a regulated
static-patch screen model. The regulator is an angular cutoff `L`; the finite
screen mode algebra has

```text
N = (L+1)^2
```

spherical-mode labels `(ell,m)` with `0 <= ell <= L`.

## Finite-Cutoff Objects

For each cutoff:

- boundary/screen mode algebra: `C^N`;
- north observer static-patch algebra: `M_N`;
- south observer static-patch algebra: `M_N`;
- shared horizon algebra: `C^N`;
- one regulated transfer kernel deriving both screen data and bridge channel.

There is no asymptotic AdS boundary.

## Regulated Kernel

Diagonal matrix units are fixed. Off-diagonal matrix units are either
geometrically damped or projected to zero:

```text
quantum kernel:   E_ij -> exp(-distance(i,j)/(L+1)^2) E_ij
classical kernel: E_ij -> 0 for i != j
```

The finite-cutoff error is

```text
epsilon_L = 1 - min_offdiag_shrink.
```

For `L=1`, `epsilon_L = 0.393469340287`; for `L=4`,
`epsilon_L = 0.273850962926`.

## Theorem-Style Result

For every checked cutoff `1 <= L <= 4`, the two kernels agree on:

- screen entropy shadows;
- low-order diagonal correlator shadows;
- horizon-overlap data;
- screen-restricted transfer data.

But they induce different epsilon-recoverable bridge algebras:

```text
regulated quantum bridge: M_N
classical horizon bridge: C^N
```

Thus finite dS/CFT-like screen data remain insufficient.

## Intrinsic Completion

Full intrinsic operator data separates the kernels:

- off-diagonal relative-entropy response;
- full transfer response;
- modular/off-diagonal response;
- commutator/OTOC-style growth.

Inside this regulated family, that data determines the algebraic bridge channel
with the recorded cutoff error.

## Zero-Geometry Limit

Setting the geometric shrink to `1` recovers the Goal 22 finite transfer
family. Goal 23 turns that zero-geometry switch into a cutoff kernel with an
explicit `epsilon_L`.

## Continuum Gate

The continuum gate is not passed. Before claiming dS/CFT or ER=EPR in de
Sitter, the next model must:

- derive the kernel from an actual static-patch path integral or Hamiltonian;
- prove reflection positivity/unitarity or control non-unitarity;
- identify the continuum boundary operator dictionary;
- show cutoff errors vanish in a controlled large-`L` limit;
- replace finite Type-I algebras with the appropriate Type-II/Type-III limit;
- derive generalized entropy or QES data from the same dynamics;
- prove the ER=EPR interpretation in the continuum model.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 23 certificate | `PYTHONPATH=. python3 -m qgtoy regulated-static-patch --max-cutoff 4 --screen-probability 0.75 --low-order 2` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_static_patch_testbed` |
| JSON certificate index validation | `python3 -m json.tool docs/goal23_regulated_static_patch_ds_cft_testbed_certificate_index.json` |
