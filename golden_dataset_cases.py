"""Phase B golden-dataset case manifest.

This module defines the small set of referee-facing runs that we want to keep
reproducible and easy to regenerate. The intent is not to encode every
experimental sweep that happened during development. Instead, we record:

1. a compact "core" dataset that supports the paper figures and principal claims
2. an optional "time_audit" dataset that checks the comoving constant-velocity
   interpretation with matched seeds across different time labels

Each case contains both optimizer settings and the preferred post-processing
settings used to generate reviewer-facing plots.
"""

from __future__ import annotations

from copy import deepcopy


def _case(
    *,
    case_id: str,
    domain: int,
    v: float,
    t: float,
    seed: int,
    epochs: int,
    n_xyz: int,
    pretrain_trials: int,
    pretrain_epochs: int,
    with_colorbar: bool,
    diagnostic_nxyz: int,
    dpi: int,
    map_size: tuple[float, float],
    line_size: tuple[float, float],
    interpolation: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    description: str,
) -> dict:
    """Build one golden-dataset case record.

    The returned dictionary is intentionally plain JSON-like data so that it can
    be serialized later if needed and can be consumed by simple scripts without a
    dependency on dataclasses or pydantic.
    """

    return {
        "id": case_id,
        "description": description,
        "optimizer": {
            "domain": int(domain),
            "v": float(v),
            "t": float(t),
            "seed": int(seed),
            "epochs": int(epochs),
            "n_xyz": int(n_xyz),
            "pretrain_trials": int(pretrain_trials),
            "pretrain_epochs": int(pretrain_epochs),
        },
        "plotting": {
            "with_colorbar": bool(with_colorbar),
            "diagnostic_nxyz": int(diagnostic_nxyz),
            "dpi": int(dpi),
            "map_size": [float(map_size[0]), float(map_size[1])],
            "line_size": [float(line_size[0]), float(line_size[1])],
            "interpolation": str(interpolation),
            "xlim": [float(xlim[0]), float(xlim[1])],
            "ylim": [float(ylim[0]), float(ylim[1])],
        },
    }


CORE_CASES = [
    _case(
        case_id="domain1_paper",
        domain=1,
        v=0.1,
        t=30.0,
        seed=147,
        epochs=2200,
        n_xyz=36,
        pretrain_trials=6,
        pretrain_epochs=60,
        with_colorbar=False,
        diagnostic_nxyz=128,
        dpi=500,
        map_size=(8.5, 8.5),
        line_size=(9.0, 7.0),
        interpolation="bicubic",
        xlim=(-2.2, 2.2),
        ylim=(-2.2, 2.2),
        description="Single-shell paper-grade reference bundle at v=0.1, t=30.0.",
    ),
    _case(
        case_id="domain2_paper",
        domain=2,
        v=0.1,
        t=30.0,
        seed=247,
        epochs=2200,
        n_xyz=36,
        pretrain_trials=6,
        pretrain_epochs=60,
        with_colorbar=False,
        diagnostic_nxyz=128,
        dpi=500,
        map_size=(8.5, 8.5),
        line_size=(9.0, 7.0),
        interpolation="bicubic",
        xlim=(-2.2, 2.2),
        ylim=(-2.2, 2.2),
        description="Double-shell paper-grade reference bundle at v=0.1, t=30.0.",
    ),
]


TIME_AUDIT_CASES = [
    _case(
        case_id="domain1_time_audit_t0p2",
        domain=1,
        v=0.1,
        t=0.2,
        seed=147,
        epochs=2200,
        n_xyz=36,
        pretrain_trials=6,
        pretrain_epochs=60,
        with_colorbar=True,
        diagnostic_nxyz=96,
        dpi=400,
        map_size=(8.0, 8.0),
        line_size=(8.5, 6.5),
        interpolation="bilinear",
        xlim=(-2.2, 2.2),
        ylim=(-2.2, 2.2),
        description="Single-shell constant-velocity audit case paired with the t=30.0 seed.",
    ),
    _case(
        case_id="domain2_time_audit_t0p2",
        domain=2,
        v=0.1,
        t=0.2,
        seed=247,
        epochs=2200,
        n_xyz=36,
        pretrain_trials=6,
        pretrain_epochs=60,
        with_colorbar=True,
        diagnostic_nxyz=96,
        dpi=400,
        map_size=(8.0, 8.0),
        line_size=(8.5, 6.5),
        interpolation="bilinear",
        xlim=(-2.2, 2.2),
        ylim=(-2.2, 2.2),
        description="Double-shell constant-velocity audit case paired with the t=30.0 seed.",
    ),
]


CASE_GROUPS = {
    "core": CORE_CASES,
    "time_audit": TIME_AUDIT_CASES,
    "all": CORE_CASES + TIME_AUDIT_CASES,
}


def get_case_group(name: str) -> list[dict]:
    """Return a deep-copied case list so callers can safely mutate it."""

    if name not in CASE_GROUPS:
        raise KeyError(f"Unknown case group '{name}'. Expected one of: {', '.join(sorted(CASE_GROUPS))}")
    return deepcopy(CASE_GROUPS[name])
