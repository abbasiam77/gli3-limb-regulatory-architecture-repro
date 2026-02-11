#!/usr/bin/env python3
import argparse
import gzip
from pathlib import Path
import matplotlib.pyplot as plt

def read_vector_tsv(path: str):
    xs, ys = [], []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            xs.append(int(float(parts[0])))
            ys.append(float(parts[1]))
    return xs, ys

def read_bed_mids(path: str):
    opener = gzip.open if str(path).endswith(".gz") else open
    mids = []
    with opener(path, "rt") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("track") or line.startswith("browser"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            try:
                start = int(parts[1]); end = int(parts[2])
            except Exception:
                continue
            mids.append((start + end) // 2)
    return mids

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vector", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--viewpoint", type=int, required=True)
    ap.add_argument("--bed", default=None)
    ap.add_argument("--ticks", action="store_true")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    xs, ys = read_vector_tsv(args.vector)
    data = sorted([(x, y) for x, y in zip(xs, ys) if args.start <= x < args.end], key=lambda t: t[0])
    if not data:
        raise SystemExit("No data points in requested window")

    xs_f = [x for x, _ in data]
    ys_f = [y for _, y in data]
    xs_mb = [x / 1e6 for x in xs_f]
    vp_mb = args.viewpoint / 1e6

    fig = plt.figure(figsize=(9.0, 3.4), dpi=300)
    ax = fig.add_subplot(111)

    ax.plot(xs_mb, ys_f, linewidth=1.8)
    ax.axvline(vp_mb, linewidth=1.2, linestyle="--")

    ax.set_xlim(args.start / 1e6, args.end / 1e6)
    ax.set_xlabel("Genomic position (Mb, mm9)")
    ax.set_ylabel("Virtual 4C signal (O/E, KR)")

    if args.ticks and args.bed:
        mids = [m for m in read_bed_mids(args.bed) if args.start <= m < args.end]
        ymin, ymax = ax.get_ylim()
        y0 = ymin + 0.02 * (ymax - ymin)
        y1 = ymin + 0.08 * (ymax - ymin)
        for m in mids:
            xm = m / 1e6
            ax.plot([xm, xm], [y0, y1], linewidth=1.0)

    fig.tight_layout()
    png_path = outdir / f"{args.prefix}.png"
    pdf_path = outdir / f"{args.prefix}.pdf"
    fig.savefig(png_path)
    fig.savefig(pdf_path)
    plt.close(fig)

    print("WROTE:", png_path)
    print("WROTE:", pdf_path)

if __name__ == "__main__":
    main()
