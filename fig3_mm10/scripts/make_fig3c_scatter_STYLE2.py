import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

IN_TSV = "derived/Fig3C_data_mm10_HOXA13_HOXD13.tsv"
OUT_PNG = "outputs/panels/Fig3C_scatter_mm10_STYLE2_v1.png"
OUT_SVG = "outputs/panels/Fig3C_scatter_mm10_STYLE2_v1.svg"

def main():
    df = pd.read_csv(IN_TSV, sep="\t")
    df["group"] = df["group"].astype(str).str.lower()

    xcol = "log10_1p_HOXA13"
    ycol = "log10_1p_HOXD13"

    # STYLE2 look: clean axes, no grid, no outer box
    fig, ax = plt.subplots(figsize=(7.2, 5.6))

    # Colors to match your "style2" example (blue + orange)
    # (Change if you want your gold/green instead)
    color_intronic = "#1f77b4"  # blue
    color_upstream = "#ff7f0e"  # orange

    # 1) square markers for ALL points (no outlines)
    #    (If you later want intronic squares + upstream circles, tell me)
    for grp, col in [("intronic", color_intronic), ("upstream", color_upstream)]:
        sub = df[df["group"] == grp]
        if len(sub) == 0:
            continue
        ax.scatter(
            sub[xcol], sub[ycol],
            s=260,                 # big markers like your style2
            marker="s",            # squares
            c=col,
            edgecolors="none",     # 4) no black outline
            linewidths=0,
            label=grp,
            zorder=3
        )

    # Title + axis labels (match your style2 wording)
    ax.set_title("HOX13 binding over Gli3 enhancers (mm10)", pad=14)
    ax.set_xlabel("log10(1 + mean HOXA13)")
    ax.set_ylabel("log10(1 + mean HOXD13)")

    # 3) only x and y axis lines: hide top/right spines; no grid
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)

    # 2) legend top-left with NO title (keep the intronic/upstream text like your style2)
    ax.legend(loc="upper left", frameon=False, title=None, fontsize=12)

    # (Optional) add a little padding so points aren't on edges
    xmin, xmax = float(df[xcol].min()), float(df[xcol].max())
    ymin, ymax = float(df[ycol].min()), float(df[ycol].max())
    padx = (xmax - xmin) * 0.18 if xmax > xmin else 0.2
    pady = (ymax - ymin) * 0.18 if ymax > ymin else 0.2
    ax.set_xlim(xmin - padx, xmax + padx)
    ax.set_ylim(ymin - pady, ymax + pady)

    fig.tight_layout()

    Path(OUT_PNG).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=600)
    fig.savefig(OUT_SVG)
    plt.close(fig)

    print("Wrote:", OUT_PNG)
    print("Wrote:", OUT_SVG)

if __name__ == "__main__":
    main()
