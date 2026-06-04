# Observer Algebra Tomography in Finite Quantum Error-Correcting Codes

## Entropy shadows, erasure shadows, and a `k=1` reconstruction boundary

This note is self-contained. It describes a finite operator-algebra quantum
error-correction question motivated by holography and observer Hilbert-space
ideas:

```text
Which finite diagnostic data determine an observer's accessible logical algebra?
```

The answer below is deliberately modest but sharp. Entropy-like data can agree
while observer reconstruction algebras differ. However, in the simplest
nontrivial stabilizer setting, one logical qubit, a stronger all-region
channel diagnostic is complete for the observer-algebra signature.

The slogan is:

```text
observer entropy gives size information;
observer algebra requires channel/erasure information.
```

## Basic Objects

A stabilizer quantum error-correcting code is specified by commuting Pauli
checks on `n` physical qubits. If the code has `k` logical qubits, its logical
Pauli operators form a binary symplectic quotient

```text
L = centralizer(checks) / stabilizer(checks),     dim L = 2k.
```

For a physical region `R`, let `L_R` be the subspace of logical Pauli classes
that have at least one representative supported entirely inside `R`. This is a
finite version of asking which logical observables an observer with access to
`R` can reconstruct.

The finite observer algebra of `R` is summarized by the signature

```text
tau_C(R) = (logical_dim, center_dim, commutant_dim, reconstructs_all),
```

where:

- `logical_dim = dim L_R`;
- `center_dim` is the radical dimension of the symplectic form restricted to
  `L_R`;
- `commutant_dim` is the dimension of logical classes commuting with all of
  `L_R`;
- `reconstructs_all` means `L_R = L`.

This signature is not a continuum von Neumann algebra invariant. It is a finite
stabilizer/OA-QEC proxy for the same kind of question: what algebra of logical
observables is visible from a region?

## Observer Atlases

An observer atlas is a named finite collection of regions. In the main
counterexample family, the atlas has two observer causal patches,
`observer_p` and `observer_q`, a shared overlap called `shared_horizon`, and a
union called `static_diamond`.

The names matter. A named observer atlas is weaker than all-region tomography:
it only probes a chosen list of physical regions. The positive theorem below
uses the stronger all-region setting, where every subset of physical qubits is
included.

## Diagnostic Shadows

This note compares several finite diagnostic shadows. A shadow is a compressed
record of code data; the question is whether that record determines the
observer algebra.

**Entropy shadow.** The entropy shadow records code-state entropies for a
declared set of regions. In the observer-atlas examples it also records region
overlaps, mutual information, conditional mutual information, tripartite
information, shared-horizon entropy, and shared-horizon algebra.

**Horizon-visible data.** In the observer-atlas examples, horizon-visible data
means the finite overlap structure of two observer patches, especially the
shared region `shared_horizon`.

**Min-cut shadow.** In a finite tensor-network version of the construction, the
min-cut shadow records exact graph min-cut values for declared boundary
regions. It is an entropy-like geometric diagnostic, not by itself a
reconstruction invariant.

**Erasure shadow.** For a region `E`, the erasure-correctability bit records
whether erasing `E` is correctable. In stabilizer language:

```text
erase_ok(E) = 1  iff  L_E = 0.
```

So `E` is correctable exactly when it supports no nontrivial logical operator.

**Survivor fixed-point data.** For an erased region `E`, the survivor is the
complement `E^c`. The survivor fixed-point bit records whether the surviving
region reconstructs all logicals:

```text
survivor_all(E) = 1  iff  L_{E^c} = L.
```

All-region erasure plus all-region survivor fixed-point data form the channel
shadow used in the positive theorem.

## Main Results

The results have two sides.

First, entropy-like shadows are not complete. There are finite codes that look
the same to entropy/horizon/min-cut diagnostics but differ in observer
reconstruction and channel behavior.

Second, this does not mean tomography is hopeless. For one logical qubit,
all-region erasure plus survivor fixed-point data exactly determines the
all-region observer-algebra signature.

## Theorem A: Non-Identifiability

**Theorem A.** There are certified finite stabilizer/OA-QEC separations showing
that entropy-visible, horizon-visible, and finite min-cut-visible diagnostics
are not complete observer-algebra invariants. The visible shadows can agree
while reconstruction-visible and channel-visible diagnostics differ.

The result has two certified components.

**A1. Observer-atlas family.** There is an explicit infinite family of paired
stabilizer codes `A_m,B_m`, indexed by a bridge count `m >= 1`, with a named
observer atlas. For every `m`, the two codes agree on:

- named observer entropy;
- observer overlap;
- shared-horizon region and shared-horizon entropy;
- MI/CMI/I3 tables for the named patches;
- shared-horizon algebra;
- erasure-correctability booleans for the named erasures;
- survivor fixed-point booleans.

Nevertheless, the two codes have different observer-algebra signatures on the
observer patches and different erasure-channel algebra semantics.

**A2. Finite tensor-network counterpart.** There is also a finite
tensor-network/holographic-code witness in which boundary entropy and finite
min-cut diagnostics agree while reconstruction-visible and channel-visible
geometry differ.

**Proof sketch for A1.** The paired codes are built by adding bridge checks
symmetrically. This preserves the declared entropy and horizon data for the
observer atlas. The two realizations place different logical quotient classes
inside the observer patches, so their region-algebra signatures differ even
though the named entropy and erasure/fixed-point shadows agree.

**Proof sketch for A2.** The tensor-network certificate computes exact finite
min-cut values for the declared boundary regions and compares them with exact
region-algebra and erasure-channel diagnostics. The min-cut data remain
entropy-like; the supported logical classes and channel behavior see additional
structure.

**Scope note.** Theorem A does not claim that every conceivable min-cut
invariant is incomplete. It says the certified finite min-cut diagnostics used
in the tensor-network witness are incomplete as observer-algebra invariants.

## Theorem B: `k=1` Tomography Boundary

**Theorem B.** For any finite stabilizer/OA-QEC code with one logical qubit,
the all-region erasure-correctability profile together with all-region survivor
fixed-point data determines the all-region observer-algebra signature
`tau_C(R)` for every physical region `R`.

Equivalently, for `k=1`, the all-region channel shadow determines the function

```text
R -> (logical_dim, center_dim, commutant_dim, reconstructs_all).
```

**Proof.** When `k=1`, the full logical quotient `L` is a two-dimensional
symplectic vector space. For any physical region `R`, the subspace `L_R` can
have dimension only `0`, `1`, or `2`.

The erasure bit for `R` identifies the zero-dimensional case:

```text
erase_ok(R) = 1  iff  dim L_R = 0.
```

The survivor fixed-point bit for the complement identifies the
two-dimensional case:

```text
survivor_all(R^c) = 1  iff  dim L_R = 2.
```

If neither condition holds, then `dim L_R = 1`. In a two-dimensional
symplectic vector space, these three cases force the full signature:

```text
dim L_R = 0  ->  tau_C(R) = (0,0,2,false)
dim L_R = 1  ->  tau_C(R) = (1,1,1,false)
dim L_R = 2  ->  tau_C(R) = (2,0,0,true)
```

Thus all-region erasure-correctability plus all-region survivor fixed-point
data determines every all-region observer-algebra signature.

## What This Says Conceptually

In holographic quantum error correction, entropy and min-cut data often capture
geometric size or area-like information. Reconstruction, however, is an
operator-algebra statement: it asks which logical observables are actually
available to a region.

The finite lesson is:

```text
entropy scale is not observer algebra;
observer algebra is fixed by reconstruction/channel structure.
```

In a closed-universe or observer-Hilbert-space setting, one might say that an
observer entropy `S_Ob` sets a size scale, but does not by itself specify the
observer's effective quantum mechanics. A finite replacement for that missing
information is:

```text
observer physics = entropy scale + accessible algebra + channel/coarse-graining rule.
```

Theorem A gives explicit finite separations showing that entropy-like shadows
are too weak. Theorem B gives a clean positive boundary in the simplest
nontrivial logical sector: for `k=1`, all-region channel data determines the
observer-algebra signature.

## What Is Machine-Certified

The accompanying code emits JSON certificates for the statements above. The
certificates are not needed to understand the mathematics, but they make the
finite witnesses reproducible.

The default observer-tomography certificate checks the paired observer-atlas
family through a finite prefix, records the all-`m` theorem statement, and runs
an exhaustive bounded implementation audit for the `k=1` completion lemma over
stabilizer-code representatives through `n <= 4`.

That bounded audit checks:

```text
835 one-logical-qubit stabilizer-code representatives
12,638 physical regions
0 signature mismatches
```

The audit is not the proof of Theorem B; the proof above is the proof. The
audit verifies that the implementation of the finite algebra signatures and
channel shadows behaves as the theorem predicts on the declared bounded class.

## Reproducibility Commands

Run commands from the repository root.

| Claim | Evidence class | Command |
| --- | --- | --- |
| Observer algebra tomography package | Exact theorem package plus bounded audit | `python3 -m qgtoy observer-tomography --max-m 3` |
| `k=1` all-region completion lemma audit | Exact theorem plus bounded implementation audit | `python3 -m qgtoy observer-tomography --max-m 3 --scan-max-n 4` |
| Balanced-bridge symbolic theorem seed | Exact theorem checker | `python3 -m qgtoy bridge-proof-check` |
| Static observer entropy/horizon shadow | Exact finite certificate | `python3 -m qgtoy cosmology-phase1 --max-m 3` |
| Erasure and survivor fixed-point shadow | Exact finite certificate | `python3 -m qgtoy cosmology-phase2 --max-m 3` |
| Strict-cover bounded audit | Exhaustive bounded evidence | `python3 -m qgtoy cosmology-phase31 --max-bonus 2` |
| Finite min-cut/reconstruction/channel witness | Exact finite certificate with bounded search obligations | `python3 -m qgtoy holography-phase40` |
| Combined tomography with live min-cut audit | Exact plus bounded evidence | `python3 -m qgtoy observer-tomography --max-m 3 --include-holography` |

## Limitations

This is a finite stabilizer/OA-QEC theorem note, not a continuum
quantum-gravity claim. The observer-atlas family is exact for the declared
all-`m` construction, but it uses a specific finite atlas. The min-cut result
is a certified finite tensor-network witness, not an asymptotic RT theorem. The
positive tomography theorem is exact only for all-region `k=1` stabilizer
atlases. Named observer atlases, `k>1` logical sectors, approximate codes,
continuum limits, and state-dependent observer reconstructions remain open.

## Open Problems

1. **Generalize or refute Theorem B for `k>1`.** Does all-region erasure plus
   survivor fixed-point data determine all-region observer-algebra signatures
   for arbitrary logical dimension?
2. **Find the next missing diagnostic if `k>1` fails.** Candidate additions are
   center profiles, commutant dimensions, richer channel fixed-point data, and
   logical-probe response data.
3. **Upgrade signatures to algebra equivalence.** Theorem B determines finite
   algebra signatures. A stronger theorem would classify observer algebras up
   to an explicit finite-code equivalence.
4. **Connect to observer Hilbert-space programs.** Translate the finite channel
   boundary into a question about what data specify an observer's effective
   algebra in closed-universe settings.

## Email-Sized Pitch

I found a finite OA-QEC theorem pair that may be adjacent to observer
Hilbert-space questions. First, entropy/horizon/min-cut shadows are not
complete invariants of observer reconstruction: explicit stabilizer families
and finite tensor-network witnesses can have identical visible shadows but
different observer algebras or channel semantics. Second, for `k=1`
stabilizer/OA-QEC codes, all-region erasure-correctability plus survivor
fixed-point data determines the all-region observer-algebra signature. So
observer entropy is not observer algebra, but erasure/channel data give a
finite tomography boundary in the one-logical-qubit case. I would be curious
whether this is known in the OA-QEC literature, or whether the `k>1` case is
the interesting next problem.
