#!/usr/bin/env python3
import argparse
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_location_map(path: str) -> dict:
    if not path:
        return {}
    df = pd.read_csv(path, sep=None, engine="python", header=None)
    if df.shape[1] < 2:
        raise ValueError(f"Location map file must have >=2 columns: {path}")
    return dict(zip(df.iloc[:, 0].astype(str), df.iloc[:, 1].astype(str)))

def guess_location_column(df: pd.DataFrame):
    candidates = [
        "location", "Location", "region", "Region", "class", "Class",
        "type", "Type", "category", "Category", "group", "Group"
    ]
    for c in candidates:
        if c in df.columns:
            return c
    return None

def short_enhancer_name(s: str) -> str:
    """
    Convert labels like:
      CNE14_hs1586_mm1977  -> CNE14
      mm2164              -> mm2164
      anything_else       -> token before first underscore
    """
    s = str(s)
    m = re.match(r'^(CNE\d+|mm\d+)', s)
    if m:
        return m.group(1)
    return s.split("_")[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", required=True)
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--loc-map", default="", help="Optional 2-col file: enhancer<tab>location")
    ap.add_argument("--sort-within", default="H3K4me1_mean",
                    help="Sort within each group by this column (desc).")
    ap.add_argument("--dpi", type=int, default=600)

    # Visual layout controls
    ap.add_argument("--bar-h", type=float, default=0.22)
    ap.add_argument("--inner-sep", type=float, default=0.26)
    ap.add_argument("--gap-between-enhancers", type=float, default=0.30)
    ap.add_argument("--gap-between-groups", type=float, default=0.80)

    # Behavior
    ap.add_argument("--drop-all-zero", action="store_true",
                    help="Drop enhancers where all three marks are 0/NA (recommended).")
    ap.add_argument("--zero-eps", type=float, default=1e-9,
                    help="Threshold for considering a value effectively zero.")

    # Annotation for H3K4me3 only
    ap.add_argument("--annotate-me3", action="store_true",
                    help="Annotate only H3K4me3 bars with numeric values.")
    ap.add_argument("--annotate-min", type=float, default=0.01,
                    help="Annotate only if H3K4me3 >= this value (reduces clutter).")

    args = ap.parse_args()

    df = pd.read_csv(args.tsv, sep="\t")
    if df.empty:
        raise SystemExit(f"TSV empty: {args.tsv}")

    # Identify enhancer name column
    name_col = None
    for c in ["enhancer", "Enhancer", "name", "Name", "id", "ID"]:
        if c in df.columns:
            name_col = c
            break
    if name_col is None:
        name_col = df.columns[0]

    # Required signal columns
    col_me1 = "H3K4me1_mean"
    col_ac  = "H3K27ac_mean"
    col_me3 = "H3K4me3_mean"
    missing = [c for c in [col_me1, col_ac, col_me3] if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing expected columns: {missing}\nFound: {list(df.columns)}")

    # Coerce numeric (safe)
    for c in [col_me1, col_ac, col_me3]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    # Location/status: from TSV column if present, otherwise mapping file
    loc_map = load_location_map(args.loc_map)
    loc_col = guess_location_column(df)

    def get_loc(row) -> str:
        if loc_col is not None:
            v = str(row[loc_col]).strip()
            if v and v.lower() != "nan":
                return v.lower()
        key = str(row[name_col])
        return str(loc_map.get(key, "unknown")).lower()

    df["_loc"] = df.apply(get_loc, axis=1)

    # Normalize expected group names
    df["_loc"] = df["_loc"].replace({
        "intronic": "intronic",
        "intron": "intronic",
        "upstream": "upstream",
        "up": "upstream"
    })

    # Optional: drop all-zero rows
    if args.drop_all_zero:
        mask_nonzero = (df[col_me1].abs() > args.zero_eps) | (df[col_ac].abs() > args.zero_eps) | (df[col_me3].abs() > args.zero_eps)
        dropped = int((~mask_nonzero).sum())
        df = df.loc[mask_nonzero].copy()
        if dropped > 0:
            print(f"[INFO] Dropped {dropped} all-zero enhancers (useful to avoid empty rows).")

    # Short labels: "CNE14 (intronic)"
    df["_short"] = df[name_col].astype(str).apply(short_enhancer_name)
    df["_label"] = df["_short"] + " (" + df["_loc"] + ")"

    # Group order
    loc_order = {"intronic": 0, "upstream": 1, "unknown": 2}
    df["_loc_order"] = df["_loc"].map(lambda x: loc_order.get(x, 2))

    # Sort within group
    sort_col = args.sort_within if args.sort_within in df.columns else col_me1
    df = df.sort_values(["_loc_order", sort_col], ascending=[True, False]).reset_index(drop=True)

    labels = df["_label"].tolist()
    me1 = df[col_me1].to_numpy()
    ac  = df[col_ac].to_numpy()
    me3 = df[col_me3].to_numpy()
    locs = df["_loc"].tolist()

    # --- y positions with extra gap between intronic/upstream groups ---
    inner_sep = args.inner_sep
    group_step = (3 * inner_sep) + args.gap_between_enhancers

    y_base = []
    y = 0.0
    prev_group = None
    for loc in locs:
        group = loc if loc in ("intronic", "upstream") else "unknown"
        if prev_group is not None and group != prev_group:
            y += args.gap_between_groups
        y_base.append(y)
        y += group_step
        prev_group = group

    y_base = np.array(y_base)
    y_me1 = y_base - inner_sep
    y_ac  = y_base
    y_me3 = y_base + inner_sep

    # Colors by mark type (keep consistent across paper)
    color_me1 = "#1f77b4"   # H3K4me1
    color_ac  = "#ff7f0e"   # H3K27ac
    color_me3 = "#2ca02c"   # H3K4me3

    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42

    n = len(df)
    fig_h = max(6.0, 0.50 * n)
    fig, ax = plt.subplots(figsize=(14, fig_h))

    ax.barh(y_me1, me1, height=args.bar_h, color=color_me1, label="H3K4me1")
    ax.barh(y_ac,  ac,  height=args.bar_h, color=color_ac,  label="H3K27ac")
    ax.barh(y_me3, me3, height=args.bar_h, color=color_me3, label="H3K4me3")

    ax.set_yticks(y_base)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()

    ax.set_xlabel("mean bigWig signal (WT hindlimb E11.5, mm9)")
    ax.set_title("Fig 2C — enhancer chromatin signatures (shared scale)")

    ax.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.5)
    ax.legend(frameon=False, loc="lower right")

    # Annotate only H3K4me3 (promoter-mark control), thresholded
    if args.annotate_me3:
        maxv = max(float(np.nanmax(me1)), float(np.nanmax(ac)), float(np.nanmax(me3)), 1e-9)
        pad = 0.01 * maxv
        for y, v in zip(y_me3, me3):
            if v >= args.annotate_min:
                ax.text(v + pad, y, f"{v:.3f}", va="center", fontsize=8)

    # More left margin for labels
    plt.tight_layout(rect=[0.22, 0.02, 0.98, 0.98])

    out_png = args.out_prefix + ".png"
    out_svg = args.out_prefix + ".svg"
    fig.savefig(out_png, dpi=args.dpi, bbox_inches="tight")
    fig.savefig(out_svg, bbox_inches="tight")
    plt.close(fig)

    print(f"[OK] Wrote:\n  {out_png}\n  {out_svg}")

if __name__ == "__main__":
    main()
