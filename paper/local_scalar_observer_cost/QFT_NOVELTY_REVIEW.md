# Relativistic Detector/QFT Novelty Review

## Review Assignment

Determine whether the finite-pointer energy-support-purity theorem below is
already known in relativistic detector theory, quantum communication, or
horizon decoherence, and whether its prescribed-source interpretation is
sound. The exact controlled Weyl channel is prior art and is not under review
as a new result.

## Result Under Review

For finite pointer weights `w_i` and conditional half-line momenta `p_i`
with common final support `[0,L]`, the paper proves

```text
Tr(rho_P^2)
 >= P_cl+(1-P_cl)exp[-C_beta(L)E_bar/(1-P_cl)],

S_2(rho_P)<=min{H_2(w),C_beta(L)E_bar},
```

where the pairwise thermal coefficient obeys

```text
C_beta(L)=2 L Lambda(pi L/beta).
```

The symmetric binary top-mode record saturates the entropy bound; global
sharpness for arbitrary pointer dimension is not claimed. For a conformal
massless scalar in a four-dimensional de Sitter static patch,
the Bunch-Davies relation `beta=2 pi R` makes the same s-wave momentum profile
the unique optimum over every angular and canonical sector. Sharpness concerns
final Cauchy support. A source radius and switching duration enter only through
the finite-propagation envelope for that support.

## Internal Equation-Level Audit

The following matrices record an author-side inspection of the primary
sources, completed on 2026-06-23. They replace a title-level similarity search
with an explicit comparison of models and variational problems. They do not
replace the requested specialist disposition.

### Channel and model matrix

| Source | Detector and switching | Exactness | State and covariance | Dephasing normalization |
| --- | --- | --- | --- | --- |
| [Landulfo 2016](https://arxiv.org/abs/1603.06641) | Prescribed gapless two-level systems; smooth compact spacetime smearings | Exact Weyl channel, nonperturbative | Arbitrary quasifree state, including KMS states through `mu` | Exactly `nu_j=omega[W(E(2f_j))]=exp[-2 mu(Ef_j,Ef_j)]` |
| [Barcellos and Landulfo 2021](https://arxiv.org/abs/2109.13896) | Same prescribed gapless qubits with compact switching and spatial smearing | Exact channel and energy accounting | Explicit KMS example with `coth(beta h/2)` | Same factor `exp[-2<K Ef,coth(beta h/2)K Ef>]` |
| [Aspling and Lawler 2023](https://arxiv.org/abs/2309.07218) | Delta-like UDW gates with tunable coupling and smearing | Controlled-unitary algebra is exact; near-unit-capacity examples use a strong-coupling approximation | Coherent-state/vacuum channel, not the static KMS covariance used here | Coherent overlaps are packaged as a bosonic dephasing parameter |
| [Batista et al. 2026](https://arxiv.org/abs/2605.00956) | Gapless finite-time detector in a trajectory superposition; smooth switching, pointlike examples | Exact Magnus/Weyl calculation | Minkowski vacuum with a Rindler thermal interpretation; a massive scalar controls infrared behavior | Exact overlap is expressed through the norm of the difference of sourced solutions |
| [de Ramon et al. 2021](https://arxiv.org/abs/2102.03408) | General compactly smeared nonrelativistic detectors | Causality analysis includes perturbative and structural statements | Not a KMS optimization paper | Warns that nonperturbative spatial smearing requires a microcausal interaction density |
| [Perche et al. 2024](https://arxiv.org/abs/2308.11698) | A relativistic probe field localized by an external potential | Single-mode detector equivalence is leading order in coupling | Not the exact KMS channel here | Supplies a possible autonomous-probe refinement, not this normalization theorem |

The factor of two in this manuscript is therefore **known-channel structure**,
not a new result. The present `Z phi(J)` interaction density is microcausal
because the same fixed `Z` commutes with itself and the scalar field is
microcausal. Nevertheless, one finite-dimensional pointer is shared across
the smearing. The paper must retain its stated boundary: a prescribed
gapless smeared detector, not an autonomous relativistic probe field.

### Optimization and support matrix

| Source | Compact support notion | Energy quantity | Energy optimized? | Sharp support constant or remainder? | Angular reduction and achievability? |
| --- | --- | --- | --- | --- | --- |
| [Landulfo 2016](https://arxiv.org/abs/1603.06641) | Compact interaction test functions | None in the channel theorem | No | No | No de Sitter all-sector reduction; no final-data controllability result |
| [Barcellos and Landulfo 2021](https://arxiv.org/abs/2109.13896) | Compact interaction test functions and finite switching intervals | Separates background production, individual switching work, and communication work at null infinity | No optimization over final profiles at fixed field energy | No support-dependent best constant | No de Sitter angular theorem; prescribed smearings are evaluated rather than optimized |
| [Aspling and Lawler 2023](https://arxiv.org/abs/2309.07218) | Detector smearing and switching parameters | No post-switch scalar-field variational constraint | No | No | No |
| [DSW 2023](https://arxiv.org/abs/2301.00026), [Gralla and Wei 2024](https://arxiv.org/abs/2311.11461), [DSW 2025](https://arxiv.org/abs/2407.02567), and [Li 2025](https://arxiv.org/abs/2501.00213) | Worldline or laboratory protocol scales, not compact final Cauchy support | Horizon/local soft-mode decoherence rates; negligible Killing energy is possible as duration grows | No fixed-support field-energy extremization | Rates and asymptotic laws, not `C_beta(L)` | No reduction of all scalar angular and canonical sectors to a compact-kernel optimizer |
| [Batista et al. 2026](https://arxiv.org/abs/2605.00956) | Finite detector activation and trajectory separation | Particle number and external switching-work interpretation | No | No | No; exact finite-time sources are analyzed for selected trajectories |
| Present manuscript | Final Cauchy data supported in `[0,L]`; source support enters only through a causal envelope | Post-switch scalar Killing energy of the coherent displacement | Yes: maximize exact dephasing at fixed energy and final support | Yes: `C_beta(L)` plus two uniform remainders | Yes in conformal de Sitter; smooth sources approach final-support data as the source worldtube approaches the final ball |

### First failed reductions

1. **Landulfo normalization map succeeds.** Set the two conditional source
   labels to `+J` and `-J`; their difference is `2J`, reproducing the paper's
   `Gamma=2 mu(EJ,EJ)`. The reduction first fails because no energy or final-
   support quotient is posed.
2. **Barcellos-Landulfo energy map partly succeeds.** Their individual
   source term is the classical energy of a sourced solution and their KMS
   characteristic function has the same `coth` covariance. The reduction
   first fails at the constraint: the source profile is prescribed, and no
   supremum at fixed post-switch energy and final Cauchy support is taken.
3. **Horizon-decoherence map fails at the variational problem.** Those works
   calculate rates or long-time soft-mode laws. Allowing the protocol duration
   and support to grow is precisely what the fixed-`L` theorem forbids.
4. **Localized-probe replacement fails at exactness.** Perche et al. derive
   an effective detector mode from a relativistic probe field at leading
   order. That result does not supply the exact Weyl channel or the sharp
   compact-support quotient, but it identifies a concrete future refinement.

### Finite-pointer composition

For diagonal sources `J_i`, the conditional purified field states form a
Gram matrix and give the exact Schur channel

```text
|i><j| -> G_ij |i><j|,
Gamma_ij=<p_i-p_j,B_beta,L(p_i-p_j)>/4.
```

The binary convention is recovered by `p_+=p` and `p_-=-p`. The
finite-pointer result then uses only the weighted variance identity and
Jensen's inequality. No inspected detector source supplies this exact
energy-support-purity composition or a general-d sharpness theorem.

## Internal Finding

**DISTINCT CONJUNCTION, EXTERNALLY PENDING.** The channel, KMS covariance,
normalization, and source-energy accounting are established prior art. No
inspected primary source supplies their conjunction with a finite-pointer
purity theorem, a fixed-final-support field-energy optimum, the explicit
thermal kernel remainders, and the strict conformal-de-Sitter all-sector
reduction.

This finding narrows rather than proves novelty. A detector/QFT specialist
must still decide whether the conjunction is physically useful and whether
the prescribed smeared-pointer boundary is acceptable for a short paper.

## Decisive Questions

1. Is the finite-pointer purity theorem already standard for controlled
   Gaussian displacements? If yes, give the source and match its normalization
   and centered energy to the equations here.
2. Is the constrained pairwise optimization already solved? If yes, give the source
   and map its dephasing functional, energy, support notion, and temperature to
   `Gamma`, `E`, `L`, and `beta` here.
3. Is the separation between the arbitrary-`beta` half-line theorem and the
   de Sitter all-sector corollary physically clear and useful?
4. Is a prescribed smeared finite pointer acceptable for this narrow theorem
   when actuator work, probe stress, and autonomous switching are expressly
   excluded?
5. Is the source-radius and duration statement correctly limited to a causal
   envelope, rather than sharp fixed-cylinder controllability?
6. Are the normalization, KMS covariance, canonical energy, and strict
   all-sector comparison correct?
7. Without the gravity appendix, is the central conjunction substantial
   enough for a short relativistic quantum-information or mathematical-
   physics paper? If not, identify the minimum bounded addition.

## Requested Disposition

Return one of the following in `REVIEW_RESPONSE_FORM.md`:

- **NOVEL:** no known work immediately supplies the constrained theorem and
  its de Sitter reduction; state why it is useful.
- **KNOWN:** give a precise source and equation-level reduction.
- **TECHNICALLY NEW BUT INSUFFICIENT:** identify the minimum theorem or physical
  realization needed to make the result publishable.

Please flag any normalization, causality, energy-accounting, or physical-
framing error separately from the novelty disposition.

The paper does not claim a new detector channel, general-d saturation, total
measurement cost, autonomous apparatus, perturbed-geometry channel, or coupled
gravitational evolution.
