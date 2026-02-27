import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

IN_TSV = "derived/Fig3C_data_mm10_HOXA13_HOXD13.tsv"
OUT_PNG = "outputs/panels/Fig3C_scatter_mm10_NOLABELS_v1.png"
OUT_SVG = "outputs/panels/Fig3C_scatter_mm10_NOLABELS_v1.svg"

# Exact RGBs from your BED tracks:
# upstream: 255,215,0 (gold); intronic: 144,238,144 (green)
COLORS = {
    "upstream": (255/255, 215/255,   0/255),
    "intronic": (144/255, 238/255, 144/255),
}

def main():
    df = pd.read_csv(IN_TSV, sep="\t")
    df["group"] = df["group"].astype(str).str.lower()

    xcol = "log10_1p_HOXA13"
    ycol = "log10_1p_HOXD13"

    # Match your "good" plot look (circles, black edge, grid, legend lower-right)
    plt.figure(figsize=(6.0, 5.4))

    for grp in ["upstream", "intronic"]:
        sub = df[df["group"] == grp]
        if len(sub) == 0:
            continue
        plt.scatter(
            sub[xcol], sub[ycol],
            s=60,
            alpha=0.9,
            edgecolors="black",
            linewidths=0.4,
            label=grp,
            c=[COLORS.get(grp, (0.5, 0.5, 0.5))] * len(sub),
            zorder=2
        )

    plt.xlabel("log10(1 + HOXA13 mean signal)")
    plt.ylabel("log10(1 + HOXD13 mean signal)")

    # Keep the same padded limits so points/legend match the good version
    xmin, xmax = float(df[xcol].min()), float(df[xcol].max())
    ymin, ymax = float(df[ycol].min()), float(df[ycol].max())
    padx = (xmax - xmin) * 0.18 if xmax > xmin else 0.30
    pady = (ymax - ymin) * 0.14 if ymax > ymin else 0.30
    plt.xlim(xmin - padx, xmax + padx)
    plt.ylim(ymin - pady, ymax + pady)

    plt.grid(True, linewidth=0.4, alpha=0.35)
    plt.legend(title="enhancer class", frameon=True, fontsize=9, title_fontsize=9, loc="lower right")

    plt.tight_layout()

    Path(OUT_PNG).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_PNG, dpi=600)
    plt.savefig(OUT_SVG)
    plt.close()

    print("Wrote:", OUT_PNG)
    print("Wrote:", OUT_SVG)

if __name__ == "__main__":
    main()
