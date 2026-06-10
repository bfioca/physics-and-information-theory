# Conditional Fixed-Profile Skyrmion Observer-Capacity Proposition

Status: conditional fixed-profile proxy-budget elimination proposition;
numerical profile constants are currently floating diagnostics pending their
sharp interval substitution

## Result

Fix the dimensionless profile data `(mu, lambda, x_w)` and its total mass and
rotor inertia constants `(c_M,c_I)`. The same object then has

```text
M = c_M/(e^2 R sqrt(lambda)),
r_w = x_w R sqrt(lambda),
I = c_I R sqrt(lambda)/e^2.                         (1)
```

Impose a compactness budget `C<=C_*` and a rigid-rotation budget
`epsilon_rot<=s_*` at the largest occupied physical spin `K`. Eliminating the
Skyrme coupling gives

```text
C epsilon_rot
 = 2G c_M sqrt[K(K+1)]/(c_I x_w lambda R^2),

sqrt[K(K+1)]
 <= C_* s_* c_I x_w lambda R^2/(2G c_M).            (2)
```

Equation (2) is independent of the `e`/`f_pi` co-scaling that preserves the
fixed dimensionless profile. It therefore gives a finite uniform upper bound
`J_max` on the support of an exactly hard-supported projective state, where
`K=J+1/2` in the `B=1` sector.

The sharp hard-cutoff fusion theorem then yields

```text
R_frame >= sin^2[pi/(2(J_max+2))] > 0.               (3)
```

Thus, at fixed profile, `R^2/G`, compactness-proxy margin, and
maximum-occupied-spin slow-rotation margin, no coupling co-scaling produces
arbitrarily accurate orientation inside the exactly truncated state class.
This is a same-profile compactness/slow-rotation proxy obstruction, not a
failure at one parameter point.

The proposition does **not** derive the hard cutoff dynamically. It says that
if a state has exact odd-sector support and every occupied spin obeys the two
declared proxy budgets, then its support cannot exceed `J_max`. It is not an
Einstein-Skyrme backreaction theorem.

## Localization Variables

The same profile fixes three distinct support measures:

```text
r_areal = R x_w sqrt(lambda),
s_proper = R asin[x_w sqrt(lambda)],
y_optical = R atanh[x_w sqrt(lambda)].               (4)
```

The executable record reports all three, the wall static metric factor, and the proper
horizon clearance. This prevents optical, proper, and areal localization from
being silently identified.

For the present diagnostic constants

```text
(mu,lambda,x_w)=(1,0.0025,4),
(C_*,s_*,G/R^2)=(0.5,0.1,10^-6),
```

the maximum odd-sector cutoff is `J_max=173`. The number is illustrative; the
proposition is the conditional invariant product (2) and risk floor (3).

## Coherence Corollary

If the reference undergoes isotropic rotational heat flow for dimensionless
time `gamma T`, then

```text
R_frame(T) >= 3/4(1-e^(-2 gamma T))
              + e^(-2 gamma T) R_frame(0).           (5)
```

This strengthens (3), but it is conditional until `gamma` and the
finite-coupling approximation error are derived from the same supported
Skyrmion/KMS action. AU.3 supplies the spectral inputs for that remaining
step.

## What Is And Is Not New

The compactness and slow-rotation scalings separately are standard. The paper
candidate is their elimination against the sharp global projective
orientation-risk theorem, with proper/optical support tracked for the same
matter profile. It closes the most obvious coupling-rescaling escape route.

The result does not yet cover profile-changing double scalings, soft spectral
tails, a dynamical origin of exact support, wall inertia, off-center
acceleration, nonspherical wall modes, or full Einstein-Skyrme junction
control. The current `c_M,c_I` substitution is numerical; a paper-grade
fixed-profile corollary requires directed interval energy and inertia bounds
from the authenticated profile tube. A genuine gravitational theorem also
requires constraints or junction equations that turn the compactness proxy
into controlled geometry.

## Reproduction

```bash
PYTHONPATH=. python -m unittest tests.test_skyrmion_observer_capacity
```

Artifacts:

- `qgtoy/skyrmion_observer_capacity.py`
- `tests/test_skyrmion_observer_capacity.py`
- `qgtoy/skyrmion_joint_scaling_no_go.py`
- `qgtoy/global_so3_reference_risk.py`
