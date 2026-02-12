import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Gli3_enhancers_GLI3log2_mean.tsv", sep="\t")

# Label all (only 13 enhancers, so this is readable)
label_these = set(df["name"].tolist())

intr = df[df["group"]=="intronic"]
up   = df[df["group"]=="upstream"]

# IGV RGB colors (match your tracks)
up_color   = (255/255, 215/255, 0/255)     # gold
intr_color = (144/255, 238/255, 144/255)   # light green

plt.figure(figsize=(8.5,4.6), dpi=200)

plt.scatter(up["mid_Mb"], up["GLI3_log2_mean"], marker="s", s=95,
            label="upstream", color=up_color, edgecolor="black", linewidth=0.3)
plt.scatter(intr["mid_Mb"], intr["GLI3_log2_mean"], marker="s", s=95,
            label="intronic", color=intr_color, edgecolor="black", linewidth=0.3)

for _, r in df.iterrows():
    if r["name"] in label_these:
        plt.text(r["mid_Mb"], r["GLI3_log2_mean"], r["name"], fontsize=9,
                 ha="left", va="bottom")

plt.xlabel("chr13 position (Mb, mm10)")
plt.ylabel("GLI3 enrichment (mean log2[ChIP/Input])")
plt.legend(frameon=False, loc="upper left")

# Tight y-axis for your data (so it doesn't look empty)
ymin = min(df["GLI3_log2_mean"].min() - 0.03, -0.05)
ymax = df["GLI3_log2_mean"].max() + 0.05
plt.ylim(ymin, ymax)

plt.tight_layout()
plt.savefig("SuppFig_Gli3_binding_PanelC.svg")
plt.savefig("SuppFig_Gli3_binding_PanelC.png", dpi=600)

print("Saved: SuppFig_Gli3_binding_PanelC.svg and .png")
print(f"Y-range used: {ymin:.3f} to {ymax:.3f}")
