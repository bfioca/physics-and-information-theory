# Angular-Edge Symmetry And Spectral Robustness

Status: exact finite theorem and fragility gate

## Why This Audit Is Necessary

The relational observer model originally hid an axial `U(1)` phase reference.
That is not the same operation as losing a complete spatial orientation frame.
The edge correction also used the exact `m` degeneracy of the fuzzy Laplacian.
Both assumptions must be visible before the result is interpreted physically.

## Full Rotation Reference

After hiding the time reference, the harmonic Hilbert space is

```text
direct_sum_{ell=0}^L V_ell
```

and its algebra is `direct_sum_ell M_{2ell+1}`. Each `SU(2)` irrep occurs once.
Schur's lemma therefore gives

```text
axial U(1) fixed algebra: C^{(L+1)^2},
full SU(2) fixed algebra: direct_sum_ell C I_{V_ell} = C^{L+1}.
```

The full rotation expectation is blockwise normalized trace. It retains only
the center of the time-blind algebra. The removed dimension is

```text
sum_ell (2ell+1)^2 - (L+1)
  = 4L(L+1)(L+2)/3,
```

and the retained fraction is

```text
3/(4L^2+8L+3) = 3/(4L^2) + O(L^-3).
```

Thus the earlier `3/(4L)` law is specifically an axial-reference result. Full
orientation loss retains exactly `1/(L+1)` of the axial fixed algebra and
removes an additional `L(L+1)` dimensions. Orthogonal
phase states within one irrep have identical full-rotation outputs, so the
same minimax decoder error lower bound `1/2` applies.

These formulas are for the algebra after time averaging. On the full
`B(H_L)`, axial weights recur across different `ell` sectors and the `U(1)`
fixed algebra is larger.

## Spectral Robustness

Perturb the time generator by

```text
H_delta |ell,m> = [ell(ell+1)+delta m] |ell,m>,
delta = r sqrt(2),  r nonzero rational.
```

The spectrum is nondegenerate. Equality of two energies would require an
integer to cancel a rational multiple of `sqrt(2)` times an integer. Hence
infinite-time averaging is already fully diagonal for every nonzero `delta`,
however small. The exact distinction between time loss and axial-edge loss is
therefore not structurally stable without symmetry protection.

At finite averaging time `T`, the conclusion is continuous. For the extremal
phase pair in the `ell=L` block, the remaining trace distance is exactly

```text
|sinc(delta L T)|.
```

The characteristic resolution scale is `T ~ 1/(|delta|L)`, and the first exact
zero occurs at `T=pi/(|delta|L)`. Because the sinc function has side lobes and
revivals, this is not a globally monotone decay law. The edge-specific
distinction is perturbatively robust while `|delta|LT` is small. By contrast,
perturbations `H'=f(K_L)` that preserve full rotational symmetry retain every
magnetic degeneracy and the original time-block algebra.

## Consequence

The edge theorem needs one of two physics inputs:

- a full `SU(2)` orientation-reference formulation, whose fixed algebra is the
  center rather than the axial diagonal algebra; or
- a justified axial stabilizer together with a symmetry mechanism protecting
  within-`ell` degeneracy over the observer's time scale.

This audit narrows the paper target. The next theorem must derive the relevant
rotation group and modular Hamiltonian from the same KMS/static-patch model,
then extend that group expectation to the Type-II continuous core.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy edge-symmetry-robustness --max-level 8
PYTHONPATH=. python3 -m unittest tests.test_edge_symmetry_robustness
```
