# GLI3 limb manuscript resubmission — Phase 1 enhancer prioritization extension (Supplementary Table S5)

## Project context and scope

This folder documents the **Phase 1 enhancer-prioritization extension** added to the GLI3 limb manuscript resubmission (*Developmental Biology*). The aim of this phase was to generate a **new occupancy-supported prioritization layer** for the same 13 named Gli3 locus enhancers already used in the HOX13 and GLI3 enhancer-wise quantification analyses.

### Manuscript supplement logic (recommended structure)
- **Table S2**: HOXA13/HOXD13 enhancer-wise quantification (source table)
- **Table S3**: GLI3 enhancer-wise quantification (source table)
- **Table S5**: p300/HAND2/PITX1 prioritization extension (this folder/workflow)
- **Optional Table S6**: integrated prioritization summary across all factors (future)

### Phase 1 objective (this workflow)
Generate **Supplementary Table S5** using enhancer-wise occupancy signals from:
- **p300**
- **HAND2**
- **PITX1**

with:
- mm10 enhancer reference set (13 enhancers),
- mm10→mm9 liftOver for quantification on mm9 tracks,
- enhancer-wise signal extraction (`bigWigAverageOverBed`),
- rank-based cross-dataset integration,
- conservative, non-causal prioritization tiers.

> **Interpretation principle**: This is an **occupancy/support/prioritization** layer only. It is not used to claim direct enhancer function or causality.

---

## Computational platform and environment

### Platform
- **Windows host + WSL Ubuntu** (user standard workflow)
- Working path (WSL view of `E:` drive):
  - `/mnt/e/Amir Various research data_Oct 20th 2024/GLI3 review_Aug 2023/3D genome analysis stuff/Limbs/Publication work_june 2024/Re-Submission to Developmental Biology-Stuff/05_phase1_enhancer_prioritization_TableS5`

### Core tools used
- `bash`, `awk`, `wget`, `tar`, `gunzip`, `find`, `md5sum`
- **UCSC tools** (installed in `/home/amir/bin/ucsc`):
  - `liftOver`
  - `wigToBigWig`
  - `bigWigAverageOverBed`
  - `fetchChromSizes`
- `python3`
- Python package(s):
  - `pandas`
  - `numpy`

### Important conversion detail (WIG → bigWig)
Some GEO WIG files contained entries extending slightly beyond chromosome ends (common for binned WIG tracks near contig boundaries). Conversion therefore used:
- removal of `track` / `browser` header lines, and
- `wigToBigWig -clip`

Warnings were expected and conversion was considered successful if the `.bw` file was created.

---

## Folder organization (Phase 1 workspace)

### Root folder
`05_phase1_enhancer_prioritization_TableS5/`

### Shared folders
- `scripts/` — scripts and shell helpers used in the workflow
- `shared_metadata/` — enhancer master table, manifests, checksums, UCSC helper files
- `shared_beds/` — frozen enhancer BEDs (mm10 primary and mm9 lifted)
- `shared_qc/` — QC summaries (e.g., track consistency correlations)
- `tables/` — intermediate and draft output tables
- `docs/` — notes/checklists/documentation
- `logs/` — download/conversion logs
- `tmp/` — temporary files (WIG cleaning/conversion scratch)

### Factor-specific folders
For each of `p300/`, `HAND2/`, `PITX1/`:
- `metadata/`
- `raw/`
- `tracks/mm9`, `tracks/mm10`
- `peaks/mm9`, `peaks/mm10`
- `beds/mm9`, `beds/mm10`, `beds/liftover`
- `quant/`
- `qc/`
- `logs/`
- `tmp/`

---

## Enhancer reference set used in Table S5

### Source of the 13 named enhancer set (mm10)
The 13-enhancer reference set for Table S5 was derived from the existing **Fig3 mm10 named enhancer file**:
- `05_fig3_mm10/coords/Gli3_named_enhancers.mm10.bed`

This file included a UCSC `track` header line and BED9-style fields. For Phase 1, the file was converted into a clean BED4 file by:
- removing `track`/`browser` lines,
- retaining columns 1–4 (`chr`, `start`, `end`, `enhancer_id`),
- preserving enhancer order.

### Frozen mm10 enhancer BED for Phase 1
- `shared_beds/enhancers_13_mm10.bed`

### Validation performed (frozen set)
- **13 rows**
- **4 columns per row**
- **13 unique enhancer IDs**
- Coordinate sanity (`start < end`)

### Ordered enhancer IDs used throughout S5
1. `mm2080`
2. `mm2176`
3. `mm1859`
4. `mm2164`
5. `mm1887`
6. `mm1179`
7. `mm1889`
8. `CNE14_hs1586_mm1977`
9. `mm2018`
10. `CNE18`
11. `CNE19`
12. `CNE21`
13. `CNE13`

### Enhancer freeze integrity files
- `shared_metadata/enhancers_13_master_mm10.tsv`
- `shared_metadata/enhancer_ids_13_ordered.txt`
- `shared_metadata/enhancer_set_checksums.md5`

---

## Data sources, accessions, developmental stages, and databases

### Databases used
- **NCBI GEO** (sample/series supplementary files)
- **NCBI FTP GEO supplementary directories** (WIG/BED/TAR downloads)
- **UCSC** (liftOver chain, chrom sizes, utilities)

### Factor datasets included in Table S5 workflow

#### 1) p300 (scoring dataset)
- **Database**: GEO
- **Series accession**: **GSE13845**
- **Sample accession**: **GSM348066**
- **Run accession**: **SRX002661** (recorded in manifest)
- **Data type used**: GEO supplementary processed **WIG** (converted to bigWig) + peaks BED
- **Genome build**: **mm9**
- **Biological context**: embryonic limb
- **Embryonic stage**: **E11.5**
- **Notes**: Single processed p300 weighted-coverage track used for scoring

#### 2) PITX1 (scoring datasets; two replicates)
- **Database**: GEO
- **Series accession**: **GSE41591**
- **Sample accession (Rep1)**: **GSM1019784** (PITX1 ChIP)
- **Sample accession (Rep2)**: **GSM1019786** (PITX1 ChIP)
- **Controls**: **GSM1019785**, **GSM1019787** (inputs)
- **Run accessions** (manifest): **SRX195355**, **SRX195357**
- **Data type used**: GEO supplementary processed **WIG** (converted to bigWig) + peaks BED
- **Genome build**: **mm9**
- **Biological context**: embryonic **hindlimb bud**
- **Embryonic stage**: **E11.5**
- **Genotype**: WT
- **Notes**: Rep1 and Rep2 aggregated at factor level (median percentile)

#### 3) HAND2 (two scoring tracks + one descriptive/sensitivity track)
- **Database**: GEO
- **Series accession**: **GSE55707**
- **Download route**: `GSE55707_RAW.tar` (series tar contained processed WIGs)
- **Track/sample files extracted**:
  - **GSM1342122** — HAND2 limb WT WIG (**score**)
  - **GSM1342121** — HAND2 limb 3xF WIG (**score**)
  - **GSM1447340** — HAND2 limb 3xF reprocessed WIG (`...mm9...`) (**descriptive_only**)
- **Input tracks extracted for provenance/QC**:
  - **GSM1342124** — Input WT
  - **GSM1342123** — Input 3xF
  - **GSM1447341** — Input 3xF reprocessed
- **Data type used**: processed WIG (converted to bigWig)
- **Genome build**: **mm9** (explicitly indicated in reprocessed filename; working assumption for series WIGs validated by chromosome naming and compatibility)
- **Biological context**: embryonic limb bud
- **Embryonic stage (reported context)**: **E10.5**
- **Notes**:
  - WT + 3xF used in primary HAND2 factor scoring aggregation
  - reprocessed 3xF track retained as **descriptive/sensitivity** due sparse dynamic range and higher zero count across the 13 enhancers

---

## Reproducible workflow summary (download → quantification → ranking → S5)

### 1) Workspace initialization and templates
Created root/factor folder structure and templates:
- `scripts/env_phase1.sh`
- `README.md` (this file; updated final documentation)
- `shared_metadata/phase1_tf_manifest.tsv` and candidate manifest
- `shared_metadata/enhancers_13_master_mm10.tsv` (template, later auto-populated)
- `shared_beds/enhancers_13_mm10.bed` (frozen enhancer BED)

### 2) Enhancer set freezing (mm10)
- Selected `Gli3_named_enhancers.mm10.bed` from existing Fig3 mm10 work
- Removed UCSC track header
- Kept BED4
- Validated 13 rows / 13 unique IDs / coordinate sanity
- Generated:
  - `shared_metadata/enhancers_13_master_mm10.tsv`
  - `shared_metadata/enhancer_ids_13_ordered.txt`
  - `shared_metadata/enhancer_set_checksums.md5`

### 3) Data download and organization
Processed-first strategy used.

#### p300 downloads
- `p300/tracks/mm9/GSM348066_p300_wiggle.mm9.wig.gz`
- `p300/peaks/mm9/GSM348066_p300_peaks.mm9.bed.gz`
- optional provenance/raw files:
  - `p300/raw/GSM348066_p300_aligned.txt.gz`
  - `p300/raw/GSE13845_RAW.tar`

#### PITX1 downloads
- `PITX1/tracks/mm9/GSM1019784_hl1_pitx1_chip.mm9.wig.gz`
- `PITX1/tracks/mm9/GSM1019786_hl2_pitx1_chip.mm9.wig.gz`
- peaks:
  - `GSM1019784_hl1_pitx1_peaks.mm9.bed.gz`
  - `GSM1019784_top_pitx1_peaks.mm9.bed.gz`
  - `GSM1019786_hl2_pitx1_peaks.mm9.bed.gz`
- optional provenance/raw:
  - `PITX1/raw/GSE41591_RAW.tar`

#### HAND2 downloads and extraction
- Downloaded:
  - `HAND2/raw/GSE55707_RAW.tar`
- Inspected tar contents and found processed WIG tracks
- Extracted and renamed key tracks into `HAND2/tracks/mm9/`
- Extracted input tracks into `HAND2/raw/inputs/`

### 4) UCSC helper files and tools
Installed/used:
- `liftOver`
- `wigToBigWig`
- `bigWigAverageOverBed`
- `fetchChromSizes`

Created UCSC helper files in:
- `shared_metadata/ucsc/mm10ToMm9.over.chain.gz`
- `shared_metadata/ucsc/mm9.chrom.sizes`

### 5) mm10 → mm9 enhancer liftOver for quantification
Primary enhancer reference remained **mm10**, but quantification was performed on **mm9** tracks.

Generated:
- `shared_beds/enhancers_13_from_mm10_to_mm9.bed`
- `shared_beds/enhancers_13_from_mm10_to_mm9.unmapped.bed`

Copied mm9 BED into factor folders:
- `p300/beds/mm9/enhancers_13_mm9_from_mm10.bed`
- `PITX1/beds/mm9/enhancers_13_mm9_from_mm10.bed`
- `HAND2/beds/mm9/enhancers_13_mm9_from_mm10.bed`

### 6) WIG → bigWig conversion (processed tracks)
For each WIG file:
1. decompressed with `gunzip -c`
2. stripped `track`/`browser` lines with `awk`
3. converted with `wigToBigWig -clip`
4. logged warnings (expected for end-of-chromosome overhanging bins in some GEO WIGs)

Generated `.bw` tracks under each factor `tracks/mm9/` folder.

### 7) Enhancer-wise signal quantification
Used:
- `bigWigAverageOverBed`

Inputs:
- bigWig signal track (`*.bw`)
- lifted enhancer BED (`enhancers_13_from_mm10_to_mm9.bed`)

Outputs:
- per-track quant files in each factor `quant/` folder
- columns (UCSC standard):
  - `name` (enhancer_id)
  - `size`
  - `covered`
  - `sum`
  - `mean0`
  - `mean`

**Primary metric used for scoring**: `mean0`

### 8) QC and exploratory checks
Generated/used QC summaries for:
- dataset-level enhancer-wise signal distribution
- zero-counts across 13 enhancers
- PITX1 replicate consistency
- HAND2 track consistency (WT vs 3xF vs reprocessed 3xF)

The observed QC pattern supported proceeding with S5, including:
- strong multi-factor support at **CNE14/hs1586** and **CNE18**,
- PITX1-biased support at **CNE19**,
- low bulk occupancy for **mm1179** in available datasets.

### 9) Rank-based scoring and Table S5 construction
Implemented in Python script:
- `scripts/build_table_s5_phase1_from_quant.py`

Core steps:
1. Parse all `bigWigAverageOverBed` outputs
2. Join curated manifest (`shared_metadata/phase1_tf_manifest.tsv`)
3. Compute **within-dataset enhancer ranks** by descending `mean0`
4. Convert to **percentile ranks** (0–1 scale)
5. Aggregate percentiles at factor level (median across scoring datasets per factor)
6. Create factor support flags (`percentile >= 0.67`)
7. Compute composite prioritization score
8. Assign tiers (A/B/C)
9. Write draft and root-copy Table S5 TSVs

---

## Scoring framework used for Table S5 (Phase 1)

### Why rank-based integration?
Raw ChIP-seq track values are not directly comparable across:
- factor datasets,
- replicates/processing pipelines,
- developmental stages,
- track generation methods.

Therefore, cross-factor integration used **rank percentiles**, not raw signal magnitudes.

### Dataset-level ranking
For each track, the 13 enhancers were ranked by descending `mean0`.
Percentile rank was computed (highest = 1.0, lowest = 0.0; ties handled with average ranks).

### Factor-level aggregation
- **p300**: single scoring dataset
- **PITX1**: Rep1 + Rep2 aggregated by median percentile
- **HAND2**: WT + 3xF aggregated by median percentile
- **HAND2 3xF reprocessed**: `descriptive_only` (not included in primary factor scoring)

### Support flag
Per factor:
- `support_flag = 1` if factor percentile ≥ **0.67** (top ~1/3 of 13 enhancers)
- else `0`

### Composite prioritization score
- `mean_factor_percentile` = mean of p300/HAND2/PITX1 factor percentiles
- `support_breadth_fraction` = proportion of factors with support flag = 1
- `composite_priority_score = 0.75 * mean_factor_percentile + 0.25 * support_breadth_fraction`

### Tier definitions
- **Tier A**: `composite_priority_score >= 0.70` **and** `n_factors_supported >= 2`
- **Tier B**: intermediate support (score ≥ 0.45 or at least one factor support)
- **Tier C**: lower occupancy support across available bulk datasets

---

## Scripts and command files used (workflow provenance)

### Core scripts/helpers created in this workspace
- `scripts/env_phase1.sh` — exports `BASE`, `ROOT`, `P300`, `HAND2`, `PITX1`
- `scripts/download_phase1_candidates.sh` — initial processed-first download helper (p300/PITX1 + HAND2 tar)
- `scripts/build_table_s5_phase1_from_quant.py` — parses quant outputs and builds Table S5 draft/final TSV

### Additional QC / helper scripts used during development
(Depending on final cleanup, these may exist as scripts or as terminal one-liners recorded in shell history/logs)
- WIG→bigWig conversion helpers (`wigToBigWig -clip` workflow)
- QC summaries of `bigWigAverageOverBed` outputs
- track consistency correlation calculations (PITX1, HAND2)

### Logs generated
- `logs/download_history_phase1.log`
- `logs/wig_to_bigwig_phase1.log` (and per-track wigToBigWig stderr logs where used)
- `HAND2/logs/GSE55707_RAW_contents.txt` (tar contents inventory)

---

## Key intermediate and final output files

### Intermediate quantification and scoring tables (`tables/`)
- `tables/quant_enhancer_signal_long_phase1.tsv`
- `tables/quant_enhancer_signal_dataset_ranked_phase1.tsv`
- `tables/factor_level_aggregates_phase1.tsv`
- `tables/Table_S5_phase1_enhancer_prioritization_DRAFT.tsv`
- `tables/Table_S5_phase1_enhancer_prioritization_DRAFT_v1.tsv` (if frozen copy created)
- `tables/Table_S5_phase1_priority_summary_compact.tsv` (compact review table)

### Root-level TSV copy used for manuscript workflow convenience
- `Table_S5_phase1_enhancer_prioritization_FINAL.tsv`

> Note: the root filename may contain a draft-equivalent snapshot during iterative work. Keep a versioned draft copy in `tables/` for reproducibility.

### Final manuscript-facing Excel table (Supplementary Table S5)
- `Supplementary_Table_S5.xlsx` (final reformatted version with footnotes on same sheet; stage details included)

Formatting details of final Excel version:
- title and subtitle rows included
- footnotes placed **on the same sheet** beneath the main table
- explicit embryonic stage notes included for each factor dataset group
- empty “overall rank” column removed

---

## Biological interpretation notes (important for manuscript consistency)

This table provides an **occupancy-supported prioritization layer** and should be interpreted conservatively.

### Examples relevant to manuscript discussion
- **CNE14_hs1586_mm1977**: strong multi-factor support across available bulk datasets; high prioritization support
- **CNE19**: PITX1-associated support with limited p300/HAND2 bulk occupancy in available datasets (factor-specific support pattern)
- **mm1179**: low bulk occupancy across available datasets; this does **not** exclude genetic relevance or context-specific activity

### Why modest bulk ChIP signal may occur at relevant enhancers
- developmental stage mismatch
- limb tissue heterogeneity
- focal occupancy diluted across full enhancer interval
- context-specific or transient occupancy

---

## Reproducibility and GitHub push guidance

### Recommended GitHub destination
- Repository: **`abbasiam77/gli3-limb-fig1-repro`**

### Suggested files to include (push)
Include:
- `README.md` (this file)
- `scripts/` (especially `env_phase1.sh`, `build_table_s5_phase1_from_quant.py`, and finalized helper scripts)
- `shared_metadata/` (manifests, enhancer master table, checksums, UCSC helper metadata if desired)
- `shared_beds/` (frozen mm10 and lifted mm9 BEDs)
- `tables/` (intermediate and draft TSVs)
- `shared_qc/` (QC summaries/correlations)
- final `Supplementary_Table_S5.xlsx`
- root-level final TSV copy (optional convenience)

Avoid (or LFS if needed):
- large raw tar files (`GSE*.tar`)
- large WIG/BW files
- temporary conversion files

### Existing `.gitignore`
A local `.gitignore` was added to avoid accidental commits of raw FASTQ/BAM/WIG/bigWig and temp files.

### Example push workflow (adapt as needed)
```bash
cd "/mnt/e/.../Re-Submission to Developmental Biology-Stuff/05_phase1_enhancer_prioritization_TableS5"

# (Optional) copy/rsync selected reproducibility files into your fig1 repo subfolder
# rsync -av --exclude 'raw/' --exclude 'tracks/' --exclude 'tmp/' ./ /path/to/gli3-limb-fig1-repro/phase1_tableS5/

cd /path/to/gli3-limb-fig1-repro
git status
git add .
git commit -m "Add Phase 1 p300/HAND2/PITX1 enhancer prioritization workflow and final Supplementary Table S5"
git push
```

---

## Future extension (optional, not part of current S5)
A future **integrated synthesis table** (optional **Table S6**) can combine:
- HOXA13/HOXD13 summary metrics from **S2**,
- GLI3 summary metrics from **S3**,
- p300/HAND2/PITX1 support from **S5**,

while retaining S2/S3/S5 as non-redundant source/extension tables.

---

## Contact / ownership (project context)
This Phase 1 workflow and S5 prioritization layer were developed as part of the GLI3 limb manuscript resubmission reproducibility pipeline under the broader architecture-first, integrative quantitative framing of the manuscript.

