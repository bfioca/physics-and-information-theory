# Gravitational Reference-Frame Discriminator

Status: current-literature comparison and paper-positioning gate

Reviewed through: 2026-06-07

## Question

Can a clock or rotationally scalar observer degree of freedom define the full
static-patch observer algebra, or must the observer carry nontrivial charge
under the spatial/de Sitter isometry group?

The regulated result in this repository is:

```text
a rotationally scalar bath or clock cannot supply missing orientation data;
for a spin-L probe the full-orientation relative-entropy deficit is log(2L+1),
and screen-factored recovery has worst-case error at least 1/2.
```

The result survives symmetry-preserving interactions and the Type-II
continuous-core clock extension. It is a statement about normal probe states in
a KMS representation; the invariant KMS background itself has zero loss.

## Comparison With Live Constructions

### G-Framed Crossed Products

Ahmad, Chemissany, Klinger, and Leigh explicitly require a reference frame to
transform commensurately with the system symmetry and organize inequivalent
choices in a `G`-framed algebra:
[arXiv:2405.13884](https://arxiv.org/abs/2405.13884).

The scalar-bath no-go is consistent with that principle and adds a finite
quantitative corollary. A reference carrying the trivial `SU(2)` representation
cannot remove the `log(2L+1)` deficit. To evade it, the frame must carry
nontrivial rotation charge, break the symmetry, or change the representation
multiplicities.

### Covariant de Sitter Observers

Chen and Xu introduce a covariant observer with quantum reference frame
`L^2(SO(1,d))`, impose the full de Sitter constraints, and obtain an averaged
Type-II observer algebra over fluctuating static patches:
[arXiv:2511.00622v2](https://arxiv.org/abs/2511.00622v2).
The current arXiv version is v2, revised February 10, 2026.

This construction evades the no-go by design because the observer carries the
full nontrivial isometry representation. The regulator here instead predicts a
failure mode for any truncation that keeps only a time clock while treating
orientation degrees as scalar: spin multiplets remain operationally incomplete
with the stated recovery and entropy penalties.

### Observer-Dependent Entropy And Entangled Clocks

De Vuyst, Eccles, Hoehn, and Kirklin allow multiple clocks, degenerate spectra,
and arbitrary clock-field entanglement, finding observer-dependent Type-II
entropies and nonzero corrections:
[arXiv:2412.15502v3](https://arxiv.org/abs/2412.15502v3).

Entanglement alone does not evade the present obstruction if every added clock
is rotationally scalar. The representation carried by the reference, not only
its entanglement or energy fluctuations, decides whether angular information is
available. A charged rotational reference lies outside the no-go hypothesis.

### Physical Clocks Without External Clock Systems

Chen and Penington obtain Type-`II_infinity` gravitational algebras from
out-of-equilibrium physical clocks such as an inflaton or evaporating black
hole, without an external clock system:
[arXiv:2406.02116v2](https://arxiv.org/abs/2406.02116v2).

The scalar-bath theorem does not rule out these constructions. It asks an
additional question: does the physical clock or background also select/carry a
spatial orientation frame? If it is rotationally scalar and the symmetry is
unbroken, it can solve the time constraint without completing the angular
observer algebra.

## Paper-Worthy Claim Boundary

The qualitative statement that a reference must transform under the symmetry
is already known. The Type-III and Type-II factor mechanisms are also standard.
The candidate contribution is the combined quantitative theorem in a controlled
regulator:

1. time, axial, and full-rotation reference loss give distinct algebras;
2. full orientation loss has retained fraction `3/(4L^2+8L+3)`;
3. the missing-orientation probe entropy is `log(2L+1)`;
4. every decoder through the frame-blind record has error at least `1/2`;
5. these statements survive rotationally invariant bath interactions and the
   Type-II continuous core;
6. a scalar clock cannot evade them, while a covariant group-valued observer
   falls outside the no-go hypothesis.

This becomes a physics paper only after the same bound is proved inside a named
gravitational observer construction, or after a covariant charged-reference
regulator is shown to saturate and remove the deficit.

## Completed Baseline And Next Calculation

The finite charged auxiliary block has now been constructed:

```text
V_L^* tensor C^{2L+1}
```

It contains an exact `d=2L+1` singlet multiplicity code. The audit shows that
this is not yet the desired treatment: its encoder is noncovariant from a
charged input, its exact decoder reads a pre-encoded trivial multiplicity
register, and the KMS/core factor is a spectator.

The next calculation must define two genuinely matched channels on the same
angular/KMS net:

```text
control:   rho_S tensor eta_scalar, then symmetry reduction,
treatment: rho_S tensor eta_charged, then the same symmetry reduction.
```

Allowed encoders and decoders must obey the same covariance constraints. The
target is the optimal recovery error as a function of reference representation,
dimension, charge variance, and energy, followed by the analogous calculation
for a regulated `SO(1,d)` observer. Only that result would convert the current
obstruction into a direct model-selection theorem for covariant observers.

The axial `U(1)` version is now solved as a control calculation: a fixed
prepared reference followed by joint twirling and sector decoding gives an
exact triangular coherence channel, and the optimal reference for one selected
gap is a sine profile with `Theta((L/N)^2)` error. The remaining mismatch is
therefore geometric: derive the rotation-reference Hamiltonian and energy cost
inside the same physical KMS net, then extend the channel to the full
`SO(1,d)` observer constraints.

The first full-rotation calculation is also complete and is a no-go: one
irreducible spin-`J` reference remains multiplicity-free with `V_L`, so the
joint twirl is entanglement-breaking and full quantum recovery has normalized
diamond error at least `1-1/(2L+1)`, independent of `J`. A gravitational frame
cannot be modeled as merely a larger coherent spin; the next treatment must use
reducible group-valued reference content with controlled multiplicities.

That reducible treatment is now explicit. For a general finite rotation
reference, the largest joint irrep multiplicity gives a diamond-error lower
bound, and no finite prepared reference gives exact deterministic recovery. An
integer-spin Peter-Weyl cutoff, interpreted as an `SO(3)` or center-blind
`SU(2)` orientation reference, supplies a covariant measurement-and-correction
decoder whose tensor-rank errors vanish for a fixed target as the cutoff grows.
Its mean left Casimir is `3J(J+2)/5`.

The same-target redshifted comparison is now also explicit. On the hard-energy spin
`L_delta=Theta(sqrt(R/delta))`, the clock-only fixed point has exact optimal
error `1-1/(2L_delta+1)^2`. The Peter-Weyl decoder reaches error at most
`epsilon` for the sufficient cutoff
`J=ceil[3(2L_delta+1)^2/(8 epsilon)]`. If its compact orientation dynamics are
modeled by the declared rotor `H_ref=C_left/(2I)`, the sufficient mean-energy
cost scales as `R^2/(I epsilon^2 delta^2)`.

The remaining gravitational discriminator is therefore sharper and local: does
a named static-patch observer derive the rotor inertia, Hamiltonian, and
multiplicities with this cost, a softer cost, or a backreaction cutoff, and what
recovery law results after the full `SO(1,d)` constraints? The representation
cutoff and inertia can no longer be chosen by hand if the result is to count as
gravitational physics.

The Chen-Xu v2 action audit sharpens this into an exact identifiability no-go.
Their `dS_2` model supplies conserved isometry charges and a worldline coupling;
the higher-dimensional orthogonal frame is specified kinematically on
`L^2(SO(1,d))`, without a rotational kinetic term or frame inertia. For the
compact Peter-Weyl treatment here, replacing `H=a_J C_left` by any other positive
coefficient leaves the token and recovery channel unchanged while rescaling its
ground-subtracted energy. Therefore neither the `delta^-2` law nor any alternative
energy exponent follows from covariance and recovery alone.

This is not the final discriminator: the rescaling fact is elementary and the
different Hamiltonians are different dynamical models. Its value is to rule out
closing the gravitational gate with kinematics. The next calculation must
upgrade the selected finite-size EFT to a matter-derived local interaction,
lifetime analysis, and controlled backreaction constraint.

The compact part of that calculation is now explicit as an EFT. A marked
spherical-top action gives `H_rot=C_left/(2I)` after stipulating the constitutive
law `I=kappa m a^2`. Requiring mean rotational excitation below a fraction of
rest energy and imposing a declared local compactness margin bounds the mean
Casimir. Markov truncation and gentle projection transfer the exact finite
Peter-Weyl multiplicity obstruction to every admissible state on `L^2(SO(3))`,
forcing every decoder's append-and-twirl recovery error toward one on the growing
hard-energy horizon spin sector. This is stronger than the earlier fixed-
inertia cost estimate because it handles high-spin tails rather than assuming a
physical representation cutoff.

The result still does not finish the gravitational discriminator. The inertia
law and compactness margin are EFT hypotheses rather than consequences of a
rotating Einstein-matter solution. A conditional finite-time bridge now exists:
collective isotropic rotation diffusion converges to Haar append-and-twirl with
a representation-independent diamond correction, and the correction is `O(1/L)`
for `gamma T=(1/2)log(2L+1)`. But the noise is collective in angular charge and
has not been derived from a spatially local coupling to the Bunch-Davies net.
The diffusion rate, bath record, noncompact boost/clock sector, and Type-II trace
remain outside the gravitational model.

The required common mode now has a quantitative falsification test. In an axial
two-charge Markov reduction, correlation coefficient `c` produces channel
mismatch at least `[1-exp(-2 gamma T Delta^2(1-c))]/2` for axial charge gap
`Delta`. Keeping that contribution at `O(1/L)` along the logarithmic schedule
requires `1-c=O(1/(Delta^2 L log L))`. This is not a generic locality no-go: a local massless or
critical bath can have long-range correlations. The discriminator now asks
whether the covariance derived from the named Bunch-Davies/worldtube coupling
passes this scaling test together with lifetime and backreaction constraints.

For one named local surrogate, it does not pass at fixed separation. Two
identical equal-redshift axial zero-Bohr couplings to the conformal Bunch-Davies
scalar have normalized cross coefficient
`c_0(y)=y/sinh(y)`, `y=d_H/R`. The `O(1/L)` covariance allocation therefore
forces `d_H/R=O(1/sqrt(L log L))` for fixed charge gap. On a shell at horizon
distance `rho`, the allowed angle is
`O((rho/R)/sqrt(L log L))`. This is a scalar pure-dephasing result, not the
three-axis spherical-top torque; finite switching, optical smearing, and the
proper-time rate remain open.

The conformal scalar collar calculation supplies a hard finite-wall field-
energy comparison: redshift permits integer-spin sectors through
`L_delta=Theta(sqrt(R/delta))`, a pure coherent directional token over them has
`SO(3)` relative entropy of frameness `log(R/delta)+O(1)`, and the same-target compact
reference theorem quantifies the constructive cost of retaining the spin. The
decisive next step is the named gravitational coupling and Type-II trace.
