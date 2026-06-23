# Finite-Pointer Observer Entropy Theorem

Status: four-gate analytic derivation and manuscript integration pass;
external proof and novelty review remain open

## Claim

Let a finite pointer have basis `|i>` with probabilities `w_i`, and let its
conditional post-switch scalar momentum data be `p_i`, all supported in the
same optical interval `[0,L]`. Define

```text
P_cl = sum_i w_i^2,
p_bar = sum_i w_i p_i,
E_bar = sum_i w_i ||p_i-p_bar||^2/2.
```

For the localized thermal covariance

```text
B_beta,L = P_L h_0^-1 coth(beta h_0/2) P_L,
C_beta(L) = sup_p <p,B_beta,L p>/(||p||^2/2),
```

the exact controlled-displacement channel and the existing localization
theorem imply

```text
Tr(rho_P^2)
 >= P_cl + (1-P_cl)
    exp[-C_beta(L) E_bar/(1-P_cl)],                 (1)

S_2(rho_P)
 <= -log{P_cl+(1-P_cl)
         exp[-C_beta(L) E_bar/(1-P_cl)]}
 <= min{H_2(w), C_beta(L) E_bar}.                  (2)
```

The first inequality is saturated by the symmetric binary pointer when the
profile difference is the top eigenfunction of `B_beta,L`. Global sharpness
for arbitrary pointer dimension is not claimed.

## Gate 1: Exact Finite-Pointer Channel

Use the diagonal controlled source

```text
S_int = -int sqrt(-g) phi(X)
        sum_i J_i(X)|i><i| d^4X.
```

The pointer projectors commute, and the free-field commutator is a c-number.
The Magnus series therefore stops after second order in every controlled
sector. Up to sector-dependent phases,

```text
U = sum_i |i><i| tensor W(J_i).
```

Purify the initial KMS field state and write

```text
|e_i> = W(J_i)|Omega_beta>,
G_ij = <e_j|e_i>.
```

`G` is a positive-semidefinite correlation matrix, since it is a Gram matrix.
Tracing out the purified field gives the exact Schur channel

```text
|i><j| -> G_ij |i><j|,
|G_ij| = exp(-Gamma_ij),
Gamma_ij = <p_i-p_j,B_beta,L(p_i-p_j)>/4.          (3)
```

The factor in (3) is fixed by the binary normalization: for conditional data
`p_+=p` and `p_-=-p`, equation (3) gives
`Gamma_+-=<p,B_beta,L p>`, exactly as in the binary manuscript.

For an initial pointer state `sum_i sqrt(w_i)|i>`, the reduced density matrix
is

```text
rho_ij = sqrt(w_i w_j) exp(i theta_ij) exp(-Gamma_ij),

Tr(rho^2) = sum_ij w_i w_j exp(-2 Gamma_ij).       (4)
```

The phases cancel from the purity.

Gate 1 disposition: **PASS**.

## Gate 2: Energy-Support-Renyi Bound

Set

```text
d_ij = p_i-p_j,
x_ij = 2 Gamma_ij = <d_ij,B_beta,L d_ij>/2.
```

The sharp binary localization theorem says

```text
<d,B_beta,L d> <= C_beta(L)||d||^2/2,
```

so

```text
x_ij <= C_beta(L)||d_ij||^2/4.                   (5)
```

The weighted pairwise-variance identity is

```text
sum_ij w_i w_j ||p_i-p_j||^2 = 4 E_bar.          (6)
```

Combining (5) and (6) gives

```text
sum_ij w_i w_j x_ij <= C_beta(L) E_bar.          (7)
```

The diagonal terms have `x_ii=0` and total weight `P_cl`. Normalize the
off-diagonal weights by `1-P_cl` and apply Jensen's inequality to the convex
function `exp(-x)`. Equations (4) and (7) then give (1).

The first simpler bound in (2) follows because the right-hand side of (1) is
at least `P_cl`. The second follows from convexity once more:

```text
P_cl + (1-P_cl) exp[-z/(1-P_cl)] >= exp(-z).
```

Taking `z=C_beta(L)E_bar` proves `S_2<=C_beta(L)E_bar`.

For a two-state pointer with equal weights and opposite top-mode profiles,
all off-diagonal exponents agree and every inequality above is an equality.
For more than two pointer states, simultaneous equality would require both
top-eigenspace alignment of all profile differences and equality in Jensen.
Those conditions are generally incompatible, so no general-d sharpness claim
is made.

Gate 2 disposition: **PASS, binary-sharp**.

## Gate 3: Harlow-Code Insertion

The purified controlled-displacement state is

```text
|omega> = sum_i sqrt(w_i)|i>_Ob |e_i>_Ob'.       (8)
```

Its two reductions have the same nonzero spectrum. Therefore

```text
exp[-S_2(omega_Ob')] = Tr(rho_Ob'^2)
                     = Tr(rho_P^2).              (9)
```

Equation (4.2) of Harlow, Usatyuk, and Zhao gives the Haar-averaged squared
inner-product fluctuation of their simple code. For two orthogonal CRT-real
matter states, both matter-overlap terms vanish, leaving the exact identity

```text
E_O |<phi|Vhat^dagger Vhat|psi>|^2
 = D/(D+2) Tr(rho_Ob'^2),                         (10)
```

where `D` is the dimension of the orthogonal encoding matrix. Equations (1),
(9), and (10) imply the physical floor

```text
E_O |<phi|Vhat^dagger Vhat|psi>|^2
 >= D/(D+2)
    [P_cl+(1-P_cl)
     exp{-C_beta(L)E_bar/(1-P_cl)}].              (11)
```

Thus the same purity controlled by the localized field-energy theorem enters
the Harlow code calculation. This closes the algebraic bridge that the binary
diamond error did not provide.

The interpretation is deliberately limited. Equation (8) treats the
purified field record as the nonideal record system in the code state. It is a
physical replacement of the ideal pointer record at the level of the simple
code model, not a derivation of the gravitational observer rule. Equation
(11) is a Haar-ensemble mean-square floor for an orthogonal matter pair; it is
not a lower bound for every fixed encoding map.

Gate 3 disposition: **PASS for the simple random-code model**.

## Gate 4: Branchwise Final-Slice Gravity

Now specialize to conformal de Sitter, where

```text
C_beta(L) = R C_opt(y),
y=L/R,
b=R tanh(y),
N(b)=sech(y)^2.
```

Assume every conditional branch is engineered to have spherical `q_i=0`
final data and obeys the local constraint budget

```text
Q_b,i <= delta < 1.
```

The existing final-slice constraint identity applies separately to every
branch:

```text
E_i <= delta b N(b)/(2G).                         (12)
```

The centered energy is not itself a branch mass, but

```text
E_bar = sum_i w_i E_i - ||p_bar||^2/2
      <= sum_i w_i E_i
      <= max_i E_i.                               (13)
```

Combining (2), (12), and (13) yields

```text
S_2(rho_P)
 <= delta (R^2/G)
    C_opt(y)tanh(y)sech(y)^2/2.                   (14)
```

At `y=1`, the frozen Galerkin illustration `C_opt(1)=1.0295979905445`
gives the nonrigorous geometric coefficient

```text
0.1646584608126553.
```

The rigorous row-sum upper bound `C_opt(1)<=1.1594713304692` instead gives

```text
S_2(rho_P) <= 0.18542845497445 delta R^2/G.       (15)
```

The numerical value `0.165` must therefore be labeled illustrative. Equation
(14), with exact `C_opt(y)`, is the analytic result.

As in the binary appendix, this is a branchwise final-slice constraint
corollary. The dephasing channel is still computed on the fixed de Sitter
background; it has not been recomputed on the conditional geometries, and no
coupled Einstein-scalar evolution is claimed.

Gate 4 disposition: **PASS with branchwise and final-slice hypotheses**.

## Reproduction

```bash
PYTHONPATH=. python experiments/finite_pointer_observer_audit.py
PYTHONPATH=. python experiments/finite_pointer_observer_clean_room_check.py
PYTHONPATH=. python -m pytest -q tests/test_finite_pointer_observer.py
```

The first command writes the source-bound four-gate certificate. The second
independently replays 64 finite-dimensional cases without importing the
production implementation. Neither computation replaces the analytic proof
above or certifies literature novelty.

## Pivot Decision

Gate 3 closes in the stated simple-code sense, so the manuscript may now be
reframed around a finite-observer entropy and code-accuracy floor. The binary
paper remains the technical engine and fallback revision. The upgraded paper
must retain the following boundaries:

- no general-d global sharpness claim;
- no identification with a deterministic error floor for every fixed code;
- no autonomous observer or actuator accounting;
- no channel calculation on a perturbed geometry;
- no coupled gravitational evolution; and
- external detector/QFT, operator-theory, and quantum-gravity novelty review
  remain required.
