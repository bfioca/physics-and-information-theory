# Finite-Time Rotation Diffusion

Status: exact finite-time `SO(3)` heat-kernel channel and representation-
independent diamond convergence to Haar append-and-twirl; spatially local bath
derivation and gravitational backreaction remain open

## Proper-Time Open-System Model

Let the hard angular target and marked spherical-top reference carry collective
rotation generators

```text
Q_a=J_a^(target)+J_a^(rotor,left),  a=1,2,3.
```

In the interaction picture with respect to the free target and rotor
Hamiltonians, assume

```text
[H_target+H_rot,Q_a]=0,
```

as holds for a rotationally invariant target and the Casimir spherical top, or
specify a toggling control that makes the interaction-picture `Q_a` constant.
Then impose isotropic proper-time diffusion

```text
d rho/d tau=-gamma sum_a [Q_a,[Q_a,rho]],       (1)
```

equivalently the GKSL operators `L_a=sqrt(2 gamma)Q_a`. A Stratonovich
stochastic-Hamiltonian realization is

```text
H_noise(tau)=sum_a xi_a(tau)Q_a,
E[xi_a(tau)xi_b(tau')]
 =2 gamma delta_ab delta(tau-tau').             (2)
```

This is a standard twirling semigroup: Brownian convolution on the rotation
group produces a random-unitary quantum dynamical semigroup. See
[Aniello, Kossakowski, Marmo, and Ventriglia](https://arxiv.org/abs/1002.3507)
and the broader covariant-semigroup framework reviewed by
[Holevo](https://arxiv.org/abs/quant-ph/9701037).

The common generator `Q_a` is a substantive assumption. Ordinary environmental
torque on the top produces rotor-only rotational decoherence, friction, and
diffusion, as in
[Stickler, Schrinski, and Hornberger](https://arxiv.org/abs/1712.05163) and
[Papendell, Stickler, and Hornberger](https://arxiv.org/abs/1712.05596). It does
not automatically rotate the target by the same stochastic trajectory. The
channel (1) requires a perfectly correlated common-mode orientation fluctuation,
or an effective stochastic frame, acting with equal strength on target and
reference. For a spatial bath kernel this is the rank-one/common-mode limit;
short-range local noise generally produces a different dissipator.

Equation (1) is time-local/Markovian in observer proper time but collective in
the target angular charge. It assumes an isotropic white-noise model. It is not yet a
derivation from a spatially local coupling to the static-patch field current.
Phase tracking alone is not a substitute for the commutator/control hypothesis
above. The Brownian trajectory, bath output, and bath purification are assumed
inaccessible. If the trajectory is measured, feedback can undo the common
random rotation and the no-go does not apply in this form.

The exact white-noise model has infinite bandwidth. A finite quantum-bath
derivation would be approximate and would additionally require a finite bath
correlation time, an isotropic zero-frequency spectrum, Lamb-shift control, and
a quantified Davies/Markov error. It must establish a hierarchy such as
`max(a,tau_B)<<T<<min(tau_life,tau_recurrence)` rather than importing (1) as an
exact finite-stress-energy interaction. Passive uncertainty about an unknown
frame is also distinct: averaging that uncertainty is epistemic coarse graining,
not this active discarded-bath dynamics.

## Heat-Kernel Channel

Let `s=gamma T`. The solution after proper time `T` is

```text
N_(eta,T)(rho)=integral_SO3 dg k_s(g)
 [U_L(g)rho U_L(g)^*] tensor [U_R(g)eta U_R(g)^*].       (3)
```

The central heat kernel has Peter-Weyl expansion

```text
k_s(g)=sum_(j>=0)(2j+1)e^[-s j(j+1)] chi_j(g).          (4)
```

At `T=0`, (3) is the identity-starting append channel `rho -> rho tensor eta`.
As `T` tends to infinity, `k_s` tends to the Haar density `1`, so (3) tends to
the exact prepared-reference append-and-twirl channel used by the preceding
recovery theorem.

## Representation-Independent Diamond Bound

For random-unitary channels, the diamond distance is bounded by the `L1`
distance between the probability densities. Haar normalization and
Cauchy-Schwarz give

```text
eta_heat(s)
 :=(1/2)||N_(eta,T)-N_(eta,infinity)||_diamond
 <=(1/2)||k_s-1||_1
 <=(1/2)||k_s-1||_2.                          (5)
```

Character orthogonality yields

```text
||k_s-1||_2^2
 =sum_(j>=1)(2j+1)^2 e^[-2s j(j+1)].          (6)
```

Since `j(j+1)>=2j`, put `q=e^(-4s)` and sum the elementary geometric moments:

```text
eta_heat(s)
 <= min{1,
    (1/2)sqrt[q(9-2q+q^2)/(1-q)^3]}.          (7)
```

This bound is independent of target spin, reference representation, and
reference state. In particular it applies directly to states on the full
`L^2(SO(3))` rotor Hilbert space and does not introduce a hard cutoff. On that
unbounded Hilbert space, the random-unitary formula is the mild heat semigroup;
the double-commutator master equation holds on its natural strong-generator
domain.

## Finite-Time Recovery Obstruction

Let `d=2L+1` and let the prepared rotor state obey
`Tr(eta C_left)<=Cbar`. The Haar theorem gives

```text
epsilon_Haar
 >= max_(J>=0) max{0,
      1-(J+1)^2/d
       -sqrt[Cbar/((J+1)(J+2))]}.             (8)
```

For every deterministic CPTP decoder acting only on the target-plus-rotor
output, without the Brownian record, bath output, or bath purification,
contractivity and the triangle inequality transfer (8) to finite time:

```text
epsilon_T
 >= max{0,epsilon_Haar-eta_heat(gamma T)}.    (9)
```

This is the promised controlled replacement for instantaneous Haar averaging
inside the collective Markov model. It does not yet prove that a local
static-patch measurement implements (1).

## Logarithmic Mixing-Time Consequence

Choose

```text
gamma T=(1/2)log d.
```

Then `q=d^-2`, and (7) implies

```text
eta_heat
 <= 3/[2d(1-d^-2)^(3/2)]
 =O(1/d).                                    (10)
```

Therefore the finite-time correction is of the same order as the Haar deficit
when `Cbar=0`, and is subleading when fixed positive `Cbar` makes the
`d^-1/3` term dominant. On the hard-energy static-patch sector

```text
L_delta=Theta(sqrt(R/delta)),
```

if `gamma` is cutoff independent, a sufficient diffusion-time choice is

```text
T_delta=Theta[gamma^-1 log(R/delta)].         (11)
```

Equation (11) is a conditional sufficient protocol-time upper bound, not a
necessary mixing law or an observable prediction. At fixed finite `T`, (9)
gives the asymptotic floor `1-eta_heat(gamma T)` only when the certified
`eta_heat(gamma T)<1`; it does not force the error itself to one unless
`gamma T` also grows.

## Claim Boundary

Established:

1. an identity-starting strongly continuous collective `SO(3)` diffusion
   semigroup;
2. exact heat-kernel convergence to Haar append-and-twirl;
3. a representation-independent normalized diamond bound;
4. an all-state finite-time recovery lower bound under the mean-Casimir budget;
5. the logarithmic sufficient diffusion-time scaling.

Not established:

1. a spatially local field-current/top interaction producing the white-noise
   kernel and its required target-rotor common mode;
2. a finite-memory, non-Markovian, or energy-exchanging bath treatment;
3. preparation and phase tracking of cross-spin rotor coherences under
   `H_rot=C_left/(2I)`;
4. recovery protocols with access to the Brownian environment record or feedback
   during the diffusion;
5. observer lifetime, stress-energy, horizon displacement, or backreaction;
6. the noncompact boost sector, Type-II observer trace, or generalized entropy.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy finite-time-rotation-diffusion
PYTHONPATH=. python3 -m unittest tests.test_finite_time_rotation_diffusion
```
