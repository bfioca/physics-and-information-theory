# Covariant-Observer Energy Identifiability No-Go

Status: exact compact-`SO(3)` identifiability obstruction for instantaneous
reference recovery; not a physical no-go for a specified observer action

## Question

Does a covariant observer Hilbert space, symmetry representation, and recovery
accuracy determine the energy or backreaction cost of the reference frame?

For the compact rotation sector used in this repository, the answer is no.
Those data determine a kinematic resource requirement, but a physical energy
requires an additional dynamical completion.

## Exact Statement

Fix the truncated Peter-Weyl reference

```text
R_J=direct_sum_(j=0)^J V_j tensor V_j^*,
```

its canonical token, orientation POVM, and measure-and-correct decoder. The
recovery channel depends on the representation cutoff `J`, not on a separately
assigned Hamiltonian.

The left Casimir is positive, has ground value zero, commutes with the rotation
action, and obeys

```text
<C_left>=3J(J+2)/5
```

in the canonical token. For every positive coefficient `a_J`, therefore,

```text
H_J=a_J C_left
```

is an admissible positive rotation-invariant Hamiltonian for this kinematic
model. Given any prescribed positive ground-subtracted token energy `E_J`, the
choice

```text
a_J=5E_J/[3J(J+2)]
```

realizes it exactly. The target spin, reference dimension, token, POVM, decoder,
and recovery error are unchanged.

Consequently, apart from the trivial positivity bound, covariance and
instantaneous recovery data alone imply no positive universal lower bound, no
finite universal upper bound, and no universal stretched-horizon energy
exponent. The fixed-inertia law

```text
E_ref=3J(J+2)/(10I)=O(delta^-2)
```

remains correct inside the previously declared rotor model with `I` fixed. It
is not selected by the observer algebra or recovery theorem.

Different cutoff-dependent choices of `a_J` or `I_J` are dynamically inequivalent
regulator completions. Their role in the certificate is to prove missing
identifiability, not to claim that one physical observer can change its inertia
arbitrarily.

## Chen-Xu Action Audit

Chen and Xu construct a covariant de Sitter observer and averaged Type-II
algebra in [arXiv:2511.00622v2](https://arxiv.org/abs/2511.00622v2). Their
explicit `dS_2` first-order action couples conserved isometry charges to the
worldline. In higher dimensions they introduce the clock and orthogonal frame
kinematically on `L^2(SO(1,d))`, together with the corresponding generators and
constraints.

The source does not provide a higher-dimensional rotational kinetic term,
moment of inertia, finite-size frame action, or positive compact-frame
Hamiltonian. Its large-mass condition gives a qualitative route for suppressing
trajectory recoil, but does not determine the compact rotor energy used here.

This source audit identifies the missing dynamical input that prevents the
repository's compact Peter-Weyl comparison from being promoted to a Chen-Xu
energy prediction. The theorem itself applies only to that finite compact token
and instantaneous decoder, not to the full ideal `L^2(SO(1,d))` observer or its
noncompact constraint algebra.

## Prior-Art Boundary

Quantum-reference-frame resource theory already distinguishes representation,
asymmetry, size, and task accuracy from realization-specific energy. Relevant
primary sources include:

- [Gour and Spekkens](https://arxiv.org/abs/0711.0043), resource theory of
  quantum reference frames;
- [Marvian and Spekkens](https://arxiv.org/abs/1104.0018), group-theoretic
  characterization of pure-state asymmetry;
- [Miyadera and Loveridge](https://arxiv.org/abs/2006.14247), reference-size and
  channel-accuracy tradeoffs;
- [Peres and Scudo](https://arxiv.org/abs/quant-ph/0103149) and
  [Bagan, Baig, and Munoz-Tapia](https://arxiv.org/abs/quant-ph/0106014),
  rotational-frame transmission;
- [Yang et al.](https://arxiv.org/abs/2007.09154), recovery with bounded quantum
  reference frames.

The elementary rescaling observation is not claimed as a new general QRF
principle. The contribution here is to isolate its exact consequence for the
repository's geometry-derived target and recovery certificate, preventing the
fixed-`I` `delta^-2` illustration from being misidentified as a gravitational
prediction.

The statement is also restricted to a compact rotation subgroup and an
instantaneous protocol. For time translations the Hamiltonian is itself the
symmetry generator, and finite-time accuracy can introduce genuine energy-time
relations.

## Required Physical Replacement

To obtain a gravitational energy or backreaction theorem, one must add:

1. a finite-size worldline/tetrad action with explicit rotational and boost
   degrees of freedom;
2. a positive Hamiltonian and inertia tensor derived from mass, size, and
   internal stress energy;
3. a normalizable finite-energy reference state and its preparation protocol;
4. a local coupling to the Lorentzian Bunch-Davies static-patch net;
5. finite-time orientation tracking and recovery under the same dynamics;
6. a stress-energy and gravitational backreaction bound;
7. the regulated `SO(1,d)` constraint and its Type-II trace.

Only after these inputs are fixed can the reference energy be optimized and
compared with horizon backreaction.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy covariant-observer-energy-no-go
PYTHONPATH=. python3 -m unittest tests.test_covariant_observer_energy_no_go
```
