import argparse
import csv
import sys
from pathlib import Path

import numpy as np

from manuscript_targets import get_target


def _resolve_base(base: str) -> Path:
    path = Path(base)
    if path.suffix:
        raise ValueError("--base must be a basename/stem without a file suffix")
    return path


def _read_single_row(path: Path) -> dict:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError(f"Expected exactly one row in {path}, found {len(rows)}")
    row = {}
    for key, value in rows[0].items():
        value = value.strip()
        row[key] = np.nan if value == "" else float(value)
    return row


def compare(base: str, atol: float, rtol: float) -> tuple[bool, list[str]]:
    base_path = _resolve_base(base)
    base_name = base_path.name
    root = base_path.parent if str(base_path.parent) not in ("", ".") else Path(".")
    target = get_target(base_name)
    if target is None:
        raise KeyError(f"No manuscript target is defined for {base_name}")

    final_params = _read_single_row(root / f"{base_name}_final_params.csv")
    lines = [f"Comparison for {base_name}"]
    ok = True
    for key in ("A", "B", "R0"):
        target_value = float(target[key])
        actual_value = 0.0 if key == "R0" and not np.isfinite(final_params.get("R0", np.nan)) else float(final_params[key])
        delta = actual_value - target_value
        close = np.isclose(actual_value, target_value, atol=atol, rtol=rtol)
        status = "OK" if close else "DIFF"
        lines.append(
            f"- {key}: actual={actual_value:.6f} target={target_value:.6f} delta={delta:+.6f} [{status}]"
        )
        ok = ok and bool(close)
    lines.append(f"Overall: {'within tolerance' if ok else 'outside tolerance'} (atol={atol}, rtol={rtol})")
    return ok, lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare optimized final parameters against manuscript target values.")
    parser.add_argument("--base", required=True, help="Run basename, e.g. domain_2_v_0p1_t_30p0")
    parser.add_argument("--atol", type=float, default=5e-2, help="Absolute tolerance for parameter comparison")
    parser.add_argument("--rtol", type=float, default=5e-2, help="Relative tolerance for parameter comparison")
    parser.add_argument("--strict", action="store_true", help="Return nonzero exit code when targets are outside tolerance")
    args = parser.parse_args()

    try:
        ok, lines = compare(args.base, atol=float(args.atol), rtol=float(args.rtol))
    except Exception as exc:  # pragma: no cover
        print(f"FAIL: {exc}")
        return 1

    for line in lines:
        print(line)
    if args.strict and not ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
