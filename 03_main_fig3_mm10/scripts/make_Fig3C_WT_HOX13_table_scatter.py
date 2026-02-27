#!/usr/bin/env python3
import os, math
import pandas as pd
import pyBigWig
import matplotlib.pyplot as plt

BASE = "/mnt/e/Amir Various research data_Oct 20th 2024/GLI3 review_Aug 2023/3D genome analysis stuff/Limbs/Publication work_june 2024/Re-Submission to Developmental Biology-Stuff/05_fig3_mm10"

BW_A = os.path.join(BASE, "raw", "HOXA13_mm10_WT_E12p5_DFL_mean.bw")
BW_D = os.path.join(BASE, "raw", "HOXD13_mm10_WT_E12p5_DFL_mean.bw")

BED_UP = os.path.join(BASE, "coords", "Gli3_enhancerBlocks_upstream.mm10.bed")
BED_IN = os.path.join(BASE, "coords", "Gli3_enhancerBlocks_intronic.mm10.bed")
BED_NAMES = os.path.join(BASE, "coords", "Gli3_named_enhancers.mm10.bed")

OUTDIR = os.path.join(BASE, "outputs")
os.makedirs(OUTDIR, exist_ok=True)

TSV_OUT  = os.path.join(OUTDIR, "Fig3C_namedEnhancers_meanHOXSignal_mm10_WT_E12p5_DFL.tsv")
PNG_OUT  = os.path.join(OUTDIR, "Fig3C_HOX_scatter_mm10_WT_E12p5_DFL_NOlabels_cleanAxes.png")
SVG_OUT  = os.path.join(OUTDIR, "Fig3C_HOX_scatter_mm10_WT_E12p5_DFL_NOlabels_cleanAxes.svg")
XLSX_OUT = os.path.join(OUTDIR, "Table_Sx_Fig3C_HOX13_binding_Gli3_mm10_WT_E12p5_DFL.xlsx")

def read_bed(bed_path: str, group: str) -> pd.DataFrame:
    rows = []
    with open(bed_path, "r") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("track"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            chrom = parts[0]
            start = int(parts[1])
            end   = int(parts[2])
            rows.append((chrom, start, end, group, end-start))
    return pd.DataFrame(rows, columns=["chrom","start","end","group","len_bp"])

def read_name_bed(bed_path: str) -> dict:
    m = {}
    with open(bed_path, "r") as f:
        for line in f:
            if not line.strip() or line.startswith("#") or line.startswith("track"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            chrom = parts[0]
            start = int(parts[1])
            end   = int(parts[2])
            name = parts[3] if len(parts) >= 4 and parts[3].strip() else f"{chrom}:{start}-{end}"
            m[(chrom,start,end)] = name
    return m

def bw_stat(bw, chrom, start, end, stat):
    v = bw.stats(chrom, start, end, type=stat, exact=True)[0]
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return 0.0
    return float(v)

def main():
    for p in [BW_A, BW_D, BED_UP, BED_IN]:
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing: {p}")

    df = pd.concat([
        read_bed(BED_UP, "upstream"),
        read_bed(BED_IN, "intronic")
    ], ignore_index=True)

    name_map = read_name_bed(BED_NAMES) if os.path.exists(BED_NAMES) else {}
    df["enhancer"] = [name_map.get((c,s,e), f"{c}:{s}-{e}") for c,s,e in df[["chrom","start","end"]].itertuples(index=False, name=None)]

    bwA = pyBigWig.open(BW_A)
    bwD = pyBigWig.open(BW_D)

    df["mean_HOXA13"] = [bw_stat(bwA,c,s,e,"mean") for c,s,e in df[["chrom","start","end"]].itertuples(index=False, name=None)]
    df["mean_HOXD13"] = [bw_stat(bwD,c,s,e,"mean") for c,s,e in df[["chrom","start","end"]].itertuples(index=False, name=None)]
    df["max_HOXA13"]  = [bw_stat(bwA,c,s,e,"max")  for c,s,e in df[["chrom","start","end"]].itertuples(index=False, name=None)]
    df["max_HOXD13"]  = [bw_stat(bwD,c,s,e,"max")  for c,s,e in df[["chrom","start","end"]].itertuples(index=False, name=None)]

    bwA.close(); bwD.close()

    df["sum_mean"] = df["mean_HOXA13"] + df["mean_HOXD13"]

    out = df[["chrom","start","end","enhancer","group","len_bp",
              "mean_HOXA13","mean_HOXD13","max_HOXA13","max_HOXD13","sum_mean"]].copy()

    out.to_csv(TSV_OUT, sep="\t", index=False)
    try:
        out.to_excel(XLSX_OUT, index=False)
    except Exception as e:
        print("Excel export warning:", e)

    out["x"] = out["mean_HOXA13"].apply(lambda v: math.log10(1.0 + v))
    out["y"] = out["mean_HOXD13"].apply(lambda v: math.log10(1.0 + v))

    plt.figure(figsize=(10,7))
    for grp, marker in [("intronic","s"), ("upstream","o")]:
        sub = out[out["group"] == grp]
        plt.scatter(sub["x"], sub["y"], marker=marker, s=220, label=grp)

    plt.title("HOX13 binding over Gli3 enhancers (mm10)")
    plt.xlabel("log10(1 + mean HOXA13)")
    plt.ylabel("log10(1 + mean HOXD13)")
    plt.legend(frameon=False)
    plt.tight_layout()

    plt.savefig(PNG_OUT, dpi=300)
    plt.savefig(SVG_OUT)

    print("Wrote TSV:", TSV_OUT)
    print("Wrote PNG:", PNG_OUT)
    print("Wrote SVG:", SVG_OUT)
    print("Wrote XLSX:", XLSX_OUT)

if __name__ == "__main__":
    main()
