#!/usr/bin/env python3
import argparse
import gzip
from pathlib import Path
import matplotlib.pyplot as plt

INTRONIC_SET_DEFAULT = {
    "CNE14/hs1586/mm1977",
    "CNE18",
    "CNE19",
    "CNE13",
    "mm2018",
    "CNE21",
}

def read_vector_tsv(path: str):
    xs, ys = [], []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            a, b = line.split()[:2]
            xs.append(int(float(a)))
            ys.append(float(b))
    return xs, ys

def open_maybe_gz(path: str):
    return gzip.open(path, "rt") if str(path).endswith(".gz") else open(path, "r")

def read_bed_features(path: str, start_bp: int, end_bp: int):
    feats = []
    with open_maybe_gz(path) as f:
        for line in f:
            if (not line.strip()) or line.startswith("#") or line.startswith("track") or line.startswith("browser"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            try:
                s = int(parts[1]); e = int(parts[2])
            except Exception:
                continue
            name = parts[3] if len(parts) >= 4 else ""
            mid = (s + e) // 2
            if start_bp <= mid < end_bp:
                feats.append({"start": s, "end": e, "mid": mid, "name": name})
    feats.sort(key=lambda d: d["mid"])
    return feats

def main():
    ap = argparse.ArgumentParser(description="Plot Virtual4C OE(KR) curve + enhancer ticks (NO labels).")
    ap.add_argument("--vector", required=True)
    ap.add_argument("--bed", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--viewpoint", type=int, required=True)
    ap.add_argument("--intronic", nargs="*", default=None,
                    help="Override intronic set (light green). If not provided, uses default set.")
    args = ap.parse_args()

    intronic_set = set(args.intronic) if args.intronic is not None else set(INTRONIC_SET_DEFAULT)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    xs, ys = read_vector_tsv(args.vector)
    data = sorted([(x, y) for x, y in zip(xs, ys) if args.start <= x < args.end], key=lambda t: t[0])
    if not data:
        raise SystemExit("No vector points in requested window.")

    xs_bp = [x for x, _ in data]
    ys_v  = [y for _, y in data]
    xs_mb = [x / 1e6 for x in xs_bp]
    vp_mb = args.viewpoint / 1e6

    feats = read_bed_features(args.bed, args.start, args.end)

    # Remove CNE6 completely
    feats = [f for f in feats if f["name"] != "CNE6"]

    fig = plt.figure(figsize=(12.8, 4.2), dpi=300)
    ax = fig.add_subplot(111)

    ax.plot(xs_mb, ys_v, linewidth=2.0)

    ymax = max(ys_v) if ys_v else 1.0
    ax.set_ylim(0, ymax * 1.12)
    ax.set_xlim(args.start / 1e6, args.end / 1e6)

    ax.set_xlabel("Genomic position (Mb, mm9)")
    ax.set_ylabel("Virtual 4C signal (O/E, KR)")

    # Viewpoint: line only, NO label
    ax.axvline(vp_mb, linewidth=1.4, linestyle="--")

    # Enhancer ticks only, NO labels
    color_intronic = "lightgreen"
    color_upstream = "goldenrod"

    y0 = ymax * 0.02
    y1 = ymax * 0.14

    for f in feats:
        xm = f["mid"] / 1e6
        name = f["name"]
        col = color_intronic if name in intronic_set else color_upstream
        ax.plot([xm, xm], [y0, y1], linewidth=2.2, color=col)

    fig.tight_layout()

    png = outdir / f"{args.prefix}.png"
    pdf = outdir / f"{args.prefix}.pdf"
    fig.savefig(png)
    fig.savefig(pdf)
    plt.close(fig)

    print("WROTE:", png)
    print("WROTE:", pdf)

if __name__ == "__main__":
    main()
