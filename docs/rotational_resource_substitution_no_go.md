# Rotational Resource Substitution No-Go

Status: exact kinematic theorem; the localized energy and gravity bridge remains open

## Result

For every spin `j>1`, consider

```text
|cat_j>=(|j,j>+|j,-j>)/sqrt(2).
```

Its mean angular momentum vanishes. Direct ladder-operator evaluation gives

```text
Cov(J_x,J_y,J_z)=diag(j/2,j/2,j^2).
```

For the pure rotational orbit, `F_ab=4 Cov(J_a,J_b)`, so

```text
F=diag(2j,2j,4j^2),
Tr(F)=4j(j+1).
```

The QFI is full rank and grows quadratically even though `|<J>|=0`. Therefore a
classical body inequality controlling only mean angular momentum cannot bound
the rotational sensitivity needed by the observer theorem.

Now compare the maximally mixed state on the same spin irrep. It has the same
Casimir `J^2=j(j+1)` and the same energy under an isotropic rotor Hamiltonian,
but it is rotation invariant and has zero QFI. Therefore large Casimir or rotor
energy alone does not certify orientation quality.

The only safe chain for the universal program is one-way:

```text
small global orientation risk
    -> large rotational QFI
    -> large angular-momentum second moment
    -> localized energy and gravity cost.
```

The first and final arrows remain theorem gates. This result proves that they
cannot be replaced by a mean-charge bound or by treating Casimir as reference
quality.

## Rare-Tail QFI Failure

Local QFI also cannot be used as global quality without a tail hypothesis. For
integer `j>=2`, define the pure reducible state

```text
|psi_j>=sqrt(1-1/j)|0,0>+sqrt(1/j)|cat_j>.
```

Its mean linear spin cost is exactly one, while

```text
Tr(F)=4(j+1).
```

Nevertheless every rotated state is at trace distance exactly `1/sqrt(j)`
from the invariant spin-zero state. The complete rotation orbit therefore
converges uniformly to an uninformative state while its local QFI diverges.

This changes the preferred theorem route:

```text
small global orientation risk
 -> robust typical-spin or global asymmetry resource
 -> localized energy and gravity cost.
```

QFI remains useful only with a hard spectral budget, an energy-variance bound,
or another condition excluding vanishing high-spin tails.

## Scope

This is a kinematic finite-dimensional statement. Local QFI does not by itself
remove global discrete orientation ambiguities, so the primary theorem still
needs a covariant Bayesian or minimax risk bound. The certificate also does not
derive a stress-energy, size, or backreaction inequality.

Primary context:

- Kudo and Tajima, [Fisher Information Matrix as a Resource Measure in Resource
  Theory of Asymmetry](https://arxiv.org/abs/2205.03245).
- Goldberg and James, [Quantum-Limited Euler Angle Measurements Using
  Anticoherent States](https://arxiv.org/abs/1806.02355).
- Dain, [Inequality Between Size and Angular Momentum for
  Bodies](https://arxiv.org/abs/1305.6645).

Reproduce with:

```bash
PYTHONPATH=. python3 -m unittest tests.test_rotational_resource_substitution_no_go
```
