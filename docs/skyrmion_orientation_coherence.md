# Skyrmion Matter-Derived Orientation Coherence Gate

Status: exact zero-mode/risk composition under the declared Davies convention;
conservative AU.3a and a tail-dominated authenticated AU.3b baseline are
certified, while useful tail constants, finite-coupling dynamics, switching,
stress, and lifetime remain open

## Rate From The Matter Current

The centered rigid-Skyrmion current and the local pseudoscalar gyroscope action
give the stationary optical spectrum

```text
j_Sky(omega)=j_0(omega) H_Sky(R|omega|)^2.
```

At static lapse `N=sin(rho/R)`, the proper zero-frequency spectrum is

```text
S_prop(0)=N^-3 j_Sky(0).
```

Using the diffusion convention already declared by the gyroscope/Davies model,

```text
gamma_prop=g^2 S_prop(0)=g^2 N^-3 j_Sky(0).             (1)
```

This fixes the rate parameter in the global heat-risk theorem from the same
leading matter current that supplies the spatial form factor. It does not yet
bound the difference between exact reduced dynamics and the Davies/ULE model.

## Projective Risk Evolution

For the fermionic odd Peter-Weyl sector through cutoff `J`, the initial global
risk floor is

```text
r_0=sin^2[pi/(2J+4)].                                  (2)
```

Reference-only isotropic diffusion then implies

```text
R_ref(T)>=3/4[1-exp(-2 gamma_prop T)]
          +r_0 exp(-2 gamma_prop T).                   (3)
```

At target risk `epsilon<3/4`, the necessary coherence ceiling is

```text
T<=gamma_prop^-1/2
   log[(3/4-r_0)/(3/4-epsilon)].                       (4)
```

The same record tracks the loaded weak-coupling diagnostic

```text
mu_Davies=gamma_prop tau_B,prop K_max(K_max+1),
tau_B,prop=N tau_B,opt.                                (5)
```

Small `mu_Davies` is a diagnostic, not a certified error bound.

## Default Audit

For `J=8`, `g=10^-3`, `rho/R=0.2`, and the existing default hard-wall profile,

```text
j_Sky(0)=0.0013526857272251475,
gamma_prop=1.725060857625238e-7,
mu_Davies=2.76743724078367e-6,
r_0=0.024471741852423214,
T_max(epsilon=0.1)=318619.6535716556.
```

These numbers audit the composition and scaling. They are not a physical
prediction because `g`, the optical correlation time, switching, and the
finite-coupling remainder have not all been derived or interval certified.

## Remaining Gate

AU.2 supplies the exact tail envelope and all derivative inputs. AU.3a turns
them into conservative directed global norms. The authenticated AU.3b baseline
is weaker because its joined tail dominates; sharper tail/product bounds and a
separate finite-coupling ULE/Davies error theorem must still be strong enough that
equation (3) survives after subtracting the approximation, switching,
collective-band, and access errors. The final window must also lie below the
Skyrmion stress and lifetime ceilings.

## Reproduction

```bash
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_orientation_coherence
```

Artifacts:

- `qgtoy/skyrmion_orientation_coherence.py`
- `tests/test_skyrmion_orientation_coherence.py`
- `docs/static_patch_skyrmion_bath.md`
- `docs/global_so3_reference_risk.md`
