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
    ap.add_argument("--sort-within", default="H3K4me1_mean", help="Sort within group by this column (desc).")
    ap.add_argument("--dpi", type=int, default=600)

    # Layout controls
    ap.add_argument("--bar-h", type=float, default=0.22)
    ap.add_argument("--inner-sep", type=float, default=0.26)
    ap.add_argument("--gap-between-enhancers", type=float, default=0.30)
    ap.add_argument("--gap-between-groups", type=float, default=0.45)  # reduced by default

    # Behavior
    ap.add_argument("--drop-all-zero", action="store_true")
    ap.add_argument("--zero-eps", type=float, default=1e-9)

    # Clean styling toggles (defaults match your request)
    ap.add_argument("--show-legend", action="store_true", help="Show legend (default: off).")
    ap.add_argument("--show-grid", action="store_true", help="Show grid lines (default: off).")
    ap.add_argument("--keep-box", action="store_true", help="Keep full box spines (default: only left+bottom).")

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

    # Coerce numeric
    for c in [col_me1, col_ac, col_me3]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    # Location: from TSV col if present else mapping file
    loc_map = load_location_map(args.loc_map)
    loc_col = guess_location_column(df)

    def get_loc(row) -> str:
        if loc_col is not None:
            v = str(row[loc_col]).strip()
            if v and v.lower() != "nan":
                return v.lower()
        return str(loc_map.get(str(row[name_col]), "unknown")).lower()

    df["_loc"] = df.apply(get_loc, axis=1)
    df["_loc"] = df["_loc"].replace({"intron":"intronic", "intronic":"intronic", "up":"upstream", "upstream":"upstream"})

    # Optional: drop all-zero rows
    if args.drop_all_zero:
        nz = (df[col_me1].abs() > args.zero_eps) | (df[col_ac].abs() > args.zero_eps) | (df[col_me3].abs() > args.zero_eps)
        df = df.loc[nz].copy()

    # Short labels
    df["_short"] = df[name_col].astype(str).apply(short_enhancer_name)
    df["_label"] = df["_short"] + " (" + df["_loc"] + ")"

    # Group order
    loc_order = {"intronic": 0, "upstream": 1, "unknown": 2}
    df["_loc_order"] = df["_loc"].map(lambda x: loc_order.get(x, 2))

    sort_col = args.sort_within if args.sort_within in df.columns else col_me1
    df = df.sort_values(["_loc_order", sort_col], ascending=[True, False]).reset_index(drop=True)

    labels = df["_label"].tolist()
    me1 = df[col_me1].to_numpy()
    ac  = df[col_ac].to_numpy()
    me3 = df[col_me3].to_numpy()
    locs = df["_loc"].tolist()

    # y positions with adjustable group gap
    inner_sep = args.inner_sep
    step = (3 * inner_sep) + args.gap_between-enhancers if False else (3 * inner_sep) + args.gap_between_enhancers

    y_base = []
    y = 0.0
    prev_group = None
    for loc in locs:
        group = loc if loc in ("intronic", "upstream") else "unknown"
        if prev_group is not None and group != prev_group:
            y += args.gap_between_groups
        y_base.append(y)
        y += step
        prev_group = group

    y_base = np.array(y_base)
    y_me1 = y_base - inner_sep
    y_ac  = y_base
    y_me3 = y_base + inner_sep

    # Colors by mark type
    color_me1 = "#1f77b4"
    color_ac  = "#ff7f0e"
    color_me3 = "#2ca02c"

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

    # Grid + legend defaults OFF (as requested)
    if args.show_grid:
        ax.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.5)

    if args.show_legend:
        ax.legend(frameon=False, loc="lower right")

    # Remove border spines except left+bottom (keep only X and Y axis lines)
    if not args.keep_box:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout(rect=[0.22, 0.02, 0.98, 0.98])

    out_png = args.out_prefix + ".png"
    out_svg = args.out_prefix + ".svg"
    fig.savefig(out_png, dpi=args.dpi, bbox_inches="tight")
    fig.savefig(out_svg, bbox_inches="tight")
    plt.close(fig)

    print(f"[OK] Wrote:\n  {out_png}\n  {out_svg}")

if __name__ == "__main__":
    main()
