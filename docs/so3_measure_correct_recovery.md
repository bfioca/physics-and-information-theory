# SO(3) Orientation Risk To Spin-1 Recovery

Status: exact two-sided comparison for the declared measure-and-correct
protocol; arbitrary coherent decoders and higher-spin targets remain open

## Protocol

Measure the orientation of the prepared reference, obtaining `g_hat`, and use
that estimate to correct a spin-1 vector target. If the true orientation is
`g`, the residual channel is

```text
Lambda(rho)=integral p(dh) U_1(h)rho U_1(h)^*,
h=g_hat^-1 g.
```

Let

```text
R_ref=E[sin^2(theta(h)/2)]
```

and let `epsilon_rec=(1/2)||Lambda-identity||_diamond`.

## Two-Sided Bound

The protocol obeys

```text
(8/9) R_ref <= epsilon_rec <= min{1,2 sqrt(R_ref)}.  (1)
```

For the upper bound, convexity of diamond norm and

```text
||U_1(h)-I|| <= 2 sin(theta/2)
```

give `epsilon_rec<=2 E[sin(theta/2)]<=2 sqrt(R_ref)`.

For the lower bound, evaluate the channel on half of a maximally entangled
spin-1 pair. Its entanglement fidelity is

```text
F_e=E[|Tr U_1(h)|^2]/9=E[chi_1(h)^2]/9.
```

Since `chi_1 in [-1,3]` and

```text
1-chi_1^2/9
 =(3-chi_1)(3+chi_1)/9
 >=(8/9) sin^2(theta/2),
```

the Choi trace-distance witness proves the lower half of (1).

Thus a sufficient orientation budget for target recovery error `delta` is

```text
R_ref<=delta^2/4,                              (2)
```

while any achieved error `delta` in this protocol requires
`R_ref<=min(1,9delta/8)`.

## Role In The Tradeoff

Equation (1) closes UO.1b for an operationally explicit vector
estimate-and-correct observer. Substituting (2) into the localized-observer
theorem gives a sufficient design target with

```text
C_req=Omega(delta^-2),
a_min=Omega(sqrt(G/delta))
```

at fixed compactness margins. It does not show that arbitrary coherent
recovery is equivalent to estimation, and it does not yet derive the
orientation POVM from a local Skyrmion/field interaction.

## Reproduction

```bash
PYTHONPATH=. python3 -m unittest tests.test_so3_measure_correct_recovery
```

Artifacts:

- `qgtoy/so3_measure_correct_recovery.py`
- `tests/test_so3_measure_correct_recovery.py`
- `docs/global_so3_reference_risk.md`
- `docs/localized_so3_observer_tradeoff.md`
