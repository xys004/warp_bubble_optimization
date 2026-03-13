from __future__ import annotations

from pathlib import Path

import numpy as np


FIELD_EXPORT_SUFFIXES = (
    "XY_rho.png",
    "XY_WECmin.png",
    "XY_NECmin.png",
    "XY_DECmargin.png",
    "XY_SEC.png",
    "XZ_rho.png",
    "XZ_WECmin.png",
    "XZ_NECmin.png",
    "XZ_DECmargin.png",
    "XZ_SEC.png",
)

OPTIMIZATION_EXPORT_SUFFIXES = (
    "loss_components.png",
    "success_fractions.png",
    "params.png",
)


def fmt_num(value: float) -> str:
    text = f"{float(value):.3f}".rstrip("0").rstrip(".")
    return text.replace(".", "p") if "." in text else f"{text}p0"


def field_plot_base(base_name: str, final_params: dict, domain_type: int) -> str:
    a_value = float(final_params["A"])
    b_value = float(final_params["B"])
    r0_raw = final_params.get("R0", np.nan)
    r0_value = 0.0 if domain_type == 1 or not np.isfinite(r0_raw) else float(r0_raw)
    return f"{base_name}_a{fmt_num(a_value)}_b{fmt_num(b_value)}_R0{fmt_num(r0_value)}"


def expected_plot_paths(root: Path, base_name: str, final_params: dict, domain_type: int) -> list[Path]:
    field_base = field_plot_base(base_name, final_params, domain_type)
    field_paths = [root / f"{field_base}_{suffix}" for suffix in FIELD_EXPORT_SUFFIXES]
    optimization_paths = [root / f"{base_name}_{suffix}" for suffix in OPTIMIZATION_EXPORT_SUFFIXES]
    return field_paths + optimization_paths
