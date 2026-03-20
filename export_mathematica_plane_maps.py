"""Export audited 2D diagnostic planes for final rendering in Mathematica.

This script does not create manuscript PNGs itself. Instead, it rebuilds the
same XY/XZ diagnostic fields used by the cleaned Python workflow and exports
them in a Mathematica-friendly JSON format. Mathematica can then focus purely
on presentation quality while all quantitative diagnostics remain anchored to
the Python pipeline and the exported bundle data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from output_naming import field_plot_base
from postprocess_plots import FIELD_EXPORTS, PLANE_NAMES, _parse_planes, compute_plane_map, load_run


def _json_ready_matrix(values: np.ndarray) -> list[list[float | None]]:
    """Convert a 2D numpy array into a JSON-safe nested list.

    Mathematica's JSON importer handles ``null`` far more reliably than NaN
    strings when we later filter out masked samples. Keeping the shape intact
    also makes it easy to reconstruct regular-grid coordinates on the Wolfram
    side without any guesswork.
    """

    array = np.asarray(values, dtype=float)
    output: list[list[float | None]] = []
    for row in array.tolist():
        output.append([None if value is None or not np.isfinite(value) else float(value) for value in row])
    return output


def _field_limits(values: np.ndarray) -> dict[str, float]:
    """Record conservative display limits for downstream rendering.

    These limits are not used for scientific claims. They simply give the
    Mathematica renderer a reproducible starting point for zero-centered color
    scaling.
    """

    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return {"abs_q98": 1.0, "abs_max": 1.0}
    abs_finite = np.abs(finite)
    q98 = float(np.nanpercentile(abs_finite, 98.0))
    abs_max = float(np.nanmax(abs_finite))
    return {
        "abs_q98": q98 if np.isfinite(q98) and q98 > 0.0 else abs_max if abs_max > 0.0 else 1.0,
        "abs_max": abs_max if np.isfinite(abs_max) and abs_max > 0.0 else 1.0,
    }


def export_plane_bundle(base: str, outdir: Path, planes: tuple[str, ...], plane_n: int | None) -> Path:
    """Export one audited run bundle to a Mathematica-ready directory."""

    run = load_run(base)
    metadata = run["metadata"]
    final_params = run["final_params"]
    outdir.mkdir(parents=True, exist_ok=True)

    bundle_name = field_plot_base(
        run["base_name"],
        final_params=final_params,
        domain_type=int(metadata["domain_type"]),
    )
    bundle_dir = outdir / bundle_name
    bundle_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "base_name": run["base_name"],
        "bundle_name": bundle_name,
        "domain_type": int(metadata["domain_type"]),
        "time": float(metadata["time"]),
        "velocity": float(metadata["velocity"]),
        "plane_n": int(plane_n if plane_n is not None else metadata["N_xyz"]),
        "xyz_range": [float(v) for v in metadata["xyz_range"]],
        "final_params": {
            "A": float(final_params["A"]),
            "B": float(final_params["B"]),
            "R0": None if not np.isfinite(final_params.get("R0", np.nan)) else float(final_params["R0"]),
            "alpha": float(final_params["alpha"]),
        },
        "planes": {},
    }

    for plane in planes:
        plane_map = compute_plane_map(run, plane=plane, plane_n=plane_n)
        plane_entry: dict[str, object] = {
            "xlabel": plane_map["xlabel"],
            "ylabel": plane_map["ylabel"],
            "axis_x": [float(v) for v in plane_map["axis_x"]],
            "axis_y": [float(v) for v in plane_map["axis_y"]],
            "fields": {},
        }
        for field_name, export_meta in FIELD_EXPORTS.items():
            values = np.asarray(plane_map["fields"][field_name], dtype=float)
            field_filename = f"{bundle_name}_{plane}_{export_meta['filename']}.json"
            field_path = bundle_dir / field_filename
            payload = {
                "field_name": field_name,
                "plane": plane,
                "title": export_meta["title"],
                "axis_x": plane_entry["axis_x"],
                "axis_y": plane_entry["axis_y"],
                "values": _json_ready_matrix(values),
                "display_limits": _field_limits(values),
            }
            field_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            plane_entry["fields"][field_name] = field_filename
        manifest["planes"][plane] = plane_entry

    (bundle_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return bundle_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export cleaned plane-map diagnostics for final Mathematica rendering."
    )
    parser.add_argument("--base", required=True, help="Bundle stem, e.g. manuscript_target_bundles/domain_2_v_0p1_t_30p0")
    parser.add_argument("--outdir", default="mathematica_exports", help="Root directory for Mathematica-ready exports")
    parser.add_argument(
        "--planes",
        nargs="+",
        default=list(PLANE_NAMES),
        help="Plane list, e.g. --planes XY XZ or --planes XY,XZ",
    )
    parser.add_argument(
        "--plane-n",
        type=int,
        default=800,
        help="Sampling resolution per axis for the exported 2D plane maps",
    )
    args = parser.parse_args()

    planes = _parse_planes(args.planes)
    bundle_dir = export_plane_bundle(
        base=args.base,
        outdir=Path(args.outdir),
        planes=planes,
        plane_n=args.plane_n,
    )
    print(bundle_dir)


if __name__ == "__main__":
    main()
