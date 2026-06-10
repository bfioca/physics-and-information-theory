# Harlow Review Packet: Claim-Evidence Ledger

Status: external-claim audit, 2026-06-10

This ledger governs the wording of the Harlow review packet. It distinguishes
the exact mathematics already established in the repository from assumptions
of an effective model, floating design evidence, and genuinely missing
physical bridges. A composite sentence inherits the least-complete status of
its ingredients.

## Status vocabulary

- **[PROVED]** means an analytic or computer-assisted theorem is established
  on the explicitly stated domain. It does not license a broader physical
  interpretation.
- **[CONDITIONAL]** means either an exact implication assumes a stipulated
  effective channel/model, or a physical construction is supported only by
  source-bound floating numerics. The condition must appear in the same
  paragraph as the claim.
- **[OPEN]** means the required implication, norm estimate, interval
  certificate, or physical identification has not been established.

`S_dir`, effective record dimension, Casimir, QFI, thermodynamic entropy, and
the observer entropy `S_Ob` are distinct quantities throughout. Likewise,
classical record stability is not quantum-state coherence, measurement
back-action is not gravitational backreaction, and fixed-background response
is not self-consistent gravity.

## Executive claim state

| ID | Status | Conservative external wording | Evidence and exact boundary |
| --- | --- | --- | --- |
| E1 | **[PROVED]** | The repository proves global, tail-robust resource lower bounds for a Haar-prior relational `SO(3)` alignment task. | Research Theorem W3 in `THEOREMS.md`; `docs/global_so3_reference_risk.md`; `qgtoy/global_so3_reference_risk.py`; `tests/test_global_so3_reference_risk.py`. This is a full-frame Bayes-risk theorem, not an observer-entropy theorem. |
| E2 | **[PROVED]** | Within named matter classes, localization and energy constrain the rotational resource entering those alignment bounds. | Research Theorems W3a and W3b; `docs/localized_orbital_reference.md`; `docs/supported_skyrmion_collective_spectral_floor.md`; focused tests. The orbital result is nonrelativistic and spinless; the Skyrmion result concerns the supported adiabatic collective hedgehog family, not the complete rotating field spectrum. |
| E3 | **[CONDITIONAL]** | A stipulated isotropic heat channel gives an exact degradation law for the relational orientation score and an abstract capacity-lifetime compatibility inequality. | W3, W3a.1, W4, W6, and Y. The physical heat channel, preparation, access, and readout have not all been derived from the Skyrmion action. |
| E4 | **[OPEN]** | Whether one localized matter system acquires, stores, and exposes an operational classical directional record through one norm-controlled microscopic interaction is the primary missing bridge. | Y2 and the finite-switch ULE results specify the norms needed, but there is no physical-to-heat diamond estimate, autonomous preparation/readout protocol, positive physical coupling window, or common stress ledger. |
| E5 | **[PROVED]** | On fixed pure de Sitter, the repository has exact static `ell=2` master-source, transmission, and exterior electric-Weyl reconstruction formulas. | W3m, W3t, W3v, and W3x. These are exact maps and convention checks; they do not prove that the completed Skyrmion sources a nonzero continuum amplitude. |
| E6 | **[CONDITIONAL]** | Source-bound floating calculations give a stable nonzero completed Skyrmion master/Weyl target near `-2.8e-3`, and the response has been reduced to one scalar exterior amplitude. | W3u-W3x and W3z.17; floating feasibility artifact SHA256 `584a22ea3ae9807dcc9da8cd6cc20274c943c52bb23c38923cbe8e6dcf986bf7`. It is design evidence, not the publishable zero-exclusion result. |
| E7 | **[OPEN]** | The current fixed-background Skyrmion Weyl interval does **not** exclude zero. No positive lower bound `|B_W| >= b_min > 0` is presently proved. | W3z.17 and W3z.21-W3z.29. The regular-origin adjoint master load is absent, and the certified partial adjoint dual bound is too broad for zero exclusion. |
| E8 | **[PROVED]** | A computer-assisted theorem establishes a local, strictly decreasing hard-wall Skyrmion profile with negative wall slope and finite positive inertia at the declared fixed-background parameters. | AU.1; exact profile artifact SHA256 `c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff`. This is not a rotating or self-gravitating solution. |
| E9 | **[OPEN]** | `S_dir=A_SO3` has not been identified with Harlow's observer entropy `S_Ob`, a generalized entropy, or a thermodynamic memory entropy. | The repository proves operational inequalities for `A_SO3`; no theorem supplies the `S_dir`-to-`S_Ob` dictionary. This is review question 1, not a conclusion. |
| E10 | **[OPEN]** | The proposed one-action observer tradeoff and a self-consistent rotating Einstein-Skyrme-de Sitter observer are not yet proved. | The common physical channel, interval Weyl zero exclusion, background/membrane matching, and common parameter window remain incomplete. |

## Observer-register claims

| ID | Status | Claim allowed in the packet | Evidence | Required qualification |
| --- | --- | --- | --- | --- |
| O1 | **[PROVED]** | For Haar-distributed relative orientation and chordal full-frame cost, every state and POVM obey `R_ref >= 1/(16 <J^2>+8)`. | W3; `docs/global_so3_reference_risk.md`; `tests/test_global_so3_reference_risk.py`. | The task estimates the group element aligning two physical frames. Do not call it absolute orientation or a local-QFI bound. |
| O2 | **[PROVED]** | With `S_dir:=A_SO3(rho)=D(rho||G_SO3(rho))`, `R_ref >= c_SO3 exp(-2 S_dir/3)`, where `c_SO3=6/(e*pi^(5/3))`; therefore achieving `R_ref<=epsilon<c_SO3` requires `S_dir >= (3/2)log(c_SO3/epsilon)`. | W3 and the Holevo/data-processing derivation in `docs/global_so3_reference_risk.md`. | `S_dir` is an operational asymmetry resource for this covariant ensemble. It is not automatically a memory size, thermodynamic entropy, or `S_Ob`. |
| O3 | **[PROVED]** | A mean-spin Gibbs envelope and, under finite sector partition function, an energy Gibbs envelope upper-bound `A_SO3`. | W3 and W3a; `qgtoy/global_so3_reference_risk.py`; `qgtoy/rotational_spectral_capacity.py`. | Covariance and finite mean energy alone are insufficient; the sector-floor premise is essential. |
| O4 | **[PROVED]** | For the declared spin-1 measure-and-correct protocol, `(8/9)R_ref <= epsilon_rec <= min(1,2 sqrt(R_ref))`. | W5; `docs/so3_measure_correct_recovery.md`; `tests/test_so3_measure_correct_recovery.py`. | This does not cover arbitrary coherent decoders and does not derive the POVM/readout from a local interaction. |
| O5 | **[OPEN]** | No general theorem presently converts `S_dir` into an effective classical record dimension or `S_Ob`. | The Harlow-facing goal G2 explicitly leaves this dictionary open. | The packet may ask whether such a comparison is meaningful; it must not assert one. |
| O6 | **[PROVED]** | For confined spinless nonrelativistic orbital matter satisfying the stated quadratic-form hypothesis, `<L^2> <= 2 M a^2 E_ex`, hence `R_ref >= 1/(32 M a^2 E_ex+8)`. | W3a; `docs/localized_orbital_reference.md`; `tests/test_localized_orbital_reference.py`. | Excludes intrinsic spin, relativistic fields, soft support, and negative interaction energy. The separate compactness line is a declared proxy, not a GR body theorem. |
| O7 | **[PROVED]** | For hard-supported hedgehog profiles in the adiabatic collective family, `I <= [4/(3N_w)] M a^2`, giving a sector floor linear in large spin and a finite rotational partition function. | W3b; `docs/supported_skyrmion_collective_spectral_floor.md`; `tests/test_supported_skyrmion_collective_spectral_floor.py`. | Collective-band completeness, projection error, noncollective modes, isospin access, and a marked rotating wall are open. |
| O8 | **[PROVED]** | If a declared observer class supplies `C2<=C_max`, a support map, and heat exposure `Gamma`, then the abstract risk bound in W3a.1 follows. | `experiments/universal_observer_tradeoff_certificate.json`, SHA256 `5c88eb4af23764204333b5e899083c87911066895d70fc132f263e180c175ad6`; `tests/test_universal_observer_tradeoff.py`; audit test. | This is an exact implication, not evidence that one physical observer supplies all premises. |
| O9 | **[CONDITIONAL]** | Under reference-only isotropic heat diffusion, `R_ref(T)` obeys the exact exponential interpolation between its initial floor and `3/4`. | W3, W6, and Y; `tests/test_finite_time_rotation_diffusion.py`; `tests/test_skyrmion_orientation_coherence.py`. | Call this an effective heat-model degradation law, not a measured lifetime or an action-derived record channel. |
| O10 | **[CONDITIONAL]** | The leading rigid-Skyrmion current fixes the zero-frequency form factor and, under the declared Davies convention, the rate parameter `gamma_prop=g^2 N^-3 j_Sky(0)`. | W6; `docs/skyrmion_orientation_coherence.md`; `qgtoy/skyrmion_orientation_coherence.py`. | The exact reduced dynamics, switching, collective projection, local access, finite-coupling error, stress, and lifetime are not controlled together. |
| O11 | **[CONDITIONAL]** | AU.3a supplies rigorous global Sobolev inputs and AU.3b authenticates a profile-resolved spectral pipeline; a prescribed-switch ULE gives an ancilla-stable state operator-norm residual. | AU.3a artifact SHA256 `b6a9931cc50359ec4a9bed7a6d3443471f39b39f60c37e3a92d39073ba0cc55c`; AU.3b artifact SHA256 `bc6cf2ea21f44c122001fcc3f7fa6cffb9983d4ec4e35591323aa2d29b25c529`; `docs/validated_skyrmion_ule.md`. | The residual is not a physical channel diamond distance. The reported coupling lower bound is zero, so the formal nonempty interval is not a physical window. |
| O12 | **[OPEN]** | Preparation, storage, and readout from one local action with `eta_channel` below the operational risk margin remain unproved. | Harlow-facing gate G3; Y2; `docs/static_patch_matter_observer_channel.md`. | This must be called the primary conceptual bottleneck. |
| O13 | **[PROVED]** | In the named Bunch-Davies scalar/gradient effective models, nonzero optical separation prevents perfectly common rotational noise. | Theorems Z, AA-AC; `docs/common_mode_locality_mismatch.md`; `docs/static_patch_scalar_common_mode.md`; `docs/static_patch_radial_smearing.md`. | These are coupling-specific locality results, not a theorem over all fields, multipoles, controls, or full `SO(3)` record protocols. |
| O14 | **[OPEN]** | Operational stability of a classical relational record has not yet been derived from acquisition through readout. | The existing exact results concern orientation risk, measure-and-correct recovery, or stipulated diffusion. | Do not replace this gap with the phrase "long quantum coherence." |

## Gravitational-witness claims

| ID | Status | Claim allowed in the packet | Evidence | Required qualification |
| --- | --- | --- | --- | --- |
| G1 | **[PROVED]** | The fixed-pure-de-Sitter static `ell=2` operator has an exact positive Green kernel and `A_2>=6/R^2`. | W3m; `experiments/static_patch_l2_response_exact_certificate.json`, SHA256 `45871bfe3e15a65b546eddd6391d42d0d8e6665ee981c9f24618409f52dcd051`. | This acts on a valid conserved master source; density alone is insufficient. |
| G2 | **[PROVED]** | The undeformed fixed-profile rigid rotational stress fails the exact static conservation gate, so the centrifugal matter and membrane deformation cannot be omitted. | W3n-W3p; rigid no-go artifact SHA256 `a91577f62a2992f3aca8c7ffe9af171c6c5759a0dcff80550c3dff5240286bfe`. | This rejects the rigid source, not rotating Skyrmions generally. |
| G3 | **[PROVED]** | The declared centrifugal weak form has a closed positive Friedrichs operator with `||A^-1||<=100` and a unique nonzero weak matter deformation. | W3z.15 artifact SHA256 `4a4e3ecd48a205860de3aa045c94d2b825c0afce1c0f12f4b96254db355b85bb`; W3z.16 artifact SHA256 `9edc2bc479534fab3f527ce535a373da1373b45085c6fbf4602f4ee9cdd32db7`. | A nonzero matter deformation does not imply a nonzero exterior master or Weyl amplitude. |
| G4 | **[CONDITIONAL]** | Exact conservation identities plus source-bound floating refinement support a completed bulk-plus-moving-membrane stress at the default point. | W3r artifact SHA256 `79f588642456d91eb58107de613a639566af0e7924cd29e8d480bf109ecea5db`; W3s artifact SHA256 `1ef92b3579f60fe52d2849d3da3202dc55be33be538b401117218f81cdea53aa`. | The analytic factorization is exact, but default branch closure is floating, not interval-certified or self-gravitating. Use "source-bound floating conservation audit," not simply "a certified conserved source." |
| G5a | **[PROVED]** | The conserved-stress-to-master source identity, ideal-shell transmission law, and vacuum master-to-electric-Weyl reconstruction are exact in the frozen fixed-de-Sitter convention. | W3t, W3v, and W3x; artifact hashes `3be17612134bb6b72535db9d3c80a74acf1271a39e04eec4b1591c9bd8967887`, `c83536779d2ab62684218291dd99de190569f9973417d9accd2ceff426901ade`, and `3025d65fe82585e584150e956de9481380ab3f4a72d26a7cacb744974838c070`. | Exact maps do not certify a nonzero input amplitude. |
| G5b | **[CONDITIONAL]** | The action gives the displayed physical collective scaling formula once the inertia and leading collective state are supplied. | W3w; `experiments/centrifugal_skyrmion_physical_response_certificate.json`, SHA256 `fc8ae96c6215c4dbe7c8905bbfb59a80cb12cd96e7a3dc9c3849a973174b9470`. | The default response coefficient and inertia normalization are source-bound floating numerics, and collective-band control and higher-order rotation remain open. |
| G6 | **[CONDITIONAL]** | The floating completed response has one stable exterior amplitude; the dual-weighted target is `-0.002818947812...` with a fine-discrete residual product `4.50997e-5`. | W3u artifact SHA256 `07c66bb0731588a268db1398f9714746dd43b1e666867d004ee472e525873437`; W3z.17 feasibility artifact SHA256 `584a22ea3ae9807dcc9da8cd6cc20274c943c52bb23cbe8e6dcf986bf7`. | The error product is exact only relative to the assembled fine Galerkin system and omits continuum/profile/origin effects. Do not quote it as an interval lower bound. |
| G7 | **[PROVED]** | The current interval program certifies the positive-radius primal residual square `<=0.010027698207072146`, origin primal residual square `<=2.1330073298636e-5`, exact internal conormal cancellation, the moving-wall adjoint load, and the positive-radius weak adjoint load. | W3z.24-W3z.28; artifact hashes `814da74d5c21cf96b45e9967dd5b8d297d90480a46c3f3ae7fd82ba3ffaad3e7`, `7924fb7da3bb96e92fb43f68cf9311b9ac9a6077292e69474fccf5579abab504`, `1ee677788edc45190c9b164c45bc4a76a1b9e395d172f12b5aa13241748200e2`, `ee73b3527750f91bcb2ed585df3d1d58376cbe0f4ff8db47919356872a86ed42`, and `3db6d390d521494d192c5df6b4bc5dfd1ee09f6d441f0bd69c3be2d18add44f5`. | These are components of the response proof, not zero exclusion. The origin artifact's tiny adjoint-shaped value uses zero load and is not an adjoint residual. |
| G8 | **[PROVED]** | The current direct positive-radius-plus-wall adjoint form-dual bound is `delta_z,partial<=0.769420221021594403`; over 99% comes from the adjusted bulk value coefficient near `x=0.5`. | W3z.29; `experiments/validated_centrifugal_adjoint_energy_dual.json`, SHA256 `500e56b5aa36c64846100dc59a7383b2051a12c6676fcf8e6d49574f61142d0e`. | This is a partial upper bound and representation diagnostic. The regular-origin master load is absent; its size is not a physical no-go. |
| G9 | **[OPEN]** | A rigorous interval for the completed exterior amplitude and normalized `B_W` that excludes zero remains missing. | W3z.17 completion requires full primal and adjoint `V*` residuals, including the regular-origin adjoint load, whose product is smaller than the corrected-amplitude margin. | The packet must say the Weyl zero-exclusion gate is open even though exact reconstruction and favorable floating evidence exist. |
| G10 | **[PROVED]** | Identical de Sitter geometry on both sides cannot support positive pure tension, and nonspherical promotion requires six physical shell amplitudes. | W3z.18; `experiments/israel_junction_gate_certificate.json`, SHA256 `d2c7f542490966c51d37b2d10db45efb4f4c746ac696d5996df1a9b16c29a950`. | This is an acceptance gate and benchmark, not completed Skyrmion Israel matching. |
| G11 | **[OPEN]** | Spherical Einstein-Skyrme/Kottler matching, the six-amplitude nonspherical Israel reconstruction, deformed-background response, and a self-consistent rotating geometry remain open. | Harlow-facing goal and W3z.18 claim boundary. | Fixed-background `B_W` may witness non-invisibility; it may not be called a self-gravitating capacity bound. |
| G12 | **[CONDITIONAL]** | A rank-two tidal signal has an exact finite-time mean detector transfer in the declared heat/Jacobi/Gaussian model. | W3z.20; `experiments/finite_time_tidal_detector_certificate.json`, SHA256 `9c72f7cd75f4d1d542fb9bfd08a907f2b31e42a1e55e07f6eecb557c9571e7`. | The Weyl amplitude, physical rate, detector noise, finite-separation remainder, and detector backreaction are not derived from one action. |
| G13 | **[OPEN]** | No theorem shows that `B_W` is the gravitational quantity that caps observer information. | Harlow-facing goal G4 and review question 2. | Collapse, horizon/QES displacement, or another invariant may be the relevant bottleneck. |

## Realization and publication claims

| ID | Status | Claim allowed in the packet | Evidence | Required qualification |
| --- | --- | --- | --- | --- |
| R1 | **[PROVED]** | AU.1 proves local existence and uniqueness in a certified Newton neighborhood, strict monotonicity, `F'(4) in [-0.09465,-0.08746]`, and positive finite inertia for the declared hard-wall profile. | Exact artifact SHA256 `c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff`; focused AU.1 tests. | The hard wall is a physical modeling input, not a harmless numerical regulator. Global uniqueness and arbitrary wall dynamics are outside the theorem. |
| R2 | **[CONDITIONAL]** | The supported Skyrmion is a serious candidate matter realization of the register architecture. | AU.1, AU.3a/b, the collective spectral theorem, centrifugal inverse, and response architecture. | It is not yet a one-action observer, and the architecture must survive rejection of the wall or Skyrmion realization. |
| R3 | **[OPEN]** | Novelty, venue fit, and publishability relative to the complete literature are not mathematical outputs of the repository. | `docs/primary_source_novelty_matrix.md` supports a nearest-neighbor comparison but explicitly treats search absence as non-proof. | Use "candidate contribution" or "question for specialist review," never "first" or "breakthrough." |
| R4 | **[OPEN]** | A closed-universe path integral, observer-rule derivation, or identification with the finite observer in Harlow's framework is not supplied. | Explicit non-goals in `docs/harlow_facing_paper_goal.md`. | The packet asks whether the semiclassical register is useful; it does not claim that it already instantiates the observer rule. |

## Source-bound artifact index

The hashes below were recomputed from the current worktree on 2026-06-10.

| Role | Artifact | SHA256 | Evidentiary use |
| --- | --- | --- | --- |
| Abstract observer composition | `experiments/universal_observer_tradeoff_certificate.json` | `5c88eb4af23764204333b5e899083c87911066895d70fc132f263e180c175ad6` | **[PROVED]** conditional implication |
| AU.1 nonlinear profile | `experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json` | `c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff` | **[PROVED]** fixed-background hard-wall profile |
| AU.3a Sobolev inputs | `experiments/skyrmion_au3_global_sobolev_exact_certificate.json` | `b6a9931cc50359ec4a9bed7a6d3443471f39b39f60c37e3a92d39073ba0cc55c` | **[PROVED]** rigorous spectral upper inputs |
| AU.3b sharp baseline | `experiments/skyrmion_au3b_sharp_global_exact_certificate.json` | `bc6cf2ea21f44c122001fcc3f7fa6cffb9983d4ec4e35591323aa2d29b25c529` | **[PROVED]** authenticated but tail-dominated baseline |
| Fixed-de Sitter resolvent | `experiments/static_patch_l2_response_exact_certificate.json` | `45871bfe3e15a65b546eddd6391d42d0d8e6665ee981c9f24618409f52dcd051` | **[PROVED]** exact Green operator |
| Centrifugal inverse | `experiments/centrifugal_skyrmion_friedrichs_form_certificate.json` | `4a4e3ecd48a205860de3aa045c94d2b825c0afce1c0f12f4b96254db355b85bb` | **[PROVED]** closed operator and inverse |
| Nonzero weak matter response | `experiments/centrifugal_skyrmion_forced_response_certificate.json` | `9edc2bc479534fab3f527ce535a373da1373b45085c6fbf4602f4ee9cdd32db7` | **[PROVED]** matter response only |
| Completed stress | `experiments/centrifugal_skyrmion_completed_stress_certificate.json` | `79f588642456d91eb58107de613a639566af0e7924cd29e8d480bf109ecea5db` | **[CONDITIONAL]** source-bound floating closure |
| Membrane stress | `experiments/centrifugal_skyrmion_membrane_stress_certificate.json` | `1ef92b3579f60fe52d2849d3da3202dc55be33be538b401117218f81cdea53aa` | **[CONDITIONAL]** exact identities plus floating branch |
| Master-source map | `experiments/static_patch_l2_master_source_certificate.json` | `3be17612134bb6b72535db9d3c80a74acf1271a39e04eec4b1591c9bd8967887` | **[PROVED]** exact map |
| Ideal-shell transmission | `experiments/static_patch_l2_transmission_certificate.json` | `c83536779d2ab62684218291dd99de190569f9973417d9accd2ceff426901ade` | **[PROVED]** exact distributional transmission law |
| Floating master response | `experiments/centrifugal_skyrmion_master_response_certificate.json` | `07c66bb0731588a268db1398f9714746dd43b1e666867d004ee472e525873437` | **[CONDITIONAL]** default-point response evidence |
| Physical collective wrapper | `experiments/centrifugal_skyrmion_physical_response_certificate.json` | `fc8ae96c6215c4dbe7c8905bbfb59a80cb12cd96e7a3dc9c3849a973174b9470` | **[CONDITIONAL]** exact scaling formula with floating default normalization |
| Weyl reconstruction | `experiments/static_patch_l2_weyl_reconstruction_certificate.json` | `3025d65fe82585e584150e956de9481380ab3f4a72d26a7cacb744974838c070` | **[PROVED]** exact vacuum reconstruction, not nonzero source amplitude |
| Floating adjoint target | `experiments/centrifugal_skyrmion_master_adjoint_feasibility.json` | `584a22ea3ae9807dcc9da8cd6cc20274c943c52bb23c38923cbe8e6dcf986bf7` | **[CONDITIONAL]** fine-Galerkin design target |
| Rational trials | `experiments/centrifugal_skyrmion_rational_response_trials.json` | `9dd83028d00b55c85d280087a696884338941b6602e3f9148a41d524f5ace921` | **[PROVED]** exact conforming trial archive |
| Origin response | `experiments/validated_centrifugal_origin_profile_jets.json` | `7924fb7da3bb96e92fb43f68cf9311b9ac9a6077292e69474fccf5579abab504` | **[PROVED]** primal origin residual; no adjoint load |
| Interface cancellation | `experiments/centrifugal_conormal_interface_certificate.json` | `1ee677788edc45190c9b164c45bc4a76a1b9e395d172f12b5aa13241748200e2` | **[PROVED]** no internal conormal deltas |
| Wall master load | `experiments/validated_centrifugal_wall_master_load.json` | `ee73b3527750f91bcb2ed585df3d1d58376cbe0f4ff8db47919356872a86ed42` | **[PROVED]** wall part only |
| Weak adjoint bulk load | `experiments/validated_centrifugal_adjoint_bulk_load.json` | `3db6d390d521494d192c5df6b4bc5dfd1ee09f6d441f0bd69c3be2d18add44f5` | **[PROVED]** positive-radius part only |
| Correlated primal residual | `experiments/validated_centrifugal_correlated_residual.json` | `814da74d5c21cf96b45e9967dd5b8d297d90480a46c3f3ae7fd82ba3ffaad3e7` | **[PROVED]** positive-radius primal bound |
| Partial adjoint dual bound | `experiments/validated_centrifugal_adjoint_energy_dual.json` | `500e56b5aa36c64846100dc59a7383b2051a12c6676fcf8e6d49574f61142d0e` | **[PROVED]** partial bound; cannot exclude zero |
| Israel acceptance gate | `experiments/israel_junction_gate_certificate.json` | `d2c7f542490966c51d37b2d10db45efb4f4c746ac696d5996df1a9b16c29a950` | **[PROVED]** gate, not matched Skyrmion |

## Consistency audit and wording corrections

The numerical values and artifact hashes used in the colleague brief agree
with the current artifacts: the outer primal residual square is
`0.010027698207072146`; the origin primal residual square is
`0.000021330073298636`; `gamma_B` lies in
`[0.002688103336731132,0.002834701713361219]`; and the partial adjoint dual
upper bound is `0.769420221021594403`.

The following current repository phrasings need conservative translation in
the external packet:

1. W3u says the composition "gives a nonzero" master response, W3x says the
   cat "therefore produces a nonzero" tidal quadrupole, and W3y says the two
   states have distinct tidal fields. Their own claim boundaries identify the
   construction as source-bound floating numerics. Externally, describe these
   as **[CONDITIONAL] floating nonzero targets** until W3z.17 closes.
2. The colleague brief lists "conserved smooth bulk plus distributional
   membrane stress" under proved ingredients. W3r and W3s instead provide
   exact conservation/factorization identities plus source-bound floating
   closure on the default branch. Use that full phrase and do not imply an
   interval-certified physical source.
3. The exact Weyl reconstruction artifact proves the map
   `delta E_rr=-6 Psi Y/r^3`; it does not prove `Psi` is nonzero for the
   continuum completed Skyrmion. Keep the map **[PROVED]** and zero exclusion
   **[OPEN]** as separate rows.
4. The AU.1 profile certificate is
   `skyrmion_newton_reduced_hessian_rounded_exact_certificate.json` with hash
   `c4c95d...`. The distinct
   `centrifugal_skyrmion_bvp_certificate.json` (`ddc489...`) is exploratory
   floating centrifugal-response evidence and must not be cited as the AU.1
   existence proof.
5. AU.3b's formally nonempty coupling interval has lower endpoint zero. It is
   an automatic mathematical interval, not evidence for an experimentally or
   physically nonempty observer window.

No stale response constants or mismatched hashes were found among the
source-bound artifacts listed above. The substantive contradiction is one of
claim strength, not arithmetic: exact reconstruction plus a stable floating
target is repeatedly easy to read as a certified nonzero Weyl result, but the
current interval evidence does not support that conclusion.

## Verification

The current-state claim surface was replayed with 152 focused tests, covering
the global `SO(3)` bounds, orbital and collective capacity results, abstract
observer composition, measure-and-correct and heat-model statements, AU.1,
exact Weyl reconstruction, the floating adjoint target, and all current
source-bound primal/adjoint response components:

```bash
python -m pytest -q \
  tests/test_global_so3_reference_risk.py \
  tests/test_localized_orbital_reference.py \
  tests/test_rotational_spectral_capacity.py \
  tests/test_supported_skyrmion_collective_spectral_floor.py \
  tests/test_universal_observer_tradeoff.py \
  tests/test_universal_observer_tradeoff_audit.py \
  tests/test_so3_measure_correct_recovery.py \
  tests/test_finite_time_rotation_diffusion.py \
  tests/test_static_patch_matter_observer_channel.py \
  tests/test_skyrmion_orientation_coherence.py \
  tests/test_validated_skyrmion_bvp.py \
  tests/test_skyrmion_newton_linearization_audit.py \
  tests/test_static_patch_l2_weyl_reconstruction.py \
  tests/test_static_patch_l2_weyl_reconstruction_audit.py \
  tests/test_centrifugal_skyrmion_master_adjoint.py \
  tests/test_centrifugal_skyrmion_master_adjoint_audit.py \
  tests/test_validated_centrifugal_origin_profile_jets.py \
  tests/test_validated_centrifugal_origin_profile_jets_audit.py \
  tests/test_validated_centrifugal_wall_master_load.py \
  tests/test_validated_centrifugal_wall_master_load_audit.py \
  tests/test_validated_centrifugal_adjoint_bulk_load.py \
  tests/test_validated_centrifugal_adjoint_bulk_load_audit.py \
  tests/test_validated_centrifugal_correlated_residual.py \
  tests/test_validated_centrifugal_correlated_residual_audit.py \
  tests/test_validated_centrifugal_adjoint_energy_dual.py \
  tests/test_validated_centrifugal_adjoint_energy_dual_audit.py
```

Result: `152 passed in 232.46s` on 2026-06-10.

A second focused batch replayed the exact static `ell=2` resolvent and source
map, shell transmission, physical collective wrapper, Friedrichs inverse,
nonzero weak matter response, Israel gate, and finite-time detector transfer,
including every corresponding source-hash audit. Result:
`67 passed in 9.11s`. Total focused tests for this ledger: `219 passed`.

## Packet-level allowed conclusion

The strongest accurate summary is:

> **[PROVED]** The project has global operational `SO(3)` resource bounds,
> named matter-capacity theorems, a validated fixed-background hard-wall
> profile, an exact fixed-de-Sitter gravitational-response architecture, and
> substantial interval components of the response proof. **[CONDITIONAL]**
> Effective heat/Davies models and source-bound floating response calculations
> support a plausible finite-record construction. **[OPEN]** The physical
> preparation-storage-readout channel, the `S_dir`-to-`S_Ob` dictionary, Weyl
> zero exclusion, self-consistent gravity, and the one-action common parameter
> window remain unresolved.

This is enough to ask Dr. Harlow whether the architecture targets the right
observer concept. It is not yet enough to present the proposed observer
tradeoff or a nonzero Skyrmion Weyl footprint as a completed physical theorem.
