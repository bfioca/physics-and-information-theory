# Goal 5: `k>1` Observer Algebra Tomography

## Theorem-first audit note

Stop condition: no new examples are introduced here. This note audits the Goal
5 result in standard finite stabilizer/OA-QEC notation and separates human
proofs from certificate-backed finite searches.

## Definitions

Let `C` be an `[[n,k]]` stabilizer code with stabilizer space `S` inside the
binary Pauli symplectic space `V_n`. Let

```text
L = S^perp / S
```

be the `2k`-dimensional logical symplectic vector space. For a physical region
`R`, let `V_R` denote Pauli vectors supported in `R`, and define

```text
L_R = image(S^perp cap V_R -> S^perp / S).
```

Equivalently, `L_R` is the subspace of logical Pauli classes with at least one
representative supported entirely in `R`.

The finite observer-algebra signature of `R` is

```text
tau_C(R) = (dim L_R, dim Z_R, dim L_R^perp, L_R = L),
Z_R = L_R cap L_R^perp.
```

Here `L_R^perp` is the symplectic orthogonal complement of `L_R` inside the
full logical space `L`. This is the logical commutant dimension used in the
note. It is not a physical-region commutant, and it is not an assertion about
continuum von Neumann algebras. In the implementation this is the subspace of
logical quotient classes whose symplectic product with every element of `L_R`
vanishes.

The all-region erasure/survivor channel shadow records, for every region `R`,
only

```text
L_R = 0?      erasure-correctability of R
L_R = L?      full reconstruction by R
```

so it detects forbidden and qualified regions but not the symplectic type of
intermediate regions.

## Proof-Audit Verdict

Goal 5 survives the sanity pass in a narrow theorem-program form:

- exact theorem: channel shadows are insufficient for `k>1`;
- exact counterexample: channel plus center is insufficient;
- exact linear-algebra completion: center plus logical commutant dimensions
  determine the observer-algebra signature;
- certificate-backed evidence: first-hit/minimality statements in the bounded
  permutation-quotient scan and the all-region amplified scan.

No claim below is a continuum de Sitter theorem, a general non-stabilizer
OA-QEC theorem, or an asymptotic gravity result.

## Strict Hierarchy

The certified hierarchy is:

```text
channel shadow
  < channel + center shadow
  < center + logical-commutant shadow
  = observer-algebra signature
```

The first two strict inequalities are witnessed by finite stabilizer codes.
The equality is a human proof from symplectic linear algebra. It is useful
bookkeeping, but it is not by itself a non-tautological operational tomography
theorem because the logical commutant dimension is already algebraic access
data.

## Theorem A: Channel Shadow Is Insufficient For `k>1`

For `k>1`, all-region erasure-correctability plus survivor/full-reconstruction
booleans do not determine all-region observer-algebra signatures.

Minimal witness under qubit-permutation equivalence:

```text
A = <XXI>
B = <XXX>
```

Both are `[[3,2,1]]` stabilizer codes. In both codes:

- `L_empty = 0`;
- `L_full = L`;
- every nonempty proper region is intermediate.

Thus the all-region channel shadows match. But on region `{0,1}`,

```text
tau_A({0,1}) = (2,0,2,false)
tau_B({0,1}) = (3,1,1,false).
```

So the channel shadow does not determine the observer-algebra signature.

Certificate role: the bounded scan checks `k=2` representatives through
`n<=4` and finds no channel-shadow collision at `n=2`, then finds this first
collision at `n=3`.

## Theorem B: Channel Plus Center Is Still Insufficient

There exist finite `k>1` stabilizer codes whose all-region channel shadows and
all-region center dimensions match, but whose all-region observer-algebra
signatures differ.

Witness:

```text
A = <XIIX, XXXI>
B = <IZXI, ZIXX>
```

Both are `[[4,2,1]]` stabilizer codes. They match on channel shadow and center
shadow. On region `{1,2}`,

```text
tau_A({1,2}) = (3,1,1,false)
tau_B({1,2}) = (1,1,3,false).
```

The center dimension is `1` in both cases, but the commutant dimension differs.

Certificate role: the pair is an exact counterexample to sufficiency of
channel plus center. The statement that it appears at this bounded tier, with
the recorded scan behavior through `n<=4`, is finite bounded-search evidence
rather than an all-`n` minimality theorem.

## Proposition C: Center Plus Logical Commutant Completes Signatures

For every finite stabilizer/OA-QEC code and every physical region `R`, the
pair

```text
(dim Z_R, dim L_R^perp)
```

determines `tau_C(R)`.

Proof. Let `W = L_R` and `c = dim W^perp` inside the full nondegenerate
`2k`-dimensional symplectic space `L`. Nondegeneracy gives the standard
dimension identity

```text
dim W + dim W^perp = 2k.
```

Rearranging,

```text
dim W = 2k - c.
```

Thus the logical commutant dimension determines `dim L_R`; the center dimension
supplies `dim Z_R`; and the full-reconstruction bit is equivalent to
`dim L_R = 2k`. Therefore the observer-algebra signature is determined.

Certificate role: the bounded scan finds no collisions through `n<=4` once
center and logical commutant dimensions are included, as predicted by the
linear-algebra proposition.

Implementation audit: `qgtoy/stabilizer.py` computes `commutant_dim` by taking
the nullspace of symplectic-product equations against `L_R` in the full
`2k`-dimensional logical basis. That matches `dim L_R^perp` in the proposition.

## Distance-Amplified Witness

The minimal witness has distance `1`. The certificate also builds a
distance-amplified witness by concatenating each physical qubit of the
`[[3,2,1]]` pair with the canonical five-qubit perfect `[[5,1,3]]` code. The
result is a pair of `[[15,2,3]]` stabilizer codes.

Human proof sketch:

1. The inner five-qubit code has threshold behavior: regions of size `<=2` are
   forbidden and regions of size `>=3` are qualified.
2. Therefore any region of the concatenated code induces an outer block subset
   for zero/full channel access.
3. Since the outer `[[3,2,1]]` pair has matching all-region channel shadows,
   the concatenated pair also has matching all-region channel shadows.
4. The representative region using three qubits in each of outer blocks `0`
   and `1` realizes the same signature split:

```text
(2,0,2,false)  vs  (3,1,1,false).
```

Certificate role: the default certificate audits exact distance `3` by checking
all weight `<3` regions are correctable and exhibiting a weight-3 logical
witness. The optional command directly scans all `32,768` regions of the
`[[15,2,3]]` pair and confirms channel-shadow matching.

## Stress-Tested Witnesses

**`[[3,2,1]]` channel-shadow witness.** The pair `<XXI>` versus `<XXX>` has the
same zero/full access pattern on every region: empty is forbidden, full is
qualified, and every nonempty proper region is intermediate. The split on
`{0,1}` is therefore purely intermediate-algebra data: one side reconstructs a
two-dimensional nondegenerate logical subspace, while the other reconstructs a
three-dimensional subspace with a one-dimensional radical.

**`[[4,2,1]]` channel-plus-center witness.** The pair `<XIIX,XXXI>` versus
`<IZXI,ZIXX>` matches the channel shadow and center dimension for every
region. On `{1,2}`, both centers have dimension `1`, but the logical dimensions
and commutant dimensions are exchanged from `(3,1,1,false)` to
`(1,1,3,false)`.

**`[[15,2,3]]` distance-amplified witness.** Concatenation with the five-qubit
perfect inner code preserves the outer channel-shadow equality under the
inner-code threshold map and raises distance to `3`. The certificate checks all
weight `<3` erasures and gives a weight-`3` logical witness; the optional
full-scan command checks all `32,768` amplified regions.

## What Is Known vs New

**Known-derived.** The `k=1` completion lemma is best viewed as a stabilizer
cleaning / quantum-secret-sharing access-structure fact. In a two-dimensional
logical symplectic space, a region is forbidden, qualified, or carries exactly
one central logical direction; the channel shadow is enough only because there
is no richer intermediate symplectic type.

**New finite hierarchy, subject to expert audit.** The `k>1` result isolates
the missing intermediate data. Forbidden/qualified access data are
insufficient; center data alone is still insufficient. Center plus logical
commutant dimensions exactly complete the observer-algebra signature, but that
top equality is algebraic bookkeeping. The potentially new part is the
diagnostic hierarchy and tomography framing, not the underlying fact that
stabilizer access structures can be computed by symplectic linear algebra.

This is the finite observer-algebra tomography question in compact form:

```text
What is the weakest finite shadow that determines the observer's accessible algebra?
```

For stabilizer signatures, the algebraic completion is center plus logical
commutant dimensions. The non-tautological open problem is to replace direct
logical-commutant input with operational channel, entropy, recovery, or
commutator probes.

## Harlow-Facing One-Paragraph Version

We found a strict finite stabilizer/OA-QEC diagnostic hierarchy for observer
algebras. Entropy/min-cut data and even all-region erasure/survivor channel
data do not determine observer reconstruction algebras for `k>1`; the bounded
first channel-shadow counterexample is a `[[3,2,1]]` pair, and the separation
persists after concatenation to a `[[15,2,3]]` pair. Center data alone is still
insufficient, but center plus logical commutant dimensions determine the
observer-algebra signature by the symplectic identity
`dim L_R = 2k - dim L_R^perp`. This final equality is algebraic bookkeeping,
not an operational tomography theorem. The sharper open question is whether
direct logical-commutant input can be replaced by entropy-response,
relative-entropy, recovery, channel-spectrum, or commutator-test data.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 5 theorem/counterexample certificate | `python3 -m qgtoy observer-tomography-kgt1 --max-n 4` |
| Direct all-region scan of `[[15,2,3]]` amplified witness | `python3 -m qgtoy observer-tomography-kgt1 --max-n 4 --include-amplified-full-scan` |
| Goal 4 `k=1` boundary certificate | `python3 -m qgtoy observer-tomography --max-m 3 --scan-max-n 4` |
| One-page Harlow-facing theorem note | `docs/goal5_harlow_theorem_note.md` |

## Limitations

This is finite stabilizer/OA-QEC mathematics. Proposition C determines
signatures from direct logical-commutant dimensions; it is not a claim that the
commutant has been inferred from operational data. It also does not determine
basis-level algebra isomorphisms or continuum operator algebras. The
`[[3,2,1]]` minimality statement is certificate-backed under qubit-permutation
equivalence through the declared bounded scan. Approximate codes, non-Pauli
algebras, state dependence, and gravitational observer algebras remain outside
the claim.
