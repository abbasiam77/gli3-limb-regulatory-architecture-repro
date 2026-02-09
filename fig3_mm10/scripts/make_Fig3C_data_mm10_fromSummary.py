import pandas as pd
import numpy as np

bed5_path  = "derived/enhancers_merged.mm10.chr.sorted.bed"
hoxa_path  = "derived/HOXA13_bwSummary1.tsv"
hoxd_path  = "derived/HOXD13_bwSummary1.tsv"
out_path   = "derived/Fig3C_data_mm10_HOXA13_HOXD13.tsv"

bed = pd.read_csv(bed5_path, sep="\t", header=None, names=["chrom","start","end","name","group"])
bed["len_bp"] = bed["end"] - bed["start"]

hoxa = pd.read_csv(hoxa_path, sep="\t")
hoxd = pd.read_csv(hoxd_path, sep="\t")

hoxa = hoxa.rename(columns={"mean":"HOXA13_mean_summary", "status":"HOXA13_status"})
hoxd = hoxd.rename(columns={"mean":"HOXD13_mean_summary", "status":"HOXD13_status"})

df = bed.merge(hoxa[["name","HOXA13_mean_summary","HOXA13_status"]], on="name", how="left") \
        .merge(hoxd[["name","HOXD13_mean_summary","HOXD13_status"]], on="name", how="left")

# Ensure numeric; treat NA/ERR as 0 for plotting (but keep status columns)
df["HOXA13_mean_summary"] = pd.to_numeric(df["HOXA13_mean_summary"], errors="coerce").fillna(0.0)
df["HOXD13_mean_summary"] = pd.to_numeric(df["HOXD13_mean_summary"], errors="coerce").fillna(0.0)

# log transform (what you wanted for Fig3C)
df["log10_1p_HOXA13"] = np.log10(1.0 + df["HOXA13_mean_summary"])
df["log10_1p_HOXD13"] = np.log10(1.0 + df["HOXD13_mean_summary"])

# Combined score for ranking
df["sum_mean"] = df["HOXA13_mean_summary"] + df["HOXD13_mean_summary"]

df = df.sort_values(["sum_mean","HOXA13_mean_summary","HOXD13_mean_summary"], ascending=False)

df.to_csv(out_path, sep="\t", index=False)

print("Wrote:", out_path)
print("Rows:", len(df))
print("HOXA ERR count:", int((df["HOXA13_status"]=="ERR").sum()))
print("HOXD ERR count:", int((df["HOXD13_status"]=="ERR").sum()))
print("Top 5 (name, group, HOXA, HOXD, sum):")
print(df[["name","group","HOXA13_mean_summary","HOXD13_mean_summary","sum_mean"]].head(5).to_string(index=False))
