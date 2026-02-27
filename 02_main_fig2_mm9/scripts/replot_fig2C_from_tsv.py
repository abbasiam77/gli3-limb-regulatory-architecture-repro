import argparse
import pandas as pd
import matplotlib.pyplot as plt

def rgb_to_mpl(rgb_str: str):
    r,g,b = [int(x) for x in rgb_str.split(",")]
    return (r/255.0, g/255.0, b/255.0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", required=True)
    ap.add_argument("--out_prefix", required=True)
    ap.add_argument("--sort_by", default="H3K4me1_mean",
                    choices=["H3K4me1_mean","H3K27ac_mean","H3K4me3_mean","name"])
    args = ap.parse_args()

    df = pd.read_csv(args.tsv, sep="\t")
    # ensure expected columns
    for c in ["name","rgb","H3K4me1_mean","H3K27ac_mean","H3K4me3_mean"]:
        if c not in df.columns:
            raise SystemExit(f"Missing column: {c}")

    # sort
    if args.sort_by == "name":
        df = df.sort_values("name")
    else:
        df = df.sort_values(args.sort_by, ascending=False)

    colors = [rgb_to_mpl(x) for x in df["rgb"].astype(str)]
    y = range(len(df))

    fig, axes = plt.subplots(2, 1, figsize=(13, 8), dpi=150)

    axes[0].barh(y, df["H3K4me1_mean"], color=colors)
    axes[0].set_yticks(list(y))
    axes[0].set_yticklabels(df["name"])
    axes[0].invert_yaxis()
    axes[0].set_title("H3K4me1 (WT hindlimb E11.5, mm9)")
    axes[0].set_xlabel("mean bigWig signal")

    axes[1].barh(y, df["H3K27ac_mean"], color=colors)
    axes[1].set_yticks(list(y))
    axes[1].set_yticklabels([""]*len(df))  # keep labels only once (top)
    axes[1].invert_yaxis()
    axes[1].set_title("H3K27ac (WT hindlimb E11.5, mm9)")
    axes[1].set_xlabel("mean bigWig signal")

    fig.tight_layout()
    fig.savefig(args.out_prefix + ".png")
    fig.savefig(args.out_prefix + ".svg")

if __name__ == "__main__":
    main()
