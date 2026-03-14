# Phase B: Golden Dataset

Phase B defines the small set of revised bundles that we want to treat as the
referee-facing reproducibility baseline.

## Goal

The purpose of the golden dataset is not to replace exploratory work. It is to
give the paper and its review package a compact, stable set of runs that:

- use the cleaned revised pipeline
- keep seeds explicit
- record enough metadata to rerender and verify outputs
- can be regenerated without old notebooks

## Case groups

The manifest lives in `golden_dataset_cases.py`.

### `core`

This is the minimum paper-facing dataset:

- `domain1_paper`
- `domain2_paper`

Both cases use:

- `v = 0.1`
- `t = 30.0`
- `n_xyz = 36`
- `epochs = 2200`
- `pretrain_trials = 6`
- `pretrain_epochs = 60`

The seeds are held fixed and explicit:

- domain 1: `147`
- domain 2: `247`

### `time_audit`

This is an optional constant-velocity audit group that reuses the same seeds as
the corresponding `t = 30.0` cases while changing only the time label to `t = 0.2`.

The purpose is not to claim exact equality of optimizer outcomes in every noisy
run, but to remove the old confound where different time labels also changed the
random initialization.

### `all`

Runs both `core` and `time_audit`.

## Runner

Use:

```bash
python run_golden_dataset.py --group core --outdir golden_dataset --overwrite
```

The runner performs three steps for each manifest case:

1. generate the optimizer bundle
2. rerender the plots using the case-specific high-resolution settings
3. verify the final outputs

## Why a separate runner exists

We already have lower-level helpers such as:

- `einstein_optimizer.py`
- `generate_run_bundle.py`
- `postprocess_plots.py`
- `verify_outputs.py`

The dedicated Phase B runner exists so the referee-facing dataset is encoded in
one obvious place instead of being spread across notebook cells, terminal history,
or ad hoc command snippets.

## Recommended use in the paper workflow

Treat the `core` group as the default source for:

- final parameter tables
- optimization-curve figures
- XY/XZ diagnostic maps
- quantitative statements tied to the revised principal-stress diagnostics

Treat the `time_audit` group as a methodological cross-check rather than as a
required figure source.
