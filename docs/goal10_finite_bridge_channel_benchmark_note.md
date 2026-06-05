# Goal 10: Finite Bridge-Channel Benchmark

Goal 10 builds a finite bridge-channel benchmark for algebraic ER=EPR
diagnostics. The finite question is operational:

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

**Theorem.** For this family, the number of perfect named-port product channels
under the identity decoder is the number of fixed points of `pi`. This is not a
quantum-capacity formula. Coarse L/R entropy and EPR min-cut diagnostics depend
only on `m`, so they do not determine the named-port channel.

The channel is now constructed from the Bell-projection and feed-forward Kraus
operators. The certificate checks trace preservation, Choi rank, Pauli
transfer, entanglement fidelity, and the preserved operator algebra.

## Representative Witness

For `m=2`:

| Model | Algebraic connectivity | Coarse L/R entropy and min-cut | Perfect fixed ports |
| --- | --- | --- | --- |
| aligned | `L0-R0`, `L1-R1` | `S(L)=S(R)=mincut(L)=2` | `2` qubits |
| crossed | `L0-R1`, `L1-R0` | `S(L)=S(R)=mincut(L)=2` | `0` qubits |

For the crossed model with the identity decoder, the simultaneous two-qubit
channel is the correlated `II/XX/YY/ZZ` twirl. It has no perfect fixed-port
qubit and no quantum noiseless subsystem, but preserves a two-generator
classical center. The pairing-aware decoder is exactly the identity channel.

## Diagnostics

- Entropy/min-cut-visible: coarse L/R entropy, mutual information, and EPR
  min-cut agree for aligned and crossed resources.
- Algebra-visible: the connectivity matrix differs and predicts the declared
  channel.
- Channel-visible: explicit Choi and Pauli-transfer diagnostics distinguish the
  identity channel from the correlated crossed-mouth twirl.
- Structural-control visible: the crossed resource has the same one-qubit
  pair-generator weight but different named resource connectivity. Dynamics
  are reported only by the explicit channel calculation.

Port-resolved pair entropies do distinguish this simple EPR witness. This is
why the result is a finite channel benchmark against coarse entropy/min-cut
shadows, not a claim that all entropy data are blind.

## Relation To Prior Goals

Goals 1-3 showed that entropy/min-cut shadows can miss reconstruction and
channel-visible structure. Goals 5-9 built observer-algebra tomography. Goal 10
uses that lesson for bridge-channel diagnostics: a bridge should be tested by
an operational channel, and the relevant finite invariant is the algebraic
connectivity of the resource.

## Relation To Engelhardt-Liu

Engelhardt and Liu's
["Algebraic ER=EPR and Complexity Transfer"](https://arxiv.org/abs/2311.04281)
is the primary conceptual prior art for the broad claim that ER=EPR should
depend on operator-algebraic entanglement structure, not just entanglement
amount. Goal 10 does not propose that framework. It gives a finite stabilizer
bridge-channel benchmark certificate inside that conceptual neighborhood: coarse entropy and
min-cut shadows match, while a named channel depends on the resource's
connectivity matrix.

## Scientific Interpretation

The finite lesson is: bridge-channel behavior should not be modeled as "amount
of entanglement implies a bridge." The better finite test is whether operator-algebraic
connectivity predicts a recoverable channel under a declared coupling. In this
benchmark it does, exactly.

## Limitations

This is a stabilizer port benchmark, not a continuum-gravity theorem and not a
generic many-body traversable-wormhole simulation. The crossed resource is an
exact wrong-mouth/permutation-scrambling proxy, not a chaotic SYK-like control.
The next harder target is a non-Clifford or tensor-network family where
complete entropy data collide while operator algebra predicts an operational
recovery distinction.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 10 channel certificate | `PYTHONPATH=. python3 -m qgtoy er-epr-channel --max-pairs 4` |
| Focused Goal 10 regression | `PYTHONPATH=. python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal10_finite_bridge_channel_benchmark_certificate` |
| JSON certificate index validation | `python3 -m json.tool docs/goal10_finite_bridge_channel_benchmark_certificate_index.json` |
