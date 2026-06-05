# Goal 8 Related-Work and Novelty Audit

This is a quick primary-source sanity pass, not a comprehensive literature
review. The purpose is to keep the Goal 8 claim honest before a Harlow-facing
package.

## Verdict

Goal 8 is **not** novel as a standalone stabilizer/OAQEC linear-algebra
identity. Its algebraic ingredients are close to known stabilizer secret-sharing,
stabilizer-OAQEC, and finite-dimensional OAQEC facts.

The plausible contribution is the **observer-algebra tomography hierarchy**:
weak physical-only shadows collide, while physical response plus commutator
tomography completes the all-region observer-algebra signature, with bounded
minimality records and certificate-backed witnesses.

## Closest Sources

| Source | What It Already Covers | Overlap With Goal 8 |
| --- | --- | --- |
| Beny-Kempf-Kribs, *Quantum Error Correction of Observables* ([arXiv:0705.1574](https://arxiv.org/abs/0705.1574)) | Heisenberg/operator-algebra QEC for correctable observable algebras, including hybrid quantum-classical information. | Foundational OAQEC language; Goal 8 should cite this as background, not novelty. |
| Almheiri-Dong-Harlow, *Bulk Locality and Quantum Error Correction in AdS/CFT* ([arXiv:1411.7041](https://arxiv.org/abs/1411.7041)) | Connects AdS/CFT reconstruction, QSS, and OAQEC. | Confirms that QSS/OAQEC is the right holographic language. Goal 8 is a finite diagnostic program, not a new AdS/CFT theorem. |
| Harlow, *The Ryu-Takayanagi Formula from Quantum Error Correction* ([arXiv:1607.03901](https://arxiv.org/abs/1607.03901)) | Presents quantum-corrected RT results in finite-dimensional OAQEC/subalgebra-code language. | Directly adjacent framing; Goal 8 can be pitched as finite observer-algebra tomography, not RT-from-QEC. |
| Dauphinais-Kribs-Vasmer, *Stabilizer Formalism for Operator Algebra Quantum Error Correction* ([arXiv:2304.11442](https://arxiv.org/abs/2304.11442)) | Stabilizer-OAQEC formalism and a theorem characterizing correctable Pauli errors. | High-overlap for stabilizer-OAQEC mechanics; Goal 8 should not claim a new stabilizer-OAQEC formalism. |
| Matsumoto/Yamashita, *Classical Access Structures of Ramp Secret Sharing Based on Quantum Stabilizer Codes* ([arXiv:1811.05217](https://arxiv.org/abs/1811.05217)) | Qualified/forbidden/intermediate access structures and intermediate information in terms of finite-field stabilizer linear spaces. | Closest overlap for intermediate-region information. Goal 8's `dim L_R`/center/rank computations should be treated as known-derived until proven otherwise. |

## Claim Audit

| Goal 8 Component | Novelty Risk | Safe Status |
| --- | --- | --- |
| `dim L_R = dim(S^perp \cap P_R) - dim(S \cap P_R)` | High overlap with stabilizer/QSS/OAQEC linear algebra. | Known-derived lemma. |
| Restricted commutator rank determines center/radical dimension. | Standard symplectic linear algebra. | Known-derived bookkeeping. |
| `dim L_R^perp = 2k - dim L_R`. | Standard nondegenerate symplectic identity. | Known-derived bookkeeping. |
| Weak shadows such as channel, center, and dimension-only response fail for `k>1`. | Likely close to known access-structure/intermediate-information phenomena. | Certificate-backed finite hierarchy; phrase as bounded atlas evidence unless generalized. |
| Physical response plus commutator tomography determines `tau(R)`. | May reduce to local-centralizer quotient plus symplectic form. | Theorem-style packaging of known ingredients; novelty is the intrinsic operational framing and hierarchy. |
| Equivalence-aware atlas with minimal collisions and distance-amplified witnesses. | I did not find this exact diagnostic-atlas package in the quick search. | Plausibly new artifact/contribution. |
| Observer-algebra tomography as Harlow-facing program. | Conceptually adjacent to OAQEC and observer-algebra work, but not found as a named finite-code diagnostic hierarchy. | Plausibly new framing; should be pitched humbly. |

## Do Not Claim

- Do not claim a new stabilizer-OAQEC formalism.
- Do not claim the local-centralizer quotient identity is new.
- Do not claim a continuum-gravity or AdS/dS theorem.
- Do not claim exhaustive novelty without a deeper review of QSS access
  structures and OAQEC recovery/tomography literature.

## Safe Claim Language

Use:

> We give a finite stabilizer/OAQEC observer-algebra tomography hierarchy.
> Standard stabilizer/OAQEC linear algebra implies that local physical response
> plus commutator data determine the observer-algebra signature. The new
> contribution is to package this as an intrinsic diagnostic hierarchy, with
> bounded-minimal counterexamples for weaker physical-only shadows and exact
> certificates.

Avoid:

> We discovered a new way to reconstruct OAQEC algebras.

## Harlow-Facing Pitch

> This may be known in QSS/OAQEC language, so I am framing it cautiously. The
> finite result is an observer-algebra tomography hierarchy: entropy/channel and
> several intrinsic response shadows fail, while local physical response plus
> commutator tomography determines the observer algebra in stabilizer/OAQEC. The
> implementation gives bounded-minimal collision witnesses and distance-amplified
> certificates. I would be curious whether this hierarchy is already standard, or
> whether the observer-diagnostic framing is worth formalizing.

## Next Sanity Check

Before calling the theorem publishable, map the Goal 8 signature

```text
tau(R) = (dim L_R, dim Z_R, dim L_R^perp, L_R = L)
```

onto the precise stabilizer secret-sharing information groups/access-structure
quantities in Matsumoto/Yamashita and the correctable-Pauli characterization in
Dauphinais-Kribs-Vasmer. If the map is exact, the theorem is known-derived and
the paper should lead with the hierarchy/certificates/framing. If the map is not
exact, the difference should be stated as the real mathematical contribution.
