# Harlow-Facing Paper Goal

Status: proposed paper-level completion goal under the active observer-algebra
research program

## Working title

**Finite Directional Records in a de Sitter Static Patch: Information
Capacity, Lifetime, and Gravitational Footprint of a Localized Observer**

## Goal

Produce a theorem-first manuscript showing that, for one declared localized
observer model on fixed de Sitter, a relational `SO(3)` directional record has
a jointly controlled information capacity, operational lifetime, optical and
proper support, and gauge-invariant gravitational footprint, all evaluated on
one common state family, protocol, parameter regime, and perturbative order.

The paper is complete only when it:

1. derives a lower bound on the directional-record information required for a
   target global relational alignment risk;
2. derives the record's finite-time degradation and readout error from the same
   local interaction used to create or access that record;
3. upper-bounds the available directional-record information using the same
   model's localization, energy, and weak-backreaction budgets;
4. certifies that the supported reference produces a nonzero normalized
   exterior electric-Weyl response on fixed de Sitter; and
5. eliminates the auxiliary budgets into one dimensionless compatibility or
   obstruction inequality with a complete error ledger.

The supported massive Skyrmion is the explicit realization. It is not the
scope of the operational theorem and does not belong in the headline.

## Theorem target

Freeze a declared model class `C_dir` consisting of:

- a localized directional register `O` with a unitary `SO(3)` action;
- a localized target or detector `D` carrying physical orientation markers;
- a static-patch field environment `E` in a specified KMS state;
- one local action for `O+D+E` and the supporting membrane;
- one controlled family of initial states;
- one preparation, storage, and relational readout protocol;
- explicit proper-time and optical-support conventions; and
- a fixed-background weak-response criterion.

For every admissible model, state, and allowed protocol in `C_dir`, prove a
statement of the schematic form

```text
R_rel(T) >= F_record[S_dir, Gamma(T), eta_channel],
S_dir    <= F_capacity[E_K, a, s_opt, rho_h, B_W; theta],

therefore

Phi(R_rel(T), T, s_opt, rho_h, B_W; theta) >= 0.
```

Here:

```text
R_rel(T)   Haar-prior global risk for alignment of D relative to O
S_dir      directional-record information, initially A_SO3(rho_O)
Gamma(T)   derived record-degradation exposure
eta_channel finite-time physical-to-effective channel error
E_K        Killing energy of the same observer configuration
a          proper enclosing radius
s_opt      optical support radius
rho_h      proper horizon distance
B_W        normalized gauge-invariant exterior electric-Weyl footprint
theta      declared model and approximation parameters
```

`S_dir` is directional record information, not thermodynamic entropy by
definition. For a covariant orientation ensemble it is naturally represented
by relative entropy of rotational asymmetry,

```text
S_dir=A_SO3(rho)=S(G_SO3[rho])-S(rho).
```

The existing theorem already gives

```text
R_rel >= c_SO3 exp[-2 S_dir/3],
c_SO3=6/(e pi^(5/3)),
```

and hence the necessary information allocation

```text
S_dir >= (3/2) log(c_SO3/R_rel)
```

whenever the right-hand side is positive. The manuscript must separately
prove any comparison between `S_dir`, effective record dimension, coarse-
grained observer entropy, and the `S_Ob` used in observer-rule frameworks.
They must not be identified by notation.

## Relational and record definitions

The task is not absolute orientation relative to coordinates. It is estimation
of the group element aligning two localized physical systems. "Global" refers
to the Haar prior and loss over all of `SO(3)`.

The record criterion is also not long-lived quantum coherence. Define record
stability operationally: after storage time `T`, the best allowed relational
readout must retain risk at most `epsilon`, or equivalently preserve a declared
number of distinguishable directional hypotheses to a declared error.

The same interaction should, within one controlled approximation:

- select or stabilize the orientation-record states;
- produce observer-environment entanglement;
- determine the degradation rate;
- implement or justify the readout channel; and
- contribute to the stress-energy ledger.

## Frozen gravitational observable

For this paper, use a fixed-background quantity that the repository can
actually certify:

```text
B_W = normalized l=2 electric-Weyl response on a fixed exterior annulus,
delta E_rr = -6 Psi(r) Y_2m/r^3.
```

The normalization must remove master-field convention and state clearly:

- the collective `Omega^2` or spin-quadrupole normalization;
- the observation annulus;
- center and horizon boundary conditions;
- the source-to-master and master-to-Weyl maps; and
- the perturbative smallness regime.

This establishes that the directional register is not gravitationally
invisible. It does not claim that `B_W` is the final entropy bottleneck in a
closed-universe observer rule. Whether horizon shift, QES displacement,
collapse, or another invariant should replace it is a central question for
external critique.

## Completion gates

### G1. Theorem domain

Write the exact quantifiers for `C_dir`, including randomized and adaptive
protocols, treatment of postselection, tunable parameters, approximation
order, and pointwise versus asymptotic scope.

Pass condition: a reader can construct a counterexample candidate without
guessing what an "observer" means.

### G2. Entropy and record dictionary

Prove the chain

```text
target relational risk
  -> required A_SO3
  -> required effective directional record dimension/information
  -> model energy and representation cost.
```

Pass condition: every arrow is a named inequality. No Casimir, QFI, asymmetry,
Hilbert-space dimension, or thermodynamic entropy is silently substituted for
another.

### G3. Physical finite-time record channel

Derive the preparation, storage, and readout channel from the declared local
action and prove an explicit distance to the effective heat/measure-correct
channel.

Pass condition:

```text
eta_channel < operational risk margin
```

on a nonempty open parameter set. A stipulated heat rate does not pass.

### G4. Certified gravitational footprint

Complete the current dual-weighted response enclosure and prove a normalized
lower bound

```text
|B_W| >= b_min > 0.
```

Pass condition: the interval excludes zero after origin, bulk, wall, and
finite-response errors are included. The current floating value is design
evidence only.

### G5. Common parameter window

Evaluate capacity, lifetime, support, channel error, and response on one state
family and one parameter box.

Pass condition: all assumptions hold simultaneously at the same perturbative
order. Combining bounds from incompatible regimes does not pass.

### G6. Eliminated theorem and manuscript

Eliminate internal budgets into one dimensionless inequality, state its escape
routes, and include the Skyrmion only as the theorem's realization.

Pass condition: a 15-25 page main manuscript can be read without the interval
audit details. Certificates and the profile proof live in appendices or a
technical companion.

## Explicit non-goals

This goal does not require:

- a theorem for arbitrary observers;
- identification of `S_dir` with a closed-universe observer entropy;
- a full Hartle-Hawking or gravitational path-integral derivation;
- self-consistent rotating Einstein-Skyrme geometry;
- tensorial Israel matching as a premise of the fixed-background theorem;
- a claim that nonzero Weyl response is the ultimate gravitational capacity
  bound; or
- publication "approval" from one external scientist.

The requested outcome from Dr. Harlow is conceptual critique and redirection.
Publication approval belongs to authors, editors, and referees.

## Decision rules

1. If G4 closes, freeze the fixed-background response theorem rather than
   immediately expanding into full self-gravity.
2. If G3 cannot produce a controlled physical record channel, publish Paper R
   separately and keep the lifetime theorem conditional.
3. If the `S_dir` to observer-entropy comparison is not meaningful, retain
   `S_dir` as operational directional information and ask what quantity should
   replace it.
4. If interval widths remain large, improve one correlation-aware
   representation. Do not reinterpret an upper-bound failure as a physical
   no-go.
5. Keep the validated profile theorem as a technical companion or independent
   fallback, not as the reason the observer paper matters.

## Harlow review packet

The review packet should contain:

1. a one-page theorem and dependency diagram;
2. a 3-5 page conceptual note weighted approximately 70% observer theorem,
   25% gravitational realization, and 5% profile certification;
3. the draft manuscript or detailed theorem outline;
4. a nearest-neighbor literature table with two or three papers per claim;
5. one linked technical certificate index; and
6. exactly three questions:

```text
1. Is A_SO3/effective directional record information meaningfully comparable
   to the observer entropy in the observer rule, or are they different
   resources?

2. Which gauge-invariant gravitational quantity should cap the capacity of a
   finite observer register in a de Sitter causal patch?

3. Would a one-action semiclassical model deriving relational records,
   lifetime, localization, and gravitational footprint clarify the observer
   rule, or is the closed-universe path integral essential from the outset?
```

## One-sentence finish line

**Deliver a theorem-first paper in which one localized finite directional
register acquires, stores, and reads a relational orientation record with
quantified information and lifetime, while the same controlled model fixes its
support, energy cost, and nonzero gauge-invariant gravitational footprint.**
