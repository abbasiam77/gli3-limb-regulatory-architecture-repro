#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_location_map(path: str) -> dict:
    """
    Expect a 2-column TSV/CSV with:
      enhancer<TAB>location
    where location is 'intronic' or 'upstream' (or any text you want).
    """
    if not path:
        return {}
    df = pd.read_csv(path, sep=None, engine="python", header=None)
    if df.shape[1] < 2:
        raise ValueError(f"Location map file must have >=2 columns: {path}")
    return dict(zip(df.iloc[:, 0].astype(str), df.iloc[:, 1].astype(str)))

def guess_location_column(df: pd.DataFrame):
    # Try common names used in earlier scripts
    candidates = [
        "location", "Location", "region", "Region", "class", "Class",
        "type", "Type", "category", "Category", "group", "Group"
    ]
    for c in candidates:
        if c in df.columns:
            return c
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", required=True, help="Input TSV (Fig2C mean signal table).")
    ap.add_argument("--out-prefix", required=True, help="Output prefix (no extension).")
    ap.add_argument("--loc-map", default="", help="Optional 2-col file: enhancer<tab>location.")
    ap.add_argument("--sort-by", default="H3K4me1_mean",
                    help="Column to sort by (default: H3K4me1_mean).")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--annotate", action="store_true",
                    help="Write numeric value at end of each bar (can be busy).")
    args = ap.parse_args()

    df = pd.read_csv(args.tsv, sep="\t")
    if df.empty:
        raise SystemExit(f"TSV is empty: {args.tsv}")

    # Identify enhancer name column
    name_col = None
    for c in ["enhancer", "Enhancer", "name", "Name", "id", "ID"]:
        if c in df.columns:
            name_col = c
            break
    if name_col is None:
        # fallback: assume first column is enhancer id/name
        name_col = df.columns[0]

    # Required signal columns
    col_me1 = "H3K4me1_mean"
    col_ac  = "H3K27ac_mean"
    col_me3 = "H3K4me3_mean"
    missing = [c for c in [col_me1, col_ac, col_me3] if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing expected columns in TSV: {missing}\nColumns found: {list(df.columns)}")

    # Location/status: from TSV if present, otherwise from mapping file
    loc_map = load_location_map(args.loc_map)
    loc_col = guess_location_column(df)

    def get_loc(row) -> str:
        if loc_col is not None and pd.notna(row[loc_col]):
            return str(row[loc_col]).strip()
        key = str(row[name_col])
        return loc_map.get(key, "unknown")

    df["_loc"] = df.apply(get_loc, axis=1)

    # Nice labels: "Enhancer (intronic)" etc.
    df["_label"] = df[name_col].astype(str) + " (" + df["_loc"].astype(str) + ")"

    # Sort
    if args.sort_by in df.columns:
        df = df.sort_values(args.sort_by, ascending=False)

    labels = df["_label"].tolist()
    me1 = df[col_me1].astype(float).to_numpy()
    ac  = df[col_ac].astype(float).to_numpy()
    me3 = df[col_me3].astype(float).to_numpy()

    n = len(df)

    # ---- Layout: 3 bars per enhancer + 1 bar-space gap between enhancers ----
    bar_h = 0.22
    inner_sep = 0.26          # spacing among the 3 bars within an enhancer
    group_gap = 0.30          # "one bar space" between enhancers (tweak if needed)
    group_step = (3 * inner_sep) + group_gap

    y_base = np.arange(n) * group_step
    y_me1 = y_base - inner_sep
    y_ac  = y_base
    y_me3 = y_base + inner_sep

    # Colors by mark type
    color_me1 = "#1f77b4"   # H3K4me1
    color_ac  = "#ff7f0e"   # H3K27ac
    color_me3 = "#2ca02c"   # H3K4me3

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    # Figure size: increase height if many enhancers
    fig_h = max(6.5, 0.55 * n)
    fig, ax = plt.subplots(figsize=(14, fig_h))

    ax.barh(y_me1, me1, height=bar_h, color=color_me1, label="H3K4me1")
    ax.barh(y_ac,  ac,  height=bar_h, color=color_ac,  label="H3K27ac")
    ax.barh(y_me3, me3, height=bar_h, color=color_me3, label="H3K4me3")

    ax.set_yticks(y_base)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()

    ax.set_xlabel("mean bigWig signal (WT hindlimb E11.5, mm9)")
    ax.set_title("Fig 2C — enhancer chromatin signatures (shared scale)")

    ax.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.5)
    ax.legend(frameon=False, loc="lower right")

    # Optional value labels
    if args.annotate:
        maxv = max(float(np.nanmax(me1)), float(np.nanmax(ac)), float(np.nanmax(me3)), 1e-9)
        pad = 0.01 * maxv
        def add_vals(ypos, vals):
            for y, v in zip(ypos, vals):
                ax.text(v + pad, y, f"{v:.3f}", va="center", fontsize=8)
        add_vals(y_me1, me1)
        add_vals(y_ac,  ac)
        add_vals(y_me3, me3)

    # Extra left margin for long labels
    plt.tight_layout(rect=[0.22, 0.02, 0.98, 0.98])

    out_png = args.out_prefix + ".png"
    out_svg = args.out_prefix + ".svg"
    fig.savefig(out_png, dpi=args.dpi, bbox_inches="tight")
    fig.savefig(out_svg, bbox_inches="tight")
    plt.close(fig)

    print(f"[OK] Wrote:\n  {out_png}\n  {out_svg}")

if __name__ == "__main__":
    main()
