# Goal 10: Algebraic ER=EPR Channel Benchmark

Goal 10 pivots from observer-algebra tomography back to ER=EPR. The finite
question is operational:

```text
Does entanglement define a bridge channel, or does the algebraic connectivity
of the entanglement define the channel?
```

## Exact Result

The certificate uses a finite stabilizer family of EPR-pair resources with
named left and right mouth ports:

```text
L_0,...,L_{m-1}, R_0,...,R_{m-1}.
```

A permutation `pi` specifies the algebraic bridge edges

```text
L_i -- R_{pi(i)}.
```

The declared coupling is the standard Clifford teleportation gadget through the
identity mouths:

```text
Q_i + L_i -> R_i.
```

**Theorem.** For this family, the fixed-mouth quantum channel capacity is the
number of fixed points of `pi`. Coarse L/R entropy and EPR min-cut diagnostics
depend only on `m`, so they do not determine the fixed-mouth channel.

## Representative Witness

For `m=2`:

| Model | Algebraic connectivity | Coarse L/R entropy and min-cut | Fixed-mouth capacity |
| --- | --- | --- | --- |
| aligned | `L0-R0`, `L1-R1` | `S(L)=S(R)=mincut(L)=2` | `2` qubits |
| crossed | `L0-R1`, `L1-R0` | `S(L)=S(R)=mincut(L)=2` | `0` qubits |

The crossed model is the exact wrong-mouth control: the probe is transferred,
but to the wrong named right port. Its optimal capacity after right-port relabeling
is still `2`, so the claim is not that entanglement disappeared. The claim is
that coarse entanglement does not specify the named bridge channel.

## Diagnostics

- Entropy/min-cut-visible: coarse L/R entropy, mutual information, and EPR
  min-cut agree for aligned and crossed resources.
- Algebra-visible: the connectivity matrix differs and predicts the declared
  channel.
- Channel-visible: the Pauli transfer matrix to each declared target is either
  identity `(1,1,1)` or zero `(0,0,0)`.
- Control-visible: the crossed resource has the same one-qubit operator size
  but sends probes to off-target mouths. The certificate also records an
  OTOC-like detector signal: the crossed resource lights up the actual wrong
  mouth, not the declared target.

Port-resolved pair entropies do distinguish this simple EPR witness. This is
why the result is a finite channel benchmark against coarse entropy/min-cut
shadows, not a claim that all entropy data are blind.

## Relation To Prior Goals

Goals 1-3 showed that entropy/min-cut shadows can miss reconstruction and
channel-visible structure. Goals 5-9 built observer-algebra tomography. Goal 10
uses that lesson for ER=EPR: a bridge should be tested by an operational channel,
and the relevant finite invariant is the algebraic connectivity of the resource.

## Scientific Interpretation

The finite lesson is: ER=EPR should not be modeled as "amount of entanglement
implies a bridge." The better finite test is whether operator-algebraic
connectivity predicts a recoverable channel under a declared coupling. In this
benchmark it does, exactly.

## Limitations

This is a stabilizer port benchmark, not a continuum-gravity theorem and not a
generic many-body traversable-wormhole simulation. The crossed resource is an
exact wrong-mouth/permutation-scrambling proxy, not a chaotic SYK-like control.
The next harder target is a non-Clifford or tensor-network family where richer
entropy/min-cut diagnostics still collide while algebraic connectivity predicts
channel capacity.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 10 channel certificate | `python3 -m qgtoy er-epr-channel --max-pairs 4` |
| Focused Goal 10 regression | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal10_algebraic_er_epr_channel_benchmark_certificate` |
| JSON certificate index validation | `python3 -m json.tool docs/goal10_algebraic_er_epr_channel_benchmark_certificate_index.json` |
