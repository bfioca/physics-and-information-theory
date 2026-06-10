# Authenticated Moving-Membrane Radial Gap

Status: complete for the regular `l=0` Skyrmion profile coupled to a spherical
positive-tension Nambu-Goto membrane in static Young-Laplace equilibrium

## Coupled Form

Let the wall displacement be `q` and write `y=F_0'(a)<0`. The linearized
ideal-mirror condition is

```text
eta(a)+y q=0.                                             (1)
```

In the radial Jacobi normalization, the quadratic potential and kinetic forms
are

```text
V=q_J[eta]+4 k_b q^2,
T=integral W eta^2 dx + m q^2,                            (2)
```

where `m=M_wall/pi`. Eliminating `q=-eta(a)/y` turns this into a bulk form with
one dynamical boundary degree of freedom.

Set `u=lambda a^2` and impose exact spherical Young-Laplace balance. The
equilibrium tension cancels from the normalized boundary ratios:

```text
m/y^2 = M_0 = a^3/[2(2-3u)],
4k_b/y^2 = B_0
 = a(1-2u)+a(2-9u+6u^2)/[2(2-3u)].                       (3)
```

For the authenticated wall `a=4`, `lambda=1/400`,

```text
u=1/25,  M_0=800/47,  B_0=6386/1175.                    (4)
```

The cancellation is important: the numerical frequency theorem does not use a
floating wall slope, tension, branch curvature, or finite-difference branch
tangent.

## Compatible Witness

Use the strictly positive rational witness

```text
v(x)=1/[(x-9/4)^2+8].                                    (5)
```

For `L=-(P d/dx)d/dx+Q`, the exact quotient is

```text
Lv/v = Q + 2z P'/(z^2+8)
          +P[16-6z^2]/(z^2+8)^2,
z=x-9/4.                                                  (6)
```

Authenticated interval replay through the exact AU.1 Newton tube proves

```text
Lv/v >= 1/100                                             (7)
```

on the complete interval `0<=x<=4`. The positive-radius replay has 95 leaves,
uses maximum refinement depth five, and has recomputed minimum quotient
`>0.01297111385`. The cancellation-preserving origin quotient is
`>37.27705445`.

The ground-state transform gives

```text
V >= (1/100) integral eta^2 dx
     +[B_0+P(a)v'(a)/v(a)] eta(a)^2.                      (8)
```

Here

```text
P(a)=384/25,
v'(a)/v(a)=-56/177,
B_0+P(a)v'(a)/v(a)=39878/69325>0.                         (9)
```

The earlier fixed-wall witness fails this last sign test. That was a witness
failure, not an instability; equation (5) supplies the compatible witness.

## Frequency Theorem

The exact hard-support kinetic estimates are

```text
W<=25,
T<=25 integral eta^2 dx +(800/47)eta(a)^2.               (10)
```

Combining equations (8)-(10),

```text
omega_hat^2 >= min[(1/100)/25,
                   (39878/69325)/(800/47)]
              =1/2500,
omega_hat >=1/50,
omega_K >= e f_pi/50.                                    (11)
```

This is the complete coupled spherical profile-membrane `l=0` gap. It does not
cover anchor motion, nonspherical membrane or Skyrmion channels, rotational
zero modes, collective-band projection, or self-gravity.

The branch-coordinate theorem in `coupled_radial_wall_gap.md` remains useful:
certifying its branch shape and curvature could improve `1/50` toward the
current floating comparison `0.198`. Those inputs are no longer required for a
strict positive moving-wall radial theorem.

## Reproduction

```bash
python experiments/skyrmion_moving_wall_radial_gap_audit.py
python -m pytest -q tests/test_validated_skyrmion_moving_wall_gap.py
```

Artifacts:

- `qgtoy/validated_skyrmion_moving_wall_gap.py`
- `tests/test_validated_skyrmion_moving_wall_gap.py`
- `experiments/skyrmion_moving_wall_radial_gap_exact_certificate.json`
  (SHA256
  `2bb48f770504ab5a0a0f9b3139b881877a414ddb9b8c19cd34c81bfd26b42686`)
