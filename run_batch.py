import os
import shutil
import subprocess
import sys

OUTDIR = "runs"
os.makedirs(OUTDIR, exist_ok=True)

SRC = "einstein_optimizer.py"
DST = os.path.join(OUTDIR, "einstein_optimizer.py")

if not os.path.exists(SRC):
    raise SystemExit("Cannot find einstein_optimizer.py in the current directory. Run the cell that writes it first.")
shutil.copy2(SRC, DST)

RUNS = [
    (1, 0.1, 0.2),
    (1, 0.1, 30.0),
    (2, 0.1, 0.2),
    (2, 0.1, 30.0),
]


def fmt_num(x: float) -> str:
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return s.replace(".", "p") if "." in s else f"{s}p0"


def main():
    py = sys.executable
    for domain, v, t in RUNS:
        print("\n" + "=" * 88)
        print(f"Launching: domain={domain}  v={v}  t={t}")
        seed = 47 + int(100 * domain + round(t * 10))
        result = subprocess.run(
            [py, "einstein_optimizer.py", "--domain", str(domain), "--v", str(v), "--t", str(t), "--seed", str(seed)],
            cwd=OUTDIR,
            check=False,
        )
        if result.returncode != 0:
            raise SystemExit(f"Run failed for domain={domain}, v={v}, t={t}")

    print("\nAll runs completed. Output files live in:", os.path.abspath(OUTDIR))
    print("You should see names like:")
    for domain, v, t in RUNS:
        print(f"  domain_{domain}_v_{fmt_num(v)}_t_{fmt_num(t)}_*")


if __name__ == "__main__":
    main()
