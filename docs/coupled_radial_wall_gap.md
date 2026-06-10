# Coupled Radial Profile-Wall Gap Gate

Status: exact branch-coordinate transfer and insufficiency result; a separate
compatible-witness certificate now closes the positive spherical membrane gap

## Direct Closure

The missing branch inputs below are required only for this sharper
branch-coordinate comparison. They are not required for a strict positive
coupled gap. The authenticated theorem in
`skyrmion_moving_wall_radial_gap.md` instead eliminates the wall displacement
with the mirror boundary condition and uses

```text
v=1/[(x-9/4)^2+8].
```

Exact Young-Laplace cancellation gives boundary mass `800/47`, transformed
boundary stiffness `39878/69325`, and `Lv/v>=1/100` on the full exact profile.
Consequently the complete spherical profile-membrane channel obeys

```text
omega_hat_l0>=1/50.
```

The material below remains useful because a certified branch tangent and
curvature could improve this conservative floor toward the floating `0.198`.

## Moving Boundary

Let `a(tau)=a_0+q(tau)` and let `F_a` be a `C^2` family of exact static
Dirichlet profiles. The ideal-mirror constraint gives

```text
eta(a_0)+F_0'(a_0)q=0.                                  (1)
```

Set `chi=partial_a F_a|a_0`, so `chi(a_0)=-F_0'(a_0)`, and write
`eta=xi+q chi`. Then `xi` obeys homogeneous fixed-wall Dirichlet data. Because
every `F_a` is stationary against such profile variations, this branch
coordinate diagonalizes the static quadratic form:

```text
V_2 >= alpha ||xi||_2^2+k q^2.                          (2)
```

Here `alpha=1` is now authenticated for the default exact profile and `k` is
the total fixed-tension Dirichlet-branch energy curvature in the same
normalization.

Equivalently, a harmonic mode obeys the weak wall equation

```text
-F_0'(a_0)P(a_0)eta'(a_0)+4k_b q
  =omega_hat^2 [M_wall/pi]q.                            (2a)
```

## Nambu-Goto Normalization

For a spherical shell in
`ds^2=-N d tau^2+dx^2/N+x^2d Omega^2`,

```text
S_wall=-(4 pi/e^2) integral d tau
       sigma a^2 sqrt(N) sqrt(1-dot(a)^2/N^2).           (3)
```

Thus the shell kinetic mass is

```text
M_wall=4 pi sigma a_0^2/N_0^(3/2).                      (4)
```

The radial Jacobi quadratic action carries the common factor `4pi/8`, so its
dimensionless bracket uses

```text
m=M_wall/pi,  k=E_branch''/pi.                          (5)
```

This normalization preserves the shell-only ratio `k/m=E_branch''/M_wall`.

## Exact Transfer

Motion along the static branch drags the field. With
`c^2=<chi,W chi>` and `W<=W_max`,

```text
T_2 <= W_max ||xi||^2
       +2 sqrt(W_max)c ||xi|| |q|+(c^2+m)q^2.           (6)
```

Let

```text
S=alpha(c^2+m)+k W_max,  D=W_max m.
```

The smaller generalized eigenvalue of the comparison forms is

```text
omega_coupled^2 >=
  2 alpha k/[S+sqrt(S^2-4D alpha k)].                   (7)
```

At `c=0`, this is exactly
`min(alpha/W_max,k/m)`. It stays positive for every finite certified `c`.

## Insufficiency

The lift norm is an independent physical input. The pure wall-coordinate
trial vector has

```text
omega_min^2 <= k/(c^2+m).                               (8)
```

Thus `alpha>0`, `k>0`, and `m>0` do not imply a uniform coupled gap when `c`
is unbounded. The current shell-only value `sqrt(E_branch''/M_wall)=1.03214`
omits this added profile mass and cannot be presented as a coupled normal-mode
frequency.

There is also no direct shortcut using the current fixed-wall Barta witness.
For `v=8/[(x-33/16)^2+4]`, the moving-endpoint ground-state transform leaves

```text
[P(a)v'(a)/v(a)+4k_b/F_0'(a)^2] eta(a)^2.               (9)
```

At the default wall, `v'/v=-992/1985` and the two terms sum to approximately
`-2.24124`. The witness therefore fails the moving-endpoint boundary test.
This is a witness obstruction, not evidence for a negative physical mode; the
static-branch coordinate and equation (7) remain the clean route.

For the default branch, the repository currently has:

- authenticated `alpha=1` and `W_max=25`;
- step-converged evidence `E_branch''=0.4399062320>0`;
- step-converged `M_wall=0.4129339430>0`; and
- no certified `c^2=<partial_aF_a,W partial_aF_a>`.

The shortest route to sharpen equation (7) is to construct the exact branch
tangent from the AU.1 shooting sensitivity, certify its weighted norm, and
replace the finite-difference pressure derivative by an interval bound. The
positive coupled `l=0` gap itself is already closed by the direct witness above.

Exploratory radius differencing gives `c^2 approximately 0.063759`. If that
number and the current branch curvature were certified, equation (7) would
give the conservative full coupled bound `omega_hat>=0.198`. The adiabatic
branch estimate, which keeps the total relaxed stiffness but adds the dragged
profile mass, would be

```text
sqrt[E_branch''/(M_wall+pi c^2)] approximately 0.847,    (10)
```

not the shell-only `1.032`. Both numbers remain floating diagnostics.

## Reproduction

```bash
python -m pytest -q tests/test_coupled_radial_wall_gap.py
```

Artifacts:

- `qgtoy/coupled_radial_wall_gap.py`
- `tests/test_coupled_radial_wall_gap.py`
