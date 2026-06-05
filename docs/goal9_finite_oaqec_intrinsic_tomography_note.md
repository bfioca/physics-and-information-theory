# Goal 9: Finite-Dimensional OAQEC Intrinsic Tomography

Goal 9 generalizes the Goal 8 stabilizer result to finite-dimensional
operator-algebra QEC. The question is whether an observer's reconstructable
algebra `A_R` can be recovered from intrinsic region-local operational data.

## Result

There is a positive theorem if the intrinsic data include a full local
product/* tomography table:

> For a finite-dimensional OAQEC observer algebra `A_R`, an operational basis
> of region-local distinguishable code-preserving effects together with product,
> adjoint, identity, trace/normalization, and commutator structure constants
> determines `A_R` up to finite-dimensional `*-`algebra isomorphism.

Equivalently, it determines the abstract Wedderburn block type

```text
A_R ~= direct-sum_alpha M_{d_alpha}.
```

With channel fixed-point or commutant multiplicity data, it also determines the
represented type

```text
A_R ~= direct-sum_alpha I_{m_alpha} tensor M_{d_alpha}.
```

This is a theorem-style finite-dimensional algebra result, not a new OAQEC
formalism.

## Proof Sketch

Finite-dimensional `C*`-algebras are semisimple. Product and adjoint tomography
identify:

- the center `Z(A_R)`;
- the minimal central projections `p_alpha`;
- each simple corner `p_alpha A_R p_alpha`.

Each simple corner has dimension `d_alpha^2` and is isomorphic to `M_{d_alpha}`.
Thus the product/* table recovers the abstract Wedderburn block sizes
`d_alpha`. Channel fixed-point or commutant data supply representation
multiplicities `m_alpha`.

## Weak-Shadow Failure

The certificate searches finite direct sums of matrix algebras with

```text
block_dim <= 4
number_of_blocks <= 5
```

and finds the first bounded collision for the weak shadow

```text
(algebra_dim, center_dim, commutator_subspace_dim).
```

| Algebra 1 | Algebra 2 | Shared weak shadow |
| --- | --- | --- |
| `C^4 direct-sum M_4` | `M_2 direct-sum M_2 direct-sum M_2 direct-sum M_2 direct-sum M_2` | `(20, 5, 15)` |

So dimension, center size, and commutator-subspace dimension do not determine
Wedderburn block type. Full product structure is doing real work.

## Goal 8 Special Case

For a stabilizer region `R`, Goal 8 recovers the supported logical Pauli quotient
`L_R` and its restricted symplectic form. If the restricted symplectic rank is
`2q` and the radical dimension is `c`, then the generated finite-dimensional
observable algebra has abstract Wedderburn type

```text
C^{2^c} tensor M_{2^q},
```

equivalently a direct sum of `2^c` copies of `M_{2^q}`. Goal 8's
`(dim L_R, dim Z_R, dim L_R^perp, L_R=L)` is the Pauli/symplectic compression
of the Goal 9 Wedderburn signature.

## Relation To Known Work

- Bény-Kempf-Kribs provide the Heisenberg/OAQEC observable-algebra framework:
  [arXiv:0705.1574](https://arxiv.org/abs/0705.1574).
- Almheiri-Dong-Harlow connect AdS reconstruction, QSS, and OAQEC:
  [arXiv:1411.7041](https://arxiv.org/abs/1411.7041).
- Harlow formulates RT-from-QEC in finite-dimensional OAQEC/subalgebra-code
  language: [arXiv:1607.03901](https://arxiv.org/abs/1607.03901).
- Dauphinais-Kribs-Vasmer develop stabilizer-OAQEC:
  [arXiv:2304.11442](https://arxiv.org/abs/2304.11442).
- Matsumoto/Yamashita stabilizer QSS access structures are the closest
  stabilizer-side overlap: [arXiv:1811.05217](https://arxiv.org/abs/1811.05217).

## Harlow-Facing Summary

Goal 9 reframes observer algebra as an intrinsically tomographable
finite-dimensional observable algebra. Weak shadows such as dimension, center
size, and commutator dimension do not determine the algebra, but full
region-local product/* response determines Wedderburn block type. Goal 8 is the
stabilizer special case, where product/* data collapse to local Pauli response
plus symplectic commutator tomography.

The honest novelty claim is not a new finite-dimensional algebra theorem. The
claim is the diagnostic hierarchy: which observer-accessible shadows fail, which
strong intrinsic data complete the algebra, and how the stabilizer certificate
sits as a special case.

## Limitations

Full product/* tomography is a strong input and is close to supplying the
algebra directly. The harder frontier is to replace it with weaker recovery,
relative-entropy, modular, or noisy response data while still recovering
Wedderburn type.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 9 finite-OAQEC certificate | `python3 -m qgtoy observer-tomography-oaqec --max-block-dim 4 --max-blocks 5` |
| Focused Goal 9 regression | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal9_finite_oaqec_intrinsic_observer_tomography_certificate` |
| Goal 8 stabilizer baseline | `python3 -m qgtoy observer-tomography-intrinsic --max-n 4` |
