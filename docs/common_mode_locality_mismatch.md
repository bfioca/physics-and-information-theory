# Common-Mode Locality Mismatch

Status: exact two-charge witness and finite-cell bounded-generator comparison;
the static-patch noise kernel and gravitational source remain open

## Why This Gate Exists

The finite-time heat-twirl theorem assumes that the target and spherical-top
reference experience the same stochastic rotation. A local bath does not
generically have this property, although local massless or critical systems can
carry long-range correlations. This note turns that distinction into a quantitative
test rather than treating “common noise” as synonymous with “local
interaction.”

Collective-noise decoherence-free subspaces are standard. Equal-strength
coupling to a common environment was isolated in the noiseless-code analysis of
[Zanardi and Rasetti](https://arxiv.org/abs/quant-ph/9705044), while spatially
dependent bath coherence was already central in
[Palma, Suominen, and Ekert](https://arxiv.org/abs/quant-ph/9702001). The result
below applies that mechanism as a falsification test for the particular
target-reference common mode required by the observer-algebra program.

## Exact Axial Witness

Let two commuting axial charges `q_T,q_R` experience Stratonovich Gaussian
white noise with normalized covariance

```text
C=[[1,c],[c,1]],       -1<=c<=1,
E[xi_i(t)xi_j(t')]=2 gamma C_ij delta(t-t').
```

The Markov generator is

```text
L_C(rho)=-gamma sum_(i,j=T,R) C_ij [q_i,[q_j,rho]].       (1)
```

Use charge eigenstates whose exchanged axial charge has gap `Delta>0`. After
normalizing the branch labels as `(1,0)` and `(0,1)`, the relational witness

```text
|psi_rel>=(|1,0>+|0,1>)/sqrt(2)
```

has charge-difference vector `(1,-1)`. At `s=gamma T`, its off-diagonal
visibility is therefore exactly

```text
v(s,c)=exp[-s Delta^2 (1,-1) C (1,-1)^T]
      =exp[-2s Delta^2(1-c)].                            (2)
```

For perfect common mode, `c=1`, both branches acquire the same stochastic phase
and the coherence is decoherence free. For every `c<1`, it decays.

Let `Phi_C,T` be the actual channel and `Phi_*,T` the ideal `c=1` common-mode
channel. Their outputs on `|psi_rel>` have normalized trace distance

```text
(1/2)||Phi_C,T(psi_rel)-Phi_*,T(psi_rel)||_1
 =(1-v)/2.
```

Consequently

```text
(1/2)||Phi_C,T-Phi_*,T||_diamond
 >= [1-exp(-2 gamma T Delta^2(1-c))]/2.                   (3)
```

This is a lower bound on channel mismatch, not a recovery lower bound by itself.
It says that the exact common-mode heat channel cannot approximate imperfectly
correlated axial noise better than the witness permits.
Additional transverse dynamics is outside this exact two-charge calculation and
must be controlled before applying the witness to a full isotropic channel.

## Correlation Accuracy Required By The Heat Schedule

To make the mismatch in (3) at most `eta<1/2`, a necessary condition is

```text
1-c <= -log(1-2 eta)/(2 gamma T Delta^2).                (4)
```

Use the sufficient heat-twirl schedule from Research Theorem Y,

```text
gamma T=(1/2)log d,
```

and demand that the new common-mode error be no larger than `A/d`. Then

```text
1-c <= -log(1-2A/d)/(Delta^2 log d)
     =2A/[Delta^2 d log d]+O(1/[d^2 log d]).             (5)
```

Thus an `O(1/d)` heat-kernel correction is useful only if the physical bath
approaches a rank-one target-reference covariance with defect
`O(1/(Delta^2 d log d))` for fixed nonzero `Delta`. If `c<1` remains fixed
while `gamma T` grows, the witness in (3) tends to `1/2`.

For the illustrative finite-correlation model

```text
c(r)=exp(-r/ell_B),
```

at fixed target-reference separation `r`, (5) requires

```text
ell_B/r=Omega(Delta^2 d log d).                          (6)
```

Equation (6) is model specific. The invariant result is (4); any proposed local
static-patch bath must supply its own covariance `c(r)` and pass that test.

## Finite-Cell Sufficient Bound

There is also a complementary upper bound. For finitely many cells with bounded
charges `q_(a,i)`, covariance `C`, and ideal all-ones covariance `C_*`, define

```text
L_C=-gamma sum_(a,i,j) C_ij [q_(a,i),[q_(a,j),.]].       (7)
```

The completely bounded commutator estimate

```text
||[A,[B,.]]||_diamond<=4||A|| ||B||
```

and the Duhamel formula between CPTP contraction semigroups give

```text
(1/2)||exp(T L_C)-exp(T L_*)||_diamond
 <= min{1,
    2 gamma T sum_(a,i,j)
      |C_ij-1| ||q_(a,i)|| ||q_(a,j)||}.                 (8)
```

Equation (8) is a sufficient finite-cell covariance-closeness criterion. It
does not apply directly to the unbounded full rotor without a spectral/energy
restriction and a corresponding unbounded-generator theorem.

## Consequence For The Research Program

The finite-time recovery estimate must ultimately have an error budget of the
form

```text
epsilon_physical
 >= epsilon_Haar
    -eta_heat
    -eta_covariance
    -eta_Davies
    -eta_access
    -eta_control.                                       (9)
```

Research Theorem Y controls `eta_heat`. Equations (3)-(8) now make
`eta_covariance` testable from a derived bath kernel. The remaining work is not
to assume a sufficiently collective bath, but to calculate its covariance from
a named local field/worldtube action and determine whether a joint scaling
window exists.

## Claim Boundary

Established:

1. the exact axial visibility law (2);
2. the channel-distance witness (3);
3. the necessary common-mode correlation accuracy (4)-(5);
4. the illustrative exponential-correlation consequence (6);
5. the finite-cell bounded-generator Duhamel estimate (8).

Not established:

1. a static-patch field or material bath producing the required covariance;
2. isotropic `SO(3)` rather than the axial witness;
3. a finite-memory Davies approximation and its error;
4. an unbounded-generator covariance comparison on full `L^2(SO(3))`;
5. a correlation length compatible with observer size, lifetime, energy, and
   gravitational backreaction;
6. novelty beyond the stated application of standard collective-dephasing
   mathematics until the geometric bath calculation is completed.

This is therefore a finite-correlation/common-mode mismatch result, not a
generic locality no-go.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy common-mode-locality-mismatch
PYTHONPATH=. python3 -m unittest tests.test_common_mode_locality_mismatch
```
