#!/usr/bin/env python3
import argparse
import pandas as pd
import pyBigWig
import matplotlib.pyplot as plt

def parse_bed9(path):
    rows = []
    with open(path) as f:
        for line in f:
            if not line.strip() or line.startswith(("#","track","browser")):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            chrom = parts[0]
            start = int(parts[1])
            end = int(parts[2])
            name = parts[3]
            rgb = parts[8] if len(parts) >= 9 else ""
            # classify using itemRgb (gold vs green)
            group = "upstream"
            if "0,128,0" in rgb or "0,255,0" in rgb or "34,139,34" in rgb:
                group = "intronic"
            if "255,215,0" in rgb or "218,165,32" in rgb or "255,200,0" in rgb:
                group = "upstream"
            rows.append((chrom, start, end, name, rgb, group))
    df = pd.DataFrame(rows, columns=["chrom","start","end","name","rgb","group"])
    df["len_bp"] = df["end"] - df["start"]
    return df

def bw_mean(bw, chrom, start, end):
    val = bw.stats(chrom, start, end, type="mean")[0]
    return 0.0 if val is None else float(val)

def add_signal(df, bw_path, colname):
    bw = pyBigWig.open(bw_path)
    vals = []
    for r in df.itertuples(index=False):
        vals.append(bw_mean(bw, r.chrom, int(r.start), int(r.end)))
    bw.close()
    df[colname] = vals
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bed9", required=True)
    ap.add_argument("--h3k27ac", required=True)
    ap.add_argument("--h3k4me1", required=True)
    ap.add_argument("--h3k4me3", required=False, default=None)
    ap.add_argument("--out_prefix", required=True)
    args = ap.parse_args()

    df = parse_bed9(args.bed9)
    df = add_signal(df, args.h3k27ac, "H3K27ac_mean")
    df = add_signal(df, args.h3k4me1, "H3K4me1_mean")
    if args.h3k4me3:
        df = add_signal(df, args.h3k4me3, "H3K4me3_mean")

    # rank by H3K27ac to show "subset high"
    df = df.sort_values("H3K27ac_mean", ascending=False).reset_index(drop=True)
    out_tsv = args.out_prefix + ".tsv"
    df.to_csv(out_tsv, sep="\t", index=False)

    # plotting (compact, one panel with two stacked bars)
    colors = df["group"].map({"upstream":"#DAA520", "intronic":"#2E8B57"}).tolist()
    y = list(range(len(df)))

    fig = plt.figure(figsize=(7.2, 4.2), dpi=200)
    ax1 = fig.add_axes([0.12, 0.55, 0.83, 0.38])  # top
    ax2 = fig.add_axes([0.12, 0.10, 0.83, 0.38])  # bottom

    ax1.barh(y, df["H3K4me1_mean"], color=colors, edgecolor="none")
    ax1.set_yticks(y)
    ax1.set_yticklabels(df["name"], fontsize=7)
    ax1.invert_yaxis()
    ax1.set_xlabel("mean bigWig signal")
    ax1.set_title("H3K4me1 (WT hindlimb E11.5, mm9)", fontsize=9)

    ax2.barh(y, df["H3K27ac_mean"], color=colors, edgecolor="none")
    ax2.set_yticks(y)
    ax2.set_yticklabels([""]*len(y))
    ax2.invert_yaxis()
    ax2.set_xlabel("mean bigWig signal")
    ax2.set_title("H3K27ac (WT hindlimb E11.5, mm9)", fontsize=9)

    # small legend text
    fig.text(0.12, 0.01, "gold=upstream enhancers; green=intronic enhancers", fontsize=8)

    out_png = args.out_prefix + ".png"
    out_svg = args.out_prefix + ".svg"
    fig.savefig(out_png, bbox_inches="tight")
    fig.savefig(out_svg, bbox_inches="tight")
    print("Wrote:", out_tsv)
    print("Wrote:", out_png)
    print("Wrote:", out_svg)

if __name__ == "__main__":
    main()
