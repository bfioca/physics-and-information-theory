# Finite Type-Certification Control Result And Stop Decision

Status: completed prove-or-kill sprint, 2026-06-17. The exact finite controls
and primary-source audit pass. The proposed generic finite-certification
theorem does **not** survive as a new paper result.

## Executive Verdict

The motivating question was whether bounded observers are unable to certify
non-Type-I algebraic structure because every bounded protocol has an
indistinguishable Type-I surrogate. That statement is not a viable generic
headline.

First, factor type is not operationally invisible. Embezzlement and related
entanglement tasks distinguish von Neumann types and subtypes when the task is
quantified over arbitrarily large targets and arbitrarily small errors. In
particular, Type-`III_1` factors are universal embezzlers.

Second, the bounded version becomes either elementary or false depending on
what the surrogate must preserve:

- on a declared finite tensor cylinder, the finite Type-I cutoff reproduces
  the complete protocol exactly;
- for approximately matched channel calls, the ordinary adaptive hybrid
  argument controls the output distance;
- reproducing a fixed finite list of statistics is finite-dimensional
  simulation, not a theorem about global algebraic connectivity; and
- requiring a Type-I surrogate to preserve the complete global factor or
  connectivity structure asks it to preserve the very invariant it is meant
  to differ on.

The sprint therefore yields a useful control package but triggers its kill
rule.

```text
Decision: CONTROL PASS / STOP as a generic finite-certification paper.
```

One ambitious residual remains open: derive the support, energy, time,
complexity, or gravitational cost of implementing a known operational type
witness in one named local physical model. That is not proved here.

## 1. Protocol Domain

A protocol budget is

```text
B=(d_P,n,E,T,m,a,d_out),
```

where `d_P` is the probe dimension, `n` the number of calls, `E` an energy cap,
`T` a duration cap, `m` the accessible tensor cylinder or named localization
region, `a` records whether adaptive controls are permitted, and `d_out` is
one of half trace distance, total variation distance, or an
energy-constrained half-diamond distance. Every postselection flag remains in
the unconditional output.

An admissible surrogate must reproduce the declared operational interface:

1. the nested local algebras actually addressed by the protocol;
2. the restricted state and all allowed preparations and instruments;
3. the declared dynamics and covariance on that interface;
4. the same probe, call, energy, duration, support, and adaptivity ledger; and
5. the refinement maps among all addressed cutoffs.

It need not preserve the inaccessible global factor type. Demanding that would
make a Type-I surrogate impossible by definition. Conversely, replacing only
the final transcript distribution is too weak: any one finite experiment can
be encoded as a finite classical-quantum channel.

The executable schema is `FiniteCertificationBudget` in
`qgtoy/finite_type_certification_control.py`. Its energy and duration entries
are ledgers only. A physical theorem must separately derive finite support or
channel approximation from those caps.

## 2. Exact Cylinder Control

Let

```text
A_m=M_2 tensor ... tensor M_2,
A_infinity=closure union_m A_m,
```

with the alternating faithful Gibbs product state and its product modular
dynamics. If every preparation, channel, memory interaction, and readout in a
protocol is supported on the first `m` factors, then running it in the infinite
system is exactly equivalent to running it on the finite Type-I system
`A_m=M_(2^m)`.

The reason is stronger than agreement of a few expectations. The state,
products, adjoints, inclusions `A_j subset A_m` for `j<=m`, and modular action
all restrict exactly. Induction over the adaptive branches therefore gives
identical joint states and transcripts at every round:

```text
d_out(pi[A_infinity],pi[A_m])=0.                       (FC.1)
```

This is an exact model control, not a general AQFT theorem. It does not show
that a bound on energy or duration forces support on finitely many tensor
factors.

## 3. Approximate Adaptive Control

Suppose a protocol makes `n` calls and each physical call differs from its
surrogate by at most `epsilon` in the halved diamond norm, or in an
energy-constrained version whose domain contains every adaptive input. Insert
the surrogate calls one at a time. Contractivity of intervening channels and
the triangle inequality give

```text
d_out <= min(1,n epsilon).                             (FC.2)
```

Arbitrary finite memories and adaptive controls are allowed. Equation (FC.2)
does not produce the per-call estimate. Nuclearity, the split property, or
strong convergence alone does not automatically supply a uniform
energy-constrained diamond bound that also preserves the full declared net and
dynamics.

## 4. Why Embezzlement Changes The Question

Operational algebra-type results make a blanket invisibility claim false.
For a Type-`III_1` factor, every normal state is an embezzling state: arbitrary
finite entangled targets can be produced with arbitrarily small error by local
algebra unitaries while the resource state is almost unchanged. Hyperfinite
Type-`III_1` systems also induce finite-dimensional embezzling families along
increasing matrix subalgebras.

This does not give a one-shot finite certificate against unrestricted Type-I
alternatives. For each fixed target and nonzero tolerance, a sufficiently
large finite catalyst can pass the same test. What separates the infinite
factor is the uniform family as target dimension grows and error shrinks.

For a pure finite catalyst of local Schmidt dimension `D`, a maximally
entangled target of rank `k`, and global half trace error `t`, local unitaries
preserve the catalyst marginal entropy. The
[Audenaert continuity bound](https://arxiv.org/abs/quant-ph/0610146) gives the
necessary condition

```text
log k <= t log(D k-1)+h_2(t),                          (FC.3)

D >= {1+exp[(log k-h_2(t))/t]}/k.                     (FC.4)
```

Perfect finite-dimensional embezzlement is therefore impossible. For qubit
sites, (FC.4) gives an explicit support floor by taking `ceil(log_2 D)`.
This is a standard entropy-continuity consequence, not a new factor theorem.

## 5. Exact Finite-Prefix Frontier

The repository's alternating Gibbs ITPFI construction provides a useful
bridge model. Its infinite product-state GNS algebra is the hyperfinite
Type-`III_1` factor, while each `m`-site prefix is the Type-I matrix algebra
`M_(2^m)`.

Let `p_1>=...>=p_D` be the prefix Schmidt probabilities. Before embezzlement,
the target register is separable, so the combined Schmidt vector is `p` padded
with zeros. The desired catalyst-plus-maximally-entangled-target vector has
probabilities `p_i/k`, each repeated `k` times. Local unitaries preserve the
Schmidt coefficients. The rearrangement inequality therefore gives the exact
maximum root fidelity

```text
F_root^max=sum_(r=1)^D sqrt[p_r q_r],                  (FC.5)
q=sort_desc({p_i/k repeated k times}),
t_min=sqrt(1-(F_root^max)^2).                          (FC.6)
```

Multiplicity blocks make (FC.5) computable without storing `2^m` entries. A
separate brute-force enumeration agrees through five sites to below
`5e-15`.

For a Bell-pair target at `beta=1`, selected exact finite-spectrum values are:

| sites `m` | optimal half trace error |
| ---: | ---: |
| 8 | 0.3188699191 |
| 16 | 0.2184901025 |
| 32 | 0.1442971222 |
| 64 | 0.0995070495 |
| 128 | 0.0695149854 |
| 256 | 0.0490796359 |

Across the checked range, `sqrt(m)t_min` approaches a target-dependent
constant for target ranks `2`, `4`, and `8`. This is numerical evidence for a
`m^(-1/2)` prefix rate, not a proved asymptotic theorem. Turning it into a
central-limit theorem would still price only support under arbitrary local
unitaries, not energy, time, locality of gates, or gravity.

## 6. Prior-Art Audit

| Source | What it establishes | Consequence here |
| --- | --- | --- |
| van Luijk, *Entanglement in von Neumann Algebraic Quantum Information Theory* ([arXiv:2510.07563](https://arxiv.org/abs/2510.07563)) | Operational entanglement properties classify von Neumann factor types and subtypes. | Generic operational invisibility is false. |
| van Luijk, Stottmeister, Werner, and Wilming, *Embezzlement of entanglement, quantum fields, and the classification of von Neumann algebras* ([arXiv:2401.07299](https://arxiv.org/abs/2401.07299)) | Type-`III_1` factors are universal embezzlers; hyperfinite restrictions yield finite embezzling families. | The right issue is quantitative physical cost, not existence of an operational witness. |
| van Luijk, Stottmeister, and Wilming, *Critical Fermions are Universal Embezzlers* ([arXiv:2406.11747](https://arxiv.org/abs/2406.11747)) | Infinite critical systems are universal embezzlers and finite ground-state subsequences form embezzling families. | Finite manifestations are already known; the theorem is qualitative in the required system size. |
| Fewster, *The split property for locally covariant quantum field theories in curved spacetime* ([arXiv:1501.02682](https://arxiv.org/abs/1501.02682)) | Nuclearity can imply Type-I split inclusions between nested local regions. | A split inclusion is not a complete Type-I replacement of the net and supplies no protocol error rate by itself. |
| Hirshberg, Kirchberg, and White, *Decomposable approximations of nuclear C*-algebras* ([arXiv:1109.2379](https://arxiv.org/abs/1109.2379)) | Nuclear algebras admit refined finite-dimensional completely positive approximations. | Finite-set CP approximation does not automatically preserve local inclusions, dynamics, covariance, and an operational norm uniformly. |
| Shirokov, *Energy-constrained diamond norms and their use in quantum information theory* ([arXiv:1706.00361](https://arxiv.org/abs/1706.00361)) | Energy-constrained diamond norms metrize strong channel convergence and support continuity bounds. | This is the appropriate approximate protocol metric once a physical per-call estimate is proved. |

The closest source also states the surviving problem directly: the required
QFT embezzlement unitaries and their status as physically viable local
operations are not known explicitly, and quantification by available energy
density remains open. That substantially narrows the novelty lane.

## 7. Counterexample And Kill Audit

| Candidate claim | Decisive test | Result |
| --- | --- | --- |
| Every finite protocol detects global type | Restrict the ITPFI model to its addressed cylinder | False: exact Type-I surrogate, (FC.1). |
| No finite protocol can display Type-III behavior | Run a fixed embezzlement target at nonzero tolerance | Misframed: large finite Type-I catalysts approximate the same task. |
| Hyperfiniteness proves the full physical theorem | Demand local net, dynamics, covariance, and energy-constrained comb control | Not established by finite-set CP approximation. |
| Preserve complete global connectivity in the surrogate | Require a Type-I system to preserve the global factor invariant | Inconsistent by construction. |
| The observed prefix rate is the paper | Compare with known embezzling families and arbitrary-unitary assumptions | Control calculation only; physical implementation cost is absent. |

Algebraic connectivity adds a separate ambiguity. A global connectivity
criterion such as a factor inclusion or algebraic ER=EPR condition is not a
finite output observable. To test it operationally one must first name a
uniform family of challenges and a closed alternative model class. Without
that definition, either finite statistics are simulable or preservation of
the answer is built into the surrogate requirement.

## 8. Surviving Ambitious Direction

A paper-worthy successor would fix one Hamiltonian or local QFT model and one
operational witness, then prove a two-sided resource statement such as

```text
t_m(k) <= epsilon
  => max{support radius, energy, duration, circuit cost, backreaction}
     >= L(k,epsilon),                                  (FC.7)
```

with `L` diverging as `epsilon -> 0` or `k -> infinity`, together with an
explicit admissible protocol showing that the scaling is achievable or nearly
so. The operations must arise from the named local action rather than from the
entire abstract unitary group of a local algebra.

This is a credible ambitious program because the algebraic witness exists and
the physical implementation problem is explicitly open. It is not yet a
paper, and the present sprint does not justify a static-patch, gravitational,
connectivity, or ER=EPR claim.

## Reproduction

```bash
PYTHONPATH=. python3 -m pytest -q \
  tests/test_finite_type_certification_control.py
PYTHONPATH=. python3 \
  experiments/finite_type_certification_control_audit.py
python3 -m json.tool \
  experiments/finite_type_certification_control_certificate.json >/dev/null
```

The focused suite checks the entropy floor, adaptive hybrid bound, exact
cylinder surrogate, compressed-versus-brute-force spectrum optimization, and
frontier monotonicity. The JSON certificate records ordinary floating-point
values; it is not an interval proof of the apparent asymptotic rate.
