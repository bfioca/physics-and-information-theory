# Spacelike Replication: Priority Reduction Audit

Audit date: 2026-06-11 UTC

Disposition: **NOVELTY STOP FOR THE PRESENT CENTRAL THEOREM.** The
state-weighted three-cell inequality is a direct corollary of the established
completely-positive-map covariance Cauchy-Schwarz lemma in Janssens,
*Unifying Decoherence and the Heisenberg Principle*. The spacelike `SO(3)`
application remains a useful internal lemma, but it is not a viable standalone
paper claim. The project's predeclared priority kill gate is satisfied.

Primary source: [Janssens, Letters in Mathematical Physics 107, 1557-1579
(2017)](https://doi.org/10.1007/s11005-017-0953-z), especially Lemma 1 and
Theorem 3.

## 1. Exact CP-Map Reduction

Let `W:C -> H` be the encoding isometry, `W^*W=I_C`, `P=WW^*`, and `Q=I-P`.
For a code-supported state on `H`, write `rho_C=W^* rho W`; below we suppress the
subscript, equivalently identifying `C` with `P H`. Define the unital
completely positive compression

```text
T(X)=W^* X W.                                          (1.1)
```

Janssens defines the covariance form

```text
(X,Y)_T=T(X*Y)-T(X)*T(Y)                              (1.2)
```

and proves the CP Cauchy-Schwarz inequality

```text
(X,Y)_T (Y,X)_T <= ||(Y,Y)_T|| (X,X)_T.               (1.3)
```

For each self-adjoint cell observable `A_a`, its Schwarz defect is exactly the
branch's off-code noise operator:

```text
D_a:=(A_a,A_a)_T
   =W^* A_a Q A_a W,
||D_a||=||Q A_a W||^2=lambda_a^2,
Tr(rho D_a)=p_a(rho).                                  (1.4)
```

If `[A_a,A_b]=0`, then

```text
[T(A_a),T(A_b)]=(A_b,A_a)_T-(A_a,A_b)_T.              (1.5)
```

Applying (1.3) to the two terms in (1.5), right multiplying by
`rho^(1/2)`, and using the Hilbert-Schmidt triangle inequality gives

```text
||[T(A_a),T(A_b)] rho^(1/2)||_2
 <=lambda_b sqrt[p_a(rho)]+lambda_a sqrt[p_b(rho)].    (1.6)
```

Substituting `T(A_a)=alpha J_a` and a cyclic triple `(a,b,c)` yields

```text
|alpha|^2 sqrt[Tr(rho J_c^2)]
 <=lambda_b sqrt[p_a(rho)]+lambda_a sqrt[p_b(rho)].    (1.7)
```

Equation (1.7) is exactly equation (3.4) of the theorem note. With
`lambda_a<=lambda_*`, squaring, applying `(x+y)^2<=2(x^2+y^2)`, and summing
the three cyclic pairs gives

```text
alpha^4 Tr(rho J^2)<=4 lambda_*^2 sum_a p_a(rho).      (1.8)
```

Thus the main state-weighted theorem is not merely analogous to the prior
lemma; it follows immediately from it.

## 2. Joint-Measurement Interpretation

The setup is an unbiased joint-measurement dilation in established language:

| Present notation | Joint-measurement notation |
| --- | --- |
| commuting `A_a` | compatible pointer observables |
| `T(A_a)=alpha J_a` | compressed pointer first moments |
| `D_a=T(A_a^2)-T(A_a)^2` | added-noise operator |
| `p_a(rho)=Tr(rho D_a)` | state-dependent added variance |
| `lambda_a^2=||D_a||` | maximal added variance |

Janssens' Theorem 3 gives the corresponding pairwise joint-measurement noise
bound; the construction following its proof establishes sharpness.
Polterovich uses the same noise operator and Janssens inequality in Theorem
2.4 of [*Symplectic Geometry of Quantum Noise*](https://doi.org/10.1007/s00220-014-1937-9).
For the three commuting pointers here, the joint spectral theorem directly
supplies a common PVM. Related Naimark-dilation characterizations cover pairs
in Beneduci, Theorems 4.5-4.7
([arXiv:1404.1477](https://arxiv.org/abs/1404.1477)), and finite sets of
finite-outcome POVMs in Mitra, Ghosh, and Mandayam, Theorem 3
([arXiv:2011.11364](https://arxiv.org/abs/2011.11364)).

The language "spacelike replication forces off-code leakage" is therefore a
physical interpretation of established joint-measurement added noise, not a
new mathematical obstruction.

## 3. Relative-Covariance Dictionary

The earlier covariant-QEC comparison remains useful for placing the variables.
Exact compression says

```text
A_a W-W alpha J_a=Q A_a W.                            (3.1)
```

For a code-state purification `|psi_rho>`, define the relative
covariance-defect path

```text
|Psi_a(t)>=([exp(-it A_a) W exp(it alpha J_a)] tensor I)|psi_rho>.
```

Its tangent is `-i(Q A_aW tensor I)|psi_rho>`, orthogonal to the encoded
state, so its pure-path QFI is

```text
F_a^rel(rho)=4p_a(rho).                                (3.2)
```

This is not the QFI of the ordinary orbit generated only by `A_a`, which also
contains the logical variance. The main theorem can be rewritten as

```text
alpha^4 Tr(rho J^2)
 <=lambda_*^2 sum_a F_a^rel(rho).                       (3.3)
```

That reformulation does not restore novelty: it is the same added-variance
operator from Section 1 expressed as a relative covariance tangent.

## 4. Why The Initial QEC Search Did Not Kill It

The closest approximate-cleaning and covariant-QEC papers use stronger or
different structures: a noise channel, recovery map, subsystem erasure,
transversal physical charge, or channel-level covariance defect. They do not
state (1.8) in the present variables, so the QEC-only audit returned a
provisional non-reduction. The decisive prior art lies one layer earlier, in
the general theory of UCP compression and joint-measurement noise.

Relevant QEC sources remain useful context:

- [Beny, *Conditions for the approximate correction of algebras*](https://arxiv.org/abs/0907.4207);
- [Flammia, Haah, Kastoryano, and Kim](https://arxiv.org/abs/1610.06169);
- [Beny, Zimboras, and Pastawski](https://arxiv.org/abs/1806.10324);
- [Faist et al., *Continuous Symmetries and Approximate Quantum Error Correction*](https://arxiv.org/abs/1902.07714);
- [Zhou, Liu, and Jiang, *New perspectives on covariant quantum error correction*](https://quantum-journal.org/papers/q-2021-08-09-521/); and
- [Liu and Zhou, *Quantum error correction meets continuous symmetries*](https://arxiv.org/abs/2111.06360).

They do not rescue a novelty claim already subsumed by (1.3).

## 5. Compact-Lie Generalization Does Not Rescue The Paper

For a compact simple Lie algebra of dimension `d`, choose an orthonormal basis
with

```text
[X_i,X_j]=i f_ij^k X_k,
sum_ij f_ij^k f_ij^l=C_adj delta_kl.
```

Applying (1.6) to every pair and summing gives

```text
sum_i p_i(rho)
 >=alpha^4 C_adj Tr[rho sum_k X_k^2]
   /[4(d-1)Lambda^2].                                  (5.1)
```

For `su(2)`, `d=3` and `C_adj=2`, recovering the factor `1/(4Lambda^2)`.
This is a clean extension, but it is still a direct pairwise summation of
Janssens' lemma and is not a new central result.

## 6. Research Disposition

**Stop the bounded-theorem manuscript as a publication track.** Retain the
result as a rigorous internal locality/joint-measurement lemma for the broader
observer program and cite Janssens prominently whenever it is used.

A new paper direction would need a result not supplied by CP-map and
joint-measurement theory, for example:

1. a genuinely multi-observable inequality stronger than every pairwise
   Janssens consequence, with new optimality or equality structure;
2. a dynamical theorem converting added variance into a rate, lifetime, or
   recoverability statement;
3. a physical bound relating `lambda_*` to localization, energy, optical
   support, or gravitational backreaction; or
4. a standalone sharp global `SO(3)` Bayes-risk theorem, with the leakage
   relation cited only as an application.

The current bounded result remains technically correct. What stops is the
paper-level novelty claim, not the mathematics.
