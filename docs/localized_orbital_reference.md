# Localized Orbital Reference: Energy, Capacity, And Necessity

Status: analytic all-state theorem for confined spinless nonrelativistic
orbital matter; weak-gravity elimination is a declared compactness proxy, not
a general-relativistic body theorem

## Result

Consider finitely many spinless particles with masses `m_i>0`, total rest mass
`M=sum_i m_i`, and a rotationally invariant configuration domain on which
every `|x_i|<=a`. Work in units `hbar=c=1`. Let a nonnegative,
rotation-invariant orbital energy Hamiltonian obey the quadratic-form inequality

```text
H_ex >= T=sum_i p_i^2/(2m_i) >= 0.
```

The choice of energy zero is part of the premise. `H_ex` is not an arbitrary
ground-subtracted Dirichlet Hamiltonian. If the available Hamiltonian is
`H_gs`, the theorem applies only after exhibiting `Delta>=0` such that
`H_gs+Delta>=T` as quadratic forms; every occurrence of `E_ex` below then
means `E_gs+Delta`. If `H_phys>=T` and
`H_gs=H_phys-E_phys,0`, choosing `Delta=E_phys,0` suffices. A later
gravitational ledger must use one consistent physical energy, including wall
and support costs, without subtracting or restoring the same offset twice.

The total orbital generator `L=sum_i x_i cross p_i` then satisfies, for every
state in the form domain,

```text
<L^2> <= 2 M a^2 <T> <= 2 M a^2 <H_ex>.                 (1)
```

Combining (1) with the all-state/all-POVM global `SO(3)` theorem gives

```text
R_ref >= 1/[32 M a^2 E_ex+8],                           (2)
```

where `E_ex=<H_ex>`. The independent asymmetry/Gibbs floor is obtained by
using

```text
<j> <= [sqrt(1+8 M a^2 E_ex)-1]/2.                     (3)
```

Equations (1)-(3) apply to mixed states, zero-mean states, and states with rare
high-spin tails. Any internal multiplicity on which rotations act trivially is
allowed and does not weaken the risk theorem.

## Heat-Exposure Composition

For isotropic rotational heat exposure
`Gamma=integral gamma(tau)d tau`, the same named matter class obeys

```text
R(T)>=3/4[1-exp(-2Gamma)]
      +exp(-2Gamma)/[32 M a^2 E_ex+8].
```

Under the declared compactness proxy this becomes

```text
R(T)>=3/4[1-exp(-2Gamma)]
      +exp(-2Gamma)/[8+2chi^2 a^4/G^2].
```

The module implements the forward bound, its exact minimum-radius inversion,
and a proper-support-ceiling no-go record. `Gamma` is noise exposure, not time
alone; no universal decoherence rate is assumed.

## Quadratic-Form Proof

For a pure form-domain wavefunction, including a rotation-trivial internal
Hilbert space, pointwise mass-weighted Cauchy-Schwarz gives

```text
|sum_i x_i cross grad_i psi|^2
 <= (sum_i m_i |x_i|^2)(sum_i |grad_i psi|^2/m_i)
 <= M a^2 (sum_i |grad_i psi|^2/m_i).
```

Integration yields (1). Convexity extends it to mixed states. No polarization,
local unbiasedness, fixed irrep, particle-number bound, or semiclassical state
assumption is used.

For every integer cutoff `J`, Markov's inequality also gives the explicit tail
control

```text
Pr(j>=J+1) <= 2 M a^2 E_ex/[(J+1)(J+2)].               (4)
```

Thus a vanishing probability assigned to arbitrarily remote spin cannot evade
the result.

## Spectral Form

The physical content of (1) is a growing rotational-sector energy floor. More
generally, write a rotationally invariant Hamiltonian as

```text
H=direct_sum_j identity_(V_j) tensor H_j,
epsilon_j=inf spectrum(H_j).
```

For spin weights `p_j` and arbitrary rotation-trivial multiplicities,

```text
A_SO3(rho) <= H(p)+2 sum_j p_j log(2j+1).
```

If

```text
Z_H(beta)=sum_j (2j+1)^2 exp(-beta epsilon_j)<infinity,
```

relative-entropy positivity against
`q_beta,j proportional to (2j+1)^2 exp(-beta epsilon_j)` gives

```text
A_SO3(rho) <= beta E+log Z_H(beta),
R_ref >= 6/[e pi^(5/3)] exp[-(2/3)(beta E+log Z_H(beta))].  (5)
```

The infimum over admissible `beta>0` is allowed. In particular,
`H_ex>=alpha L^2` gives

```text
R_ref >= alpha/(16E+8alpha).                            (6)
```

If `epsilon_>J=inf_(j>J) epsilon_j>0`, the cutoff transfer gives

```text
R_ref >= [sin^2(pi/(2J+3))-sqrt(min(1,E/epsilon_>J))]_+. (7)
```

The projective half-integer version replaces the cutoff term by
`sin^2[pi/(2J+4)]`.

## Why A Spectral Premise Is Necessary

Covariance, positivity, localization vocabulary, and finite mean energy do not
alone imply a reference-capacity bound. On `L^2(SO(3))`, let `P_j` be the
Peter-Weyl spin projector and fix

```text
H_bad=sum_(j>=0) (1-exp(-j)) P_j,       0<=H_bad<1.     (8)
```

The normalized Peter-Weyl kernel through spin `J` has energy below one and
achievable chordal risk

```text
R_J={4J(J+2)+3}/{4(J+1)(2J+1)(2J+3)/3}=O(1/J).         (9)
```

Hence `R_J->0` at uniformly bounded energy. A universal observer theorem must
derive growing `epsilon_j` from its physical matter action; rotational
covariance does not supply it.

## Declared Weak-Gravity Corollary

If the same body is assigned the explicit proxy

```text
2G(M+E_ex)/a <= chi < 1,
```

then `M E_ex<=(M+E_ex)^2/4` and (1) imply

```text
<L^2> <= chi^2 a^4/(8G^2),
R_ref >= 1/[8+2 chi^2 a^4/G^2].                        (10)
```

This elimination is useful because it no longer assumes a rigid spherical-top
inertia law. It is still not a theorem of Einstein gravity: the compactness
proxy, hard support, and positive excitation Hamiltonian are assumptions.

## Claim Boundary

The theorem covers spinless nonrelativistic orbital matter, positive masses,
hard radius support, and rotation-trivial internal labels. It does not cover
intrinsic spin, relativistic or massless fields, negative interaction energy,
soft localization tails, pre-correlated recovery memories, nontrivially
rotating light species, a local finite-time readout, support stress, lifetime,
or metric response. Large Casimir is used only as a necessary capacity budget;
it is never asserted to be sufficient reference quality.

This theorem is therefore a genuine UO.2Q closure for a named matter class,
not yet the full static-patch observer tradeoff. The next physics step is to
derive an analogous uniform sector floor for the supported Skyrmion action,
including noncollective modes and collective-coordinate errors, and then join
it to UO.3/UO.4 using the same local interaction.

## Reproduction

```bash
python -m pytest -q tests/test_localized_orbital_reference.py \
  tests/test_rotational_spectral_capacity.py
```

Artifacts:

- `qgtoy/localized_orbital_reference.py`
- `qgtoy/rotational_spectral_capacity.py`
- `tests/test_localized_orbital_reference.py`
- `tests/test_rotational_spectral_capacity.py`
