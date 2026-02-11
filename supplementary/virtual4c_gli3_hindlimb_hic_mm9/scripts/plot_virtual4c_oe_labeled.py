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

# If you decide later that something should be excluded from labels (e.g., CNE6), add it here.
EXCLUDE_DEFAULT = set()

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

def open_maybe_gz(path: str):
    return gzip.open(path, "rt") if str(path).endswith(".gz") else open(path, "r")

def read_bed_features(path: str, start_bp: int, end_bp: int):
    """
    Returns list of dicts: {chrom, start, end, mid, name}
    Filters to features whose mid is within [start_bp, end_bp).
    """
    feats = []
    with open_maybe_gz(path) as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("track") or line.startswith("browser"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            chrom = parts[0]
            try:
                s = int(parts[1]); e = int(parts[2])
            except Exception:
                continue
            name = parts[3] if len(parts) >= 4 else ""
            mid = (s + e) // 2
            if start_bp <= mid < end_bp:
                feats.append({"chrom": chrom, "start": s, "end": e, "mid": mid, "name": name})
    # sort left-to-right
    feats.sort(key=lambda d: d["mid"])
    return feats

def main():
    ap = argparse.ArgumentParser(description="Plot Virtual 4C (OE, KR) with labeled enhancer lines (intronic vs upstream).")
    ap.add_argument("--vector", required=True, help="TSV with: bin_start <tab> value (e.g., out/gli3_virtual4c_OE_10kb_FULL_vector.tsv)")
    ap.add_argument("--bed", required=True, help="Enhancer BED(.gz) with names in col4 (e.g., work/gli3_enhancers_mm9.bed.gz)")
    ap.add_argument("--outdir", required=True, help="Output directory (e.g., 4C_Figure)")
    ap.add_argument("--prefix", required=True, help="Output file prefix (no extension)")
    ap.add_argument("--start", type=int, required=True, help="Plot window start (bp)")
    ap.add_argument("--end", type=int, required=True, help="Plot window end (bp)")
    ap.add_argument("--viewpoint", type=int, required=True, help="Viewpoint bin start (bp), e.g., 15550000")

    ap.add_argument("--intronic", nargs="*", default=None,
                    help="Names to treat as intronic (green). If omitted, uses default intronic set.")
    ap.add_argument("--exclude", nargs="*", default=None,
                    help="Names to exclude from plotting/labels (optional).")
    ap.add_argument("--title", default=None, help="Optional title (leave blank for UNLABELED style).")

    args = ap.parse_args()

    intronic_set = set(args.intronic) if args.intronic is not None else set(INTRONIC_SET_DEFAULT)
    exclude_set = set(args.exclude) if args.exclude is not None else set(EXCLUDE_DEFAULT)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # --- read curve ---
    xs, ys = read_vector_tsv(args.vector)
    data = sorted([(x, y) for x, y in zip(xs, ys) if args.start <= x < args.end], key=lambda t: t[0])
    if not data:
        raise SystemExit(f"No vector points found in range {args.start}-{args.end}")

    xs_bp = [x for x, _ in data]
    ys_v = [y for _, y in data]
    xs_mb = [x / 1e6 for x in xs_bp]
    vp_mb = args.viewpoint / 1e6

    # --- read enhancers ---
    feats = read_bed_features(args.bed, args.start, args.end)
    feats = [f for f in feats if f["name"] not in exclude_set]

    # --- figure ---
    fig = plt.figure(figsize=(10.2, 3.8), dpi=300)
    ax = fig.add_subplot(111)

    ax.plot(xs_mb, ys_v, linewidth=2.0)

    # y-axis: keep >=0 for journal friendliness
    ymax = max(ys_v) if ys_v else 1.0
    ax.set_ylim(0, ymax * 1.08)

    ax.set_xlim(args.start / 1e6, args.end / 1e6)
    ax.set_xlabel("Genomic position (Mb, mm9)")
    ax.set_ylabel("Virtual 4C signal (O/E, KR)")

    # viewpoint line + label
    ax.axvline(vp_mb, linewidth=1.4, linestyle="--")
    ax.text(vp_mb, ymax * 1.02, "Promoter region", rotation=90,
            va="bottom", ha="right")

    # enhancer vertical lines + labels
    # color choices: green + gold (matplotlib named colors)
    color_intronic = "green"
    color_upstream = "goldenrod"

    # draw lines from a small baseline up toward top region
    y0 = ymax * 0.02
    y1 = ymax * 0.13   # line height
    label_y = ymax * 0.14

    for f in feats:
        xm = f["mid"] / 1e6
        name = f["name"]
        col = color_intronic if name in intronic_set else color_upstream
        ax.plot([xm, xm], [y0, y1], linewidth=2.0, color=col)
        ax.text(xm, label_y, name, rotation=90, va="bottom", ha="center", fontsize=8, color=col)

    if args.title:
        ax.set_title(args.title)

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
