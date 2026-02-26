#!/usr/bin/env python3
import re
from pathlib import Path
from datetime import date
import numpy as np
import pandas as pd

ROOT = Path("/mnt/e/Amir Various research data_Oct 20th 2024/GLI3 review_Aug 2023/3D genome analysis stuff/Limbs/Publication work_june 2024/Re-Submission to Developmental Biology-Stuff/05_phase1_enhancer_prioritization_TableS5")

manifest = pd.read_csv(ROOT / "shared_metadata/phase1_tf_manifest.tsv", sep="\t")
enh = pd.read_csv(ROOT / "shared_metadata/enhancers_13_master_mm10.tsv", sep="\t")

# -----------------------------
# 1) Collect quant files
# -----------------------------
quant_files = sorted(list((ROOT/"p300/quant").glob("*.tsv")) +
                     list((ROOT/"PITX1/quant").glob("*.tsv")) +
                     list((ROOT/"HAND2/quant").glob("*.tsv")))

rows = []
for f in quant_files:
    m = re.match(r"(.+)\.(mm9|mm10)\.bigWigAverageOverBed\.tsv$", f.name)
    if not m:
        print(f"[WARN] Skipping unrecognized quant filename: {f.name}")
        continue
    dataset_label = m.group(1)
    genome_build_quant = m.group(2)

    df = pd.read_csv(f, sep="\t", header=None,
                     names=["enhancer_id","size","covered","sum","mean0","mean"])
    df["dataset_label"] = dataset_label
    df["genome_build_quant"] = genome_build_quant
    df["quant_file"] = f.name
    rows.append(df)

if not rows:
    raise SystemExit("No quant files found.")

q = pd.concat(rows, ignore_index=True)

# Join manifest
q = q.merge(manifest, on="dataset_label", how="left", validate="many_to_one")

# Basic checks
missing_meta = q["factor"].isna()
if missing_meta.any():
    print("[WARN] Some quant files did not match manifest rows:")
    print(q.loc[missing_meta, ["quant_file","dataset_label"]].drop_duplicates().to_string(index=False))

# Save raw combined long table
tables_dir = ROOT / "tables"
tables_dir.mkdir(exist_ok=True, parents=True)
q.to_csv(tables_dir / "quant_enhancer_signal_long_phase1.tsv", sep="\t", index=False)

# -----------------------------
# 2) Dataset-level ranks/percentiles
# -----------------------------
def add_rank_percentiles(df):
    df = df.copy()
    n = df["enhancer_id"].nunique()
    df["rank_desc_mean0"] = df["mean0"].rank(method="average", ascending=False)
    if n > 1:
        df["percentile_rank"] = (n - df["rank_desc_mean0"]) / (n - 1)
    else:
        df["percentile_rank"] = np.nan
    return df

q_ranked = q.groupby("dataset_label", group_keys=False).apply(add_rank_percentiles)
q_ranked.to_csv(tables_dir / "quant_enhancer_signal_dataset_ranked_phase1.tsv", sep="\t", index=False)

# -----------------------------
# 3) Factor-level aggregation using score datasets only
# -----------------------------
q_score = q_ranked[q_ranked["preferred_use"] == "score"].copy()

# Normalize factor names for stable column naming
q_score["factor_norm"] = q_score["factor"].str.strip().str.lower()

factor_agg = (
    q_score.groupby(["enhancer_id","factor_norm"], as_index=False)
    .agg(
        signal_mean0_agg=("mean0","median"),
        factor_percentile=("percentile_rank","median"),
        n_datasets=("dataset_label","nunique"),
        datasets_used=("dataset_label", lambda x: ";".join(sorted(set(map(str, x)))))
    )
)

# factor rank (1 = strongest within factor)
factor_agg["factor_rank"] = factor_agg.groupby("factor_norm")["factor_percentile"].rank(method="average", ascending=False)

# support flag (top ~1/3)
factor_agg["support_flag"] = (factor_agg["factor_percentile"] >= 0.67).astype(int)

factor_agg.to_csv(tables_dir / "factor_level_aggregates_phase1.tsv", sep="\t", index=False)

# -----------------------------
# 4) Pivot factor-level metrics to wide
# -----------------------------
wide = enh.copy()

# Ensure enhancer order retained if present
order_col = "display_order" if "display_order" in wide.columns else None

for fac in ["p300","pitx1","hand2"]:
    tmp = factor_agg[factor_agg["factor_norm"] == fac].copy()
    if tmp.empty:
        continue
    tmp = tmp[["enhancer_id","datasets_used","signal_mean0_agg","factor_rank","factor_percentile","support_flag"]].rename(columns={
        "datasets_used": f"{fac}_datasets_used",
        "signal_mean0_agg": f"{fac}_signal_mean0_agg",
        "factor_rank": f"{fac}_rank",
        "factor_percentile": f"{fac}_percentile",
        "support_flag": f"{fac}_support_flag",
    })
    wide = wide.merge(tmp, on="enhancer_id", how="left")

# Add factor-level QC notes (same repeated note across rows for transparency)
wide["p300_qc_note"] = "Single E11.5 limb p300 processed WIG (mm9) used for scoring"
wide["hand2_qc_note"] = "WT + 3xF score; reprocessed 3xF retained as descriptive-only (sparser)"
wide["pitx1_qc_note"] = "Rep1 + Rep2 E11.5 hindlimb PITX1 tracks aggregated by median percentile"

# -----------------------------
# 5) Composite prioritization metrics
# -----------------------------
factor_percentile_cols = [c for c in ["p300_percentile","pitx1_percentile","hand2_percentile"] if c in wide.columns]
support_cols = [c for c in ["p300_support_flag","pitx1_support_flag","hand2_support_flag"] if c in wide.columns]

wide["n_factors_measured"] = wide[factor_percentile_cols].notna().sum(axis=1)
wide["n_factors_included_in_scoring"] = wide["n_factors_measured"]
wide["n_factors_supported"] = wide[support_cols].fillna(0).sum(axis=1).astype(int)

wide["mean_factor_percentile"] = wide[factor_percentile_cols].mean(axis=1, skipna=True)
wide["support_breadth_fraction"] = np.where(
    wide["n_factors_included_in_scoring"] > 0,
    wide["n_factors_supported"] / wide["n_factors_included_in_scoring"],
    np.nan
)

wide["composite_priority_score"] = 0.75 * wide["mean_factor_percentile"] + 0.25 * wide["support_breadth_fraction"]

# rank overall (1 = highest)
wide["priority_rank_overall"] = wide["composite_priority_score"].rank(method="average", ascending=False)

def assign_tier(row):
    s = row["composite_priority_score"]
    n_sup = row["n_factors_supported"]
    if pd.isna(s):
        return "NA"
    if (s >= 0.70) and (n_sup >= 2):
        return "Tier A"
    elif (s >= 0.45) or (n_sup >= 1):
        return "Tier B"
    else:
        return "Tier C"

wide["priority_tier"] = wide.apply(assign_tier, axis=1)

# -----------------------------
# 6) Conservative interpretation notes (especially requested enhancers)
# -----------------------------
def interp_note(enh_id):
    if enh_id == "CNE14_hs1586_mm1977":
        return "Consistent multi-factor occupancy support across available bulk datasets; high prioritization support."
    if enh_id == "CNE19":
        return "PITX1-supported with limited p300/HAND2 bulk occupancy in available datasets; factor-specific support pattern."
    if enh_id == "mm1179":
        return "Low bulk occupancy across available datasets; modest signal does not exclude genetic relevance or context-specific activity."
    return ""

wide["interpretation_note"] = wide["enhancer_id"].map(interp_note).fillna("")

# provenance
wide["scoring_version"] = "phase1_rank_v1_0"
wide["analysis_date"] = str(date.today())
wide["table_build_note"] = "Primary enhancer coordinates mm10; quantification performed on mm9 processed tracks using mm10->mm9 lifted enhancer BED"

# optional sort by display_order
if order_col:
    wide = wide.sort_values(order_col).reset_index(drop=True)

# -----------------------------
# 7) Output draft Table S5 + root copy
# -----------------------------
# Column order (close to planned schema)
col_order = [
    "enhancer_id","enhancer_label","enhancer_group","chr_mm10","start_mm10","end_mm10","length_bp","display_order",

    "p300_datasets_used","p300_signal_mean0_agg","p300_rank","p300_percentile","p300_support_flag","p300_qc_note",
    "hand2_datasets_used","hand2_signal_mean0_agg","hand2_rank","hand2_percentile","hand2_support_flag","hand2_qc_note",
    "pitx1_datasets_used","pitx1_signal_mean0_agg","pitx1_rank","pitx1_percentile","pitx1_support_flag","pitx1_qc_note",

    "n_factors_measured","n_factors_included_in_scoring","n_factors_supported",
    "mean_factor_percentile","support_breadth_fraction","composite_priority_score",
    "priority_rank_overall","priority_tier","interpretation_note",

    "scoring_version","analysis_date","table_build_note"
]
# keep only existing + append any extras
existing = [c for c in col_order if c in wide.columns]
extras = [c for c in wide.columns if c not in existing]
wide = wide[existing + extras]

draft_path = tables_dir / "Table_S5_phase1_enhancer_prioritization_DRAFT.tsv"
wide.to_csv(draft_path, sep="\t", index=False)

# Also copy to root placeholder name (still draft content for now)
root_copy = ROOT / "Table_S5_phase1_enhancer_prioritization_FINAL.tsv"
wide.to_csv(root_copy, sep="\t", index=False)

print(f"Wrote: {draft_path}")
print(f"Wrote: {root_copy}")
print("\nTop rows by composite priority:")
print(wide.sort_values('composite_priority_score', ascending=False)[[
    'enhancer_id','p300_percentile','hand2_percentile','pitx1_percentile',
    'n_factors_supported','composite_priority_score','priority_tier'
]].to_string(index=False))
