# Physical Static-Patch Continuum-Lift Hinge

## Purpose

This is the next-phase physics audit. It asks whether a physically natural
static-patch cutoff/coarse-graining structure can make the continuum-lift
obstruction non-artificial.

The answer at this checkpoint is:

```text
C. minimal missing assumption.
```

The finite theorem engine is intact, and two physically motivated bounded
routes remain positive. But the current machinery still lacks a canonical
static-patch refinement that is both screen-compatible and noncommutative in
the observer-algebra sense.

This is not outcome A because no audited candidate is both physically
canonical and lift-complete. It is not outcome B because harmonic and
heat-kernel routes keep the finite obstruction alive. The result is the
minimal missing assumption below.

## Minimal Missing Assumption

```text
there exists a screen-compatible, trace-compatible, approximately covariant
cutoff refinement into a noncommutative observer algebra that is norm-faithful
on a fixed finite nonabelian operator subsystem and compatible with short-time
modular/heat locality
```

This is stronger than "screen shadows converge" and weaker than assuming the
full observer algebra by fiat. It names the exact bridge from finite
diagnostics to a physically meaningful static-patch/operator-algebra theorem.

## Candidate Audit

| Candidate | Status | Main Lesson |
| --- | --- | --- |
| Berezin-Toeplitz / fuzzy-sphere symbol-quantization | conditional | Pure symbols land in a commutative screen and lose commutators; a quantization-side noncommutative operator system must remain accessible. |
| Spherical-harmonic projection/refinement | bounded positive | Low-harmonic diagonal data are preserved and the operator-norm witness survives in the low-mode corner, but this is not yet a canonical static-patch embedding. |
| Heat-kernel coarse graining | bounded positive | CP/unital heat kernels preserve screen data and retain response under double-scaled short-time locality; canonical static-patch dynamics remain conditional. |
| Modular/KMS conditional expectations | no-go unless localized | KMS covariance/detailed balance alone allows stationary twirling or fixed-width averaging, which can erase the noncommutative witness. |
| Coherent-state/fuzzy-sphere refinement | conditional | A coherent-state screen map can be natural, but a symbol-only route is commutative; norm-faithful quantized operator data are required. |
| Common continuum `L^2(S^2)` / screen embedding | no-go for observer algebra | This is natural for screen shadows but cannot determine the noncommutative observer algebra because the target is commutative. |

## Gate Matrix

Statuses are deliberately coarse:

| Status | Meaning |
| --- | --- |
| `pass` | The current finite certificate supports the gate under its declared scope. |
| `conditional` | The gate is plausible or bounded, but depends on an additional continuum/static-patch choice. |
| `fail` | The candidate fails the gate as a route to observer-algebra recovery. |

| Candidate | CP/trace | Multiplicative | Covariant | Screen | Response | Continuity | Type-II route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Berezin-Toeplitz | conditional | conditional | conditional | conditional | conditional | conditional | conditional |
| Spherical harmonic refinement | pass | pass | conditional | pass | pass | conditional | conditional |
| Heat-kernel coarse graining | pass | pass | pass | pass | pass | conditional | conditional |
| Modular/KMS expectations | conditional | fail | pass | pass | fail | fail | conditional |
| Coherent-state refinement | conditional | conditional | conditional | conditional | conditional | conditional | conditional |
| Common `L^2(S^2)` screen | pass | fail | pass | pass | fail | fail | fail |

The matrix is the main decision object. Screen-only routes can pass the screen
gate while failing response and Type-II gates. Harmonic and heat routes pass
the finite response gate, but still leave the canonical static-patch
continuum route conditional.

## Theorem Candidate Under The Missing Assumption

If the minimal missing assumption holds, then the existing continuum-lift
obstruction theorem applies:

```text
screen-only static-patch data cannot determine the observer algebra whenever
the noncommutative operator-response witness persists in the lift.
```

## No-Go Content

Two no-go lessons are already sharp:

1. KMS/modular covariance alone is insufficient. Stationary modular twirling
   and fixed-width modular averaging can satisfy screen/KMS-looking
   conditions while failing the strong-continuity/response requirement.
2. A common commutative continuum screen, such as `L^2(S^2)` or `C(S^2)`, can
   organize screen shadows but cannot recover a noncommutative observer
   algebra without extra operator-system data.

## What Would Upgrade This To Outcome A

Any one candidate would upgrade the result from C to A if it supplied a
physically motivated family of maps that:

1. is CP/unital/trace-compatible, or has controlled nonunitarity;
2. is asymptotically multiplicative on the low-mode sector;
3. is approximately covariant under the intended static-patch/fuzzy-sphere
   symmetries;
4. preserves the declared screen-shadow equivalence;
5. is norm-faithful on a fixed finite nonabelian operator subsystem;
6. is compatible with cutoff-local short-time modular/heat dynamics;
7. has a noncommutative operator-algebra limit route.

The current certificate shows that the finite parts of this list are not the
obstruction. The missing input is the canonical noncommutative refinement.

## Claim Boundary

This is not a continuum de Sitter theorem, a dS/CFT construction, or an
ER=EPR proof. It is a physics-hinge audit that identifies the weakest
non-tautological assumption currently needed to promote the finite obstruction
into a physically natural static-patch theorem.

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy physical-static-patch-lift --max-cutoff 5
```

Run the focused regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_physical_static_patch_lift
```
