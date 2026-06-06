# Goal 21: Finite dS/CFT-ER=EPR Compatibility Benchmark

Goal 21 asks whether finite dS/CFT-like screen data can determine an
ER=EPR-style algebraic bridge channel between observer static patches. The
answer in this benchmark is a no-go with a completion principle:

```text
screen-visible horizon data can hide the bridge algebra;
intrinsic observer-algebra response is the missing datum.
```

## Finite Objects

The model has two observer primitives:

- a north static patch;
- a south static patch.

They share a finite horizon/screen algebra `C^d`. There is no asymptotic AdS
boundary. The bridge algebra under test is `M_d`.

The screen/CFT-like shadow records only finite screen-visible data:

- north/south screen entropies;
- diagonal correlator shadows on `C^d`;
- shared-horizon overlap data;
- transfer-matrix spectra restricted to the screen algebra `C^d`.

This is a finite diagnostic abstraction, not a continuum CFT dictionary.

## No-Go Theorem

For every `d >= 2`, compare two realizations with the same finite screen layer:

```text
quantum bridge:          identity on M_d
classical horizon bridge: complete dephasing onto C^d
```

Restricted to the horizon/screen algebra `C^d`, the declared screen-visible
data match exactly. But the maximal recoverable bridge algebras differ:

```text
identity:  M_d
dephasing: C^d
```

So finite dS/CFT-visible screen shadows do not determine algebraic ER=EPR
connectivity in this family.

## Completion

An off-diagonal matrix-unit coherence probe separates the channels immediately.
Equivalently, one needs an informationally complete operator probe atlas or a
maximality test. This recovers the Goal 20 obstruction in dS/CFT language:
diagonal response certifies `C^d`, but not whether `M_d` is also recoverable.

## Representative Witnesses

| Witness | Dimension | Shared Screen | Quantum Bridge | Dephased Bridge |
| --- | ---: | --- | --- | --- |
| minimal | `2` | `C^2` | `M_2` | `C^2` |
| non-Pauli finite-dimensional | `3` | `C^3` | `M_3` | `C^3` |

For `d=2`, diagonal relative entropy is `0.333333333333` bits for both
channels. The off-diagonal completion probe has `0.184241398542` bits under the
identity bridge and `0` under dephasing.

## Entropy-Only Control

At screen probability `p=0.75`, north and south screen entropies tie because
`H(p)=H(1-p)`. Channel recovery still favors the north patch. Thus entropy-only
screen data fail even to orient patch recovery in this finite control.

## Bounded Family

The certificate checks `2 <= d <= 5`.

| Quantity | Value |
| --- | --- |
| screen shadows match | yes |
| bridge algebras differ | yes |
| completion probes separate | yes |

## Claim Boundary

This is a finite QEC/OA-QEC compatibility benchmark. It is not a continuum
dS/CFT theorem, not de Sitter quantum gravity, not a type-III algebra theorem,
and not a proof of ER=EPR in de Sitter.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 21 certificate | `PYTHONPATH=. python3 -m qgtoy ds-cft-er-epr --max-dim 5 --screen-probability 0.75` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_ds_cft_er_epr` |
| JSON certificate index validation | `python3 -m json.tool docs/goal21_ds_cft_er_epr_compatibility_benchmark_certificate_index.json` |
