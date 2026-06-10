# Centered Skyrmion Collective-Current Moments

Status: analytic consequences of the standard leading collective-current
ansatz plus a converged radial certificate for the centered inversion-symmetric
hard-wall rigid rotor.

## Collective Current

For the centered hedgehog, write the rotational kinetic density as

```text
kappa(r)=sin^2(F)/4 [f_pi^2/N
          +4/e^2 (F_r^2+sin^2(F)/(N r^2))],
I=(8 pi/3) int dr r^2 kappa(r).                         (1)
```

After compression to the leading collective band, write the coordinate-time
component of the soldered physical rotation current as

```text
ell_i^t(r,n)=[kappa(r)/I](delta_ij-n_i n_j)J_j.         (2)
```

For the static slice, `dSigma_mu ell_i^mu=r^2dr dOmega ell_i^t`; equivalently,
the proper volume factor and unit-normal factor cancel. Thus
`int_Sigma dSigma_mu ell_i^mu=J_i`. This flux notation is essential: treating
`ell_i^t` as a scalar density under the proper volume measure would insert an
incorrect extra `N^-1/2`.

The vector-isospin current is the dynamically rotated version
`j_a^t=-D_ai(A)ell_i`, up to the convention for left and right generators.
The spatial dependence in (2) is even under `n -> -n`.

## Signed Moments

Use centered static-slice Riemann-normal coordinates

```text
xi^k=rho(r)n^k,
rho(r)=R asin(r/R).                                     (3)
```

Angular parity gives the componentwise operator identity

```text
int_Sigma dSigma_mu xi^k ell_i^mu=0.                    (4)
```

The exact signed second moment is

```text
int_Sigma dSigma_mu xi^k xi^l ell_i^mu
=<rho^2>_I/10
 (4 delta_kl J_i-delta_ki J_l-delta_li J_k),            (5)

<rho^2>_I=
 [int dr r^2 rho(r)^2 kappa(r)]/[int dr r^2 kappa(r)].  (6)
```

Taking the spatial trace of (5) gives
`int_Sigma dSigma_mu rho^2 ell_i^mu=<rho^2>_I J_i`.

In the dimensionless variables of the worldtube solver,

```text
w(x)=x^2 sin^2(F)[N^-1+4F'^2+4sin^2(F)/(N x^2)],
q(x)=asin(sqrt(lambda)x)/sqrt(lambda),

(e f_pi)^2<rho^2>_I=[int q(x)^2w(x)dx]/[int w(x)dx].    (7)
```

## Absolute Moments

Equation (4) is a signed operator cancellation. It does not make the
norm-weighted first moment used in a generic Lipschitz estimate vanish. On a
spin-`L` sector, a conservative angular bound is

```text
M1_abs <=(9 pi/8)L<rho>_I,
M2_abs <=(9 pi/8)L<rho^2>_I.                            (8)
```

Thus (4) licenses the Hessian remainder in the centered zero-Bohr collective
current, while (8) supplies the absolute second moment required by that bound.
For a collective Hamiltonian `h(J^2)`, (2) commutes with the Hamiltonian and is
entirely zero Bohr frequency at this order.

## Default Certificate

For `mu=1`, `lambda=0.0025`, and `x_w=4`,

```text
c_I=34.2662015525,
(e f_pi)^2<r^2>_I=2.1843206906,
(e f_pi)^2<rho^2>_I=2.1902355498,
e f_pi sqrt(<rho^2>_I)=1.4799444415,

M1_abs <=4.9397264442 L/(e f_pi),
M2_abs <=7.7409314019 L/(e f_pi)^2.                    (9)
```

Step halving changes the proper mean-square constant by less than `4e-11`.

## Claim Boundary

The executable artifact assumes the standard leading collective-current
compression and checks its angular consequences and radial integrals; it is not
an independent Noether-current derivation. The result uses the centered
inversion-symmetric hard wall and leading rigid rotor. An off-center static
observer is accelerated; the Fermi lapse and
support traction contain an `l=1` term, so the deformed matter-wall solution
need not preserve (4). Vibrations, relativistic deformation, wall modes, and a
bare unsoldered local isospin current can also introduce nonzero-Bohr sectors.
The theorem therefore supplies the centered matter-derived baseline, not the
near-horizon off-center channel theorem.

Useful primary comparisons are [Hata and Kikuchi on the spinning-Skyrmion
normalization](https://arxiv.org/abs/1002.2464), [Acus, Norvaisas, and Riska on
isovector densities and form factors](https://arxiv.org/abs/nucl-th/0007012),
and [Brihaye and Delsate on de Sitter Skyrmions](https://arxiv.org/abs/hep-th/0512339).

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-current-moments
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_current_moments
```
