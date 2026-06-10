# Operational Finite Phase Reference

Status: exact prepared-reference append/twirl/decode theorem for `U(1)`

## Physical Task

The system has charges `m=-L,...,L`. Prepare one fixed finite reference state

```text
|eta_N> = (N+1)^(-1/2) sum_{n=0}^N |n>.
```

For an unknown system state `rho`, append `|eta_N>`, apply the joint `U(1)`
twirl, and decode within each conserved total-charge sector `q`:

```text
|m,q-m> -> |m>_logical tensor |q>_flag.
```

Tracing the flag is an allowed sectorwise decoder. Unlike the singlet-code
baseline, the encoder here is the fixed physical channel
`rho -> rho tensor |eta_N><eta_N|` followed by the symmetry reduction.

## Exact Channel

The matrix element `rho_{m,m'}` survives in exactly

```text
max(0,N+1-|m-m'|)
```

total-charge sectors. The decoded logical channel is therefore

```text
rho_{m,m'} -> v_{m-m'} rho_{m,m'},
v_Delta = max(0,1-|Delta|/(N+1)).
```

The visibility matrix is the Gram matrix of shifted uniform reference windows,
so the Schur multiplier is completely positive; its unit diagonal makes the
channel trace preserving.

## Sharp Phase-Pair Error

For

```text
|psi_+/- > = (|m> +/- |m'>)/sqrt(2),
```

the decoded outputs have trace distance `v_Delta`. Contractivity and the
triangle inequality imply that every decoder has worst-case trace-distance
error at least

```text
(1-v_Delta)/2.
```

The sector decoder attains that value on both phase states, so it is minimax
optimal for this two-state task.

For the extremal gap `|Delta|=2L`,

```text
error = 1/2,       N < 2L,
error = L/(N+1),   N >= 2L.
```

Thus, within the uniform boxcar family, target error `epsilon<1/2` requires and
is achieved by

```text
dim(reference)=N+1 >= ceil(L/epsilon).
```

No finite uniform charge window gives exact recovery of a nonzero charge
coherence.

## Pairwise-Optimal Reference Profile

The linear `L/epsilon` boxcar cost is not fundamental. For one selected charge
gap `Delta`, maximizing visibility at fixed maximum reference charge `N` is a
path-graph eigenvalue problem. The charges split into step-`Delta` chains. If

```text
r = floor(N/|Delta|)+1,
```

the optimal reference is the sine eigenvector on a longest chain and has

```text
v_opt = cos(pi/(r+1)),
error_opt = [1-cos(pi/(r+1))]/2.
```

For the extremal gap `|Delta|=2L`, this gives asymptotic pairwise error
`Theta((L/N)^2)` and maximum-charge cost `Theta(L/sqrt(epsilon))`. This is an
exact pairwise optimum under the maximum-charge cutoff, not a simultaneous
optimum for every coherence in the full spin sector.

## Claim Boundary

This closes the operational gap for an axial `U(1)` phase reference and one
sharp pairwise minimax task. The triangular attenuation law is a standard
finite-reference phenomenon, and the sine-profile optimization is standard
spectral machinery; neither is by itself a novelty claim. The next physics
theorem must derive the analogous channel and optimal resource law for a full
`SU(2)` directional reference, then place that reference inside the local
static-patch KMS/crossed-product model. A full-space or diamond-norm optimum,
reference energy cost, de Sitter boosts, and generalized entropy remain open.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy operational-phase-reference --max-level 8
PYTHONPATH=. python3 -m unittest tests.test_operational_phase_reference
```
