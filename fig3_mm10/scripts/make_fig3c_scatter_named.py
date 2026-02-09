import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

IN_TSV = "derived/Fig3C_data_mm10_HOXA13_HOXD13.tsv"
OUT_PNG = "outputs/panels/Fig3C_HOXA13_vs_HOXD13_scatter_mm10.png"
OUT_SVG = "outputs/panels/Fig3C_HOXA13_vs_HOXD13_scatter_mm10.svg"

# Match your enhancer colors (as in your BED track RGBs)
# upstream: 255,215,0 (gold); intronic: 144,238,144 (green)
COLORS = {
    "upstream": (255/255, 215/255,   0/255),
    "intronic": (144/255, 238/255, 144/255),
}

# Labels to show (clean, story-driven)
LABEL_PREFIXES = ("CNE14", "CNE18", "CNE19", "CNE21", "CNE13")

def main():
    df = pd.read_csv(IN_TSV, sep="\t")
    df["group"] = df["group"].astype(str).str.lower()

    xcol = "log10_1p_HOXA13"
    ycol = "log10_1p_HOXD13"

    # Figure size tuned for manuscript panel
    plt.figure(figsize=(5.2, 5.0))

    # plot each group for legend
    for grp in ["upstream", "intronic"]:
        sub = df[df["group"] == grp]
        if len(sub) == 0:
            continue
        plt.scatter(
            sub[xcol], sub[ycol],
            s=52,
            alpha=0.9,
            edgecolors="black",
            linewidths=0.4,
            label=grp,
            c=[COLORS.get(grp, (0.5,0.5,0.5))] * len(sub)
        )

    # axis labels
    plt.xlabel("log10(1 + HOXA13 mean signal)")
    plt.ylabel("log10(1 + HOXD13 mean signal)")

    # sensible padded limits
    xmin, xmax = float(df[xcol].min()), float(df[xcol].max())
    ymin, ymax = float(df[ycol].min()), float(df[ycol].max())
    padx = (xmax - xmin) * 0.07 if xmax > xmin else 0.2
    pady = (ymax - ymin) * 0.07 if ymax > ymin else 0.2
    plt.xlim(xmin - padx, xmax + padx)
    plt.ylim(ymin - pady, ymax + pady)

    # label key enhancers only
    def should_label(name: str) -> bool:
        return any(str(name).startswith(p) for p in LABEL_PREFIXES)

    for _, r in df.iterrows():
        nm = str(r["name"])
        if should_label(nm):
            plt.text(r[xcol] + 0.01, r[ycol] + 0.01, nm, fontsize=8)

    # grid and legend
    plt.grid(True, linewidth=0.4, alpha=0.35)
    plt.legend(title="enhancer class", frameon=True, fontsize=8, title_fontsize=8, loc="lower right")

    plt.tight_layout()

    Path(OUT_PNG).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_PNG, dpi=600)
    plt.savefig(OUT_SVG)
    plt.close()

    print("Wrote:", OUT_PNG)
    print("Wrote:", OUT_SVG)

if __name__ == "__main__":
    main()
