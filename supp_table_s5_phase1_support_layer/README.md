# Supplementary Table S5 (Phase 1 support-layer extension) reproducibility module

## Purpose
This module contains the reproducibility assets for **Supplementary Table S5**, which provides a **support-layer / prioritization extension** using p300, HAND2, and PITX1 datasets across the GLI3 enhancer set.

## Framing (important)
This module supports the manuscript's **architecture-first, quantitative, and conservative** interpretation.
It is used as an **extension support layer** and is **not** intended to replace the main source quantification tables.

- **S2** = HOX13 quantification source table
- **S3** = GLI3 quantification source table
- **S5** = p300/HAND2/PITX1 extension support-layer table
- No integrated “master prioritization” table is introduced here (no S6 at this stage)

## Contents overview
This module includes:
- final S5 exports (`.xlsx`, final `.tsv`)
- factor-specific subfolders (`p300/`, `HAND2/`, `PITX1/`) containing BEDs, metadata, peaks/quantification outputs
- shared enhancer BEDs and shared metadata
- QC summaries
- scripts used for download, track conversion, and S5 table construction
- intermediate/supporting tables retained for provenance

## Folder guide
- `scripts/` — build/download/conversion scripts for the Phase 1 workflow
- `p300/`, `HAND2/`, `PITX1/` — factor-specific inputs/metadata/quantification assets
- `shared_beds/` — frozen enhancer BEDs (mm10 and lifted mm9 variants used in workflow)
- `shared_metadata/` — enhancer manifests, checksums, UCSC chain/sizes, workflow manifests
- `shared_qc/` — QC summaries (e.g., track consistency)
- `tables/` — intermediate and draft/supporting tables retained for provenance
- top-level `Supplementary_Table_S5.xlsx` and final TSV — final deliverables

## Notes
This module has been reorganized for reviewer-facing clarity while preserving existing factor-level organization and file paths used during analysis.
