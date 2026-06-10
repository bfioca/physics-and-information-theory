# Operational Reducible Rotation Reference

Status: matched prepared-reference recovery theorem with multiplicity and Casimir cost

## Physical Channel

For an unknown spin-`L` state and a fixed prepared reference state `eta`, remove
the external orientation by applying

```text
N_eta(rho)=integral_SU(2) dg
  [U_L(g) rho U_L(g)^*] tensor [U_R(g) eta U_R(g)^*].
```

A deterministic decoder may act on the entire twirled system-reference output.

## Exact Finite-Reference No-Go

No finite-dimensional prepared reference for the connected rotation group
permits exact full-sector recovery.
For a pure reference, the continuous Kraus overlaps are

```text
K_g^* K_h = <eta|U_R(g^-1 h)|eta> U_L(g^-1 h).
```

Exact Knill-Laflamme correction would require this to be scalar for all `g,h`.
The reference characteristic function is continuous and equals one at the
identity, so it is nonzero on a neighborhood containing rotations for which the
nontrivial spin representation `U_L` is not scalar. Mixed reference states give
the same contradiction through a spectral Kraus family. Approximate recovery
can improve without bound, but equality is impossible at finite dimension.
Pre-correlated relational encodings, exact recovery of a logical multiplicity
subsystem, and postselection are outside this no-go.

## Multiplicity Lower Bound

Write

```text
R=direct_sum_j V_j tensor C^{m_j},
V_L tensor R=direct_sum_K V_K tensor C^{n_K},
n_K=sum_j m_j 1{|L-j|<=K<=L+j}.
```

The twirl removes each carrier `V_K` and retains its multiplicity algebra
`M_{n_K}`. If `r=max_K n_K` and `d=2L+1`, the twirled Choi state has Schmidt
number at most `r`. Every deterministic decoder therefore obeys

```text
(1/2)||D N_eta-identity_d||_diamond >= max(0,1-r/d).
```

For `R=V_0 direct_sum V_1`, the fixed algebra is

```text
C direct_sum M_2 direct_sum C,
```

so one relational qubit survives, but full-sector recovery error is at least
`1-2/(2L+1)` and tends to one.

## Truncated Peter-Weyl Treatment

The repository uses positive integer spins, so the concrete treatment is the
integer-spin Peter-Weyl cutoff of `SO(3)`, equivalently the center-blind sector
of `SU(2)` for conjugation channels on the target operator algebra:

```text
R_J=direct_sum_{j=0}^J V_j tensor V_j^*,
D_J=dim R_J=(J+1)(2J+1)(2J+3)/3.
```

The group acts only on the left carrier:

```text
U_R(g)=direct_sum_j U_j(g) tensor identity_{V_j^*}.
```

The dual factor is the intrinsic right-regular multiplicity index. Acting as
`U_j tensor U_j^*` instead would leave each `|Phi_j>` invariant and would not
provide an orientation reference.

With normalized maximally entangled vectors `|Phi_j>`, prepare

```text
|eta_J>=D_J^(-1/2) sum_j (2j+1)|Phi_j>.
```

The covariant POVM seed `sum_j(2j+1)|Phi_j>` resolves the identity. Measuring
the orientation and correcting the system gives

```text
Lambda_{L,J}(rho)=integral dg p_J(g)U_L(g)rho U_L(g)^*,
p_J(g)=D_J^-1 |sum_j(2j+1)chi_j(g)|^2.
```

On irreducible tensor operators of rank `k`,

```text
Lambda_{L,J}(T_kq)=lambda_k(J)T_kq,
lambda_k(J)=
  sum_{j,l<=J}(2j+1)(2l+1)1{|j-l|<=k<=j+l}
  /[(2k+1)D_J].
```

For tensor ranks `k<=2J`, and hence for the full target whenever `J>=L`,

```text
1-lambda_k(J)=
 k(k+1)[12J(J+2)-k(k+1)+11]
 /[6(2k+1)D_J].
```

The deficits increase with rank. A conservative full-channel bound is

```text
(1/2)||Lambda_{L,J}-identity||_diamond
 <= min{1,(2L+1)[1-lambda_{2L}(J)]/2}.
```

Thus the constructive decoder converges in diamond norm for fixed `L` as
`J` grows, while exact equality never occurs at finite `J`.

The convergence is not uniform when the target spin grows proportionally with
`J`. For fixed rank, the deficit is `O(1/J)`; for `k=alpha J` it approaches a
nonzero function of `alpha`.

The maximally mixed entanglement fidelity is exact from the multiplier sum. The
reference resource has

```text
<C_left> = 3J(J+2)/5.
```

This turns representation multiplicity into a quantitative recovery/Casimir
tradeoff. The decoder is constructive, not proved optimal. The theorem uses
positive integer spins and contains no local KMS dynamics, gravitational energy
constraint, half-integer full-`SU(2)` cutoff, or `SO(1,d)` boost sector.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy operational-su2-reference --max-system-spin 6
PYTHONPATH=. python3 -m unittest tests.test_operational_su2_reference
```
