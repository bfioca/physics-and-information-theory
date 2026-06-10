# Skyrmion Compactness/Slow-Rotation Joint No-Go

Status: exact conditional scaling theorem for a fixed dimensionless centered
worldtube profile.

## Fixed-Profile Identities

Fix the dimensionless hard-wall data `(mu,lambda,x_w)` and its total mass and
interior inertia constants `(c_M,c_I)`. Since

```text
e f_pi=1/(R sqrt(lambda)),
M=c_M/(e^2 R sqrt(lambda)),
a=x_w R sqrt(lambda),
I=c_I R sqrt(lambda)/e^2,                                (1)
```

the compactness and maximum-spin slow-rotation parameter are

```text
C=2GM/a=2G c_M/(e^2 x_w lambda R^2),
epsilon_rot=e^2 sqrt[K(K+1)]/c_I.                       (2)
```

Their product is independent of the constrained `e`/`f_pi` co-scaling that
preserves `e f_pi`, and hence the fixed dimensionless profile:

```text
C epsilon_rot=
2G c_M sqrt[K(K+1)]/(c_I x_w lambda R^2).               (3)
```

For fixed budgets `C<=C_*` and `epsilon_rot<=epsilon_*`, an admissible coupling
exists exactly when

```text
sqrt[K(K+1)] <=
C_* epsilon_* c_I x_w lambda R^2/(2G c_M).              (4)
```

Thus no fixed-profile family at fixed `R^2/G` admits an asymptotically growing
controlled reference cutoff. Lowering `e` improves slow rotation but worsens
compactness by the inverse factor.

For the executable defaults

```text
mu=1, lambda=0.0025, x_w=4,
c_M=48.95760325, c_I=34.26620155,
R=1, G=10^-6, C_*=0.5, epsilon_*=0.1,
```

the largest admissible physical source spin in the fermionic `B=1` sector is
`K=173.5`, corresponding to odd Peter-Weyl cutoff `J=173`, with a narrow
nonempty `e^2` interval. The next allowed source spin, `K=174.5`, has no
coupling satisfying both budgets. This finite number is illustrative and
parameter dependent; the theorem is the product identity and finite-window
conclusion.

## Claim Boundary

The theorem fixes `(mu,lambda,x_w)` and uses the centered ideal-wall mass and
inertia. It does not exclude profile-changing double scalings, wall inertia,
different matter sources, `Omega^4` corrections, deformation, radiation,
off-center support, or full Einstein-Skyrme backreaction. It is nevertheless a
matter-derived obstruction to the simplest attempt to evade the earlier
compact-top ansatz by co-varying `e` and `f_pi` while holding `e f_pi` and the
dimensionless profile fixed.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-joint-scaling-no-go
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_joint_scaling_no_go
```
