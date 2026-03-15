# Phase C Synthesis: legacy vs optimized vs manuscript-target evaluation

This note consolidates the three evidence streams now available in the repository:

1. legacy CSV exports from the older notebook workflow,
2. regenerated optimized bundles from the cleaned pipeline,
3. direct evaluations of the manuscript parameter targets using the same cleaned pipeline.

The purpose of this synthesis is to answer a practical referee-facing question: **which statements in the paper are robust under both regeneration and direct parameter evaluation, and which statements should be revised?**

## Evidence sources

### Legacy workflow

Single-shell legacy (`data/domain1_t30.0_*`):

- final parameters: `A = 2.3488`, `B = 0.6604`
- exported success columns: `h1 = 100.0`, `h2 = 75.25`, `h3 = 75.16`, `h4 = 64.48`
- final loss: `total_loss = 11.8102`, `physics_loss = 11.8096`

Double-shell legacy (`data/domain2_t30.0_*`):

- final parameters: `A = 2.3971`, `B = 1.2368`, `R0 = 1.0000`
- exported success columns: `h1 = 100.0`, `h2 = 96.56`, `h3 = 96.87`, `h4 = 93.90`
- final loss: `total_loss = 4.48e-04`, `physics_loss = 1.15e-09`

### Regenerated optimized bundles

Single-shell optimized (`golden_dataset/domain_1_v_0p1_t_30p0_*`):

- final parameters: `A = 1.0500`, `B = 1.6419`
- success fractions: `NEC = 32.70%`, `WEC = 30.23%`, `DEC = 1.35%`, `SEC = 66.17%`
- final loss: `total_loss = 4.4905`, `physics_loss = 7.32e-13`

Double-shell optimized (`golden_dataset/domain_2_v_0p1_t_30p0_*`):

- final parameters: `A = 1.0426`, `B = 1.3141`, `R0 = 1.2644`
- success fractions: `NEC = 40.13%`, `WEC = 40.13%`, `DEC = 9.87%`, `SEC = 74.34%`
- final loss: `total_loss = 4.4803`, `physics_loss = 4.97e-15`

### Direct manuscript-target evaluation

Single-shell manuscript target (`manuscript_target_bundles/domain_1_v_0p1_t_30p0_*`):

- fixed parameters: `A = 0.9700`, `B = 1.3210`
- success fractions: `NEC = 33.63%`, `WEC = 33.49%`, `DEC = 1.77%`, `SEC = 67.16%`
- single synthetic evaluation epoch, no optimization updates

Double-shell manuscript target (`manuscript_target_bundles/domain_2_v_0p1_t_30p0_*`):

- fixed parameters: `A = 1.8480`, `B = 1.1350`, `R0 = 1.2920`
- success fractions: `NEC = 32.04%`, `WEC = 32.04%`, `DEC = 5.83%`, `SEC = 59.71%`
- single synthetic evaluation epoch, no optimization updates

## Important comparability warning

The legacy workflow is **not** directly comparable to the cleaned pipeline on the level of exported success metrics.

- Legacy CSVs export `h1..h4` component-based diagnostics.
- The cleaned pipeline exports principal-stress success fractions for `NEC`, `WEC`, `DEC`, and `SEC`.

This means the legacy outputs remain useful as historical context, but not as a referee-grade benchmark for the revised manuscript claims.

## Cross-pipeline conclusions

### 1. The legacy workflow is an outlier, not a confirmation set

The legacy runs show dramatically more optimistic success-like diagnostics than either regenerated optimized bundles or direct manuscript-target evaluation. Since the metric definitions differ, this does **not** mean the new code is wrong. It means the old exports should not be treated as direct confirmation of the revised paper language.

Practical implication:

- the paper should not rely on the old Mathematica-era success plots as if they were measuring the same quantities as the current pipeline.

### 2. The manuscript target parameters do not rescue the current wording

This is the most important result of the new fixed-parameter evaluator.

For both topologies, evaluating the published paper parameters under the cleaned pipeline still yields:

- `WEC/NEC` success fractions around `32%` to `34%`, not a high-success regime,
- `DEC` as the tightest residual constraint,
- `SEC` easier than `DEC` in aggregate, but not uniformly positive on sampled slices.

Practical implication:

- the current manuscript wording is not just inconsistent with the optimizer's new convergence point,
- it is also too strong even when the published seed parameters are evaluated directly.

### 3. The optimized bundles and the paper-target bundles agree on the hierarchy

Even though the parameter values differ, the cleaned pipeline gives a consistent hierarchy in both modes:

- `DEC` is the hardest condition,
- `SEC` is easier than `DEC`,
- `WEC/NEC` are intermediate and still substantially violated in aggregate.

This is true for both single-shell and double-shell runs.

Practical implication:

- the paper can safely emphasize **constraint hierarchy** and **localization of residual obstruction**,
- but it should stop claiming near-saturation or widespread success for `WEC/NEC`.

### 4. The optimizer-loss narrative should be revised globally

In both regenerated optimized runs:

- `physics_loss` is extremely small numerically,
- `reg_breach` goes to zero,
- late-time `total_loss` is dominated by `inv_alpha`.

This means the current prose about the optimizer "primarily reducing the physics loss" does not match the exported histories well.

Practical implication:

- training descriptions should be reframed in terms of stabilization, mask regularity, and parameter stationarity,
- not dramatic physics-term descent.

### 5. The pretraining stage explains the near-flat parameter plots

The cleaned optimizer now documents that the visible training run begins **after** Monte-Carlo pretraining has already selected a favorable snapshot. This is consistent with the nearly stationary parameter trajectories we now see, especially for `domain_1`.

Practical implication:

- captions and text should explain that the published optimization history is the main run after pretraining,
- not imply a large initial transient in the visible curves.

## What the paper can still claim safely

The following statements are supported across the cleaned-pipeline evidence:

- the seed construction keeps `rho` non-negative in the intended sense of the analytic setup,
- the surviving obstruction is stress-dominated rather than density-dominated,
- `DEC` is typically the tightest residual constraint,
- `SEC` is easier than `DEC` in aggregate,
- double-shell configurations are more constrained than single-shell ones,
- the optimization is best described as a **physics-penalized parametric optimization**, not a PINN and not an exact constraint solver.

## What should be removed or softened

The following statements are not supported robustly by the new evidence:

- `WEC/NEC` reach high success fractions,
- `WEC_min` is everywhere non-negative to numerical accuracy on the displayed slices,
- `SEC` stays positive throughout the shell or throughout the sampled slices,
- the optimizer primarily reduces the physics loss,
- the visible parameter curves show a pronounced initial transient before plateauing.

## Recommended editorial position

A referee-facing revision should adopt this posture:

- present the cleaned pipeline as the authoritative workflow,
- treat the old workflow as historical only,
- keep the paper focused on the **hierarchy and localization** of residual deficits,
- avoid language that suggests the weak/null conditions are nearly solved,
- explain explicitly that pretraining changes how the main training curves should be read.

## Recommended next step

The next manuscript step should be a **single coordinated text revision** in `warpdrive_clean_submission.tex`, using:

- `phase_c_domain1_audit.md`,
- `phase_c_domain2_audit.md`,
- this synthesis note,
- and the manuscript-target bundles as the paper-parameter reference set.

At this point, the main scientific question is no longer whether the code can reproduce old plots. It is whether the paper's claims are phrased honestly relative to what the cleaned and auditable pipeline now shows. The answer is: **partly yes, but only after a substantial softening of the WEC/NEC/SEC language.**
