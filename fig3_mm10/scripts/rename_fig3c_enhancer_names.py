import pandas as pd
from pathlib import Path
import shutil

BASE = Path(".")
IN_TSV  = BASE / "derived" / "Fig3C_data_mm10_HOXA13_HOXD13.tsv"
MAP_BED = BASE / "coords" / "Gli3_named_enhancers.mm10.bed"   # confirmed exists in your coords listing
OUT_TSV = BASE / "derived" / "Fig3C_data_mm10_HOXA13_HOXD13.tsv"          # overwrite (with backup)
OUT_NAMED = BASE / "derived" / "Fig3C_data_mm10_HOXA13_HOXD13.named.tsv"  # extra copy

def read_bed9_skip_track(path: Path) -> pd.DataFrame:
    # BED9-ish: chrom start end name score strand thickStart thickEnd itemRgb
    rows = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("track", "browser", "#")):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            rows.append(parts[:4])  # chrom,start,end,name
    df = pd.DataFrame(rows, columns=["chrom","start","end","true_name"])
    df["start"] = pd.to_numeric(df["start"], errors="coerce").astype("Int64")
    df["end"]   = pd.to_numeric(df["end"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["start","end"])
    # de-dup keys if any (shouldn't happen)
    df = df.drop_duplicates(subset=["chrom","start","end"], keep="first")
    return df

def main():
    if not IN_TSV.exists():
        raise FileNotFoundError(f"Missing input TSV: {IN_TSV}")
    if not MAP_BED.exists():
        raise FileNotFoundError(f"Missing mapping BED: {MAP_BED}")

    df = pd.read_csv(IN_TSV, sep="\t")
    m  = read_bed9_skip_track(MAP_BED)

    # Ensure numeric types for join
    df["start"] = pd.to_numeric(df["start"], errors="coerce").astype("Int64")
    df["end"]   = pd.to_numeric(df["end"], errors="coerce").astype("Int64")

    # Keep old names
    if "name_old" not in df.columns:
        df["name_old"] = df["name"]

    merged = df.merge(m, on=["chrom","start","end"], how="left")

    # Replace only where mapping exists
    merged["name"] = merged["true_name"].fillna(merged["name"])
    merged = merged.drop(columns=["true_name"])

    # Report mapping success
    n_total = len(merged)
    n_mapped = (merged["name"] != merged["name_old"]).sum()
    n_unmapped = n_total - n_mapped
    print(f"Total rows: {n_total}")
    print(f"Mapped (name replaced): {n_mapped}")
    print(f"Unmapped (kept original): {n_unmapped}")

    if n_unmapped > 0:
        print("\nUnmapped rows (showing chrom/start/end/name_old):")
        print(merged.loc[merged["name"] == merged["name_old"], ["chrom","start","end","name_old"]].to_string(index=False))

    # Backup and write
    bak = OUT_TSV.with_suffix(OUT_TSV.suffix + ".bak")
    shutil.copy2(IN_TSV, bak)

    merged.to_csv(OUT_TSV, sep="\t", index=False)
    merged.to_csv(OUT_NAMED, sep="\t", index=False)

    print(f"\nBackup saved: {bak}")
    print(f"Updated TSV written: {OUT_TSV}")
    print(f"Also written: {OUT_NAMED}")

if __name__ == "__main__":
    main()
