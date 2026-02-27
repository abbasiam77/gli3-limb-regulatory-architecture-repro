import pandas as pd

# enhancer BED with group (we already generated it)
bed = pd.read_csv(
    "Gli3_named_enhancers.mm10.with_group.bed",
    sep="\t",
    header=None,
    names=["chrom","start","end","name","group"]
)

# deepTools raw counts table: contains a non-comment line ("Number of bins found: 13")
rows = []
with open("Gli3_log2_over_enhancers.tab", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("Number of bins found"):
            continue
        if line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 4:
            continue
        chrom, start, end, val = parts
        rows.append((chrom, int(start), int(end), float(val)))

raw = pd.DataFrame(rows, columns=["chrom","start","end","GLI3_log2_mean"])

df = bed.merge(raw, on=["chrom","start","end"], how="left")
df["mid_bp"] = (df["start"] + df["end"]) / 2
df["mid_Mb"] = df["mid_bp"] / 1e6
df = df.sort_values(["chrom","mid_bp"]).reset_index(drop=True)

df.to_csv("Gli3_enhancers_GLI3log2_mean.tsv", sep="\t", index=False)

print("Wrote: Gli3_enhancers_GLI3log2_mean.tsv")
print(df[["name","group","GLI3_log2_mean","mid_Mb"]].to_string(index=False))
print("Missing values:", df["GLI3_log2_mean"].isna().sum())
