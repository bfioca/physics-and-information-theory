# Global Geometric Thermal Type-I No-Go

Status: exact angular-cutoff convergence theorem and static-patch model-selection gate

## Geometric Regulator

Consider a normal-ordered positive-mass free boson on a sphere of radius `R`.
At angular cutoff `L`, retain modes

```text
0 <= ell <= L,  -ell <= m <= ell,
omega_ell = sqrt(mu^2 + ell(ell+1)/R^2),
H_L = sum_{ell,m} omega_ell a^*_{ell,m} a_{ell,m}.
```

This is the direct global-field completion of the repository's fuzzy angular
kinematics. It is geometric and state-derived: the state is the Gibbs density
`rho_L=exp(-beta H_L)/Z_L`.

## Trace-Class Continuum Limit

For `mu>0`, set `q=exp(-beta/R)`. Since `omega_ell>=ell/R`,

```text
log Z_infinity - log Z_L
 <= [1/(1-q)] sum_{ell>L}(2ell+1)q^ell
 = q^(L+1)[(2L+3)-(2L+1)q]/(1-q)^3.
```

The bound tends exponentially to zero. The infinite partition function and
mean total occupation are finite.

Embed `rho_L` into the full Fock space by putting all omitted modes in their
vacuum. The infinite Gibbs density factorizes into retained and tail modes, so
the normalized trace distance is

```text
D(rho_L tensor |0_tail><0_tail|, rho_infinity)
 = 1 - 1/Z_tail
 <= log Z_tail.
```

Thus the angular-cutoff states converge in trace norm to a genuine trace-class
global Gibbs density.

## Algebra-Type Consequence

Declare the global observable algebra to be the weak closure of the Weyl
algebra in its irreducible Fock representation,

```text
M_global=B(Gamma_s(L^2(S^2))).
```

The trace-class Gibbs state is faithful and normal on this declared algebra, and
its GNS von Neumann algebra is again `B(Fock)`, Type `I_infinity`. Its modular
action is inner. The modular crossed product is a Type-I semifinite algebra with
diffuse center, not the Type-`II` factor used for the gravitational observer
algebra. This remains true after adding arbitrarily many compact angular
harmonics to the global algebra. Restricting a normal global state to localized
AQFT algebras is a different construction and can yield Type III.

For `mu=0`, the formal occupation-number factor of the `ell=0` mode diverges.
Canonically, the noncompact constant scalar mode is a free particle rather than
a zero-frequency oscillator, and its thermal trace also diverges. That is an
infrared zero-mode failure, not a mechanism producing a local Type-`III` factor
or a Type-`II` observer algebra. Adding mass, removing the zero mode, or
compactifying the target returns to the global Type-I conclusion above.

## Physics Consequence

The engineered alternating qubit chain cannot simply be replaced by a global
free-field Gibbs state on the fuzzy horizon. A successful construction must
retain localization and net structure. A faithful static-patch field regulator
should additionally include the radial and near-horizon redshift degrees of
freedom before forming the modular crossed product. In algebraic QFT, Type
`III_1` belongs to localized region algebras and their net structure, not to a
trace-class density on the global Fock algebra.

In four-dimensional de Sitter, the optical volume of a static spatial slice cut
off a coordinate distance `delta` from the horizon is

```text
V_opt(delta)=4 pi int_0^(R-delta) r^2 dr/(1-r^2/R^2)^2
            ~ pi R^4/delta.
```

This divergent geometric limit is absent from angular-only refinement. The
theorem does not claim that radial modes are mathematically necessary for every
Type-III net; it identifies the localization limit that a faithful static-patch
model must still represent.

This theorem is a model-selection no-go, not a standalone novelty claim. It
connects the finite fuzzy regulator to the precise reason it fails to generate
the desired factor type. Interacting local nets, the Bunch-Davies
representation, gauge constraints, de Sitter boosts, and generalized entropy
remain open.

Primary context:

- Yngvason, [The Role of Type III Factors in Quantum Field
  Theory](https://arxiv.org/abs/math-ph/0411058).
- Chandrasekaran, Longo, Penington, and Witten, [An Algebra of Observables for
  de Sitter Space](https://arxiv.org/abs/2206.10780).
- Chen and Xu, [An algebra for covariant observers in de Sitter
  space](https://arxiv.org/abs/2511.00622v2).

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy geometric-thermal-type-no-go --max-cutoff 24
PYTHONPATH=. python3 -m unittest tests.test_geometric_thermal_type_no_go
```
