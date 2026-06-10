# Validated Finite-Cell Conormal Origin Transfer

The exact conormal scaffold reduces the finite-origin problem to

```text
2tX_t=A(t)X+q(t),  X=(a,z),  t=x^2.
```

The regular block theorem proves `A-A0=O(t)`, `q=O(t)`, and `t^3` residual
divisibility for the two homogeneous and one forced degree-two germs. This
certificate supplies the missing functional remainders on the full origin
cell.

## Taylor Models

The authenticated shooting interval is split into two exact rational cells.
On each cell, the already validated quintic profile family supplies

```text
rho=-F'=b-3ct-5dt^2+t^3 r_p,  |r_p|<=13/10,
u=(pi-F)/x=b-ct-dt^2+t^3 r_u, |r_u|<=13/70.
```

Entire sine and cosine kernels are composed with these models. The regular
`Cbar,Mbar,Pbar` and source blocks are then propagated through the exact
conormal formulas. No derivative of either profile remainder is taken.

The constant coefficient in `A(t)-A(0)` is cancelled symbolically before
interval evaluation. Likewise, the exact recurrence theorem cancels the
constant, linear, and quadratic residual coefficients before the remaining
Taylor remainder is interpreted as `e=E/t^3`. These cancellations retain the
parameter correlation that a direct interval subtraction would lose.

## Bounds

In the weighted state norm with weights

```text
(36/25,73/50,13/20,73/100),
```

the exact rational audit proves

```text
gamma = ||G||_w                  < 0.500310,
delta = sup ||A-A0||_w           < 0.145445,
gamma delta                      < 0.072576.
```

For each branch, choose

```text
R_j=2 gamma epsilon_j/(1-gamma delta).
```

Then every cell satisfies

```text
gamma epsilon_j + gamma delta R_j <= R_j.
```

The global residual and radius maxima in branch order
`(linear homogeneous, cubic homogeneous, forced particular)` are

```text
epsilon < (825.125,304.773,23.538),
R       < (887.903,327.961,25.328).
```

These radii multiply `t^3`. At the cutoff `t=1/256`, every component of the
actual conormal state error is below `1e-4`; the largest certified component
is approximately `7.73e-5`.

## Consequence

For every authenticated shooting slope and each of the three affine columns,
the exact degree-two conormal germ has a unique regular continuation through
`x=1/16` inside its certified weighted ball. The two free homogeneous columns
and one forced column therefore define a validated affine conormal boundary
tube at the finite cutoff.

## Reproduce

```bash
PYTHONPATH=. python experiments/validated_centrifugal_conormal_remainder_audit.py
python -m pytest -q tests/test_validated_centrifugal_conormal_remainder.py tests/test_validated_centrifugal_conormal_remainder_audit.py
```

## Claim Boundary

This is a finite-cell conormal-state transfer theorem. A direct interval tube
for physical `(f,g,f',g')`, equivalence with the Friedrichs trace space, the
global continuum inverse, and the validated nonzero exterior response remain
separate gates.
