# Physics and Information Theory Toy Verifier

This repository contains an exact, dependency-light verifier for small
stabilizer states and stabilizer quantum error-correcting codes.

The current implementation focuses on finite binary symplectic calculations:

- graph-state enumeration up to graph local complementation and qubit
  relabeling;
- stabilizer-code enumeration with selectable equivalence: raw rowspaces,
  qubit relabeling, or local Clifford plus qubit relabeling;
- stabilizer-code representation from Pauli generators;
- exact stabilizer entropy vectors for the normalized code state;
- mutual information, tripartite information, and conditional mutual
  information;
- centralizer/logical quotient calculations;
- erasure correctability;
- logical Pauli reconstruction regions;
- region algebra dimensions, commutants, and centers;
- code distance;
- a small search for entropy-matched codes with different reconstruction or
  algebra profiles.
- robust low-order searches with nontriviality filters such as minimum distance,
  minimum reconstruction-region size, and no single-qubit non-central logical
  algebra.

The verifier is intended to treat search systems as hypothesis generators and
to make every candidate pass exact checks.

## Examples

Run the built-in search:

```bash
python3 -m qgtoy search --max-n 4 --k 1
```

Certify the first low-order entropy/reconstruction separation:

```bash
python3 -m qgtoy search --max-n 4 --k 1 --max-subset-size 2 --minimal
```

List graph-state local-Clifford representatives:

```bash
python3 -m qgtoy graph-reps --n 4
```

List stabilizer-code representatives up to local Clifford equivalence:

```bash
python3 -m qgtoy code-reps --n 2 --k 1 --dedupe local-clifford
```

Verify a code from stabilizer generators:

```bash
python3 -m qgtoy code-info XZZXI IXZZX XIXZZ ZXIXZ
```

Include explicit region-algebra Pauli bases:

```bash
python3 -m qgtoy code-info XZZXI IXZZX XIXZZ ZXIXZ --include-bases
```

Run the robust distance-2 frontier over structured sources:

```bash
python3 -m qgtoy robust-search --max-n 6 --k 1 --max-subset-size 2 --min-distance 2 --min-reconstruction-size 2 --stop-on-pair
```

Restrict to CSS codes and fixed boundary labels:

```bash
python3 -m qgtoy robust-search --max-n 6 --k 1 --source css --entropy-key labeled --stop-on-pair
```

As of the current verifier, the robust CSS scan finds an `n=6`, `k=1`,
`d=2` pair whose one- and two-body entropy data match while
reconstruction/algebra profiles differ. The previous `n=4`, `d=1` pair should
be treated as a calibration case.

Analyze the robust witness mechanism:

```bash
python3 -m qgtoy witness-mechanism
```

Search first lift rules:

```bash
python3 -m qgtoy lift-frontier
```

Verify the repeated balanced-bridge family through three appended bridge pairs:

```bash
python3 -m qgtoy bridge-family --max-steps 3
```

Emit the theorem-style package:

```bash
python3 -m qgtoy bridge-theorem --max-exact-steps 3
```

Run the independent symbolic proof checker:

```bash
python3 -m qgtoy bridge-proof-check
```

Emit the finite de Sitter-like QEC toy model capstone certificate:

```bash
python3 -m qgtoy desitter-toy --max-m 3 --max-bonus 2
```

Emit the Goal 4 observer-algebra tomography certificate:

```bash
python3 -m qgtoy observer-tomography --max-m 3
```

Read the Harlow-facing theorem note:

```text
docs/harlow_facing_observer_algebra_tomography_note.md
```

Run the bounded all-region tomography scan through `n <= 4` and audit the
exact `k=1` all-region erasure/fixed-point completion lemma:

```bash
python3 -m qgtoy observer-tomography --max-m 3 --scan-max-n 4
```

Emit the Goal 5 `k>1` observer-algebra tomography certificate:

```bash
python3 -m qgtoy observer-tomography-kgt1 --max-n 4
```

Read the Goal 5 Harlow-facing theorem note:

```text
docs/goal5_harlow_theorem_note.md
```

Emit the Goal 6 operational observer-algebra tomography certificate:

```bash
python3 -m qgtoy observer-tomography-operational --max-n 4
```

Read the Goal 6 operational theorem note:

```text
docs/goal6_operational_observer_tomography_note.md
```

Emit the Goal 7 equivalence-aware observer-algebra tomography atlas:

```bash
python3 -m qgtoy observer-tomography-atlas --max-n 4
```

Read the Goal 7 atlas memo:

```text
docs/goal7_observer_tomography_atlas_note.md
```

Emit the Goal 8 intrinsic observer-algebra tomography atlas:

```bash
python3 -m qgtoy observer-tomography-intrinsic --max-n 4
```

Read the Goal 8 intrinsic tomography memo:

```text
docs/goal8_intrinsic_observer_tomography_note.md
```

Optionally include the full all-region scan of the distance-amplified
`[[15,2,3]]` witness:

```bash
python3 -m qgtoy observer-tomography-kgt1 --max-n 4 --include-amplified-full-scan
```

Optionally include the heavier finite min-cut/reconstruction/channel audit:

```bash
python3 -m qgtoy observer-tomography --max-m 3 --include-holography
```

Emit the first finite causal-patch / horizon-code certificate:

```bash
python3 -m qgtoy cosmology-phase1 --max-m 3
```

Emit the deterministic growth and erasure-channel certificate:

```bash
python3 -m qgtoy cosmology-phase2 --max-m 3
```

Emit the bounded causal-patch cover-search certificate:

```bash
python3 -m qgtoy cosmology-phase3 --m 2 --max-hits 5
```

Emit the code-source and generic cover-search certificate:

```bash
python3 -m qgtoy cosmology-phase4 --max-hits-per-pair 3
```

Emit the cached source-frontier and targeted-lift certificate:

```bash
python3 -m qgtoy cosmology-phase5
```

Emit the source-aware cover-template certificate:

```bash
python3 -m qgtoy cosmology-phase6
```

Emit the persistent frontier-cache replay certificate:

```bash
python3 -m qgtoy cosmology-phase7
```

Emit the graph/encoder extended frontier-cache certificate:

```bash
python3 -m qgtoy cosmology-phase8
```

Emit the graph-specific cover-template no-go certificate:

```bash
python3 -m qgtoy cosmology-phase9
```

Emit the labeled graph/CWS strict-atlas certificate:

```bash
python3 -m qgtoy cosmology-phase10
```

Emit the distance-repaired graph-atlas tension certificate:

```bash
python3 -m qgtoy cosmology-phase11
```

Emit the atlas-aware repaired-cover recovery certificate:

```bash
python3 -m qgtoy cosmology-phase12
```

Emit the repaired cover-dynamics and CSS-baseline comparison certificate:

```bash
python3 -m qgtoy cosmology-phase13
```

Emit the bounded repaired-cover transition-graph certificate:

```bash
python3 -m qgtoy cosmology-phase14
```

Emit the multi-source cover-flow invariant atlas certificate:

```bash
python3 -m qgtoy cosmology-phase15
```

Emit the mixed CSS code-cover transition graph certificate:

```bash
python3 -m qgtoy cosmology-phase16
```

Emit the repaired non-CSS local-Clifford flow certificate:

```bash
python3 -m qgtoy cosmology-phase17
```

Emit the non-CSS outer-code swap taxonomy certificate:

```bash
python3 -m qgtoy cosmology-phase18
```

Emit the bounded outer-code mutation search certificate:

```bash
python3 -m qgtoy cosmology-phase19
```

Emit the bounded inner graph/CWS mutation search certificate:

```bash
python3 -m qgtoy cosmology-phase20
```

Emit the mixed inner-outer transition graph certificate:

```bash
python3 -m qgtoy cosmology-phase21
```

Emit the exact time/channel dynamics certificate:

```bash
python3 -m qgtoy cosmology-phase22
```

Emit the biased channel comparison certificate:

```bash
python3 -m qgtoy cosmology-phase23
```

Emit the bounded exact channel-rule search certificate:

```bash
python3 -m qgtoy cosmology-phase24
```

Emit the target-constrained channel synthesis certificate:

```bash
python3 -m qgtoy cosmology-phase25
```

Emit the cross-substrate channel-rule transfer certificate:

```bash
python3 -m qgtoy cosmology-phase26
```

Emit the multi-substrate robust channel synthesis certificate:

```bash
python3 -m qgtoy cosmology-phase27
```

Emit the audited rule-language proof certificate:

```bash
python3 -m qgtoy cosmology-phase28
```

Emit the bounded substrate-family co-design certificate:

```bash
python3 -m qgtoy cosmology-phase29
```

Emit the bounded observer-cover co-design certificate:

```bash
python3 -m qgtoy cosmology-phase30
```

Emit the strict-cover exhaustive audit certificate:

```bash
python3 -m qgtoy cosmology-phase31
```

Emit the Goal 3 stabilizer tensor-network seed certificate:

```bash
python3 -m qgtoy holography-phase1
```

Emit the Goal 3 bounded graph/CWS ring-spoke atlas certificate:

```bash
python3 -m qgtoy holography-phase2
```

Emit the Goal 3 distance-repaired lifted ring-spoke atlas certificate:

```bash
python3 -m qgtoy holography-phase3
```

Emit the Goal 3 multi-bulk-node layout audit certificate:

```bash
python3 -m qgtoy holography-phase4
```

Emit the Goal 3 generated Clifford/MERA-style layout search certificate:

```bash
python3 -m qgtoy holography-phase5
```

Emit the Goal 3 generated Clifford tensor-network audit certificate:

```bash
python3 -m qgtoy holography-phase6
```

Emit the Goal 3 joint Clifford circuit and compact-patch search certificate:

```bash
python3 -m qgtoy holography-phase7
```

Emit the Goal 3 distance-gated Clifford synthesis search certificate:

```bash
python3 -m qgtoy holography-phase8
```

Emit the Goal 3 compressed pentagon two-layer block certificate:

```bash
python3 -m qgtoy holography-phase9
```

Emit the Goal 3 five-qubit perfect outer-block certificate:

```bash
python3 -m qgtoy holography-phase10
```

Emit the Goal 3 same-distance perfect-outer variant certificate:

```bash
python3 -m qgtoy holography-phase11
```

Emit the Goal 3 perfect-outer embedding robustness certificate:

```bash
python3 -m qgtoy holography-phase12
```

Emit the Goal 3 two-perfect-tensor tiling certificate:

```bash
python3 -m qgtoy holography-phase13
```

Emit the Goal 3 three-perfect-cell chain/ring atlas certificate:

```bash
python3 -m qgtoy holography-phase14
```

Emit the Goal 3 capacity/branching fixed-witness grammar certificate:

```bash
python3 -m qgtoy holography-phase15
```

Emit the Goal 3 capacity-sensitive interval no-go certificate:

```bash
python3 -m qgtoy holography-phase16
```

Emit the Goal 3 four-perfect-cell tree fixed-witness certificate:

```bash
python3 -m qgtoy holography-phase17
```

Emit the Goal 3 four-cell tree shell-bottleneck certificate:

```bash
python3 -m qgtoy holography-phase18
```

Emit the Goal 3 compact-core plus shell hybrid no-go certificate:

```bash
python3 -m qgtoy holography-phase19
```

Emit the Goal 3 four-cell outer-tree local-variant no-go certificate:

```bash
python3 -m qgtoy holography-phase20
```

Emit the Goal 3 four-cell outer-tree topology no-go certificate:

```bash
python3 -m qgtoy holography-phase21
```

Emit the Goal 3 five-cell branching internal-witness audit certificate:

```bash
python3 -m qgtoy holography-phase22
```

Emit the Goal 3 interface-cell star audit certificate:

```bash
python3 -m qgtoy holography-phase23
```

Emit the Goal 3 punctured interface-shell frontier certificate:

```bash
python3 -m qgtoy holography-phase24
```

Emit the Goal 3 two-layer Clifford/MERA-like frontier certificate:

```bash
python3 -m qgtoy holography-phase25
```

Emit the Goal 3 offset-flip entropy-gated neighborhood certificate:

```bash
python3 -m qgtoy holography-phase26
```

Emit the Goal 3 second-root-hole region-grammar certificate:

```bash
python3 -m qgtoy holography-phase27
```

Emit the Goal 3 leaf-private sentinel region-grammar certificate:

```bash
python3 -m qgtoy holography-phase28
```

Emit the Goal 3 full leaf-private region-grammar certificate:

```bash
python3 -m qgtoy holography-phase29
```

Emit the Goal 3 bridge-axis source-pairing certificate:

```bash
python3 -m qgtoy holography-phase30
```

Emit the Goal 3 shared logical-basis twist certificate:

```bash
python3 -m qgtoy holography-phase31
```

Emit the Goal 3 independent logical-basis twist priority certificate:

```bash
python3 -m qgtoy holography-phase32
```

Emit the Goal 3 full independent logical-basis twist certificate:

```bash
python3 -m qgtoy holography-phase33
```

Emit the Goal 3 bounded alternative graph/CWS source-pair scout certificate:

```bash
python3 -m qgtoy holography-phase34
```

Emit the Goal 3 full alternative source-pair semantic audit certificate:

```bash
python3 -m qgtoy holography-phase35
```

Emit the Goal 3 full entropy-mismatch near-hit audit certificate:

```bash
python3 -m qgtoy holography-phase36
```

Emit the Goal 3 split-support region-grammar certificate:

```bash
python3 -m qgtoy holography-phase37
```

Emit the Goal 3 q139 support-scale strict-hit certificate:

```bash
python3 -m qgtoy holography-phase38
```

Emit the Goal 3 representative strict-hit robustness certificate:

```bash
python3 -m qgtoy holography-phase39
```

Emit the Goal 3 theorem-style holographic-cousin package:

```bash
python3 -m qgtoy holography-phase40
```

The current bridge-family rule starts from the `n=6` CSS witness and appends
bridge pairs. For bridge `j`, add qubits `a=6+2j,b=7+2j` and add the same two
checks to both codes:

```text
Z_1 Z_2 Z_a Z_b
X_0 X_5 X_a X_b
```

The verifier confirms the family steps for `m=1,2,3`, giving `n=8,10,12`,
`k=1`, `d=2`, matching labeled `t=2` entropy diagnostics, no single-qubit
non-central logical support, and different reconstruction/algebra profiles.

## Balanced-Bridge Theorem Package

Let `(A_m,B_m)` be the CSS code pair obtained from the `n=6` seed pair by
adding bridge qubits `p_j=6+2j`, `q_j=7+2j` for `j=0,...,m-1` and adding the
same two stabilizer checks to both codes:

```text
Z_1 Z_2 Z_{p_j} Z_{q_j}
X_0 X_5 X_{p_j} X_{q_j}
```

The theorem output includes two complementary artifacts:

- `symbolic_checker`: a support-mask/GF(2)-rank checker that derives the
  all-`m` claims from the generator templates without calling the full
  `StabilizerCode` verifier. Its `restricted_rank_schema` field records the
  case classifier, seed-span obligations, fresh-coordinate checks, and
  exhaustive finite-prefix enumeration used to audit the one- and two-qubit
  rank claim. Its `restricted_rank_formula_schema` field derives the six
  case-by-case rank predictions from the generator rule, checks the polynomial
  case counts, and compares predicted ranks against direct GF(2) restricted
  ranks on finite prefixes.
- `exact_prefix`: exact stabilizer verifier certificates for the requested
  finite prefix.

The proof establishes for all `m`:

- `n=6+2m`, `k=1`, and `d=2`;
- every labeled one- and two-qubit entropy agrees between `A_m` and `B_m`;
- no single-qubit region reconstructs a non-central logical algebra;
- the reconstruction/algebra profiles are distinct.

The explicit separating region is
`R_m={1,2,3} union {p_j : 0 <= j < m}`. On `R_m`, `A_m` has only the central
logical `Z_1Z_3`, with algebra signature `(1,1,1,false)`, while `B_m`
supports both `Z_1Z_3` and `X_2X_3 product_j X_{p_j}`, with signature
`(2,0,0,true)`.

The entropy mechanism is restricted stabilizer rank blindness:
`S(R)=|R|-rank(S_R)`. Old-old rank data match in the seed; each bridge pair has
the same local stabilizer `X_{p_j}X_{q_j}` in both codes; all other bridge
singletons/pairs contribute equal local rank. Thus all labeled `t=2` entropy
queries agree even though reconstructability differs.

### Proof Details

Commutation follows from even overlaps. The bridge Z old support `{1,2}` has
even overlap with every seed X check in both seeds, and the bridge X old support
`{0,5}` has even overlap with every seed Z check in both seeds. A bridge Z and
same-index bridge X overlap on exactly the two fresh qubits; different bridge
indices have no fresh overlap, and `{1,2}` is disjoint from `{0,5}`.

The rank is `5+2m`: each seed has three independent Z checks and two
independent X checks. Bridge `j` has fresh coordinates `{p_j,q_j}` in its own
sector, and no other same-sector bridge row contains those coordinates, so each
bridge contributes one independent Z row and one independent X row. Since
`n=6+2m`, this gives `k=1`.

The distance is exactly `2`. The A family keeps the weight-two Z logical
`Z_0Z_5`; the B family keeps `Z_1Z_3`. Both commute with all X checks and are
not Z stabilizers. No weight-one Pauli is central because every old qubit is
touched by at least one seed Z check and one seed X check, while every new
qubit is touched by its bridge Z and bridge X checks.

For the restricted-rank claim, use `S(R)=|R|-rank(S_R)`. Every singleton or pair
falls into one of six support cases:

- old singleton: bridge rows cannot contribute because their fresh coordinates
  cannot be canceled by same-sector rows, so ranks reduce to the matched seed
  table;
- old-old pair: the same old-only reduction applies;
- new singleton: rank `0` in both families;
- old-new pair: rank `0` in both families, again by the unique fresh-coordinate
  obstruction;
- full bridge pair `{p_j,q_j}`: rank `1` in both families because
  `X_0X_5X_{p_j}X_{q_j}` times the seed `X_0X_5` gives
  `X_{p_j}X_{q_j}`, and `{1,2}` is not in either seed Z span;
- two new qubits from distinct bridge pairs: rank `0` in both families.

These cases exhaust all labeled one- and two-qubit subsets for every `m`, so
the labeled `t=2` entropy vectors match for the whole family.

The command `python3 -m qgtoy bridge-proof-check` emits this same argument as a
machine-readable certificate. The restricted-rank portion is not just proof
text: `restricted_rank_formula_schema` derives the rank formula for each case
from the seed spans and bridge supports, then checks the formula against direct
restricted-rank calculations for every one- and two-qubit region in the sampled
prefix.

## Goal 2 Phase 1: Finite Causal Patches

The first QEC-cosmology layer treats a stabilizer code plus a named region cover
as a finite toy cosmology. For the balanced-bridge family with `m>=1`, the
default cover is:

- `observer_p`: `{1,2,3} union {p_j}`;
- `observer_q`: `{1,2,3} union {q_j}`;
- `shared_horizon`: `{1,2,3}`;
- `bridge_shell`: `{p_j,q_j}`;
- `static_diamond`: `observer_p union observer_q`.

The two observer patches overlap exactly on `shared_horizon`. The Phase 1
certificate computes, exactly:

- patch entropies and region-algebra signatures;
- pairwise intersections, unions, mutual information, conditional mutual
  information, and tripartite information;
- complement erasure-correctability for each named patch;
- A/B comparisons of entropy-overlap data versus logical reconstruction data.

For `m=1,2,3`, the certificate verifies a static causal-patch separation:

- A and B have the same labeled one- and two-qubit entropy data;
- A and B have the same named patch entropy, overlap, MI, CMI, and I3 data;
- A and B have the same shared-horizon algebra `(1,1,1,false)`;
- the observer patches differ: in A they have signature `(1,1,1,false)`, while
  in B they have full logical algebra signature `(2,0,0,true)`.

This is a finite horizon-code toy universe: horizon-visible and
entropy-overlap-visible data match, but observer-patch reconstructability does
not. The certificate recommends adapting the next phase toward explicit
time/channel dynamics on this patch atlas, starting with deterministic
bridge-growth and simple erasure/noise channels.

## Goal 2 Phase 2: Growth And Erasure Channels

Phase 2 adds a minimal exact dynamics layer. The time index is the bridge count
`m`. A deterministic growth step `m -> m+1` appends a bridge pair
`p_m=6+2m`, `q_m=7+2m`, assigns `p_m` to `observer_p`, assigns `q_m` to
`observer_q`, and leaves the shared horizon fixed.

The Phase 2 certificate verifies, for every slice through `--max-m`:

- the Phase 1 static separation still holds;
- exact erasure probes satisfy the QEC complementarity identity:
  an erased region is correctable iff the survivor complement reconstructs all
  logicals;
- private observer-shell erasures are correctable in both A and B;
- shared-horizon erasure is not correctable in either A or B;
- A and B have the same named-erasure correctability profile and the same
  erased-region entropy profile;
- observer-patch erasure still distinguishes the codes at the algebra level.

For growth transitions, the certificate checks:

- `shared_horizon` is fixed;
- `observer_p`, `observer_q`, `bridge_shell`, and `static_diamond` grow by the
  expected new qubits;
- observer entropy increments by `1`;
- observer-pair mutual information and private conditional mutual information
  increment by `2`;
- observer-pair tripartite information and the witness algebra signatures stay
  fixed.

The Phase 2 recommendation is `proceed_as_written`: the verifier now supports
static causal patches, deterministic patch growth, and exact erasure-channel
probes. The next phase should add bounded search over patch covers, bridge
assignments, and small CSS/tensor-network-like constructions, looking for new
entropy-overlap/reconstruction separations automatically.

## Goal 2 Phase 3: Bounded Cover Search

Phase 3 adds the first exact search layer for causal-patch covers. For a fixed
balanced-bridge slice `m`, it enumerates:

- old-qubit shared horizons of a chosen size;
- all bridge-side assignments where each bridge pair contributes one qubit to
  each observer;
- two observer patches, a shared horizon, a bridge shell, and a static diamond
  for each candidate cover.

A candidate is a search hit only if exact verification proves all of:

- A and B have the same named-patch entropy/overlap/MI/CMI/I3 data;
- the observer overlap is exactly the named shared horizon;
- A and B have the same shared-horizon algebra;
- A and B differ in observer-patch reconstruction or algebra signatures;
- A and B have the same named-erasure correctability profile;
- at least one erasure probe distinguishes their algebras.

For the default command, the search space is the `m=2` balanced-bridge CSS
family slice with horizon size `3`. It scans a bounded set of candidate covers
and returns verified hits as machine-readable certificates. The first hit
recovers the hand-found `{1,2,3}` horizon cover, but through enumeration and
exact scoring rather than by special-casing it.

The Phase 3 recommendation is `adapt_then_proceed`: the cover-search interface
works, but the next phase should broaden the source space beyond the
balanced-bridge family to small CSS, graph/CWS-like, and shallow-encoder code
pairs while preserving the same patch-cover certificate schema.

## Goal 2 Phase 4: Code-Source Search

Phase 4 moves beyond bridge-grown slices and searches generic two-observer
covers over exact code-pair sources. A generic cover consists of:

- a shared horizon of configurable size;
- disjoint private regions for `observer_p` and `observer_q`;
- derived `bridge_shell` and `static_diamond` regions.

The default certificate uses two exact code-pair sources:

- `seed_css_witness`: the robust `n=6`, `k=1`, `d=2` CSS witness from Goal 1,
  before bridge growth;
- `minimal_n4_calibration_pair`: the exact minimal `n=4`, `k=1` low-order
  entropy/reconstruction calibration pair.

It also reports lightweight bounded source scans for small CSS, cyclic-CSS,
graph/CWS-like, and shallow-encoder sources. These scans are included as
machine-readable evidence even when they do not yield robust pairs under the
current bounds.

A Phase 4 hit uses the same exact criteria as Phase 3:

- same named-patch entropy/overlap/MI/CMI/I3 data;
- observer overlap equal to the named shared horizon;
- same shared-horizon algebra;
- different observer reconstruction or algebra;
- same named-erasure correctability profile;
- an erasure algebra difference.

With the default settings, the seed CSS witness produces verified generic-cover
hits while the `n=4` calibration pair is reported as no-hit for this cover
template. The Phase 4 recommendation is `adapt_then_proceed`: add source-frontier
caching and targeted mutations/lifts for CSS, graph/CWS-like, and
shallow-encoder codes, then feed every entropy-matched reconstruction-discordant
pair into the generic cover scorer.

## Goal 2 Phase 5: Cached Source Frontier

Phase 5 adds a deterministic source-frontier cache before cover scoring. The
default cache includes:

- the robust CSS seed witness;
- targeted balanced-bridge CSS lifts through `m=2`;
- the exact `n=4` calibration pair.

Every cached source is scored by the same generic two-observer cover search used
in Phase 4. The certificate records a cache key from the source name and Pauli
generators, per-source cover counts, verified hits, no-hit records, and optional
bounded source scans.

With the default settings, the robust seed source still produces verified
generic-cover hits. The first targeted bridge lifts are scored exactly but are
no-hit under the bounded generic cover template. This is useful pressure: the
lifted CSS family needs source-aware cover templates, such as the bridge-aware
patch atlas from Phases 1-3, rather than only generic small private regions.

The Phase 5 recommendation is `adapt_then_proceed`: add source-aware cover
templates and cached frontier files, especially bridge-aware covers for lifted
CSS families and targeted graph/CWS-like or shallow-encoder mutations that keep
low-order entropy fixed while perturbing reconstruction algebras.

## Goal 2 Phase 6: Source-Aware Cover Templates

Phase 6 adds a template layer between cached code-pair sources and generic cover
enumeration. For each targeted balanced-bridge lift, the scorer first tries the
source-derived bridge observer atlas:

- `observer_p`: `{1,2,3} union {p_j}`;
- `observer_q`: `{1,2,3} union {q_j}`;
- `shared_horizon`: `{1,2,3}`;
- `bridge_shell`: all bridge-pair qubits;
- `static_diamond`: the observer union.

The generic two-observer cover search remains as a fallback for sources without
a known atlas. The certificate records candidate and hit counts by template
kind, so a hit can be attributed to `source_aware_bridge_observer` rather than
to generic enumeration.

This phase resolves the Phase 5 pressure test: the lifted CSS frontier is
no-hit under the bounded generic template, but becomes a verified hit when the
source rule supplies its natural bridge-aware causal patch cover. The exact hit
criteria are unchanged: matching named entropy/overlap/MI/CMI/I3 data, matching
shared-horizon algebra, different observer reconstruction/algebra, matching
erasure correctability, and an erasure algebra difference.

The Phase 6 recommendation is `adapt_then_proceed`: move from in-memory cached
sources to persistent frontier-cache artifacts, then add source-aware templates
for graph/CWS-like and shallow-encoder mutation rules so the framework can
compare search-generic geometries against source-specific atlases.

## Goal 2 Phase 7: Persistent Frontier-Cache Replay

Phase 7 turns the deterministic in-memory frontier into a persistent JSON
artifact at `qgtoy/frontier_cache/goal2_phase7_frontier.json`. Each record stores:

- source metadata and mutation depth;
- first/second Pauli generator lists;
- exact quality and low-order entropy/reconstruction diagnostics;
- a SHA-256 cache digest over the source identity and generator data;
- template hints such as `source_aware_bridge_observer`.

The Phase 7 certificate does not trust the file blindly. It verifies every
record by reconstructing `StabilizerCode` objects from the Pauli generators,
recomputing diagnostics, checking each digest, confirming digests are unique,
and comparing the artifact digest list against the deterministic generator
parameters stored in the artifact.

After cache verification, the certificate replays the Phase 6 source-aware
cover scorer using only the loaded records. With the default artifact, the seed
source remains available for generic scoring, both balanced-bridge lift records
replay as verified `source_aware_bridge_observer` hits, and the calibration pair
remains a no-hit for this atlas.

The Phase 7 recommendation is `adapt_then_proceed`: add graph/CWS-like and
shallow-encoder mutation records to the persistent frontier, with exact source
diagnostics and template hints, then replay the same cache scorer to compare
bridge-specific, graph-specific, and generic emergent patch atlases.

## Goal 2 Phase 8: Graph/Encoder Extended Frontier

Phase 8 adds a second persistent artifact at
`qgtoy/frontier_cache/goal2_phase8_extended_frontier.json`. It keeps the Phase 7
bridge/CSS records and adds:

- `graph_cws_profile_n4_calibration_pair`: a graph/CWS-like `n=4`, `k=1`
  calibration pair found by a bounded graph-subspace scan with profile entropy
  matching and relaxed filters;
- `robust_graph_n5_labeled_no_pair`: a bounded robust graph scan record;
- `robust_encoder_n5_depth3_labeled_no_pair`: a bounded robust shallow-encoder
  scan record.

The graph/CWS-like pair is deliberately labeled calibration-only: it differs in
reconstruction profile and matches the unlabeled low-order entropy profile, but
it fails the robust distance filter and does not match labeled `t=2` entropy.
When replayed through the current generic two-observer cover scorer, it is a
certified no-hit. This is useful pressure on the folk move from "same entropy
profile" to "same named causal-patch geometry."

The two scan records are also replayable. The certificate recomputes each scan,
checks scan digests, and verifies that the bounded robust graph and encoder
searches remain no-pair under the stated labeled-entropy and quality filters.

The Phase 8 recommendation is `adapt_then_proceed`: add graph-specific cover
templates based on graph neighborhoods/cuts and widen the encoder frontier
before treating non-CSS entropy coincidences as geometric candidates.

## Goal 2 Phase 9: Graph-Specific Cover No-Go

Phase 9 keeps the Phase 8 graph/CWS-like calibration pair but stops scoring it
only through generic small covers. It adds two exact graph-native cover template
families:

- `graph_closed_neighborhood_overlap`: observer patches from closed
  neighborhoods in the stabilizer-support co-occurrence graph;
- `graph_generator_support_cut`: observer patches from overlapping generator
  support cuts.

For the cached `graph_cws_profile_n4_calibration_pair`, these graph-specific
templates produce no causal-patch hit. The certificate then scores the complete
tiny search space of all ordered, non-identical, overlapping two-observer covers
on four qubits. That exhaustive space also produces no hit, even though some
covers do expose observer-reconstruction differences.

The lesson is sharper than the Phase 8 result: the graph/CWS-like pair has
reconstruction-visible structure, but because it matches only the unlabeled
entropy profile and not the named labeled `t=2` data, no two-observer named
causal-patch atlas exists in this finite cover class.

The Phase 9 recommendation is `adapt_then_proceed`: search for non-CSS sources
that preserve labeled low-order entropy data, or pivot back to bridge-family
time/channel dynamics where the causal-patch atlas is already certified.

## Goal 2 Phase 10: Labeled Graph/CWS Strict Atlas

Phase 10 adapts the non-CSS search rather than continuing with the Phase 8
profile-only graph calibration pair. It runs a bounded graph/CWS-like subspace
scan on `n=5`, `k=1` sources using labeled `t=2` entropy and relaxed
distance-one calibration constraints. The certificate preserves graph provenance
for the found pair: edge masks, edge lists, neighborhoods, kept/deleted graph
checks, graph-state generators, code generators, and exact quality diagnostics.

The found pair has identical labeled one- and two-qubit entropy data and
different reconstruction/algebra profiles. This repairs the Phase 8/9 weakness:
the entropy match is named and labeled, not merely an unlabeled profile
collision.

The atlas result is mixed in a useful way. Graph-native neighborhood/support
templates still produce no causal-patch hit. But the strict finite cover search
with a one-qubit shared horizon and one private qubit per observer does produce
certified hits. The strict exhaustive two-observer search, requiring nonempty
private regions on both observer sides, also produces hits. The first hits have
the same named entropy/overlap/MI/CMI/I3 data and different observer
reconstruction, with exact erasure-profile checks.

The caveat is important: both graph/CWS-like codes have distance `1` and fail
the stricter robust horizon-code filters. Phase 10 is therefore a labeled
non-CSS calibration toy and a strict finite atlas hit, not yet a robust
horizon-code family.

The Phase 10 recommendation is `adapt_then_proceed`: try exact distance repair
for this labeled graph atlas via lifting, padding, or concatenation, then replay
the same strict atlas and erasure/channel diagnostics before moving to richer
time dynamics.

## Goal 2 Phase 11: Distance-Repaired Graph Atlas Tension

Phase 11 repairs the distance-one weakness in the Phase 10 labeled graph/CWS
pair by logical concatenation with a four-qubit outer stabilizer code:

```text
XXIZ
ZIZX
XZXX
```

The resulting pair has `n=20`, `k=1`. The certificate avoids exponential
centralizer enumeration by using rank-kernel support restriction: it solves
exactly for stabilizer or centralizer combinations supported in each queried
region. A regression test checks that this rank-kernel path agrees with the
original exact small-code diagnostics.

The repair succeeds on two important axes:

- exact bounded logical-weight search certifies no weight-one logical in either
  repaired code; the first repaired code has a weight-two witness, while the
  second has no witness through weight two;
- all labeled one- and two-qubit entropy probes still match, with 211 subsets
  checked and zero mismatches.

The repair does not preserve the simple Phase 10 atlas as a full causal-patch
certificate. Phase 11 replays 525 lifted strict-atlas candidates made by
repeating the first Phase 10 observer covers over overlapping outer-code block
sets. Many candidates still match entropy/horizon data and expose observer
algebra differences, but the bounded replay produces no full hit after the
erasure/complementarity checks. A separate explicit region still certifies a
reconstruction/algebra difference after repair.

The lesson is a useful pressure result: distance repair, labeled low-order
entropy matching, and finite causal-patch atlas semantics are separable
constraints. The Phase 11 recommendation is `adapt_then_proceed`: search
atlas-aware repair rules or broader repaired-cover templates before moving to
time/channel dynamics for the repaired non-CSS toy.

## Goal 2 Phase 12: Atlas-Aware Repaired-Cover Recovery

Phase 12 follows the Phase 11 recommendation and treats the patch cover as part
of the repaired QEC/cosmology data. It keeps the Phase 11 `n=20`, `k=1`
distance-repaired graph/CWS pair, reuses the exact rank-kernel diagnostics, and
scores 525 atlas-aware covers built from one canonical Phase 10 strict inner
atlas hit and all overlapping masks of the four outer repair blocks.

The certificate checks three template families:

- `phase12_full_outer_block_control`: complete inner blocks selected by outer
  block masks. These match entropy and horizon algebra but have zero raw
  observer-reconstruction hits, so they are too coarse.
- `phase12_inner_strict_block_lift`: the canonical Phase 10 strict inner atlas
  repeated over outer block masks. This produces raw near-hits, but a certified
  representative still fails the erasure-correctability profile, matching the
  Phase 11 failure mode.
- `phase12_private_full_shared_inner`: shared outer blocks keep the inner
  observer overlap, while private outer blocks are promoted to complete inner
  blocks. This produces a full repaired atlas hit.

The first full hit has observer P on the tiny inner patch `(0,1)` in outer block
`0`, and observer Q on inner patch `(1,4)` in shared block `0` plus complete
private outer blocks `2` and `3`. It verifies the full causal-patch claim:
same named entropy/overlap/MI/CMI/I3 data, observer overlap equal to the shared
horizon, same shared-horizon algebra, different observer reconstruction,
matching erasure-correctability profile, and erasure-algebra differences.

The Phase 12 recommendation is `proceed_as_written`: compare this repaired
non-CSS atlas against the balanced-bridge CSS baseline under simple time/channel
dynamics, especially transitions between the plain inner-lift near-miss and the
atlas-aware repaired hit.

## Goal 2 Phase 13: Repaired Cover Dynamics

Phase 13 adds a tiny exact time/channel layer on top of the Phase 12 repaired
non-CSS toy. The code pair is fixed at the Phase 11 `n=20`, `k=1` repaired pair;
the time variable is the causal-patch cover. The certificate tracks a two-slice
cover flow:

- `t=0`, `plain_inner_lift_near_miss`: observer P is `(0,1)`, observer Q is
  `(1,4,6,9)`, and the shared horizon is `(1)`. This slice has the same named
  entropy/overlap data and different observer reconstruction, but fails matching
  erasure correctability.
- `t=1`, `atlas_aware_repaired_hit`: observer P and the horizon stay fixed,
  while observer Q drops `(6,9)` and adds complete private outer blocks `2` and
  `3`, namely qubits `10` through `19`. This repairs the erasure-correctability
  profile while preserving the observer-algebra separation.

The transition is therefore a cover/atlas flow on a fixed code, not a code
growth rule. The certificate records patch deltas, exact rank-kernel entropy and
observer-pair metrics, erasure-channel fixed-point summaries, and
QEC-complementarity identities for every named erasure scenario.

Phase 13 also compares the repaired non-CSS hit with the CSS balanced-bridge
Phase 2 baseline. Both pass exact channel-style diagnostics, but they assign
different semantics to the same role label: shared-horizon erasure is not
correctable in the CSS bridge baseline, while the repaired non-CSS atlas hit has
correctable shared-horizon erasure. The lesson is that role labels are not
enough; horizon semantics must be certified from the exact erasure channel and
operator algebra at each slice.

The Phase 13 recommendation is `adapt_then_proceed`: build a bounded graph of
certified covers and small patch-edit transitions, then classify which
role-labeled horizons have stable erasure semantics across CSS and non-CSS toy
models.

## Goal 2 Phase 14: Bounded Cover-Transition Graph

Phase 14 turns the Phase 13 cover transition into a bounded graph search. Nodes
are Phase 12 repaired-cover candidates on the fixed `n=20`, `k=1` repaired code
pair, restricted to a canonical 24-node neighborhood with observer-P block masks
`{1,3}` and observer-Q block masks `{3,5,9,13}` across the three Phase 12
template families. Nodes are scored exactly with the rank-kernel cover scorer.

Edges are small patch edits: observer P and the shared horizon must stay fixed,
observer Q may change by at most five qubits, and both endpoints must preserve
the entropy/reconstruction signal. The graph search finds a path from the plain
inner-lift near-miss to the atlas-aware repaired hit. Along the certified path:

- named entropy/overlap data stay matched;
- observer reconstruction remains different;
- the erasure-correctability profile changes from mismatched to matched;
- the erasure-algebra difference set shrinks from four named scenarios to two.

The role-semantics classifier checks every named erasure scenario against the
CSS Phase 2 baseline. The shared-horizon erasure profile is stable inside the
repaired-cover flow, but disagrees with the CSS bridge baseline. This makes the
Phase 13 lesson searchable: a finite graph can preserve the ER=EPR-like
entropy/overlap signal while changing the channel fixed-point semantics attached
to the same role labels.

The Phase 14 recommendation is `adapt_then_proceed`: broaden the node sources to
multiple CSS and non-CSS cover graphs, then classify flow invariants such as
stable horizon correctability, erasure fixed points, and algebra-difference
monotonicity.

## Goal 2 Phase 15: Multi-Source Flow Invariant Atlas

Phase 15 broadens the Phase 14 graph classifier to three exact cover-flow
graphs:

- the CSS balanced-bridge orientation hypercube at `m=2`, with 4 nodes;
- the CSS balanced-bridge orientation hypercube at `m=3`, with 8 nodes;
- the repaired non-CSS Phase 14 neighborhood, with 24 nodes.

Every node is scored with exact rank-kernel entropy, operator-algebra, erasure
correctability, survivor fixed-point, and QEC-complementarity diagnostics. The
CSS graph edges flip one bridge-pair orientation while keeping the shared
horizon, bridge shell, and static diamond fixed. The repaired graph reuses the
Phase 14 bounded patch-edit edge rule.

The certificate classifies both graph-global and canonical-path invariants. On
the CSS orientation paths, shared-horizon erasure stays non-correctable with
survivor fixed point `(false,false)`, and the algebra-difference count is flat:
`3,3,3` for `m=2` and `3,3,3,3` for `m=3`. On the repaired non-CSS canonical
path, shared-horizon erasure stays correctable with survivor fixed point
`(true,true)`, and the algebra-difference count is nonincreasing:
`4,4,2,2`.

The useful pressure-test is that shared-horizon semantics are path-stable but
not model-stable. They are also not global across the full repaired graph: the
classifier finds repaired nodes with different shared-horizon correctability
even though the canonical repaired flow keeps that role stable. Thus a horizon
label is not itself a semantic invariant; the invariant must specify the source
graph and flow.

The Phase 15 recommendation is `adapt_then_proceed`: add code-changing edges,
such as bridge-growth steps or small local Clifford/graph moves, so exact
invariants can be tested across mixed code-cover dynamics rather than cover
edits alone.

## Goal 2 Phase 16: Mixed CSS Code-Cover Graph

Phase 16 adds genuine code-changing edges to the balanced-bridge CSS toy
cosmology. Nodes are all orientation covers for `m=1..3`, so the graph has
`2+4+8=14` exact code-cover nodes. Each node carries its own code pair
`(A_m,B_m)` and a cover orientation assigning one qubit from every bridge pair
to each observer.

There are two edge types:

- `cover_orientation_flip`: fixed code size, flip one bridge-pair orientation;
- `bridge_growth`: grow `m -> m+1`, preserve the old orientation prefix, and
  append one oriented bridge pair.

The default certificate has 29 edges: 17 orientation flips and 12 bridge-growth
edges. The canonical path
`mixed_css:m1:o0 -> mixed_css:m1:o1 -> mixed_css:m2:o11 -> mixed_css:m3:o111`
uses one cover edit and two code-growth edges.

Every node and edge is checked with exact entropy, rank-kernel algebra, erasure
correctability, survivor fixed-point, and QEC-complementarity diagnostics. The
mixed graph keeps the CSS baseline rigid through the checked prefix: low-order
entropy matches at every code size, all nodes preserve the
entropy/reconstruction signal, shared-horizon erasure remains non-correctable
with survivor fixed point `(false,false)`, and the algebra-difference count is
flat at `3` on the mixed path and across the full graph.

The Phase 16 recommendation is `adapt_then_proceed`: add non-CSS code-changing
edges or explicit local Clifford/graph moves, then test whether the Phase 15
repaired-horizon semantics survive mixed code-cover dynamics or collapse back
to the rigid CSS bridge-growth baseline.

## Goal 2 Phase 17: Repaired Non-CSS Local-Clifford Flow

Phase 17 adds explicit local-Clifford code-transformation edges to the repaired
non-CSS Phase 12 hit. The cover is fixed at the atlas-aware repaired hit
`private:p1:q13`, while the code pair is transformed by two disjoint toggles:

- `H_on_shared_horizon`, applied to the shared-horizon qubit;
- `S_on_observer_q_private`, applied to observer Q's private shell.

These two toggles form a four-node hypercube. Each edge flips one toggle and
verifies, by direct phase-free Pauli transformation, that the target stabilizer
generators are exactly obtained from the source generators. Thus Phase 17 is a
code-flow probe, not just a cover-flow replay.

The certificate finds 4 nodes and 4 local-Clifford edges. The canonical path
`repaired_lc:h0:s0 -> repaired_lc:h0:s1 -> repaired_lc:h1:s1` uses two
code-transform edges. Across the whole local-Clifford graph, all nodes preserve
the entropy/reconstruction signal and QEC complementarity, shared-horizon
erasure remains correctable with survivor fixed point `(true,true)`, and the
erasure-algebra difference names stay
`erase_observer_q_private, erase_observer_q` with count `2`.

The phase also compares against the Phase 16 CSS mixed bridge-growth baseline:
the CSS mixed graph keeps shared-horizon erasure non-correctable
`(false,false)` with algebra-difference count `3`, while the repaired non-CSS
local-Clifford graph keeps the same role correctable `(true,true)` with count
`2`. This shows the repaired semantics are not an artifact of one stabilizer
generator presentation.

The Phase 17 recommendation is `adapt_then_proceed`: add non-CSS code-changing
edges that are not merely local-unitary equivalences, such as outer-code swaps,
graph-edge mutations, or concatenation-depth changes.

## Goal 2 Phase 18: Outer-Code Swap Taxonomy

Phase 18 tests non-CSS repair transformations that are not just local-Clifford
presentation changes on the repaired `n=20` code. It fixes the same repaired
cover as Phase 17 and swaps the four-qubit outer repair code used in the Phase
11 logical concatenation. Every outer code in the bounded menu has `n=4`,
`k=1`, distance `2`, and the same minimal reconstruction-region shape.

The certificate compares four outer repairs:

- `phase11_outer`: the original repaired hit;
- `same_class_preserve`: a same outer local-Clifford class swap that preserves
  the full repaired semantics;
- `same_class_collapse`: a same outer local-Clifford class swap that preserves
  low-order entropy and shared-horizon semantics but collapses the observer
  algebra separation;
- `distinct_class_entropy_break`: a distinct outer local-Clifford class swap
  that keeps shared-horizon semantics but breaks low-order entropy matching.

This gives a three-way exact taxonomy rather than a yes/no result. Shared
horizon erasure remains correctable with survivor fixed point `(true,true)` for
all checked outer swaps. Low-order entropy and observer algebra are stricter:
one swap preserves both, one preserves low-order entropy but removes the
erasure-algebra difference set, and one breaks low-order entropy.

The Phase 18 recommendation is `adapt_then_proceed`: run a bounded
outer-code/graph-mutation search that scores transformations into these
taxonomy buckets, then extract structural features of the transformations that
preserve horizon fixed points and nonzero erasure-algebra differences.

## Goal 2 Phase 19: Bounded Outer-Code Mutation Search

Phase 19 turns the Phase 18 hand-sized outer-code taxonomy into an explicit
bounded search. Starting from the Phase 11 outer repair code, it enumerates all
single-entry Pauli mutations of radius one and two, dedupes by stabilizer
generator span, and keeps only valid `n=4`, `k=1`, distance-`2` outer codes
with the same minimal reconstruction-region shape as the baseline. Each
accepted outer code is concatenated with the fixed Phase 10 graph/CWS inner
pair and scored on the repaired Phase 12 cover.

The default search accepts 37 mutated outer codes. The exact outcome counts are:

- 25 full-semantics-preserving mutations;
- 8 operator-geometry-collapsing mutations;
- 4 low-order-entropy-breaking mutations.

The radius split is the useful structural signal. Radius-one mutations already
recover preservation and operator collapse, but they do not break low-order
entropy. Radius-two mutations introduce entropy breaks. Two of those entropy
breaks collapse the observer algebra, while two are sharper: labeled `t=2`
entropy breaks, but the observer reconstruction signal and two erasure-algebra
differences survive.

Across every accepted mutation, shared-horizon erasure remains correctable with
survivor fixed point `(true,true)`. Thus Phase 19 strengthens the Phase 18
lesson: shared-horizon channel semantics are robust in this mutation ball, but
low-order entropy and operator reconstruction split into independently
search-visible features.

The Phase 19 recommendation is `adapt_then_proceed`: run a bounded inner
graph/CWS mutation search under the fixed repaired outer code and Phase 12
cover, then compare whether the same bucket structure appears when the inner
connectivity changes instead of only the outer repair.

## Goal 2 Phase 20: Bounded Inner Graph/CWS Mutation Search

Phase 20 mutates the Phase 10 inner graph/CWS source instead of the outer repair
code. It keeps the Phase 11 outer distance repair and the repaired Phase 12
cover fixed, then toggles one graph edge on exactly one side of the inner pair.
The kept graph-generator indices stay fixed at `(0,1,2,3)`, so the search is a
20-node radius-one edge-toggle ball: 10 possible edge toggles on the first
inner graph and 10 on the second.

Every accepted mutation is logically concatenated with the fixed outer repair
and scored with the same exact rank-kernel entropy, operator-algebra, erasure,
fixed-point, and QEC-complementarity diagnostics. The search finds:

- 4 full-semantics-preserving inner graph toggles;
- 2 operator-geometry-collapsing toggles;
- 13 low-order-entropy-breaking toggles;
- 9 toggles where the observer reconstruction signal survives.

The important contrast with Phase 19 is radius sensitivity. Phase 19 outer-code
radius-one mutations never broke low-order entropy; Phase 20 inner graph-edge
radius-one mutations do. The inner search also produces richer algebra buckets:
some entropy breaks leave algebra residue after the observer signal collapses,
and one entropy-preserving mutation adds extra erasure-algebra differences.

Across all 20 inner graph mutations, shared-horizon erasure remains correctable
with survivor fixed point `(true,true)`. The pressure-test lesson is therefore
sharper: fixed horizon channel semantics can survive both outer repair edits and
inner connectivity edits, but inner connectivity is the more sensitive control
knob for low-order entropy and operator-algebra structure.

The Phase 20 recommendation is `adapt_then_proceed`: build a mixed inner-outer
mutation graph whose edges are certified single inner graph toggles or single
outer repair mutations, then classify reachable bucket transitions and
monotonicity failures.

## Goal 2 Phase 21: Mixed Inner-Outer Transition Graph

Phase 21 combines the Phase 19 outer repair mutation atlas with the Phase 20
inner graph/CWS mutation atlas. To keep the graph exact and bounded, it takes
one representative inner graph toggle from each Phase 20 bucket, crosses those
seven inner states with the baseline plus all six Phase 19 radius-one outer
mutations, and scores the resulting `7 x 7` product graph.

The certificate has 49 nodes, 84 certified axis edges, and 36 commuting
inner/outer squares. Every edge is either:

- `inner_graph_toggle`: same outer repair, one selected inner graph-edge toggle;
- `outer_repair_mutation`: same inner graph pair, one radius-one outer repair
  mutation.

Every node is checked with exact rank-kernel entropy, operator algebra, erasure
correctability, survivor fixed points, and QEC-complementarity diagnostics. The
shared-horizon erasure profile remains correctable with survivor fixed point
`(true,true)` across the whole mixed graph.

The new pressure-test is monotonicity. Algebra-difference count is not monotone
on the mixed graph: 14 certified edges increase it, 11 decrease it, and 59 keep
it flat. The graph also has 21 entropy-match-flip edges and 17
observer-signal-flip edges. Thus the same stable horizon channel semantics can
coexist with reachable entropy breaks, operator collapse, and extra
algebra-residue buckets within two exact mutation steps.

The Phase 21 recommendation is `adapt_then_proceed`: add a time/channel layer on
this mixed graph, treating edges as elementary stochastic or deterministic
transitions, then certify stationary bucket weights, absorbing sets, and horizon
fixed-point invariants exactly over rational transition matrices.

## Goal 2 Phase 22: Exact Time/Channel Dynamics

Phase 22 adds exact rational transition dynamics on the certified Phase 21 mixed
inner-outer graph. It does not sample trajectories or estimate probabilities.
Instead, it emits sparse transition matrices with rational entries and verifies
their claims by exact arithmetic.

The certificate defines two channels:

- `uniform_edge_random_walk`: from each node, choose a neighboring Phase 21
  transition edge uniformly. The stationary distribution is verified exactly by
  checking `pi P = pi`. Its stationary bucket weights include
  `full_semantics_preserved = 8/21` and `operator_geometry_collapsed = 5/28`.
- `algebra_descent_channel`: from each node, choose uniformly among adjacent
  nodes with strictly smaller algebra-difference count; if no such neighbor
  exists, stay fixed. This channel is exactly row-stochastic and algebra
  nonincreasing on every positive-probability transition.

The descent channel has 28 absorbing local-minimum nodes. They are not all
global algebra minima: the absorbing algebra counts are `(0,2)`. From a uniform
initial node distribution, the exact absorbing bucket weights include
`operator_geometry_collapsed = 29/49` and
`entropy_break_operator_collapsed_algebra_residue = 13/98`.

Both channels preserve the repaired shared-horizon correctability and survivor
fixed-point profile `(true,true)` on every positive-probability transition. The
time-dynamics lesson is that the same static toy cosmology can support both a
reversible stationary flow and an irreversible absorbing flow while keeping the
horizon channel semantics fixed.

The Phase 22 recommendation is `adapt_then_proceed`: add a small family of
exact biased channels on the Phase 21 graph, then certify which bucket weights,
absorbing classes, and horizon invariants are robust under changing transition
rules.

## Goal 2 Phase 23: Biased Channel Comparison

Phase 23 keeps the same certified Phase 21 mixed inner-outer transition graph
and compares a small family of exact rational channel rules. The reversible
channels are weighted random walks with symmetric integer edge weights, so their
stationary distributions are not numerically estimated: each is certified by
the exact weighted-degree formula and by checking `pi P = pi` over rational
entries.

The four reversible walks are:

- `uniform_edge_random_walk`: all adjacent transition edges have weight `1`;
- `entropy_match_preserving_bias`: entropy-match-preserving edges have weight
  `2`, entropy-flip edges have weight `1`;
- `observer_signal_preserving_bias`: observer-signal-preserving edges have
  weight `2`, signal-flip edges have weight `1`;
- `algebra_flat_bias`: algebra-difference-flat edges have weight `2`,
  algebra-changing edges have weight `1`.

The stationary bucket weights are rule-dependent in every bucket. For example,
`full_semantics_preserved` has weights `8/21`, `55/147`, `57/151`, and
`54/143` across the four walks, while `operator_geometry_collapsed` has weights
`5/28`, `19/98`, `51/302`, and `25/143`. Thus even reversible local dynamics
on the same static graph can change the emergent bucket measure.

Phase 23 also compares absorbing structure against the Phase 22
`algebra_descent_channel`. All four biased walks have one closed communicating
class of size `49` and no absorbing nodes. Algebra descent has `28` singleton
closed classes, all absorbing. Absorbing structure is therefore strongly
rule-dependent, not a graph-only invariant.

The stable diagnostic is the repaired shared horizon: every compared channel
preserves shared-horizon correctability and survivor fixed point `(true,true)`
on every positive-probability transition. In this toy universe, horizon-channel
semantics are more robust than stationary bucket weights or absorbing classes.

The Phase 23 recommendation is `adapt_then_proceed`: search over bounded exact
channel rules, rather than hand-picking them, and certify extremal stationary
bucket weights plus absorbing-class no-go/yes-go patterns under preserved
horizon semantics.

## Goal 2 Phase 24: Bounded Channel-Rule Search

Phase 24 turns the Phase 23 hand-picked channel comparison into a bounded exact
search. It keeps the Phase 21 graph fixed and enumerates two small rule
families.

The first family has 27 positive symmetric weighted walks. Each edge weight is

```text
1 + e*[same low-order entropy flag]
  + o*[same observer-signal flag]
  + a*[same algebra-difference count]
```

with `e,o,a in {0,1,2}`. Because these are symmetric positive integer edge
weights on the connected Phase 21 graph, each rule has an exact stationary
distribution from weighted degrees. The certificate verifies row stochasticity,
symmetry, positivity, and `pi P = pi` exactly for every rule.

The search certifies stationary extrema for every outcome bucket. For example:

- `full_semantics_preserved` ranges from `13/35`, attained by
  `edge_bonus_e2_o0_a0`, up to `8/21`, attained by the uniform rule
  `edge_bonus_e0_o0_a0`;
- `operator_geometry_collapsed` ranges from `18/109`, attained by
  `edge_bonus_e0_o2_a0`, up to `1/5`, attained by `edge_bonus_e2_o0_a0`;
- `entropy_break_operator_collapsed_algebra_residue` ranges from `69/688` to
  `51/404`.

The second family has 7 score-descent channels. Each score is a nonzero
`{0,1}` linear combination of algebra-difference count, the low-order entropy
match bit, and the observer-signal bit. A node moves uniformly to adjacent nodes
with strictly lower score, or stays fixed if none exist. The certificate
verifies exact absorption probabilities for every rule.

The no-go/yes-go result is sharp in this finite model:

- every positive symmetric weighted walk has one closed communicating class of
  size `49` and no absorbing nodes;
- every score-descent rule has absorbing nodes, and the count is rule-dependent,
  ranging from `28` to `42`.

Across all 34 searched rules, every positive-probability transition preserves
the repaired shared-horizon correctability and survivor fixed point
`(true,true)`. Thus the searched channel rules can move stationary measures and
absorbing landscapes, but not this horizon invariant.

The Phase 24 recommendation is `adapt_then_proceed`: add target-constrained
channel synthesis that searches for minimal exact rules maximizing a specified
bucket gap while holding horizon and observer-patch constraints fixed.

## Goal 2 Phase 25: Target-Constrained Channel Synthesis

Phase 25 uses the same bounded weighted-walk rule language as Phase 24, but
switches from extrema-per-bucket to synthesis-per-target. The candidate rules
are the 27 positive symmetric edge-bonus rules with `e,o,a in {0,1,2}`. Every
candidate is required to satisfy the hard constraints:

- exact rational row-stochastic transition matrix;
- positive symmetric edge weights;
- stationary distribution verified by exact `pi P = pi`;
- transitions restricted to certified Phase 21 observer edges;
- repaired shared-horizon correctability and survivor fixed point `(true,true)`
  preserved on positive-probability transitions.

The certificate groups outcome buckets into three target metrics:

- `full_semantics`;
- `entropy_break`;
- `operator_collapse`.

It then maximizes six signed bucket-gap objectives and emits the
least-complexity rule witnesses among exact maximizers. Complexity is ordered by
total feature bonus, then number of nonzero feature terms, largest single
feature bonus, and rule name.

Example exact witnesses:

- `full_semantics - entropy_break` is maximized by `edge_bonus_e2_o0_a0` with
  gap `9/140`;
- `full_semantics - operator_collapse` is maximized by `edge_bonus_e0_o2_a0`
  with gap `39/436`;
- `operator_collapse - entropy_break` is maximized by `edge_bonus_e2_o0_a0`
  with gap `1/70`.

Two target preferences remain impossible inside this bounded rule language:
even the best rule has negative gap for `entropy_break - full_semantics`
(`-7/404`) and for `operator_collapse - full_semantics` (`-1/20`). This gives a
small certified no-go: the search can bias toward entropy breaks or operator
collapse, but cannot make either grouped weight exceed full semantics while
preserving the hard constraints.

The Pareto frontier over `(full_semantics, entropy_break, operator_collapse)`
has 7 rules and 7 distinct metric vectors; the other 20 candidate rules are
dominated. The frontier includes the uniform rule and several nonuniform
witnesses, showing that no single channel rule optimizes all three emergent
structure metrics at once.

The Phase 25 recommendation is `adapt_then_proceed`: test whether these minimal
rule witnesses transfer across nearby graph substrates, or whether they are
overfit to the Phase 21 mixed graph.

## Goal 2 Phase 26: Cross-Substrate Rule Transfer

Phase 26 asks whether the Phase 25 channel-rule witnesses are robust facts
about the finite toy cosmology, or artifacts of one transition graph. It keeps
the same 49 exact Phase 21 nodes and the same 27 positive symmetric weighted
walk rules, then evaluates target synthesis on four certified substrates:

- `full_mixed_graph`: all 84 certified Phase 21 edges;
- `entropy_stable_edges`: the 63 edges that do not flip the low-order entropy
  match flag;
- `observer_signal_stable_edges`: the 67 edges that do not flip the
  entropy/reconstruction signal flag;
- `algebra_flat_edges`: the 59 edges with zero algebra-difference-count delta.

Every substrate is an edge-filtered subgraph of the certified Phase 21 graph.
Every candidate rule is rechecked for exact row stochasticity, positive
symmetric edge weights, exact stationarity, certified observer-edge transitions,
and preserved shared-horizon correctability/fixed point `(true,true)`.

The transfer result is mixed, which is the point. Across the three nonbaseline
substrates and six target objectives, 16 baseline minimal witnesses remain
maximizers and 2 fail to transfer. The no-transfer counterexamples are:

- on `entropy_stable_edges`, the baseline witness for
  `entropy_break - operator_collapse` fails; the new maximizer is
  `edge_bonus_e0_o2_a2` with gap `3/514`;
- on `observer_signal_stable_edges`, the baseline witness for
  `operator_collapse - full_semantics` fails; the new maximizer is
  `edge_bonus_e0_o0_a2` with gap `-13/173`.

Pareto transfer also changes on every nonbaseline substrate. The entropy-stable
and observer-signal-stable substrates preserve all baseline frontier rules but
add new frontier rules. The algebra-flat substrate drops four baseline frontier
rules and adds none. Thus a synthesized rule must be reported with its substrate
assumptions: some target behavior transfers, but not all.

The Phase 26 recommendation is `adapt_then_proceed`: synthesize channel rules
jointly over multiple substrates, maximizing worst-case target gaps and
separating robust witnesses from graph-overfit witnesses.

## Goal 2 Phase 27: Robust Channel Synthesis

Phase 27 synthesizes channel rules jointly over the Phase 26 substrate family.
Instead of optimizing on one transition graph and checking transfer afterward,
it evaluates every candidate rule on all four substrates and scores each target
objective by its worst-case signed gap.

The bounded search space is unchanged:

- 27 positive symmetric edge-bonus weighted walks;
- 4 certified substrates: full graph, entropy-stable edges,
  observer-signal-stable edges, and algebra-flat edges;
- 6 signed target objectives over `full_semantics`, `entropy_break`, and
  `operator_collapse`.

For each objective, the certificate computes exact gaps on every substrate,
takes the minimum, and emits the least-complexity rule among maximizers of that
worst-case value.

Robust witnesses include:

- `full_semantics - entropy_break`: `edge_bonus_e2_o0_a0`, worst-case gap
  `2/149`;
- `full_semantics - operator_collapse`: `edge_bonus_e0_o2_a0`, worst-case gap
  `3/55`;
- `entropy_break - operator_collapse`: `edge_bonus_e0_o2_a2`, worst-case gap
  `3/514`.

Three objectives remain robust no-go cases: their best worst-case gaps are
negative. For example, `operator_collapse - entropy_break` is maximized by
`edge_bonus_e2_o0_a0`, but its worst-case gap is `-5/114` on the
observer-signal-stable substrate.

The robust Pareto frontier over worst-case
`(full_semantics, entropy_break, operator_collapse)` has 17 rules and 17 metric
vectors; the other 10 rules are dominated. This frontier is larger than the
single-substrate Phase 25 frontier, reflecting that robustness preserves
different tradeoff shapes across filtered transition geometries.

Across all candidates and substrates, the repaired shared-horizon
correctability and survivor fixed point `(true,true)` remain invariant. Thus
the robust wins and robust no-go results are about transition geometry, not
horizon failure.

The Phase 27 recommendation is `adapt_then_proceed`: add a symbolic/audited
rule-language proof layer explaining which rule features force the robust no-go
cases and which allow positive robust gaps, then check those explanations
against exact enumeration.

## Goal 2 Phase 28: Audited Rule-Language Proof

Phase 28 wraps the robust Phase 27 enumeration in a theorem-style audited proof
layer. The rule language is finite and explicit:

```text
edge_bonus_e{entropy_bonus}_o{observer_bonus}_a{algebra_bonus}
```

with each bonus in `{0,1,2}` and edge weight

```text
1 + entropy_bonus*[same low-order entropy flag]
  + observer_bonus*[same observer-signal flag]
  + algebra_bonus*[same algebra-difference count].
```

For each target objective, Phase 28 states a feature predicate and checks that
the predicate selects exactly the robust maximizers found by exact enumeration.
It also checks the sign of the exact worst-case gap and records the substrate
where the worst case is attained.

The audited feature conditions are:

- `full_semantics - entropy_break`: `entropy_bonus=2, observer_bonus=0,
  algebra_bonus=0`, gap `2/149`, positive;
- `full_semantics - operator_collapse`: `entropy_bonus=0, observer_bonus=2,
  algebra_bonus=0`, gap `3/55`, positive;
- `entropy_break - full_semantics`: `entropy_bonus=0, observer_bonus=0,
  algebra_bonus=2`, gap `-7/153`, no-go;
- `operator_collapse - full_semantics`: `entropy_bonus=0, observer_bonus=0,
  algebra_bonus=2`, gap `-13/173`, no-go;
- `entropy_break - operator_collapse`: `entropy_bonus=0, observer_bonus=2,
  algebra_bonus=2`, gap `3/514`, positive;
- `operator_collapse - entropy_break`: `entropy_bonus=2, observer_bonus=0,
  algebra_bonus=0`, gap `-5/114`, no-go.

Thus Phase 28 does not merely state a symbolic interpretation of the robust
search. It emits proof text plus machine-checkable obligations:

- the rule schema covers all 27 enumerated candidates;
- one audited feature condition exists for each target objective;
- each feature condition selects exactly the robust maximizer set;
- minimal witnesses obey the feature condition;
- positive/no-go sign classifications match exact worst-case gaps;
- every audit records an exact worst-case substrate.

The Phase 28 recommendation is `adapt_then_proceed`: move from audited rule
features to bounded code/cover co-design, searching for nearby cover or
substrate changes that flip or preserve robust no-go signs while keeping the
same audit schema.

## Goal 2 Phase 29: Bounded Substrate-Family Co-Design

Phase 29 makes the Phase 28 no-go claims work harder. It keeps the exact
three-bonus rule language but varies the robust substrate family over the full
Phase 21 graph plus every subset of the three Phase 26 filtered substrates:

```text
full_mixed_graph + subset{entropy_stable_edges,
                          observer_signal_stable_edges,
                          algebra_flat_edges}
```

This gives exactly eight robust families. For each family, Phase 29 recomputes
all 27 exact minimax rule scores, derives the bonus-signature predicates for
that family's exact maximizers, and checks that the predicates select exactly
the maximizer set. It also reruns the Phase 28 predicates as transfer claims,
so the output records where the old proof conditions still apply and where
they fail.

The search finds two negative-to-positive no-go flips. In the Phase 28
all-filter family, `operator_collapse - entropy_break` has best worst-case gap
`-5/114`; in both `full_only` and `full_plus_entropy`, the same objective flips
to `1/70`. This is a concrete substrate-family artifact, not a failure of the
horizon constraints.

Two negative objectives remain negative across all eight families that include
the full mixed substrate:

- `entropy_break - full_semantics`;
- `operator_collapse - full_semantics`.

Thus Phase 29 separates fragile robust no-go signs from persistent ones inside
the bounded substrate-family search. The certificate also confirms that every
included substrate remains certified, every local feature audit is exact, and
the repaired shared-horizon profile remains invariant throughout the search.

The Phase 29 recommendation is `adapt_then_proceed`: move from substrate-family
co-design to observer-cover co-design, changing patch covers or observer roles
and checking whether the persistent signs survive.

## Goal 2 Phase 30: Bounded Observer-Cover Co-Design

Phase 30 moves the co-design knob from substrate-family selection to observer
cover choice. It evaluates four selected Phase 12 private-full/shared-inner
covers:

- three strict repaired-cover hits whose seed certificates pass the full
  entropy, horizon, reconstruction, and erasure-profile gate;
- one explicit near-miss whose entropy/reconstruction data look promising but
  whose erasure-correctability profile fails.

For each cover, the certificate rebuilds the mixed inner/outer transition
graph, applies the four Phase 26 substrate filters, recomputes all 27 exact
robust channel-rule scores, and audits the cover-local feature predicates
against exact enumeration.

The strict cover `strict_operator_flip_p3_q13` flips one Phase 29 persistent
no-go sign: `operator_collapse - full_semantics` changes from `-13/173` on the
baseline cover to `3/70`. The same cover also reshapes the rest of the sign
pattern, so the certificate treats it as a cover-level pressure test rather
than a universal improvement.

The other Phase 29 persistent no-go, `entropy_break - full_semantics`, remains
negative for the selected strict repaired-cover hits. A near-miss cover,
`near_miss_entropy_flip_p3_q5`, flips it from `-7/153` to `7/365`, but that
cover is rejected because its seed erasure-correctability profiles differ.
Thus the tempting entropy flip is recorded as pressure on the erasure gate, not
accepted as a strict cover witness.

The Phase 30 recommendation is `adapt_then_proceed`: exhaust the eight strict
Phase 12 repaired-cover hits or synthesize strict covers directly against a
target sign, keeping the erasure gate hard.

## Goal 2 Phase 31: Strict-Cover Exhaustive Audit

Phase 31 exhausts the Phase 12 private-full/shared-inner repaired-cover family
under the strict causal-patch gate. It scans all 175 ordered overlapping block
mask covers, checks the full seed cover certificate for each, and separates:

- 66 raw entropy/reconstruction/horizon hits;
- 8 strict repaired-cover hits;
- 58 raw hits rejected by the erasure-correctability-profile gate.

The certificate then rebuilds the mixed inner/outer transition graph for each
of the eight strict covers, reruns the four Phase 26 substrate filters and all
27 robust channel rules, and audits cover-local feature predicates against
exact enumeration.

The entropy objective `entropy_break - full_semantics` is a strict-cover no-go
for this whole family. Its best exact worst-case gap is still negative on every
strict cover: the maximum is `-1/53`, attained on `strict_hit_p3_q13`,
`strict_hit_p6_q13`, `strict_hit_p10_q7`, and `strict_hit_p12_q11`.

Operator-related sign flips are completely classified by the private-block
pattern in this strict family. The four covers with nonempty
`observer_p_private_blocks` flip both:

- `operator_collapse - full_semantics`, whose maximum becomes `3/70`;
- `operator_collapse - entropy_break`, whose maximum becomes `19/284`.

The four covers with empty `observer_p_private_blocks` preserve the baseline
operator signs. Thus the Phase 31 toy lesson is sharper than Phase 30: the
entropy no-go survives the strict repaired-cover family, while operator
geometry is cover-private-block sensitive.

The Phase 31 recommendation is `adapt_then_proceed`: search a broader bounded
cover grammar, or synthesize strict covers directly against the entropy
objective while keeping the erasure gate hard.

## Goal 3 Phase 1: Stabilizer Tensor-Network Seed Atlas

Goal 3 starts from the consolidated causal-patch results and wraps the
`m=1` balanced-bridge CSS pair in an explicit finite tensor-network skeleton:
eight boundary qubits on a ring,
`(0, 1, 6, 2, 3, 7, 4, 5)`, plus one bulk-center node with unit-capacity
spokes to every boundary qubit. Min-cuts are certified exactly by exhaustive
assignment of the internal node, so the command checks a concrete graph
diagnostic instead of invoking continuum geometry language.

The certificate deliberately separates three finite notions of geometry:

- min-cut-visible geometry from the shared ring-spoke skeleton;
- entropy-visible geometry from exact stabilizer subsystem entropies;
- reconstruction-visible geometry from region algebra, erasure, and survivor
  fixed-point checks.

Both code realizations have `n=8,k=1,d=2`, share the same min-cut profile, and
match all named patch entropies plus all boundary-ring interval entropies of
length one and two. Nevertheless the observer patches still separate:
`observer_p=(1,2,3,6)` and `observer_q=(1,2,3,7)` have central-only algebra in
the first code and full logical reconstruction in the second, while the shared
horizon algebra matches. A low-order boundary interval witness,
`(5,0)`, has matching entropy but different erasure-correctability and survivor
fixed-point reconstruction.

This is not a global RT theorem. The ring-spoke graph is a finite diagnostic
wrapper around the balanced-bridge seed, and its min-cut values are reported
beside exact entropies rather than identified with them. The Phase 1
recommendation is `adapt_then_proceed`: next search small graph-state, CSS
tensor-network, or Clifford-MERA-like families for less hand-seeded examples
with the same exact diagnostics.

## Goal 3 Phase 2: Bounded Graph/CWS Ring-Spoke Atlas

Phase 2 runs the first less hand-seeded Goal 3 search. It scans exact finite
`n=5,k=1` source menus under the strict robust labeled-entropy constraints:
CSS, cyclic-CSS, graph-subspace, and shallow-encoder codes. All four strict
menus are exhausted within their stated generator bounds and return no
entropy-matched reconstruction-discordant pair.

The phase then relaxes the graph/CWS guardrail to the labeled distance-one
calibration constraints used by the earlier non-CSS frontier work. That bounded
graph-subspace scan finds a pair after 24 raw records:

```text
first:  XIXZI, IXZXI, IZXII, ZIIXI
second: XIXZZ, IXZXI, IZXII, ZIIXI
```

Both codes have `n=5,k=1,d=1`, so the result is explicitly frontier evidence,
not a robust horizon-code theorem. The search then checks all 12 boundary ring
orders modulo rotation and reversal on a ring-spoke min-cut skeleton with one
bulk-center node. For the selected order `(0,1,2,4,3)`, all length-one and
length-two ring-interval entropies match and the min-cut profile is shared, but
the length-two interval `(2,4)` has different observer-algebra semantics:

```text
entropy:          2 versus 2
min-cut:          4 versus 4
algebra:          (2,0,0,true) versus (1,1,1,false)
erasure profile:  false versus false
```

Thus Phase 2 isolates a reconstruction-visible split in a graph/CWS-derived
ring-spoke toy while the entropy-visible and min-cut-visible data match. It does
not yet isolate a channel/erasure-visible split, and it does not repair the
distance-one weakness.

The Phase 2 recommendation is `adapt_then_proceed`: run exact distance-repair or
small concatenation transforms on the graph/CWS ring witness, then replay the
same ring-spoke min-cut, entropy, algebra, erasure, and survivor checks.

## Goal 3 Phase 3: Distance-Repaired Lifted Ring-Spoke Atlas

Phase 3 repairs the Phase 2 graph/CWS ring witness by logically concatenating
both inner codes with the existing four-qubit `k=1,d=2` outer stabilizer code.
The repaired pair has `n=20,k=1`, and exact bounded logical search excludes all
weight-one logical operators in both codes:

```text
distance lower bound: d >= 2
checked weights:      1
logical witnesses:    none in either repaired code
```

The repair preserves all labeled subsystem entropies through size two: the
certificate checks 211 subsets and finds zero mismatches. It then scores three
source-aware repaired boundary orders on the same ring-spoke min-cut skeleton:
block-contiguous, inner-position interleaved, and witness-strip. All three have
matching length-one and length-two ring-interval entropy profiles and shared
min-cut profiles.

The original Phase 2 interval `(2,4)` no longer gives an operator split inside
a single repaired block: all four single-block lifts collapse to matching
algebra and erasure behavior. But lifting the same inner interval over exactly
two outer blocks produces six exact hits. The selected source-aware
witness-strip hit is block mask `3`, region `(2,4,7,9)`, a boundary interval of
length four in the witness-strip order:

```text
entropy:          4 versus 4
min-cut:          6 versus 6
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
survivor fixed:   false versus true
```

Larger lifts are not accepted automatically: block masks `7,11,13,14,15` are
rejected by the entropy gate. Thus Phase 3 gives a repaired holographic-code
cousin of the bridge phenomenon, but with source-aware atlas semantics: the
entropy/min-cut-visible geometry matches, while reconstruction-visible and
channel/erasure-visible geometry split on a lifted two-block witness.

The Phase 3 recommendation is `adapt_then_proceed`: search less source-aware
small stabilizer tensor-network layouts, including multi-bulk-node ring/tiling,
HaPPY-like, or Clifford-MERA-like skeletons, and replay the same exact
diagnostics.

## Goal 3 Phase 4: Multi-Bulk-Node Layout Audit

Phase 4 keeps the repaired Phase 3 `n=20,k=1,d>=2` code pair fixed and asks a
more geometric question: does the lifted witness remain a compact causal patch
when the boundary order and min-cut skeleton are less source-aware?

The certificate scores four boundary orders:

- raw natural block order;
- block-contiguous Phase 2 ring order;
- inner-position interleaved order;
- the source-aware witness-strip order from Phase 3.

For each boundary order it scores four exact min-cut skeletons:

- one central bulk node with boundary spokes;
- four outer-block bulk nodes connected by a path;
- five inner-position bulk nodes connected by a cycle;
- a binary outer-block tree.

All 16 layout candidates have matching length-one and length-two ring-interval
entropy profiles, and every min-cut is computed by exhaustive internal-node
assignment. The selected Phase 3 witness `(2,4,7,9)` still has the same
operator/channel split in every layout:

```text
entropy:          4 versus 4
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
survivor fixed:   false versus true
```

What changes is locality. The source-aware witness-strip order recovers the
witness as a strict boundary interval of length four for all four min-cut
skeletons. The less source-aware layouts are exact near-misses: they preserve
the entropy/min-cut and operator/channel facts, but the smallest boundary
interval covering the witness has extra sites:

```text
natural block order:          cover length 8
block-contiguous Phase 2:     cover length 7
inner-position interleaved:   cover length 6
source-aware witness strip:   cover length 4
```

Thus Phase 4 sharpens the Phase 3 caveat. The repaired operator/channel witness
is robust across these multi-bulk-node skeletons, but compact causal-patch
locality is still source-aware in this bounded layout class.

The Phase 4 recommendation is `adapt_then_proceed`: search generated
Clifford-MERA, HaPPY-like, or graph-state tensor-network layouts where boundary
locality is not manually inherited from the repaired witness strip.

## Goal 3 Phase 5: Generated Clifford/MERA-Style Layout Search

Phase 5 removes the manually inherited witness-strip order from the search
grammar and generates boundary layouts instead. The bounded grammar includes:

- all affine modular ring scans `q_i=b+a*i mod 20` with `gcd(a,20)=1`;
- five-bit bit-reversal, Gray-code, and bit-reversed Gray-code orders;
- a riffled-halves butterfly order;
- natural tensor-product block/inner orders;
- two Phase-2-seeded tensor-product orders that may use the Phase 2 inner ring
  but do not use the lifted witness strip.

The certificate scores 169 raw generated layouts, deduplicates them to 168
unique boundary orders, and audits the repaired Phase 3 witness `(2,4,7,9)`
against the same four exact min-cut skeletons from Phase 4. All selected
min-cuts are enumerated exactly, and the repaired operator/channel split is
still present:

```text
entropy:          4 versus 4
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
survivor fixed:   false versus true
```

No generated layout recovers the witness as a strict compact boundary interval.
The exact cover-length distribution is:

```text
6:  1 layout
7:  1 layout
8:  80 layouts
10: 2 layouts
11: 1 layout
12: 80 layouts
13: 1 layout
14: 1 layout
15: 1 layout
```

The best source-agnostic layouts have cover length 8. The best Phase-2-seeded
layout, `inner_major_phase2_inner_ring`, improves this to cover length 6 with
cover `(2,7,12,17,4,9)`, but still fails strict locality. Thus Phase 5 turns the
Phase 4 caveat into a bounded generated-layout no-go: in this grammar,
operator/channel separation survives, but compact causal-patch locality does
not emerge without stronger source-aware structure.

The Phase 5 recommendation is `adapt_then_proceed`: move from boundary-order
generators to actual small stabilizer tensor-network constructions with
internal Clifford tensors and jointly generated boundary/bulk partitions.

## Goal 3 Phase 6: Generated Clifford Tensor-Network Audit

Phase 6 moves from boundary-order generation to actual Clifford tensor layers.
It keeps the repaired Phase 3 code pair fixed, transforms both codes by the same
bounded Clifford circuit, and checks the selected output patch `(2,4,7,9)` with
exact entropy, region algebra, erasure, survivor fixed point, and circuit
interaction min-cut diagnostics.

The audited Clifford tensor networks are:

- identity reference;
- all-boundary `H` layer;
- all-boundary `S` layer;
- even nearest-neighbor `CX` layer;
- butterfly half-pair `CX` layer;
- a source-aware Phase-2 witness-pair `CX` control.

All six circuits keep the selected patch entropy matched at `4 versus 4`, and
all circuit interaction min-cuts are computed by exhaustive internal-node
assignment. But operator/channel semantics are circuit-sensitive:

```text
identity / H / S:      split preserved
nearest-neighbor CX:   split collapsed
butterfly CX:          split preserved
witness-pair control:  split preserved
```

The nearest-neighbor `CX` layer collapses both codes to matching
`(0,0,2,false)` algebra and matching erasure-correctability on the selected
patch. The butterfly `CX` layer keeps entropy fixed but changes the first code
to full reconstruction `(2,0,0,true)` while the second remains `(0,0,2,false)`.
Thus Phase 6 gives a sharper tensor-network lesson: once internal Clifford
tensors are generated explicitly, entropy/min-cut-visible data can remain
fixed while reconstruction-visible and channel-visible geometry either survive
or collapse depending on the tensor layer.

The Phase 6 recommendation is `adapt_then_proceed`: run a bounded joint search
over Clifford circuits, compact output patches, and candidate bulk-logical
regions rather than fixing the Phase 3 witness patch in advance.

## Goal 3 Phase 7: Joint Clifford Circuit and Compact-Patch Search

Phase 7 takes the Phase 6 recommendation literally: it keeps the repaired
`n=20,k=1` code pair fixed, applies the same six Clifford tensor circuits, and
searches all compact output-boundary ring intervals of length one through six.
Candidate patches are promoted to hits only after exact entropy matching,
exact min-cut enumeration on the circuit interaction graph, and an exact
operator, erasure, or survivor fixed-point difference.

The bounded search checks:

```text
circuits scored:                 6
compact intervals scanned:       720
entropy-gate passes:             655
operator/channel hits:           23
distance-preserving hits:        11
low-distance frontier hits:      12
one-qubit frontier hits:         2
```

The main robust result is a replacement-patch phenomenon. In Phase 6, the
nearest-neighbor `CX` layer collapsed the fixed Phase 3 witness patch. Phase 7
shows that this does not mean the transformed tensor network lost the
separation: the same circuit has two compact length-six intervals that preserve
the weight-one distance audit and still separate the two code realizations. The
selected replacement interval is `(9,10,11,12,13,14)`:

```text
entropy:          2 versus 2
min-cut:          4 versus 4
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
survivor fixed:   false versus true
distance gate:    both transformed codes have no weight-one logical witness
```

The search also finds very small frontier hits. The butterfly `CX` layer
produces a one-site hit at `(4)`, and the source-aware control layer produces a
one-site hit at `(9)`. These are not reported as robust holographic-code hits:
the same exact certificate finds a weight-one logical witness in the first
transformed code for both circuits. Thus Phase 7 separates two lessons rather
than blending them:

- distance-preserving entangling layers can move the observer patch while
  preserving an exact compact reconstruction/channel split;
- one-site dramatic hits are real finite algebra facts, but they belong in a
  low-distance frontier bucket.

The Phase 7 recommendation is `adapt_then_proceed`: synthesize or enumerate
distance-preserving entangling Clifford layers with the compact patch search
inside the objective, then test HaPPY/perfect-tensor-like stabilizer blocks
under the same entropy, min-cut, algebra, erasure, survivor, and distance
gates.

## Goal 3 Phase 8: Distance-Gated Clifford Synthesis Search

Phase 8 turns the Phase 7 lesson into a bounded synthesis search. Instead of
auditing six named circuits, it generates 38 adjacent-pair `CX` layers from
boundary-order rules and puts the compact-patch search inside the objective.
The grammar includes:

- 30 affine modular adjacency layers: all stride-one offsets and ten even
  stride-three offsets;
- four hierarchical bit-order layers: bit reversal, Gray code, bit-reversed
  Gray code, and even/odd shuffle;
- four controls from riffle/tensor-product/Phase-2-seeded orders.

Every layer is checked by the exact weight-one distance gate before robust hits
are counted. Every candidate interval also gets exact entropy, circuit
interaction min-cut, region algebra, erasure, and survivor fixed-point checks.

```text
synthesized CX layers:           38
distance-preserving layers:      35
distance-gate rejections:        3
compact intervals scanned:       4560
entropy-gate passes:             4274
operator/channel hits:           130
distance-preserving hits:        95
low-distance frontier hits:      35
```

The main new result is that hierarchical layers improve compactness. The
affine adjacency layers all preserve distance and produce only length-six
robust hits. The hierarchical Gray-code family produces distance-preserving
length-four hits. The selected shortest robust witness is in the bit-reversed
Gray layer, interval `(12,19,4,11)`:

```text
entropy:          3 versus 3
min-cut:          2 versus 2
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
distance gate:    both transformed codes have no weight-one logical witness
```

The exact hit-length distributions are:

```text
distance-preserving:  length 4: 4, length 5: 8, length 6: 83
low-distance frontier: length 1: 3, length 2: 9, length 3: 7,
                       length 4: 7, length 5: 5, length 6: 4
```

Thus the one-site dramatic hits remain real algebra facts but are still
frontier artifacts: the exact distance gate rejects the riffle natural-halves,
inner-major natural, and inner-major Phase-2 layers because each creates a
weight-one logical witness in the first transformed code.

Phase 8 also records a locality warning. The block-major Phase-2 inner-ring
layer preserves the distance gate and keeps the fixed Phase 3 patch split, but
has zero compact interval hits of length at most six. So even a surviving fixed
observer-patch split does not automatically become a compact boundary patch in
the synthesized output geometry.

The Phase 8 recommendation is `adapt_then_proceed`: move from one-layer
adjacent-pair `CX` synthesis toward small perfect-tensor/HaPPY-like stabilizer
blocks or two-layer distance-gated circuits, keeping the same exact
entropy/min-cut/algebra/erasure/survivor checks.

## Goal 3 Phase 9: Compressed Pentagon Two-Layer Block Audit

Phase 9 moves from one-layer adjacency circuits to two-layer Clifford block
dynamics while keeping min-cut enumeration finite. It first screens all ordered
pairs from a 13-layer seed menu with the exact weight-one distance gate:

```text
seed layers:                  13
ordered two-layer pairs:      169
distance-gate accepted:       153
distance-gate rejected:       16
```

It then audits an 18-circuit block menu. The code dynamics are exact two-layer
Clifford circuits with 20 `CX` gates. The geometry is deliberately compressed:
the output boundary is scored on a five-pentagon block skeleton, with five
internal block nodes, four boundary legs per block, and capacity-2 cycle links.
Every min-cut is still exact, because the certificate enumerates all `2^5=32`
internal block assignments.

```text
block-menu circuits:             18
compact intervals scanned:       2160
entropy-gate passes:             2058
operator/channel hits:           112
distance-preserving hits:        112
max min-cut assignments:         32
```

The main result is a compactness improvement under the compressed block atlas.
Phase 8's one-layer distance-preserving witnesses first appeared at length
four. Phase 9 finds distance-preserving length-two witnesses and no
distance-preserving length-one witnesses. The selected shortest hit is the
two-layer bit-reversed Gray block, interval `(19,4)`:

```text
entropy:          2 versus 2
min-cut:          4 versus 4
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
distance gate:    both transformed codes have no weight-one logical witness
```

The exact robust hit-length distribution is:

```text
length 1: 0
length 2: 2
length 3: 7
length 4: 22
length 5: 34
length 6: 47
```

This is not a literal HaPPY theorem. The code transformations are exact
two-layer Clifford circuits, but the min-cut geometry is a declared compressed
pentagon-block skeleton rather than the full 20-gate interaction graph. The
lesson is still useful: once a finite block atlas is made explicit, compact
observer-patch locality can change while entropy-visible data and exact
operator/channel diagnostics remain separately checkable.

The Phase 9 recommendation is `adapt_then_proceed`: either construct a literal
small stabilizer perfect-tensor/`[[5,1,3]]` network with exact boundary-region
diagnostics, or strengthen the distance audit for the best Phase 8/9
transformed code pairs beyond weight-one logical exclusion.

## Goal 3 Phase 10: Five-Qubit Perfect Outer-Block Audit

Phase 10 follows the Phase 9 recommendation by replacing the compressed
pentagon-block story with a literal stabilizer `[[5,1,3]]` five-qubit perfect
outer code. The outer block has exact distance `3`, erasure threshold `2`, all
size-two-or-less erasures correctable, and all size-three regions reconstruct
the logical algebra. Concatenating this outer block with the Phase 2 graph/CWS
source gives a paired `n=25,k=1` finite code family with exact low-order
checks.

The exact distance audit is stronger than the Phase 8/9 weight-one screen:

```text
first concatenated code distance:   3
second concatenated code distance:  4
both distances at least three:      true
```

The two realizations still match all labeled subsystem entropies through size
two: the certificate checks 326 subsets and finds zero mismatches. The
distance profile differs, so this is not a same-distance theorem. It is a
literal perfect-outer-block pressure test where entropy matching, distance
repair, compact atlas locality, and observer algebra are all certified
separately.

Phase 10 scores three boundary atlases on a five-internal-node perfect-outer
block-cycle skeleton. Every min-cut is exact by exhaustive enumeration of all
`2^5=32` internal assignments.

```text
boundary atlases scored:              3
compact intervals scanned:            600
entropy-gate passes:                  493
entropy-gate rejections:              107
operator/channel compact hits:        29
block-contiguous compact hits:        0
inner-major compact hits:             12
witness-strip compact hits:           17
```

The block-contiguous atlas has no compact hits through length eight. The
inner-major atlas recovers length-three compact hits, with selected interval
`(4,9,14)`:

```text
entropy:          3 versus 3
min-cut:          5 versus 5
algebra:          (2,0,0,true) versus (0,0,2,false)
erasure profile:  false versus true
exact distances:  3 versus 4
```

The source-aware witness-strip atlas also recovers lifted Phase 2 witnesses:
31 block masks are checked, 10 three-block lifted hits pass the entropy and
operator/channel gates, and 3 of those are strict boundary-ring intervals. The
selected strict lifted hit is block mask `7`, region `(2,4,7,9,12,14)`, with
min-cut `8` and the same algebra split `(2,0,0,true)` versus
`(0,0,2,false)`.

Phase 10 is still not a full HaPPY theorem. It uses a literal perfect outer
stabilizer block and exact finite min-cut skeleton, but not a multi-tensor
hyperbolic tiling. The result is best read as a higher-distance holographic
cousin of the bridge phenomenon: low-order entropy and exact outer-block
semantics can be aligned while compact observer reconstruction and erasure
semantics still split.

The Phase 10 recommendation is `adapt_then_proceed`: search for same-distance
perfect-outer variants, or compose multiple five-qubit perfect tensors into a
small multi-tensor HaPPY-like stabilizer network with exact boundary entropy,
min-cut, region algebra, erasure, survivor, and distance certificates.

## Goal 3 Phase 11: Same-Distance Perfect-Outer Variant Search

Phase 11 directly attacks the Phase 10 caveat that the two perfect-outer
concatenated codes had different exact distances. It keeps the same Phase 2
graph/CWS inner source and the same literal `[[5,1,3]]` five-qubit perfect
outer block, but searches a bounded menu of outer logical-embedding variants:

- 4 global local-Clifford layers: `I`, `H`, `S`, and `HS` on every outer qubit;
- 15 single-site local-Clifford edits: `H`, `S`, or `HS` on one outer qubit;
- 10 two-site Hadamard edits;
- 10 two-site phase edits;
- 5 simple outer-qubit permutations: four cyclic shifts plus reversal.

Every variant remains a five-qubit perfect code with distance `3`, erasure
threshold `2`, all size-two-or-less erasures correctable, and all size-three
regions reconstructing. Every concatenated pair also preserves labeled
subsystem entropy matching through size two: all 44 variants check 326 subsets
with zero mismatches.

The exact bounded search separates two buckets:

```text
outer variants scored:                         44
same exact distance-3 concatenated variants:   20
asymmetric / second d>=4 under weight-3 audit: 24
same-distance variants with compact hits:      20
inner-major compact scans:                     4000 intervals
inner-major compact hits across same-distance: 240
minimum same-distance compact hit length:      3
```

The same-distance variants are exactly the single-site `H`/`HS` edits and the
two-site Hadamard edits in this menu. Global edits, pure phase edits, and the
simple outer permutations do not remove the Phase 10 distance asymmetry under
the weight-three audit.

The selected simplest witness is `q0_H`: apply a single Hadamard to outer
perfect-code qubit `0` before concatenation. Both resulting `n=25,k=1` codes
then have exact distance `3`:

```text
first logical witness:   qubits (4,9,14)
second logical witness:  qubits (4,9,24)
```

The compact atlas result survives unchanged. The selected inner-major interval
is again `(4,9,14)`:

```text
entropy:          3 versus 3
min-cut:          5 versus 5
algebra:          (2,0,0,true) versus (0,0,2,false)
erasure profile:  false versus true
exact distances:  3 versus 3
```

For the selected `q0_H` variant, the full Phase 10 atlas replay gives:

```text
block-contiguous hits:       0
inner-major hits:            12
witness-strip hits:          17
compact interval hits total: 29
strict lifted hits:          3
```

Thus the Phase 10 distance asymmetry is not an invariant of the literal
perfect-outer construction. Within this bounded menu, the outer tensor remains
perfect, low-order entropy still matches, exact min-cuts are still enumerated,
the compact observer algebra still splits, and the two code realizations can
have the same exact distance.

This is still a bounded result. Phase 11 does not exhaust the full local
Clifford/permutation orbit of the five-qubit code and does not build a full
multi-tensor HaPPY tiling. It is a small exact certificate that the
same-distance caveat can be repaired without losing the compact
operator/erasure witness.

The Phase 11 recommendation is `adapt_then_proceed`: either broaden the
perfect-outer local-Clifford/permutation search, or build a two-perfect-tensor
stabilizer tiling with exact boundary entropy, min-cut, region algebra,
erasure, survivor, and distance certificates.

## Goal 3 Phase 12: Perfect-Outer Embedding Robustness Audit

Phase 12 asks whether the Phase 11 same-distance repair is a fragile one-off or
part of a wider outer-embedding pattern. It keeps the Phase 2 graph/CWS inner
source and the literal `[[5,1,3]]` five-qubit perfect outer block, then scores a
170-spec bounded superset:

- the 44 Phase 11 variants;
- 2 additional global phase-free local Clifford maps;
- 10 additional one-site full local Clifford edits;
- 114 additional nontrivial outer-qubit permutations, which together with the
  identity and the Phase 11 simple permutations cover all of `S5`.

Every operation spec is checked as an exact stabilizer code after
concatenation. All 170 variants remain five-qubit-perfect outer blocks, and all
170 preserve labeled subsystem entropy matching through size two.

The exact bucket counts are:

```text
outer embedding variants scored:       170
Phase 11 seed variants embedded:        44
added variants:                        126
full S5 permutations covered:          120
same exact distance-3 variants:         30
same-distance Phase 11 variants:        20
same-distance added one-site LC:        10
pure-permutation same-distance hits:     0
```

The robust pattern is sharper than Phase 11. Same-distance repairs occur for
one-site outer local Clifford edits that change logical-axis semantics, plus
the Phase 11 two-site Hadamard witnesses. Pure outer-qubit relabelings do not
repair the distance asymmetry anywhere in the full `S5` permutation audit, and
global local-Clifford layers do not repair it either.

All 30 same-distance variants keep compact observer witnesses in the
inner-major atlas:

```text
same-distance compact scans:              30
inner-major intervals scanned:          6000
inner-major compact hits:                360
minimum compact hit length:                3
```

The selected simplest witness remains the Phase 11 `q0_H` variant. The selected
compact interval is `(4,9,14)`:

```text
entropy:          3 versus 3
min-cut:          5 versus 5
algebra:          (2,0,0,true) versus (0,0,2,false)
erasure profile:  false versus true
exact distances:  3 versus 3
```

The selected witness also replays the Phase 10 atlas profile exactly:
block-contiguous hits `0`, inner-major hits `12`, witness-strip hits `17`,
total compact interval hits `29`, and strict lifted hits `3`.

The interpretation is now more precise. The same-distance compact split is not
merely a qubit-labeling artifact: pure permutations fail. It is also not a
global block symmetry: global local-Clifford layers fail. The successful repair
depends on outer logical-embedding semantics, which is exactly the diagnostic
distinction this toy cosmology is meant to expose.

This is still bounded. Phase 12 covers all pure `S5` outer permutations and a
declared one-site/full-local-Clifford extension of Phase 11, but it does not
exhaust the full five-qubit local-Clifford orbit and does not yet build a
multi-perfect-tensor HaPPY tiling.

The Phase 12 recommendation is `adapt_then_proceed`: move from one perfect
outer block to a small two-perfect-tensor stabilizer tiling and replay the same
exact entropy, min-cut, region algebra, erasure, survivor, and distance gates.

## Goal 3 Phase 13: Two-Perfect-Tensor Tiling Audit

Phase 13 follows the Phase 12 recommendation by replacing the single perfect
outer block with a literal two-cell stabilizer tiling. The outer code is built
from two canonical `[[5,1,3]]` five-qubit perfect blocks joined by one encoded
bridge stabilizer, giving a `[[10,1,3]]` outer tiling code with erasure
threshold `2`. Concatenating this outer tiling with the Phase 2 graph/CWS inner
source gives an `n=50,k=1` code pair.

The audit scores a targeted 48-spec tiling menu:

```text
bridge identities:                         3
X-bridge one-site axis swaps:             20
Y-bridge one-site axis swaps:             20
Y-bridge paired-leg Hadamards:             5
```

All 48 variants remain `k=1,d=3` outer tiling codes and preserve labeled
subsystem entropy matching through size two after concatenation. The three
unrepaired bridge identities are distance-asymmetric in the concatenated pair.
The 45 targeted local-axis repairs are exact same-distance witnesses with
distance `3` versus `3`.

To keep the certificate exact but bounded, the compact scan uses one
representative from each same-distance repair family:

```text
representatives:                         X_q0_HS, Y_q0_H, Y_paired_leg0_H
inner-major intervals scanned:            1200
inner-major compact hits:                   60
minimum compact hit length:                  3
```

The selected simplest same-distance tiling is `Y_q0_H`. Its compact witness is
the interval `(4,9,14)`:

```text
entropy:          3 versus 3
min-cut:          5 versus 5
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
survivor fixed:   false versus true
exact distances:  3 versus 3
```

The selected two-cell atlas replay scans four boundary templates:

```text
candidate intervals scanned:             1600
entropy-gate passes:                     1352
entropy-gate rejections:                  248
block-contiguous compact hits:              0
inner-major compact hits:                  20
cell-major compact hits:                   22
witness-strip compact hits:                35
total compact interval hits:               77
min-cut internal assignments per check:     4
```

The interpretation is now stronger than the one-block Phase 10/12 story. The
compact reconstruction/erasure split survives in a genuine two-perfect-cell
outer tiling, and the same-distance repair is not supplied by the unrepaired
bridge identity. It depends on local logical-axis semantics at the outer tiling
legs.

The scope is still deliberately bounded. Phase 13 does not exhaust the full
two-cell local-Clifford orbit, all possible bridge capacities, or a hyperbolic
HaPPY network. It certifies a finite two-perfect-block stabilizer tiling, a
declared 48-spec repair menu, representative compact scans for the repair
families, and a full atlas replay for the selected witness.

The Phase 13 recommendation is `adapt_then_proceed`: vary bridge capacities and
connectivities, or move to a three-perfect-cell chain/ring, while keeping exact
entropy, min-cut, algebra, erasure, survivor, and distance certificates.

## Goal 3 Phase 14: Three-Perfect-Cell Chain/Ring Atlas Audit

Phase 14 follows the Phase 13 recommendation by moving from two perfect cells
to a three-cell outer stabilizer chain. The outer code is built from three
canonical `[[5,1,3]]` five-qubit perfect blocks joined by two nearest-neighbor
encoded bridge stabilizers, giving a `[[15,1,3]]` outer chain with erasure
threshold `2`. Concatenating this outer chain with the Phase 2 graph/CWS inner
source gives an `n=75,k=1` code pair.

The audit scores a bounded 9-spec three-cell menu:

```text
bridge identities:                         3
XX single-cell axis repairs:               3
YY single-cell axis repairs:               3
```

All 9 variants remain `k=1,d=3` outer chains and preserve labeled subsystem
entropy matching through size two after concatenation. The three unrepaired
bridge identities are distance-asymmetric under the weight-three audit. The six
single-cell axis repairs give exact same-distance witnesses with distance
`3` versus `3`. For the repaired variants, exact distance is certified by a
no-weight-one-or-two logical audit plus an explicit verified weight-three
logical witness.

The selected simplest same-distance chain is `YY_q0_H`. Its distance proof
object verifies weight-three logical witnesses on `(4,9,14)` and `(4,9,24)`.
The selected compact inner-major witness is again `(4,9,14)`:

```text
entropy:          3 versus 3
min-cut:          5 versus 5
algebra:          (1,1,1,false) versus (0,0,2,false)
erasure profile:  false versus true
survivor fixed:   false versus true
exact distances:  3 versus 3
```

Phase 14 then replays the selected code pair on two declared three-internal-node
min-cut skeletons: a chain and a ring. Each min-cut is exact over `8` internal
assignments. Both skeletons give the same compact-hit table:

```text
candidate intervals scanned per topology: 2400
entropy-gate passes per topology:         2031
entropy-gate rejections per topology:      369
block-contiguous compact hits:               0
inner-major compact hits:                   27
cell-major compact hits:                    33
witness-strip compact hits:                 53
total compact hits per topology:           113
```

Across chain and ring together:

```text
candidate intervals scanned:             4800
entropy-gate passes:                     4062
entropy-gate rejections:                  738
total compact interval hits:              226
inner-major compact hits:                  54
cell-major compact hits:                   66
witness-strip compact hits:               106
block-contiguous compact hits:              0
```

The interpretation is now sharper. The compact reconstruction/erasure split
survives a larger three-perfect-cell outer chain and is stable under the
declared chain-versus-ring min-cut replay for the selected witness. But the
block-contiguous atlas remains a zero-hit control, so source-aware boundary
semantics are still doing real work.

The scope remains bounded. Phase 14 certifies one finite three-cell stabilizer
chain, a 9-spec axis/leg repair menu, and two declared min-cut skeletons. It
does not exhaust all three-cell local-Clifford embeddings, all bridge-axis
patterns, all bridge capacities, or a full HaPPY tiling.

The Phase 14 recommendation is `adapt_then_proceed`: search a small branching
perfect-cell tree or bridge-capacity grammar, retaining exact entropy, min-cut,
algebra, erasure, survivor, and distance certificates.

## Goal 3 Phase 15: Capacity/Branching Fixed-Witness Grammar Audit

Phase 15 follows the Phase 14 recommendation, but keeps the check surgical
rather than launching another full interval search. It fixes the selected
Phase 14 same-distance tiling, `YY_q0_H`, and audits three certified compact
witness regions against a finite grammar of min-cut skeletons:

```text
chain skeletons:                5
ring skeletons:                 5
rooted-branch skeletons:        5
branch-plus-chain skeletons:    3
total skeletons:               18
fixed witness regions:          3
region/skeleton records:       54
```

The three fixed regions are:

```text
inner_major_local_short:       (4,9,14)
inner_major_cross_cell_short:  (14,19,24,29)
witness_strip_cross_cell:      (14,17,19,22,24,27)
```

Every record recomputes the exact min-cut on the declared skeleton and the
exact stabilizer entropy, region algebra, erasure, and survivor diagnostics.
The two cross-cell regions explicitly span perfect cells `0` and `1`.

The result is a bounded robustness/no-go:

```text
entropy-match records:                 54 / 54
operator/channel split records:         54 / 54
exact min-cut records:                  54 / 54
branching skeletons included:            8
internal assignments per min-cut:      8 or 16
min-cut invariant regions:               3
min-cut variable regions:                0
```

The invariant min-cut values are:

```text
inner_major_local_short:        5
inner_major_cross_cell_short:   6
witness_strip_cross_cell:       8
```

The interpretation is deliberately modest. For these certified compact
witnesses, reconstruction-visible and erasure-visible geometry remain split
across all tested chain, ring, rooted-branch, and branch-plus-chain skeletons.
The tested capacity grammar changes the declared internal graph, but not the
min-cut-visible geometry of the fixed witnesses.

The scope is also deliberately bounded. Phase 15 audits fixed witness regions,
not all boundary intervals. It does not prove that no larger interval has
capacity-sensitive min-cut behavior, and it does not exhaust all branching
tensor-network skeletons.

The Phase 15 recommendation is `adapt_then_proceed`: search directly for
capacity-sensitive compact witnesses using an early min-cut-variation filter,
then certify any hits with exact entropy, algebra, erasure, survivor, and
distance checks.

## Goal 3 Phase 16: Capacity-Sensitive Interval No-Go Audit

Phase 16 follows the Phase 15 recommendation with a bounded interval search
instead of fixed witnesses. It keeps the selected Phase 14 same-distance tiling,
`YY_q0_H`, and searches for compact intervals where three conditions line up:

```text
1. exact min-cut value varies across a probe skeleton grammar;
2. paired-code entropy still matches on the interval;
3. reconstruction, erasure, or survivor semantics still split.
```

The certified search grammar uses two source-aware boundary templates and
eight probe skeletons:

```text
templates:            three_perfect_inner_major, three_perfect_witness_strip
interval lengths:     9 through 45
probe skeletons:      8
filter order:         min-cut variation -> entropy match -> operator/channel split
```

The probe skeletons are low/high-capacity versions of chain, ring,
rooted-branch, and branch-plus-chain geometries:

```text
chain_1_1, chain_3_3
ring_1_1_1, ring_3_3_3
rooted_branch_1_1_1, rooted_branch_3_3_3
branch_plus_chain_2_2_1_1_1, branch_plus_chain_2_2_2_2_2
```

The exact funnel counts are:

```text
intervals scanned:                       5550
min-cut-variable intervals:              1888
entropy matches after variation:          196
operator/channel hits:                      0

inner-major min-cut-variable intervals:   450
inner-major entropy candidates:           196
witness-strip min-cut-variable intervals: 1438
witness-strip entropy candidates:           0
```

So Phase 16 is a bounded no-go. Min-cut-visible geometry does vary in this
grammar, and entropy-matched candidates exist, but none of the entropy-matched,
min-cut-variable candidates in the searched templates retain the
operator/erasure/survivor split.

The interpretation is useful. Phase 15 showed that certified compact witnesses
are robust but not capacity-sensitive. Phase 16 shows the converse obstruction
inside this bounded search: capacity-sensitive intervals exist, but they do not
carry the certified bridge witness semantics.

The scope is explicit. Phase 16 covers two source-aware templates and interval
lengths `9..45`. It excludes block-contiguous and cell-major templates from the
certified search window, and it is not a theorem over all boundary intervals or
all tensor-network skeletons.

The Phase 16 recommendation is `adapt_then_proceed`: change the code/atlas, not
only the min-cut skeleton. The next phase should build a branching outer
stabilizer code or four-cell tree where the logical witness is forced across a
genuine internal bottleneck, then replay exact entropy, min-cut, algebra,
erasure, survivor, and distance diagnostics.

## Goal 3 Phase 17: Four-Perfect-Cell Tree Fixed-Witness Audit

Phase 17 follows the Phase 16 recommendation by changing the substrate. It
builds four literal five-qubit perfect-code outer cells, joins them by encoded
`YY` bridge stabilizers on the tree edges `0-1`, `1-2`, and `1-3`, applies the
same one-leg `H` repair pattern used by the selected Phase 14 tiling, and
concatenates the result with the Phase 2 graph/CWS inner source.

The resulting pair is an exact finite tensor-network/QEC toy:

```text
outer code:        n=20, k=1
outer distance:    exact weight-3 logical witness found by bounded audit
concatenated pair: n=100, k=1
t<=2 entropy:      5051 subsets checked, 0 mismatches
```

The fixed-witness atlas intentionally touches all four perfect cells and
includes branch-spanning regions:

```text
fixed regions scored:             8
capacity profiles scored:         7
region/capacity records:         56
exact min-cut records:           56
operator/channel split records:  56
touched perfect cells:            4
branch-spanning regions:          3
```

The certified min-cut values are invariant across the tested tree-capacity
profiles:

```text
cell-local compact witnesses:      5
adjacent cross-cell witnesses:     6
branch 1-3 cross-cell witness:     8
cell-3 witness-strip region:       7
min-cut-variable regions:          0
```

So Phase 17 is a robustness lift plus another useful no-go. The
reconstruction-visible and erasure-visible bridge witness survives in a larger
four-cell branching tensor-network substrate, including a side-branch witness.
But the tested fixed witnesses are still min-cut-invariant across bridge
capacities. Branching by itself does not yet align capacity-sensitive
min-cut geometry with observer-patch semantics.

The scope is explicit. Phase 17 certifies one four-cell `YYY` tree with one
local `H` repair and eight fixed source-aware witness regions. It does not
exhaust four-cell local-Clifford variants, topology variants, reduced-boundary
min-cut skeletons, or long interval searches.

The Phase 17 recommendation is `adapt_then_proceed`: either run a narrower
long-interval/topology funnel on the `n=100` tree, or modify the declared
min-cut skeleton so the witness cannot be cut off only by boundary legs. The
next certificate should test whether branch bottlenecks can become
operator-visible without abandoning exact entropy, min-cut, algebra, erasure,
survivor, and distance checks.

## Goal 3 Phase 18: Four-Cell Tree Shell-Bottleneck Audit

Phase 18 tests the other half of the Phase 17 recommendation. Instead of
looking only at compact witnesses, it scores whole-cell and branch-shell
regions on the same `n=100,k=1` four-perfect-cell source. These regions are
large enough that tree bridge capacities can control the declared min-cut.

The audit uses two declared skeleton modes:

```text
tree_only:           cell legs plus internal tree bridges, no boundary ring
unit_boundary_ring:  Phase 17 boundary ring plus the same internal tree bridges
```

The exact finite audit is:

```text
shell regions scored:              8
capacity profiles scored:          7
boundary modes scored:             2
shell/capacity records:          112
exact min-cut records:           112
entropy-match records:           112
operator/channel split records:    0
capacity-sensitive mode/regions:  16 / 16
shell lengths:                    25 through 75
```

Representative min-cut vectors over the seven capacity profiles are:

```text
tree_only cell0_shell:                  1,2,3,1,3,1,3
tree_only cell1_root_shell:             3,6,9,7,5,5,7
tree_only root_plus_side_leaf_shell:    2,4,6,4,4,2,6
unit_boundary_ring cell0_shell:         3,4,5,3,5,3,5
unit_boundary_ring complement_root:     5,8,11,9,7,7,9
```

So Phase 18 gives the complementary decoupling to Phase 17. Branch bottlenecks
can become visible to min-cut geometry on shell regions, but those same regions
have matching entropy, matching algebra signatures, matching erasure behavior,
and matching survivor semantics across the paired codes. In short:
capacity-sensitive min-cut geometry appears, but it is operator-blind in this
bounded shell atlas.

The scope is deliberately finite. Phase 18 certifies eight large shell regions,
seven capacity profiles, and two skeleton modes on the Phase 17 source. It is
not an exhaustive interval search, and it does not prove that all
capacity-sensitive regions are operator-blind.

The Phase 18 recommendation is `adapt_then_proceed`: search hybrid regions that
combine the compact bridge-witness core with whole-cell shells, or alter the
code construction so compact bridge witnesses must cross an internal bottleneck.
The next certificate should keep the same filter discipline: min-cut variation
first, then exact entropy, algebra, erasure, survivor, and distance diagnostics.

## Goal 3 Phase 19: Compact-Core Plus Shell Hybrid No-Go Audit

Phase 19 follows the Phase 18 recommendation with a bounded hybrid-region
grammar on the same `n=100,k=1` four-perfect-cell tree. Each candidate is the
union of one Phase 17 compact witness core and one Phase 18 shell region. The
audit skips cases where the core is already contained in the shell, then applies
the same strict funnel:

```text
1. exact min-cut variation across seven tree bridge capacity profiles;
2. exact entropy match between the paired codes;
3. exact operator/reconstruction or erasure/survivor split.
```

The exact bounded funnel is:

```text
boundary modes scored:             2
compact cores scored:              8
shell regions scored:              8
core/shell pairs per mode:        64
contained skips:                  38
hybrid candidates:                90
min-cut-variable candidates:      90
entropy matches after variation:  12
entropy mismatches after variation: 78
operator/channel hits:             0
hybrid lengths:                   26 through 78
```

Both skeleton modes have the same funnel shape:

```text
tree_only:          45 candidates, 45 min-cut-variable, 6 entropy matches, 0 hits
unit_boundary_ring: 45 candidates, 45 min-cut-variable, 6 entropy matches, 0 hits
```

Representative entropy-matched hybrids are still operator-blind:

```text
tree_only adjacent_0_1 + cell0 shell:          2,3,4,2,4,2,4
tree_only branch_1_3 + root_plus_leaf2 shell:  3,5,7,5,5,5,5
unit-ring branch_1_3 + root_plus_leaf2 shell:  7,9,11,9,9,9,9
```

So Phase 19 is a sharper no-go for the most obvious repair strategy. Compact
cores carry the operator/erasure split, and shell regions carry capacity
sensitivity, but naively gluing them does not align the two diagnostics. In
this bounded grammar, capacity-sensitive hybrids either break entropy matching
or remain operator-blind.

The scope is finite: Phase 19 covers the eight Phase 17 fixed compact cores,
the eight Phase 18 shell regions, two skeleton modes, and seven capacity
profiles. It does not exhaust arbitrary hybrid intervals or modify the code
construction itself.

The Phase 19 recommendation is `adapt_then_proceed`: change the code or bridge
construction next. The next phase should search small outer-tree bridge-axis or
local-Clifford variants, or add a dedicated internal witness bridge whose
logical support cannot be absorbed by whole-cell shells.

## Goal 3 Phase 20: Four-Cell Outer-Tree Local-Variant No-Go Audit

Phase 20 changes the code construction within a bounded local menu. It first
audits bridge-axis validity for the four-cell tree: all `27` `X/Y/Z` bridge-axis
triples are tried at the outer-code level. Only the uniform-axis patterns
commute on the shared-root tree:

```text
valid bridge axes:       XXX, YYY, ZZZ
rejected mixed axes:      24
reason:                  noncommuting shared-root logical bridge checks
```

It then crosses the three valid bridge-axis choices with thirteen representative
local repair specs: identity, single-leg `H`, single-leg `LC4`, and selected
paired-`H` repairs on the four representative tree legs. Each variant is
concatenated with the Phase 2 inner source and scored on the Phase 19
entropy-survivor sentinel probes.

The exact bounded variant funnel is:

```text
valid variants scored:             39
outer distance-three witnesses:    39
code pairs:                        n=100,k=1 for all variants
probe pairs per variant:            6
boundary modes per variant:         2
variant/probe records:            468
exact min-cut probe records:      468
min-cut-variable probe records:   468
entropy-match probe records:      468
operator/channel hits:              0
```

Each uniform bridge-axis family contributes thirteen variants and zero hits:

```text
XXX variants: 13, hits: 0
YYY variants: 13, hits: 0
ZZZ variants: 13, hits: 0
```

So Phase 20 stabilizes the Phase 19 no-go under a small outer-tree
bridge-axis/local-Clifford variant menu. Changing between uniform `X`, `Y`, and
`Z` bridge axes, and adding representative local repairs, does not make the
capacity-sensitive hybrid probes operator-visible. The obstruction is no longer
just a bad local basis choice in the tested menu.

The scope is finite. Phase 20 is not a full local-Clifford orbit, and it does
not add a new internal witness bridge stabilizer. It certifies this bounded
variant menu and the Phase 19 sentinel probes.

The Phase 20 recommendation is `adapt_then_proceed`: stop only changing local
bases. The next phase should add a genuinely new internal witness bridge or
move to a different branching stabilizer block/topology, then rerun the exact
min-cut variation -> entropy -> operator/erasure funnel.

## Goal 3 Phase 21: Four-Cell Outer-Tree Topology No-Go Audit

Phase 21 changes the outer-tree topology itself. It enumerates all sixteen
labeled trees on four perfect-code cells, builds a `YYY` bridge outer code with
the Phase 17 `q0_H` repair on each topology, and scores the Phase 20 sentinel
hybrid probes on topology-matched min-cut skeletons.

The exact bounded topology funnel is:

```text
labeled tree topologies:          16
outer distance-three topologies:  16
code pairs:                       n=100,k=1 for all topologies
probe pairs per topology:          6
boundary modes per topology:       2
topology/probe records:          192
exact min-cut probe records:     192
min-cut-variable probe records:  192
entropy-match probe records:     192
operator/channel hits:             0
```

This includes both star-like and path-like labeled trees, with the first and
last canonical entries:

```text
tree_01_02_03
tree_03_13_23
```

So Phase 21 extends the Phase 20 no-go from local basis/axis changes to the
full labeled four-cell tree-topology menu, at fixed `YYY` bridge axis and
`q0_H` repair. Matching the declared min-cut skeleton to a different tree
connectivity still does not make the capacity-sensitive sentinel probes
operator-visible.

The scope is finite. Phase 21 fixes the bridge axis and repair, and it reuses
the Phase 20 sentinel probes. It does not search a full local-Clifford orbit on
each topology, and it does not add a new internal witness bridge stabilizer.

The Phase 21 recommendation is `adapt_then_proceed`: topology changes alone are
not enough. The next step should change the logical construction more
substantially, such as adding an explicit internal witness bridge or moving to a
larger/different stabilizer block, then rerunning the exact min-cut, entropy,
algebra, erasure, survivor, and distance diagnostics.

## Goal 3 Phase 22: Five-Cell Branching Internal-Witness Audit

Phase 22 follows the Phase 21 recommendation by changing the code construction
rather than only the declared topology. It builds five literal five-qubit
perfect-code outer cells, joins them by encoded `Y` bridge stabilizers on the
binary-tree edges `0-1`, `1-2`, `1-3`, and `3-4`, and concatenates this outer
code with the Phase 2 graph/CWS inner source.

The resulting exact tensor-network/QEC toy has:

```text
outer code:                 n=25,k=1
outer distance witness:      3
concatenated pair:          n=125,k=1
t<=2 entropy checks:      7876
t<=2 entropy mismatches:     0
tree capacity profiles:      9
min-cut internal choices:   32 per profile
```

The audit separates three region families:

```text
compact source-aware witnesses:        9
compact operator/channel splits:       9
compact min-cut-variable records:      0

whole-cell shell regions:              5
shell min-cut-variable records:        5
shell operator/channel splits:         0

compact-core plus shell candidates:  225
entropy-matched core-shell candidates: 99
capacity-variable survivors:          99
operator/channel survivor hits:        0
```

So the five-cell construction strengthens the negative lesson. The compact
source-aware witnesses still carry the reconstruction/erasure separation, but
their tree-only min-cut values are invariant across the tested bridge-capacity
profiles. Whole-cell shells expose the internal bottlenecks, but their operator
and channel semantics match. Adding one-, two-, or three-cell shells to compact
cores makes many regions entropy-matched and capacity-sensitive, but all `99`
survivors lose the operator/channel split.

This is not a universal no-go. It fixes one five-cell `Y`-bridge binary tree,
tree-only min-cut skeletons, nine bridge-capacity profiles, compact cores, and
shell subsets of size one to three. It does not exhaust five-cell local-Clifford
variants, tree topologies, or arbitrary boundary regions.

The Phase 22 recommendation is `adapt_then_proceed`: introduce an explicit
gauge/interface cell or a two-layer Clifford/MERA-like outer code where a
compact logical witness is forced through an internal bottleneck by
construction, then rerun exact entropy, min-cut, algebra, erasure, survivor, and
distance diagnostics.

## Goal 3 Phase 23: Interface-Cell Star Audit

Phase 23 follows the Phase 22 recommendation by adding an explicit interface
cell. It builds six literal five-qubit perfect-code outer cells, uses cell `5`
as a root/interface, joins it to leaf cells `0..4` by encoded `Y` bridge
stabilizers, and concatenates this interface-star outer code with the Phase 2
graph/CWS inner source.

The resulting exact tensor-network/QEC toy has:

```text
outer code:                 n=30,k=1
outer distance witness:      3
concatenated pair:          n=150,k=1
t<=2 entropy checks:     11326
t<=2 entropy mismatches:     0
tree capacity profiles:     10
min-cut internal choices:   64 per profile
```

The named audit separates compact source-aware witnesses from interface-shell
probes:

```text
compact regions:                         11
compact operator/channel splits:         11
compact min-cut-variable records:         0

interface-shell regions:                 10
root-shell-plus-edge regions:             5
root-plus-leaf shell regions:             5
interface min-cut-variable records:      10
interface operator/channel splits:        0
```

The root-shell-plus-edge probes are smaller and more interface-local than the
Phase 22 whole-cell shell unions. For example, `root_shell_plus_edge_0` has
length `26`, matching entropy `(2,2)`, and exact min-cut values
`(6,8,10,11,14,16)` across the ten capacity profiles. Its algebra signatures
match, however: `(1,1,1,false)` versus `(1,1,1,false)`. The compact witness
`cell0_local_compact` still has matching entropy `(3,3)` and an operator/channel
split, but its min-cut value is invariant at `3`.

So the interface cell improves the holographic-looking substrate but preserves
the separation of roles: compact regions see reconstruction/erasure semantics,
while root/interface shell regions see the bottleneck capacities. The tested
named regions still do not make the same boundary region both capacity-sensitive
and operator/channel-visible.

The scope is finite. Phase 23 fixes one six-cell `Y`-bridge interface star,
tree-only min-cut skeletons, ten bridge-capacity profiles, eleven compact
witnesses, and ten named interface-shell probes. It does not exhaust punctured
interface shells, local-Clifford variants, or two-layer Clifford/MERA encoders.

The Phase 23 recommendation is `adapt_then_proceed`: either run a narrow
punctured-interface-shell frontier, or build a genuine two-layer Clifford/MERA-
like outer encoder that mixes compact witness support across layers before
concatenation.

## Goal 3 Phase 24: Punctured Interface-Shell Frontier

Phase 24 follows the first Phase 23 recommendation. It reuses the six-cell
interface-star outer code and scans a narrow punctured-shell frontier: start
from each `root_shell_plus_edge_i` probe, then remove one root/interface
witness-line qubit from offsets `4,9,14,19,24`.

The exact frontier is:

```text
root witness-line holes:          5
leaf cells scored:                5
punctured records:               25
capacity profiles:               10
entropy-match records:           25
min-cut-variable records:        25
operator/channel hits:            0
min-cut internal choices:        64 per profile
```

A representative puncture, `root_shell_plus_edge_0_minus_q129`, has length `25`,
matching entropy `(3,3)`, and exact min-cut values
`(7,12,17,15,9,9,9,9,11,11)` across the ten capacity profiles. Its algebra
signatures still match: `(1,1,1,false)` versus `(1,1,1,false)`.

So one-qubit punctures sharpen but do not repair the Phase 23 mismatch. They
raise the region entropy to the compact-witness scale and keep the internal
bottleneck visible, but the operator/channel semantics remain shell-like rather
than compact-witness-like.

The scope is finite. Phase 24 fixes the Phase 23 `Y`-bridge interface star and
checks only one-qubit root witness-line punctures. It does not exhaust arbitrary
holes, two-hole punctures, local-Clifford variants, or two-layer Clifford/MERA
encoders.

The Phase 24 recommendation is `adapt_then_proceed`: move away from shell
surgery and build a genuine two-layer Clifford/MERA-like outer encoder that
mixes interface and leaf supports before concatenation.

## Goal 3 Phase 25: Two-Layer Clifford Frontier

Phase 25 follows the second Phase 24 recommendation. It fixes the Phase 23
interface-star network and the 25 Phase 24 punctured interface-shell regions,
then applies four bounded two-layer CX menus to the outer code before
concatenation:

```text
root_to_leaf_same_position
leaf_to_root_same_position
alternating_disentangler_isometry
sparse_offset_ladder
```

The exact frontier is:

```text
two-layer variants:                         4
punctured records per variant:             25
total punctured records:                  100
capacity profiles:                         10
entropy-match records:                     20
min-cut-variable records:                 100
operator/channel split records:            30
admissible entropy-matched operator hits:   0
entropy-mismatched operator near-hits:      30
distance-3 witness variants:                2
distance-lower-bound-4 variants:            2
min-cut internal choices:                  64 per profile
```

The `leaf_to_root_same_position` circuit creates 25 operator/channel-visible
near-hits, but all are rejected by the entropy gate. The `alternating_
disentangler_isometry` circuit preserves entropy equality for 20 punctures and
creates 5 operator/channel-visible near-hits, again only on entropy-mismatched
records. The other two menus produce no operator/channel split on this frontier.

So the obstruction moved but did not disappear: bounded two-layer Clifford
mixing can make the punctured shell operator-visible, but in this menu it does
so only by breaking the paired entropy equality. The certified admissible set
remains empty under the exact filter:

```text
entropy match + capacity-sensitive min-cut + operator/channel split
```

The scope is finite. Phase 25 checks four hand-built CX menus and the 25
Phase 24 punctured regions. It does not enumerate all Clifford circuits, all
MERA layouts, two-hole punctures, arbitrary boundary regions, or alternate
inner sources.

The Phase 25 recommendation is `adapt_then_proceed`: run a local
gate-neighborhood search around the alternating and leaf-to-root near-hits, or
change the inner source/outer block pairing so mixed support can regain entropy
equality.

Human memo: [docs/goal3_phase25_two_page_human_memo.md](docs/goal3_phase25_two_page_human_memo.md)

## Goal 3 Phase 26: Offset-Flip Entropy-Gated Neighborhood

Phase 26 follows the first Phase 25 recommendation with a bounded local
neighborhood around the two near-hit parent circuits:

```text
leaf_to_root_same_position
alternating_disentangler_isometry
```

For each parent and each outer offset `0..4`, it flips the direction of all
five same-position root/leaf `CX` gates at that offset. This gives ten
neighbor circuits. The default certificate uses a strict entropy-first filter:
every candidate record gets exact entropy and exact min-cut checks, but
operator algebra, erasure, and survivor fixed-point checks are run only for
records that pass the entropy gate.

The exact default frontier is:

```text
offset-flip variants:                    10
punctured records per variant:           25
total candidate records:                250
capacity profiles:                       10
entropy-match records:                   90
entropy-mismatch records:               160
operator/channel checked records:        90
entropy-gate rejections:                160
min-cut-variable records:               250
operator/channel splits among checked:    0
admissible entropy-matched hits:          0
distance-3 witness variants:             10
min-cut internal choices:                64 per profile
```

The `leaf_to_root_same_position` neighborhood contributes 50 entropy-matched
records across five variants, and the `alternating_disentangler_isometry`
neighborhood contributes 40. None of those 90 entropy-matched records has a
different reconstruction, erasure, or survivor fixed-point diagnostic.

So the local offset-flip neighborhood makes the Phase 25 no-go sharper:
direction flips can repair pieces of the entropy frontier, but the repaired
records lose the operator/channel distinction. The strict triple intersection
again remains empty:

```text
entropy match + capacity-sensitive min-cut + operator/channel split
```

The scope is finite. Phase 26 checks ten global offset-flip circuits and the
same 25 Phase 24 punctured regions. By default it does not audit
operator/channel near-hits in entropy-rejected records; run
`python3 -m qgtoy holography-phase26 --audit-entropy-mismatch-near-hits` for
that heavier diagnostic.

The Phase 26 recommendation is `adapt_then_proceed`: change the region grammar
instead of only flipping global offset directions. A bounded two-hole or
leaf-private-region grammar around the Phase 26 entropy-passing records is the
next natural exact search.

## Goal 3 Phase 27: Second-Root-Hole Region Grammar

Phase 27 follows the Phase 26 recommendation by changing the region grammar
while reusing the ten Phase 26 offset-flip circuits. For every Phase 26 base
puncture that passes the entropy gate, it removes one additional root
witness-line qubit from the four remaining root-hole positions.

The exact frontier is:

```text
offset-flip variants:                    10
base punctured regions:                  25
base entropy-pass records:               90
candidate second-hole records:          360
capacity profiles:                       10
entropy-match records:                   60
entropy-mismatch records:               300
operator/channel checked records:        60
second-hole entropy rejections:         300
min-cut-variable records:               360
operator/channel splits among checked:    0
admissible entropy-matched hits:          0
distance-3 witness variants:             10
min-cut internal choices:                64 per profile
```

The second-hole grammar is asymmetric across the Phase 26 parents. The
`leaf_to_root_same_position` neighborhood contributes 200 second-hole records,
but all 200 fail the second-hole entropy gate. The
`alternating_disentangler_isometry` neighborhood contributes 160 second-hole
records; 60 remain entropy-matched and receive exact algebra, erasure, and
survivor checks. None of those 60 has an operator/channel split.

A representative surviving second-hole record is
`root_shell_plus_edge_0_minus_q129__second_root_hole_q134`: entropy `(4,4)`,
min-cut values `(8,10,12,13,16,18)`, and matching algebra signatures
`(1,1,1,false)` versus `(1,1,1,false)`.

So the root-side two-hole region grammar keeps every candidate
capacity-sensitive, but it still does not align entropy/min-cut-visible
geometry with reconstruction/channel-visible geometry.

The scope is finite. Phase 27 exhausts only the second-root-hole grammar around
Phase 26 entropy-passing records. It does not cover leaf-private additions,
arbitrary two-hole punctures, changed inner sources, or broader Clifford/MERA
circuits.

The Phase 27 recommendation is `adapt_then_proceed`: audit a carefully bounded
leaf-private add grammar, likely with a smaller sentinel set or cached
certificate path, or change the inner/outer source pairing.

## Goal 3 Phase 28: Leaf-Private Sentinel Region Grammar

Phase 28 follows the Phase 27 recommendation with a bounded sentinel audit. It
reuses the two entropy-rich alternating offset-flip branches:

```text
alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root
alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root
```

For each entropy-passing base puncture in those two branches, it adds one
leaf-private qubit at local leaf offsets `0..3`. This probes whether
leaf-private boundary growth can preserve entropy/min-cut agreement while
revealing an observer-algebra or channel-semantic split.

The exact frontier is:

```text
sentinel variants:                         2
base punctured regions:                   25
base entropy-pass records:                30
candidate leaf-private records:          120
capacity profiles:                        10
entropy-match records:                   120
entropy-mismatch records:                  0
operator/channel checked records:        120
leaf-private entropy rejections:           0
min-cut-variable records:                120
operator/channel splits among checked:     0
admissible entropy-matched hits:           0
distance-3 witness variants:               2
min-cut internal choices:                 64 per profile
```

Unlike the second-root-hole grammar, every leaf-private sentinel candidate
passes the entropy gate. All 120 records are capacity-sensitive under the
min-cut profiles and receive exact algebra, erasure, and survivor fixed-point
checks. None has a different operator/channel-visible diagnostic, so the
strict intersection remains empty:

```text
entropy match + capacity-sensitive min-cut + operator/channel split
```

A representative surviving record is
`root_shell_plus_edge_0_minus_q129__add_leaf_private_q0`: entropy `(5,5)`,
min-cut values `(8,10,12,13,16,18)`, matching algebra signatures
`(1,1,1,false)` versus `(1,1,1,false)`, and matching non-correctable erasure
semantics.

The scope is finite and sentinel-only. Phase 28 covers two alternating
offset-flip branches and local leaf-private offsets `0..3`; it does not cover a
full leaf-private grammar, all Phase 26 variants, arbitrary leaf additions, or
new source pairings.

The Phase 28 recommendation is `adapt_then_proceed`: either change the
inner/outer source pairing or add a cached full leaf-private grammar audit, then
test whether the obstruction is source-specific or region-grammar-wide.

## Goal 3 Phase 29: Full Leaf-Private Region Grammar

Phase 29 removes the sentinel-only caveat from Phase 28. It reuses every Phase
26 offset-flip neighbor, keeps the same exact entropy gate on the 25 base
punctured regions, and then adds one leaf-private qubit at local leaf offsets
`0..3` to every entropy-passing base puncture.

The exact frontier is:

```text
offset-flip variants:                    10
parent circuits:                          2
base punctured regions:                  25
base entropy-pass records:               90
candidate leaf-private records:         360
capacity profiles:                       10
entropy-match records:                  360
entropy-mismatch records:                 0
operator/channel checked records:       360
leaf-private entropy rejections:          0
min-cut-variable records:               360
operator/channel splits among checked:    0
admissible entropy-matched hits:          0
distance-3 witness variants:             10
min-cut internal choices:                64 per profile
```

Parent-level aggregation keeps the no-go visible:

```text
leaf_to_root_same_position:        5 variants, 50 base passes, 200 leaf records
alternating_disentangler_isometry: 5 variants, 40 base passes, 160 leaf records
```

Every generated leaf-private record matches entropy, remains capacity-sensitive
under the min-cut profiles, and receives exact algebra, erasure, and survivor
fixed-point checks. None has a different operator/channel-visible diagnostic,
so the strict intersection is still empty:

```text
entropy match + capacity-sensitive min-cut + operator/channel split
```

A representative first matched record is
`root_shell_plus_edge_0_minus_q134__add_leaf_private_q0`: entropy `(6,6)`,
min-cut values `(8,10,12,13,16,18)`, and matching algebra signatures
`(0,0,2,false)` versus `(0,0,2,false)`.

The scope is finite. Phase 29 exhausts local leaf-private offsets `0..3` around
Phase 26 entropy-passing records across the offset-flip neighborhood. It does
not cover arbitrary leaf additions, changed bridge axes, changed inner sources,
all Clifford/MERA circuits, or non-local region grammars.

The Phase 29 recommendation is `adapt_then_proceed`: run an outer
bridge-axis/source-pairing audit over the same exact entropy, min-cut, algebra,
erasure, and survivor checks.

## Goal 3 Phase 30: Bridge-Axis Source-Pairing Audit

Phase 30 follows the Phase 29 recommendation by changing the interface-star
outer bridge axis instead of expanding the local region grammar. It uses the
same fixed Phase 2 graph/CWS source pair and the same `logical_concatenate_k1`
logical `Z/X` mapping, then replays the Phase 26 offset-flip punctured frontier
for bridge axes `X`, `Y`, and `Z`.

The exact frontier is:

```text
bridge axes:                              3
source pairings:                          1
offset-flip variants per axis:           10
axis variant records:                    30
base punctured regions:                  25
candidate punctured records:            750
capacity profiles:                       10
entropy-match records:                  165
entropy-mismatch records:               585
operator/channel checked records:       165
entropy-gate rejections:                585
min-cut-variable records:               750
operator/channel splits among checked:    0
admissible entropy-matched hits:          0
distance-3 witness axis variants:        30
min-cut internal choices:                64 per profile
```

Axis choice changes the entropy gate profile:

```text
X bridge axis: 30 entropy matches
Y bridge axis: 90 entropy matches
Z bridge axis: 45 entropy matches
```

The `Y` axis remains the most entropy-friendly Phase 26 pairing, while `X` and
`Z` shift entropy support mostly into alternating branches. Every punctured
record remains capacity-sensitive under the min-cut profiles. Every
entropy-matched record receives exact algebra, erasure, and survivor fixed-point
checks. None has a different operator/channel-visible diagnostic, so the strict
intersection remains empty:

```text
entropy match + capacity-sensitive min-cut + operator/channel split
```

Representative first matched records:

```text
X: root_shell_plus_edge_0_minus_q129, entropy (5,5), algebra (1,1,1,false)
Y: root_shell_plus_edge_0_minus_q134, entropy (5,5), algebra (0,0,2,false)
Z: root_shell_plus_edge_0_minus_q129, entropy (5,5), algebra (1,1,1,false)
```

The scope is finite and entropy-gated. Phase 30 covers one fixed Phase 2 source
pair, the fixed `logical_concatenate_k1` logical-basis mapping, bridge axes
`X/Y/Z`, the Phase 26 offset-flip circuits, and the 25 Phase 24 punctured
regions. It does not audit entropy-mismatched operator near-hits, full
leaf-private grammars for `X/Z`, arbitrary source pairs, logical-basis twists,
or non-local region grammars.

The Phase 30 recommendation is `adapt_then_proceed`: audit logical-basis twists
or alternative Phase 2 graph/CWS source pairs under the same exact entropy,
min-cut, algebra, erasure, and survivor checks. Entropy-mismatch near-hit
auditing would also be useful as a guide for that source-pair search.

## Goal 3 Phase 31: Shared Logical-Basis Twist Audit

Phase 31 follows the Phase 30 recommendation by twisting the inner logical basis
used by concatenation. For a `k=1` stabilizer code, the nonzero logical labels
are `Z`, `X`, and `Y=Z+X`; any ordered distinct pair is a valid symplectic
logical `Z/X` basis. Phase 31 audits all six shared twists, using the same
ordered pair for both members of the Phase 2 source pair, with bridge axis `Y`.

The exact frontier is:

```text
shared logical-basis twists:              6
bridge axes:                              1
source pairings:                          1
offset-flip variants per twist:          10
twist variant records:                   60
base punctured regions:                  25
candidate punctured records:           1500
capacity profiles:                       10
entropy-match records:                  290
entropy-mismatch records:              1210
operator/channel checked records:       290
entropy-gate rejections:               1210
min-cut-variable records:              1500
operator/channel splits among checked:    0
admissible entropy-matched hits:          0
distance-3 witness twist variants:       60
min-cut internal choices:                64 per profile
```

The shared-twist entropy profile is:

```text
Z as Z, X as X: 90 entropy matches
Z as Z, Y as X: 90 entropy matches
X as Z, Z as X: 55 entropy matches
X as Z, Y as X:  0 entropy matches
Y as Z, Z as X: 55 entropy matches
Y as Z, X as X:  0 entropy matches
```

Thus logical-basis pairing is visible to the entropy/min-cut frontier: two
twists keep the Phase 26 entropy profile, two narrow it, and two collapse the
entropy gate entirely. Every punctured record remains capacity-sensitive under
the min-cut profiles. Every entropy-matched record receives exact algebra,
erasure, and survivor fixed-point checks. None has a different
operator/channel-visible diagnostic, so the strict intersection remains empty:

```text
entropy match + capacity-sensitive min-cut + operator/channel split
```

Representative first matched records:

```text
Z_as_Z__X_as_X: root_shell_plus_edge_0_minus_q134, entropy (5,5), algebra (0,0,2,false)
X_as_Z__Z_as_X: root_shell_plus_edge_0_minus_q129, entropy (5,5), algebra (0,0,2,false)
```

The scope is finite and entropy-gated. Phase 31 covers shared logical-basis
twists only, fixes bridge axis `Y`, uses the Phase 26 offset-flip circuits, and
scores the 25 Phase 24 punctured regions. It does not cover independent
first/second twists, alternative graph/CWS source pairs, entropy-mismatched
near-hit auditing, full leaf-private grammars for every twist, or non-local
region grammars.

The Phase 31 recommendation is `adapt_then_proceed`: break the shared-twist
symmetry by auditing independent first/second logical-basis twists, or switch to
a bounded set of alternative Phase 2 graph/CWS source pairs. Entropy-mismatch
near-hit auditing should be used to prioritize expensive semantic checks.

## Goal 3 Phase 32: Independent Logical-Basis Twist Atlas

Phase 32 breaks the shared-twist symmetry from Phase 31. It audits all
independent first/second logical-basis twist pairs on the fixed `Y` bridge axis:
six choices for the first Phase 2 source code times six choices for the second.

This phase is deliberately two-layered. It exhausts exact entropy and exact
min-cut summaries for all independent pairs, then runs exact algebra, erasure,
and survivor fixed-point checks on four priority representatives:

```text
shared_high:    first Z_as_Z__X_as_X, second Z_as_Z__X_as_X
offdiag_high:   first X_as_Z__Y_as_X, second Z_as_Z__X_as_X
shared_medium:  first X_as_Z__Z_as_X, second X_as_Z__Z_as_X
offdiag_medium: first Z_as_Z__X_as_X, second X_as_Z__Z_as_X
```

The exact atlas frontier is:

```text
independent twist pairs:                 36
first twists:                             6
second twists:                            6
bridge axes:                              1
source pairings:                          1
offset-flip variants per pair:           10
independent pair variant records:       360
base punctured regions:                  25
candidate punctured records:           9000
capacity profiles:                       10
entropy-match records:                 1740
entropy-mismatch records:              7260
min-cut-variable records:              9000
distance-3 witness outer variants:       10
min-cut internal choices:                64 per profile
```

The independent-pair entropy profile has a simple distribution:

```text
12 pairs with 90 entropy matches
12 pairs with 55 entropy matches
12 pairs with  0 entropy matches
```

In this frontier, the entropy-match count is controlled by the second-code
twist. Varying the first-code twist independently does not change the
entropy-profile class.

The priority semantic audit is:

```text
priority semantic pairs:                  4
priority candidate punctured records:  1000
priority entropy-match records:         290
priority entropy-mismatch records:      710
operator/channel checked records:       290
operator/channel splits among checked:    0
admissible entropy-matched hits:          0
deferred entropy-matched records:      1450
```

All priority entropy-matched records remain capacity-sensitive and receive
exact algebra, erasure, and survivor checks. None has an
operator/channel-visible split. The result strengthens the no-go evidence for
representative independent-twist pairings, but it is not a full semantic no-go
over all 36 independent pairs because 1450 entropy-matched records are
explicitly deferred.

The Phase 32 recommendation is `adapt_then_proceed`: either complete the cached
semantic audit for the deferred 1450 entropy-matched independent-twist records,
or pivot to alternative Phase 2 graph/CWS source pairs using entropy-mismatch
near-hit auditing to prioritize expensive checks.

## Goal 3 Phase 33: Full Independent Logical-Basis Twist Audit

Phase 33 completes the semantic audit deferred by Phase 32. It keeps the same
fixed Phase 2 source pair, bridge axis `Y`, six-by-six independent logical-basis
twist grid, Phase 26 offset-flip circuits, and 25 Phase 24 punctured regions.
Unlike Phase 32, it runs exact algebra, erasure, and survivor fixed-point checks
on every entropy-matched independent-twist record.

The exact frontier is:

```text
independent twist pairs:                 36
first twists:                             6
second twists:                            6
bridge axes:                              1
source pairings:                          1
offset-flip variants per pair:           10
independent pair variant records:       360
base punctured regions:                  25
candidate punctured records:           9000
capacity profiles:                       10
entropy-match records:                 1740
entropy-mismatch records:              7260
operator/channel checked records:      1740
entropy-gate rejections:               7260
deferred entropy-matched records:         0
min-cut-variable records:              9000
operator/channel splits among checked:    0
admissible entropy-matched hits:          0
distance-3 witness twist variants:      360
min-cut internal choices:                64 per profile
```

The entropy-profile distribution remains the Phase 32 atlas result:

```text
12 pairs with 90 entropy matches
12 pairs with 55 entropy matches
12 pairs with  0 entropy matches
```

Every entropy-matched record in the independent-twist atlas now has exact
operator/channel diagnostics. None has an operator/channel-visible split, so the
strict intersection remains empty across this bounded frontier:

```text
entropy match + capacity-sensitive min-cut + operator/channel split
```

Representative first matched records:

```text
first_Z_as_Z__X_as_X__second_Z_as_Z__X_as_X: root_shell_plus_edge_0_minus_q134
first_X_as_Z__Y_as_X__second_Z_as_Z__X_as_X: root_shell_plus_edge_0_minus_q134
first_X_as_Z__Z_as_X__second_X_as_Z__Z_as_X: root_shell_plus_edge_0_minus_q129
```

The scope is finite. Phase 33 is exhaustive for independent logical-basis twists
on the fixed Phase 2 source pair, bridge axis `Y`, the Phase 26 offset-flip
circuits, and the 25 Phase 24 punctured regions. It does not cover alternative
graph/CWS source pairs, entropy-mismatched near-hit auditing, full leaf-private
grammars for every twist, changed bridge axes, or non-local region grammars.

The Phase 33 recommendation is `adapt_then_proceed`: change the underlying
Phase 2 graph/CWS source pair or expand beyond local punctured-shell grammars.
The most targeted next step is a bounded alternative-source search guided by
entropy-mismatch near-hit auditing.

## Goal 3 Phase 34: Bounded Alternative Source-Pair Scout

Phase 34 moves the search lever from logical-basis twists to the underlying
Phase 2 graph/CWS source pair. It enumerates the bounded `n=5,k=1` graph/CWS
subspace atlas under permutation equivalence, groups codes by labeled `t<=2`
entropy, and keeps every source pair in a bucket whose reconstruction profile
differs.

The exact bounded source atlas is:

```text
raw graph/CWS codes:                    33
relaxed codes checked:                  33
labeled entropy classes:                28
reconstruction-discordant source pairs:  4
source-pair ordinals:                   (16,23), (21,26), (21,27), (26,27)
Phase 2 primary pairs:                   1
non-primary alternatives:                3
```

Each source pair is replayed through the Phase 26 Y-bridge offset-flip frontier:

```text
source pairs:                            4
offset-flip variants per source pair:   10
variant records:                        40
punctured regions per variant:          25
candidate entropy/min-cut records:    1000
capacity profiles:                      10
entropy-match records:                 520
entropy-mismatch records:              480
min-cut-variable records:             1000
exact min-cut internal choices:         64 per profile
```

The source-pair entropy profile is the new signal:

```text
graph_cws_labeled_source_ord16_ord23:  90 / 250
graph_cws_labeled_source_ord21_ord26: 250 / 250
graph_cws_labeled_source_ord21_ord27:  90 / 250
graph_cws_labeled_source_ord26_ord27:  90 / 250
```

Thus the non-primary source pair `(21,26)` removes all entropy rejections in the
Phase 26 frontier while keeping the same outer geometry and min-cut cache.

Phase 34 is intentionally a scout rather than a full semantic no-go. It runs
exact algebra, erasure, and survivor checks on the first entropy-matched record
and, when present, the first entropy-mismatched record for each Phase 26 parent
circuit and source pair:

```text
priority semantic checks:               14
priority entropy-match checks:           8
priority entropy-mismatch checks:        6
deferred entropy-match checks:         512
deferred entropy-mismatch near-hit checks: 474
operator/channel splits checked:         3
admissible entropy-matched hits:         0
priority entropy-mismatch near-hits:     3
```

The priority entropy-matched checks have no operator/channel split. Three
priority entropy-mismatched probes still show operator/channel-visible
near-hits, so the next expensive audit has a precise queue.

The Phase 34 recommendation is `adapt_then_proceed`: run a full cached semantic
audit for source pair `(21,26)` across all 250 Phase 26 punctured records, then
separately audit the queued entropy-mismatched near-hits.

## Goal 3 Phase 35: Full Alternative Source-Pair Semantic Audit

Phase 35 spends the expensive semantic budget on the strongest Phase 34 source
signal: graph/CWS source-pair ordinals `(21,26)`. This pair was the only bounded
alternative source pair that preserved entropy on every Phase 26 punctured
record, so Phase 35 runs exact algebra, erasure, and survivor checks on all of
its records rather than sampling priority representatives.

The exact full audit is:

```text
selected source pair:                 (21,26)
raw graph/CWS codes:                       33
relaxed codes checked:                     33
bridge axis:                                Y
offset-flip variants:                      10
parent circuits:                            2
punctured regions per variant:             25
candidate records:                        250
capacity profiles:                         10
entropy-match records:                    250
entropy-mismatch records:                   0
operator/channel checked records:         250
deferred entropy-match checks:              0
min-cut-variable records:                 250
operator/channel splits checked:            0
admissible entropy-matched hits:            0
entropy-mismatch near-hits:                 0
distance-3 witness source variants:        10
exact min-cut internal choices:            64 per profile
```

Thus `(21,26)` repairs the entropy/min-cut frontier but does not produce a
reconstruction-visible or channel-visible separation on the Phase 26 punctured
region grammar. The strongest source-pair candidate is therefore a finite
semantic no-go for this exact outer geometry and region family.

The Phase 35 recommendation is `adapt_then_proceed`: audit the Phase 34
entropy-mismatched operator/channel near-hit surface from the other alternative
source pairs, then expand the region grammar around those split-support regions
if the entropy obstruction persists.

## Goal 3 Phase 36: Full Entropy-Mismatch Near-Hit Audit

Phase 36 audits the entropy-rejected operator/channel surface left by Phase 34
and Phase 35. It selects the three source pairs whose Phase 26 frontier still
has entropy mismatches, then runs exact algebra, erasure, and survivor checks on
every entropy-mismatched record:

```text
selected source pairs:               (16,23), (21,27), (26,27)
raw graph/CWS codes:                       33
relaxed codes checked:                     33
bridge axis:                                Y
source-pair variant records:              30
offset-flip variants per source pair:      10
parent circuits:                            2
punctured regions per variant:             25
candidate records:                        750
entropy-match records skipped:            270
entropy-mismatch records checked:         480
mismatch min-cut-variable records:         480
operator/channel split records:           165
entropy-mismatch near-hits:               165
channel-visible near-hits:                 85
operator-only near-hits:                   80
leaf-to-root near-hits:                     0
alternating near-hits:                    165
distance-3 witness source variants:        30
```

The source-pair profile repeats exactly:

```text
graph_cws_labeled_source_ord16_ord23: 55 near-hits
graph_cws_labeled_source_ord21_ord27: 55 near-hits
graph_cws_labeled_source_ord26_ord27: 55 near-hits
```

The parent-circuit partition is sharp:

```text
leaf_to_root_same_position:          0 near-hits
alternating_disentangler_isometry: 165 near-hits
```

The alternating variant profile is:

```text
flip_offset_0_to_leaf_to_root: 30 near-hits
flip_offset_1_to_root_to_leaf: 45 near-hits
flip_offset_2_to_leaf_to_root: 15 near-hits
flip_offset_3_to_root_to_leaf: 45 near-hits
flip_offset_4_to_leaf_to_root: 30 near-hits
```

Thus the operator/channel-visible geometry is present, but it is localized on
an entropy-mismatched alternating-circuit support. The obstruction is no longer
diffuse: Phase 36 points directly at split-support regions such as
`root_shell_plus_edge_*_minus_q129` and `root_shell_plus_edge_*_minus_q139`.

The Phase 36 recommendation is `adapt_then_proceed`: build a bounded
split-support region grammar around the alternating near-hit regions, then rerun
the exact entropy/min-cut/operator/channel filter.

## Goal 3 Phase 37: Split-Support Region Grammar

Phase 37 follows the Phase 36 recommendation with a bounded local support
grammar around the alternating near-hit surface. It reuses the three Phase 36
alternative source pairs, the Y-axis interface star, and only the alternating
offset-flip variants that carried near-hits. For each seed region, it tries two
local leaf-support edits:

```text
add_leaf_private: add one leaf-private qubit at offsets 0..3
swap_leaf_handle: move the original leaf handle at offset 4 to offsets 0..3
```

The exact frontier is:

```text
selected source pairs:                  (16,23), (21,27), (26,27)
raw graph/CWS codes:                          33
relaxed codes checked:                        33
seed alternating variants:                     5
seed variant/root-hole rules:                 11
seed base records:                           165
unique split-support regions:                200
candidate split-support records:            1320
add-leaf-private records:                    660
swap-leaf-handle records:                    660
capacity profiles scored:                     10
entropy-match records:                         0
entropy-mismatch records:                   1320
operator/channel checked records:              0
min-cut-variable records:                   1320
admissible entropy-matched hits:               0
distance-3 witness source variants:           15
```

The candidate profile preserves the Phase 36 near-hit multiplicity:

```text
graph_cws_labeled_source_ord16_ord23: 440 candidates
graph_cws_labeled_source_ord21_ord27: 440 candidates
graph_cws_labeled_source_ord26_ord27: 440 candidates
```

The root-hole pressure is strongly concentrated at q139:

```text
q129: 240 candidates
q134: 120 candidates
q139: 600 candidates
q144: 120 candidates
q149: 240 candidates
```

Every adapted region remains capacity-sensitive, with min-cut value profiles
`(7,9,11,12,15,17)` and `(8,10,12,13,16,18)`, but none repairs entropy. Thus
the local split-support edits do not turn the Phase 36 operator/channel
near-hit surface into a strict holographic cousin. The obstruction survives as
an entropy-gate failure before the exact operator/channel stage is reached.

The Phase 37 recommendation is `adapt_then_proceed`: change the support scale
instead of doing more single-leaf surgery. A next bounded scout should focus on
the q139-heavy seed surface with two-leaf additions, cross-leaf handle swaps, or
an outer-circuit/source-pair change while preserving exact min-cut, entropy,
algebra, erasure, and survivor checks.

## Goal 3 Phase 38: q139 Support-Scale Strict Hits

Phase 38 follows the Phase 37 recommendation and focuses on the q139-heavy seed
surface. It reuses the three alternative graph/CWS source pairs, the Y-axis
interface star, and the five alternating offset-flip variants. Around each q139
seed region it tries two bounded larger-support edits:

```text
same_leaf_two_private_add: add two private qubits from leaf offsets 0..3
cross_leaf_private_add:    add one private qubit on a different leaf cell
```

The exact frontier is:

```text
selected source pairs:                  (16,23), (21,27), (26,27)
raw graph/CWS codes:                          33
relaxed codes checked:                        33
q139 base regions:                             5
seed alternating variants:                     5
seed base records:                            75
unique q139 support regions:                 110
candidate q139 support records:             1650
same-leaf two-private records:               450
cross-leaf private records:                 1200
capacity profiles scored:                     10
entropy-match records:                        25
entropy-mismatch records:                   1625
operator/channel checked records:             25
min-cut-variable records:                   1650
admissible entropy-matched hits:              25
channel-visible admissible hits:              15
operator-only admissible hits:                10
distance-3 witness source variants:           15
```

The strict hits are completely localized:

```text
source pair: graph_cws_labeled_source_ord21_ord27
edit kind:   same_leaf_two_private_add
leaf offsets added: (0,3)
hits per alternating variant: 5
hits per leaf cell:           5
```

Their entropy profile is:

```text
(4,4): 10 hits
(5,5):  5 hits
(6,6): 10 hits
```

Every strict hit has exact min-cut values `(9,11,13,14,17,19)`, remains
capacity-sensitive, and has a reconstruction-visible operator-algebra split.
Fifteen of the twenty-five also differ in erasure/channel-visible semantics;
the remaining ten are operator-only splits. This is the first certified finite
Goal 3 tensor-network/holographic-code layer where entropy/min-cut-visible
geometry agrees while observer-patch reconstruction, and often channel
behavior, differs.

The Phase 38 recommendation is `proceed`: validate and compress the witness.
The next phase should isolate the smallest representative hit, audit nearby
single-qubit deletions/additions and alternative offsets, and export a concise
human-facing theorem-style certificate for the exact separation.

## Goal 3 Phase 39: Representative Witness Robustness

Phase 39 compresses the Phase 38 strict-hit family to one canonical witness and
audits its local neighborhood. The representative is:

```text
source pair:       graph_cws_labeled_source_ord21_ord27
bridge axis:       Y
outer variant:     alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root
base region:       root_shell_plus_edge_0_minus_q139
added leaf qubits: q0, q3
region length:     27
entropy pair:      (4,4)
min-cut values:    (9,11,13,14,17,19)
semantic split:    reconstruction-visible and channel-visible
```

It then checks three exact local buckets:

```text
same-leaf offset alternatives:       6 records,  1 strict hit
single-qubit deletions:             27 records, 15 strict hits
bounded local single additions:     19 records, 18 strict hits
total neighborhood records:         52
neighborhood strict hits:           34
all records exact/min-cut-variable: 53 including representative
```

The offset alternative audit shows that `(0,3)` is unique among the six
same-leaf private offset pairs. The deletion/addition audit shows that the
representative is not locally minimal: many neighboring regions still preserve
the strict entropy/min-cut plus reconstruction/channel separation. All 34
neighbor strict hits are channel-visible.

The strict deletion qubits are:

```text
125, 128, 129, 130, 133, 134, 135, 136, 137, 138, 140, 143, 144, 146, 147
```

The strict addition qubits are:

```text
1, 2, 25, 26, 27, 28, 50, 51, 52, 53, 75, 76, 77, 78, 100, 101, 102, 103
```

So the Phase 38 witness is not a one-record accident. It is a compact,
channel-visible local plateau: entropy/min-cut-visible geometry agrees while
observer reconstruction and channel semantics differ across a small certified
neighborhood.

The Phase 39 recommendation is `proceed`: export the human-facing theorem-style
memo and compact witness index for the representative hit plus its robust
deletion/addition plateau.

## Goal 3 Phase 40: Theorem-Style Holographic-Cousin Package

Phase 40 packages the Phase 38 strict-hit family and Phase 39 representative
plateau into a compact theorem-style witness bundle:

```text
representative: graph_cws_labeled_source_ord21_ord27
bridge axis:    Y
outer variant:  alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root
region:         root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3
entropy pair:   (4,4)
min-cut values: (9,11,13,14,17,19)
separation:     reconstruction-visible and channel-visible
```

The package records six proof obligations:

```text
entropy-visible geometry agrees
min-cut-visible geometry is exact and capacity-sensitive
observer reconstruction geometry differs
channel/erasure geometry differs
the representative is supported by the 25-hit Phase 38 family
the representative has the 34-hit Phase 39 local plateau
```

Supporting portable artifacts:

```text
docs/goal3_phase40_theorem_package.md
docs/goal3_phase40_witness_index.json
```

The Phase 40 recommendation is `stop` for the core finite Goal 3 search target:
an exact finite holographic-cousin witness now has machine certificates, JSON
artifacts, README notes, and a human-facing package. Natural extensions are to
generalize across bridge axes, search for smaller/familial variants, or turn the
finite package into a formal proof appendix.

Capstone package:

```text
docs/finite_ds_like_qec_capstone_memo.md
docs/desitter_qec_toy_model_memo.md
docs/desitter_qec_certificate_index.json
docs/goals1_3_program_memo.md
docs/goal3_tensor_network_holographic_result.md
docs/goal3_certificate_index.json
```

Run tests:

```bash
python3 -m unittest discover -s tests
```
