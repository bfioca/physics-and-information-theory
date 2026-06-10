# Finite-Size Static-Patch Rotation Observer

Status: compact-`SO(3)` worldtube EFT, mean-energy-constrained all-state
Peter-Weyl obstruction, and a protocol-specific spectral threshold; local
interaction, rotating GR completion, boosts, and Type-II entropy remain open

## Physical Completion

The previous Peter-Weyl theorem specified a representation, token, and decoder,
but assigned the rotor Hamiltonian by hand. The energy-identifiability no-go
proved that covariance could not fill that gap. This document selects one
physical completion.

Let an observer carry a marked spherical top of proper radius `a`, rest energy
`m`, and orientation `Q(tau) in SO(3)`. In its local proper time use the
worldtube effective action

```text
S_obs = integral d tau
  [-m + I |Q^{-1} D_tau Q|^2/2],
I = kappa m a^2,
0 < kappa <= 2/3.
```

The upper value `2/3` is the support bound for an isotropic inertia tensor:
if positive rest-energy density lies inside radius `a`, then
`3I=Tr(I_tensor)<=2ma^2`. A thin spherical shell saturates it. Marks or internal
degrees make the otherwise spherical body an orientation reference without
changing the leading inertia model.

Canonical quantization gives configuration Hilbert space `L^2(SO(3))` and

```text
H_rot=C_left/(2I).
```

Thus the canonical cutoff-`J` Peter-Weyl token has

```text
<H_rot>=3J(J+2)/(10 kappa m a^2).
```

The action selects the rotor dynamics, while `I=kappa m a^2` is a stipulated
constitutive law constrained by the spherical support bound. This is a compact
rest-frame EFT ansatz, not a matter-derived worldtube stress tensor or a positive
Hamiltonian for the noncompact de Sitter group.

## Mean-Casimir Capacity

Work in units `c=hbar=1`, so `[G]=length^2`. For an arbitrary prepared rotor
state `eta`, write

```text
Cbar=Tr(eta C_left),
E_rot=Cbar/(2 kappa m a^2).
```

Impose the declared mean-energy conditions

```text
E_rot/m <= zeta <= 1,
2G(m+E_rot)/a <= chi < 1.
```

The second line is a local compactness hypothesis, not a general theorem for
rotating nonspherical quantum matter. Maximizing `Cbar=2 kappa m a^2 E_rot`
over these two inequalities gives

```text
Cbar
 <= kappa chi^2 zeta a^4
    /[2 G^2(1+zeta)^2].                       (1)
```

This is a mean-Casimir bound on the full `L^2(SO(3))` Hilbert space. It does not
create a hard representation cutoff and allows high-spin tails.

For comparison, the canonical cutoff-`J` token has

```text
<C_left>=3J(J+2)/5.
```

Substitution in (1) excludes canonical tokens above

```text
J(J+2)
 <= 5 kappa chi^2 zeta a^4
    /[6 G^2(1+zeta)^2].                       (2)
```

Equation (2) is a statement about that token family, not a physical truncation
of the rotor.

## All-State Any-Decoder Obstruction

Let `P_J` project the reference onto Peter-Weyl spins `j<=J`. Since the first
Casimir eigenvalue outside this subspace is `(J+1)(J+2)`, Markov's inequality
gives

```text
q_J=Tr[(1-P_J)eta]
 <= Cbar/[(J+1)(J+2)].                        (3)
```

When `q_J<1`, the normalized projected state
`eta_J=P_J eta P_J/(1-q_J)` is within trace distance `sqrt(q_J)` of `eta` by
the fidelity/gentle-projection bound. Candidates with `q_J=1` give no positive
transferred lower bound and are discarded by clipping. The append-and-twirl
channel is contractive in this distance.

The Peter-Weyl representation through `J` has total right-regular multiplicity

```text
sum_(j=0)^J (2j+1)=(J+1)^2.
```

For a target spin `L`, dimension `d=2L+1`, the exact finite-multiplicity theorem
and a triangle inequality therefore imply, for every prepared state satisfying
`Tr(eta C_left)<=Cbar` and every deterministic CPTP decoder after the fixed
append-and-twirl channel,

```text
epsilon_opt(eta)
 >= max_(J>=0) max{0,
      1-(J+1)^2/d
       -sqrt[Cbar/((J+1)(J+2))]}.             (4)
```

Here `epsilon=(1/2)||D N_eta-identity_d||_diamond`. Terms for which the Markov
bound exceeds one are simply uninformative and are removed by clipping at zero.

When the continuous optimizer lies above the `J=0` boundary,
`J+1` is of order `(sqrt(Cbar)d)^(1/3)`. Uniformly over both regimes,

```text
epsilon_opt
 >= 1-O[1/d+(Cbar/d)^(1/3)].                  (5)
```

Thus every fixed finite observer satisfying (1) has error tending to one on the
hard-energy static-patch sector

```text
L_delta=Theta(sqrt(R/delta)).
```

This result covers high-spin tails and needs no hard support postulate. It is
universal over prepared rotor states and deterministic decoders only after the
specified append-and-twirl channel. It does not cover pre-correlated relational
encoders, postselection, different reference representations or hardware, or
general finite-time evolution during the protocol. The conditional collective
Markov extension is treated separately in `finite_time_rotation_diffusion.md`.

## Collar-Following Observer

The redshifted target states live in a collar whose fixed tortoise width shrinks
in proper size with the stretched-horizon distance

```text
rho_delta=2R asin sqrt[delta/(2R)]
         =sqrt(2R delta)+o(sqrt(R delta)).
```

To model a local apparatus that follows this collar, impose

```text
a_delta=alpha rho_delta,
0 < alpha <= 1.
```

Then (1) gives `Cbar=O(a_delta^4/G^2)=O(R^2 delta^2/G^2)`, and (4) again tends
to one. The available mean rotational asymmetry now decreases while the target
dimension grows.

There is also a separate protocol-specific consequence. To certify that every
occupied sector of the repository's canonical hard-cutoff token respects the
same excitation and compactness limits, impose the stronger spectral condition

```text
j(j+1)
 <= kappa chi^2 zeta a^4
    /[2 G^2(1+zeta)^2].                       (6)
```

The existing measure-and-correct channel is certified at error `epsilon` by a
cutoff

```text
J_cert=O(R/(epsilon delta)).
```

Equating this sufficient cutoff with the spectral bound (6) gives the leading
feasibility scale

```text
delta_protocol = Theta(sqrt(G/epsilon)),
rho_protocol   = Theta(sqrt(R sqrt(G)) epsilon^(-1/4)).
```

The constants depend explicitly on `alpha,kappa,chi,zeta` and on the collar
energy coefficient. This scale can be much larger than the Planck length for a
large de Sitter radius. Crossing it means the repository's explicit decoder no
longer has a compactness-compatible certified cutoff. It does not rule out a
more efficient reference protocol.

## Conditional Access-Capacity Fork

The all-angular static-patch theorem already supplies the complementary fixed-
interior estimate

```text
||1_(0,B) P_[0,E^2](h_L)||
 <= E R sinh(B/R)/sqrt[L(L+1)].
```

At `L=L_delta`, a fixed interior worldtube therefore has low-energy overlap at
most `O(sqrt(delta/R))` with the hard angular target. Turning this geometric
overlap into a finite-time channel bound requires a declared local interaction,
but it identifies the physical fork:

1. keep the observer at fixed interior size, and its direct access to the
   moving collar vanishes;
2. move the observer with the collar, and its proper size, inertia, and
   gravitational reference capacity shrink.

This is a conditional access-capacity fork, not an exhaustive physical
dichotomy. The fixed-interior estimate is not yet a finite-time channel theorem,
and the collar-following branch rests on the declared compactness hypothesis.

## Literature And Scope

The group configuration and quantization of a spherical top on `SO(3)` are
standard; see [Khatua and Ganesh, arXiv:2202.04096](https://arxiv.org/abs/2202.04096).
Finite rotational-reference accuracy and size tradeoffs are developed by
[Peres and Scudo](https://arxiv.org/abs/quant-ph/0103149),
[Bagan, Baig, and Munoz-Tapia](https://arxiv.org/abs/quant-ph/0106014), and
[Miyadera and Loveridge](https://arxiv.org/abs/2006.14247). Related limitations
from finite continuous-symmetry resources and reference degradation appear in
[Faist et al.](https://arxiv.org/abs/1902.07714) and
[Bartlett et al.](https://arxiv.org/abs/quant-ph/0602069).

Compactness bounds require matter and symmetry assumptions. Examples include
[Andreasson](https://arxiv.org/abs/gr-qc/0702137) for spherical anisotropic
matter and [Mak, Dobson, and Harko](https://arxiv.org/abs/gr-qc/0104031) with a
positive cosmological constant. Those theorems do not directly prove the
declared rotating quantum compactness condition above.
[Dain's angular-momentum/size inequalities](https://arxiv.org/abs/1305.6645)
are adjacent but concern net angular momentum under restricted axisymmetric GR
hypotheses, whereas the present token may have zero mean charge and nonzero
Casimir fluctuations.

Not established here:

1. a rotating Einstein-matter or semiclassical-gravity solution for the top;
2. a local field-top interaction or bounded-time decoder;
3. preparation work, stress-energy fluctuations, binding, support apparatus,
   or lifetime;
4. the noncompact boost sector and full `SO(1,d)` group averaging;
5. extension through the gravitational crossed product, a finite Type-II trace,
   or generalized entropy.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy finite-size-static-patch-observer
PYTHONPATH=. python3 -m unittest tests.test_finite_size_static_patch_observer
```
