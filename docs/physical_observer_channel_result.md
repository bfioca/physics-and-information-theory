# Physical Observer Channel: Exact Finite Result And ER=EPR Stop

**Decision: RETAIN the exact finite observer-channel theorem; STOP the ER=EPR
extension on this action.**

The sprint succeeded at its literal target. A finite pointer register, matter
projector, and finite environment are now coupled by one piecewise local action.
Tracing out the environment gives an exactly soluble approximation to the
binary observer-decoherence channel, and the same action implements a
sectorwise-local relational patch measurement. Entropy, duration, energy,
complexity, localization, and a declared spherical backreaction envelope are
all explicit.

It did not produce a connectivity observable. Matched Bell and separable
controls are distinguishable with a two-setting entanglement witness, but that
is ordinary entanglement detection, not a bridge, area, QES, topology, or
operator-algebra connectivity result. The ER=EPR promotion gate therefore
fails cleanly. The finite channel theorem is useful infrastructure, but the
controlled-unitary dephasing mechanism is too standard to be a standalone
quantum-gravity paper without a continuum implementation or a new resource
obstruction.

## 1. Target And Literature Boundary

Harlow, Usatyuk, and Zhao propose an observer-effective description with a
finite entropy and errors suppressed with observer entropy in
[*Quantum mechanics and observers for gravity in a closed
universe*](https://arxiv.org/abs/2501.02359). Engelhardt, Gesteau, and Harlow
write the ideal pointer-basis observer channel explicitly in
[*Observer complementarity for black holes and
holography*](https://arxiv.org/abs/2507.06046):

```text
C_Ob(|a><b|) = delta_ab |a><a|.                         (PO.1)
```

Harlow's [*Observers, alpha-parameters, and the Hartle-Hawking
state*](https://arxiv.org/abs/2602.03835) further motivates observables whose
locations are defined relative to an observer. Those works motivate the two
targets here: physically realize (PO.1), and make the measured patch
observer-relative.

This note does **not** claim to derive their gravitational path integrals,
observer entropy `S_Ob`, or closed-universe interpretation. Finite
controlled-unitary dilations of dephasing channels are standard quantum
information. The repository contribution is the same-action construction,
exact error formula, complete declared resource ledger, and binding
connectivity control.

## 2. Frozen Finite Model

There are two classical observer-location sectors, `A` and `B`. The total
space is a direct sum of two local laboratory sectors, rather than a coherent
location qubit controlling a remote interaction. In those sectors define

```text
Q_rel = |A><A| tensor Q_A tensor I_B
      + |B><B| tensor I_A tensor Q_B,                  (PO.2)
```

where `Q_A` and `Q_B` are binary projectors supported in their respective
worldtubes. A pointer qubit `P` starts in `|0>`, and `m` environment qubits
start in `|+>^m`.

The single action has disjoint acquisition and decoherence switching windows:

```text
H(t) = chi_acq(t) g Q_rel tensor X_P
     + chi_dec(t) lambda Pi_1^P tensor sum_j Z_Ej.     (PO.3)
```

Choose

```text
g tau = pi/2,                 lambda T = theta,
0 <= theta <= pi/2.                                   (PO.4)
```

The acquisition unitary is

```text
U_acq = (I-Q_rel) tensor I_P - i Q_rel tensor X_P,    (PO.5)
```

so the binary patch value is copied exactly to the pointer, up to an
irrelevant branch phase. The simultaneous swap `A <-> B` exchanges the two
terms in (PO.2), hence fixes `Q_rel` and the action. Locality and covariance
are exact on this finite direct-sum domain.

## 3. Observer-Channel Theorem

**Theorem PO.1 (finite pointer-worldtube realization).** Under (PO.2)-(PO.4),
tracing out the environment produces the pointer channel

```text
D_kappa([[a,b],[c,d]]) = [[a,kappa b],[kappa c,d]],
kappa = cos(theta)^m.                                  (PO.6)
```

Let `D_0` be the ideal channel (PO.1). With the standard halved diamond
distance,

```text
(1/2)||D_kappa-D_0||_diamond = |kappa|/2.              (PO.7)
```

The same equality holds between the coherent matter-pointer premeasurement
followed by `D_kappa` and its fully dephased measurement instrument.

**Proof.** Conditional on pointer state `|1>`, each environment qubit acquires
`exp(-i theta Z)`. Its overlap with the unrotated `|+>` state is `cos(theta)`,
so the `m`-qubit overlap is (PO.6). Moreover,

```text
D_kappa-D_0 = (kappa/2)(id-Ad_Z).                      (PO.8)
```

The identity and `Z` unitary channels are perfectly distinguishable, giving
the unhalved norm `|kappa|`. Pre- and post-composition bound the instrument
distance by the same value, while a superposition of the two `Q_rel`
eigenspaces saturates it. This proves (PO.7). `square`

At fixed `0<theta<pi/2`, target error `0<epsilon<1/2` requires exactly

```text
m >= ceiling[log(2 epsilon)/log(cos theta)].           (PO.9)
```

At `theta=pi/2`, one environment qubit gives exact reduced dephasing. This is
not fundamental irreversibility: the joint pointer-environment action remains
unitary and can be reversed by an agent controlling the environment.

One useful subtlety is now explicit. Exact acquisition already gives the
correct diagonal pointer probabilities after matter is traced out. The
environment is needed to suppress coherent pointer blocks in the joint
premeasurement state, not to repair the Born probabilities.

## 4. Entropy And Action Ledger

For a `|+>` pointer diagnostic, the reduced pointer eigenvalues are

```text
p_plus/minus = (1 +/- |kappa|)/2,                      (PO.10)
```

and therefore

```text
Tr rho_P^2 = (1+kappa^2)/2,
S_2(P) = -log[(1+kappa^2)/2],
S(P) = h_2[(1+|kappa|)/2].                             (PO.11)
```

Because the pointer-environment state is pure, `S(E)=S(P)` and
`I(P:E)=2S(P)`. These are entropies of one model record. The calculation makes
no identification between them and Harlow's thermodynamic `S_Ob`.

The acquisition duration is `tau=pi/(2g)`. If all commuting environment terms
act in parallel, the decoherence duration is `theta/lambda` and peak
interaction norm is `max(g,m lambda)`. A serial two-body schedule instead has
duration `m theta/lambda` and peak norm `max(g,lambda)`. Both have

```text
integral ||H(t)|| dt = pi/2 + m theta.                 (PO.12)
```

Per realized observer sector, the gate count is one controlled acquisition
plus `m` controlled phase gates. The serial depth is `m+1`; with simultaneous
commuting environment couplings the depth is two. Two separated copies have
twice the gate count and retain depth two when operated in parallel.

The default replay uses `m=4`, `theta=pi/3`, and `g=lambda=1`. It gives

```text
kappa                         = 1/16
halved diamond distance       = 1/32
parallel duration             = 5 pi/6
parallel peak norm            = 4
serial duration               = 11 pi/6
serial peak norm              = 1
integrated interaction norm   = 11 pi/6
S(P)                          = 0.9971803989 bits.
```

## 5. Localization, Energy, And Backreaction Ledger

All matter, pointer, and environment terms are declared to lie in one
worldtube of areal radius `a<R`. On the fixed de Sitter background,

```text
proper support radius  = R asin(a/R),
optical support radius = R atanh(a/R),
wall redshift           = sqrt(1-a^2/R^2).             (PO.13)
```

The channel calculation sets free Hamiltonians to zero. The gravity ledger
separately declares positive matter, pointer, and environment mass-energy
budgets and adds the peak interaction norm as a conservative source envelope
`E_env`. This is a ledger assumption, not a stress-tensor derivation.

For one explicit spherical embedding, take

```text
m(r) = E_env (r/a)^3,                 0<=r<=a.         (PO.14)
```

The exact time-symmetric spherical constraint variable is

```text
q(r) = 2Gm(r)/[r(1-r^2/R^2)].                         (PO.15)
```

For (PO.14), `q(r)` is monotone and its supremum is

```text
q_max = 2G E_env/[a(1-a^2/R^2)].                      (PO.16)
```

If `q_max<=beta<1`, the exact spherical constraint result already in this
repository gives positive radial metric factor and relative radial metric
distortion at most `beta/(1-beta)`.

The default parallel schedule declares three units of rest/support energy and
four units of peak interaction envelope. With `a=0.2`, `R=1`, and `G=0.001`,

```text
E_env                         = 7
q_max                         = 0.07291666667
radial metric distortion cap  = 0.07865168539
proper support radius         = 0.2013579208
optical support radius        = 0.2027325541.
```

This closes a precise *declared spherical ledger*, not self-consistent
Einstein-matter dynamics. The channel Hamiltonian has not been derived from
the profile's stress tensor; pressure, lapse, junction, stability, and the
nonspherical two-worldtube geometry remain open.

## 6. Matched Two-Region Controls

Apply two copies of the same local action to

```text
rho_ent = |Phi+><Phi+|,
rho_sep = (|00><00|+|11><11|)/2.                      (PO.17)
```

The states have the same maximally mixed local marginals, the same energy for
any equal one-site Hamiltonians, the same declared per-worldtube gravity
ledger, and the same `Z tensor Z` transcript:

```text
p(00)=p(11)=1/2,             p(01)=p(10)=0.            (PO.18)
```

Thus a single `Z` patch setting has exactly zero entanglement-specific
contrast. A second local setting gives the standard witness

```text
W = [<X tensor X>+<Z tensor Z>]/2.                    (PO.19)
```

For separable states `W<=1/2` by the Bloch-vector Cauchy-Schwarz inequality and
convexity. The Bell control gives `W=1`; the matched separable control gives
`W=1/2`. The witness gap is therefore `1/2`.

This nonzero number does not pass the ER=EPR gate. Equations (PO.2)-(PO.3)
define no area, extremal surface, topology, bridge algebra, reconstruction
region, or other signed connectivity variable. The same action therefore has

```text
entanglement-witness contrast       = 1/2
derived connectivity contrast       = undefined
ER=EPR decision                     = STOP.            (PO.20)
```

Relabeling `W` as connectivity would be the overclaim the matched-control gate
was designed to prevent.

## 7. What Is Proved, And What Would Make It A Paper

**Proved on the finite declared domain**

1. One sectorwise-local action exactly acquires a binary relational patch
   projector and induces (PO.6).
2. Its distance to ideal observer dephasing is exactly (PO.7), with resource
   inversion (PO.9).
3. The entropy, duration, peak norm, integrated action, gate count, support,
   redshift, and spherical constraint envelope are explicit.
4. Matched Bell and separable controls isolate a genuine entanglement witness
   while ruling out a connectivity claim for this action.

**Not proved**

1. `S_model=S_Ob`, closed-universe irreversibility, or a microscopic origin of
   the Harlow observer rule.
2. A continuum local-QFT detector with gravitational dressing.
3. A self-consistent stress tensor and Einstein-matter solution for the same
   channel action.
4. Any algebraic or geometric ER=EPR dictionary.

The best publication upgrade is now narrow and concrete: replace `Q_A` and
`Q_B` by observer-conditioned smeared QFT operators in a named static-patch
model, derive the pointer/environment channel and source stress tensor from
that same action, and test a predeclared algebraic-connectivity observable on
the matched controls. A nonzero ordinary entanglement witness is not enough.

## 8. Reproduction

```bash
PYTHONPATH=. python -m pytest -q tests/test_physical_observer_channel.py
PYTHONPATH=. python experiments/physical_observer_channel_audit.py
python -m json.tool \
  experiments/physical_observer_channel_certificate.json >/dev/null
```

The frozen default certificate is
`experiments/physical_observer_channel_certificate.json`. Its binding status
is `pass_observer_channel_stop_er_epr`.
