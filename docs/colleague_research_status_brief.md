# Static-Patch Rotational Observer Program: Colleague Feedback Brief

Date: 2026-06-10

Branch: `codex/observer-algebra-research-program`

## Executive assessment

This repository can support a publishable mathematical-physics paper, but it
does not yet establish a new gravitational-physics breakthrough.

The most promising high-level paper is no longer “a Skyrmion calculation.” It
is a class-uniform observer tradeoff:

> A localized rotational reference in a static patch cannot simultaneously
> achieve arbitrarily accurate global orientation recovery, long operational
> coherence, small optical/proper support, and negligible gravitational
> disturbance, within a declared class of local matter references and
> interactions.

The massive supported Skyrmion is the candidate rigorous realization of the
premises and the source of explicit constants. This distinction matters. The
repository already proves substantial ingredients in separate controlled
models, but it has not yet proved that one physical action realizes all of them
simultaneously.

There are currently three credible publication outcomes:

1. A focused computer-assisted profile paper is close to submission-ready,
   conditional on an external novelty check and a careful defense of the hard
   wall.
2. A stronger fixed-background response paper becomes viable if the remaining
   interval enclosure certifies a nonzero gauge-invariant exterior response.
3. The full observer-tradeoff paper remains the highest-value target, but it
   additionally needs the self-gravitating junction and one-action open-system
   bridges.

## What is actually proved

### Operational reference bounds

For the Haar-prior global `SO(3)` chordal orientation task, every state and
measurement obeys two independent resource bounds, including

```text
R_ref >= 1/(16 <J^2>+8).
```

The result covers arbitrary spin-sector mixtures, rare high-spin tails, and
rotation-trivial multiplicities. It is a global orientation statement, not a
local-QFI proxy. For the declared spin-1 measure-and-correct protocol,

```text
(8/9) R_ref <= epsilon_rec <= 2 sqrt(R_ref).
```

For isotropic rotational heat flow, the risk at proper time `T` satisfies

```text
R_ref(T) >= 3/4 [1-exp(-2 Gamma)]
             + exp(-2 Gamma)/(16 C_max+8),
Gamma=integral_0^T gamma(tau) d tau.
```

A confined nonrelativistic orbital-matter class also has an all-state
localization-energy capacity theorem,

```text
<L^2> <= 2 M a^2 E_ex,
R_ref >= 1/(32 M a^2 E_ex+8).
```

These are genuine class-uniform theorems. They are not yet a theorem about all
relativistic observers or all recovery protocols.

### Certified Skyrmion profile and capacity inputs

For the prescribed fixed-background massive hard-wall problem with
`mu^2=1`, `lambda=1/400`, and wall radius `x=4`, a computer-assisted Newton
argument proves local existence and uniqueness, strict monotonicity, a
strictly negative wall slope, and finite positive rotor inertia. Representative
directed outputs include

```text
F'(4) in [-0.09465,-0.08746],
I_dimensionless in [21.149,48.921].
```

The spherical radial Hamiltonian constraint, a fixed-field lapse bound, a
collective gravity-to-Casimir elimination, and positive fixed-wall and moving-
wall radial gaps are also certified under their stated assumptions. These do
not yet constitute a rotating Einstein-Skyrme solution.

### Same-action centrifugal response on fixed de Sitter

The leading rotational quadrupole cannot consistently be treated as a rigid
profile. Static stress conservation forces a coupled two-field centrifugal
deformation plus a moving membrane. The repository now has:

- the exact coupled Hessian, rotational source, and pure-tension wall law;
- a closed positive Friedrichs realization with `||A^-1||<=100`;
- an exact nonzero weak matter deformation;
- conserved smooth bulk plus distributional membrane stress;
- exact conserved-stress-to-master-source and exterior-Weyl maps;
- exact rational primal and adjoint trial archives;
- cancellation-safe origin residuals and exact internal conormal continuity;
- validated moving-wall and positive-radius weak adjoint master loads.

The largest recent numerical advance is a centered correlated residual model.
On the same 43 authenticated outer cells it reduces the rigorous primal
residual-square enclosure from about

```text
328.1385  ->  0.01002770,
```

an improvement by more than a factor of 30,000. This shows that the former
barrier was dependency wrapping, not evidence of a large physical residual.
The certified origin primal residual square is about `2.13e-5`, and the primal
wall mismatch is below `0.001421`.

For the master adjoint, the moving-wall coefficient is rigorously positive,

```text
gamma_B in [0.00268810,0.00283471],
```

and the loaded adjoint wall mismatch is below `0.00634`. The positive-radius
bulk load has the exact weak form

```text
B_bulk(v)=integral (b0 dot v+b1 dot v') dx.
```

Because the derivative-test coefficient is nonzero, its norm must be bounded
directly in the form dual; treating it as an ordinary `L2` residual would be
incorrect. A completed-square `V*` construction is implemented. Its current
positive-radius-plus-wall diagnostic is about `0.77`, far above the
approximately `0.04` design target, with the dominant interval loss near
`x=0.5`. The regular-origin adjoint load is still missing, so this is not yet a
full adjoint residual certificate.

The floating exterior amplitude is stable and nonzero, of order `-2.8e-3`, but
floating stability is not the claimed result. The publishable response theorem
requires the rigorous dual-weighted interval to exclude zero.

## What is not proved

The following statements must not appear as conclusions of a paper today:

- a universal no-go theorem for arbitrary observers;
- a self-consistent rotating Einstein-Skyrme-de Sitter solution;
- a tensorially matched gravitating membrane worldtube;
- a physical KMS/open-system channel derived from the same total action as the
  profile, stress, and detector;
- a certified nonzero exterior master or Weyl amplitude;
- a full quantum-gravity detector prediction;
- novelty relative to the current literature without external specialist
  review.

The hard wall is physically consequential. It is not a harmless numerical
regulator: it supplies support, stress, boundary conditions, and spectral tail
behavior. A submission must either defend it as a physical membrane, smooth it
within a controlled family, or make the boundary-regularity dependence itself
part of the result.

## Recommended paper hierarchy

### Paper U: class-uniform observer tradeoff

Headline target: eliminate representation capacity, optical/proper support,
coherence exposure, and weak-backreaction budgets into one dimensionless
inequality over a named class of local rotational references.

This has the highest conceptual relevance. It is not ready to claim because
the capacity, bath rate, local readout, and gravitational margins are not yet
derived from one action.

### Paper R: certified fixed-background gravitational response

Headline target: prove that the supported rotating Skyrmion plus moving
membrane produces a nonzero gauge-invariant exterior static-patch quadrupole,
with a completely audited error interval.

This is the most important near-term technical gate. A positive result supplies
the physical realization needed by Paper U. A failure caused by a controlled
family-wide cancellation could instead become a no-go result; failure of a
coarse interval bound would not.

### Paper A: validated nonlinear profile

Headline target: computer-assisted existence and local uniqueness for the
declared massive hard-wall fixed-de Sitter Skyrmion profile, including signs,
wall slope, inertia, and radial stability.

This is the lowest-risk paper and could be drafted now. Its likely weakness is
physics impact unless novelty and the membrane interpretation are compelling.

### Ranked fallback papers

1. Optical common-mode no-go for separated local rotational observers.
2. Boundary-regularity universality of form-factor spectral tails.
3. The broader ULE/open-system construction after its constants become useful.

## Shortest decision path

1. Finish the response enclosure. Preserve Newton graph/slope correlations in
   the primal and adjoint Taylor models, certify the regular-origin adjoint
   load, and test whether the dual-weighted exterior interval excludes zero.
2. If zero exclusion closes, freeze Paper R's theorem and begin the spherical
   Einstein-Skyrme/Kottler plus six-amplitude Israel reconstruction.
3. If the interval remains broad, distinguish a representation failure from a
   physical cancellation. Improve the representation once; do not interpret
   an overestimate as a no-go.
4. In parallel, prepare Paper A and obtain an external novelty review. This
   gives the program a publishable result even if the larger bridge takes
   longer.
5. Promote to Paper U only after one declared total action supplies the
   reference capacity, support, bath exposure, readout time, stress, and
   gravitational margins on one open parameter family.

## Questions for external feedback

1. Is the global `SO(3)` localization-reference-coherence-backreaction framing
   sufficiently distinct from existing quantum-reference-frame and clock
   backreaction results?
2. Is a physical pure-tension supporting membrane an acceptable model, or is a
   smooth confining family essential for credibility?
3. Would a certified nonzero fixed-de Sitter exterior Weyl response be enough
   for a focused mathematical-physics paper, or is self-gravitating Israel
   matching expected before publication?
4. Is the computer-assisted profile theorem independently novel enough for a
   short paper?
5. Which audience is the best fit: mathematical relativity, soliton physics,
   quantum reference frames, or open quantum systems in curved spacetime?
6. Which premise of the proposed class-uniform theorem looks least defensible:
   the rotational spectral floor, local KMS coupling, optical/proper support
   map, or weak-backreaction criterion?

## Bottom line

There is a real paper here already at the computer-assisted
mathematical-physics level, subject to novelty review. There is a plausible
stronger paper in the certified fixed-background response, and the latest
correlation result materially improves its prospects. The universal observer
tradeoff remains possible and worth pursuing, but it should be presented as
the primary research target rather than as a theorem already established.
