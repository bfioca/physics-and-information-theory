# Supported Skyrmion Collective Spectral Floor

Status: analytic profile-uniform theorem for the hard-supported hedgehog
collective family; full field-theory sector completeness and band projection
remain open

## Theorem

For the massive `SU(2)` Skyrme action in the static patch, restrict to
hard-supported hedgehog profiles inside dimensionless radius `x_w`, with

```text
N(x)=1-lambda x^2,  N_w=N(x_w)>0.
```

Let `M[F]` be the static Killing energy, `I[F]` the collective orientation
inertia, and `a=x_w/(e f_pi)` the areal support radius. Every admissible profile
obeys

```text
I[F] <= kappa_w M[F] a^2,
kappa_w=4/(3N_w).                                      (1)
```

For the adiabatic collective Hamiltonian at spin `j`, arbitrary relaxation of
the supported hedgehog profile therefore gives

```text
E_j = inf_F {M[F]+j(j+1)/(2I[F])}
    >= sqrt[3N_w j(j+1)/2]/a.                          (2)
```

Equation (2) is uniform over the profile family. It is not a fixed-profile
rigid-rotor estimate and does not assume that the certified static profile
remains unchanged as spin grows.

## Density Proof

Write `m(x)=4 pi E(x)` for the dimensionless mass density and

```text
i(x)=(2pi/3)x^2 sin^2(F)
 [1/N+4F'^2+4sin^2(F)/(Nx^2)]
```

for the inertia density. The positive terms in `m(x)` include

```text
pi sin^2(F),
4pi N sin^2(F)F'^2,
2pi sin^4(F)/x^2.
```

Since `x^2/N(x)<=x_w^2/N_w`, the corresponding three inertia terms are bounded
by respectively `2/3`, `2/3`, and `4/3` times
`(x_w^2/N_w)` times those mass terms. All omitted mass terms are nonnegative.
Thus

```text
i(x) <= [4x_w^2/(3N_w)]m(x).
```

Integration and the exact physical scalings

```text
M=c_M f_pi/e,
I=c_I/(e^3 f_pi),
a=x_w/(e f_pi)
```

give (1). A positive spherically symmetric wall mass can be included in `M`
and only weakens the bound.

For each profile, (1) and AM-GM give

```text
M+j(j+1)/(2I)
 >= M+j(j+1)/(2kappa_w M a^2)
 >= sqrt[2j(j+1)/kappa_w]/a,
```

which is (2).

## Global Reference Consequence

Define

```text
s_w=sqrt(3N_w/2)/a.
```

Because `sqrt[j(j+1)]>=j`, the sector floor implies `E_j>=s_w j`. The
rotational partition function is therefore finite for every `beta>0`. With
`x=exp(-beta s_w)`, explicit upper bounds are

```text
Z_integer(beta) <= (1+6x+x^2)/(1-x)^3,
Z_projective(beta) <= 4sqrt(x)(1+x)/(1-x)^3.            (3)
```

The second line is the fermionic Finkelstein-Rubinstein sector
`j=1/2,3/2,...`. For any collective-band state with mean total Killing energy
at most `E`, the global asymmetry theorem gives

```text
A_SO3 <= beta E+log Z_upper(beta),
R_ref >= 6/[e pi^(5/3)]
         exp[-2(beta E+log Z_upper(beta))/3].           (4)
```

This is all-state and tail robust. For the first sector above a cutoff, Markov
also gives `Pr(j>=j_*)<=E/E_floor(j_*)`.

## Relation To The Omega Expansion

For a fixed profile, the two- and four-derivative Skyrme action is exactly
quadratic in collective angular velocity:

```text
L[F,Omega]=-M[F]+I[F]Omega^2/2.
```

An effective `Omega^4` term appears after the profile or wall is allowed to
relax. If `K` is the supported static Hessian and `grad I` the inertia gradient,
formal stable perturbation theory gives

```text
J_4=(1/2)<grad I,K^-1 grad I> >= 0,
H(J)=M+J^2/(2I)-J_4 J^4/(4I^4)+...
```

Thus the undeformed rigid rotor generally overestimates the sector energy at
quartic order. Equation (2) remains valid without computing `J_4`, because it
optimizes over all supported hedgehog profiles before applying the density
bound. A controlled `Omega^4` coefficient is still needed for a precision
low-spin expansion, not for the present high-spin coercivity theorem.

## Numerical Baseline

For `mu=1`, `lambda=0.0025`, and `x_w=4`, `N_w=0.96` and
`kappa_w=1.388888...`. The existing supported profile has

```text
M_total=48.95760325,
I=34.26620155,
I/(M_total a^2)=0.04374474 < kappa_w.
```

The large slack is not used as a universal improvement: (1) is the
profile-independent analytic constant.

## Claim Boundary

The theorem covers the hard-supported hedgehog collective-coordinate family,
including arbitrary radial profile relaxation. It assumes the standard
adiabatic sector energy `M[F]+j(j+1)/(2I[F])`. It does not prove that the
collective band exhausts the full Skyrme field-theory spin sectors, bound
noncollective rotating modes, control Born-Oppenheimer or band-projection
errors, prove coherent access to the right/isospin multiplicity, or derive the
finite-coupling readout, wall completion, lifetime, and metric response from
one action. A marked or rotating wall would also contribute additional
orientation inertia and must be included separately.

The next decisive theorem is therefore a collective-band completeness or
spectral-comparison bound, not another fixed-profile cutoff calculation.

## Reproduction

```bash
PYTHONPATH=. python -m qgtoy \
  supported-skyrmion-collective-spectral-floor
python -m pytest -q tests/test_supported_skyrmion_collective_spectral_floor.py
```

Artifacts:

- `qgtoy/supported_skyrmion_collective_spectral_floor.py`
- `tests/test_supported_skyrmion_collective_spectral_floor.py`
