import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

input_xlsx = "04_tables/Supplementary Tables.xlsx"
sheet_name = "S6a"

out_png = "05_figures/Supplementary_Figure_S3/Supplementary_Figure_S3_limb_vs_non_limb_summary.png"
out_pdf = "05_figures/Supplementary_Figure_S3/Supplementary_Figure_S3_limb_vs_non_limb_summary.pdf"
out_tsv = "05_figures/Supplementary_Figure_S3/Supplementary_Figure_S3_plotting_data.tsv"

# Read formatted S6a robustly
raw = pd.read_excel(input_xlsx, sheet_name=sheet_name, header=None)

header_idx = None
for i in range(len(raw)):
    row_values = [str(x).strip() for x in raw.iloc[i].tolist()]
    if "enhancer_id" in row_values and "class" in row_values:
        header_idx = i
        break

if header_idx is None:
    raise RuntimeError("Could not find S6a table header row.")

df = pd.read_excel(input_xlsx, sheet_name=sheet_name, header=header_idx)
df = df[df["class"].isin(["limb", "non_limb"])].copy()

needed = [
    "enhancer_id",
    "class",
    "HOX13_sum_mean0",
    "active_enhancer_score_H3K4me1_plus_H3K27ac",
    "GLI3_mean0",
    "PITX1_mean0_average_HL1_HL2"
]

missing = [c for c in needed if c not in df.columns]
if missing:
    raise ValueError(f"Missing expected columns in S6a: {missing}")

df = df[needed].copy()

for c in needed[2:]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df.to_csv(out_tsv, sep="\t", index=False)

class_order = ["limb", "non_limb"]

panels = [
    (
        "HOX13_sum_mean0",
        "A. HOX13 combined signal",
        "HOXA13 mean + HOXD13 mean"
    ),
    (
        "active_enhancer_score_H3K4me1_plus_H3K27ac",
        "B. Active enhancer score",
        "H3K4me1 mean + H3K27ac mean"
    ),
    (
        "GLI3_mean0",
        "C. GLI3 signal",
        "GLI3 mean signal"
    ),
    (
        "PITX1_mean0_average_HL1_HL2",
        "D. PITX1 average signal",
        "Mean PITX1 signal"
    )
]

fig, axes = plt.subplots(2, 2, figsize=(9.2, 7.6), dpi=600)
axes = axes.flatten()

rng = np.random.default_rng(42)

for ax, (col, title, ylabel) in zip(axes, panels):
    values_by_class = [
        df.loc[df["class"] == cls, col].dropna().values
        for cls in class_order
    ]

    bp = ax.boxplot(
        values_by_class,
        positions=[1, 2],
        widths=0.52,
        patch_artist=True,
        showfliers=False
    )

    for patch in bp["boxes"]:
        patch.set_facecolor("white")
        patch.set_edgecolor("black")
        patch.set_linewidth(1.0)

    for key in ["whiskers", "caps", "medians"]:
        for item in bp[key]:
            item.set_color("black")
            item.set_linewidth(1.0)

    for i, cls in enumerate(class_order, start=1):
        y = df.loc[df["class"] == cls, col].dropna().values
        x = rng.normal(i, 0.055, size=len(y))
        ax.scatter(x, y, s=24, alpha=0.75)

    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Limb\n(n=13)", "Non-limb\n(n=41)"])
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=10)
    ax.tick_params(axis="both", labelsize=9, length=3, width=0.8)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)

fig.tight_layout()
fig.savefig(out_png, dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")

print("Header row detected at Excel row:", header_idx + 1)
print("Data rows used:", len(df))
print("Class counts:")
print(df["class"].value_counts())

print("\nSaved:")
print(out_png)
print(out_pdf)
print(out_tsv)

print("\n===== Data summary =====")
for col, _, _ in panels:
    print(f"\n--- {col} ---")
    print(df.groupby("class")[col].describe())
