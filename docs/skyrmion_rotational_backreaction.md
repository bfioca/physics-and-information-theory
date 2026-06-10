# Spherical Collective Rotational Backreaction

Status: authenticated conditional gravity-to-Casimir-to-risk theorem in the
fixed-field leading collective sector; rotating Einstein-Skyrme completion open.

## Constraint Elimination

Let the spherical areal metric factor be

```text
A(x)=N(x)[1-q(x)],  N(x)=1-lambda x^2,
sup q<=beta<1.
```

For one fixed Skyrmion profile, positivity of the static energy terms gives

```text
c_M[A]>=(1-beta)c_M[N].                              (1)
```

The collective inertia density contains terms proportional to `1/A` and terms
independent of `A`. Therefore

```text
c_I[A]<=c_I[N]/(1-beta).                             (2)
```

For a leading collective state with `Cbar=<J^2>`, the bulk wall constraint must
then obey

```text
q_w >= Xi(1-beta)/(x_w N_w)
       [c_M/e^2 + e^2 Cbar/(2c_I)],
Xi=2G/(R^2 lambda).                                  (3)
```

The rest term scales as `e^-2`, while the rotational term scales as
`e^2 Cbar`. Minimizing over `e^2` gives the coupling-independent necessary
condition

```text
Cbar <= [beta x_w N_w/(Xi(1-beta))]^2 c_I/(2c_M).    (4)
```

Combining (4) with the all-state global orientation theorem gives

```text
R_ref >= 1/(16 Cbar_max+8).                          (5)
```

Unlike the earlier fixed-profile result, this route does not impose a separate
compactness number and slow-rotation budget and then eliminate `e`. It prices
the leading collective rotational energy directly in the radial gravitational
constraint. Slow rotation remains necessary to justify truncation to that
collective Hamiltonian.

## Authenticated Default

The audit pins the authenticated AU.3b artifact and compresses its exact
endpoints outward to six decimal places:

```text
c_M,bulk >= 33.833816,
c_I,bulk <= 48.390986.
```

At

```text
beta=1/2,  x_w=4,  lambda=1/400,  R^2/G=10^6,
```

equations (4)-(5) give

```text
<J^2> <= 16476538.109682929,
R_ref >= 3.79327245124592e-9.                        (6)
```

The number is weaker than the existing proxy-plus-slow-rotation risk floor.
Its value is structural: it is the first authenticated chain in this project

```text
local radial gravity budget
  -> mean rotational Casimir capacity
  -> global orientation Bayes-risk floor,
```

with the matter mass and inertia taken from the same certified profile.

## Claim Boundary

This is a necessary condition within a fixed-field, spherical radial-metric,
leading collective-rotor model. The membrane is excluded from both mass and
inertia. The theorem does not solve the lapse equation, control anisotropic
rotation stress, construct the collective projector, bound higher-order
rotation, or solve a rotating Einstein-Skyrme system. It therefore cannot yet
be advertised as the universal observer theorem. Its next falsification test is
whether lapse, nonspherical stress, and collective-projection corrections leave
an open parameter interval and a nontrivial risk floor.

## Reproduction

```bash
python experiments/skyrmion_rotational_backreaction_audit.py
python -m pytest -q tests/test_spherical_rotational_backreaction.py \
  tests/test_skyrmion_rotational_backreaction_audit.py
```

Artifact:

```text
experiments/skyrmion_rotational_backreaction_exact_certificate.json
SHA256 7bfb5119a89da2bffbca47a5794e7bbf756f5bc4ea1d1b51877b216ac1a33433
```
